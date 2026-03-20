"""Diff new extension SVG output against the legacy plugin (must be byte-identical).

Also re-verifies the committed fixture under tests/fixtures/.
"""
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

from _helpers import enable_extension, out_path  # noqa: E402

REPO_ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LEGACY = os.path.join(REPO_ROOT, "legacy", "controller.py")
FIXTURE = os.path.join(REPO_ROOT, "tests", "fixtures", "two_curves_z_scale100.svg")

bpy.ops.wm.read_factory_settings(use_empty=True)
enable_extension()
bpy.ops.curve.primitive_bezier_curve_add()
bpy.context.active_object.name = "BC1"
bpy.ops.curve.primitive_bezier_circle_add(location=(5, 0, 0))
bpy.context.active_object.name = "BC2"

new_svg = out_path("diff_new.svg")
leg_svg = out_path("diff_legacy.svg")

bpy.ops.bezier2svg.export(filepath=new_svg, projection_axis="Z", selection_only=False, scale=100)

bpy.ops.preferences.addon_disable(module="bl_ext.user_default.leomoon_bezier2svg")
spec = importlib.util.spec_from_file_location("legacy_controller", LEGACY)
legacy = importlib.util.module_from_spec(spec)
sys.modules["legacy_controller"] = legacy
spec.loader.exec_module(legacy)
bpy.utils.register_class(legacy.BEZIER2SVG_OT_export)
bpy.ops.bezier2svg.export(filepath=leg_svg, projection_axis="Z", selection_only=False, scale=100)

a = open(new_svg).read()
b = open(leg_svg).read()
print("new bytes:", len(a), "legacy bytes:", len(b))

if a != b:
    import difflib
    for line in difflib.unified_diff(
        b.splitlines(keepends=True), a.splitlines(keepends=True),
        fromfile="legacy", tofile="new", n=1,
    ):
        sys.stdout.write(line)
    print("FAIL: legacy and new SVG differ")
    sys.exit(1)

print("OK: legacy ≡ new (byte-identical)")

if os.path.exists(FIXTURE):
    fixture = open(FIXTURE).read()
    if fixture != a:
        print(f"FAIL: fixture {FIXTURE} drifted from current output")
        sys.exit(1)
    print(f"OK: fixture {os.path.relpath(FIXTURE, REPO_ROOT)} matches")
else:
    print(f"WARN: fixture not found at {FIXTURE}")
