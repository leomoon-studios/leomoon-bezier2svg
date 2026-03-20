"""Unit tests for `bezier2svg.core.projection`."""

from __future__ import annotations

import importlib.util
import os
import sys
import unittest

_MODULE_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "bezier2svg",
        "core",
        "projection.py",
    )
)
_spec = importlib.util.spec_from_file_location("projection", _MODULE_PATH)
assert _spec and _spec.loader
_proj = importlib.util.module_from_spec(_spec)
sys.modules["projection"] = _proj
_spec.loader.exec_module(_proj)
projection_matrix = _proj.projection_matrix
AXIS_CHOICES = _proj.AXIS_CHOICES


def _apply(m, p):
    """Apply a 4x4 row-major matrix to a 3-vector (treating w=1)."""
    x, y, z = p
    return tuple(
        m[r][0] * x + m[r][1] * y + m[r][2] * z + m[r][3]
        for r in range(3)
    )


class TestProjectionMatrix(unittest.TestCase):
    def test_z_is_identity_for_xyz(self) -> None:
        m = projection_matrix("Z")
        self.assertEqual(_apply(m, (1.0, 2.0, 3.0)), (1.0, 2.0, 3.0))

    def test_neg_z_inverts_all_axes(self) -> None:
        m = projection_matrix("-Z")
        self.assertEqual(_apply(m, (1.0, 2.0, 3.0)), (1.0, -2.0, -3.0))

    def test_x_swaps_axes(self) -> None:
        # Looking down +X: world Y becomes screen X, world Z becomes screen Y.
        m = projection_matrix("X")
        out = _apply(m, (10.0, 4.0, 7.0))
        self.assertEqual(out, (4.0, 7.0, 10.0))

    def test_neg_x_swaps_axes(self) -> None:
        m = projection_matrix("-X")
        out = _apply(m, (10.0, 4.0, 7.0))
        self.assertEqual(out, (-4.0, 7.0, -10.0))

    def test_y_and_neg_y(self) -> None:
        my = projection_matrix("Y")
        self.assertEqual(_apply(my, (4.0, 5.0, 6.0)), (-4.0, 6.0, 5.0))
        mny = projection_matrix("-Y")
        self.assertEqual(_apply(mny, (4.0, 5.0, 6.0)), (4.0, 6.0, -5.0))

    def test_viewport_raises(self) -> None:
        with self.assertRaises(ValueError):
            projection_matrix("Viewport")

    def test_unknown_axis_raises(self) -> None:
        with self.assertRaises(ValueError):
            projection_matrix("Q")

    def test_axis_choices_include_viewport(self) -> None:
        self.assertIn("Viewport", AXIS_CHOICES)
        for axis in ("Z", "-Z", "X", "-X", "Y", "-Y"):
            self.assertIn(axis, AXIS_CHOICES)


if __name__ == "__main__":
    unittest.main()
