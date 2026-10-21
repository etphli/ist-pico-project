"""Six LOGICAL wiring diagrams for docs/04 and docs/16 (Pip v0.3).

Edit labels and positions here. Every number in a component() call is a canvas pixel:
component(id, x, y, width, height, title, sub, pins=[(name, side, offset, label, net)]).
Wires take lists of points; c.P(component, pin) returns a pin's position.

Wire IDs, terminal labels and open items follow docs/04-wiring-pin-plan.md
(W1-W17, W13a-d, C1-C9, B-rows, WO0-WO7 open items, PG-gates). If 04 changes, change this file.
These are logical maps: they do not show physical terminal order, connector
orientation, port positions or cable routes. Every circuit is on HOLD.
"""

from kit import Canvas, INK, INK2, MUTED, NETS

OUT = "docs/images/wiring"
LOGICAL_FOOTER = ("Logical map: box layout and pin order are NOT the physical terminal order. "
                  "Read the printed labels on the delivered parts.   Pip v0.3 · illustrations/wiring.py")
BADGES = [("LOGICAL", "LOGICAL MAP"), ("HOLD", "HOLD")]


# ============================================================================ 1
def power_overview():
    c = Canvas(2400, 1660, "Power overview: two separate bank outputs",
               "QW01 output 1 powers the body. Output 2 powers the head. Micro-USB is the bank's charging input only.",
               BADGES, LOGICAL_FOOTER, number="Wiring 1")

    # bank
    c.component("bank", 60, 300, 330, 900, "MINISO QW01", "owned power bank\n≈130 × 60 × 10 mm\n(user estimate)",
                pins=[("out1", "r", 180, "OUT 1\nUSB-A", "5V"), ("out2", "r", 760, "OUT 2\nUSB-A", "5V"),
                      ("in", "b", 165, "micro-USB IN", "5V")])
    c.para(84, 560, "Each output: 5 V / 2 A (label, user report)", 280, 21, color=INK2)
    c.badge(84, 690, "UNVERIFIED", "combined limit", size=20)
    c.para(84, 740, "Shared limit of both outputs together is unknown.", 280, 21, color=INK2)
    c.para(84, 860, "Port positions on the real bank are not known.", 280, 21, color=INK2)

    # ------------------------------------------------------------------ body
    c.panel(430, 190, 1560, 740, "BODY · bank output 1", badge=("HOLD", "HOLD: not cleared"), gid="body")
    c.component("ada", 520, 330, 250, 250, "ADA3628", "USB-A plug to\nterminals (B8)",
                pins=[("usb", "l", 150, None, "5V"), ("vbus", "r", 150, "VBUS", "5V"), ("gnd", "r", 205, "GND", "GND")])
    c.text(645, 610, "D+, D−, sleeve: unused", 20, color=MUTED, ha="center")
    c.component("lev", 860, 300, 210, 340, "Wago levers", "2 × 221-413 (B9)\none +5V, one GND",
                pins=[("in5", "l", 180, None, "5V"), ("ing", "l", 235, None, "GND"),
                      ("k5", "r", 180, None, "5V"), ("kg", "r", 235, None, "GND"),
                      ("s5", "r", 290, None, "5V"), ("sg", "r", 320, None, "GND")],
                title_size=25, sub_size=19)
    c.component("kit", 1170, 300, 360, 400, "Kitronik 5331", "+ Pico 2 WH",
                pins=[("p5", "l", 180, "Power +", "5V"), ("pg", "l", 235, "Power −", "GND"),
                      ("m1a", "r", 170, "Motor 1 A", "MOTOR_A"), ("m1b", "r", 215, "Motor 1 B", "MOTOR_B"),
                      ("m2a", "r", 265, "Motor 2 A", "MOTOR_A"), ("m2b", "r", 310, "Motor 2 B", "MOTOR_B"),
                      ("bus", "r", 365, "GND 3V GP0 GP1", None), ("gp27", "b", 90, "GP27", "SIG")])
    c.component("servo", 1170, 770, 360, 140, "FS90 servo", "power pigtail not selected\n(B20)",
                pins=[("v", "l", 45, None, "5V"), ("g", "l", 85, None, "GND"), ("sig", "t", 90, None, "SIG")],
                sub_size=20)
    c.component("motl", 1660, 400, 300, 125, "Left TT motor", None,
                pins=[("a", "l", 70, None, "MOTOR_A"), ("b", "l", 115, None, "MOTOR_B")], title_y=440)
    c.component("motr", 1660, 525, 300, 105, "Right TT motor", None,
                pins=[("a", "l", 40, None, "MOTOR_A"), ("b", "l", 85, None, "MOTOR_B")], title_y=590)
    c.component("pd", 1660, 650, 300, 160, "PiicoDev chain", "10 modules via B7\n(Wiring 2 and 3)",
                pins=[("in", "l", 15, None, None)], sub_size=20, title_y=712)

    c.wire([c.P("bank", "out1"), c.P("ada", "usb")], "USB")
    c.tag(455, 480, "W1", "5V")
    c.wire([c.P("ada", "vbus"), c.P("lev", "in5")], "5V")
    c.wire([c.P("ada", "gnd"), c.P("lev", "ing")], "GND")
    c.tag(815, 480, "W2", "5V", size=20)
    c.tag(815, 535, "W3", "GND", size=20)
    c.wire([c.P("lev", "k5"), c.P("kit", "p5")], "5V")
    c.wire([c.P("lev", "kg"), c.P("kit", "pg")], "GND")
    c.tag(1120, 480, "W4", "5V", size=20)
    c.tag(1120, 535, "W5", "GND", size=20)
    s5, sg = c.P("lev", "s5"), c.P("lev", "sg")
    c.wire([s5, (1120, s5[1]), (1120, 815), c.P("servo", "v")], "5V", dashed=True)
    c.wire([sg, (1095, sg[1]), (1095, 855), c.P("servo", "g")], "GND", dashed=True)
    c.tag(1108, 730, "W6 W7", "5V", size=20, dashed=True)
    c.wire([c.P("kit", "gp27"), c.P("servo", "sig")], "SIG")
    c.tag(1260, 735, "W8", "SIG", size=20)
    # each motor terminal is its own conductor
    for kp, mp, net, wid in (("m1a", ("motl", "a"), "MOTOR_A", "W9"), ("m1b", ("motl", "b"), "MOTOR_B", "W10"),
                             ("m2a", ("motr", "a"), "MOTOR_A", "W11"), ("m2b", ("motr", "b"), "MOTOR_B", "W12")):
        a, b = c.P("kit", kp), c.P(*mp)
        c.wire([a, b], net, lw=5)
        c.tag(1595, a[1], wid, net, size=17)
    bus = c.P("kit", "bus")
    c.bundle([bus, (1660, bus[1])])
    c.tag(1595, 720, "W13a–d", "SDA", size=18)

    c.rect(460, 700, 580, 210, fc="#FFF4DE", ec="#9A6200", lw=2, r=14, z=2)
    c.para(482, 716, "Body fault estimate 3.3–4.1 A exceeds the 2 A reported for one port. "
           "Nothing on output 1 is cleared (WO0). The servo taps 5 V before the Kitronik switch, "
           "so it stays live while OUT 1 is plugged in.", 540, 20)

    # ------------------------------------------------------------------ head
    c.panel(430, 960, 1560, 340, "HEAD · bank output 2", badge=("HOLD", "HOLD: PG4"), gid="head")
    c.component("sw", 690, 1040, 290, 150, "In-line switch", "B12 · USB-C\nfemale in → male out",
                pins=[("i", "l", 20, None, "5V"), ("o", "r", 20, None, "5V")], sub_size=20)
    c.component("dfr", 1170, 1020, 360, 220, "DFR1154", "camera · mic · amp\nUSB-C 5 V in",
                pins=[("usb", "l", 40, None, "5V"), ("spk", "r", 40, "SPK", "SIG")])
    c.component("spk", 1660, 1020, 300, 120, "Speaker", "supplied with DFR1154",
                pins=[("i", "l", 40, None, "SIG")], sub_size=20)
    c.wire([c.P("bank", "out2"), c.P("sw", "i")], "USB")
    c.tag(540, 1060, "W14", "5V", size=20)
    c.text(540, 1120, "B11 USB-A → C", 20, color=INK2, ha="center")
    c.wire([c.P("sw", "o"), c.P("dfr", "usb")], "USB")
    c.tag(1075, 1060, "W15", "5V", size=20)
    c.wire([c.P("dfr", "spk"), c.P("spk", "i")], "SIG")
    c.tag(1595, 1060, "W16", "SIG", size=20)
    c.para(1660, 1160, "Gravity port on DFR1154: unused", 300, 19, color=MUTED)

    # ------------------------------------------------------------------ laptop and Wi-Fi
    c.component("lap", 2030, 380, 320, 640, "Laptop", "Pip bridge\n(FUTURE software)\n\nno wire to\nthe robot")
    c.wire([(1450, 300), (1450, 268), (2190, 268), (2190, 380)], "WIFI")
    c.tag(1600, 268, "Wi-Fi data", "WIFI", size=19)
    c.wire([(1440, 1240), (1440, 1275), (2190, 1275), (2190, 1020)], "WIFI")
    c.tag(1830, 1275, "Wi-Fi data", "WIFI", size=19)

    # ------------------------------------------------------------------ charging
    c.component("chg", 60, 1330, 330, 150, "Charger", "micro-USB cable\nonly after BOTH\noutput plugs are out",
                sub_size=19, title_y=1356)
    c.arrow((225, 1328), (225, 1214), color=NETS["5V"][0], lw=5, head=26)

    c.notes(440, 1340, 1240, [
        "Never join the two outputs or use a Y cable. Both outputs come from one bank, so they may share "
        "ground inside it: no extra ground wire is added, and no isolation is claimed.",
        "Hard-off = unplug both USB-A plugs. Neither the Kitronik switch nor the camera switch isolates everything.",
        "No motor or servo current through Pico pins, the 3V terminal, PiicoDev cables, breadboards or jumper pins. "
        "The sensors use the 3V terminal and SH cables as intended.",
        "Charging and programming (W17) only with both output plugs removed: see Wiring 6.",
    ], size=21, gap=8)
    c.legend(1720, 1350, ["5V", "GND", "SIG", "MOTOR_A", "MOTOR_B", "WIFI"], size=19)
    return c.save(OUT, "01-power-overview")


# ============================================================================ 2
def piicodev_breakout():
    c = Canvas(2400, 1600, "Kitronik terminals to the PiicoDev chain (B7 cable)",
               "Four B7 conductors (W13a–d) join the Kitronik GND, 3V, GP0 and GP1 terminals to the first module.",
               BADGES, LOGICAL_FOOTER, number="Wiring 2")
    rows = [("gnd", 260, "GND", "GND"), ("v3", 360, "3V  (Pico 3V3 OUT)", "3V3"),
            ("gp0", 460, "GP0  I2C0 SDA", "SDA"), ("gp1", 560, "GP1  I2C0 SCL", "SCL"),
            ("gp27", 690, "GP27  servo signal", "SIG"), ("gp28", 790, "GP28  spare", "unused")]
    c.component("kit", 90, 230, 620, 880, "Kitronik 5331 + Pico 2 WH",
                "screw terminals, labelled by GPIO\n(Kitronik datasheet)",
                pins=[(n, "r", off, lab, net) for n, off, lab, net in rows])
    c.badge(112, 470, "LOGICAL", "order is logical", size=19)
    c.para(112, 520, "Read the printed label beside each terminal on the real board.", 250, 20, color=INK2)
    c.para(112, 690, "GPIO numbers are not header pin numbers.", 250, 20, color=INK2)

    c.component("b7", 1250, 430, 230, 420, "B7 cable", "SH plug end\n(CE07796, 200 mm,\nmale pins)",
                pins=[("gnd", "l", 60, None, "GND"), ("v3", "l", 160, None, "3V3"),
                      ("gp0", "l", 260, None, "SDA"), ("gp1", "l", 360, None, "SCL"),
                      ("out", "r", 210, None, None)], sub_size=20, title_y=470)
    for (pin, net, tag, ins) in (("gnd", "GND", "W13a · GND · black wire", "black"),
                                 ("v3", "3V3", "W13b · 3.3 V · red wire", "red"),
                                 ("gp0", "SDA", "W13c · SDA · blue wire", "blue"),
                                 ("gp1", "SCL", "W13d · SCL · yellow wire", "yellow")):
        a = c.P("kit", pin)
        b = c.P("b7", pin)
        c.wire([a, (900, a[1]), (900, b[1]), b] if a[1] != b[1] else [a, b], net)
        c.tag(1060, b[1], tag, net, size=20, swatch=ins)
    c.text(1080, 400, "wire colour chips = B7 insulation colours (Core product page)", 19, color=INK2, ha="center")

    c.component("ba", 1640, 520, 300, 240, "Button A", "wake · first module\n0x42 (ID 1–4 OFF)\nrear upright",
                pins=[("in", "l", 120, None, None), ("out", "r", 120, None, None)], sub_size=20)
    c.bundle([c.P("b7", "out"), c.P("ba", "in")])
    c.tag(1560, 590, "SH plug", "SDA", size=19)
    c.bundle([c.P("ba", "out"), (2010, 640)])
    c.para(2050, 600, "C1 to Button B and the rest of the chain: Wiring 3", 300, 20, color=INK2)

    gp27 = c.P("kit", "gp27")
    c.component("srv", 1250, 880, 420, 90, "to FS90 signal (Wiring 5)", None, title_size=22,
                pins=[("in", "l", 40, None, "SIG")], title_y=925)
    c.wire([gp27, (900, gp27[1]), (900, 920), c.P("srv", "in")], "SIG")
    c.tag(1060, 920, "W8 · signal", "SIG", size=20)
    gp28 = c.P("kit", "gp28")
    c.line([gp28, (770, gp28[1])], MUTED, lw=4)
    c.cross(790, gp28[1], s=10, color=MUTED, lw=4)
    c.text(820, gp28[1], "not connected", 20, color=MUTED)

    c.panel(1720, 820, 620, 690, "Bus conditioning", badge=("NOT SELECTED", "B19 NOT SELECTED"), gid="cond")
    c.notes(1744, 890, 580, [
        "Core's B7 page recommends 4.7 kΩ pull-ups and 120 Ω series resistors when wiring a module "
        "directly to a microcontroller. Equivalent conditioning on the Kitronik terminals is not documented: assess under B19.",
        "Ten modules already add their own pull-ups in parallel. Adding more without a calculation could make the bus too strong.",
        "B19 (interface, unselected) may change how W13 is wired. This drawing is direct wiring as now listed (WO1).",
    ], size=20, gap=10)

    c.panel(90, 1160, 1580, 350, "Rules", gid="rules")
    c.notes(114, 1220, 1530, [
        "Male pins clamping securely in the Kitronik screw terminals is unconfirmed (WO2).",
        "The 3V terminal is the Pico's 3V3 OUT. Its capacity is not stated; the Pico datasheet recommends under 300 mA (PG6, WO6).",
        "Never connect 5 V to a GPIO terminal or to the PiicoDev chain.",
        "Future firmware must set I2C0 to GP0 (SDA) and GP1 (SCL); the PiicoDev library defaults to GP8 and GP9. "
        "First scan at 100 kHz only; the OLED driver recommends at least 400 kHz later (FUTURE).",
    ], size=21, gap=8)
    return c.save(OUT, "02-piicodev-breakout")


# ============================================================================ 3
MODULES_ROW1 = [  # id, title, sub
    ("ba", "Button A", "wake\n0x42 · ID 1–4 OFF"),
    ("bb", "Button B", "movement enable\n0x09 · ID 1 ON,\nID 2–4 OFF"),
    ("atm", "Atmospheric", "mount not modelled\n(WO5)\nscan and record"),
    ("acc", "Accelerometer", "behind colour sensor\nscan and record"),
    ("col", "Colour", "front, facing down\nscan and record"),
]
MODULES_ROW2 = [  # right to left
    ("tch", "Touch", "below the OLED\nscan and record"),
    ("oled", "OLED", "belly window\nscan and record"),
    ("buz", "Buzzer", "right cheek\nscan and record"),
    ("tof", "ToF distance", "chest window\nscan and record"),
    ("rgb", "RGB LED", "left cheek\nscan and record"),
]


def module_chain():
    c = Canvas(2400, 1660, "PiicoDev module chain: ten modules, cables C1–C9",
               "B7 feeds Button A. Nine standard SH-to-SH cables continue the bus. C5 is the front-shell service break.",
               BADGES, LOGICAL_FOOTER, number="Wiring 3")
    w, h, gap, x0 = 300, 210, 110, 300
    xs = [x0 + i * (w + gap) for i in range(5)]
    c.panel(270, 200, 1240, 430, "REAR UPRIGHT", gid="z-upright")
    c.panel(1530, 200, 820, 430, "BASE PLATE", gid="z-base")
    c.panel(270, 820, 2080, 400, "FRONT SHELL · stays plugged together on the shell", gid="z-front")
    y1, y2 = 300, 940
    for (mid, title, sub), x in zip(MODULES_ROW1, xs):
        c.component(mid, x, y1, w, h, title, sub, sub_size=20,
                    pins=[("l", "l", 105, None, "anchor"), ("r", "r", 105, None, "anchor"), ("b", "b", w / 2, None, "anchor")])
    for (mid, title, sub), x in zip(MODULES_ROW2, reversed(xs)):
        c.component(mid, x, y2, w, h, title, sub, sub_size=20,
                    pins=[("l", "l", 105, None, "anchor"), ("r", "r", 105, None, "anchor"), ("t", "t", w / 2, None, "anchor")])

    c.component("kit", 50, 640, 200, 150, "Kitronik", "terminals\n(Wiring 2)", sub_size=19,
                pins=[("o", "t", 100, None, "anchor")])
    c.bundle([c.P("kit", "o"), (150, 405), c.P("ba", "l")])
    c.tag(150, 540, "B7", "SDA", size=20)

    chain = [m[0] for m in MODULES_ROW1]
    for i in range(4):
        a, b = c.P(chain[i], "r"), c.P(chain[i + 1], "l")
        c.bundle([a, b])
        c.tag((a[0] + b[0]) / 2, a[1] - 52, f"C{i + 1}", "SDA", size=21)
    a, b = c.P("col", "b"), c.P("tch", "t")
    c.bundle([a, b])
    c.tag(a[0], 700, "C5", "SDA", size=21)
    c.badge(a[0] - 60, 760, "HOLD", "service break: unplug C5 to remove the front shell", size=20, anchor="right")
    row2 = [m[0] for m in MODULES_ROW2]
    for i in range(4):
        a, b = c.P(row2[i], "l"), c.P(row2[i + 1], "r")
        c.bundle([a, b])
        c.tag((a[0] + b[0]) / 2, a[1] - 52, f"C{i + 6}", "SDA", size=21)

    # inset: the bus is parallel
    c.panel(50, 1260, 1150, 340, "Inside every module: one parallel bus", gid="inset")
    mx, my = 110, 1340
    c.rect(mx + 120, my, 300, 200, fc="white", ec=INK, lw=2.5)
    c.text(mx + 270, my + 30, "any module", 20, bold=True, ha="center")
    nets = [("GND", "GND"), ("3V3", "3.3 V"), ("SDA", "SDA"), ("SCL", "SCL")]
    for i, (net, lab) in enumerate(nets):
        y = my + 70 + i * 34
        c.wire([(mx + 70, y), (mx + 470, y)], net, lw=5)
        c.text(mx + 60, y, lab, 18, bold=True, ha="right")
    for sx in (mx + 120, mx + 420):
        c.rect(sx - 14, my + 54, 28, 136, fc="#30363D", ec=INK, lw=1.5, r=4, z=5)
    c.text(mx + 120, my + 228, "socket", 18, color=INK2, ha="center")
    c.text(mx + 420, my + 228, "socket", 18, color=INK2, ha="center")
    c.para(680, 1320, "Both SH sockets carry the same four conductors. There is no IN or OUT socket, "
           "and nothing adds in series. Every module sees the same 3.3 V and the same SDA and SCL lines. "
           "Module order changes routing only.", 500, 20)

    c.panel(1240, 1260, 1110, 340, "Before this bus can be cleared", badge=("HOLD", "HOLD: WO1"), gid="clear")
    c.notes(1264, 1320, 1060, [
        "Ten-module bus load is UNVERIFIED. Core's connection guide warns that more than about six modules can overload the bus.",
        "Owning enough cables does not make the bus stronger: each module and cable adds capacitance and pull-ups.",
        "Use the shortest standard SH-to-SH cable that reaches, add strain relief, and record each length.",
    ], size=20, gap=6)
    return c.save(OUT, "03-module-chain")


# ============================================================================ 4
def body_power_split():
    c = Canvas(2400, 1660, "Body power split: two separate lever connectors",
               "One Wago 221-413 carries +5V (W2, W4, W6). A second, separate one carries GND (W3, W5, W7).",
               BADGES, LOGICAL_FOOTER, number="Wiring 4")
    c.component("ada", 80, 250, 480, 640, "ADA3628 (B8)", "USB-A plug to 5 screw terminals\n← W1 from QW01 OUT 1",
                pins=[("vbus", "r", 210, "VBUS", "5V"), ("dp", "r", 290, "D+", "unused"),
                      ("dm", "r", 360, "D−", "unused"), ("gnd", "r", 440, "GND", "GND"),
                      ("sl", "r", 530, "SLEEVE (shell)", "unused")], sub_size=20)
    c.para(102, 450, "The fifth terminal is the plug sleeve, not an ID pin.", 210, 20, color=INK2)
    c.para(102, 640, "Leave D+, D− and the sleeve empty.", 210, 20, color=INK2)
    for p in ("dp", "dm", "sl"):
        x, y = c.P("ada", p)
        c.cross(x + 36, y, s=11, color=MUTED, lw=4)

    c.component("w5", 860, 250, 440, 300, "+5V lever connector", "Wago 221-413 (B9)\nnet BODY_5V",
                pins=[("p1", "l", 210, None, "5V"), ("p2", "r", 150, None, "5V"), ("p3", "t", 410, None, "5V")],
                sub_size=20)
    p1, p2, p3 = c.P("w5", "p1"), c.P("w5", "p2"), c.P("w5", "p3")
    c.text(p3[0] - 30, p3[1] - 26, "3", 21, bold=True, ha="center")
    c.line([p1, (p3[0], p1[1]), p3], NETS["5V"][0], lw=9, z=5)
    c.line([(p3[0], p2[1]), p2], NETS["5V"][0], lw=9, z=5)
    c.text(p1[0] + 20, p1[1] - 26, "1", 21, bold=True)
    c.text(p2[0] - 30, p2[1] - 28, "2", 21, bold=True)
    c.text(1050, 505, "all 3 points: one potential", 20, color=INK2, ha="center")

    c.component("wg", 860, 760, 440, 300, "GND lever connector", "Wago 221-413 (B9)\nnet BODY_GND",
                pins=[("p1", "l", 200, None, "GND"), ("p2", "r", 120, None, "GND"), ("p3", "r", 220, None, "GND")],
                sub_size=20)
    g1, g2, g3 = c.P("wg", "p1"), c.P("wg", "p2"), c.P("wg", "p3")
    c.line([g1, (1250, g1[1]), (1250, g2[1]), g2], NETS["GND"][0], lw=9, z=5)
    c.line([(1250, g1[1]), (1250, g3[1]), g3], NETS["GND"][0], lw=9, z=5)
    c.text(g1[0] + 20, g1[1] - 26, "1", 21, bold=True)
    c.text(g2[0] - 30, g2[1] - 28, "2", 21, bold=True)
    c.text(g3[0] - 30, g3[1] + 28, "3", 21, bold=True)
    c.text(1040, 1010, "all 3 points: one potential", 20, color=INK2, ha="center")

    c.component("kit", 1500, 260, 420, 300, "Kitronik 5331", "power input terminal\n(then board switch, Pico)",
                pins=[("p", "l", 140, "Power +", "5V"), ("n", "l", 240, "Power −", "GND")], sub_size=20)
    c.component("servo", 1500, 860, 420, 240, "FS90 servo plug", "logical functions,\nnot the plug's pin order",
                pins=[("g", "l", 120, "GND", "GND"), ("sig", "l", 190, "signal", "SIG"), ("v", "r", 120, "V+", "5V")],
                sub_size=20)

    vb, gd = c.P("ada", "vbus"), c.P("ada", "gnd")
    c.wire([vb, c.P("w5", "p1")], "5V")
    c.tag(720, 460, "W2", "5V", size=21)
    c.wire([gd, (700, gd[1]), (700, 960), c.P("wg", "p1")], "GND")
    c.tag(700, 840, "W3", "GND", size=21)
    c.wire([c.P("w5", "p2"), c.P("kit", "p")], "5V")
    c.tag(1400, 400, "W4", "5V", size=21)
    p2 = c.P("wg", "p2")
    c.wire([p2, (1400, p2[1]), (1400, 500), c.P("kit", "n")], "GND")
    c.tag(1400, 700, "W5", "GND", size=21)
    p3 = c.P("w5", "p3")
    sv = c.P("servo", "v")
    c.wire([p3, (p3[0], 200), (2110, 200), (2110, sv[1]), sv], "5V", dashed=True)
    c.tag(1700, 200, "W6", "5V", size=21, dashed=True)
    c.wire([c.P("wg", "p3"), c.P("servo", "g")], "GND", dashed=True)
    c.tag(1400, 980, "W7", "GND", size=21, dashed=True)
    sig = c.P("servo", "sig")
    c.wire([(1340, sig[1]), sig], "SIG")
    c.text(1480, sig[1] + 52, "W8 from GP27 (Wiring 5)", 19, color=INK2, ha="right")
    c.badge(1960, 1050, "NOT SELECTED", "W6/W7 pigtail", size=19)
    c.para(1960, 1085, "Rated ~22 AWG pre-terminated servo harness (B20, WO3). Never thin M/M jumper tails.",
           380, 19, color=INK2)

    # bottom panels
    c.panel(80, 1210, 800, 370, "Strip lengths", gid="strip")
    y = 1370
    c.line([(150, y), (560, y)], NETS["5V"][0], lw=20, z=4)
    c.line([(560, y), (720, y)], "#B87333", lw=9, z=4)
    c.line([(110, y), (150, y)], "#B87333", lw=9, z=4)
    c.line([(560, y - 40), (720, y - 40)], INK, lw=2.4)
    for xx in (560, 720):
        c.line([(xx, y - 52), (xx, y - 18)], INK, lw=2.4)
    c.text(640, y - 70, "11 mm", 22, bold=True, ha="center")
    c.text(740, y, "Wago end", 20, color=INK2)
    c.text(130, y + 50, "other end", 20, color=INK2, ha="left")
    c.para(104, 1450, "Wago end: 11 mm (Wago 221 data sheet). ADA3628 and Kitronik ends: strip to suit "
           "that terminal, from the actual part, then mark it. Do not apply 11 mm to every end.", 760, 20)

    c.panel(910, 1210, 600, 370, "Never", badge=("STOP", "STOP"), gid="never")
    c.rect(1080, 1270, 230, 120, fc="white", ec=INK, lw=2.5)
    c.text(1195, 1410, "one Wago", 20, bold=True, ha="center")
    c.wire([(950, 1300), (1080, 1300)], "5V")
    c.wire([(950, 1360), (1080, 1360)], "GND")
    c.cross(1195, 1330, s=60, lw=9)
    c.para(934, 1450, "Never put +5V and GND in the same lever connector. That is a short circuit.", 560, 21, bold=True)

    c.panel(1540, 1210, 800, 370, "Conductors", gid="cond")
    c.notes(1564, 1270, 750, [
        "W2–W5: known-rated ~22 AWG stranded copper (B14). Red for 5 V, black for GND. W2/W3 ≤ 15 cm.",
        "Wago 221-413 accepts 24–12 AWG; fine-stranded 0.14–4 mm².",
        "The servo taps BODY_5V before the Kitronik switch: live while OUT 1 is plugged in.",
    ], size=20, gap=8)
    return c.save(OUT, "04-body-power-split")


# ============================================================================ 5
def motors_and_servo():
    c = Canvas(2400, 1500, "Motors and head servo",
               "Each motor has two leads to its own terminal pair. The servo takes power from the lever connectors and its signal from GP27.",
               BADGES, LOGICAL_FOOTER, number="Wiring 5")
    c.component("ml", 80, 290, 380, 210, "Left TT motor", "own 28 AWG leads\nwith male pins (B2)",
                pins=[("a", "r", 80, "lead", "MOTOR_A"), ("b", "r", 150, "lead", "MOTOR_B")], sub_size=20)
    c.component("mr", 80, 590, 380, 210, "Right TT motor", "own 28 AWG leads\nwith male pins (B2)",
                pins=[("a", "r", 80, "lead", "MOTOR_A"), ("b", "r", 150, "lead", "MOTOR_B")], sub_size=20)
    c.component("kit", 820, 220, 760, 800, "Kitronik 5331 + Pico 2 WH", None,
                pins=[("m1a", "l", 150, "Motor 1 A", "MOTOR_A"), ("m1b", "l", 220, "Motor 1 B", "MOTOR_B"),
                      ("m2a", "l", 450, "Motor 2 A", "MOTOR_A"), ("m2b", "l", 520, "Motor 2 B", "MOTOR_B"),
                      ("p", "r", 130, "Power +", "5V"), ("n", "r", 200, "Power −", "GND"),
                      ("gp27", "r", 310, "GP27", "SIG")])
    # board internals: fixed tracks, not wires
    c.rect(1040, 300, 330, 620, fc="#EEF2F6", ec="#7A8FA6", lw=2, ls="--", r=12, z=3)
    c.para(1056, 312, "on the board's PCB: not wires you add", 300, 19, color=INK2)
    c.rect(1080, 400, 250, 100, fc="white", ec=INK, lw=2, z=4)
    c.text(1205, 450, "Pico 2 WH", 22, bold=True, ha="center")
    c.rect(1080, 700, 250, 100, fc="white", ec=INK, lw=2, z=4)
    c.text(1205, 750, "DRV8833 driver", 22, bold=True, ha="center")
    for x in (1120, 1155):
        c.line([(x, 500), (x, 700)], NETS["MOTOR_A"][0] if x == 1120 else NETS["MOTOR_B"][0], lw=3, ls=(0, (3, 2)), z=4)
    for x in (1255, 1290):
        c.line([(x, 500), (x, 700)], NETS["MOTOR_A"][0] if x == 1255 else NETS["MOTOR_B"][0], lw=3, ls=(0, (3, 2)), z=4)
    c.text(1137, 600, "GP2\nGP3", 18, bold=True, ha="right", va="center", box=("white", "#C9D2DC"))
    c.text(1272, 600, "GP6\nGP7", 18, bold=True, ha="left", va="center", box=("white", "#C9D2DC"))
    # driver to terminals (internal)
    for pin, net, yy in (("m1a", "MOTOR_A", 715), ("m1b", "MOTOR_B", 735), ("m2a", "MOTOR_A", 765), ("m2b", "MOTOR_B", 785)):
        px, py = c.P("kit", pin)
        xx = 990 + (yy - 715) * 0.5
        c.line([(1080, yy), (xx, yy), (xx, py), (975, py)], NETS[net][0], lw=2.5, ls=(0, (3, 2)), z=3)
    c.line([(1330, 450), (1460, 450), (1460, c.P("kit", "gp27")[1]), (1475, c.P("kit", "gp27")[1])],
           NETS["SIG"][0], lw=2.5, ls=(0, (3, 2)), z=3)
    c.para(840, 950, "GPIO numbers are not header pin numbers.", 700, 20, color=INK2)

    for mp, kp, wid in ((("ml", "a"), "m1a", "W9"), (("ml", "b"), "m1b", "W10"),
                        (("mr", "a"), "m2a", "W11"), (("mr", "b"), "m2b", "W12")):
        a, b = c.P(*mp), c.P("kit", kp)
        net = "MOTOR_A" if kp.endswith("a") else "MOTOR_B"
        c.wire([a, b], net)
        c.tag(640, a[1], wid, net, size=21)
    c.para(80, 830, "Each lead is its own conductor. Never join A and B.", 380, 20, color=INK2)

    for pin in ("p", "n"):
        a = c.P("kit", pin)
        c.wire([a, (1700, a[1])], "5V" if pin == "p" else "GND")
    c.text(1720, 385, "W4 / W5 from the lever\nconnectors (Wiring 4)", 19, color=INK2)

    c.component("servo", 1880, 500, 440, 380, "FS90 servo", "logical functions only.\nPlug order and lead colours\nfrom the supplier (WO4)",
                pins=[("sig", "l", 180, "signal", "SIG"), ("v", "l", 250, "V+", "5V"), ("g", "l", 320, "GND", "GND")],
                sub_size=19)
    g27, sg = c.P("kit", "gp27"), c.P("servo", "sig")
    c.wire([g27, (1740, g27[1]), (1740, sg[1]), sg], "SIG")
    c.tag(1740, 600, "W8", "SIG", size=21)
    for pin, net in (("v", "5V"), ("g", "GND")):
        a = c.P("servo", pin)
        c.wire([(1790, a[1]), a], net, dashed=True)
    c.tag(1760, 785, "W6 W7", "5V", size=19, dashed=True)
    c.para(1640, 900, "W6/W7 from the lever connectors. Rated pigtail B20 not selected. "
           "W8 conductor: B10 jumper (provisional, signal only) or B20's signal lead.", 700, 19, color=INK2)

    c.panel(80, 1070, 1200, 360, "Rules", gid="rules")
    c.notes(104, 1130, 1150, [
        "To reverse a motor, fix it in firmware or swap that motor's two leads with power removed. Lead colours are not assumed.",
        "Male pins clamping in the screw terminals is unconfirmed (WO2).",
        "No breadboard. No motor or servo current through Pico pins, the 3V terminal, PiicoDev cables or jumper pins.",
        "Never feed servo V+ from the 3V terminal.",
    ], size=21, gap=8)
    c.panel(1310, 1070, 1030, 360, "Open checks", badge=("HOLD", "HOLD"), gid="checks")
    c.notes(1334, 1130, 980, [
        "Body fault estimate 3.3–4.1 A exceeds the 2 A port (WO0). Do not connect motors or servo.",
        "The delivered servo's 3.3 V signal compatibility is unverified. Check its documentation or an approved PG2 plan (WO4).",
        "Servo supply margin is small: 4.8–6 V rating on a nominal 5 V bank (PG2).",
    ], size=20, gap=8)
    return c.save(OUT, "05-motors-and-servo")


# ============================================================================ 6
def head_and_charge():
    c = Canvas(2400, 1720, "Head power, programming and charging",
               "Output 2 feeds only the head. Programming and charging both start with BOTH output plugs removed.",
               BADGES, LOGICAL_FOOTER, number="Wiring 6")
    c.panel(60, 190, 2280, 580, "A · Head power: bank output 2", badge=("HOLD", "HOLD: PG4"), gid="a")
    c.component("bank", 100, 290, 260, 380, "QW01", "OUT 2\n5 V / 2 A\n(reported)",
                pins=[("o2", "r", 200, None, "5V")], sub_size=20)
    c.component("sw", 690, 390, 380, 200, "In-line switch (B12)", "USB-C female in\n→ switch → USB-C male out",
                pins=[("i", "l", 100, None, "5V"), ("o", "r", 100, None, "5V")], sub_size=20)
    c.component("dfr", 1360, 290, 470, 420, "DFR1154 camera board", "camera · PDM mic · amplifier\ndata: Wi-Fi to laptop",
                pins=[("usb", "l", 200, "USB-C 5 V in", "5V"), ("spk", "r", 150, "SPK (MX1.25)", "SIG"),
                      ("gr", "b", 340, None, "unused")], sub_size=20)
    c.text(1700, 650, "Gravity: UNUSED", 20, bold=True, color=MUTED, ha="center")
    c.cross(1700, 740, s=12, color=MUTED, lw=4)
    c.component("spk", 2010, 380, 300, 140, "Speaker", "supplied with\nDFR1154", pins=[("i", "l", 60, None, "SIG")],
                sub_size=20)
    c.wire([c.P("bank", "o2"), c.P("sw", "i")], "USB")
    c.tag(525, 490, "W14", "5V", size=21)
    c.text(525, 555, "B11 USB-A → USB-C\n50 cm, 2 A", 19, color=INK2, ha="center", va="top")
    c.wire([c.P("sw", "o"), c.P("dfr", "usb")], "USB")
    c.tag(1215, 490, "W15", "5V", size=21)
    c.text(1215, 555, "loops ≈80 mm body,\n≈60 mm head\n(provisional)", 19, color=INK2, ha="center", va="top")
    c.wire([c.P("dfr", "spk"), c.P("spk", "i")], "SIG")
    c.tag(1920, 440, "W16", "SIG", size=21)
    c.para(2010, 545, "Both speaker wires are amplifier outputs, not GND. No speaker wire to GND, a GPIO or the body.",
           310, 19, color=INK2)
    c.para(1860, 690, "Never plug a PiicoDev cable into the Gravity port.", 460, 19, color=INK2)

    # programming
    c.panel(60, 810, 1120, 560, "B · Initial programming (W17)", badge=("FUTURE", "Pip firmware future"), gid="b")
    c.component("bank2", 100, 900, 260, 300, "QW01", None,
                pins=[("o1", "r", 110, "OUT 1", "unused"), ("o2", "r", 210, "OUT 2", "unused")], title_y=940)
    for y in (1010, 1110):
        c.rect(420, y - 18, 70, 36, fc="#C9CED6", ec=INK, lw=2, r=5, z=5)
        c.arrow((400, y), (510, y), color=INK)
    c.text(455, 1240, "1. both output\nplugs OUT", 20, bold=True, ha="center", va="top")
    c.component("pico", 600, 960, 220, 160, "Pico 2 WH", "USB socket", pins=[("u", "r", 80, None, None)], sub_size=20)
    c.component("lap", 960, 960, 190, 160, "Laptop", None, pins=[("u", "l", 80, None, None)], title_y=1040)
    c.line([c.P("pico", "u"), c.P("lap", "u")], "#55606E", lw=10)
    c.tag(890, 1040, "W17", "#55606E", size=20)
    c.text(875, 1240, "2. Pico alone, out of carrier\nno external loads; then W17", 20, bold=True, ha="center", va="top")

    # charging
    c.panel(1220, 810, 1120, 560, "C · Charging (adult only)", gid="c")
    c.component("chg", 1260, 1000, 220, 150, "Charger", "micro-USB cable", sub_size=20)
    c.component("bank3", 1600, 900, 300, 380, "QW01", "only input:\nmicro-USB",
                pins=[("in", "l", 175, None, "5V"), ("o1", "r", 130, "OUT 1", "unused"), ("o2", "r", 250, "OUT 2", "unused")],
                sub_size=20)
    c.arrow((1482, 1075), (1590, 1075), color=NETS["5V"][0], lw=5, head=26)
    for y in (1030, 1150):
        c.rect(1960, y - 18, 70, 36, fc="#C9CED6", ec=INK, lw=2, r=5, z=5)
        c.arrow((1940, y), (2050, y), color=INK)
    c.notes(1940, 1200, 380, ["Remove both OUT plugs.", "THEN plug in micro-USB.",
                              "Unplug the charger before reconnecting anything."], size=19, gap=4)

    c.panel(60, 1410, 2280, 230, "Never", badge=("STOP", "STOP"), gid="never")
    items = ["join the two outputs", "use a Y or combining cable", "charge through a USB-A output (no pass-through)",
             "charge through the head's USB-C lead"]
    for i, s in enumerate(items):
        x = 110 + i * 560
        c.cross(x, 1520, s=14, lw=6)
        c.para(x + 34, 1500, s, 480, 21, bold=True)
    c.para(110, 1570, "Both outputs come from one bank and may share ground inside it. No extra ground wire is added; "
           "galvanic isolation is not claimed.", 2200, 20, color=INK2)
    return c.save(OUT, "06-head-and-charge")


ALL = {
    "01-power-overview": power_overview,
    "02-piicodev-breakout": piicodev_breakout,
    "03-module-chain": module_chain,
    "04-body-power-split": body_power_split,
    "05-motors-and-servo": motors_and_servo,
    "06-head-and-charge": head_and_charge,
}
