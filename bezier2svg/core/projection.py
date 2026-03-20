"""Pure-Python projection matrices for axis-aligned exports.

Matrices are returned as tuple-of-tuples (4×4, row-major) to avoid a `mathutils`
or `numpy` dependency in the unit-test path. The Blender operator wraps these
with `mathutils.Matrix(...)` when the `bpy` runtime is available.

The "Viewport" axis is intentionally not handled here — it depends on Blender's
active 3D view and is computed at operator runtime.
"""

from __future__ import annotations

Matrix4 = tuple[
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
    tuple[float, float, float, float],
]


AXIS_CHOICES: tuple[str, ...] = ("Z", "-Z", "X", "-X", "Y", "-Y", "Viewport")


_MATRICES: dict[str, Matrix4] = {
    "-X": (
        (0.0, -1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (-1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ),
    "X": (
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ),
    "-Y": (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, -1.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ),
    "Y": (
        (-1.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ),
    "-Z": (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, -1.0, 0.0, 0.0),
        (0.0, 0.0, -1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ),
    "Z": (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 0.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    ),
}


def projection_matrix(axis: str) -> Matrix4:
    """Return the 4×4 projection matrix for the given axis name.

    Valid axes: "Z", "-Z", "X", "-X", "Y", "-Y".
    Raises `ValueError` for "Viewport" (handled at operator runtime) or unknown
    axis names.
    """
    if axis == "Viewport":
        raise ValueError("'Viewport' projection is computed at operator runtime")
    try:
        return _MATRICES[axis]
    except KeyError as exc:
        raise ValueError(f"Unknown projection axis: {axis!r}") from exc
