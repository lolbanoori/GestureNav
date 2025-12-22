bl_info = {
    "name": "GestureNav Client",
    "author": "Antigravity",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > GestureNav",
    "description": "UDP Client for GestureNav Vision Server",
    "category": "3D View",
}

import bpy
from .operator_listen import GestureNav_OT_Listen

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
            layout.operator("gesturenav.listen", text="Stop Listener", icon='CANCEL').action = "STOP"
            layout.label(text="Status: Listening...", icon='REC')
        else:
            layout.operator("gesturenav.listen", text="Start Listener", icon='PLAY').action = "START"
            layout.label(text="Status: Idle", icon='PAUSE')

def register():
    bpy.utils.register_class(GESTURENAV_PT_Panel)
    bpy.utils.register_class(GestureNav_OT_Listen)
    bpy.types.Scene.gesturenav_listening = bpy.props.BoolProperty(
        name="Listening",
        description="Is the GestureNav listener active?",
        default=False
    )

def unregister():
    bpy.utils.unregister_class(GESTURENAV_PT_Panel)
    bpy.utils.unregister_class(GestureNav_OT_Listen)
    del bpy.types.Scene.gesturenav_listening

if __name__ == "__main__":
    register()
