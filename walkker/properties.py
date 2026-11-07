# SPDX-License-Identifier: GPL-3.0-or-later
import math

import bpy
from bpy.props import BoolProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import PropertyGroup


class WalkkerSettings(PropertyGroup):
    rig: PointerProperty(
        name="Rig",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "ARMATURE",
    )
    frames: IntProperty(
        name="Frames per Cycle", default=32, min=8, max=240,
        description="Length of one full cycle (two steps)",
    )
    stance: FloatProperty(
        name="Stance Ratio", default=0.6, min=0.5, max=0.8,
        description="Fraction of the cycle a foot stays on the ground",
    )
    step_length: FloatProperty(
        name="Step Length", default=0.6, min=0.0, unit="LENGTH",
        description="Distance between front and rear foot",
    )
    foot_lift: FloatProperty(name="Foot Lift", default=0.12, min=0.0, unit="LENGTH")
    hip_bounce: FloatProperty(name="Hip Bounce", default=0.02, min=0.0, unit="LENGTH")
    hip_sway: FloatProperty(name="Hip Sway", default=0.02, min=0.0, unit="LENGTH")
    hip_yaw: FloatProperty(
        name="Hip Rotation", default=math.radians(8.0), min=0.0, subtype="ANGLE"
    )
    chest_twist: FloatProperty(
        name="Chest Twist", default=math.radians(6.0), min=0.0, subtype="ANGLE"
    )
    arm_swing: FloatProperty(
        name="Arm Swing", default=math.radians(25.0), min=0.0,
        max=math.radians(80.0), subtype="ANGLE",
        description="Forward/back swing angle from the shoulder",
    )
    arm_space: FloatProperty(
        name="Arm Space", default=0.0, min=-0.5, max=0.5, unit="LENGTH",
        description="Side distance of the hands from the body. "
        "Negative = closer to the body, positive = wider",
    )
    use_arms: BoolProperty(name="Animate Arms", default=True)
    use_fingers: BoolProperty(name="Animate Fingers", default=True)
    finger_curl: FloatProperty(
        name="Finger Curl", default=math.radians(15.0),
        min=math.radians(-90.0), max=math.radians(90.0), subtype="ANGLE",
        description="Relaxed finger curl. Use a negative value if they bend the wrong way",
    )
    finger_sway: FloatProperty(
        name="Finger Sway", default=math.radians(4.0), min=0.0,
        max=math.radians(30.0), subtype="ANGLE",
        description="Fingers lag slightly behind the arm swing",
    )
    set_ik: BoolProperty(
        name="Force IK", default=True,
        description="Set the IK_FK slider of legs and arms to IK",
    )


def register():
    bpy.utils.register_class(WalkkerSettings)
    bpy.types.Scene.walkker = PointerProperty(type=WalkkerSettings)


def unregister():
    del bpy.types.Scene.walkker
    bpy.utils.unregister_class(WalkkerSettings)
