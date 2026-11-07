# SPDX-License-Identifier: GPL-3.0-or-later
import math

import pytest

from walkker import motion

STEP, LIFT, STANCE = 0.6, 0.12, 0.6


def test_foot_starts_in_front_on_ground():
    fwd, up = motion.foot_curve(0.0, STEP, LIFT, STANCE)
    assert fwd == pytest.approx(STEP / 2)
    assert up == 0.0


def test_foot_ends_stance_at_rear():
    fwd, up = motion.foot_curve(STANCE - 1e-9, STEP, LIFT, STANCE)
    assert fwd == pytest.approx(-STEP / 2, abs=1e-6)
    assert up == 0.0


def test_foot_swing_peaks_at_mid_swing():
    mid = STANCE + (1.0 - STANCE) / 2
    _, up = motion.foot_curve(mid, STEP, LIFT, STANCE)
    assert up == pytest.approx(LIFT)


def test_foot_cycle_is_continuous():
    fwd0, up0 = motion.foot_curve(0.0, STEP, LIFT, STANCE)
    fwd1, up1 = motion.foot_curve(1.0 - 1e-9, STEP, LIFT, STANCE)
    assert fwd1 == pytest.approx(fwd0, abs=1e-6)
    assert up1 == pytest.approx(up0, abs=1e-6)


def test_torso_lowest_at_double_support():
    _, up_start = motion.torso_offsets(0.0, 0.02, 0.02)
    _, up_mid = motion.torso_offsets(0.25, 0.02, 0.02)
    assert up_start < up_mid


def test_chest_counter_rotates_hips():
    for t in (0.0, 0.13, 0.5, 0.77):
        assert motion.chest_yaw(t, 0.1) == pytest.approx(-motion.hip_yaw(t, 0.1))


def test_arm_offset_zero_at_rest():
    assert motion.arm_offset(0.6, 0.0) == pytest.approx((0.0, 0.0))


def test_arms_swing_opposite_sides():
    amp = math.radians(25)
    for t in (0.0, 0.2, 0.6):
        left = motion.arm_theta(t, amp)
        right = motion.arm_theta(t + 0.5, amp)
        assert left == pytest.approx(-right)


def test_arm_rises_slightly_at_swing_extremes():
    _, up = motion.arm_offset(0.6, math.radians(25))
    assert up > 0.0


def test_finger_angle_without_sway_scales_with_finger():
    small = motion.finger_angle(0.3, 0.3, 0.0, 0.8, 1)
    large = motion.finger_angle(0.3, 0.3, 0.0, 1.4, 1)
    assert large > small > 0.0
