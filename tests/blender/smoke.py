"""Smoke test: enable extension, export one bezier, sanity-check SVG."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

from _helpers import enable_extension, out_path  # noqa: E402

bpy.ops.wm.read_factory_settings(use_empty=True)
enable_extension()

bpy.ops.curve.primitive_bezier_curve_add()

svg = out_path("smoke.svg")
result = bpy.ops.bezier2svg.export(filepath=svg, projection_axis="Z", selection_only=False)
print("operator result:", result)

if not os.path.exists(svg):
    print("FAIL: SVG not written")
    sys.exit(1)

content = open(svg).read()
required = ["<svg", "</svg>", "<path", "Created with LeoMoon Bezier2SVG"]
missing = [s for s in required if s not in content]
if missing:
    print("FAIL: missing markers:", missing)
    sys.exit(1)

print("OK: smoke")
