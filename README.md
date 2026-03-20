# LeoMoon Bezier2SVG for Blender

## Introduction

LeoMoon Bezier2SVG is a free Blender plugin that exports bezier curves directly to SVG. Useful for taking precisely-shaped curves out of Blender into vector design tools, web graphics, cutting/plotting software, or anywhere else that consumes SVG.

More info / download: https://leomoon.com/downloads/plugins/leomoon-bezier2svg/

## Features

- Export selected curves or all visible curves
- Project along any global axis (`Z`, `-Z`, `X`, `-X`, `Y`, `-Y`) or along the active 3D viewport
- Configurable scale (px / Blender unit)
- Each Blender curve becomes its own SVG `<g>` layer, titled with the object name
- Cubic bezier path output (`M` + `C`) using Blender's native handle data
- Closed curves (`use_cyclic_u`) are correctly closed
- Non-bezier splines are skipped with a warning per object

## Changelog

- 2.0.0 2026-04-12: Ported to Blender 5.1+ modern extension format
- 1.4.0 2023-03-09: Fixed expression and animation lag when rendering
- 1.3.6 2021-06-03: Fixed compatibility issue for Blender 2.93 and 3.0
- 1.3.5: Fixed text grouping bug
- 1.3.4: Fixed dynamic section not updating while rendering
- 1.3.3: Fixed animation not updating while rendering
- 1.3.2: Fixed Blender 2.80 API warnings
- 1.3.1: Added support for Blender 2.8 and bug fixes
- 1.3.0: Improved abbreviation support with decimals
- 1.2.0: Time counter with many options
- 1.1.0: Overriding counter with lines from text file
- 1.0.0: First public release

## Usage

> **Blender 5.1+ (extension format):** Install from the [Releases page](https://github.com/leomoon-studios/leomoon-bezier2svg/releases). Do **not** use the green "Code → Download ZIP" button. That downloads the source, not the installable extension.

1. Download `leomoon-bezier2svg-X.Y.Z_blender-A.B.C.zip` from the Releases page.
2. In Blender, open `Edit → Preferences → Get Extensions`.
3. Click the **▼ dropdown arrow** in the **top-right corner** of the panel (next to the **Repositories** selector) and choose **Install from Disk…**.
4. Select the downloaded `.zip`. The extension is enabled automatically and appears under the **Installed** section.
5. Open **File → Export → Bezier2SVG (.svg)**, choose options, and save.

## Compatibility

Tested with Blender 5.1.1.

## Development

```bash
make venv     # create .venv with ruff + pytest
make check    # ruff lint + pytest
make build    # build dist/leomoon-bezier2svg-<ver>_blender-<min>.zip
make install  # build and install into the Blender user profile
make tag      # create an annotated git tag from the manifest version
```

Override the Blender binary if it isn't on `PATH`:

```bash
make build BLENDER=/path/to/blender
```
