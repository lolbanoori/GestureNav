import bpy

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
        
        props = getattr(scene, "gesture_nav", None)
        
        if not props:
            layout.label(text="Error: Properties not found")
            return

        # Status / Main Control
        box = layout.box()
        if props.listening:
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
        
        box.prop(props, "deadzone_radius", text="Size")
        row = box.row(align=True)
        row.prop(props, "deadzone_x", text="X Pos")
        row.prop(props, "deadzone_y", text="Y Pos")
        
        # Sensitivity
        box = layout.box()
        box.label(text="Sensitivity")
        box.prop(props, "orbit_sensitivity", text="Orbit Speed (Client)")
        box.prop(props, "zoom_sensitivity", text="Zoom Speed (Client)")
        box.prop(props, "orbit_sens_server", text="Response Curve (Server)")
        
        # Zoom Thresholds
        box = layout.box()
        box.label(text="Zoom Triggers")
        box.prop(props, "zoom_thresh_in", text="Pinch In <")
        box.prop(props, "zoom_thresh_out", text="Pinch Out >")
        
        # Safety
        box = layout.box()
        box.label(text="Safety Locks")
        box.prop(props, "use_fist_safety", text="Fist Locks Zoom")
        box.prop(props, "use_open_hand_safety", text="Open Hand Locks Orbit")
