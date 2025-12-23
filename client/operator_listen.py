import bpy
import socket
import json
import logging
from mathutils import Quaternion, Vector

# Setup logging
logger = logging.getLogger(__name__)

class GestureNav_OT_Start(bpy.types.Operator):
    """Start the GestureNav UDP Listener"""
    bl_idname = "gesturenav.start"
    bl_label = "Start Listener"
    
    _timer = None
    _sock = None
    _last_zoom = None
    
    # Sensitivities
    ORBIT_SENSITIVITY = 0.05
    ZOOM_SENSITIVITY = 10.0
    
    def modal(self, context, event):
        scene = context.scene
        
        # Check if we should stop
        if not scene.gesturenav_listening:
            return self.cancel(context)
            
        if event.type == 'TIMER':
            try:
                data, addr = self._sock.recvfrom(1024)
                message = data.decode('utf-8')
                try:
                    payload = json.loads(message)
                    
                    if payload.get('state') == 'active':
                        self.process_navigation(context, payload)
                    else:
                        self._last_zoom = None
                        
                except json.JSONDecodeError:
                    print(f"[GestureNav] Malformed JSON: {message}")
            except BlockingIOError:
                pass
            except Exception as e:
                print(f"[GestureNav] Error: {e}")
                
        return {'PASS_THROUGH'}
        
    def find_view3d(self, context):
        # Helper to find the 3D View area/region
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        space = area.spaces.active
                        if space.type == 'VIEW_3D': 
                             return area, region, space.region_3d
        return None, None, None

    def process_navigation(self, context, payload):
        # Try current context first
        area = context.area
        region = context.region
        r3d = context.region_data

        # Fallback: Search for the first 3D View
        if not r3d or area.type != 'VIEW_3D':
             area, region, r3d = self.find_view3d(context)
        
        if not r3d:
            return

        # 1. ORBIT (Joystick Logic)
        # Receive smoothed/processed velocity from server
        ox = payload.get('x', 0.0)
        oy = payload.get('y', 0.0)
        
        if ox != 0 or oy != 0:
            # Server already handled deadzone and sensitivity
            # ox, oy are now "Velocity" values
            
            # Apply Rotation
            rot_x = Quaternion((1, 0, 0), -oy * self.ORBIT_SENSITIVITY)
            rot_z = Quaternion((0, 0, 1), -ox * self.ORBIT_SENSITIVITY)
            
            r3d.view_rotation = r3d.view_rotation @ rot_z @ rot_x
            
            if area: 
                area.tag_redraw()

        # 2. ZOOM (Discrete Logic)
        # zoom is now -1 (Out), 0 (Idle), 1 (In)
        zoom_state = payload.get('zoom', 0)
        
        if zoom_state != 0:
            # Zoom In (1) -> Decrease Distance
            # Zoom Out (-1) -> Increase Distance
            step = 0.1 * self.ZOOM_SENSITIVITY 
            
            # If Zoom In (1): subtract step
            # If Zoom Out (-1): add step
            # -1 * 1 * step = -step (In) ??? Wait.
            # Zoom In (1) -> decrease distance.  distance -= 1 * step. Correct.
            # Zoom Out (-1) -> increase distance. distance -= -1 * step = +step. Correct.
            
            r3d.view_distance -= zoom_state * step
            
            if area: area.tag_redraw()

    def invoke(self, context, event):
        scene = context.scene
        if scene.gesturenav_listening:
            return {'FINISHED'}

        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.bind(('127.0.0.1', 5555))
            self._sock.setblocking(False)
            print("[GestureNav] Socket bound to 127.0.0.1:5555")
        except OSError as e:
            self.report({'ERROR'}, f"Socket Error: {e}")
            return {'CANCELLED'}

        scene.gesturenav_listening = True
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.016, window=context.window)
        wm.modal_handler_add(self)
        
        print("[GestureNav] Listener Started")
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        if self._timer:
            wm.event_timer_remove(self._timer)
        if self._sock:
            self._sock.close()
            self._sock = None
        context.scene.gesturenav_listening = False
        print("[GestureNav] Listener Stopped")
        return {'FINISHED'}

class GestureNav_OT_Stop(bpy.types.Operator):
    """Stop the GestureNav UDP Listener"""
    bl_idname = "gesturenav.stop"
    bl_label = "Stop Listener"
    
    def execute(self, context):
        context.scene.gesturenav_listening = False
        print("[GestureNav] Stop Signal Sent")
        return {'FINISHED'}
