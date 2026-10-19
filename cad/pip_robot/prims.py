"""Small geometry helpers on top of manifold3d."""

import math

from manifold3d import CrossSection, Manifold

SEGS = 96
SMALL = 40


def box(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from min/max extents."""
    return Manifold.cube((x1 - x0, y1 - y0, z1 - z0)).translate((x0, y0, z0))


def cyl_z(r, z0, z1, x=0.0, y=0.0, segs=SMALL, r_top=None):
    m = Manifold.cylinder(z1 - z0, r, r if r_top is None else r_top, segs)
    return m.translate((x, y, z0))


def cyl_y(r, y0, y1, x=0.0, z=0.0, segs=SMALL):
    """Cylinder along +Y from y0 to y1."""
    m = Manifold.cylinder(y1 - y0, r, r, segs).rotate((-90, 0, 0))
    return m.translate((x, y0, z))


def cyl_x(r, x0, x1, y=0.0, z=0.0, segs=SMALL):
    """Cylinder along +X from x0 to x1."""
    m = Manifold.cylinder(x1 - x0, r, r, segs).rotate((0, 90, 0))
    return m.translate((x0, y, z))


def tube_z(r_out, r_in, z0, z1, x=0.0, y=0.0, segs=SEGS):
    return cyl_z(r_out, z0, z1, x, y, segs) - cyl_z(r_in, z0 - 0.01, z1 + 0.01, x, y, segs)


def rounded_box(cx, cy, cz, sx, sy, sz, r, segs=SMALL):
    """Box centred on (cx,cy,cz) with all edges rounded by r (hull of 8 spheres)."""
    r = min(r, sx / 2 - 0.01, sy / 2 - 0.01, sz / 2 - 0.01)
    pts = []
    for dx in (-1, 1):
        for dy in (-1, 1):
            for dz in (-1, 1):
                pts.append(Manifold.sphere(r, segs).translate(
                    (cx + dx * (sx / 2 - r), cy + dy * (sy / 2 - r), cz + dz * (sz / 2 - r))))
    return Manifold.batch_hull(pts)


def union(parts):
    parts = [p for p in parts if p is not None]
    if not parts:
        return Manifold()
    return Manifold.batch_boolean(parts, _op_add())


def _op_add():
    from manifold3d import OpType
    return OpType.Add


def interp_profile(profile, z):
    """Outer radius of a (z, r) polyline profile at height z (clamped)."""
    if z <= profile[0][0]:
        return profile[0][1]
    for (z0, r0), (z1, r1) in zip(profile, profile[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            return r0 + t * (r1 - r0)
    return profile[-1][1]


def offset_polyline(pts, d):
    """Offset an open (r,z) polyline by d along its left-hand normal (towards the axis
    for a bottom->top profile). Simple miter offset; fine for gentle curves."""
    out = []
    n = len(pts)
    for i in range(n):
        if i == 0:
            tx, tz = pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]
        elif i == n - 1:
            tx, tz = pts[-1][0] - pts[-2][0], pts[-1][1] - pts[-2][1]
        else:
            ax, az = pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]
            bx, bz = pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]
            la, lb = math.hypot(ax, az), math.hypot(bx, bz)
            tx, tz = ax / la + bx / lb, az / la + bz / lb
        l = math.hypot(tx, tz)
        tx, tz = tx / l, tz / l
        # left normal of direction (tx,tz) in (r,z) plane = (-tz, tx); profile runs
        # upward with material on +r side, so inward = (-tz*?..). Use (-tz, tx) rotated:
        nx, nz = -tz, tx
        # ensure normal points to smaller r (inside) for upward-running profile
        if nx > 0:
            nx, nz = -nx, -nz
        out.append((pts[i][0] + nx * d, pts[i][1] + nz * d))
    return out


def revolve_rz(pts, segs=SEGS):
    """Revolve a closed (r,z) polygon around Z."""
    cs = CrossSection([[(max(0.0, r), z) for r, z in pts]])
    return Manifold.revolve(cs, segs)


def solid_of_profile(profile, inset=0.0, z_bottom=None, z_top=None, segs=SEGS):
    """Solid of revolution bounded by the (z,r) profile, optionally shrunk by `inset`."""
    pts = [(r, z) for z, r in profile]
    if inset:
        pts = offset_polyline(pts, inset)
    zb = pts[0][1] if z_bottom is None else z_bottom
    zt = pts[-1][1] if z_top is None else z_top
    poly = [(0.0, zb), (pts[0][0], zb)] + pts + [(pts[-1][0], zt), (0.0, zt)]
    return revolve_rz(poly, segs)


def ring_sector(r_in, r_out, z0, z1, a0_deg, a1_deg, segs=SMALL):
    """Annular sector between angles a0..a1 (deg, CCW from +X)."""
    pts = []
    steps = max(4, int(abs(a1_deg - a0_deg) / 4))
    for i in range(steps + 1):
        a = math.radians(a0_deg + (a1_deg - a0_deg) * i / steps)
        pts.append((r_out * math.cos(a), r_out * math.sin(a)))
    for i in range(steps, -1, -1):
        a = math.radians(a0_deg + (a1_deg - a0_deg) * i / steps)
        pts.append((r_in * math.cos(a), r_in * math.sin(a)))
    cs = CrossSection([pts])
    return Manifold.extrude(cs, z1 - z0).translate((0, 0, z0))


def polar(r, deg):
    a = math.radians(deg)
    return r * math.cos(a), r * math.sin(a)
