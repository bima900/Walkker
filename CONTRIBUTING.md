# Contributing to Walkker

Thanks for helping! Walkker is licensed under GPL-3.0-or-later; by contributing
you agree your work is released under the same license.

## Setup
```
pip install ruff pytest
ruff check .
pytest
```

## Guidelines
- Keep animation math in `walkker/motion.py` (no `bpy`) and add tests in `tests/`.
- Keep Rigify bone names in `walkker/rigify_map.py`.
- Test changes in Blender 5.x on a Rigify-generated rig before opening a PR.
- When reporting a bug, include your Blender version, the Rigify version/rig type,
  and the error from the system console.

## Roadmap ideas
- Moving root with foot locking (no sliding)
- Heel strike / toe-off foot roll
- Follow a path or terrain
- Walk style presets, quadruped support
