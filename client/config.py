import bpy
import socket
import json
import os

CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".gesturenav_config.json")

def send_config(self, context=None):
    """
    Sends current scene properties to the Python Server via UDP Port 5556.
    'self' is expected to be the GestureNavProperties instance.
    """
    properties = self
    if not isinstance(self, GestureNavProperties):
        if context:
            properties = getattr(context.scene, "gesture_nav", None)
            if not properties: return
    
    config = {
        'deadzone_radius': properties.deadzone_radius,
        'deadzone_offset_x': properties.deadzone_x,
        'deadzone_offset_y': properties.deadzone_y,
        'zoom_thresh_in': properties.zoom_thresh_in,
        'zoom_thresh_out': properties.zoom_thresh_out,
        'orbit_sens_server': properties.orbit_sens_server,
        'use_fist_safety': properties.use_fist_safety,
        'use_open_hand_safety': properties.use_open_hand_safety
    }
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(config).encode('utf-8'), ("127.0.0.1", 5556))
    except Exception as e:
        print(f"Config Send Error: {e}")

class GestureNavProperties(bpy.types.PropertyGroup):
    """
    Property Group for GestureNav Settings.
    """
    # Internal State
    listening: bpy.props.BoolProperty(
        name="Listening", default=False
    )
    
    # Deadzone
    deadzone_radius: bpy.props.FloatProperty(
        name="Deadzone Radius", default=0.12, min=0.01, max=0.5, update=send_config
    )
    deadzone_x: bpy.props.FloatProperty(
        name="Deadzone X", default=0.75, min=0.0, max=1.0, update=send_config
    )
    deadzone_y: bpy.props.FloatProperty(
        name="Deadzone Y", default=0.6, min=0.0, max=1.0, update=send_config
    )
    
    # Sensitivity (Client Side)
    orbit_sensitivity: bpy.props.FloatProperty(
        name="Orbit Sensitivity", default=0.02, min=0.001, max=0.2
    )
    zoom_sensitivity: bpy.props.FloatProperty(
        name="Zoom Sensitivity", default=2.0, min=0.1, max=10.0
    )
    
    # Sensitivity (Server Side)
    orbit_sens_server: bpy.props.FloatProperty(
        name="Orbit Curve", default=3.0, min=1.0, max=10.0, update=send_config
    )
    
    # Zoom Thresholds
    zoom_thresh_in: bpy.props.FloatProperty(
        name="Zoom In Threshold", default=0.05, min=0.01, max=0.2, update=send_config
    )
    zoom_thresh_out: bpy.props.FloatProperty(
        name="Zoom Out Threshold", default=0.20, min=0.05, max=0.5, update=send_config
    )
    
    # Safety
    use_fist_safety: bpy.props.BoolProperty(
        name="Fist Safety", default=True, update=send_config
    )
    use_open_hand_safety: bpy.props.BoolProperty(
        name="Open Hand Safety", default=False, update=send_config
    )

# --- Operators ---

class GestureNav_OT_Preset(bpy.types.Operator):
    """Apply a Handedness Preset"""
    bl_idname = "gesturenav.preset"
    bl_label = "Apply Preset"
    
    side: bpy.props.EnumProperty(
        items=[('RIGHT', "Right Handed", ""), ('LEFT', "Left Handed", "")]
    )
    
    def execute(self, context):
        props = getattr(context.scene, "gesture_nav", None)
        if not props: return {'CANCELLED'}

        if self.side == 'RIGHT':
            props.deadzone_x = 0.75
        else:
            props.deadzone_x = 0.25
            
        send_config(props, context)
        self.report({'INFO'}, f"Applied {self.side} Handed Preset")
        return {'FINISHED'}

class GestureNav_OT_Reset(bpy.types.Operator):
    """Reset All Settings to default"""
    bl_idname = "gesturenav.reset"
    bl_label = "Reset Settings"
    
    def execute(self, context):
        props = getattr(context.scene, "gesture_nav", None)
        if not props: return {'CANCELLED'}

        props.deadzone_radius = 0.12
        props.deadzone_x = 0.75
        props.deadzone_y = 0.6
        props.orbit_sensitivity = 0.02
        props.zoom_sensitivity = 2.0
        props.orbit_sens_server = 3.0
        props.zoom_thresh_in = 0.05
        props.zoom_thresh_out = 0.20
        props.use_fist_safety = True
        props.use_open_hand_safety = False
        
        send_config(props, context)
        self.report({'INFO'}, "Settings Reset")
        return {'FINISHED'}

class GestureNav_OT_SaveSettings(bpy.types.Operator):
    """Save current settings to disk"""
    bl_idname = "gesturenav.save"
    bl_label = "Save Config"
    
    def execute(self, context):
        props = getattr(context.scene, "gesture_nav", None)
        if not props: return {'CANCELLED'}

        data = {
            'deadzone_radius': props.deadzone_radius,
            'deadzone_x': props.deadzone_x,
            'deadzone_y': props.deadzone_y,
            'orbit_sensitivity': props.orbit_sensitivity,
            'zoom_sensitivity': props.zoom_sensitivity,
            'orbit_sens_server': props.orbit_sens_server,
            'zoom_thresh_in': props.zoom_thresh_in,
            'zoom_thresh_out': props.zoom_thresh_out,
            'use_fist_safety': props.use_fist_safety,
            'use_open_hand_safety': props.use_open_hand_safety
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
                
            props = getattr(context.scene, "gesture_nav", None)
            if not props: return {'CANCELLED'}

            if 'deadzone_radius' in data: props.deadzone_radius = data['deadzone_radius']
            if 'deadzone_x' in data: props.deadzone_x = data['deadzone_x']
            if 'deadzone_y' in data: props.deadzone_y = data['deadzone_y']
            if 'orbit_sensitivity' in data: props.orbit_sensitivity = data['orbit_sensitivity']
            if 'zoom_sensitivity' in data: props.zoom_sensitivity = data['zoom_sensitivity']
            if 'orbit_sens_server' in data: props.orbit_sens_server = data['orbit_sens_server']
            if 'zoom_thresh_in' in data: props.zoom_thresh_in = data['zoom_thresh_in']
            if 'zoom_thresh_out' in data: props.zoom_thresh_out = data['zoom_thresh_out']
            if 'use_fist_safety' in data: props.use_fist_safety = data['use_fist_safety']
            if 'use_open_hand_safety' in data: props.use_open_hand_safety = data['use_open_hand_safety']
            
            send_config(props, context)
            self.report({'INFO'}, "Settings Loaded")
        except Exception as e:
            self.report({'ERROR'}, f"Load Failed: {e}")
            
        return {'FINISHED'}
