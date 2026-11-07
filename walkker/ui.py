# SPDX-License-Identifier: GPL-3.0-or-later
import bpy
from bpy.types import Panel

from . import rigify_map


class WALKKER_PT_main(Panel):
    bl_label = "Walkker"
    bl_idname = "WALKKER_PT_main"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Walkker"

    def draw(self, context):
        layout = self.layout
        s = context.scene.walkker

        layout.prop(s, "rig")
        if s.rig:
            err = rigify_map.check_rig(s.rig)
            if err:
                layout.label(text=err, icon="ERROR")

        col = layout.column(align=True)
        col.prop(s, "frames")
        col.prop(s, "stance")
        col.prop(s, "step_length")
        col.prop(s, "foot_lift")

        box = layout.box()
        box.label(text="Body")
        box.prop(s, "hip_bounce")
        box.prop(s, "hip_sway")
        box.prop(s, "hip_yaw")
        box.prop(s, "chest_twist")

        box = layout.box()
        box.prop(s, "use_arms")
        sub = box.column()
        sub.enabled = s.use_arms
        sub.prop(s, "arm_swing")
        sub.prop(s, "arm_space")

        box = layout.box()
        box.prop(s, "use_fingers")
        sub = box.column()
        sub.enabled = s.use_fingers
        sub.prop(s, "finger_curl")
        sub.prop(s, "finger_sway")

        layout.prop(s, "set_ik")
        layout.operator("walkker.generate", icon="ARMATURE_DATA")


def register():
    bpy.utils.register_class(WALKKER_PT_main)


def unregister():
    bpy.utils.unregister_class(WALKKER_PT_main)
