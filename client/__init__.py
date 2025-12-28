bl_info = {
    "name": "GestureNav Client",
    "author": "Zohair Banoori",
    "version": (1, 6, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GestureNav",
    "description": "UDP Client for GestureNav Vision Server",
    "category": "3D View",
}

import bpy
from .config import (
    GestureNavProperties, 
    GestureNav_OT_Preset, 
    GestureNav_OT_Reset, 
    GestureNav_OT_SaveSettings, 
    GestureNav_OT_LoadSettings
)
from .ui import GESTURENAV_PT_Panel
from .networking import GestureNav_OT_Start, GestureNav_OT_Stop

classes = (
    GestureNavProperties,
    GestureNav_OT_Start,
    GestureNav_OT_Stop,
    GestureNav_OT_Preset,
    GestureNav_OT_Reset,
    GestureNav_OT_SaveSettings,
    GestureNav_OT_LoadSettings,
    GESTURENAV_PT_Panel
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        
    # Register the Property Group Pointer
    bpy.types.Scene.gesture_nav = bpy.props.PointerProperty(type=GestureNavProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
        
    del bpy.types.Scene.gesture_nav

if __name__ == "__main__":
    register()
