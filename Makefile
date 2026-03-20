# LeoMoon Bezier2SVG — dev/build Makefile
#
# Common tasks:
#   make             # show this help
#   make venv        # create .venv and install ruff/mypy/pytest
#   make lint        # ruff check
#   make fix         # ruff check --fix
#   make test        # pytest
#   make test-blende # run integration scripts inside Blender (requires `make install`)
#   make check       # lint + test
#   make build       # build the extension .zip into ./dist/
#   make install     # build then install into the Blender user profile
#   make clean       # remove dist/, caches, built zips
#
# Override the Blender binary if it isn't on PATH:
#   make build BLENDER=/path/to/blender

BLENDER ?= /mnt/usrdrv/Portables-Lin/Graphic/blender-5.1.1-linux-x64/blender
PKG_DIR := bezier2svg
DIST_DIR := dist
VENV := .venv
PY := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
RUFF := $(VENV)/bin/ruff
PYTEST := $(VENV)/bin/pytest

.DEFAULT_GOAL := help

.PHONY: help venv lint fix test test-blender check build install clean tag

help:
	@awk 'BEGIN{FS=":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*##/ {printf "  %-14s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

venv: ## Create .venv and install dev tools
	python -m venv $(VENV)
	$(PIP) install --quiet --upgrade pip
	$(PIP) install --quiet ruff mypy pytest
	@echo "venv ready: $(VENV)"

lint: ## Run ruff
	$(RUFF) check $(PKG_DIR) tests

fix: ## Run ruff with --fix
	$(RUFF) check --fix $(PKG_DIR) tests

test: ## Run pytest
	$(PYTEST) -q tests --ignore=tests/blender

test-blender: ## Run Blender integration scripts (extension must be installed)
	@which $(BLENDER) >/dev/null 2>&1 || { echo "blender not found — set BLENDER=/path/to/blender"; exit 1; }
	@for s in tests/blender/smoke.py tests/blender/menu_check.py tests/blender/multi_object.py tests/blender/legacy_diff.py; do \
		echo "=== $$s ==="; \
		$(BLENDER) --background --factory-startup --python "$$s" || exit $$?; \
	done

check: lint test ## Lint + test

build: check ## Build the extension .zip into ./dist/ as leomoon-bezier2svg-<ver>_blender-<min>.zip
	@mkdir -p $(DIST_DIR)
	@which $(BLENDER) >/dev/null 2>&1 || { echo "blender not found — set BLENDER=/path/to/blender"; exit 1; }
	cd $(PKG_DIR) && $(BLENDER) --factory-startup --command extension build --output-dir ../$(DIST_DIR)
	@PLUGIN_VERSION=$$(grep -E '^version' $(PKG_DIR)/blender_manifest.toml | head -1 | sed -E 's/.*"([^"]+)".*/\1/'); \
	BLENDER_VERSION=$$(grep -E '^blender_version_min' $(PKG_DIR)/blender_manifest.toml | head -1 | sed -E 's/.*"([^"]+)".*/\1/'); \
	SRC="$(DIST_DIR)/leomoon_bezier2svg-$$PLUGIN_VERSION.zip"; \
	DST="$(DIST_DIR)/leomoon-bezier2svg-$${PLUGIN_VERSION}_blender-$${BLENDER_VERSION}.zip"; \
	mv -f "$$SRC" "$$DST"; \
	ls -lh "$$DST"

install: build ## Build then install into the running Blender user profile
	@ZIP=$$(ls -1t $(DIST_DIR)/leomoon-bezier2svg-*_blender-*.zip | head -1); \
	echo "Installing $$ZIP …"; \
	$(BLENDER) --command extension install-file --repo user_default --enable "$$ZIP"

tag: ## Create an annotated git tag from the manifest version (does NOT push)
	@VERSION=$$(grep -E '^version' $(PKG_DIR)/blender_manifest.toml | head -1 | sed -E 's/.*"([^"]+)".*/\1/'); \
	echo "Tagging v$$VERSION …"; \
	git tag -a "v$$VERSION" -m "LeoMoon Bezier2SVG v$$VERSION"; \
	echo "Done. Push with: git push origin v$$VERSION"

clean: ## Remove build artifacts and caches
	rm -rf $(DIST_DIR) .ruff_cache .mypy_cache .pytest_cache tests/_out
	rm -f $(PKG_DIR)/*.zip
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
