"""Pure-Python SVG document model. No `bpy` import."""

from __future__ import annotations

from dataclasses import dataclass, field

_SVG_TEMPLATE = """
<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
 <!-- Created with LeoMoon Bezier2SVG -->

{layers}
</svg>
"""

_LAYER_TEMPLATE = """
 <g>
 <title>{title}</title>
 <path fill="#fff" stroke="#000" stroke-width="1.5" opacity="0.5" d="{path}" id="svg_{title}"/>
 </g>
"""


@dataclass
class Layer:
    title: str
    path: str

    def __str__(self) -> str:
        return _LAYER_TEMPLATE.format(title=self.title, path=self.path)


@dataclass
class SVGFile:
    width: float
    height: float
    layers: list[Layer] = field(default_factory=list)

    def new_layer(self, title: str, path: str) -> Layer:
        layer = Layer(title=title, path=path)
        self.layers.append(layer)
        return layer

    def to_string(self) -> str:
        return _SVG_TEMPLATE.format(
            width=self.width,
            height=self.height,
            layers="".join(str(layer) for layer in self.layers),
        )
