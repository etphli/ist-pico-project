# Open and edit the Pip section viewer

Download [index.html](index.html), then open the downloaded file in a browser with WebGL 2. The file contains the renderer and the CAD meshes. Viewing needs no server, internet connection, or Python installation. GitHub shows the HTML source, so use its **Download raw file** action before opening it locally.

Use **X section**, **Y section**, or **X + Y cut** to start. Each axis has its own enable checkbox, position slider, and retained-side selector. Z works independently too. Ochre caps show exposed printed material. Purchased envelopes retain their own colours on the cut faces.

Drag to orbit, shift-drag or right-drag to pan, and scroll to zoom. Touch supports one-finger orbit and two-finger pan and pinch. Focus the model to use arrow keys for orbit, `+` and `-` for zoom, and `Home` to fit. Click a visible part or its list entry to inspect its label, bounds, and notes. Use the visibility checkboxes, **Hide covers**, **Isolate**, and **Fit part** to reach smaller details. **Reset all** restores the assembly. **Save PNG** exports the current model view on a pale background.

## Change the source

Edit the readable files below, then regenerate. `index.html` is an output file.

| Change | File |
|---|---|
| Page layout, colours, type, help, responsive layout | [template.html](template.html), inline CSS and HTML |
| Cut planes, caps, camera controls, selection, visibility, export | [viewer.js](viewer.js) |
| Friendly purchased-part labels | [../export_viewer.py](../export_viewer.py), `LABELS` |
| Group membership and which parts count as covers | [../export_viewer.py](../export_viewer.py), `group_for` and `SHELLS` |
| Printed-part labels | [../export_viewer.py](../export_viewer.py), the `label` field in `entry` |
| Part colours, notes, and assembled instances | [../pip_robot/assembly.py](../pip_robot/assembly.py), `PARTS` |
| Dimensions and actual part geometry | [../pip_robot/params.py](../pip_robot/params.py) and [../pip_robot/parts.py](../pip_robot/parts.py) |
| Browser checks | [browser-check.js](browser-check.js) |
| Export fidelity check | [verify_export.py](verify_export.py) |

From the repository root, run:

```bash
scripts/viewer.sh
```

The command uses `uv`, Python 3.12, manifold3d 3.5.4, and NumPy. The first run can download those packages. The renderer is already vendored, so regeneration needs no Node build step. Reopen or refresh `index.html` after regeneration.

The exporter overwrites `index.html` and `model-manifest.json`. An optional `--output /path/to/index.html` writes both outputs beside that alternate file. Keep the source files when sharing an editable copy. Sharing only `index.html` is sufficient for viewing.

## Check a change

Run the mesh comparison from the repository root:

```bash
uv run --no-project --python 3.12 --with manifold3d==3.5.4 --with numpy \
  python cad/viewer/verify_export.py
node --check cad/viewer/viewer.js
node --check cad/viewer/browser-check.js
```

The comparison checks every embedded vertex and triangle index against the current CAD registry, checks source hashes, and rejects external script or stylesheet dependencies. It also checks that every non-calibration registry entry appears exactly once.

For browser checks, serve the repository:

```bash
python3 -m http.server 8766 --bind 127.0.0.1
```

Open `http://127.0.0.1:8766/cad/viewer/index.html`. Run the contents of `browser-check.js` as an expression through T3 `preview_evaluate` with `awaitPromise: true`, or paste it into the browser console. Keep the tab visible because its checks await rendered frames. The script exercises all three cut planes, independent X and Y movement, direction reversal, rendered cut-face changes, group visibility, search, selection, isolation, reset, keyboard orbit, wheel zoom, axes, and PNG generation. It restores the assembly afterward. It is intended for this v0.3 export, so update its expected counts when the registry changes.

Inspect at desktop and phone widths, including a quarter cut and covers off. Check mouse pan and touch gestures on actual input hardware. Automated checks do not establish the feel of those gestures.

[Quarter-cut PNG evidence](evidence/quarter-cut.png) is an actual image produced by the viewer's PNG export. [Verification notes](VERIFICATION.md) record the checks and tool limitations.

## Understand the geometry and its limits

This viewer exports the assembled positions from `Part.make()` and `Manifold.to_mesh()`. It does not use the printable STLs, which are rotated and moved onto a print bed. No mesh simplification or illustrative replacement geometry is applied.

The current export has 44 registry entries and 57,330 triangles. Those entries comprise 34 printed parts or assembly instances and 10 purchased envelope entries. These are entry counts, not a purchased-parts count. Some entries contain multiple envelopes, such as the controller with Pico and switch, the pair of rear buttons, five front modules, and two base modules. Calibration coupons are excluded. `model-manifest.json` records labels, kinds, bounds, notes, counts, and SHA-256 hashes of the four geometry source files.

The atmospheric module has no placement envelope in the CAD. The viewer also omits the switch holder, cables, hook-and-loop straps, screws, adhesives, and bank-fit keep-out volumes. Printed motor straps are included. The switch actuator is a concept part, and the switch knob appears within the controller envelope.

All purchased envelopes use placeholder dimensions and placements. The QW01 bank uses the user's approximate dimensions. Section caps come from stencil rendering of the watertight meshes, following the [Three.js clipping stencil example](https://threejs.org/examples/webgl_clipping_stencil.html). Caps are display effects and do not modify or export sliced solids. Exact coincident faces can flicker. Move the plane by a fraction of a millimetre to inspect an adjacent section.

The viewer establishes no physical fit, screw engagement, continuous motion clearance, cable routing, strength, or printability. Browser performance depends on WebGL 2 and the graphics device. Rendering happens only after an interaction or resize.

## Renderer provenance

`vendor/three-0.180.0.min.js` is Three.js 0.180.0, bundled from its published `build/three.cjs` with esbuild 0.25.11. Its [MIT licence](vendor/THREE-LICENSE.txt) is included. This is the only minified source. The handwritten viewer source is separate and formatted for editing.

GPT-6.1 Sol wrote the viewer, exporter, and viewer checks. The CAD geometry predates this viewer and remains in the existing parametric source files.
