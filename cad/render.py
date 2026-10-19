"""Matplotlib previews of the assembly (no GPU / CAD app needed)."""

import numpy as np


def _tris(m, max_tris=None):
    mesh = m.simplify(0.25).to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    f = np.asarray(mesh.tri_verts)
    return v[f]


def _shade(tris, base_rgb, light=np.array([0.4, -0.5, 0.8])):
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    light = light / np.linalg.norm(light)
    k = 0.45 + 0.55 * np.clip(np.abs(n @ light), 0, 1)
    return np.clip(np.outer(k, base_rgb), 0, 1)


def _hex(c):
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def _draw(ax, items, elev, azim, title):
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    # one collection for everything -> matplotlib depth-sorts per face, not per part
    tri_all, fc_all = [], []
    for tris, col, alpha in items:
        fc = np.hstack([_shade(tris, _hex(col)), np.full((len(tris), 1), alpha)])
        tri_all.append(tris)
        fc_all.append(fc)
    tri_all, fc_all = np.vstack(tri_all), np.vstack(fc_all)
    ax.add_collection3d(Poly3DCollection(tri_all, facecolors=fc_all, edgecolors="none"))
    allv = tri_all.reshape(-1, 3)
    lo, hi = allv.min(0), allv.max(0)
    c, r = (lo + hi) / 2, (hi - lo).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r)
    ax.set_ylim(c[1] - r, c[1] + r)
    ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_title(title, fontsize=9)


def render_all(built, parts, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    shells = {"front_shell", "rear_shell", "head_cap"}
    full, xray, internals = [], [], []
    for p in parts:
        if p.kind == "cal":
            continue
        tris = _tris(built[p.name])
        full.append((tris, p.colour, 1.0))
        if p.name in shells:
            xray.append((tris, p.colour, 0.10))
        else:
            xray.append((tris, p.colour, 1.0))
            internals.append((tris, p.colour, 1.0))

    fig = plt.figure(figsize=(14, 5), dpi=110)
    for i, (el, az, t) in enumerate([(12, 30, "front-left"), (12, 150, "rear-left (buttons, charge door)"),
                                     (12, 90, "left side")]):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        _draw(ax, full, el, az, t)
    fig.suptitle("Pip CAD v0.1 PROTOTYPE - assembled (placeholder dimensions, not fit-verified)", fontsize=10)
    fig.tight_layout()
    fig.savefig(out / "preview_assembly.png")
    plt.close(fig)

    fig = plt.figure(figsize=(14, 5), dpi=110)
    for i, (el, az, t) in enumerate([(15, 35, "x-ray front"), (15, 145, "x-ray rear"), (70, 90, "x-ray top")]):
        ax = fig.add_subplot(1, 3, i + 1, projection="3d")
        _draw(ax, xray, el, az, t)
    fig.suptitle("Pip CAD v0.1 - internals (shells transparent; orange/green/blue = bought-part envelopes)", fontsize=10)
    fig.tight_layout()
    fig.savefig(out / "preview_xray.png")
    plt.close(fig)

    # exploded print-part sheet
    printable = [p for p in parts if p.kind in ("print", "cal")]
    cols = 6
    rows = int(np.ceil(len(printable) / cols))
    fig = plt.figure(figsize=(16, 2.9 * rows), dpi=100)
    for i, p in enumerate(printable):
        ax = fig.add_subplot(rows, cols, i + 1, projection="3d")
        _draw(ax, [(_tris(built[p.name]), p.colour, 1.0)], 20, 35, f"{p.name} x{p.qty}")
    fig.suptitle("Pip CAD v0.1 - printable parts (assembly orientation)", fontsize=11)
    fig.tight_layout()
    fig.savefig(out / "preview_parts.png")
    plt.close(fig)
