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
                    # Payload: {'state': '...', 'orbit_x': float, 'orbit_y': float, 'zoom_dist': float}
                    
                    if payload.get('state') == 'active':
                        self.process_navigation(context, payload)
                    else:
                        # Reset Zoom tracker if hand is lost/idle so we don't jump on re-entry
                        self._last_zoom = None
                        
                except json.JSONDecodeError:
                    print(f"[GestureNav] Malformed JSON: {message}")
            except BlockingIOError:
                pass
            except Exception as e:
                print(f"[GestureNav] Error: {e}")
                
        return {'PASS_THROUGH'}
        
    def process_navigation(self, context, payload):
        region = context.region
        r3d = context.region_data
        
        if not r3d:
            return

        # 1. ORBIT (Joystick Logic)
        # orbit_x/y are offsets from center (-0.5 to 0.5)
        # Standard Joystick: Value = Speed
        ox = payload.get('orbit_x', 0.0)
        oy = payload.get('orbit_y', 0.0)
        
        if ox != 0 or oy != 0:
            # Create rotation quaternions
            # Up/Down maps to local X axis
            # Left/Right maps to local Z (View) or Global Z? Usually Orbit is Global Z + Local X
            
            # Simple Orbit: Modify the view_rotation quaternion
            # Note: Blender View Rotation is usually "inverted" camera rotation.
            
            # Horizontal Orbit (Global Z execution usually preferred, but simple Local Y is okay for now)
            # Letting Blender handle the "Turntable" vs "Trackball" math is hard manually.
            # We will apply local relative rotation.
            
            # Pitch (Up/Down) -> X Axis
            rot_x = Quaternion((1, 0, 0), -oy * self.ORBIT_SENSITIVITY)
            # Yaw (Left/Right) -> Z Axis
            rot_z = Quaternion((0, 0, 1), -ox * self.ORBIT_SENSITIVITY)
            
            # Apply to current rotation
            r3d.view_rotation = r3d.view_rotation @ rot_z @ rot_x

        # 2. ZOOM (Delta Logic)
        zoom_dist = payload.get('zoom_dist', 0.0)
        
        if self._last_zoom is not None:
            delta = zoom_dist - self._last_zoom
            
            # Threshold to prevent micro-jitter
            if abs(delta) > 0.002: 
                # Zoom In (Smaller Distance) -> Decrease View Distance
                # Zoom Out (Larger Distance) -> Increase View Distance
                
                # Check user manual: "Pinch In (Tips touching) -> Zoom In."
                # Tips touching = Small Distance. 
                # So if Distance Decreases (Negative Delta), we want to Zoom In (Decrease View Distance).
                
                # r3d.view_distance is the distance from the pivot interaction point.
                # Decrease = Closer.
                
                # Apply
                r3d.view_distance -= delta * self.ZOOM_SENSITIVITY
                
        self._last_zoom = zoom_dist

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
