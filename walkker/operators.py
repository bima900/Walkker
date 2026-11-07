# SPDX-License-Identifier: GPL-3.0-or-later
import bpy
from bpy.types import Operator
from mathutils import Quaternion, Vector

from . import motion, rigify_map

try:
    from bpy_extras import anim_utils
except ImportError:  # pragma: no cover
    anim_utils = None

# Karakter Blender/Rigify menghadap -Y, sisi .L ada di +X.
FORWARD = Vector((0.0, -1.0, 0.0))
UP = Vector((0.0, 0.0, 1.0))
SIDE_L = Vector((1.0, 0.0, 0.0))

ACTION_PREFIX = "Walkker_"


def to_bone_local(pb, vec):
    """Vektor di armature space -> arah di axes lokal bone (rest)."""
    return pb.bone.matrix_local.to_3x3().inverted() @ vec


def set_loc(pb, vec_armature):
    pb.location = to_bone_local(pb, vec_armature)


def set_rot(pb, axis_armature, angle):
    pb.rotation_mode = "QUATERNION"
    axis = to_bone_local(pb, axis_armature).normalized()
    pb.rotation_quaternion = Quaternion(axis, angle)


def key_bone(pb, frame):
    pb.keyframe_insert("location", frame=frame, group=pb.name)
    if pb.rotation_mode == "QUATERNION":
        pb.keyframe_insert("rotation_quaternion", frame=frame, group=pb.name)


def iter_fcurves(obj):
    """F-curve dari action, kompatibel dengan Action slotted (4.4+/5.x)."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return
    action = ad.action
    if anim_utils is not None and getattr(ad, "action_slot", None) is not None:
        try:
            channelbag = anim_utils.action_get_channelbag_for_slot(
                action, ad.action_slot
            )
        except Exception:
            channelbag = None
        if channelbag:
            yield from channelbag.fcurves
            return
    legacy = getattr(action, "fcurves", None)
    if legacy:
        yield from legacy


class WALKKER_OT_generate(Operator):
    bl_idname = "walkker.generate"
    bl_label = "Generate Walk"
    bl_description = "Create a looping in-place walk cycle (root stays still)"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        s = context.scene.walkker
        rig = s.rig
        err = rigify_map.check_rig(rig)
        if err:
            self.report({"ERROR"}, err)
            return {"CANCELLED"}

        pbs = rig.pose.bones
        n = s.frames
        start = context.scene.frame_start

        # Action baru (hapus action Walkker lama jika ada)
        rig.animation_data_create()
        old = rig.animation_data.action
        if old and old.name.startswith(ACTION_PREFIX):
            rig.animation_data.action = None
            if old.users == 0:
                bpy.data.actions.remove(old)
        action = bpy.data.actions.new(ACTION_PREFIX + rig.name)
        rig.animation_data.action = action

        if s.set_ik:
            for name in rigify_map.IK_FK_BONES:
                pb = pbs.get(name)
                if pb and "IK_FK" in pb:
                    pb["IK_FK"] = 0.0  # 0 = IK pada Rigify

        for i in range(n + 1):  # frame terakhir = frame pertama (loop)
            t = (i % n) / n
            frame = start + i

            # Kaki: L fase t, R fase t+0.5
            for side, offset in rigify_map.SIDES:
                phase = (t + offset) % 1.0
                fwd, up = motion.foot_curve(
                    phase, s.step_length, s.foot_lift, s.stance
                )
                pb = pbs["foot_ik" + side]
                set_loc(pb, FORWARD * fwd + UP * up)
                key_bone(pb, frame)

            # Torso: naik-turun dan geser samping
            side_off, up_off = motion.torso_offsets(t, s.hip_bounce, s.hip_sway)
            torso = pbs["torso"]
            set_loc(torso, UP * up_off + SIDE_L * side_off)
            key_bone(torso, frame)

            # Pinggul memutar, dada berlawanan
            if "hips" in pbs:
                set_rot(pbs["hips"], UP, motion.hip_yaw(t, s.hip_yaw))
                key_bone(pbs["hips"], frame)
            if "chest" in pbs:
                set_rot(pbs["chest"], UP, motion.chest_yaw(t, s.chest_twist))
                key_bone(pbs["chest"], frame)

            # Tangan: pendulum dari bahu, berlawanan dengan kaki sisi yang sama
            if s.use_arms:
                for side, offset in rigify_map.SIDES:
                    pb = pbs.get("hand_ik" + side)
                    if pb is None:
                        continue
                    theta = motion.arm_theta(t + offset, s.arm_swing)
                    fwd, up = motion.arm_offset(
                        rigify_map.arm_radius(pbs, side), theta
                    )
                    side_sign = 1.0 if side == ".L" else -1.0
                    set_loc(
                        pb,
                        FORWARD * fwd + UP * up + SIDE_L * side_sign * s.arm_space,
                    )
                    key_bone(pb, frame)

            # Jari Rigify: lengkung santai + goyang tertinggal
            if s.use_fingers:
                for side, offset in rigify_map.SIDES:
                    for finger, fscale in rigify_map.FINGERS:
                        for k, seg in enumerate(rigify_map.SEGMENTS):
                            pb = pbs.get(f"{finger}.{seg}{side}")
                            if pb is None:
                                continue
                            angle = motion.finger_angle(
                                t + offset, s.finger_curl, s.finger_sway, fscale, k
                            )
                            pb.rotation_mode = "QUATERNION"
                            pb.rotation_quaternion = Quaternion((1.0, 0.0, 0.0), angle)
                            key_bone(pb, frame)

        # Loop dengan modifier Cycles
        for fc in iter_fcurves(rig):
            if not any(m.type == "CYCLES" for m in fc.modifiers):
                fc.modifiers.new("CYCLES")
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"

        context.scene.frame_end = start + n - 1
        self.report({"INFO"}, f"Walk cycle created: {n} frames, looped with Cycles.")
        return {"FINISHED"}


def register():
    bpy.utils.register_class(WALKKER_OT_generate)


def unregister():
    bpy.utils.unregister_class(WALKKER_OT_generate)
