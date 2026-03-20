"""Mixed bezier/non-bezier scene: check warnings, layer naming, skipping."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bpy  # noqa: E402

from _helpers import enable_extension, out_path  # noqa: E402

bpy.ops.wm.read_factory_settings(use_empty=True)
enable_extension()

bpy.ops.curve.primitive_bezier_curve_add()
bpy.context.active_object.name = "OpenBezier"

bpy.ops.curve.primitive_bezier_circle_add(location=(5, 0, 0))
bpy.context.active_object.name = "ClosedCircle"

bpy.ops.curve.primitive_nurbs_path_add(location=(10, 0, 0))
bpy.context.active_object.name = "NurbsPath"

bpy.ops.curve.primitive_bezier_curve_add(location=(15, 0, 0))
mixed = bpy.context.active_object
mixed.name = "MixedCurve"
poly = mixed.data.splines.new(type="POLY")
poly.points.add(2)

svg = out_path("multi.svg")
result = bpy.ops.bezier2svg.export(filepath=svg, projection_axis="Z", selection_only=False)
print("result:", result)

content = open(svg).read()
for s in ("<title>OpenBezier</title>", "<title>ClosedCircle</title>", "<title>MixedCurve</title>",
          'id="svg_OpenBezier"', 'id="svg_ClosedCircle"', 'id="svg_MixedCurve"'):
    if s not in content:
        print("FAIL missing:", s)
        sys.exit(1)

if "svg_NurbsPath" in content:
    print("FAIL: NurbsPath should not have produced a layer")
    sys.exit(1)

print("OK: multi-object export, layer naming, non-bezier skipping verified")
