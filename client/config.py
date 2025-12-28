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
    # Bundle Settings
    # Note: self refers to the PropertyGroup instance
    config = {
        'deadzone_radius': self.deadzone_radius,
        'deadzone_offset_x': self.deadzone_x,
        'deadzone_offset_y': self.deadzone_y,
        'zoom_thresh_in': self.zoom_thresh_in,
        'zoom_thresh_out': self.zoom_thresh_out,
        'orbit_sens_server': self.orbit_sens_server,
        'use_fist_safety': self.use_fist_safety,
        'use_open_hand_safety': self.use_open_hand_safety
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
        name="Zoom Out Threshold", default=0.15, min=0.05, max=0.5, update=send_config
    )
    
    # Safety
    use_fist_safety: bpy.props.BoolProperty(
        name="Fist Safety", default=True, update=send_config
    )
    use_open_hand_safety: bpy.props.BoolProperty(
        name="Open Hand Safety", default=False, update=send_config
    )
