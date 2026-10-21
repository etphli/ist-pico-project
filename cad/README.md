# Pip CAD v0.3 (parametric prototype)

**Status: prototype, not fit-verified.** Bought-part dimensions and positions are placeholders (`# MEASURE` in `pip_robot/params.py`). The owned MINISO QW01 power bank is modelled from the user's **approximate** size (about 130 × 60 × 10 mm) with an accommodation band and printed shims; its real size, port positions and mass are not measured. Print `fit_test_coupon.stl` first, then follow `docs/12-measurement-calibration-checklist.md`.

## Build

```bash
scripts/cad.sh                 # build all parts + checks + previews (~3 min, mostly rendering)
scripts/cad.sh --no-render     # build + checks only
scripts/cad.sh --bank-fit-only # QW01 cradle regression only (~20 s, writes nothing)
```
Requires [`uv`](https://docs.astral.sh/uv/). The script runs Python 3.12 with manifold3d 3.5.4, numpy, trimesh and matplotlib in a throwaway environment. Nothing is installed system-wide.

## Files

| Path | What |
|---|---|
| `pip_robot/params.py` | All dimensions. Edit here. |
| `pip_robot/prims.py` | Geometry helpers |
| `pip_robot/parts.py` | One function per part, in assembly coordinates; FOV cone helper |
| `pip_robot/assembly.py` | Part registry (qty, colour, print orientation) and the intended-contact list with reasons |
| `pip_robot/bankfit.py` | QW01 bank-fit regression: accommodation envelopes vs structure (report §3d) |
| `build.py` | Exports STLs, runs the checks, writes `out/validation_report.md` |
| `render.py` | Per-pixel z-buffer previews and true cross-sections (matplotlib only for layout) |
| `out/stl/*.stl` | Printable parts in print orientation (generated; stale files are deleted on each build) |
| `out/assembly_preview.stl` | All parts + bought-part envelopes in position (one mesh) |
| `out/preview_assembly.png`, `preview_xray.png`, `preview_parts.png` | Shaded views |
| `out/preview_front_reference.png` | Orthographic front/rear/head elevations with labelled openings |
| `out/preview_sections.png` | Manifold slices through the head/camera and the centre line, with FOV lines |
| `out/preview_bank_fit.png` | QW01 cradle sections with the keep-out outlines; rear with the hatch removed |
| `out/assembly_parts.json`, `out/bank_fit.json` | Part metadata (qty, print rotation, bbox, notes); bank parameters and regression results |
| `out/validation_report.md` | Check results and their limits |

## What the checks do and do not establish

Done: QW01 bank-fit regression: the largest accommodated bank, a plug-and-bend sweep over every assumed port position, the open end face, the access path with the hatch off, the lead route and the strap path are each checked for zero overlap with every part. Cradle margins, floor support and filler gaps are also checked. A built-in check confirms it still detects the v0.2 bank-position collision. Mesh validity (manifold3d, then trimesh on the exported STLs). Bed fit by bounding box, comparing sorted footprint dimensions elementwise, with a self-test. Pairwise overlaps > 1 mm³ outside the intended-contact list; every intended contact is printed with its overlap volume and reason. Selected gaps. Caster swivel and head pan **sampled** every 5°. A geometric camera FOV cone.

Not established: real fit (placeholders; the bank size is a user estimate); that intended-contact overlaps are correct fits; continuous motion clearance; cable routing; screw engagement or strength; printability (no slicer); strength (no FEA); real camera image.

The previews are faithful to the meshes. v0.1's "red triangle" artifacts came from matplotlib's per-triangle depth sorting, not from the geometry.

## Coordinates

Origin on the floor at the robot centre; +X forward (face), +Y robot's left, +Z up; millimetres.
