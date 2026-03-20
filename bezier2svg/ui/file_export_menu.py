"""File > Export menu entry for Bezier2SVG."""

from __future__ import annotations

import bpy

from ..operators.export_svg import BEZIER2SVG_OT_export


def menu_func_export(self, context):
    self.layout.operator(BEZIER2SVG_OT_export.bl_idname, text="Bezier2SVG (.svg)")


def register() -> None:
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister() -> None:
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
