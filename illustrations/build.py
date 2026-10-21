"""Regenerate Pip illustrations. Run scripts/illustrations.sh from anywhere.

  scripts/illustrations.sh                    # everything (CAD renders take a few minutes)
  scripts/illustrations.sh --set wiring       # wiring | vectors | cad
  scripts/illustrations.sh --only 04-body-power-split 08-cable-route
  scripts/illustrations.sh --strict           # exit 1 if any label overlaps or leaves the canvas
"""

import argparse
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
os.chdir(REPO)
sys.path.insert(0, str(HERE))


def registry(sets):
    out = {}
    if "wiring" in sets:
        import wiring
        out.update(wiring.ALL)
    if "vectors" in sets:
        import assembly_vectors
        out.update(assembly_vectors.ALL)
    if "cad" in sets:
        import assembly_cad
        out.update(assembly_cad.ALL)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--set", nargs="+", choices=["wiring", "vectors", "cad"], default=["wiring", "vectors", "cad"])
    ap.add_argument("--only", nargs="+", help="image stems to regenerate")
    ap.add_argument("--strict", action="store_true", help="fail on label collisions")
    args = ap.parse_args()
    sets = args.set
    if args.only:
        sets = ["wiring", "vectors", "cad"]
    reg = registry(sets)
    names = args.only or list(reg)
    unknown = [n for n in names if n not in reg]
    if unknown:
        ap.error(f"unknown image(s): {', '.join(unknown)}")
    failed = 0
    for name in names:
        files, problems = reg[name]()
        rel = ", ".join(str(f) for f in files)
        print(f"{name}: {rel}", flush=True)
        for p in problems:
            print(f"   ! {p}")
        failed += bool(problems)
    if failed:
        print(f"{failed} image(s) with label problems")
        if args.strict:
            sys.exit(1)


if __name__ == "__main__":
    main()
