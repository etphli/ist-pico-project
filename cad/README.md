# Pip CAD v0.2 (parametric prototype)

**Status: prototype, not fit-verified.** Bought-part dimensions and positions are placeholders (`# MEASURE` in `pip_robot/params.py`). Print `fit_test_coupon.stl` first, then follow `docs/12-measurement-calibration-checklist.md`.

## Build

```bash
scripts/cad.sh                 # build all parts + checks + previews (~3 min, mostly rendering)
scripts/cad.sh --no-render     # build + checks only
```
Requires [`uv`](https://docs.astral.sh/uv/). The script runs Python 3.12 with manifold3d 3.5.4, numpy, trimesh and matplotlib in a throwaway environment. Nothing is installed system-wide.

## Files

| Path | What |
|---|---|
| `pip_robot/params.py` | All dimensions. Edit here. |
| `pip_robot/prims.py` | Geometry helpers |
| `pip_robot/parts.py` | One function per part, in assembly coordinates; FOV cone helper |
| `pip_robot/assembly.py` | Part registry (qty, colour, print orientation) and the intended-contact list with reasons |
| `build.py` | Exports STLs, runs the checks, writes `out/validation_report.md` |
| `render.py` | Per-pixel z-buffer previews and true cross-sections (matplotlib only for layout) |
| `out/stl/*.stl` | Printable parts in print orientation (generated; stale files are deleted on each build) |
| `out/assembly_preview.stl` | All parts + bought-part envelopes in position (one mesh) |
| `out/preview_assembly.png`, `preview_xray.png`, `preview_parts.png` | Shaded views |
| `out/preview_front_reference.png` | Orthographic front/rear/head elevations with labelled openings |
| `out/preview_sections.png` | Manifold slices through the head/camera and the centre line, with FOV lines |
| `out/validation_report.md` | Check results and their limits |

## What the checks do and do not establish

Done: mesh validity (manifold3d, then trimesh on the exported STLs). Bed fit by bounding box, comparing sorted footprint dimensions elementwise, with a self-test. Pairwise overlaps > 1 mm³ outside the intended-contact list; every intended contact is printed with its overlap volume and reason. Selected gaps. Caster swivel and head pan **sampled** every 5°. A geometric camera FOV cone.

Not established: real fit (placeholders); that intended-contact overlaps are correct fits; continuous motion clearance; cable routing; screw engagement or strength; printability (no slicer); strength (no FEA); real camera image.

The previews are faithful to the meshes. v0.1's "red triangle" artifacts came from matplotlib's per-triangle depth sorting, not from the geometry.

## Coordinates

Origin on the floor at the robot centre; +X forward (face), +Y robot's left, +Z up; millimetres.
