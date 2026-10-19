#!/usr/bin/env bash
# Build + validate + render the Pip CAD model in a throwaway Python environment.
# Needs `uv` (https://docs.astral.sh/uv/). Nothing is installed system-wide.
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run --no-project --python 3.12 \
  --with "manifold3d==3.5.4" --with numpy --with trimesh --with matplotlib \
  python cad/build.py "$@"
