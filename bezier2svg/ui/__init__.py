"""UI registration for Bezier2SVG."""

from . import file_export_menu


def register() -> None:
    file_export_menu.register()


def unregister() -> None:
    file_export_menu.unregister()
