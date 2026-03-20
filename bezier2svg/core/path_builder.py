"""Pure-Python helpers for building SVG path strings and computing bounds.

All inputs are plain tuples/sequences — no `bpy` or `mathutils` dependency.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

Point2 = tuple[float, float]
Point3 = tuple[float, float, float]


def format_moveto(x: float, y: float) -> str:
    """Format an absolute SVG `M` (moveto) command."""
    return f"M {x:5.11f} {y:5.11f} \n"


def format_curveto(p1: Point2, p2: Point2, p3: Point2) -> str:
    """Format an absolute SVG `C` (cubic curveto) command.

    `p1` is the first control point (start handle_right), `p2` the second
    control point (end handle_left), `p3` the destination point (end co).
    """
    return (
        f"C {p1[0]:5.11f} {p1[1]:5.11f}, "
        f"{p2[0]:5.11f} {p2[1]:5.11f}, "
        f"{p3[0]:5.11f} {p3[1]:5.11f} \n"
    )


def bbox_from_points(
    points: Iterable[Sequence[float]],
) -> tuple[Point3, Point2]:
    """Compute the SVG bounding box for a set of projected 3D points.

    Returns `(origin, size)` where:
      - `origin` is `(min_x, max_y, 0)` — the SVG-space top-left in world coords
        (matches legacy behavior; y is inverted in the operator step).
      - `size` is `(width, height)` in world units.

    Raises `ValueError` if `points` is empty.
    """
    pts = list(points)
    if not pts:
        raise ValueError("bbox_from_points requires at least one point")

    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    origin: Point3 = (min_x, max_y, 0.0)
    size: Point2 = (max_x - min_x, max_y - min_y)
    return origin, size
