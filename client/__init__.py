bl_info = {
    "name": "GestureNav Client",
    "author": "Antigravity",
    "version": (1, 2),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GestureNav",
    "description": "UDP Client for GestureNav Vision Server",
    "category": "3D View",
}

import bpy
import socket
import json
from .operator_listen import GestureNav_OT_Start, GestureNav_OT_Stop

# Config Sender Helper
def send_config(self, context):
    """Sends current scene properties to the Python Server via UDP Port 5556."""
    scene = context.scene
    
    # Bundle Settings
    config = {
        'deadzone_radius': scene.gesturenav_deadzone_radius,
        'deadzone_offset_x': scene.gesturenav_deadzone_x,
        'deadzone_offset_y': scene.gesturenav_deadzone_y,
        'zoom_thresh_in': scene.gesturenav_zoom_thresh_in,
        'zoom_thresh_out': scene.gesturenav_zoom_thresh_out,
        'orbit_sens_server': scene.gesturenav_orbit_sens_server,
        'use_fist_safety': scene.gesturenav_use_fist_safety,
        'use_open_hand_safety': scene.gesturenav_use_open_hand_safety
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(config).encode('utf-8'), ("127.0.0.1", 5556))
        # print(f"Sent Config: {config}")
    except Exception as e:
        print(f"Config Send Error: {e}")

class GESTURENAV_PT_Panel(bpy.types.Panel):
    """Creates a Panel in the 3D View Sidebar"""
    bl_label = "GestureNav"
    bl_idname = "GESTURENAV_PT_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GestureNav"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Status / Main Control
        box = layout.box()
        if scene.gesturenav_listening:
            box.operator("gesturenav.stop", text="Stop Listener", icon='CANCEL')
            box.label(text="Status: Listening...", icon='REC')
        else:
            box.operator("gesturenav.start", text="Start Listener", icon='PLAY')
            box.label(text="Status: Idle", icon='PAUSE')
            
        # Settings
        layout.separator()
        layout.label(text="Tuning (Real-time)", icon='PREFERENCES')
        
        # Deadzone
        box = layout.box()
        box.label(text="Orbit Deadzone")
        box.prop(scene, "gesturenav_deadzone_radius", text="Size")
        row = box.row(align=True)
        row.prop(scene, "gesturenav_deadzone_x", text="X Pos")
        row.prop(scene, "gesturenav_deadzone_y", text="Y Pos")
        
        # Sensitivity
        box = layout.box()
        box.label(text="Sensitivity")
        box.prop(scene, "gesturenav_orbit_sensitivity", text="Orbit Speed (Client)")
        box.prop(scene, "gesturenav_zoom_sensitivity", text="Zoom Speed (Client)")
        box.prop(scene, "gesturenav_orbit_sens_server", text="Response Curve (Server)")
        
        # Zoom Thresholds
        box = layout.box()
        box.label(text="Zoom Triggers")
        box.prop(scene, "gesturenav_zoom_thresh_in", text="Pinch In <")
        box.prop(scene, "gesturenav_zoom_thresh_out", text="Pinch Out >")
        
        # Safety
        box = layout.box()
        box.label(text="Safety Locks")
        box.prop(scene, "gesturenav_use_fist_safety", text="Fist Locks Zoom")
        box.prop(scene, "gesturenav_use_open_hand_safety", text="Open Hand Locks Orbit")

def register():
    bpy.utils.register_class(GESTURENAV_PT_Panel)
    bpy.utils.register_class(GestureNav_OT_Start)
    bpy.utils.register_class(GestureNav_OT_Stop)
    
    # Internal State
    bpy.types.Scene.gesturenav_listening = bpy.props.BoolProperty(
        name="Listening", default=False
    )
    
    # Config Properties (Callback triggers UDP send)
    # Deadzone
    bpy.types.Scene.gesturenav_deadzone_radius = bpy.props.FloatProperty(
        name="Deadzone Radius", default=0.12, min=0.01, max=0.5, update=send_config
    )
    bpy.types.Scene.gesturenav_deadzone_x = bpy.props.FloatProperty(
        name="Deadzone X", default=0.75, min=0.0, max=1.0, update=send_config
    )
    bpy.types.Scene.gesturenav_deadzone_y = bpy.props.FloatProperty(
        name="Deadzone Y", default=0.6, min=0.0, max=1.0, update=send_config
    )
    
    # Sensitivity (Client-side props don't need to send to server, but uniformity is nice. 
    # Actually Orbit Sens Server DOES need to send.)
    bpy.types.Scene.gesturenav_orbit_sensitivity = bpy.props.FloatProperty(
        name="Orbit Sensitivity", default=0.02, min=0.001, max=0.2
    )
    bpy.types.Scene.gesturenav_zoom_sensitivity = bpy.props.FloatProperty(
        name="Zoom Sensitivity", default=2.0, min=0.1, max=10.0
    )
    bpy.types.Scene.gesturenav_orbit_sens_server = bpy.props.FloatProperty(
        name="Orbit Curve", default=3.0, min=1.0, max=10.0, update=send_config
    )
    
    # Zoom Thresholds
    bpy.types.Scene.gesturenav_zoom_thresh_in = bpy.props.FloatProperty(
        name="Zoom In Threshold", default=0.05, min=0.01, max=0.2, update=send_config
    )
    bpy.types.Scene.gesturenav_zoom_thresh_out = bpy.props.FloatProperty(
        name="Zoom Out Threshold", default=0.15, min=0.05, max=0.5, update=send_config
    )
    
    # Safety
    bpy.types.Scene.gesturenav_use_fist_safety = bpy.props.BoolProperty(
        name="Fist Safety", default=True, update=send_config
    )
    bpy.types.Scene.gesturenav_use_open_hand_safety = bpy.props.BoolProperty(
        name="Open Hand Safety", default=False, update=send_config
    )

def unregister():
    bpy.utils.unregister_class(GESTURENAV_PT_Panel)
    bpy.utils.unregister_class(GestureNav_OT_Start)
    bpy.utils.unregister_class(GestureNav_OT_Stop)
    
    del bpy.types.Scene.gesturenav_listening
    del bpy.types.Scene.gesturenav_deadzone_radius
    del bpy.types.Scene.gesturenav_deadzone_x
    del bpy.types.Scene.gesturenav_deadzone_y
    del bpy.types.Scene.gesturenav_orbit_sensitivity
    del bpy.types.Scene.gesturenav_zoom_sensitivity
    del bpy.types.Scene.gesturenav_orbit_sens_server
    del bpy.types.Scene.gesturenav_zoom_thresh_in
    del bpy.types.Scene.gesturenav_zoom_thresh_out
    del bpy.types.Scene.gesturenav_use_fist_safety
    del bpy.types.Scene.gesturenav_use_open_hand_safety

if __name__ == "__main__":
    register()
