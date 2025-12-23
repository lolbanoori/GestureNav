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
    
    # State for Smoothing (EMA)
    _current_speed_x = 0.0
    _current_speed_y = 0.0
    
    # Constants
    ALPHA = 0.1  # Smoothing factor (Lower = Smoother)
    
    def modal(self, context, event):
        scene = context.scene
        
        if not scene.gesturenav_listening:
            return self.cancel(context)
            
        if event.type == 'TIMER':
            try:
                data, addr = self._sock.recvfrom(1024)
                message = data.decode('utf-8')
                try:
                    payload = json.loads(message)
                    # print(f"Recv: {payload}") 
                    
                    if payload.get('state') == 'active':
                        self.process_navigation(context, payload)
                    else:
                        # Decay speed to 0 if hand is lost
                        self.process_navigation(context, {'x': 0.0, 'y': 0.0, 'zoom': 0})
                        
                except json.JSONDecodeError:
                    print(f"[GestureNav] Malformed JSON: {message}")
            except BlockingIOError:
                # Still process navigation to handle smoothing decay even if no new packet
                pass
            except Exception as e:
                print(f"[GestureNav] Error: {e}")
                
        return {'PASS_THROUGH'}
        
    def find_view3d(self, context):
        for area in context.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return area, region
        return None, None

    def run_ops(self, op, override, **kwargs):
        """Execute a bpy.ops operator with context override safely across Blender versions."""
        if hasattr(bpy.context, "temp_override"):
            # Blender 3.2+
            try:
                with bpy.context.temp_override(**override):
                    op(**kwargs)
            except Exception as e:
                print(f"[GestureNav] Op Error (New API): {e}")
        else:
            # Blender < 3.2
            try:
                op(override, **kwargs)
            except Exception as e:
                print(f"[GestureNav] Op Error (Legacy API): {e}")

    def process_navigation(self, context, payload):
        # 1. State Update (EMA Smoothing)
        target_x = payload.get('x', 0.0)
        target_y = payload.get('y', 0.0)
        
        # Formula: current = (target * alpha) + (current * (1 - alpha))
        self._current_speed_x = (target_x * self.ALPHA) + (self._current_speed_x * (1.0 - self.ALPHA))
        self._current_speed_y = (target_y * self.ALPHA) + (self._current_speed_y * (1.0 - self.ALPHA))
        
        # 2. Context Setup
        area = context.area
        region = context.region
        
        if not area or area.type != 'VIEW_3D':
            area, region = self.find_view3d(context)
            
        if not area:
            return
            
        # Context Override for bpy.ops
        # Note: 'window' and 'screen' are usually required for temp_override
        override = {
            'window': context.window,
            'screen': context.screen,
            'area': area,
            'region': region,
            'scene': context.scene,
        }
        
        # 3. Apply Orbit
        if abs(self._current_speed_x) > 0.001:
            self.run_ops(bpy.ops.view3d.view_orbit, override, angle=-self._current_speed_x, type='ORBITRIGHT')

        if abs(self._current_speed_y) > 0.001:
            self.run_ops(bpy.ops.view3d.view_orbit, override, angle=self._current_speed_y, type='ORBITUP')
                
        # 4. Apply Zoom
        zoom_state = payload.get('zoom', 0)
        if zoom_state != 0:
            self.run_ops(bpy.ops.view3d.zoom, override, delta=int(zoom_state))

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
        
        # Reset state
        self._current_speed_x = 0.0
        self._current_speed_y = 0.0
        
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
