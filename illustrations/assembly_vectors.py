"""Vector assembly-detail images (code-drawn, no CAD): 01, 02, 09, 10, 13.

Edit text and positions here. Facts follow docs/14 (stages), docs/12 (Q-rows),
docs/05 (charging, gates), docs/02 (software split) and docs/bom.csv (B-rows).
Nothing here records a measurement or a test result.
"""

from kit import Canvas, INK, INK2, MUTED, NETS, BADGES

OUT = "docs/images/assembly-detail"
FOOT = "Pip v0.3 · code-drawn diagram, not a photo · no part of Pip has been built or tested   · illustrations/assembly_vectors.py"


def checklist(c, x, y, w, rows, size=21, gap=14):
    """rows: (text, badge kind or None, badge label). Draws an empty tick box per row."""
    cy = y
    for text, kind, label in rows:
        c.rect(x, cy - 2, 26, 26, fc="white", ec=INK, lw=2, r=4, z=5)
        tw = w - 50 - (0 if not kind else 0.6 * 19 * len(label or kind) + 40)
        from kit import wrap
        body = wrap(text, tw, size)
        c.text(x + 42, cy - 4, body, size, va="top")
        if kind:
            c.badge(x + w, cy + 11, kind, label, size=18, anchor="right")
        cy += (body.count("\n") + 1) * size * 1.28 + gap
    return cy


# ============================================================================ 01
def tools_inventory():
    c = Canvas(2400, 1200, "Tools and inventory",
               "Tick what is actually in hand. This is an inventory, not a shopping list or a purchase approval.",
               [("HOLD", "PURCHASES ON HOLD (D1)")], FOOT, number="Detail 1")
    c.panel(60, 190, 740, 920, "Tools", gid="tools")
    checklist(c, 90, 260, 680, [
        ("Digital calipers", "OK", "essential"),
        ("Kitchen scale (bank mass, Q8)", None, None),
        ("Screwdriver to suit your M3 and M2.5 screws", None, None),
        ("Flush cutters, deburring tool, craft knife (adult for knives)", None, None),
        ("Pin vice or drill, 2.4 / 2.5 / 2.6 mm bits: M3 pilot test only", None, None),
        ("Masking tape and marker for labels", None, None),
        ("Phone camera for evidence photos", None, None),
        ("Force scale, about 50 N (T-SAF-9)", "PENDING", "borrow"),
        ("Multimeter", "HOLD", "HOLD stages"),
        ("Wire strippers", "HOLD", "HOLD stages"),
    ])
    c.para(90, 800, "No soldering iron is needed at any stage.", 680, 22, bold=True)

    c.panel(830, 190, 760, 920, "Electronics", gid="elec")
    c.text(860, 260, "Owned", 23, bold=True, color=INK2)
    y = checklist(c, 860, 300, 700, [
        ("MINISO QW01 bank (size approximate)", "OK", "owned"),
        ("Raspberry Pi Pico 2 WH", "OK", "owned"),
        ("PiicoDev Starter Kit (assumed v1.2)", "OK", "owned"),
        ("Standard PiicoDev SH-to-SH cables for C1–C9 (BOM O1)", "OK", "owned"),
    ])
    c.text(860, y + 20, "Not bought", 23, bold=True, color=INK2)
    checklist(c, 860, y + 60, 700, [
        ("Kitronik 5331 motor board (B1)", "HOLD", None),
        ("2 × TT motor (B2)", "HOLD", None),
        ("FS90 servo (B3)", "HOLD", None),
        ("DFR1154 camera board; speaker supplied with it (B4)", "HOLD", None),
        ("2 × PiicoDev Button (B6)", "HOLD", None),
        ("B7 PiicoDev prototyping cable", "UNVERIFIED", "ownership?"),
        ("ADA3628 USB-A terminal adapter (B8)", "HOLD", None),
        ("2 × Wago 221-413 (B9)", "HOLD", None),
        ("B11 USB-A to C cable, B12 in-line switch", "HOLD", None),
        ("~22 AWG red and black wire (B14)", "HOLD", None),
    ], size=20, gap=10)

    c.panel(1620, 190, 720, 920, "Fasteners and open parts", gid="fast")
    y = checklist(c, 1650, 260, 660, [
        ("6 × M3 × 10 thread-forming", None, None),
        ("5 × M3 × 8 thread-forming", None, None),
        ("4 × M3 × 12 thread-forming", None, None),
    ])
    c.text(1650, y + 6, "= 15 × M3 in total (B16)", 22, bold=True)
    y = checklist(c, 1650, y + 60, 660, [
        ("4 × M2.5 × 6 (Buttons)", None, None),
        ("2 × hook-and-loop strap, about 12 × 250 mm", None, None),
        ("2 × O-ring or thick band, about 60 mm ID", None, None),
    ])
    c.text(1650, y + 20, "Not selected yet", 23, bold=True, color=INK2)
    checklist(c, 1650, y + 60, 660, [
        ("B18 servo tab and horn hardware (not in the 15 M3)", "NOT SELECTED", "unspecified"),
        ("B19 PiicoDev bus interface", "NOT SELECTED", None),
        ("B20 rated servo power harness (unpriced)", "NOT SELECTED", None),
        ("B10 jumpers: provisional, servo signal only", "UNVERIFIED", "provisional"),
    ], size=20, gap=12)
    return c.save(OUT, "01-tools-inventory")


# ============================================================================ 02
def measure_bank():
    c = Canvas(2400, 1640, "Measure the QW01 before printing",
               "Fill every blank from your own bank. The 130 × 60 × 10 mm figures are the user's estimate, not measurements.",
               [("UNVERIFIED", "SIZE ESTIMATED"), ("STOP", "DO NOT OPEN THE BANK")], FOOT, number="Detail 2")
    c.panel(60, 190, 1080, 900, "Sketch (not to scale)", gid="sketch")
    # oblique box
    ox, oy, L, W, T, k = 300, 640, 600, 240, 70, 0.55
    dx, dy_ = W * k, W * k * 0.75
    front = [(ox, oy), (ox + L, oy), (ox + L, oy + T), (ox, oy + T)]
    top = [(ox, oy), (ox + dx, oy - dy_), (ox + L + dx, oy - dy_), (ox + L, oy)]
    end = [(ox + L, oy), (ox + L + dx, oy - dy_), (ox + L + dx, oy - dy_ + T), (ox + L, oy + T)]
    c.poly(top, "#F2D9B0", z=3)
    c.poly(front, "#E0A040", z=3)
    c.poly(end, "#B97A22", z=3)
    c.text(ox + L / 2 + dx / 2, oy - dy_ / 2, "MINISO QW01 (owned)", 24, bold=True, ha="center")
    # length
    ly = oy + T + 50
    c.line([(ox, ly), (ox + L, ly)], INK, lw=2.4)
    for xx in (ox, ox + L):
        c.line([(xx, ly - 14), (xx, ly + 14)], INK, lw=2.4)
    c.text(ox + L / 2, ly + 36, "length ≈130 mm (estimate) → Q1", 22, bold=True, ha="center")
    # width, along the top edge of the end face, offset outward
    a, b = (ox + L + 34, oy - 6), (ox + L + dx + 34, oy - dy_ - 6)
    c.line([a, b], INK, lw=2.4)
    for p_ in (a, b):
        c.line([(p_[0] - 10, p_[1] - 10), (p_[0] + 10, p_[1] + 10)], INK, lw=2.4)
    c.text(b[0] - 10, b[1] - 50, "width ≈60 mm\n(estimate) → Q2", 22, bold=True, ha="center", va="bottom")
    # thickness
    c.line([(ox - 30, oy), (ox - 30, oy + T)], INK, lw=2.4)
    for yy in (oy, oy + T):
        c.line([(ox - 44, yy), (ox - 16, yy)], INK, lw=2.4)
    c.text(ox - 56, oy + T / 2, "thickness\n≈10 mm (est.)\n→ Q3", 22, bold=True, ha="right")
    c.callout("Which end carries each port? Positions are unknown (Q5, Q6). The CAD assumes all three on one end.",
              (ox + L + dx / 2, oy - dy_ / 2 + T / 2), (540, 860), size=21, width=540)
    c.para(90, 1000, "Tape a label on each port: \"OUT 1 → body\", \"OUT 2 → camera\", \"IN (charge)\".", 1020, 21, color=INK2)

    c.panel(1170, 190, 1170, 1210, "Record (docs/12 §A0)", gid="record")
    rows = [("Q1", "Length, longest point", "126–134"), ("Q2", "Width, widest point", "56–64"),
            ("Q3", "Thickness incl. any bulge", "8–16"), ("Q4", "Edge rounding", "—"),
            ("Q5", "Which end or face has each port?", "all on one end"),
            ("Q6", "Each port centre from centre line / bottom", "≤16 / ≥3"),
            ("Q7", "Charge LED or button position", "—"), ("Q8", "Mass (kitchen scale)", "—"),
            ("Q9", "ADA3628 protrusion + bend room", "—"), ("Q10", "USB-A→C overmould size", "—"),
            ("Q11", "Micro-USB charge plug size", "—")]
    c.text(1200, 260, "Row", 20, bold=True, color=INK2)
    c.text(1290, 260, "Measure", 20, bold=True, color=INK2)
    c.text(1900, 260, "Your value", 20, bold=True, color=INK2)
    c.text(2150, 260, "CAD accepts", 20, bold=True, color=INK2)
    for i, (q, what, acc) in enumerate(rows):
        y = 320 + i * 92
        c.rect(1190, y - 34, 1130, 76, fc="white" if i % 2 == 0 else "#F7F6F2", ec="#D5D1C8", lw=1, r=6, z=2)
        c.text(1200, y, q, 22, bold=True)
        c.text(1290, y, what, 21)
        c.line([(1900, y + 14), (2110, y + 14)], INK2, lw=2)
        c.text(2150, y, acc, 20, color=INK2)
    c.text(1200, 1340, "Units: mm (Q1–Q6, Q9–Q11), g (Q8). Leave a blank if not measured.", 20, color=INK2)

    c.panel(60, 1130, 1080, 420, "STOP if", badge=("STOP", "STOP"), gid="stop")
    c.notes(90, 1190, 1020, [
        "any size is outside 126–134 × 56–64 × 8–16 mm;",
        "a port is on a side or the far end;",
        "a port centre is more than 16 mm from the centre line.",
    ], size=22, numbered=False, gap=10)
    c.para(90, 1340, "The cradle, rails or hatch then need a CAD change. Thinner fillers do not fix it.", 1020, 21, color=INK2)
    c.panel(1170, 1430, 1170, 120, None, gid="plug")
    c.para(1200, 1450, "Q9–Q11: measure how far each real plug sticks out past the port face, plus room for its cable to bend.", 1110, 21)
    return c.save(OUT, "02-measure-bank")


# ============================================================================ 09
def bank_state(c, x, y, out1, out2, inp):
    """Small bank sketch with three port slots. States: plugged, empty, charger."""
    c.rect(x, y, 300, 170, fc="#F2D9B0", ec=INK, lw=2.5, r=10, z=3)
    c.text(x + 20, y + 26, "QW01", 20, bold=True, check=False)
    for i, (name, state) in enumerate((("OUT 1", out1), ("OUT 2", out2), ("IN", inp))):
        py = y + 60 + i * 40
        c.rect(x + 270, py - 12, 30, 24, fc="#30363D", ec=INK, lw=1.5, r=3, z=4)
        c.text(x + 258, py, name, 18, bold=True, ha="right", check=False)
        if state == "plugged":
            c.rect(x + 300, py - 13, 90, 26, fc="#9AA3AD", ec=INK, lw=2, r=4, z=5)
            c.line([(x + 390, py), (x + 440, py)], NETS["5V"][0], lw=6, z=4)
        elif state == "charger":
            c.rect(x + 300, py - 11, 70, 22, fc="#D62828", ec=INK, lw=2, r=4, z=5)
            c.line([(x + 370, py), (x + 440, py)], NETS["5V"][0], lw=6, z=4)
        elif state == "removed":
            c.rect(x + 360, py - 13, 70, 26, fc="#C9CED6", ec=INK, lw=2, r=4, z=5)
            c.arrow((x + 330, py), (x + 450, py), color=INK, lw=2.5, head=14)


def charging_sequence():
    c = Canvas(2400, 1500, "Charging sequence (adult only)",
               "Both robot output plugs come out before the charger goes in. The order matters.",
               [("STOP", "ORDER MATTERS")], FOOT, number="Detail 9")
    steps = [
        ("Switch off", "Disable movement. Switch off the body and the camera switch.", ("plugged", "plugged", "empty"), None),
        ("Open the hatch", "Adult: remove the hatch M3 screw, tilt the hatch out, lift it off its tongues.", ("plugged", "plugged", "empty"), None),
        ("Unplug BOTH outputs", "Pull OUT 1 and OUT 2 by the plug bodies. Both, every time.", ("removed", "removed", "empty"), "STOP"),
        ("THEN charge", "Charger into micro-USB IN only. Hard surface, supervised, hatch off.", ("empty", "empty", "charger"), None),
        ("Unplug the charger", "Remove the charger before anything is reconnected.", ("empty", "empty", "removed"), None),
        ("Reconnect: HOLD", "Reconnect the robot leads only once the electrical design is cleared. For now, leave both out.", ("empty", "empty", "empty"), "HOLD"),
    ]
    for i, (title, body, state, badge) in enumerate(steps):
        col, row = i % 3, i // 3
        x, y = 60 + col * 770, 200 + row * 520
        c.panel(x, y, 740, 490, None, gid=f"step{i + 1}")
        c.marker(x + 46, y + 46, str(i + 1), size=26, r=28)
        c.text(x + 92, y + 46, title, 27, bold=True)
        if badge:
            c.badge(x + 716, y + 46, badge, None, size=19, anchor="right")
        bank_state(c, x + 60, y + 110, *state)
        c.para(x + 30, y + 330, body, 680, 22)
    c.para(60, 1260, "Port order in these sketches is not the physical order: the QW01's port positions are not measured yet. "
           "Never join the outputs, use a Y cable, pass-through charge, or charge through the head's USB-C lead.", 2280, 22, color=INK2)
    c.para(60, 1360, "Full procedure: docs/05 §6 and docs/14 Stage 18.", 2280, 21, color=INK2)
    return c.save(OUT, "09-charging-sequence")


# ============================================================================ 10
def test_and_record():
    c = Canvas(2400, 1160, "Tests and the evidence record",
               "What can be checked now, what waits for the power gates or firmware, and where real results go.",
               [("PENDING", "NO RESULTS RECORDED")], FOOT, number="Detail 10")
    cols = [
        ("Unpowered fit", ("OK", "after fit STOPs cleared"), [
            "T-MECH-1 coupon clearances", "T-MECH-2 wheel on shaft", "T-MECH-3 shells off/on < 3 min",
            "T-MECH-4 10 cm drop, bare chassis", "T-MECH-5 lift by the head", "T-MECH-6/7 bank fit and access",
            "Q12–Q16 bank fit trial", "T-SAF-1 static tip ≥ 25°", "T-SAF-8 finger probe at neck",
            "T-SAF-9 ~50 N pull test"]),
        ("Electrical gates", ("HOLD", "HOLD"), [
            "PG1 bank limits and branch budget", "PG2 servo rail under load", "PG3 source, motor, servo protection",
            "PG4 camera rail under load", "PG5 master disconnect, charging", "PG6 logic, sensor-chain and I2C bus capacity",
            "PG7 reset and watchdog"]),
        ("Firmware and bridge", ("FUTURE", "FUTURE"), [
            "Pico supervisor firmware", "Servo-centring routine (horn fit)", "DFR1154 camera and audio firmware",
            "Laptop bridge", "I2C scan: record every address", "Functional calibration (docs/12 §D)"]),
    ]
    for i, (head, badge, items) in enumerate(cols):
        x = 60 + i * 590
        c.panel(x, 190, 560, 620, head, badge=badge, heading_size=24, gid=f"col{i}")
        checklist(c, x + 26, 300, 510, [(t, None, None) for t in items], size=20, gap=16)
    x = 1830
    c.panel(x, 190, 510, 620, "Result record", badge=("PENDING", "blank"), heading_size=24, gid="rec")
    for j, field in enumerate(["Test ID", "Date", "Tester", "Setup", "Result", "Photo / file"]):
        y = 280 + j * 80
        c.text(x + 26, y, field, 21, bold=True)
        c.line([(x + 180, y + 12), (x + 480, y + 12)], INK2, lw=2)
    c.text(x + 26, 770, "not yet run", 22, color=MUTED, italic=True)
    c.panel(60, 840, 2280, 240, "Rules for the record", gid="rules")
    c.notes(90, 900, 2220, [
        "Leave a field blank until a real measurement is taken. Nothing in this image is a result.",
        "Record the date, the tester and a photo for every row. Keep open STOP and HOLD items in the record.",
        "Do not test past a known component rating to find its limit, and do not stall the motors by hand.",
    ], size=22, gap=10)
    return c.save(OUT, "10-test-and-record")


# ============================================================================ 13
def software_and_feedback():
    c = Canvas(2400, 1500, "Software split and feedback loops",
               "Planned roles for future software. No firmware, bridge code, file names or commands exist yet.",
               [("FUTURE", "ALL SOFTWARE FUTURE")], FOOT, number="Detail 13")
    c.panel(60, 190, 760, 1000, "ROBOT", gid="robot")
    c.component("pico", 90, 260, 700, 520, "Pico 2 WH (body)", "safety and control, local",
                fc="white", pins=[("r", "r", 200, None, "anchor"), ("r2", "r", 300, None, "anchor")])
    c.notes(120, 380, 640, [
        "Safety supervisor: never waits on Wi-Fi",
        "Motor commands expire after 0.2 s; watchdog",
        "Button A wake, Button B movement enable",
        "Servo ±70° firmware limit, slew-limited",
        "ToF stop at 350 mm; tilt-stop heuristic",
        "OLED, touch pads, RGB LED, buzzer",
    ], size=20, numbered=False, gap=6)
    c.component("head", 90, 820, 700, 330, "DFR1154 (head)", "camera · PDM mic · amp + speaker",
                fc="white", pins=[("r", "r", 110, None, "anchor"), ("r2", "r", 210, None, "anchor")])
    c.para(120, 960, "Streams camera frames and microphone audio. Plays speech audio from the laptop.", 640, 20)

    c.component("lap", 1100, 190, 760, 1000, "Laptop bridge", "FUTURE · runs locally", fc="white",
                pins=[("l", "l", 270, None, "anchor"), ("l2", "l", 370, None, "anchor"),
                      ("hl", "l", 740, None, "anchor"), ("hl2", "l", 840, None, "anchor"),
                      ("r", "r", 420, None, "anchor"), ("r2", "r", 520, None, "anchor")])
    blocks = [("Person detector + tracker", 330), ("Track ID, freshness and range", 420),
              ("Voice detection → speech-to-text (local first)", 560), ("Dialogue manager + safety filter", 650),
              ("Text-to-speech (local first)", 740)]
    for text, y in blocks:
        c.rect(1140, y - 32, 680, 64, fc="#EEF2F6", ec="#7A8FA6", lw=1.5, r=10, z=3)
        c.text(1480, y, text, 21, bold=True, ha="center")
    c.rect(1140, 840, 680, 130, fc="#FFF4DE", ec="#9A6200", lw=2, r=10, z=3)
    c.para(1160, 856, "OpenRouter API key lives here only: adult-owned, with a credit limit. "
           "Never on the robot, never in the repository.", 640, 20, bold=True)
    c.para(1140, 1010, "The bridge sends targets and behaviours. It never commands wheel PWM.", 680, 20, color=INK2)

    c.component("or", 2010, 490, 330, 300, "OpenRouter", "text model\n(provisional,\nprovider-neutral)",
                pins=[("l", "l", 120, None, "anchor"), ("l2", "l", 220, None, "anchor")], fc="white")

    def link(a, b, label, side_y=-28):
        c.wire([a, b], "WIFI")
        c.arrow((b[0] - 40 * (1 if b[0] > a[0] else -1), b[1]), b, color=NETS["WIFI"][0], lw=3)
        c.text((a[0] + b[0]) / 2, a[1] + side_y, label, 19, ha="center", color=INK, box=("white", "#9DA9B8"))

    link(c.P("pico", "r"), c.P("lap", "l"), "telemetry 10 Hz, events")
    link(c.P("lap", "l2"), c.P("pico", "r2"), "targets, behaviour, heartbeat")
    link(c.P("head", "r"), c.P("lap", "hl"), "camera frames, mic audio")
    link(c.P("lap", "hl2"), c.P("head", "r2"), "speech audio, camera on/off")
    link(c.P("lap", "r"), c.P("or", "l"), "text\nHTTPS", side_y=-48)
    link(c.P("or", "l2"), c.P("lap", "r2"), "text\nreply", side_y=-48)
    c.text(960, 250, "Wi-Fi\n(LAN or hotspot)", 20, ha="center", color=INK2, bold=True)

    c.panel(60, 1230, 2280, 200, "Feedback loops (planned)", badge=("FUTURE", "FUTURE"), gid="loops")
    c.notes(90, 1290, 1100, [
        "Head tracking: camera → tracker → track message → Pico → servo → new camera view.",
        "Follow distance: ToF → Pico → motors. Runs on the Pico; gated by target and range checks.",
    ], size=21, gap=10)
    c.notes(1230, 1290, 1080, [
        "Wi-Fi drop: motor commands expire after 0.2 s, so motion stops; the heartbeat timeout is a second stop. Pico-only games continue.",
        "Nothing offline is presented as AI. The robot does not follow anyone offline.",
    ], size=21, gap=10)
    return c.save(OUT, "13-software-and-feedback")


ALL = {
    "01-tools-inventory": tools_inventory,
    "02-measure-bank": measure_bank,
    "09-charging-sequence": charging_sequence,
    "10-test-and-record": test_and_record,
    "13-software-and-feedback": software_and_feedback,
}
