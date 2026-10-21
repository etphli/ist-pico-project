#!/usr/bin/env bash
# Regenerate the self-contained viewer. Its vendored renderer needs no network.
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run --no-project --python 3.12 \
  --with "manifold3d==3.5.4" --with numpy \
  python cad/export_viewer.py "$@"
