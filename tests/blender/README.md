# Blender integration scripts

These scripts run inside a real Blender process to verify the installed
extension end-to-end. They are **not** picked up by `pytest` (no `test_*.py`
prefix) so they do not run in CI.

Run them via the Makefile after installing the extension:

```bash
make install            # build + install into Blender user profile
make test-blender       # run all scripts in this folder
```

Or invoke a single script directly:

```bash
BLENDER=/path/to/blender
$BLENDER --background --factory-startup --python tests/blender/smoke.py
```

Each script writes its scratch SVGs to `tests/_out/` (gitignored) and exits
non-zero on failure.

| Script             | Purpose                                                        |
| ------------------ | -------------------------------------------------------------- |
| `smoke.py`         | Enable extension, export one bezier curve, sanity-check SVG    |
| `menu_check.py`    | Verify menu wiring + operator label/description/defaults       |
| `multi_object.py`  | Mixed bezier/non-bezier scene, check warnings + layer naming   |
| `legacy_diff.py`   | Diff new extension SVG against legacy plugin (byte-identical)  |
