# Pip CAD v0.1 (parametric prototype)

**Status: prototype, not fit-verified.** Bought-part dimensions are placeholders (`# MEASURE` in `pip_robot/params.py`). Print `fit_test_coupon.stl` first, then follow `docs/12-measurement-calibration-checklist.md`.

## Build

```bash
scripts/cad.sh                 # build all parts + checks + PNG previews
scripts/cad.sh --no-render     # faster
```
Requires [`uv`](https://docs.astral.sh/uv/). The script makes a throwaway Python 3.12 environment with manifold3d 3.5.4, numpy, trimesh and matplotlib. Nothing is installed system-wide. A full build takes a few seconds.

## Files

| Path | What |
|---|---|
| `pip_robot/params.py` | **All dimensions.** Edit here. |
| `pip_robot/prims.py` | Geometry helpers |
| `pip_robot/parts.py` | One function per part, in assembly coordinates |
| `pip_robot/assembly.py` | Part registry: qty, colour, print orientation, expected contacts |
| `build.py` | Exports STLs, validates, writes `out/validation_report.md` |
| `render.py` | Matplotlib previews |
| `out/stl/*.stl` | Printable parts, already oriented for printing (generated) |
| `out/assembly_preview.stl` | All parts + bought-part envelopes in position (one mesh, for viewing) |
| `out/preview_*.png` | Assembly, x-ray, part sheet |
| `out/validation_report.md` | Checks and their results |

## What the validation does (and does not) prove

It checks that every part is a valid closed mesh (manifold3d, then re-checked independently with trimesh), that no two parts overlap unexpectedly in the assembly, that the casters can swivel a full turn and the head can pan ±70° without collisions, a few clearances, and a static tip-angle **estimate**.

It does **not** prove that the real parts fit (placeholders), that parts print well (no slicer was run), or that parts are strong enough (no FEA). The interlock and the switch actuator are concepts.

## Coordinates

Origin on the floor at the robot centre; +X forward (face), +Y left, +Z up; millimetres.
