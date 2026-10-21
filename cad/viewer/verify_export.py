#!/usr/bin/env python3
"""Check the generated document against every current CAD registry mesh."""
import base64
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pip_robot.assembly import PARTS  # noqa: E402

html = (HERE / "index.html").read_text()
model = json.loads(re.search(r'<script id="model-data" type="application/json">(.*?)</script>', html, re.S)[1])
expected = [p for p in PARTS if p.kind != "cal"]
assert [p["name"] for p in model["parts"]] == [p.name for p in expected]
for exported, part in zip(model["parts"], expected):
    mesh = part.make().to_mesh()
    vertices = np.frombuffer(base64.b64decode(exported["vertices"]), dtype="<f4").reshape(-1, 3)
    indices = np.frombuffer(base64.b64decode(exported["indices"]), dtype="<u4").reshape(-1, 3)
    np.testing.assert_array_equal(vertices, np.asarray(mesh.vert_properties)[:, :3].astype("<f4"))
    np.testing.assert_array_equal(indices, np.asarray(mesh.tri_verts).astype("<u4"))
    assert exported["triangles"] == len(indices)
    assert (exported["kind"] == "placeholder") == (part.kind == "ref")
for relative, digest in model["sourceHashes"].items():
    assert hashlib.sha256((HERE.parent / relative).read_bytes()).hexdigest() == digest, relative
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=', html), "External renderer dependency found"
assert not any(marker in html for marker in ("/* THREE_LIBRARY */", "/* MODEL_DATA */", "/* VIEWER_CODE */"))
print(f"PASS: {len(expected)} entries and every vertex/index match the current CAD; source hashes match; no external scripts/styles.")
