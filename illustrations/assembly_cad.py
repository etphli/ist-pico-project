"""CAD-rendered assembly-detail images: 03-08, 11, 12.

Every shape is the real v0.3 mesh from cad/pip_robot (parts.py, assembly.py), drawn
with cad/render.py. Nothing here changes CAD geometry. "Exploded" views only move
whole parts for display (OFFSETS below); those offsets are not an insertion path.
Bought parts are placeholder envelopes. Fastener markers sit on CAD hole positions
and are labelled approximate.

Edit callout text and canvas positions in each function. Callout anchors are 3D
points in assembly millimetres (+X forward, +Y robot's left, +Z up).
"""

import math
import sys
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "cad"))

from pip_robot.assembly import PARTS                     # noqa: E402
from pip_robot import parts as pt, params                 # noqa: E402
from pip_robot.prims import box, polar                    # noqa: E402
from render import _basis, _tris, render                  # noqa: E402

from kit import Canvas, INK, INK2, MUTED, NETS, wrap      # noqa: E402

OUT = "docs/images/assembly-detail"
FOOT = ("Pip v0.3 · render of the CAD model, not a photo · bought parts are placeholder envelopes · "
        "no physical build verified   · illustrations/assembly_cad.py")
P = params.P
DV = pt.DV
_CACHE = {}
BYNAME = {p.name: p for p in PARTS}


def mesh(name):
    if name not in _CACHE:
        _CACHE[name] = BYNAME[name].make()
    return _CACHE[name]


def servo_split():
    """ref_servo is one envelope with the horn already on the spline. Split it so views
    can show the horn OFF the spline (display only)."""
    m = mesh("ref_servo")
    cut = box(-60, 60, -60, 60, pt.SPLINE_TOP - P.neck.horn_t, pt.SPLINE_TOP + 2)
    return m - cut, m ^ cut


class View:
    """Render selected meshes into a canvas box; map 3D points to canvas pixels."""

    def __init__(self, c, rect, items, elev, azim, bounds=None, max_ppm=26.0):
        self.c, self.elev, self.azim = c, elev, azim
        self.r, self.u, _ = _basis(elev, azim)
        tri_items = [(_tris(m), col, a) for m, col, a in items]
        allv = np.vstack([t.reshape(-1, 3) for t, _, _ in tri_items])
        su, sv = allv @ self.r, allv @ self.u
        if bounds is None:
            pad = 4.0
            bounds = (su.min() - pad, su.max() + pad, sv.min() - pad, sv.max() + pad)
        x, y, w, h = rect
        ppm = min(w / (bounds[1] - bounds[0]), h / (bounds[3] - bounds[2]))
        ppm = max(3.5, min(max_ppm, ppm))
        img, ext, _ = render(tri_items, elev, azim, px_per_mm=ppm, bounds=bounds, ss=2)
        self.to_canvas = c.image(img, ext, rect)
        self.ppm = ppm

    def __call__(self, p):
        p = np.asarray(p, float)
        return self.to_canvas(p @ self.r, p @ self.u)


def item(name, offset=(0, 0, 0), alpha=1.0, colour=None, m=None):
    m = m if m is not None else mesh(name)
    if any(offset):
        m = m.translate(offset)
    return (m, colour or BYNAME[name].colour, alpha)


def centre(m, offset=(0, 0, 0), where="c"):
    b = m.bounding_box()
    lo, hi = np.array(b[:3]), np.array(b[3:])
    c = (lo + hi) / 2
    if where == "top":
        c[2] = hi[2]
    elif where == "bottom":
        c[2] = lo[2]
    return c + np.asarray(offset)


# ============================================================================ 03
def coupon_and_print():
    c = Canvas(2400, 1520, "Print and test the fit coupon first",
               "The real coupon and pegs from the CAD. Four clearance variants of each fit; record the one that fits (docs/12 §C).",
               [("CAD", "CAD RENDER")], FOOT, number="Detail 3")
    pegs_off = (0, 60, 0)
    v = View(c, (80, 220, 1380, 1060), [item("fit_test_coupon"), item("fit_test_pegs", pegs_off)], elev=52, azim=-90)
    for i in range(4):
        x = 9 + i * 17
        px, py = v((x, -9, 0))
        c.marker(px, py + 30, str(i + 1), size=24, r=24)
    c.text(v((0, -9, 0))[0] - 40, v((0, -9, 0))[1] + 30, "variant", 21, bold=True, ha="right")
    c.callout("TT shaft bore (double-D)\nradius +0.0 / +0.1 / +0.2 / +0.3 mm", v((60, 10, 10)), (1500, 860), size=21)
    c.callout("Column peg socket 6 mm and tray peg socket 5 mm", v((56, 24, 4)), (1500, 640), size=21, width=420)
    c.callout("Caster stem bore 8 mm", v((60, 37, 4)), (1500, 470), size=21)
    c.callout("PiicoDev peg posts Ø 2.0 / 2.2 / 2.4 / 2.6 mm", v((66, 37, 8)), (1500, 300), size=21, width=420)
    c.callout("Test pegs: 6 mm column, 5 mm tray, 8 mm caster stem", v((10, 60, 8)), (110, 240), size=21, width=430)
    c.callout("Edge notches 1–4 name the variant", v((56.5, 0, 3)), (650, 1200), size=21)

    c.panel(1960, 190, 380, 1250, "Choose", gid="choose")
    c.notes(1980, 260, 340, [
        "Bore: tightest that goes fully on the motor shaft by hand, no crack (motor needed).",
        "Pegs: firm push fit.",
        "Stem: turns freely, no wobble.",
        "Posts: hold a module hole without force.",
        "Record in docs/12 §C (T-MECH-1).",
    ], size=20, gap=10)
    c.para(1980, 1020, "The coupon has no M3 screw-test feature. Stage 3 tests pilot sizes in a printed scrap instead.",
           340, 20, bold=True)
    c.para(1980, 1250, "Print flat: 0.2 mm, 3 walls, 20% infill.", 340, 20, color=INK2)
    return c.save(OUT, "03-coupon-and-print", svg=False)


# ============================================================================ 04
def caster_exploded():
    c = Canvas(2400, 1380, "Caster: fork, wheel, axle pin and clip",
               "Real caster parts, exploded for clarity (left) and in place under the base plate (right). Front and rear use the same parts.",
               [("CAD", "CAD RENDER"), ("UNVERIFIED", "ORDER NOT PROVEN")], FOOT, number="Detail 4")
    off = {"caster_wheel_F": (0, 0, -30), "caster_axle_F": (0, -42, 0), "caster_clip_F": (0, 0, 22)}
    names = ["caster_fork_F", "caster_wheel_F", "caster_axle_F", "caster_clip_F"]
    v = View(c, (70, 200, 1150, 1100), [item(n, off.get(n, (0, 0, 0))) for n in names], elev=22, azim=-58)
    for n, o in off.items():
        a = centre(mesh(n), o)
        b = centre(mesh(n))
        pa, pb = v(a), v(b)
        d = np.subtract(pb, pa)
        L = np.hypot(*d)
        c.arrow(tuple(np.add(pa, d * 0.25 / 1)), tuple(np.add(pa, d * 0.8)), color="#E0590B", lw=4, head=24)
    c.callout("Fork: stem goes up through the caster tower from below", v(centre(mesh("caster_fork_F"), where="top")),
              (90, 230), size=21, width=430)
    c.callout("Clip snaps into the stem groove above the tower roof", v(centre(mesh("caster_clip_F"), off["caster_clip_F"])),
              (760, 230), size=21, width=430)
    c.callout("Axle pin: through arm, wheel, far arm; split tip snaps through", v(centre(mesh("caster_axle_F"), off["caster_axle_F"])),
              (90, 1100), size=21, width=430)
    c.callout("Wheel Ø 22 × 9 mm between the fork arms", v(centre(mesh("caster_wheel_F"), off["caster_wheel_F"])),
              (760, 1130), size=21, width=430)

    # in place, cropped around the front caster
    cx = P.caster.x
    names2 = names + ["base_plate"]
    items2 = [item(n) for n in names] + [item("base_plate", alpha=0.18)]
    r, u, _ = _basis(14, -58)
    pts = np.array([[cx - 30, -30, 0], [cx + 30, 30, 0], [cx - 30, -30, 45], [cx + 30, 30, 45]])
    bnd = ((pts @ r).min(), (pts @ r).max(), (pts @ u).min(), (pts @ u).max())
    v2 = View(c, (1300, 300, 1040, 760), items2, elev=14, azim=-58, bounds=bnd)
    c.text(1820, 250, "In place (base plate transparent)", 23, bold=True, ha="center")
    c.callout("Tower roof", v2((cx + 0.65 * P.caster.tower_r, 0, pt.CASTER_ROOF_Z + 5)), (1330, 1110), size=21)
    c.callout("Wheel sits 1.5 mm above the drive-wheel plane by design", v2((cx - P.caster.trail, 0, P.caster.lift)),
              (1700, 1110), size=21, width=560)
    c.para(1300, 1230, "Check: the fork swivels a full turn and the wheel spins freely. Arrows show visual order only, not a proven assembly path.",
           1040, 20, color=INK2)
    return c.save(OUT, "04-caster-exploded", svg=False)


# ============================================================================ 05
def frame_fasteners():
    c = Canvas(2400, 1340, "Frame and fastener locations",
               "Where the 15 M3 screws go. Markers sit on CAD hole positions and are approximate.",
               [("CAD", "CAD RENDER")], FOOT, number="Detail 5")
    names = ["base_plate", "column_L", "column_R", "tray", "rear_upright", "top_deck", "ref_controller"]
    v = View(c, (60, 200, 1000, 1000), [item(n) for n in names], elev=24, azim=150)
    c.text(560, 172, "A · frame from rear-left", 23, bold=True, ha="center")
    for i, (x, y) in enumerate(DV.column_xy):
        px, py = v((x, y, DV.deck_top))
        c.marker(px, py, f"U{i + 1}", size=18, r=22)
    hy, hz = P.boards.ctrl_hole_dy / 2, P.boards.ctrl_hole_dz / 2
    vc = P.boards.ctrl_h / 2
    for i, (uu, vv) in enumerate([(-hy, vc - hz), (hy, vc - hz), (-hy, vc + hz), (hy, vc + hz)]):
        px, py = v((pt.CTRL_FRONT_X, uu, P.boards.ctrl_bottom_z + vv))
        c.marker(px, py, f"C{i + 1}", size=18, r=22, fc="#2F6B4F")

    # underside: base plate, columns and shells from below
    names2 = ["base_plate", "front_shell", "rear_shell", "column_L", "column_R"]
    v2 = View(c, (1100, 260, 820, 900), [item(n) for n in names2], elev=-89.9, azim=0)
    c.text(1510, 172, "B · base from below", 23, bold=True, ha="center")
    z = P.body.base_z
    for i, (x, y) in enumerate(pt.COLUMN_LOW):
        px, py = v2((x, y, z))
        c.marker(px, py, f"L{i + 1}", size=18, r=22)
    k = 1
    for a in pt.SHELL_SCREW_ANG_FRONT + pt.SHELL_SCREW_ANG_REAR:
        sx, sy = polar(pt.SHELL_SCREW_R, a)
        px, py = v2((sx, sy, z))
        c.marker(px, py, f"S{k}", size=18, r=22, fc="#7A4EB5")
        k += 1
    fx, fy = v2((P.body.base_r + 14, 0, z))
    c.text(fx, fy, "FRONT", 22, bold=True, ha="center", box=("white", "#9DA9B8"))

    c.panel(1960, 190, 380, 1060, "Count", gid="count")
    rows = [("L1, L2", "M3 × 12 up into the columns"), ("U1, U2", "M3 × 12 down through the deck"),
            ("C1–C4", "M3 × 8 controller to upright"), ("S1–S4", "M3 × 10 up into the shells"),
            ("head", "2 × M3 × 10 head cap (image 11)"), ("hatch", "1 × M3 × 8 (image 12)")]
    y = 270
    for tag, text in rows:
        c.text(1984, y, tag, 21, bold=True, va="top")
        body = wrap(text, 230, 20)
        c.text(2090, y, body, 20, va="top")
        y += (body.count("\n") + 1) * 26 + 26
    c.text(1984, y + 10, "= 15 × M3", 26, bold=True, va="top")
    c.para(1984, y + 70, "Servo tab and horn hardware (B18) is extra and not selected.", 330, 20, color=INK2)
    c.para(1984, y + 200, "Thread-forming screws into printed plastic: snug only.", 330, 20, color=INK2)
    c.para(80, 1230, "Lower column screws go in from below with the frame turned over; upper ones go down through the deck "
           "and end up hidden under the head.", 1840, 21)
    return c.save(OUT, "05-frame-fasteners", svg=False)


# ============================================================================ 06
def head_neck_detail():
    c = Canvas(2400, 1560, "Neck: servo, clutch and head floor",
               "Servo seated on the neck ledges. Horn, clutch disc and head base lifted for display only.",
               [("CAD", "CAD RENDER"), ("HOLD", "HORN FIT HOLD")], FOOT, number="Detail 6")
    body, horn = servo_split()
    lift_h, lift_b = (0, 0, 34), (0, 0, 70)
    items = [item("top_deck"), item("ref_servo", m=body), item("ref_servo", lift_h, m=horn),
             item("clutch_disc", lift_h), item("head_base", lift_b, alpha=0.55)]
    r, u, _ = _basis(22, 145)
    pts = np.array([[x, y, z] for x in (-62, 62) for y in (-62, 62) for z in (178, 300)])
    bnd = ((pts @ r).min(), (pts @ r).max(), (pts @ u).min(), (pts @ u).max())
    v = View(c, (60, 200, 1300, 1260), items, elev=22, azim=145, bounds=bnd)
    N = P.neck
    sx, sy = polar(N.od / 2 - N.wall / 2 + 0.5, 180.0)
    c.callout("Stop pin on the neck top runs in the head's arc groove: mechanical stops ±75°",
              v((sx, sy, DV.neck_top + 3)), (1420, 1120), size=21, width=420)
    c.callout("FS90 envelope on the two neck ledges. Tab screws not selected (B18).",
              v((-N.servo_shaft_off, 0, pt.SPLINE_TOP - N.servo_spline_above)), (1420, 900), size=21, width=420)
    c.callout("Horn stays OFF the spline until the servo is centred electrically. Do not turn the output shaft by hand.",
              v((N.horn_len / 2 - 2, 0, pt.SPLINE_TOP - 1 + 34)), (1420, 230), size=21, width=420)
    c.callout("Clutch disc: four spring tongues click into eight notches. Arm 1.2 / 1.6 / 2.0 mm variants.",
              v((0, 14, DV.head_floor_z + 36)), (1420, 470), size=21, width=420)
    sl = polar(22.0, pt.CABLE_SLOT_ANG)
    c.callout("Camera USB-C slot on the far side, robot's left (opening hidden here; see Detail 8)", v((sl[0], sl[1], DV.deck_top)), (80, 1300), size=21, width=760)
    c.callout("Head base (lifted)", v((0, -55, DV.head_floor_z + 70 + 5)), (80, 230), size=21)

    # dial inset: mechanical vs firmware limit
    cx, cy, R = 2130, 1250, 150
    c.rect(1900, 960, 440, 470, fc="white", ec="#C9C5BD", lw=1.5, r=14, z=1)
    c.text(2120, 995, "Pan limits", 22, bold=True, ha="center")

    def arc(deg0, deg1, rad, colour, lw, ls="-"):
        t = np.radians(np.linspace(deg0, deg1, 60))
        c.line(list(zip(cx + rad * np.sin(t), cy - rad * np.cos(t))), colour, lw=lw, ls=ls, z=5)
    arc(-75, 75, R, "#33475B", 9)
    arc(-70, 70, R - 34, "#3C6EA8", 7, ls=(0, (3, 2)))
    for a, colour in ((-75, "#33475B"), (75, "#33475B")):
        t = math.radians(a)
        c.line([(cx, cy), (cx + (R + 14) * math.sin(t), cy - (R + 14) * math.cos(t))], colour, lw=2.5, z=4)
    c.line([(cx, cy), (cx, cy - R - 20)], INK2, lw=2, ls=(0, (2, 2)))
    c.text(cx + 70, cy - R - 10, "forward", 18, color=INK2, ha="center")
    c.text(1925, 1310, "±75° mechanical stops (CAD)", 19, bold=True, color="#33475B")
    c.text(1925, 1355, "±70° firmware limit (FUTURE)", 19, bold=True, color="#3C6EA8")
    return c.save(OUT, "06-head-neck-detail", svg=False)


# ============================================================================ 07
def buttons_and_shells():
    c = Canvas(2400, 1360, "Rear buttons, plungers and addresses",
               "Plungers pulled out of the rear shell for display. The shell is transparent.",
               [("CAD", "CAD RENDER")], FOOT, number="Detail 7")
    off = (-34, 0, 0)
    names = ["rear_upright", "ref_controller", "ref_buttons", "tray", "base_plate"]
    items = [item(n) for n in names] + [item("rear_shell", alpha=0.2), item("plunger_wake", off), item("plunger_move", off)]
    r, u, _ = _basis(14, 210)
    pts = np.array([[x, y, z] for x in (-140, 0) for y in (-70, 30) for z in (55, 140)])
    bnd = ((pts @ r).min(), (pts @ r).max(), (pts @ u).min(), (pts @ u).max())
    v = View(c, (60, 200, 1300, 1080), items, elev=14, azim=210, bounds=bnd)
    (wy, wz), (my, mz) = P.boards.btn_wake_yz, P.boards.btn_move_yz
    c.callout("B · movement enable: dark plunger, nearer the centre", v(centre(mesh("plunger_move"), off)), (80, 230), size=21, width=560)
    c.callout("A · wake: white plunger, outer position", v(centre(mesh("plunger_wake"), off)), (760, 230), size=21)
    c.callout("Button modules on the upright: 2 × M2.5 × 6 each; hole positions assumed (E6)",
              v((pt.BTN_FRONT_X, my + 10, mz + 10)), (80, 1150), size=21, width=560)
    c.callout("Fitted plunger tip sits just above the Button cap, not pressing it", v((pt.BTN_TOP_X, wy, wz)),
              (760, 1150), size=21, width=560)

    c.panel(1420, 190, 920, 1100, "ID switches (power off)", gid="ids")

    def dip(x, y, states, label, addr):
        c.text(x, y, label, 23, bold=True)
        c.rect(x, y + 34, 340, 150, fc="#C03030", ec=INK, lw=2, r=10, z=3)
        for i, on in enumerate(states):
            sx = x + 30 + i * 78
            c.rect(sx, y + 64, 50, 90, fc="white", ec=INK, lw=1.5, r=4, z=4)
            c.rect(sx + 6, (y + 70) if on else (y + 112), 38, 36, fc="#30363D", ec=INK, lw=1, r=3, z=5)
            c.text(sx + 25, y + 210, f"ID {i + 1}", 18, bold=True, ha="center")
            c.text(sx + 25, y + 240, "ON" if on else "OFF", 18, bold=True, ha="center",
                   color="#2F6B4F" if on else INK2)
        c.text(x + 380, y + 110, addr, 34, bold=True)
    dip(1460, 270, (False, False, False, False), "Button A (wake)", "0x42")
    dip(1460, 620, (True, False, False, False), "Button B (move enable)", "0x09")
    c.notes(1450, 940, 860, [
        "Switch art shows state only. Read the ON direction printed on the module.",
        "Core's driver: address = 8 + ID1 + 2·ID2 + 4·ID3 + 8·ID4; all OFF uses the default 0x42. B is 0x09, not 0x43.",
        "Change switches only with power off; power-cycle after a change.",
    ], size=20, gap=10)
    return c.save(OUT, "07-buttons-and-shells", svg=False)


# ============================================================================ 08
def cable_route():
    c = Canvas(2400, 1560, "Proposed cable route (open frame)",
               "Shells and hatch removed. Orange lines are a PROPOSED route drawn over the render; cables are not modelled.",
               [("CAD", "CAD RENDER"), ("PROPOSED", "PROPOSED ROUTE")], FOOT, number="Detail 8")
    skip = {"front_shell", "rear_shell", "rear_hatch", "head_cap", "switch_actuator", "plunger_wake", "plunger_move",
            "ref_front_modules", "eye_left_camera", "eye_right", "ref_head_speaker"}
    names = [p.name for p in PARTS if p.kind != "cal" and p.name not in skip]
    items = [item(n) for n in names] + [(pt.bank_cable_route(), "#E0590B", 0.28)]
    v = View(c, (60, 190, 1500, 1300), items, elev=18, azim=148)
    route_body = [(-48, 8, 54), (-66, 14, 58), (-66, 36, 98), (-48, 40, 132), (-34, 40, 160)]
    route_cam = [(-34, 40, 160), (-20, 30, 176), (polar(22, 90)[0], 22, DV.deck_top), (0, 22, DV.head_floor_z),
                 (pt.CAM_BOARD_X[0] - 4, pt.CAM_Y, DV.head_floor_z + 8)]
    for route in (route_body, route_cam):
        c.line([v(p) for p in route], NETS["PROPOSED"][0], lw=7, ls=(0, (4, 2)), z=8, casing="#FFFFFF")
    # service-loop glyphs (illustrative)
    for (p, rad) in (((-52, 40, 120), 26), ((-6, 22, DV.head_floor_z + 18), 20)):
        cx_, cy_ = v(p)
        t = np.linspace(0, 2 * np.pi, 40)
        c.line(list(zip(cx_ + rad * np.cos(t), cy_ + rad * np.sin(t))), NETS["PROPOSED"][0], lw=4, z=8)
    c.callout("Leads leave the bank's port end (port positions unknown)", v(route_body[0]), (1620, 1240), size=21, width=640)
    c.callout("Up the robot's LEFT (+Y) behind the upright (Q16)", v(route_body[2]), (1620, 900), size=21, width=640)
    c.callout("Shaded block: the CAD lead-route keep-out (K5)", v((-62, 20, 90)), (1620, 1100), size=21, width=640)
    c.callout("Camera USB-C lead: deck slot, neck, head floor", v(route_cam[2]), (1620, 470), size=21, width=640)
    c.callout("≈80 mm body loop (provisional)", v((-52, 40, 120)), (1620, 700), size=21)
    c.callout("≈60 mm head loop (provisional)", v((-6, 22, DV.head_floor_z + 18)), (1620, 230), size=21)
    c.callout("Rear buttons on the RIGHT (−Y): keep leads away from the plungers", v(centre(mesh("ref_buttons"))),
              (80, 1290), size=21, width=700)
    c.panel(1620, 1340, 720, 120, None, gid="note")
    c.para(1640, 1356, "Camera in-line switch holder: NOT MODELLED. Its location is undecided.", 680, 21, bold=True)
    return c.save(OUT, "08-cable-route", svg=False)


# ============================================================================ 11
def clutch_and_eyes():
    c = Canvas(2400, 1420, "Head: eyes and clutch",
               "A: eyes go in from inside the cap. B: the clutch parts under the head floor, lowered for display.",
               [("CAD", "CAD RENDER")], FOOT, number="Detail 11")
    eoff = (-26, 0, 0)
    items = [item("head_cap", alpha=0.2), item("head_base"), item("ref_cam_board"), item("ref_head_speaker"),
             item("eye_left_camera", eoff), item("eye_right", eoff)]
    v = View(c, (60, 250, 1120, 1000), items, elev=16, azim=28)
    c.text(620, 172, "A · eyes (cap transparent)", 23, bold=True, ha="center")
    ez = pt.EYE_Z
    for y in (P.head.eye_y, -P.head.eye_y):
        a = v((pt.EYE_FLANGE_X[0] + eoff[0], y, ez))
        b = v((pt.EYE_FLANGE_X[0] - 4, y, ez))
        c.arrow(a, b, color="#E0590B", lw=4, head=22)
    c.callout("Camera eye: robot's LEFT (+Y), aperture for the lens", v((P.head.d / 2 + eoff[0], P.head.eye_y, ez + 16)),
              (640, 1100), size=21, width=520)
    c.callout("Push each eye OUT from inside until the flange stops it", v((pt.EYE_FLANGE_X[0] + eoff[0], -P.head.eye_y, ez - 18)),
              (80, 1100), size=21, width=520)
    c.callout("Eye frame on the head base backs the flanges", v((pt.FRAME_X[1], 0, ez + 16)), (80, 300), size=21, width=420)

    body, horn = servo_split()
    doff, hoff = (0, 0, -22), (0, 0, -44)
    items2 = [item("head_base"), item("clutch_disc", doff), item("ref_servo", hoff, m=horn)]
    r, u, _ = _basis(-38, 20)
    pts = np.array([[x, y, z] for x in (-62, 62) for y in (-62, 62) for z in (DV.head_floor_z - 50, DV.head_floor_z + 8)])
    bnd = ((pts @ r).min(), (pts @ r).max(), (pts @ u).min(), (pts @ u).max())
    v2 = View(c, (1240, 300, 1100, 860), items2, elev=-38, azim=20, bounds=bnd)
    c.text(1790, 172, "B · clutch from below", 23, bold=True, ha="center")
    z0 = DV.head_floor_z
    nx, ny = polar(pt.CLUTCH_POCKET_R, 22.5)
    c.callout("Pocket with 8 notches in the head floor", v2((nx, ny, z0)), (1260, 230), size=21)
    c.callout("Clutch disc: 4 spring tongues. Print 1.2 / 1.6 / 2.0 mm arm variants; choose in Stage 17",
              v2((12, -8, z0 - 22)), (1260, 1200), size=21, width=520)
    c.callout("Horn (servo envelope) fits the pocket under the disc. Horn screw and hardware not selected (B18)",
              v2((P.neck.horn_len / 2 - 3, 0, z0 - 46)), (1820, 1200), size=21, width=500)
    for s in (1, -1):
        px, py = v2((0, s * (P.head.w / 2 - P.pr.shell - 4.0), z0))
        c.marker(px, py, "M3", size=16, r=22)
    c.callout("2 × M3 × 10 up through the floor into the cap", v2((0, (P.head.w / 2 - P.pr.shell - 4.0), z0)),
              (1900, 230), size=21, width=420, dot=False)
    return c.save(OUT, "11-clutch-and-eyes", svg=False)


# ============================================================================ 12
def shell_closure():
    c = Canvas(2400, 1420, "Close the shells and fit the hatch",
               "Front and rear shells pulled apart and the hatch pulled back, for display only. Concept order, not a proven path.",
               [("CAD", "CAD RENDER"), ("UNVERIFIED", "PATH NOT PROVEN")], FOOT, number="Detail 12")
    off = {"front_shell": (70, 0, 0), "rear_shell": (-70, 0, 0), "rear_hatch": (-140, 0, 0),
           "plunger_wake": (-70, 0, 0), "plunger_move": (-70, 0, 0), "switch_actuator": (-70, 0, 0)}
    names = [p.name for p in PARTS if p.kind != "cal"]
    items = [item(n, off.get(n, (0, 0, 0))) for n in names]
    v = View(c, (60, 200, 2280, 1020), items, elev=10, azim=70)
    z = P.body.base_z
    for a in pt.SHELL_SCREW_ANG_FRONT + pt.SHELL_SCREW_ANG_REAR:
        sx, sy = polar(pt.SHELL_SCREW_R, a)
        if sy < 0:
            continue
        px, py = v((sx, sy, z))
        c.marker(px, py, "M3", size=15, r=20)
    hx = pt.HATCH_LEDGE_X[0] - 140
    px, py = v((hx, 0, P.hatch.screw_z))
    c.marker(px, py, "M3", size=15, r=20, fc="#7A4EB5")
    c.callout("Front shell: modules fitted first; 2 ribs into base notches; 2 × M3 × 10 up through the base",
              v(centre(mesh("front_shell"), off["front_shell"], "top")), (300, 230), size=21, width=600)
    c.callout("Rear shell: plungers fitted from inside; 2 × M3 × 10 up through the base",
              v(centre(mesh("rear_shell"), off["rear_shell"], "top")), (1600, 230), size=21, width=560)
    c.callout("Hatch: hook 2 bottom tongues, swing closed, 1 × M3 × 8 into the shell ledge. Snug only.",
              v(centre(mesh("rear_hatch"), off["rear_hatch"])), (1640, 1250), size=21, width=640)
    c.callout("Base plate stays on the frame; shell screws enter from underneath (markers)",
              v((0, P.body.base_r - 10, z)), (900, 1250), size=21, width=640)
    c.para(80, 1250, "Check: both shells flush at the seam, no cable pinched, hatch clears both output plugs (Q15).",
           700, 20, color=INK2)
    return c.save(OUT, "12-shell-closure", svg=False)


ALL = {
    "03-coupon-and-print": coupon_and_print,
    "04-caster-exploded": caster_exploded,
    "05-frame-fasteners": frame_fasteners,
    "06-head-neck-detail": head_neck_detail,
    "07-buttons-and-shells": buttons_and_shells,
    "08-cable-route": cable_route,
    "11-clutch-and-eyes": clutch_and_eyes,
    "12-shell-closure": shell_closure,
}
