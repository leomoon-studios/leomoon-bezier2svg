"""Shared helpers for Blender integration scripts."""
from __future__ import annotations

import os
import sys

ADDON_ID = "bl_ext.user_default.leomoon_bezier2svg"


def out_dir() -> str:
    """Return the gitignored scratch directory for SVG output."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.normpath(os.path.join(here, "..", "_out"))
    os.makedirs(path, exist_ok=True)
    return path


def out_path(name: str) -> str:
    path = os.path.join(out_dir(), name)
    if os.path.exists(path):
        os.remove(path)
    return path


def enable_extension() -> None:
    import bpy
    bpy.ops.preferences.addon_enable(module=ADDON_ID)
    if ADDON_ID not in bpy.context.preferences.addons:
        print(f"FAIL: extension {ADDON_ID} did not enable — run `make install` first")
        sys.exit(2)
