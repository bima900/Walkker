# SPDX-License-Identifier: GPL-3.0-or-later
"""Walkker: procedural walk cycles for Rigify rigs."""

# Catatan: modul yang memakai bpy di-import di dalam register() supaya
# `walkker.motion` bisa di-import dan dites tanpa Blender.


def register():
    from . import operators, properties, ui

    properties.register()
    operators.register()
    ui.register()


def unregister():
    from . import operators, properties, ui

    ui.unregister()
    operators.unregister()
    properties.unregister()
