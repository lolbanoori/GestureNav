bl_info = {
    "name": "GestureNav Client",
    "author": "Antigravity",
    "version": (1, 1),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GestureNav",
    "description": "UDP Client for GestureNav Vision Server",
    "category": "3D View",
}

import bpy
from .operator_listen import GestureNav_OT_Start, GestureNav_OT_Stop

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

        if scene.gesturenav_listening:
            layout.operator("gesturenav.stop", text="Stop Listener", icon='CANCEL')
            layout.label(text="Status: Listening...", icon='REC')
        else:
            layout.operator("gesturenav.start", text="Start Listener", icon='PLAY')
            layout.label(text="Status: Idle", icon='PAUSE')

def register():
    bpy.utils.register_class(GESTURENAV_PT_Panel)
    bpy.utils.register_class(GestureNav_OT_Start)
    bpy.utils.register_class(GestureNav_OT_Stop)
    bpy.types.Scene.gesturenav_listening = bpy.props.BoolProperty(
        name="Listening",
        description="Is the GestureNav listener active?",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(GESTURENAV_PT_Panel)
    bpy.utils.unregister_class(GestureNav_OT_Start)
    bpy.utils.unregister_class(GestureNav_OT_Stop)
    del bpy.types.Scene.gesturenav_listening

if __name__ == "__main__":
    register()
