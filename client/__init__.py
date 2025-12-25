bl_info = {
    "name": "GestureNav Client",
    "author": "Zohair Banoori",
    "version": (1, 5),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GestureNav",
    "description": "UDP Client for GestureNav Vision Server",
    "category": "3D View",
}

import bpy
import socket
import json
import os
from .operator_listen import GestureNav_OT_Start, GestureNav_OT_Stop

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".gesturenav_config.json")

# Config Sender Helper
def send_config(self, context=None):
    """Sends current scene properties to the Python Server via UDP Port 5556."""
    if context is None:
        context = bpy.context
        
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
    except Exception as e:
        print(f"Config Send Error: {e}")

class GestureNav_OT_Preset(bpy.types.Operator):
    """Apply a Handedness Preset"""
    bl_idname = "gesturenav.preset"
    bl_label = "Apply Preset"
    
    side: bpy.props.EnumProperty(
        items=[('RIGHT', "Right Handed", ""), ('LEFT', "Left Handed", "")]
    )
    
    def execute(self, context):
        if self.side == 'RIGHT':
            context.scene.gesturenav_deadzone_x = 0.70
        else:
            context.scene.gesturenav_deadzone_x = 0.30
            
        send_config(self, context)
        self.report({'INFO'}, f"Applied {self.side} Handed Preset")
        return {'FINISHED'}

class GestureNav_OT_Reset(bpy.types.Operator):
    """Reset All Settings to default"""
    bl_idname = "gesturenav.reset"
    bl_label = "Reset Settings"
    
    def execute(self, context):
        s = context.scene
        s.gesturenav_deadzone_radius = 0.12
        s.gesturenav_deadzone_x = 0.70 # Default Right
        s.gesturenav_deadzone_y = 0.6
        s.gesturenav_orbit_sensitivity = 0.02
        s.gesturenav_zoom_sensitivity = 2.0
        s.gesturenav_orbit_sens_server = 3.0
        s.gesturenav_zoom_thresh_in = 0.05
        s.gesturenav_zoom_thresh_out = 0.15
        s.gesturenav_use_fist_safety = True
        s.gesturenav_use_open_hand_safety = False
        
        send_config(self, context)
        self.report({'INFO'}, "Settings Reset")
        return {'FINISHED'}

class GestureNav_OT_SaveSettings(bpy.types.Operator):
    """Save current settings to disk"""
    bl_idname = "gesturenav.save"
    bl_label = "Save Config"
    
    def execute(self, context):
        s = context.scene
        data = {
            'deadzone_radius': s.gesturenav_deadzone_radius,
            'deadzone_x': s.gesturenav_deadzone_x,
            'deadzone_y': s.gesturenav_deadzone_y,
            'orbit_sensitivity': s.gesturenav_orbit_sensitivity,
            'zoom_sensitivity': s.gesturenav_zoom_sensitivity,
            'orbit_sens_server': s.gesturenav_orbit_sens_server,
            'zoom_thresh_in': s.gesturenav_zoom_thresh_in,
            'zoom_thresh_out': s.gesturenav_zoom_thresh_out,
            'use_fist_safety': s.gesturenav_use_fist_safety,
            'use_open_hand_safety': s.gesturenav_use_open_hand_safety
        }
        
        try:
            with open(CONFIG_PATH, 'w') as f:
                json.dump(data, f, indent=4)
            self.report({'INFO'}, f"Saved to {CONFIG_PATH}")
        except Exception as e:
            self.report({'ERROR'}, f"Save Failed: {e}")
            
        return {'FINISHED'}

class GestureNav_OT_LoadSettings(bpy.types.Operator):
    """Load settings from disk"""
    bl_idname = "gesturenav.load"
    bl_label = "Load Config"
    
    def execute(self, context):
        if not os.path.exists(CONFIG_PATH):
            self.report({'WARNING'}, "No config file found.")
            return {'CANCELLED'}
            
        try:
            with open(CONFIG_PATH, 'r') as f:
                data = json.load(f)
                
            s = context.scene
            # Safely set props if keys exist
            if 'deadzone_radius' in data: s.gesturenav_deadzone_radius = data['deadzone_radius']
            if 'deadzone_x' in data: s.gesturenav_deadzone_x = data['deadzone_x']
            if 'deadzone_y' in data: s.gesturenav_deadzone_y = data['deadzone_y']
            if 'orbit_sensitivity' in data: s.gesturenav_orbit_sensitivity = data['orbit_sensitivity']
            if 'zoom_sensitivity' in data: s.gesturenav_zoom_sensitivity = data['zoom_sensitivity']
            if 'orbit_sens_server' in data: s.gesturenav_orbit_sens_server = data['orbit_sens_server']
            if 'zoom_thresh_in' in data: s.gesturenav_zoom_thresh_in = data['zoom_thresh_in']
            if 'zoom_thresh_out' in data: s.gesturenav_zoom_thresh_out = data['zoom_thresh_out']
            if 'use_fist_safety' in data: s.gesturenav_use_fist_safety = data['use_fist_safety']
            if 'use_open_hand_safety' in data: s.gesturenav_use_open_hand_safety = data['use_open_hand_safety']
            
            send_config(self, context)
            self.report({'INFO'}, "Settings Loaded")
        except Exception as e:
            self.report({'ERROR'}, f"Load Failed: {e}")
            
        return {'FINISHED'}

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
            
        # Presets & Management
        layout.separator()
        layout.label(text="Management", icon='FILE_TICK')
        row = layout.row(align=True)
        row.operator("gesturenav.save", text="Save Settings")
        row.operator("gesturenav.load", text="Load Settings")
        layout.operator("gesturenav.reset", text="Reset Defaults", icon='LOOP_BACK')
            
        # Settings
        layout.separator()
        layout.label(text="Tuning (Real-time)", icon='PREFERENCES')
        
        # Deadzone
        box = layout.box()
        box.label(text="Orbit Deadzone")
        
        row = box.row(align=True)
        op = row.operator("gesturenav.preset", text="Right Hand")
        op.side = 'RIGHT'
        op = row.operator("gesturenav.preset", text="Left Hand")
        op.side = 'LEFT'
        
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
    bpy.utils.register_class(GestureNav_OT_Preset)
    bpy.utils.register_class(GestureNav_OT_Reset)
    bpy.utils.register_class(GestureNav_OT_SaveSettings)
    bpy.utils.register_class(GestureNav_OT_LoadSettings)
    
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
    
    # Sensitivity 
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
    bpy.utils.unregister_class(GestureNav_OT_Preset)
    bpy.utils.unregister_class(GestureNav_OT_Reset)
    bpy.utils.unregister_class(GestureNav_OT_SaveSettings)
    bpy.utils.unregister_class(GestureNav_OT_LoadSettings)
    
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
