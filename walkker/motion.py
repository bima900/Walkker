# SPDX-License-Identifier: GPL-3.0-or-later
"""Rumus gerak murni (tanpa bpy), mudah dites.

Konvensi: ``t`` adalah posisi dalam siklus (0..1). Hasil posisi dalam meter,
sudut dalam radian. Arah "maju" dan "naik" ditentukan oleh pemanggil.
"""

import math

TAU = 2.0 * math.pi

# Pengali kelengkungan per segmen jari (.01, .02, .03).
SEGMENT_SCALE = (0.7, 1.0, 0.8)


def smoothstep(u):
    return u * u * (3.0 - 2.0 * u)


def foot_curve(phase, step, lift, stance):
    """Return (maju, naik) satu kaki untuk root diam.

    Stance: kaki bergeser ke belakang di tanah. Swing: kaki diangkat lalu maju.
    """
    if phase < stance:
        u = phase / stance
        return (step * 0.5 - step * u, 0.0)
    u = (phase - stance) / (1.0 - stance)
    return (-step * 0.5 + step * smoothstep(u), lift * math.sin(math.pi * u))


def torso_offsets(t, bounce, sway):
    """Return (samping, naik). Naik-turun 2x per siklus, geser samping 1x."""
    up = 0.5 * bounce * (-math.cos(2.0 * TAU * t))
    side = sway * math.sin(TAU * (t - 0.05))
    return side, up


def hip_yaw(t, amount):
    return -amount * math.cos(TAU * t)


def chest_yaw(t, amount):
    """Berlawanan arah dengan pinggul."""
    return amount * math.cos(TAU * t)


def arm_theta(t, amplitude):
    """Sudut ayunan lengan dari bahu (negatif = ke belakang)."""
    return -amplitude * math.cos(TAU * t)


def arm_offset(radius, theta):
    """Return (maju, naik) tangan sebagai pendulum dari bahu."""
    return (radius * math.sin(theta), radius * (1.0 - math.cos(theta)))


def finger_angle(t, curl, sway, finger_scale, segment_index):
    """Sudut tekuk satu segmen jari: lengkung santai + goyang tertinggal."""
    lag = 0.35 * (segment_index + 1)
    wave = sway * math.sin(TAU * t - lag)
    return (curl * SEGMENT_SCALE[segment_index] + wave) * finger_scale
