"""Bezier2SVG export operator (Blender-bound layer)."""

from __future__ import annotations

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty
from bpy_extras.io_utils import ExportHelper
from mathutils import Matrix, Vector

from ..core.path_builder import bbox_from_points, format_curveto, format_moveto
from ..core.projection import projection_matrix
from ..core.svg import SVGFile


class BEZIER2SVG_OT_export(bpy.types.Operator, ExportHelper):
    """Export Bezier curve as SVG"""

    bl_idname = "bezier2svg.export"
    bl_label = "Bezier2SVG (.svg)"

    # ExportHelper mixin
    filename_ext = ".svg"
    filter_glob: StringProperty(  # type: ignore[valid-type]
        default="*.svg",
        options={"HIDDEN"},
        maxlen=255,
    )

    selection_only: BoolProperty(  # type: ignore[valid-type]
        name="Selection only",
        description="Export selected objects only",
        default=True,
    )

    projection_axis: EnumProperty(  # type: ignore[valid-type]
        items=[
            ("Z", "Z", "", 0),
            ("-Z", "-Z", "", 1),
            ("X", "X", "", 2),
            ("-X", "-X", "", 3),
            ("Y", "Y", "", 4),
            ("-Y", "-Y", "", 5),
            ("Viewport", "Viewport", "", 6),
        ],
        name="Projection Axis",
        description="Projection along global axis",
        default="Viewport",
    )

    scale: FloatProperty(  # type: ignore[valid-type]
        name="Scale (px / Blender Unit) ",
        description="Scale of exported image",
        default=100,
    )

    def execute(self, context):
        # Build the projection matrix once for axis-aligned modes; for
        # "Viewport" we read the active 3D view's view_matrix.
        if self.projection_axis == "Viewport":
            view_areas = [a for a in context.window.screen.areas if a.type == "VIEW_3D"]
            if not view_areas:
                self.report({"ERROR"}, "No 3D Viewport found for 'Viewport' projection")
                return {"CANCELLED"}
            proj = view_areas[-1].spaces.active.region_3d.view_matrix
        else:
            proj = Matrix(projection_matrix(self.projection_axis))

        def project_world(obj, point: Vector) -> Vector:
            return proj @ (obj.matrix_world @ point)

        # Collect curve objects.
        if self.selection_only:
            objects = [
                ob
                for ob in context.visible_objects
                if ob.type == "CURVE" and ob.select_get()
            ]
        else:
            objects = [ob for ob in context.visible_objects if ob.type == "CURVE"]

        if not objects:
            self.report({"WARNING"}, "No curve objects to export")
            return {"CANCELLED"}

        # Canvas bounding box from all object bound_box corners.
        bounding_points = [
            project_world(ob, Vector(bp)) for ob in objects for bp in ob.bound_box
        ]
        origin_xyz, size = bbox_from_points([(p.x, p.y, p.z) for p in bounding_points])
        origin = Vector(origin_xyz)

        def to_svg_xy(obj, point: Vector) -> tuple[float, float]:
            p = (project_world(obj, point) - origin) * self.scale
            return (p.x, -p.y)

        svg_file = SVGFile(width=size[0] * self.scale, height=size[1] * self.scale)

        for obj in objects:
            path_parts: list[str] = []
            for spline in obj.data.splines:
                if not spline.bezier_points:
                    msg = f"Non-bezier curve not exported in object: {obj.name}"
                    print(msg)
                    self.report({"WARNING"}, msg)
                    continue

                first_point = spline.bezier_points[0]
                last_point = spline.bezier_points[-1]

                fx, fy = to_svg_xy(obj, first_point.co)
                path_parts.append(format_moveto(fx, fy))

                for prev_idx, b_point in enumerate(spline.bezier_points[1:]):
                    prev_point = spline.bezier_points[prev_idx]
                    path_parts.append(
                        format_curveto(
                            to_svg_xy(obj, prev_point.handle_right),
                            to_svg_xy(obj, b_point.handle_left),
                            to_svg_xy(obj, b_point.co),
                        )
                    )

                if spline.use_cyclic_u:
                    path_parts.append(
                        format_curveto(
                            to_svg_xy(obj, last_point.handle_right),
                            to_svg_xy(obj, first_point.handle_left),
                            to_svg_xy(obj, first_point.co),
                        )
                    )

            if path_parts:
                svg_file.new_layer(obj.name, "".join(path_parts))

        with open(self.filepath, "w") as f:
            f.write(svg_file.to_string())

        return {"FINISHED"}
