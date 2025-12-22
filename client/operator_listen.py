import bpy
import socket
import json
import logging

# Setup logging
logger = logging.getLogger(__name__)

class GestureNav_OT_Listen(bpy.types.Operator):
    """GestureNav UDP Listener"""
    bl_idname = "gesturenav.listen"
    bl_label = "GestureNav Listener"
    
    action: bpy.props.StringProperty(name="Action", default="START")
    
    _timer = None
    _sock = None
    
    def modal(self, context, event):
        scene = context.scene
        
        # Check if we should stop
        if not scene.gesturenav_listening:
            return self.cancel(context)
            
        if event.type == 'TIMER':
            try:
                # Attempt to receive data
                data, addr = self._sock.recvfrom(1024)
                message = data.decode('utf-8')
                
                # Parse JSON
                try:
                    payload = json.loads(message)
                    print(f"[GestureNav] Received: {payload}")
                except json.JSONDecodeError:
                    print(f"[GestureNav] Received malformed JSON: {message}")
                    
            except BlockingIOError:
                # No data waiting, this is expected
                pass
            except socket.error as e:
                print(f"[GestureNav] Socket error: {e}")
            except Exception as e:
                print(f"[GestureNav] Unexpected error: {e}")
                
        return {'PASS_THROUGH'}

    def execute(self, context):
        if self.action == "START":
            return self.invoke(context, None)
        elif self.action == "STOP":
            context.scene.gesturenav_listening = False
            return {'FINISHED'}
        return {'CANCELLED'}

    def invoke(self, context, event):
        scene = context.scene
        
        if scene.gesturenav_listening:
             return {'FINISHED'}

        # Setup Socket
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.bind(('127.0.0.1', 5555))
            self._sock.setblocking(False)
            print("[GestureNav] Socket bound to 127.0.0.1:5555")
        except OSError as e:
            self.report({'ERROR'}, f"Could not bind to port 5555: {e}")
            return {'CANCELLED'}

        # Start Modal
        scene.gesturenav_listening = True
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.016, window=context.window) # ~60fps
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
