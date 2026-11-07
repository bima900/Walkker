# SPDX-License-Identifier: GPL-3.0-or-later
"""Nama bone Rigify dan helper deteksi rig. Tanpa import bpy."""

REQUIRED_BONES = ("torso", "foot_ik.L", "foot_ik.R")
OPTIONAL_BONES = ("hips", "chest", "hand_ik.L", "hand_ik.R")

# (nama dasar, pengali kelengkungan); bone: f_index.01.L, thumb.01.L, ...
FINGERS = (
    ("thumb", 0.3),
    ("f_index", 0.8),
    ("f_middle", 1.0),
    ("f_ring", 1.2),
    ("f_pinky", 1.4),
)
SEGMENTS = ("01", "02", "03")

SIDES = ((".L", 0.0), (".R", 0.5))  # (sufiks, offset fase)

# Slider IK/FK Rigify: 0 = IK
IK_FK_BONES = (
    "thigh_parent.L",
    "thigh_parent.R",
    "upper_arm_parent.L",
    "upper_arm_parent.R",
)


def check_rig(rig):
    """Return pesan error (str) atau None jika rig valid."""
    if rig is None or rig.type != "ARMATURE":
        return "Pilih objek armature Rigify."
    missing = [n for n in REQUIRED_BONES if n not in rig.pose.bones]
    if missing:
        return "Bone Rigify tidak ditemukan: " + ", ".join(missing)
    return None


def arm_radius(pbs, side):
    """Jarak bahu ke tangan (rest) sebagai jari-jari ayunan pendulum."""
    hand = pbs.get("hand_ik" + side)
    if hand is not None:
        for name in ("upper_arm_ik", "upper_arm_fk", "upper_arm_parent"):
            shoulder = pbs.get(name + side)
            if shoulder is not None:
                length = (hand.bone.head_local - shoulder.bone.head_local).length
                return max(length, 0.05)
    return 0.6
