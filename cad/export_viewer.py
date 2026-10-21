#!/usr/bin/env python3
"""Export the registry's exact assembled meshes into one offline section viewer."""
import argparse
import base64
import hashlib
import json
from pathlib import Path

import numpy as np

from pip_robot import params
from pip_robot.assembly import PARTS

HERE = Path(__file__).resolve().parent
VIEWER = HERE / "viewer"
SHELLS = {"front_shell", "rear_shell", "head_cap", "rear_hatch"}
LABELS = {
    "ref_power_bank": "MINISO QW01 power bank",
    "ref_tt_motor_L": "Left TT motor", "ref_tt_motor_R": "Right TT motor",
    "ref_controller": "Controller + Pico + switch",
    "ref_buttons": "Rear PiicoDev buttons, pair",
    "ref_servo": "FS90 servo + horn",
    "ref_cam_board": "Camera / mic / amplifier board",
    "ref_head_speaker": "Head speaker",
    "ref_front_modules": "Front modules, five envelopes",
    "ref_base_modules": "Base modules, two envelopes",
}


def group_for(part):
    if part.kind == "ref":
        return "Purchased envelopes"
    if part.name in SHELLS:
        return "Outer covers"
    if any(token in part.name for token in ("wheel", "caster", "motor_strap")):
        return "Drive and casters"
    if any(token in part.name for token in ("head_", "eye_", "clutch")):
        return "Head internals"
    return "Body structure"


def encode(array, dtype):
    return base64.b64encode(np.asarray(array, dtype=dtype).tobytes()).decode("ascii")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=VIEWER / "index.html")
    args = parser.parse_args()
    entries, bounds = [], []
    for part in PARTS:
        if part.kind == "cal":
            continue
        solid = part.make()
        if str(solid.status()).split(".")[-1] != "NoError" or solid.is_empty():
            raise RuntimeError(f"Cannot export invalid part {part.name}")
        mesh = solid.to_mesh()
        vertices = np.asarray(mesh.vert_properties)[:, :3]
        faces = np.asarray(mesh.tri_verts)
        low, high = vertices.min(axis=0), vertices.max(axis=0)
        bounds.extend((low, high))
        entry = dict(name=part.name, label=LABELS.get(part.name, part.name.replace("_", " ")),
                     kind="placeholder" if part.kind == "ref" else "printed",
                     instance=part.kind == "inst", group=group_for(part), colour=part.colour,
                     notes=part.notes or ("Purchased-part PLACEHOLDER envelope. Measure the real item before confirming fit."
                                         if part.kind == "ref" else "Printed assembly instance."),
                     bounds=[low.tolist(), high.tolist()], triangles=len(faces),
                     vertices=encode(vertices, "<f4"), indices=encode(faces, "<u4"))
        entries.append(entry)
    sources = [HERE / "pip_robot" / name for name in ("params.py", "prims.py", "parts.py", "assembly.py")]
    hashes = {str(path.relative_to(HERE)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    data = dict(version=params.VERSION, units="mm", coordinateSystem="+X forward, +Y robot left, +Z up",
                bounds=[np.min(bounds, axis=0).tolist(), np.max(bounds, axis=0).tolist()],
                sourceHashes=hashes, parts=entries)
    manifest = dict(version=data["version"], units="mm", coordinateSystem=data["coordinateSystem"],
                    bounds=data["bounds"], sourceHashes=hashes,
                    parts=[{k: v for k, v in p.items() if k not in ("vertices", "indices")} for p in entries])
    template = (VIEWER / "template.html").read_text()
    library = (VIEWER / "vendor" / "three-0.180.0.min.js").read_text()
    script = (VIEWER / "viewer.js").read_text()
    html = template.replace("/* THREE_LIBRARY */", library).replace("/* MODEL_DATA */", json.dumps(data, separators=(",", ":"))).replace("/* VIEWER_CODE */", script)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html)
    (args.output.parent / "model-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Exported {len(entries)} assembly entries, {sum(p['triangles'] for p in entries):,} triangles to {args.output}")
    print(f"Includes {sum(p['kind'] == 'placeholder' for p in entries)} purchased envelope entries; calibration coupons excluded.")


if __name__ == "__main__":
    main()
