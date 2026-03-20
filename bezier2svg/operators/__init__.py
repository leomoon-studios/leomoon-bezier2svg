"""Operator registration for Bezier2SVG."""

import bpy

from .export_svg import BEZIER2SVG_OT_export

classes = (BEZIER2SVG_OT_export,)


def register() -> None:
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
