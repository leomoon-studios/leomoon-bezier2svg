"""Verify menu wiring + operator label/description/defaults."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

from _helpers import enable_extension  # noqa: E402

bpy.ops.wm.read_factory_settings(use_empty=True)
enable_extension()

draw_funcs = bpy.types.TOPBAR_MT_file_export._dyn_ui_initialize()
fn_names = [getattr(f, "__name__", str(f)) for f in draw_funcs]
print("draw funcs:", fn_names)
if "menu_func_export" not in fn_names:
    print("FAIL: menu_func_export not in TOPBAR_MT_file_export")
    sys.exit(1)

rna = bpy.ops.bezier2svg.export.get_rna_type()
props = rna.properties
print("label:", rna.name)
print("description:", rna.description)
print("selection_only default:", props["selection_only"].default)
print("projection_axis default:", props["projection_axis"].default)
print("scale default:", props["scale"].default)

assert rna.name == "Bezier2SVG (.svg)", rna.name
assert rna.description == "Export Bezier curve as SVG", rna.description
assert props["selection_only"].default is True
assert props["projection_axis"].default == "Viewport"
assert abs(props["scale"].default - 100.0) < 1e-6
print("OK: menu wired, defaults match legacy")
