"""Unit tests for `bezier2svg.core.path_builder`."""

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
        "path_builder.py",
    )
)
_spec = importlib.util.spec_from_file_location("path_builder", _MODULE_PATH)
assert _spec and _spec.loader
_pb = importlib.util.module_from_spec(_spec)
sys.modules["path_builder"] = _pb
_spec.loader.exec_module(_pb)
format_moveto = _pb.format_moveto
format_curveto = _pb.format_curveto
bbox_from_points = _pb.bbox_from_points


class TestFormatMoveto(unittest.TestCase):
    def test_starts_with_M(self) -> None:
        s = format_moveto(1.0, 2.0)
        self.assertTrue(s.startswith("M "))
        self.assertTrue(s.endswith("\n"))

    def test_uses_11_decimal_places(self) -> None:
        s = format_moveto(1.0, 2.0)
        # "1.00000000000" — 11 decimals
        self.assertIn("1.00000000000", s)
        self.assertIn("2.00000000000", s)


class TestFormatCurveto(unittest.TestCase):
    def test_emits_three_control_points(self) -> None:
        s = format_curveto((1.0, 2.0), (3.0, 4.0), (5.0, 6.0))
        self.assertTrue(s.startswith("C "))
        self.assertIn("1.00000000000 2.00000000000", s)
        self.assertIn("3.00000000000 4.00000000000", s)
        self.assertIn("5.00000000000 6.00000000000", s)
        self.assertEqual(s.count(","), 2)
        self.assertTrue(s.endswith("\n"))


class TestBboxFromPoints(unittest.TestCase):
    def test_single_point(self) -> None:
        origin, size = bbox_from_points([(1.0, 2.0, 0.0)])
        self.assertEqual(origin, (1.0, 2.0, 0.0))
        self.assertEqual(size, (0.0, 0.0))

    def test_multiple_points(self) -> None:
        pts = [(0.0, 0.0, 0.0), (10.0, 5.0, 0.0), (-2.0, 8.0, 0.0)]
        origin, size = bbox_from_points(pts)
        # origin = (min_x, max_y, 0)
        self.assertEqual(origin, (-2.0, 8.0, 0.0))
        # size = (max_x - min_x, max_y - min_y)
        self.assertEqual(size, (12.0, 8.0))

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            bbox_from_points([])


if __name__ == "__main__":
    unittest.main()
