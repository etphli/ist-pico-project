"""Bank-fit regression for the owned MINISO QW01 (approximate size).

Checks the PHYSICAL ACCOMMODATION envelopes (largest bank in the tolerance band, plug and
cable-bend sweep over every assumed port position, open end face, hand/plug access path,
lead route and strap path) against the modelled structure. Run alone with
`scripts/cad.sh --bank-fit-only` (about 20 s) or as part of the full build.

Passing means the MODEL leaves room for any bank inside the band. It does not mean the real
bank fits: the size is a user estimate and the port positions and plugs are placeholders.
"""

from . import parts as pt
from .params import P

BAT = P.bat
STRICT = 0.1          # mm3: keep-outs are envelopes, so any real overlap counts

# Removable fillers sized for the bank actually measured; at the largest bank they are absent.
FILLERS = {"bank_shim_L", "bank_shim_R", "bank_front_spacer"}


def _vol(a, b):
    return (a ^ b).volume()


def _grow_box(lo, hi):
    return pt.box(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])


def run(built, parts):
    lines, problems, data = [], [], {}
    names = [p.name for p in parts if p.kind != "cal"]
    t1 = pt.DV.tray_top
    for label, value, limits in (("length", BAT.len_nom, BAT.len_range),
                                 ("width", BAT.w_nom, BAT.w_range),
                                 ("thickness", BAT.t_nom, BAT.t_range)):
        if not limits[0] <= value <= limits[1]:
            problems.append(f"bank fit: nominal {label} {value} mm outside fixed cavity range {limits}")

    def check(tag, keep, exclude, why):
        hits = []
        for n in names:
            if n in exclude:
                continue
            v = _vol(keep, built[n])
            if v > STRICT:
                hits.append((n, v))
        ok = not hits
        lines.append(f"| {tag} | {why} | {'clear' if ok else ', '.join(f'`{n}` {v:.1f} mm3' for n, v in hits)} |")
        if not ok:
            problems.extend([f"bank fit: {tag} entered by {n} ({v:.1f} mm3)" for n, v in hits])
        data[tag] = {"clear": ok, "hits": {n: round(v, 2) for n, v in hits}}
        return ok

    lines.append("## 3d. Bank-fit regression (MINISO QW01, approximate size)\n")
    lmax, wmax, tmax = pt.BANK_L_MAX, pt.BANK_W_MAX, pt.BANK_T_MAX
    lines.append(f"Nominal **{BAT.len_nom:.0f} x {BAT.w_nom:.0f} x {BAT.t_nom:.0f} mm is the user's approximate size, "
                 "not a measurement.** The cradle is built for any bank in "
                 f"L {pt.BANK_L_MIN:.0f}-{lmax:.0f}, W {pt.BANK_W_MIN:.0f}-{wmax:.0f}, T {pt.BANK_T_MIN:.0f}-{tmax:.0f} mm "
                 f"(fixed cavity ranges; nominal size changes only the fillers). Port end on the plane x = {BAT.port_x:.1f}. "
                 f"Port centres assumed within |y| <= {BAT.port_y_max:.0f} and >= {BAT.port_edge_z:.0f} mm inside the "
                 f"top/bottom faces, all on the rear end (NOT confirmed). Plug sweep depth {pt.PLUG_LEN:.0f} mm "
                 "(largest of: ADA3628 protrusion + wire bend, USB-A->C overmould + bend, micro-USB + bend; all MEASURE).\n")
    lines.append("| keep-out | meaning | result |\n|---|---|---|")
    k1 = pt.bank_envelope_max()
    k2 = pt.bank_plug_keepout()
    k3 = pt.bank_end_face_keepout()
    k4 = pt.bank_access_path()
    k5 = pt.bank_cable_route()
    k6 = pt.bank_strap_band()
    check("K1 largest bank", k1, FILLERS | {"ref_power_bank"},
          f"{lmax:.0f} x {wmax:.0f} x {tmax:.0f} sharp-cornered box vs every part and envelope")
    check("K2 plug sweep", k2, {"ref_power_bank"},
          f"{2 * pt.SWEEP_Y:.0f} W x {pt.SWEEP_Z[1] - pt.SWEEP_Z[0]:.1f} H x {pt.PLUG_LEN:.0f} deep behind the port plane, incl. hatch and shims")
    check("K3 open end face", k3, FILLERS | {"ref_power_bank"},
          f"whole end face of the largest bank, {BAT.end_open_depth:.0f} mm deep (only the removable keepers may enter)")
    check("K4 access path", k4, {"ref_power_bank", "rear_hatch"},
          "straight reach from outside to the port sweep, hatch removed")
    check("K5 lead route", k5, {"ref_power_bank"}, "output leads up the +Y side behind the upright to controller height")
    check("K6 strap path", k6, {"ref_power_bank"}, "2 hook-and-loop straps: slots and under-tray band")
    lines.append("")

    # Keeper intrusion into the end face (designed, removable)
    kv = sum(_vol(k3, built[n]) for n in ("bank_shim_L", "bank_shim_R"))
    lines.append(f"- Removable rear corner keepers inside the end face: {kv:.1f} mm3 total "
                 f"(each {BAT.keeper_overlap:.0f} mm in from the side, {BAT.keeper_h:.0f} mm high; outside the port sweep: "
                 f"{'yes' if _vol(k2, built['bank_shim_L'] + built['bank_shim_R']) <= STRICT else 'NO'}). "
                 "Trim them if a port is nearer the edge than assumed.")
    data["keeper_end_face_mm3"] = round(kv, 2)

    # Cavity margins, proven by growing K1 up to just short of the rails / front wall
    side = pt.CAV_HW - wmax / 2
    front = pt.CAV_X1 - (BAT.port_x + lmax)
    g = _grow_box((BAT.port_x, -wmax / 2 - side + 0.05, t1 + 0.01), (BAT.port_x + lmax + front - 0.05, wmax / 2 + side - 0.05, t1 + tmax))
    gv = _vol(g, built["tray"])
    ok = gv <= STRICT
    lines.append(f"- Largest bank to rails {side:.2f} mm per side, to the front wall {front:.2f} mm "
                 f"(grown envelope vs tray: {gv:.2f} mm3 -> {'OK' if ok else 'FAIL'}). Rails {BAT.rail_h:.0f} mm high, "
                 f"below the thinnest bank ({pt.BANK_T_MIN:.0f} mm), so the straps bear on the bank, not the rails.")
    if not ok or BAT.rail_h >= pt.BANK_T_MIN:
        problems.append("bank fit: cradle margin or rail height check failed")

    # Floor support under the bank (continuous floor, no holes)
    for tag, L, W in (("nominal", BAT.len_nom, BAT.w_nom), ("largest", lmax, wmax), ("smallest", pt.BANK_L_MIN, pt.BANK_W_MIN)):
        foot = pt.box(BAT.port_x, BAT.port_x + L, -W / 2, W / 2, t1 - 0.5, t1)
        frac = _vol(foot, built["tray"]) / foot.volume()
        lines.append(f"- Floor under the {tag} bank footprint ({L:.0f} x {W:.0f}): {frac:.1%} solid")
        data[f"floor_{tag}"] = round(frac, 4)
        if frac < 0.95:
            problems.append(f"bank fit: floor support under the {tag} bank only {frac:.1%}")

    # Nominal configuration: bank captured by shims, spacer and keepers with small gaps
    bank = built["ref_power_bank"]
    gaps = {n: bank.min_gap(built[n], 5.0) for n in ("bank_shim_L", "bank_shim_R", "bank_front_spacer", "tray")}
    ov = {n: _vol(bank, built[n]) for n in gaps}
    shim_t = pt.SHIM_Y[1] - pt.SHIM_Y[0]
    spacer_t = pt.SPACER_X[1] - pt.SPACER_X[0]
    lines.append(f"- Nominal bank with the default fillers: shim {shim_t:.1f} mm, front spacer {spacer_t:.1f} mm; "
                 + ", ".join(f"gap to {n} {g:.2f} mm (overlap {ov[n]:.1f} mm3)" for n, g in gaps.items()))
    if any(v > STRICT for v in ov.values()) or shim_t < 1.0 or spacer_t < 1.5:
        problems.append("bank fit: nominal bank collides with its fillers, or a filler is too thin to print")
    lines.append(f"- After measuring: shim = {pt.CAV_HW - 0.2 - BAT.fit_gap:.1f} - W/2 mm, spacer = "
                 f"{pt.CAV_X1 - 0.2 - BAT.port_x - BAT.fit_gap:.1f} - L mm. A bank outside the band needs new rails, not thinner fillers.")

    # Hatch clearances
    hg = built["rear_hatch"].min_gap(built["rear_shell"], 5.0)
    pg = built["rear_hatch"].min_gap(k2, 10.0)
    lines.append(f"- Rear hatch to rear shell: {hg:.2f} mm min gap; hatch pod to the plug sweep: {pg:.2f} mm")
    if hg < 0.2 or pg < 0.5:
        problems.append(f"bank fit: hatch gap {hg:.2f} / pod clearance {pg:.2f} too small")
    data.update({"hatch_gap": round(hg, 2), "pod_to_plug_sweep": round(pg, 2)})

    # Regression: the v0.2 placement collision must still be detected
    old = pt.legacy_qw01_at_v02_position()
    oc = _vol(old, pt.legacy_v02_column()) + _vol(old, pt.legacy_v02_column().mirror((0, 1, 0)))
    nc = _vol(k1, built["column_L"]) + _vol(k1, built["column_R"])
    det = oc > 1.0
    lines.append(f"- Regression: QW01 at the v0.2 position vs the v0.2 straight columns: {oc:.1f} mm3 "
                 f"({'detected, as it should be' if det else 'NOT DETECTED - the check is broken'}); "
                 f"largest bank vs the v0.3 columns: {nc:.1f} mm3.")
    if not det:
        problems.append("bank fit: regression check failed to detect the known v0.2 collision")
    data.update({"legacy_collision_mm3": round(oc, 1), "v03_column_overlap_mm3": round(nc, 2)})

    lines.append("- Bank mass: **unmeasured**. It is left out of the stability estimate (section 4); weigh it (docs/12 E1).")
    lines.append("- Not checked: the real bank size, rounding, port positions or which end the micro-USB input is on; "
                 "real plug and lead sizes; strap tension; whether the bank can slide under shock.\n")
    keep = {"K1": k1, "K2": k2, "K3": k3, "K4": k4, "K5": k5, "K6": k6}
    return lines, problems, data, keep


def params_summary():
    return {
        "bank_model": "MINISO QW01 10000 mAh (owned)",
        "size_status": "user approximate estimate 2026-10-20; not measured",
        "nominal_mm": [BAT.len_nom, BAT.w_nom, BAT.t_nom],
        "accommodated_min_mm": [pt.BANK_L_MIN, pt.BANK_W_MIN, pt.BANK_T_MIN],
        "accommodated_max_mm": [pt.BANK_L_MAX, pt.BANK_W_MAX, pt.BANK_T_MAX],
        "port_plane_x": BAT.port_x,
        "port_assumptions": {"y_max": BAT.port_y_max, "edge_z": BAT.port_edge_z, "all_on_rear_end": True},
        "plugs_mm_protrusion_w_h_bend": {"out1_ADA3628": BAT.plug_out1, "out2_USB-A_to_C": BAT.plug_out2,
                                         "charge_micro_USB": BAT.plug_charge},
        "plug_sweep_depth": pt.PLUG_LEN, "plug_sweep_y": pt.SWEEP_Y, "plug_sweep_z": list(pt.SWEEP_Z),
        "default_shim_mm": round(pt.SHIM_Y[1] - pt.SHIM_Y[0], 2),
        "default_spacer_mm": round(pt.SPACER_X[1] - pt.SPACER_X[0], 2),
        "hatch_screw": "1 x M3 x 8 pan head, thread-forming",
    }
