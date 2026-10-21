"""Previews of the assembly with a small numpy z-buffer rasteriser (no GPU / CAD app).

Why a rasteriser: matplotlib's 3D polygon collections sort whole triangles by depth
(painter's algorithm). Around openings this draws hidden faces in front of visible
ones, which made the v0.1 belly cutouts look like red triangles. Here every pixel keeps
the nearest surface, so openings, pockets and modules behind windows show truthfully.
The meshes are the exact exported geometry (no simplification).

Outputs (cad/out/):
  preview_assembly.png         shaded views of the assembled robot
  preview_xray.png             shells and head cap transparent
  preview_front_reference.png  orthographic front / rear / head elevations with labelled openings
  preview_sections.png         true cross-sections (manifold slices) incl. camera FOV lines
  preview_bank_fit.png         QW01 cradle: sections with the bank-fit keep-outs, rear with the hatch off
  preview_parts.png            every printable part
"""

import math

import numpy as np

BG = np.array([0.97, 0.97, 0.96])


def _corner_normals(tris, crease_deg=32):
    """Area-weighted display normals, with sharp edges preserved. Meshes stay unchanged."""
    face_vectors = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    unit = face_vectors / (np.linalg.norm(face_vectors, axis=1, keepdims=True) + 1e-12)
    _, vertex_ids = np.unique(tris.reshape(-1, 3), axis=0, return_inverse=True)
    order = np.argsort(vertex_ids, kind="stable")
    boundaries = np.r_[0, np.flatnonzero(np.diff(vertex_ids[order])) + 1, len(order)]
    result = np.empty((len(tris) * 3, 3))
    threshold = math.cos(math.radians(crease_deg))
    for start, stop in zip(boundaries[:-1], boundaries[1:]):
        corners = order[start:stop]
        faces = corners // 3
        adjacent = unit[faces]
        weights = (adjacent @ adjacent.T >= threshold).astype(float)
        normal = weights @ face_vectors[faces]
        result[corners] = normal / (np.linalg.norm(normal, axis=1, keepdims=True) + 1e-12)
    return result.reshape(-1, 3, 3)


def _studio_brightness(normals, basis):
    r, u, d = basis
    nv = np.stack([normals @ r, normals @ u, normals @ d], axis=-1)
    nv[nv[..., 2] < 0] *= -1
    key = np.array([-0.45, 0.65, 0.70])
    fill = np.array([0.65, 0.15, 0.55])
    key /= np.linalg.norm(key)
    fill /= np.linalg.norm(fill)
    return 0.32 + 0.51 * np.clip(nv @ key, 0, 1) + 0.17 * np.clip(nv @ fill, 0, 1)


# --------------------------------------------------------------------------- geometry
def _tris(m):
    mesh = m.to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3].astype(np.float64)
    f = np.asarray(mesh.tri_verts).astype(np.int64)
    return v[f]


def _hex(c):
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) / 255 for i in (0, 2, 4)])


def _basis(elev, azim):
    """Orthographic camera. Returns (right, up, toward_viewer) unit vectors.
    azim is measured from +X toward +Y; elev above the horizon. azim=0 looks at the face."""
    e, a = math.radians(elev), math.radians(azim)
    d = np.array([math.cos(e) * math.cos(a), math.cos(e) * math.sin(a), math.sin(e)])
    r = np.array([-math.sin(a), math.cos(a), 0.0])
    u = np.cross(d, r)
    return r, u, d


# --------------------------------------------------------------------------- rasteriser
def _raster(tri2, tz, W, H):
    """tri2: (T,3,2) pixel coords, tz: (T,3) depth (larger = nearer).
    Returns depth buffer (H,W) and triangle-id buffer (H,W, -1 = empty)."""
    depth = np.full(H * W, -np.inf)
    tid = np.full(H * W, -1, dtype=np.int64)
    x0 = np.floor(tri2[:, :, 0].min(1)).astype(np.int64)
    x1 = np.ceil(tri2[:, :, 0].max(1)).astype(np.int64)
    y0 = np.floor(tri2[:, :, 1].min(1)).astype(np.int64)
    y1 = np.ceil(tri2[:, :, 1].max(1)).astype(np.int64)
    keep = (x1 >= 0) & (y1 >= 0) & (x0 < W) & (y0 < H)
    span = np.maximum(x1 - x0, y1 - y0) + 1
    ax, ay = tri2[:, 0, 0], tri2[:, 0, 1]
    bx, by = tri2[:, 1, 0], tri2[:, 1, 1]
    cx, cy = tri2[:, 2, 0], tri2[:, 2, 1]
    area = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
    keep &= np.abs(area) > 1e-12
    pix_all, dep_all, id_all = [], [], []
    lo = 0
    for S in (2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096):
        sel = np.nonzero(keep & (span > lo) & (span <= S))[0]
        lo = S
        if len(sel) == 0:
            continue
        oy, ox = np.divmod(np.arange(S * S), S)
        chunk = max(1, int(3e6 // (S * S)))
        for i in range(0, len(sel), chunk):
            t = sel[i:i + chunk]
            px = x0[t, None] + ox[None, :]
            py = y0[t, None] + oy[None, :]
            qx, qy = px + 0.5, py + 0.5
            w0 = ((bx[t, None] - qx) * (cy[t, None] - qy) - (by[t, None] - qy) * (cx[t, None] - qx)) / area[t, None]
            w1 = ((cx[t, None] - qx) * (ay[t, None] - qy) - (cy[t, None] - qy) * (ax[t, None] - qx)) / area[t, None]
            w2 = 1.0 - w0 - w1
            ins = (w0 >= -1e-9) & (w1 >= -1e-9) & (w2 >= -1e-9) & (px >= 0) & (py >= 0) & (px < W) & (py < H)
            if not ins.any():
                continue
            z = w0 * tz[t, 0, None] + w1 * tz[t, 1, None] + w2 * tz[t, 2, None]
            r, c = np.nonzero(ins)
            pix_all.append(py[r, c] * W + px[r, c])
            dep_all.append(z[r, c])
            id_all.append(t[r])
    if pix_all:
        pix = np.concatenate(pix_all)
        dep = np.concatenate(dep_all)
        ids = np.concatenate(id_all)
        order = np.lexsort((-dep, pix))
        pix, dep, ids = pix[order], dep[order], ids[order]
        first = np.ones(len(pix), bool)
        first[1:] = pix[1:] != pix[:-1]
        depth[pix[first]] = dep[first]
        tid[pix[first]] = ids[first]
    return depth.reshape(H, W), tid.reshape(H, W)


def _shade(tris_world, cols, basis):
    r, u, d = basis
    n = np.cross(tris_world[:, 1] - tris_world[:, 0], tris_world[:, 2] - tris_world[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    nv = np.stack([n @ r, n @ u, n @ d], axis=1)
    nv[nv[:, 2] < 0] *= -1                              # two-sided lighting
    light = np.array([-0.35, 0.55, 0.76])
    light /= np.linalg.norm(light)
    k = 0.38 + 0.62 * np.clip(nv @ light, 0, 1)
    return np.clip(cols * k[:, None], 0, 1), nv


def render(items, elev, azim, px_per_mm=3.0, bounds=None, ss=2, edges=True, bg=BG):
    """items: list of (tris (T,3,3), colour hex, alpha). alpha < 1 items are drawn as a
    transparent layer over the opaque image. Returns (rgb image, extent (mm), bounds)."""
    basis = _basis(elev, azim)
    r, u, d = basis
    opaque = [(t, c) for t, c, a in items if a >= 1.0]
    trans = [(t, c, a) for t, c, a in items if a < 1.0]
    allv = np.vstack([t.reshape(-1, 3) for t, _, _ in items])
    sx, sy = allv @ r, allv @ u
    if bounds is None:
        pad = 6.0
        bounds = (sx.min() - pad, sx.max() + pad, sy.min() - pad, sy.max() + pad)
    bx0, bx1, by0, by1 = bounds
    s = px_per_mm * ss
    W = int(math.ceil((bx1 - bx0) * px_per_mm)) * ss
    H = int(math.ceil((by1 - by0) * px_per_mm)) * ss

    def layer(group):
        tris = np.vstack([t for t, *_ in group])
        cols = np.vstack([np.tile(_hex(c), (len(t), 1)) for t, c, *_ in group])
        brightness = np.vstack([_studio_brightness(_corner_normals(t), basis) for t, *_ in group])
        p2 = np.stack([(tris @ r - bx0) * s, (by1 - tris @ u) * s], axis=-1)
        dep, tid = _raster(p2, tris @ d, W, H)
        fc, nv = _shade(tris, cols, basis)
        return dep, tid, cols, nv, p2, brightness

    def shaded_pixels(tid, cols, p2, brightness, hit):
        yy, xx = np.nonzero(hit)
        ids = tid[hit]
        p = p2[ids]
        ax, ay = p[:, 0, 0], p[:, 0, 1]
        bx, by = p[:, 1, 0], p[:, 1, 1]
        cx, cy = p[:, 2, 0], p[:, 2, 1]
        qx, qy = xx + 0.5, yy + 0.5
        area = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)
        w0 = ((bx - qx) * (cy - qy) - (by - qy) * (cx - qx)) / area
        w1 = ((cx - qx) * (ay - qy) - (cy - qy) * (ax - qx)) / area
        shade = w0 * brightness[ids, 0] + w1 * brightness[ids, 1] + (1 - w0 - w1) * brightness[ids, 2]
        return np.clip(cols[ids] * shade[:, None], 0, 1)

    img = np.tile(bg, (H, W, 1))
    dep_o = np.full((H, W), -np.inf)
    if opaque:
        dep_o, tid, cols, nv, p2, brightness = layer(opaque)
        hit = tid >= 0
        img[hit] = shaded_pixels(tid, cols, p2, brightness, hit)
        if edges:
            img = _edges(img, tid, nv, dep_o, s)
    if trans:
        for t, c, a in trans:
            dep_t, tid_t, cols_t, nv_t, p2_t, brightness_t = layer([(t, c)])
            front = (tid_t >= 0) & (dep_t > dep_o)
            img[front] = (1 - a) * img[front] + a * shaded_pixels(tid_t, cols_t, p2_t, brightness_t, front)
            if edges:
                e = _edge_mask(tid_t, nv_t, dep_t, s) & front
                img[e] = 0.75 * img[e]
    img = img.reshape(H // ss, ss, W // ss, ss, 3).mean(axis=(1, 3))
    return img, (bx0, bx1, by0, by1), bounds


def _edge_mask(tid, nv, dep, s):
    hit = tid >= 0
    n = np.zeros(tid.shape + (3,))
    n[hit] = nv[tid[hit]]
    m = np.zeros(tid.shape, bool)
    for dy, dx in ((0, 1), (1, 0)):
        a = (slice(0, tid.shape[0] - dy), slice(0, tid.shape[1] - dx))
        b = (slice(dy, None), slice(dx, None))
        diff_hit = hit[a] != hit[b]
        both = hit[a] & hit[b]
        crease = both & ((n[a] * n[b]).sum(-1) < math.cos(math.radians(28)))
        delta = np.zeros_like(dep[a])
        np.subtract(dep[a], dep[b], out=delta, where=both)
        step = both & (np.abs(delta) > 1.2 / s * 6)
        e = diff_hit | crease | step
        m[a] |= e
    return m


def _edges(img, tid, nv, dep, s):
    e = _edge_mask(tid, nv, dep, s)
    img = img.copy()
    img[e] = img[e] * 0.65
    return img


# --------------------------------------------------------------------------- figures
def _items(built, parts, names=None, alpha=None, skip=()):
    out = []
    for p in parts:
        if p.kind == "cal" or p.name in skip or (names is not None and p.name not in names):
            continue
        out.append((_tris(built[p.name]), p.colour, (alpha or {}).get(p.name, 1.0)))
    return out


def _show(ax, img, ext, title):
    ax.imshow(img, extent=ext, interpolation="lanczos")
    ax.set_title(title, fontsize=11, color="#213c50", pad=12)
    ax.set_axis_off()


def render_all(built, parts, out, keepouts=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from pip_robot import params
    from pip_robot import parts as pt

    ver = params.VERSION
    full = _items(built, parts)

    # --- assembly
    fig, axs = plt.subplots(2, 2, figsize=(14, 15), dpi=180)
    for ax, (el, az, t) in zip(axs.flat, [(0, 0, "front (orthographic)"), (14, 32, "front-left"),
                                     (14, 148, "rear-left (buttons, switch, bank hatch)"), (10, 90, "left side")]):
        img, ext, _ = render(full, el, az, px_per_mm=3.8)
        _show(ax, img, ext, t)
    fig.suptitle(f"Pip | assembled views\nCAD {ver} · purchased parts are placeholder envelopes · physical fit unverified", fontsize=16, color="#213c50")
    fig.tight_layout(rect=(.015, .035, .985, .94), h_pad=3, w_pad=3)
    fig.savefig(out / "preview_assembly.png")
    plt.close(fig)

    # --- x-ray
    shells = {"front_shell": 0.16, "rear_shell": 0.16, "head_cap": 0.16}
    xray = _items(built, parts, alpha=shells)
    fig, axs = plt.subplots(1, 3, figsize=(18, 8), dpi=180)
    for ax, (el, az, t) in zip(axs, [(15, 35, "x-ray front-left"), (15, 145, "x-ray rear-left"), (89.9, 180.0, "x-ray top (face toward top of page)")]):
        img, ext, _ = render(xray, el, az, px_per_mm=3.8)
        _show(ax, img, ext, t)
    fig.suptitle(f"Pip | inside the body and head\nCAD {ver} · translucent covers · coloured blocks are purchased-part envelopes", fontsize=16, color="#213c50")
    fig.text(.5, .015, "Green: boards   Red: PiicoDev modules   Orange: bank and speaker   Yellow: motors   Blue: servo", ha="center", fontsize=11, color="#52616b")
    fig.tight_layout(rect=(.015, .035, .985, .94), h_pad=3, w_pad=3)
    fig.savefig(out / "preview_xray.png")
    plt.close(fig)

    _front_reference(built, parts, out, plt, pt, params)
    _sections(built, parts, out, plt, pt, params)
    if keepouts:
        _bank_fit(built, parts, out, plt, pt, params, keepouts)

    _parts_sheet(built, parts, out, plt, params)


def _parts_sheet(built, parts, out, plt, params):
    ver = params.VERSION

    # --- printable parts
    printable = [p for p in parts if p.kind in ("print", "cal")]
    cols = 4
    rows = int(np.ceil(len(printable) / cols))
    fig = plt.figure(figsize=(15, 3.3 * rows), dpi=160)
    for i, p in enumerate(printable):
        ax = fig.add_subplot(rows, cols, i + 1)
        tris = _tris(built[p.name])
        right, up, _ = _basis(22, 35)
        span = max(np.ptp(tris @ right), np.ptp(tris @ up)) + 12
        resolution = min(24.0, 650.0 / span)
        img, ext, _ = render([(tris, p.colour, 1.0)], 22, 35, px_per_mm=resolution)
        _show(ax, img, ext, f"{p.name.replace('_', ' ')}  ×{p.qty}")
    fig.suptitle(f"Pip | printable parts\nCAD {ver} · individual views are not to scale · assembly orientation shown", fontsize=16, color="#213c50")
    fig.tight_layout(rect=(.015, .035, .985, .94), h_pad=3, w_pad=3)
    fig.savefig(out / "preview_parts.png")
    plt.close(fig)


def _label(ax, xy, text, xytext, color="#111"):
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=10, color=color,
                arrowprops=dict(arrowstyle="-", lw=0.7, color=color),
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.85))


def _front_reference(built, parts, out, plt, pt, params):
    """Orthographic elevations. In the 'shell alone' views the backdrop is dark, so every
    THROUGH opening shows dark and every blind pocket / thin skin shows as plastic."""
    P = params.P
    BD, F, H = P.boards, P.front, P.head
    dark = np.array([0.10, 0.14, 0.24])
    fig, axs = plt.subplots(2, 2, figsize=(15, 17), dpi=180)
    axs = axs.ravel()

    img, ext, _ = render(_items(built, parts), 0, 0, px_per_mm=3.0)
    _show(axs[0], img, ext, "A. Front elevation, assembled (viewer's right = robot's left, +Y)")

    img, ext, _ = render(_items(built, parts, names={"front_shell"}), 0, 0, px_per_mm=3.5, bg=dark)
    ax = axs[1]
    _show(ax, img, ext, "B. Front shell alone, front elevation\n(dark = through-opening; white = plastic incl. thin skins)")
    gx, gz = BD.oled_active
    _label(ax, (0, F.oled_z), f"OLED window {gx + 1.5:.1f} x {gz + 1.5:.1f} (through)\n+ glass/board pocket behind", (30, F.oled_z + 2))
    _label(ax, (0, F.touch_z), f"touch pads: {P.pr.touch_membrane:.1f} mm membrane\n(blind pocket, 3 target rings)", (30, F.touch_z - 22))
    _label(ax, (0, F.dist_z), "ToF window 12 x 7 (through)", (5, F.dist_z + 30))
    _label(ax, (F.rgb_y, F.rgb_z), f"RGB cheek: {P.pr.led_diffuser:.1f} mm diffuser\nskin (blind, not visible here)", (45, F.rgb_z + 8))
    _label(ax, (-F.rgb_y, F.rgb_z), "buzzer holes", (-90, F.rgb_z + 25))

    head_names = {"head_cap", "head_base", "eye_left_camera", "eye_right", "ref_cam_board", "ref_head_speaker", "clutch_disc"}
    img, ext, _ = render(_items(built, parts, names=head_names), 0, 0, px_per_mm=4.5)
    ax = axs[2]
    _show(ax, img, ext, f"C. Head, front elevation (camera board visible through\nthe {BD.cam_fov_design:.0f} deg aperture in the left eye)")
    ez = pt.EYE_Z
    _label(ax, (H.eye_y, ez), "camera aperture\n(design FOV cone, see sections)", (H.eye_y + 10, ez + 40))
    _label(ax, (-H.eye_y, pt.SPK_Z), "speaker grille", (-H.eye_y - 30, pt.SPK_Z - 22))
    _label(ax, (pt.MIC_HOLES[0][0], pt.MIC_HOLES[0][1]), "mic holes (placeholder)", (H.eye_y + 6, pt.MIC_HOLES[0][1] - 26))

    img, ext, _ = render(_items(built, parts), 0, 180, px_per_mm=3.0)
    ax = axs[3]
    _show(ax, img, ext, "D. Rear elevation (viewer's right = robot's right, -Y)")
    for (y, z), t in ((BD.btn_wake_yz, "A wake (white)"), (BD.btn_move_yz, "B move enable (dark)")):
        _label(ax, (-y, z), t, (-y + 25, z - 25 if "A" in t else z + 28))
    su, sv = BD.switch_uv
    _label(ax, (-su, BD.ctrl_bottom_z + sv), "power switch actuator", (-su + 20, BD.ctrl_bottom_z + sv + 30))
    hz = (P.hatch.z0 + P.hatch.z1) / 2
    _label(ax, (0, hz), "bank service hatch\n(adult, 1 x M3)", (-75, hz - 30))
    fig.suptitle(f"Pip | reference elevations\nCAD {params.VERSION} · orthographic views · dimensions and placements need physical verification", fontsize=16, color="#213c50")
    fig.tight_layout(rect=(.015, .035, .985, .94), h_pad=3, w_pad=3)
    fig.savefig(out / "preview_front_reference.png")
    plt.close(fig)


def _poly_fill(ax, cs, color, mapper=lambda p: p, alpha=1.0, z=1):
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path
    polys = cs.to_polygons()
    verts, codes = [], []
    for poly in polys:
        p = mapper(np.asarray(poly))
        if len(p) < 3:
            continue
        verts += list(p) + [p[0]]
        codes += [Path.MOVETO] + [Path.LINETO] * (len(p) - 1) + [Path.CLOSEPOLY]
    if verts:
        ax.add_patch(PathPatch(Path(np.array(verts), codes), fc=color, ec="#222", lw=0.4, alpha=alpha, zorder=z))


def _sections(built, parts, out, plt, pt, params):
    P = params.P
    BD = P.boards
    colours = {p.name: p.colour for p in parts}
    skip = {"fit_test_coupon", "fit_test_pegs"}
    fig, axs = plt.subplots(1, 3, figsize=(21, 9), dpi=180)

    # A. horizontal section through the camera axis (top view, +X up the page)
    ax = axs[0]
    zc = pt.CAM_Z
    for p in parts:
        if p.name in skip:
            continue
        cs = built[p.name].slice(zc)
        _poly_fill(ax, cs, colours[p.name], mapper=lambda q: np.stack([-q[:, 1], q[:, 0]], 1))
    lx, ly = pt.LENS_FRONT_X, pt.CAM_Y
    for half, ls, lab in ((BD.cam_fov_design / 2, "-", f"design FOV {BD.cam_fov_design:.0f} deg"),
                          (BD.cam_fov_lens / 2, ":", f"lens max {BD.cam_fov_lens:.0f} deg (vignetted)")):
        for sgn in (1, -1):
            a = math.radians(half)
            L = 30
            ax.plot([-ly, -(ly + sgn * L * math.sin(a))], [lx, lx + L * math.cos(a)], ls, color="#d02020", lw=1)
        ax.text(-ly + 2, lx + 22 if ls == "-" else lx + 5, lab, fontsize=7, color="#d02020")
    ax.set_aspect("equal")
    ax.set_xlim(-75, 75)
    ax.set_ylim(-60, 70)
    ax.set_title(f"A. Head section at camera height z={zc:.0f} (view from above, face up).\n"
                 "Eye flange is backed by the head_base frame; FOV lines from the lens front.", fontsize=9)
    ax.set_xlabel("-Y (mm)")
    ax.set_ylabel("X (mm)")

    # B. vertical section on the centre line (side view, face to the right)
    def xz_section(ax, y, xlim, ylim, title):
        for p in parts:
            if p.name in skip:
                continue
            m = built[p.name].translate((0, -y, 0)).rotate((90, 0, 0))
            cs = m.slice(0.0)
            _poly_fill(ax, cs, colours[p.name], mapper=lambda q: np.stack([q[:, 0], -q[:, 1]], 1))
        ax.set_aspect("equal")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("X (mm, face to the right)")
        ax.set_ylabel("Z (mm)")

    xz_section(axs[1], 0.0, (-110, 110), (0, 310),
               "B. Section on the centre line y=0: belly modules behind the shell,\n"
               "controller (rear), neck, servo, clutch, eye frame")
    xz_section(axs[2], pt.CAM_Y, (-10, 60), (205, 300),
               f"C. Section through the left eye / camera axis y={pt.CAM_Y:.0f}")
    lx, lz = pt.LENS_FRONT_X, pt.CAM_Z
    a = math.radians(BD.cam_fov_design / 2)
    for sgn in (1, -1):
        axs[2].plot([lx, lx + 15], [lz, lz + sgn * 15 * math.tan(a)], "-", color="#d02020", lw=1)
    axs[2].text(lx + 1, lz + 17, f"design FOV {BD.cam_fov_design:.0f} deg", fontsize=7, color="#d02020")
    fig.suptitle(f"Pip CAD v{params.VERSION} - true cross-sections (manifold slices; colours as in the assembly). "
                 "Placeholder positions for bought parts.", fontsize=11)
    fig.tight_layout(rect=(.015, .035, .985, .94), h_pad=3, w_pad=3)
    fig.savefig(out / "preview_sections.png")
    plt.close(fig)


def _poly_outline(ax, cs, color, mapper, ls="--", lw=1.2, label=None):
    first = True
    for poly in cs.to_polygons():
        p = mapper(np.asarray(poly))
        if len(p) < 2:
            continue
        p = np.vstack([p, p[:1]])
        ax.plot(p[:, 0], p[:, 1], ls, color=color, lw=lw, label=label if first else None, zorder=5)
        first = False


def _bank_fit(built, parts, out, plt, pt, params, keep):
    """QW01 cradle figure: true sections with the keep-out envelopes drawn as outlines, and
    the rear with the hatch removed (what an adult sees when charging)."""
    P = params.P
    BAT = P.bat
    colours = {p.name: p.colour for p in parts}
    skip = {"fit_test_coupon", "fit_test_pegs"}
    styles = {"K1": ("#1f5fbf", "--", f"K1 largest bank {pt.BANK_L_MAX:.0f}x{pt.BANK_W_MAX:.0f}x{pt.BANK_T_MAX:.0f}"),
              "K2": ("#d02020", "-", f"K2 plug sweep ({pt.PLUG_LEN:.0f} deep)"),
              "K4": ("#8a2be2", ":", "K4 access path (hatch off)"),
              "K5": ("#1a9a50", "-.", "K5 lead route"),
              "K6": ("#b07000", ":", "K6 strap path")}
    fig, axs = plt.subplots(1, 3, figsize=(21, 9), dpi=180)

    # A. plan section through the bank
    ax = axs[0]
    zc = pt.DV.tray_top + 4.0
    top = lambda q: np.stack([-q[:, 1], q[:, 0]], 1)
    for p in parts:
        if p.name in skip:
            continue
        _poly_fill(ax, built[p.name].slice(zc), colours[p.name], mapper=top, alpha=0.85)
    for k, (c, ls, lab) in styles.items():
        _poly_outline(ax, keep[k].slice(zc), c, top, ls, label=lab)
    ax.axhline(BAT.port_x, color="#444", lw=0.6)
    ax.text(-95, BAT.port_x + 2, f"port plane x={BAT.port_x:.1f}", fontsize=7)
    ax.set_aspect("equal")
    ax.set_xlim(-100, 100)
    ax.set_ylim(-108, 100)
    ax.legend(fontsize=7, loc="lower right")
    ax.set_title(f"A. Plan section z={zc:.0f} (face up). Orange = nominal {BAT.len_nom:.0f}x{BAT.w_nom:.0f}x{BAT.t_nom:.0f} "
                 "(user approx.)\nGrey strips = shims/spacer/keepers; jogged columns beside the bank", fontsize=9)
    ax.set_xlabel("-Y (mm)")
    ax.set_ylabel("X (mm)")

    # B. side sections
    def side(ax, y, title):
        mp = lambda q: np.stack([q[:, 0], -q[:, 1]], 1)
        for p in parts:
            if p.name in skip:
                continue
            m = built[p.name].translate((0, -y, 0)).rotate((90, 0, 0))
            _poly_fill(ax, m.slice(0.0), colours[p.name], mapper=mp, alpha=0.85)
        for k, (c, ls, lab) in styles.items():
            m = keep[k].translate((0, -y, 0)).rotate((90, 0, 0))
            _poly_outline(ax, m.slice(0.0), c, mp, ls, label=lab)
        ax.set_aspect("equal")
        ax.set_xlim(-112, 100)
        ax.set_ylim(0, 160)
        ax.set_title(title, fontsize=9)
        ax.set_xlabel("X (mm, face to the right)")
        ax.set_ylabel("Z (mm)")
        ax.legend(fontsize=7, loc="upper right")
    side(axs[1], 15.0, "B. Side section y=+15: bank on the cradle floor, plug sweep into the\nhatch pod, lead route up behind the upright")

    # C. rear elevation with the hatch removed
    ax = axs[2]
    img, ext, _ = render(_items(built, parts, skip={"rear_hatch"}), 0, 180, px_per_mm=3.0,
                         bounds=(-112, 112, 0, 175))
    _show(ax, img, ext, "C. Rear elevation, hatch removed: the whole port end of the bank is open\n"
                        "(viewer's right = robot's right, -Y)")
    hz = (P.hatch.z0 + P.hatch.z1) / 2
    _label(ax, (0, hz), "bank port end (positions unknown)", (-95, hz - 45))
    _label(ax, (0, P.hatch.z1 - 4), "hatch screw ledge (behind the opening top)", (30, P.hatch.z1 + 40))
    fig.suptitle(f"Pip CAD v{params.VERSION} - MINISO QW01 cradle and keep-outs (APPROXIMATE bank size; "
                 "not a physical fit check)", fontsize=11)
    fig.tight_layout(rect=(.015, .035, .985, .94), h_pad=3, w_pad=3)
    fig.savefig(out / "preview_bank_fit.png")
    plt.close(fig)
