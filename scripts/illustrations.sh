#!/usr/bin/env bash
# Regenerate the wiring diagrams and assembly-detail images (illustrations/README.md).
# Needs `uv` (https://docs.astral.sh/uv/). Dependencies live in a throwaway uv
# environment; nothing is installed system-wide.
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run --no-project --python 3.12 \
  --with "manifold3d==3.5.4" --with "numpy==2.5.4" --with "matplotlib==3.11.2" --with trimesh \
  python illustrations/build.py "$@"
