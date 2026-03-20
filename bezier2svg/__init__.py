"""LeoMoon Bezier2SVG — Blender 5.1+ extension."""

from . import operators, ui


def register() -> None:
    operators.register()
    ui.register()


def unregister() -> None:
    ui.unregister()
    operators.unregister()
