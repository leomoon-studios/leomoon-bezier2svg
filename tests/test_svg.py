"""Unit tests for `bezier2svg.core.svg`.

Loaded by file path so `bezier2svg/__init__.py` (which imports `bpy`) is not
triggered.
"""

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
        "svg.py",
    )
)
_spec = importlib.util.spec_from_file_location("svg", _MODULE_PATH)
assert _spec and _spec.loader
_svg = importlib.util.module_from_spec(_spec)
sys.modules["svg"] = _svg
_spec.loader.exec_module(_svg)
SVGFile = _svg.SVGFile
Layer = _svg.Layer


class TestLayer(unittest.TestCase):
    def test_layer_renders_title_and_path(self) -> None:
        out = str(Layer(title="curve1", path="M 0 0"))
        self.assertIn("<title>curve1</title>", out)
        self.assertIn('d="M 0 0"', out)
        self.assertIn('id="svg_curve1"', out)

    def test_layer_has_default_styling(self) -> None:
        out = str(Layer(title="t", path="M 1 2"))
        self.assertIn('fill="#fff"', out)
        self.assertIn('stroke="#000"', out)
        self.assertIn('stroke-width="1.5"', out)
        self.assertIn('opacity="0.5"', out)


class TestSVGFile(unittest.TestCase):
    def test_empty_document(self) -> None:
        doc = SVGFile(width=100, height=50)
        out = doc.to_string()
        self.assertIn('width="100"', out)
        self.assertIn('height="50"', out)
        self.assertIn("xmlns=\"http://www.w3.org/2000/svg\"", out)
        self.assertIn("<!-- Created with LeoMoon Bezier2SVG -->", out)
        self.assertIn("</svg>", out)

    def test_new_layer_appends_and_returns(self) -> None:
        doc = SVGFile(width=10, height=10)
        layer = doc.new_layer("a", "M 0 0")
        self.assertIsInstance(layer, Layer)
        self.assertEqual(len(doc.layers), 1)
        self.assertIs(doc.layers[0], layer)

    def test_to_string_includes_all_layers(self) -> None:
        doc = SVGFile(width=10, height=10)
        doc.new_layer("first", "M 0 0")
        doc.new_layer("second", "M 1 1")
        out = doc.to_string()
        self.assertIn("<title>first</title>", out)
        self.assertIn("<title>second</title>", out)


if __name__ == "__main__":
    unittest.main()
