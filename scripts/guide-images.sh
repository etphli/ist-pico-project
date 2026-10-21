#!/usr/bin/env bash
# Regenerate labelled assembly images from the current CAD registry.
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run --no-project --python 3.12 \
  --with "manifold3d==3.5.4" --with numpy --with trimesh --with matplotlib \
  python cad/assembly_guide_images.py "$@"
