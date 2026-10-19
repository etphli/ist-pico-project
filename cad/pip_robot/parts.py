"""Pip companion robot - CAD v0.1 part geometry.

Every function returns a manifold3d.Manifold positioned in ASSEMBLY coordinates
(see params.py). build.py re-orients printable parts for export.

This is a PROVISIONAL prototype model. Positions of buttons, switches, ports,
mounting holes etc. on bought modules are placeholders (`# MEASURE` in params).
"""

import math
from dataclasses import dataclass

from manifold3d import CrossSection, Manifold

from .params import P
from .prims import (box, cyl_x, cyl_y, cyl_z, interp_profile, polar, ring_sector,
                    rounded_box, solid_of_profile, tube_z, union)

pr, B, D, C, BAT, BD, N, H, F = P.pr, P.body, P.drive, P.caster, P.bat, P.boards, P.neck, P.head, P.front


# --------------------------------------------------------------------------- derived
@dataclass(frozen=True)
class Derived:
    plate_top: float = B.base_z + B.base_t
    plate_r: float = interp_profile(B.profile, B.base_z) - pr.shell - 0.4
    axle_z: float = D.wheel_d / 2
    wheel_yc: float = D.track / 2
    wheel_in: float = D.track / 2 - D.wheel_w / 2
    wheel_out: float = D.track / 2 + D.wheel_w / 2
    motor_out_y: float = D.track / 2 - D.wheel_w / 2 - D.hub_gap
    motor_in_y: float = D.track / 2 - D.wheel_w / 2 - D.hub_gap - D.tt_t
    motor_z0: float = D.wheel_d / 2 - D.tt_h / 2
    motor_z1: float = D.wheel_d / 2 + D.tt_h / 2
    motor_x1: float = D.tt_shaft_from_end
    motor_x0: float = D.tt_shaft_from_end - D.tt_len
    tray_top: float = B.tray_z + B.tray_t
    deck_top: float = B.top_deck_z + B.top_deck_t
    neck_top: float = B.top_deck_z + B.top_deck_t + N.h
    head_floor_z: float = B.top_deck_z + B.top_deck_t + N.h + H.gap_above_neck
    column_xy: tuple = ((24.0, 27.0), (24.0, -27.0))
    upright_x: tuple = (-34.0, -30.0)


DV = Derived()
WELL_IN_Y0 = DV.motor_out_y + 0.3              # guard wall between motor and wheel
WELL_IN_Y1 = WELL_IN_Y0 + D.wheel_well_wall
WELL_OUT_Y0 = DV.wheel_out + D.wheel_well_gap
WELL_X = D.wheel_d / 2 + D.wheel_well_gap
WELL_TOP = D.wheel_d + D.wheel_well_gap
CASTER_HOLE_R = C.trail + C.wheel_d / 2 + 2.0
CASTER_ROOF_Z = C.lift + C.wheel_d + 2.0 + C.fork_t + 0.5      # underside of tower roof
TRAY_LEGS = ((45.0, 28.0), (45.0, -28.0), (-80.0, 36.0), (-80.0, -36.0))
SHELL_RIB_ANGLES = (40.0, -40.0, 140.0, -140.0)
SHELL_SCREWS = ((40.0, 0.0), (-40.0, 0.0))     # roof screws into deck bosses (M3)
CABLE_SLOT_ANG = 90.0                          # neck/head USB-C cable pass angle
CABLE_SLOT_R = (19.0, 26.5)
SPLINE_TOP = DV.head_floor_z                   # servo spline top ~ head floor underside
CLUTCH_POCKET_R = 16.0
BOARD_COMP_X = BD.robo_back_x - BD.robo_comp_h
BTN_TOP_X = BD.robo_back_x - 4.0               # tactile button top (MEASURE)


def body_outer():
    return solid_of_profile(B.profile, segs=pr.segs)


def body_inner(extra=0.0, z_bottom=None):
    return solid_of_profile(B.profile, inset=pr.shell + extra,
                            z_bottom=(B.base_z - 1 if z_bottom is None else z_bottom), segs=pr.segs)


def r_out(z):
    return interp_profile(B.profile, z)


def shell_x(z, y, inner=False, sign=1):
    r = r_out(z) - (pr.shell if inner else 0.0)
    return sign * math.sqrt(max(r * r - y * y, 0.0))


# --------------------------------------------------------------------------- base
def base_plate():
    pt = DV.plate_top
    plate = cyl_z(DV.plate_r, B.base_z, pt, segs=pr.segs)
    adds, cuts = [], []
    for s in (1, -1):
        # wheel guard well (walls + roof) - keeps fingers out of the tyre/plate nip
        y_in0, y_in1 = sorted((s * WELL_IN_Y0, s * WELL_IN_Y1))
        y_o0, y_o1 = sorted((s * WELL_OUT_Y0, s * (WELL_OUT_Y0 + D.wheel_well_wall)))
        adds.append(box(-WELL_X - D.wheel_well_wall, WELL_X + D.wheel_well_wall, y_in0, y_in1, pt, WELL_TOP))
        adds.append(box(-WELL_X - D.wheel_well_wall, WELL_X + D.wheel_well_wall, y_o0, y_o1, pt, WELL_TOP))
        for sx in (1, -1):
            x0, x1 = sorted((sx * WELL_X, sx * (WELL_X + D.wheel_well_wall)))
            adds.append(box(x0, x1, min(y_in0, y_o0), max(y_in1, y_o1), pt, WELL_TOP))
        adds.append(box(-WELL_X - D.wheel_well_wall, WELL_X + D.wheel_well_wall,
                        min(y_in0, y_o0), max(y_in1, y_o1), WELL_TOP, WELL_TOP + D.wheel_well_wall))
        # shaft / hub-boss hole through guard wall
        cuts.append(cyl_y(8.0, y_in0 - 0.1, y_in1 + 0.1, 0.0, DV.axle_z))
        # wheel slot through plate
        ys = sorted((s * WELL_IN_Y1, s * WELL_OUT_Y0))
        cuts.append(box(-WELL_X, WELL_X, ys[0], ys[1], B.base_z - 1, pt + 0.1))
        # motor cradle: floor pad + inner wall
        my0, my1 = sorted((s * DV.motor_in_y, s * DV.motor_out_y))
        adds.append(box(DV.motor_x0 + 2, DV.motor_x1 - 2, my0, my1, pt, DV.motor_z0 - 0.2))
        wy0, wy1 = sorted((s * (DV.motor_in_y - 0.2), s * (DV.motor_in_y - 2.7)))
        adds.append(box(DV.motor_x0 + 2, DV.motor_x1 - 2, wy0, wy1, pt, DV.motor_z1 + 0.3))
        cuts.append(cyl_y(4.0, min(wy0, wy1) - 0.1, max(wy0, wy1) + 0.1, 0.0, DV.axle_z))  # inner shaft stub
        # strap peg holes in cradle wall top + strap tongue slots in guard wall
        for sx in (-10.0, -45.0):
            cuts.append(cyl_z(1.6, DV.motor_z1 - 6, DV.motor_z1 + 1, sx, s * (DV.motor_in_y - 1.45)))
            cuts.append(box(sx - 4.3, sx + 4.3, *sorted((s * (WELL_IN_Y0 - 0.1), s * (WELL_IN_Y0 + 1.6))),
                            DV.motor_z1 + 0.1, B.tray_z + 0.2))
    # caster towers (roof carries the swivel stem; print with support inside)
    for sx in (1, -1):
        cx = sx * C.x
        adds.append(tube_z(C.tower_r, CASTER_HOLE_R - 0.01, pt - 0.01, CASTER_ROOF_Z + 5, cx, 0))
        adds.append(cyl_z(C.tower_r, CASTER_ROOF_Z, CASTER_ROOF_Z + 5, cx, 0))
        cuts.append(cyl_z(CASTER_HOLE_R, B.base_z - 1, CASTER_ROOF_Z, cx, 0, segs=64))
        cuts.append(cyl_z(C.stem_d / 2 + pr.clearance, CASTER_ROOF_Z - 1, CASTER_ROOF_Z + 6, cx, 0))
    # columns, tray legs: peg sockets
    for (x, y) in DV.column_xy:
        cuts.append(cyl_z(3.0 + pr.clearance / 2, pt - 3, pt + 0.1, x, y))
    for (x, y) in TRAY_LEGS:
        cuts.append(cyl_z(2.5 + pr.clearance / 2, pt - 3, pt + 0.1, x, y))
    # colour sensor (downward) window + PiicoDev peg posts; accelerometer pegs
    cuts.append(box(22 - 7, 22 + 7, -7, 7, B.base_z - 1, pt + 1))
    for (cx, cy) in ((22.0, 0.0), (-20.0, 0.0)):
        h = BD.piico_hole_pitch / 2
        for dx in (-h, h):
            for dy in (-h, h):
                adds.append(cyl_z(1.15, pt, pt + 4.0, cx + dx, cy + dy, segs=16))
                adds.append(cyl_z(2.4, pt, pt + 1.5, cx + dx, cy + dy, segs=20))
    # cable pass holes (motor leads up to Robo Pico)
    for s in (1, -1):
        cuts.append(cyl_z(5.0, B.base_z - 1, pt + 1, -66.0, s * 30.0))
    # shell locating notches at the rim
    for a in SHELL_RIB_ANGLES:
        cx, cy = polar(DV.plate_r - 1.5, a)
        cuts.append(box(-1.8, 1.8, -7.3, 7.3, B.base_z - 1, pt + 1).rotate((0, 0, a)).translate((cx, cy, 0)))
    out = union([plate] + adds) - union(cuts)
    return out ^ cyl_z(DV.plate_r, B.base_z - 1, 400, segs=pr.segs)


def motor_strap():
    """One strap (print 4). Clamps a TT motor down; itself held down by the tray."""
    y0, y1 = DV.motor_in_y - 2.7, WELL_IN_Y0 + 1.5
    x = -10.0
    s = box(x - 4, x + 4, y0, y1, DV.motor_z1 + 0.3, B.tray_z - 0.1)
    s = s + cyl_z(1.4, DV.motor_z1 - 5, DV.motor_z1 + 0.4, x, DV.motor_in_y - 1.45, segs=20)
    return s


def tray():
    t0, t1 = B.tray_z, DV.tray_top
    shape = box(-87, 56, -47, 47, t0, t1) ^ body_inner(1.2)
    adds = []
    bx0, bx1 = BAT.rear_x - 0.6, BAT.rear_x + BAT.len + 0.6
    by = BAT.w / 2 + 0.6
    # low lip around the bank, open at the rear so the charge cable can reach
    lip = box(bx0 - 2.4, bx1 + 2.4, -by - 2.4, by + 2.4, t1, t1 + 4) - box(bx0, bx1 + 0.01, -by, by, t1 - 1, t1 + 5)
    lip = lip - box(bx0 - 3, bx0 + 1, -by + 4, by - 4, t1 - 1, t1 + 5)
    adds.append(lip)
    for (x, y) in TRAY_LEGS:
        adds.append(cyl_z(5.0, DV.plate_top + 0.2, t0 + 0.01, x, y))
        adds.append(cyl_z(2.5 - pr.clearance / 2, DV.plate_top - 2.8, DV.plate_top + 0.3, x, y))
    out = union([shape] + adds) ^ body_inner(1.0)
    cuts = []
    for (x, y) in DV.column_xy:
        cuts.append(cyl_z(6.0 + pr.clearance + 0.2, t0 - 1, t1 + 6, x, y))
    for s in (1, -1):
        # hook-and-loop strap slots
        for sx in (-55.0, -5.0):
            cuts.append(box(sx - 10, sx + 10, s * (by + 3.5) - 1.6, s * (by + 3.5) + 1.6, t0 - 1, t1 + 6))
        # upright leg sockets
        cuts.append(box(DV.upright_x[0] - 0.2, DV.upright_x[1] + 0.2, *sorted((s * 38.0, s * 46.0)), t1 - 2.0, t1 + 0.1))
        # motor/cable pass
        cuts.append(box(-70, -60, *sorted((s * 36.0, s * 46.0)), t0 - 1, t1 + 1))
    return out - union(cuts)


def column():
    """Front structural column (print 2, lying down). Pegs into base and deck."""
    x, y = DV.column_xy[0]
    c = cyl_z(6.0, DV.plate_top, B.top_deck_z, x, y, segs=40)
    c = c + cyl_z(3.0 - pr.clearance / 2, DV.plate_top - 2.8, DV.plate_top + 0.5, x, y)
    c = c + cyl_z(3.0 - pr.clearance / 2, B.top_deck_z - 0.5, B.top_deck_z + 3.0, x, y)
    return c


def rear_upright():
    x0, x1 = DV.upright_x
    plate = box(x0, x1, -48, 48, DV.tray_top, B.top_deck_z) ^ body_inner(1.5)
    plate = plate - box(x0 - 1, x1 + 1, -37, 37, DV.tray_top - 1, BD.robo_bottom_z - 1.0)
    adds = []
    # Robo Pico standoffs + location pegs (or M3 screws, see docs)
    for (u, v) in _robo_holes():
        adds.append(cyl_x(3.2, BD.robo_back_x + BD.robo_t, x0 + 0.01, u, BD.robo_bottom_z + v))
        adds.append(cyl_x(1.4, BD.robo_back_x - 2.0, BD.robo_back_x + BD.robo_t + 0.1, u, BD.robo_bottom_z + v, segs=20))
    # legs into tray, tabs into deck
    for s in (1, -1):
        adds.append(box(x0, x1, *sorted((s * 38.4, s * 45.6)), DV.tray_top - 1.8, DV.tray_top + 0.1))
        adds.append(box(x0, x1, *sorted((s * 10.0, s * 20.0)), B.top_deck_z - 0.1, B.top_deck_z + 3.0))
    out = union([plate] + adds)
    # cable windows (PiicoDev chain, motor leads, speaker lead)
    out = out - box(x0 - 1, x1 + 1, -14, 14, 158, 170)
    out = out - box(x0 - 1, x1 + 1, 30, 44, 120, 140) - box(x0 - 1, x1 + 1, -44, -30, 120, 140)
    return out


def _robo_holes():
    i = BD.robo_hole_inset
    u = BD.robo_w / 2 - i
    return [(-u, i), (u, i), (-u, BD.robo_h - i), (u, BD.robo_h - i)]


def top_deck():
    z0, z1 = B.top_deck_z, DV.deck_top
    deck = cyl_z(60, z0, z1, segs=pr.segs) ^ body_inner(0.6)
    adds = []
    # fixed neck sleeve with top flange
    adds.append(tube_z(N.od / 2, N.od / 2 - N.wall, z1 - 0.01, DV.neck_top - 3.0))
    adds.append(tube_z(N.od / 2 + 2.0, N.od / 2 - N.wall, DV.neck_top - 3.0, DV.neck_top))
    # servo ledges (servo hangs on its tabs)
    body_cx = -N.servo_shaft_off
    servo_bot = SPLINE_TOP - N.servo_spline_above - N.servo_h
    tab_z = servo_bot + N.servo_tab_z
    ri = N.od / 2 - N.wall
    half = N.servo_l / 2
    adds.append(box(-ri - 0.5, body_cx - half - 0.4, -6, 6, tab_z - 8, tab_z) ^ cyl_z(ri + 0.4, z1, DV.neck_top))
    adds.append(box(body_cx + half + 0.4, ri + 0.5, -6, 6, tab_z - 8, tab_z) ^ cyl_z(ri + 0.4, z1, DV.neck_top))
    # pan stop pin at the rear of the neck top
    sx, sy = polar(N.od / 2 - N.wall / 2 + 0.5, 180.0)
    adds.append(cyl_z(1.8, DV.neck_top - 0.5, DV.neck_top + 3.0, sx, sy, segs=20))
    # shell roof screw bosses
    for (x, y) in SHELL_SCREWS:
        adds.append(cyl_z(4.5, z0, z1, x, y))
    out = union([deck] + adds) ^ (body_inner(0.6) + cyl_z(N.od / 2 + 2.01, z1 - 1, DV.neck_top + 4))
    cuts = []
    for (x, y) in SHELL_SCREWS:
        cuts.append(cyl_z(1.25, z0 + 1.0, z1 + 0.1, x, y, segs=16))      # M3 self-tap pilot
    for (x, y) in DV.column_xy:
        cuts.append(cyl_z(3.0 + pr.clearance / 2, z0 - 0.1, z0 + 3.2, x, y))
    for s in (1, -1):
        cuts.append(box(DV.upright_x[0] - 0.2, DV.upright_x[1] + 0.2, *sorted((s * 9.8, s * 20.2)), z0 - 0.1, z0 + 3.2))
    # servo screw holes
    for xo in (-N.servo_tab_span / 2 + 2.3, N.servo_tab_span / 2 - 2.3):
        cuts.append(cyl_z(0.9, tab_z - 8, tab_z + 0.1, body_cx + xo, 0, segs=12))
    # servo lead + USB-C cable pass through the deck (inside the neck)
    cuts.append(_cable_slot(z0 - 1, z1 + 1))
    cuts.append(box(body_cx - 4, body_cx + 4, -3, 3, z0 - 1, z1 + 1))
    # PiicoDev cable pass to front
    cuts.append(box(5, 22, -6, 6, z0 - 1, z1 + 1))
    return out - union(cuts)


def _cable_slot(z0, z1):
    a = CABLE_SLOT_ANG
    ri, ro = CABLE_SLOT_R
    span = math.degrees(14.0 / ((ri + ro) / 2))
    return ring_sector(ri, ro, z0, z1, a - span / 2, a + span / 2)


# --------------------------------------------------------------------------- shells
def _shell_solid():
    outer = body_outer()
    inner = body_inner(0.0)
    s = outer - inner
    s = s - cyl_z(N.od / 2 + 1.5, 150, 260)
    return s


def _pad(z, y, w, h, depth, side=1):
    """Flat-backed mounting pad grown inwards from the shell at (z, y)."""
    xin = shell_x(z, y, inner=True, sign=side)
    if side > 0:
        blk = box(xin - depth, xin + 10, y - w / 2, y + w / 2, z - h / 2, z + h / 2)
    else:
        blk = box(xin - 10, xin + depth, y - w / 2, y + w / 2, z - h / 2, z + h / 2)
    return blk ^ body_outer()


def _flat_face_x(z, y, w, h, side=1):
    """Innermost X of the outer surface over a w x h patch: a pocket back-plane that
    leaves at least the requested skin everywhere over the patch."""
    xs = []
    for dy in (-w / 2, 0, w / 2):
        for dz in (-h / 2, 0, h / 2):
            xs.append(abs(shell_x(z + dz, y + dy, sign=1)))
    return side * min(xs)


def _module_pocket(z, y, size_y, size_z, skin, depth, side=1):
    xf = _flat_face_x(z, y, size_y, size_z, side)
    if side > 0:
        return box(xf - skin - depth, xf - skin, y - size_y / 2, y + size_y / 2, z - size_z / 2, z + size_z / 2)
    return box(xf + skin, xf + skin + depth, y - size_y / 2, y + size_y / 2, z - size_z / 2, z + size_z / 2)


def _through_window(z, y, wy, wz, side=1):
    x = abs(shell_x(z, y)) + 5
    if side > 0:
        return box(x - 25, x, y - wy / 2, y + wy / 2, z - wz / 2, z + wz / 2)
    return box(-x, -x + 25, y - wy / 2, y + wy / 2, z - wz / 2, z + wz / 2)


def _ribs(side):
    out = []
    for a in SHELL_RIB_ANGLES:
        if (side > 0) != (math.cos(math.radians(a)) > 0):
            continue
        r = DV.plate_r - 1.5
        cx, cy = polar(r + 1.5, a)
        rib = box(-1.5, 1.5, -7.0, 7.0, B.base_z, B.base_z + 18).rotate((0, 0, a)).translate((cx, cy, 0))
        out.append(rib ^ body_outer())
    return out


def front_shell():
    s = _shell_solid() ^ box(0.15, 200, -200, 200, 0, 400)
    pz = BD.piico + 2 * 3.0
    pads = [
        _pad(F.oled_z, 0, 36, 32, 7),
        _pad(F.touch_z, 0, 34, 34, 6),
        _pad(F.spk_z, 0, BD.spk + 8, BD.spk + 8, 8),
        _pad(F.dist_z, 0, pz, pz, 6),
        _pad(F.rgb_z, F.rgb_y, pz, pz, 6),
        _pad(F.rgb_z, -F.rgb_y, pz, pz, 6),
    ]
    s = union([s] + pads + _ribs(1))
    sx = SHELL_SCREWS[0][0]
    s = s + (cyl_z(4.5, B.top_deck_z + B.top_deck_t + 0.3, 195, sx, 0) ^ body_outer())
    cuts = []
    # OLED: viewing window + glass pocket + board pocket
    gx, gz = BD.oled_glass
    ax, az = BD.oled_active
    cuts.append(_through_window(F.oled_z, 0, ax + 1.5, az + 1.5))
    cuts.append(_module_pocket(F.oled_z, 0, gx + 0.6, gz + 0.6, 1.2, 1.8))
    cuts.append(_module_pocket(F.oled_z, 0, BD.piico + 0.6, BD.piico + 0.6, 3.0, 6.0))
    # capacitive touch: thin membrane over the three pads
    cuts.append(_module_pocket(F.touch_z, 0, BD.piico + 0.6, BD.piico + 0.6, pr.touch_membrane, 8.0))
    xf = _flat_face_x(F.touch_z, 0, BD.piico, BD.piico)
    for dy in (-8.0, 0.0, 8.0):   # shallow outer target rings (MEASURE pad pitch)
        ring = cyl_x(3.5, xf - 0.3, xf + 6, dy, F.touch_z - 4) - cyl_x(2.7, xf - 1, xf + 7, dy, F.touch_z - 4)
        cuts.append(ring)
    # speaker grille + module pocket
    cuts.append(_module_pocket(F.spk_z, 0, BD.spk + 0.8, BD.spk + 0.8, 1.6, 20.0))
    xs = abs(shell_x(F.spk_z, 0)) + 4
    for iy in range(-4, 5):
        for iz in range(-4, 5):
            if iy * iy + iz * iz <= 17:
                cuts.append(cyl_x(1.25, xs - 14, xs, iy * 3.6, F.spk_z + iz * 3.6, segs=12))
    # distance sensor: clear aperture (no cover - avoids ToF crosstalk)
    cuts.append(_through_window(F.dist_z, 0, 12, 7))
    cuts.append(_module_pocket(F.dist_z, 0, BD.piico + 0.6, BD.piico + 0.6, 2.0, 7.0))
    # RGB "cheek" diffuser (thin white skin) left; buzzer holes right
    cuts.append(_module_pocket(F.rgb_z, F.rgb_y, BD.piico + 0.6, BD.piico + 0.6, pr.led_diffuser, 7.0))
    cuts.append(_module_pocket(F.rgb_z, -F.rgb_y, BD.piico + 0.6, BD.piico + 0.6, 1.6, 7.0))
    xb = abs(shell_x(F.rgb_z, -F.rgb_y)) + 4
    for k in range(6):
        oy, oz = polar(5.0, k * 60)
        cuts.append(cyl_x(1.0, xb - 14, xb, -F.rgb_y + oy, F.rgb_z + oz, segs=12))
    cuts.append(cyl_x(1.0, xb - 14, xb, -F.rgb_y, F.rgb_z, segs=12))
    # roof screw (M3 clearance + head recess)
    cuts.append(cyl_z(1.7, 170, 200, sx, 0, segs=16))
    cuts.append(cyl_z(3.2, 188.6, 200, sx, 0, segs=24))
    return s - union(cuts)


def rear_shell():
    s = _shell_solid() ^ box(-200, -0.15, -200, 200, 0, 400)
    adds = _ribs(-1)
    sx = SHELL_SCREWS[1][0]
    adds.append(cyl_z(4.5, B.top_deck_z + B.top_deck_t + 0.3, 195, sx, 0) ^ body_outer())
    # charge-door rails (door slides vertically in a flat plane at DOOR_X)
    for s_ in (1, -1):
        rail = box(-110, DOOR_X1 + 0.6, *sorted((s_ * (DOOR_W / 2 + 0.4), s_ * (DOOR_W / 2 + 3.0))), DOOR_Z0 + 3.5, DOOR_Z0 + DOOR_H + DOOR_TRAVEL + 2)
        lip = box(DOOR_X1 + 0.3, DOOR_X1 + 1.8, *sorted((s_ * (DOOR_W / 2 - 1.5), s_ * (DOOR_W / 2 + 3.0))), DOOR_Z0 + 3.5, DOOR_Z0 + DOOR_H + DOOR_TRAVEL + 2)
        adds.append((rail + lip) ^ body_outer())
    # button bosses (guide the plungers)
    for (u, v) in (BD.btn_gp20_uv, BD.btn_gp21_uv):
        z = BD.robo_bottom_z + v
        xi = shell_x(z, u, inner=True, sign=-1)
        adds.append(cyl_x(8.0, xi - 1, xi + 6, u, z) ^ body_outer())
    s = union([s] + adds)
    cuts = []
    # charge port window (bank USB-C input)
    pz = B.tray_z + B.tray_t + BAT.port_z_off
    cuts.append(_through_window(pz, 0, BAT.port_w + 3, BAT.port_h + 3, side=-1))
    # bank LED window (light shows through a clear/white insert)
    cuts.append(_through_window(pz + 12, 0, *BAT.led_window, side=-1))
    # door grip slot
    cuts.append(_through_window(DOOR_Z0 + 4 + DOOR_TRAVEL / 2, 0, 5.0, DOOR_TRAVEL + 5, side=-1))
    # rear buttons
    for (u, v) in (BD.btn_gp20_uv, BD.btn_gp21_uv):
        cuts.append(cyl_x(PLUNGER_CAP_R + 0.35, -120, 0, u, BD.robo_bottom_z + v))
    # power switch actuator slot (actuator slides along Y by the switch travel)
    su, sv = BD.switch_uv
    cuts.append(box(-120, -60, su - SW_BAR / 2 - 0.4, su + SW_BAR / 2 + BD.switch_travel + 0.4,
                    BD.robo_bottom_z + sv - SW_BAR / 2 - 0.4, BD.robo_bottom_z + sv + SW_BAR / 2 + 0.4))
    # Robo Pico status LED light hole
    lu, lv = BD.led_strip_uv
    cuts.append(cyl_x(2.0, -120, 0, lu, BD.robo_bottom_z + lv))
    # vents near atmospheric sensor (rear-left) and Robo Pico
    for k in range(5):
        a = 150 + k * 4.0
        cx, cy = polar(r_out(125) - 1, a)
        cuts.append(box(-4, 4, -0.9, 0.9, 112, 138).rotate((0, 0, a + 90)).translate((cx, cy, 0)))
    cuts.append(cyl_z(1.7, 170, 200, sx, 0, segs=16))
    cuts.append(cyl_z(3.2, 188.6, 200, sx, 0, segs=24))
    return s - union(cuts)


# --------------------------------------------------------------------------- rear UI
DOOR_W = 22.0
DOOR_H = 22.0
DOOR_T = 2.5
DOOR_X1 = -88.0           # inner face of door plane
DOOR_X0 = DOOR_X1 - DOOR_T
DOOR_Z0 = B.tray_z + B.tray_t + BAT.port_z_off - DOOR_H / 2    # closed position bottom
DOOR_TRAVEL = 24.0
PLUNGER_CAP_R = 4.5


def charge_door(open_=False):
    """Sliding charge-port door (inside the rear shell, grip nub through a slot).
    v0.1 is a plain cover. The planned interlock (door can only open when the power
    switch actuator is OFF) is NOT modelled yet - it needs the measured Robo Pico
    switch position. See docs/05 and docs/11."""
    dz = DOOR_TRAVEL if open_ else 0.0
    z0 = DOOR_Z0 + dz
    door = box(DOOR_X0, DOOR_X1, -DOOR_W / 2, DOOR_W / 2, z0, z0 + DOOR_H)
    door = door + box(shell_x(DOOR_Z0 + 4, 0, sign=-1) - 1.5, DOOR_X0 + 0.01, -2.0, 2.0, z0 + 2, z0 + 7)
    return door


SW_BAR = 6.0


def switch_actuator(on=True):
    """Push-rod that lets a child-sized finger reach the Robo Pico slide switch, which
    sits ~45 mm inside the shell. Assumes the switch slides along Y (MEASURE)."""
    su, sv = BD.switch_uv
    z = BD.robo_bottom_z + sv
    y = su + (0.0 if on else BD.switch_travel)
    xo = shell_x(z, y, sign=-1)
    bar = box(xo - 2.0, BD.robo_back_x - 7.0, y - SW_BAR / 2, y + SW_BAR / 2, z - SW_BAR / 2, z + SW_BAR / 2)
    fork = box(BD.robo_back_x - 9.0, BD.robo_back_x - 3.5, y - SW_BAR / 2 - 2.0, y + SW_BAR / 2 + 2.0, z - SW_BAR / 2, z + SW_BAR / 2)
    fork = fork - box(BD.robo_back_x - 7.0, BD.robo_back_x, y - 1.6, y + 1.6, z - 10, z + 10)   # knob slot (MEASURE)
    grip = box(xo - 3.5, xo - 1.9, y - SW_BAR / 2 - 2.5, y + SW_BAR / 2 + 2.5, z - SW_BAR / 2 - 1.5, z + SW_BAR / 2 + 1.5)
    return union([bar, fork, grip])


def plunger(which=0):
    """Rear button plunger: cap through shell, retaining collar, rod to tactile button."""
    u, v = (BD.btn_gp20_uv, BD.btn_gp21_uv)[which]
    z = BD.robo_bottom_z + v
    xo = shell_x(z, u, sign=-1)
    xi = shell_x(z, u, inner=True, sign=-1)
    cap = cyl_x(PLUNGER_CAP_R, xo - 1.5, xi + 0.5, u, z)
    collar = cyl_x(6.5, xi + 0.5 + 6.2, xi + 0.5 + 8.2, u, z)
    rod = cyl_x(2.5, xi + 0.4, BTN_TOP_X - 0.3, u, z)
    return union([cap, collar, rod])


# --------------------------------------------------------------------------- drive & casters
def drive_wheel(side=1):
    yc = side * DV.wheel_yc
    w = D.wheel_w
    r = D.wheel_d / 2
    prof = [(0.0, -w / 2), (r - 1, -w / 2), (r, -w / 2 + 1), (r, -2.5),
            (r - D.tyre_groove_d, -1.5), (r - D.tyre_groove_d, 1.5), (r, 2.5),
            (r, w / 2 - 1), (r - 1, w / 2), (0.0, w / 2)]
    cs = CrossSection([[(a, b) for a, b in prof]])
    wheel = Manifold.revolve(cs, 96)                    # axis = Z, then rotate to Y
    # lightening/spoke holes
    for k in range(5):
        hx, hy = polar(19.0, k * 72)
        wheel = wheel - cyl_z(6.5, -w, w, hx, hy, segs=32)
    wheel = wheel - cyl_z(r - 6, -w / 2 + 3, w, segs=64) + cyl_z(9.0, -w / 2, w / 2, segs=48)
    for k in range(5):
        a = k * 72 + 36
        wheel = wheel + (box(0, r - 6.1, -2.0, 2.0, -w / 2 + 0.01, w / 2 - 3).rotate((0, 0, a)))
    # hub boss reaching through the guard wall towards the motor
    wheel = wheel + cyl_z(6.0, -w / 2 - 3.0, -w / 2 + 0.01, segs=40)
    # TT double-D bore
    rr = D.tt_shaft_d / 2 + 0.1
    bore = cyl_z(rr, -w, w, segs=32) ^ box(-(D.tt_shaft_flat / 2 + 0.1), D.tt_shaft_flat / 2 + 0.1, -rr, rr, -w, w)
    wheel = wheel - bore
    # orient: local +Z -> world outward (side*Y); boss faces motor
    if side > 0:
        wheel = wheel.rotate((-90, 0, 0))
    else:
        wheel = wheel.rotate((90, 0, 0))
    return wheel.translate((0, yc, DV.axle_z))


def caster_fork(sx=1):
    cx = sx * C.x
    wz = C.lift + C.wheel_d / 2
    yoke_z1 = CASTER_ROOF_Z - 0.5
    yoke_z0 = yoke_z1 - C.fork_t
    half = C.wheel_w / 2 + 0.8
    stem = cyl_z(C.stem_d / 2, yoke_z1 - 0.01, CASTER_ROOF_Z + 5 + 4.5, cx, 0)
    stem = stem - tube_z(C.stem_d / 2 + 1, C.stem_d / 2 - 1.0, CASTER_ROOF_Z + 5 + 0.8, CASTER_ROOF_Z + 5 + 2.4, cx, 0)
    yoke = box(cx - C.trail - 6, cx + 5, -half - C.fork_t, half + C.fork_t, yoke_z0, yoke_z1)
    arms = []
    for s in (1, -1):
        y0, y1 = sorted((s * half, s * (half + C.fork_t)))
        arm = box(cx - C.trail - 6, cx - C.trail + 6, y0, y1, wz - 6.0, yoke_z0 + 0.01)   # flat foot for printing
        arms.append(arm)
    f = union([stem, yoke] + arms)
    f = f - cyl_y(C.axle_d / 2 + 0.15, -20, 20, cx - C.trail, wz)
    return f


def caster_wheel(sx=1):
    cx = sx * C.x - C.trail
    wz = C.lift + C.wheel_d / 2
    w = cyl_y(C.wheel_d / 2, -C.wheel_w / 2, C.wheel_w / 2, cx, wz, segs=64)
    return w - cyl_y(C.axle_d / 2 + 0.25, -10, 10, cx, wz)


def caster_axle(sx=1):
    cx = sx * C.x - C.trail
    wz = C.lift + C.wheel_d / 2
    half = C.wheel_w / 2 + 0.8 + C.fork_t
    pin = cyl_y(C.axle_d / 2, -half - 0.5, half + 0.2, cx, wz, segs=24)
    head = cyl_y(C.axle_d / 2 + 1.5, -half - 2.0, -half - 0.5, cx, wz, segs=24)
    # split tip snaps through the far arm
    pin = pin - box(cx - 0.5, cx + 0.5, half - 4, half + 1, wz - 5, wz + 5)
    tip = cyl_y(C.axle_d / 2 + 0.5, half + 0.2, half + 1.4, cx, wz, segs=24) - box(cx - 0.5, cx + 0.5, half, half + 2, wz - 5, wz + 5)
    # D-flat underneath so the pin prints lying down with layers along its length
    return union([pin, head, tip]) - box(cx - 10, cx + 10, -20, 20, wz - 10, wz - C.axle_d / 2 + 0.5)


def caster_clip(sx=1):
    cx = sx * C.x
    z0 = CASTER_ROOF_Z + 5 + 0.9
    ring = tube_z(C.stem_d / 2 + 3.0, C.stem_d / 2 - 0.9, z0, z0 + 1.4, cx, 0)
    return ring - box(cx - 10, cx - C.stem_d / 2 + 1.0, -2.2, 2.2, z0 - 1, z0 + 3)


# --------------------------------------------------------------------------- head
def _head_hull(inset=0.0):
    z0 = DV.head_floor_z
    cx, cz = 0.0, z0 + H.h / 2
    rt, rb = H.r - inset, 8.0 - inset
    pts = []
    for dx in (-1, 1):
        for dy in (-1, 1):
            pts.append(Manifold.sphere(rt, 48).translate((cx + dx * (H.d / 2 - H.r), dy * (H.w / 2 - H.r), z0 + H.h - H.r)))
            # bottom spheres centred ON the floor plane -> vertical walls where the cap is cut
            pts.append(Manifold.sphere(rb, 24).translate((cx + dx * (H.d / 2 - 8.0), dy * (H.w / 2 - 8.0), z0)))
    return Manifold.batch_hull(pts)


EYE_Z = DV.head_floor_z + H.eye_z_off


def head_cap():
    z0 = DV.head_floor_z
    inner = _head_hull(pr.shell)
    inner = Manifold.batch_hull([inner, inner.translate((0, 0, -20))])   # open bottom
    cap = _head_hull() - inner
    cap = cap - box(-200, 200, -200, 200, z0 - 50, z0 + 0.0)
    # eye sockets
    for s in (1, -1):
        cap = cap - cyl_x(H.eye_ring_od / 2 - 2.0 + pr.clearance, 0, 80, s * H.eye_y, EYE_Z, segs=64)
    # mic port cluster under the left (camera) eye  (MEASURE mic position)
    for k in range(5):
        oy, oz = polar(2.6, k * 72)
        cap = cap - cyl_x(0.8, 20, 80, H.eye_y + oy, EYE_Z - 26 + oz, segs=12)
    # rear vents
    for k in range(4):
        cap = cap - box(-80, -30, -12 + k * 8, -9 + k * 8, z0 + 30, z0 + 50)
    # side screw bosses -> floor
    for s in (1, -1):
        y = s * (H.w / 2 - pr.shell - 4.0)
        boss = cyl_z(3.8, z0 + 6.2, z0 + 22, 0, y) - cyl_z(1.25, z0 + 6.0, z0 + 20, 0, y, segs=16)
        cap = cap + (boss ^ _head_hull(0.5))
    return cap


def head_base():
    z0 = DV.head_floor_z
    floor = (_head_hull(pr.shell + pr.clearance) ^ box(-200, 200, -200, 200, z0, z0 + 6.0))
    skirt = tube_z(N.od / 2 + 2.0 + 0.5 + 3.0, N.od / 2 + 2.0 + 0.5, DV.neck_top - 11.0, z0 + 0.01)
    # snap hooks under the neck flange (4 fingers)
    hooks = tube_z(N.od / 2 + 2.6, N.od / 2 + 0.4, DV.neck_top - 6.0, DV.neck_top - 3.5)
    hb = skirt + hooks
    for k in range(4):
        hb = hb - box(-1.2, 1.2, 0, 60, DV.neck_top - 12, DV.neck_top + 0.6).rotate((0, 0, 45 + k * 90))
    base = floor + hb
    # XIAO + camera cradle behind the left eye
    cam_y = H.eye_y
    xf = H.d / 2 - pr.shell - 0.3                 # inner face of head front
    cx1 = xf - 4.0                                # camera board face (MEASURE lens height)
    cradle = box(cx1 - BD.xiao_h - 3.0, cx1, cam_y - BD.xiao_w / 2 - 2.0, cam_y + BD.xiao_w / 2 + 2.0, z0 + 5.9, EYE_Z + BD.xiao_l / 2 - 2)
    cradle = cradle - box(cx1 - BD.xiao_h - 0.3, cx1 + 1, cam_y - BD.xiao_w / 2 - 0.3, cam_y + BD.xiao_w / 2 + 0.3, EYE_Z - BD.xiao_l / 2 - 3.0, EYE_Z + 40)
    cradle = cradle - box(cx1 - BD.xiao_h + 2, cx1 + 1, cam_y - 6, cam_y + 6, z0 + 3, EYE_Z)   # USB-C plug access
    base = base + cradle
    # floor screw holes, clutch pocket with detent notches, stop groove, cable slot
    cuts = []
    for s in (1, -1):
        y = s * (H.w / 2 - pr.shell - 4.0)
        cuts.append(cyl_z(1.7, z0 - 1, z0 + 7, 0, y, segs=16))
    cuts.append(cyl_z(CLUTCH_POCKET_R, z0 - 1, z0 + 4.0, segs=64))
    for k in range(N.clutch_teeth):
        nx, ny = polar(CLUTCH_POCKET_R, k * 360 / N.clutch_teeth + 22.5)
        cuts.append(cyl_z(1.6, z0 - 1, z0 + 4.0, nx, ny, segs=16))
    rs = N.od / 2 - N.wall / 2 + 0.5
    cuts.append(ring_sector(rs - 2.2, rs + 2.2, z0 - 1, z0 + 3.5, 180 - N.stop_deg - 3, 180 + N.stop_deg + 3))
    cuts.append(_cable_slot(z0 - 1, z0 + 7))
    return base - union(cuts)


def clutch_disc():
    """Servo horn carrier. Spring tongues click into the head pocket notches and slip
    if the head is forced (protects FS90 plastic gears). TUNE clutch_arm_t by test."""
    z0 = DV.head_floor_z + 0.1
    z1 = DV.head_floor_z + 3.9
    core = cyl_z(9.5, z0, z1, segs=48)
    core = core + box(-N.horn_len / 2 - 1.2, N.horn_len / 2 + 1.2, -N.horn_w / 2 - 1.2, N.horn_w / 2 + 1.2, z0, z1)
    beams = []
    rin = 12.6
    rout = rin + N.clutch_arm_t
    for a0 in (14.5, 104.5, 194.5, 284.5):   # bumps land on notches at 67.5 + k*90
        a1 = a0 + 55.0
        beams.append(ring_sector(rin, rout, z0, z1, a0, a1))
        beams.append(ring_sector(8.0, rout, z0, z1, a0, a0 + 6))      # root spoke
        bx, by = polar(rout + 0.6, a1 - 2)
        beams.append(cyl_z(1.5, z0, z1, bx, by, segs=16))
    disc = union([core] + beams)
    disc = disc ^ cyl_z(CLUTCH_POCKET_R + 1.2, z0 - 1, z1 + 1, segs=64)
    # horn pocket (underside) + spline screw access
    horn = box(-N.horn_len / 2 - 0.2, N.horn_len / 2 + 0.2, -N.horn_w / 2 - 0.2, N.horn_w / 2 + 0.2, z0 - 1, z0 + N.horn_t)
    horn = horn + cyl_z(3.6, z0 - 1, z0 + N.horn_t + 0.6, segs=32)
    disc = disc - horn - cyl_z(1.4, z0 - 1, z1 + 1, segs=16)
    return disc


def eye(which=1):
    """Dark eye insert (print in black). Left eye (+Y) carries the camera aperture."""
    y = which * H.eye_y
    xo = H.d / 2
    plug_r = H.eye_ring_od / 2 - 2.0
    flange = cyl_x(H.eye_ring_od / 2, xo - 0.6, xo + 1.6, y, EYE_Z, segs=64)
    plug = cyl_x(plug_r, xo - pr.shell - 1.0, xo - 0.5, y, EYE_Z, segs=64)
    e = flange + plug
    # glossy "pupil" ring detail
    e = e - (cyl_x(H.eye_ring_id / 2, xo + 1.2, xo + 3, y, EYE_Z, segs=48) - cyl_x(H.eye_ring_id / 2 - 1.2, xo, xo + 3, y, EYE_Z, segs=48))
    if which > 0:
        e = e - cyl_x(BD.cam_aperture_d / 2, xo - 10, xo + 5, y, EYE_Z, segs=32)
        e = e - cyl_x(BD.cam_board / 2 + 1.0, xo - 10, xo - 0.6, y, EYE_Z, segs=32)
    else:
        e = e - cyl_x(plug_r - 1.6, xo - 10, xo - 0.6, y, EYE_Z, segs=48)
    return e


# --------------------------------------------------------------------------- reference (bought) parts
def ref_power_bank():
    z0 = DV.tray_top
    return rounded_box(BAT.rear_x + BAT.len / 2, 0, z0 + BAT.t / 2, BAT.len, BAT.w, BAT.t, 5.0)


def ref_tt_motor(side=1):
    y0, y1 = sorted((side * DV.motor_in_y, side * DV.motor_out_y))
    m = box(DV.motor_x0, DV.motor_x1, y0, y1, DV.motor_z0, DV.motor_z1)
    shaft = cyl_y(D.tt_shaft_d / 2, min(y0, y1) - D.tt_shaft_len, max(y0, y1) + D.tt_shaft_len, 0, DV.axle_z, segs=16)
    return m + shaft


def ref_robo_pico():
    v0 = BD.robo_bottom_z
    board = box(BD.robo_back_x, BD.robo_back_x + BD.robo_t, -BD.robo_w / 2, BD.robo_w / 2, v0, v0 + BD.robo_h)
    comps = box(BOARD_COMP_X, BD.robo_back_x, -BD.robo_w / 2 + 6, BD.robo_w / 2 - 6, v0 + 6, v0 + BD.robo_h - 6)
    return board + comps


def ref_servo():
    body_cx = -N.servo_shaft_off
    bot = SPLINE_TOP - N.servo_spline_above - N.servo_h
    b = box(body_cx - N.servo_l / 2, body_cx + N.servo_l / 2, -N.servo_w / 2, N.servo_w / 2, bot, bot + N.servo_h)
    tabs = box(body_cx - N.servo_tab_span / 2, body_cx + N.servo_tab_span / 2, -N.servo_w / 2, N.servo_w / 2, bot + N.servo_tab_z, bot + N.servo_tab_z + N.servo_tab_t)
    spline = cyl_z(2.4, bot + N.servo_h, SPLINE_TOP - N.horn_t, segs=16)
    horn = box(-N.horn_len / 2, N.horn_len / 2, -N.horn_w / 2, N.horn_w / 2, SPLINE_TOP - N.horn_t + 0.05, SPLINE_TOP + 0.05)
    return union([b, tabs, spline, horn])


def ref_xiao():
    xf = H.d / 2 - pr.shell - 0.3 - 4.0
    stack = box(xf - BD.xiao_h, xf, H.eye_y - BD.xiao_w / 2, H.eye_y + BD.xiao_w / 2, EYE_Z - BD.xiao_l / 2 - 2.5, EYE_Z + BD.xiao_l / 2 - 2.5)
    cam = box(xf - 0.01, xf + 3.0, H.eye_y - BD.cam_board / 2, H.eye_y + BD.cam_board / 2, EYE_Z - BD.cam_board / 2, EYE_Z + BD.cam_board / 2)
    return stack + cam


def ref_front_modules():
    out = []
    specs = [(F.oled_z, 0, 3.0, 4.0), (F.touch_z, 0, pr.touch_membrane, 4.0), (F.dist_z, 0, 2.0, 5.0),
             (F.rgb_z, F.rgb_y, pr.led_diffuser, 4.0), (F.rgb_z, -F.rgb_y, 1.6, 6.0)]
    for z, y, skin, th in specs:
        xf = _flat_face_x(z, y, BD.piico + 0.6, BD.piico + 0.6)     # same patch as the pocket
        out.append(box(xf - skin - th, xf - skin - 0.1, y - BD.piico / 2, y + BD.piico / 2, z - BD.piico / 2, z + BD.piico / 2))
    xf = _flat_face_x(F.spk_z, 0, BD.spk + 0.8, BD.spk + 0.8)
    out.append(box(xf - 1.6 - BD.spk_depth, xf - 1.7, -BD.spk / 2, BD.spk / 2, F.spk_z - BD.spk / 2, F.spk_z + BD.spk / 2))
    return union(out)


def ref_base_modules():
    out = []
    for (cx, cy) in ((22.0, 0.0), (-20.0, 0.0)):
        out.append(box(cx - BD.piico / 2, cx + BD.piico / 2, cy - BD.piico / 2, cy + BD.piico / 2, DV.plate_top + 1.5, DV.plate_top + 4.5))
    return union(out)


# --------------------------------------------------------------------------- calibration
def fit_test_coupon():
    """Print FIRST (~20 min). Rows of clearance variants for the fits that matter:
    TT double-D shaft bore, column/tray peg sockets, PiicoDev peg posts, caster stem bore.
    Record which variant fits in docs/12 and update params.py."""
    plate = box(0, 70, 0, 46, 0, 4)
    adds, cuts = [], []
    for i, extra in enumerate((0.0, 0.1, 0.2, 0.3)):
        x = 9 + i * 17
        # TT shaft bore variants (bosses so the shaft can go fully in)
        adds.append(cyl_z(6.0, 4, 10, x, 10))
        rr = D.tt_shaft_d / 2 + extra
        fl = D.tt_shaft_flat / 2 + extra
        cuts.append(cyl_z(rr, -1, 11, x, 10, segs=32) ^ box(x - fl, x + fl, 10 - rr, 10 + rr, -1, 11))
        # peg sockets (column 6 mm / tray 5 mm pegs) with clearance variants
        cuts.append(cyl_z(3.0 + extra, 1.0, 5, x - 4, 24))
        cuts.append(cyl_z(2.5 + extra, 1.0, 5, x + 4, 24))
        # caster stem bore
        cuts.append(cyl_z(C.stem_d / 2 + extra, -1, 5, x, 37))
        # PiicoDev M2.5-hole peg posts: 2.0 / 2.2 / 2.4 / 2.6 mm
        adds.append(cyl_z(1.0 + i * 0.1, 4, 8, x + 6, 37, segs=16))
    # index notches 1..4 on the edge so variants can be identified
    for i in range(4):
        for k in range(i + 1):
            cuts.append(box(5 + i * 17 + k * 2.2, 6 + i * 17 + k * 2.2, -0.1, 1.2, 2.5, 4.1))
    return union([plate] + adds) - union(cuts)


def fit_test_pegs():
    """Matching pegs (6 mm column peg, 5 mm tray peg, 8 mm caster stem) to try in the coupon."""
    return union([cyl_z(3.0 - pr.clearance / 2, 0, 8, 0, 0), cyl_z(2.5 - pr.clearance / 2, 0, 8, 10, 0),
                  cyl_z(C.stem_d / 2, 0, 10, 22, 0)])
