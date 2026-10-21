"""Generate labelled assembly views from the v0.3 CAD, without changing geometry.

Run scripts/guide-images.sh from the repository root.
Images depict bought-part envelopes, not verified physical parts or wiring routes.
"""

from pathlib import Path
import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from pip_robot.assembly import PARTS
from render import _basis, _tris, render


OUT = Path(__file__).resolve().parents[1] / "docs" / "images" / "assembly"
ONLY = set()


def make_view(filename, title, names, labels, elev=23, azim=135, ghost=()):
    if ONLY and filename not in ONLY:
        return
    items = []
    for part in PARTS:
        if part.name not in names:
            continue
        items.append((_tris(part.make()), part.colour, 0.13 if part.name in ghost else 1))
    image, extent, _ = render(items, elev, azim, px_per_mm=3.8, ss=2)
    fig, ax = plt.subplots(figsize=(11, 8), dpi=180)
    fig.patch.set_facecolor("#f7f7f5")
    ax.imshow(image, extent=extent)
    right, up, _ = _basis(elev, azim)
    for text, point, location in labels:
        if isinstance(point, str):
            part = next(part for part in PARTS if part.name == point)
            box = part.make().bounding_box()
            point = (np.array(box[:3]) + np.array(box[3:])) / 2
        point = np.array(point)
        ax.annotate(text, xy=(point @ right, point @ up), xytext=location,
                    textcoords="axes fraction", fontsize=10, color="#132c40",
                    bbox=dict(boxstyle="round,pad=.45", fc="white", ec="#bac4cc"),
                    arrowprops=dict(arrowstyle="->", color="#195c80", lw=1.4))
    ax.set_axis_off()
    fig.suptitle(title, fontsize=17, fontweight="bold", color="#132c40")
    fig.text(.5, .025, "Pip v0.3 | millimetres | bought parts are placeholder envelopes | no physical build verified",
             ha="center", fontsize=9, color="#52616b")
    fig.tight_layout(rect=(.02, .05, .98, .94))
    fig.savefig(OUT / filename, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(filename, flush=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    drive = {"base_plate", "drive_wheel_L", "drive_wheel_R", "ref_tt_motor_L", "ref_tt_motor_R",
             "motor_strap", "motor_strap_2", "motor_strap_3", "motor_strap_4"}
    drive |= {f"caster_{part}_{end}" for part in ("fork", "wheel", "axle", "clip") for end in ("F", "R")}
    make_view("01-drive-base.png", "Build the four-wheel base | base and guards shown transparent", drive, [
        ("2 driven wheels\nFit rubber tyres", (0, 64, 32), (.02, .8)),
        ("2 TT motor envelopes\nFour printed straps", (-20, 42, 34), (.58, .88)),
        ("Front and rear swivel casters\nClip stems from above", (-66, 0, 18), (.02, .18)),
        ("Keep motor leads clear\nof shafts and wheels", (0, -45, 32), (.6, .2)),
    ], elev=40, azim=140, ghost=("base_plate",))
    frame = drive | {"tray", "column_L", "column_R", "rear_upright"}
    make_view("02-frame.png", "Add the cradle and upright", frame, [
        ("Jogged columns\nLower ends outboard", (24, 43, 130), (.02, .83)),
        ("Rear upright\nController faces rear", (-22, 0, 140), (.62, .82)),
        ("Thread two straps\nbefore fitting the tray", (40, 40, 49), (.02, .25)),
        ("Two lower M3 x 12 screws\nEnter from below", (24, -43, 18), (.58, .17)),
    ])
    bank = {"tray", "bank_shim_L", "bank_shim_R", "bank_front_spacer", "ref_power_bank"}
    make_view("03-bank.png", "Fit the measured QW01 with removable fillers", bank, [
        ("Port end faces the rear\nVerify all actual ports", (-47.5, 0, 54), (.02, .82)),
        ("Side shims + rear keepers\nRegenerate from measured width", (0, 31, 52), (.55, .82)),
        ("Front spacer\nRegenerate from measured length", (85, 0, 52), (.04, .12)),
        ("Straps use both pairs of slots\nStraps and cables not modelled", (40, -40, 49), (.55, .12)),
    ], elev=38, azim=145)
    electronics = frame | {"ref_controller", "ref_buttons", "ref_base_modules", "ref_power_bank",
                           "bank_shim_L", "bank_shim_R", "bank_front_spacer"}
    make_view("04-controller.png", "Mount the controller and rear buttons", electronics, [
        ("Kitronik + Pico envelope\n4 x M3 x 8 into standoffs", (-25, 0, 135), (.02, .88)),
        ("Two PiicoDev buttons\n4 x M2.5 x 6 total", (-30, -27, 92), (.6, .72)),
        ("Power leads go up robot-left\nNo motor power on breadboard", (-25, 43, 100), (.02, .4)),
        ("QW01 below electronics\nBoth USB outputs disconnected", (15, 0, 54), (.6, .16)),
    ], elev=15, azim=180)
    neck = electronics | {"top_deck", "ref_servo", "clutch_disc"}
    make_view("05-neck.png", "Fit the deck, servo and clutch", neck, [
        ("Servo sits on neck ledges\nCentre electrically before horn fit", (5, 0, 202), (.02, .88)),
        ("Clutch disc\nTune slip using printed variants", (0, 0, 218), (.57, .74)),
        ("2 upper M3 x 12 screws\nDeck to columns", (24, 27, 183), (.02, .62)),
        ("Camera USB lead passes\nthrough deck and neck slots", (-12, 0, 186), (.58, .4)),
    ], elev=18, azim=140)
    head = {"head_base", "head_cap", "eye_left_camera", "eye_right", "ref_cam_board", "ref_head_speaker"}
    make_view("06-head.png", "Assemble the camera head", head, [
        ("Camera envelope\nLens aligned with camera eye", "ref_cam_board", (.02, .82)),
        ("Speaker envelope\nMeasure supplied speaker first", "ref_head_speaker", (.57, .18)),
        ("Insert both eyes from inside\nFlanges retained by cap and base", "eye_right", (.02, .13)),
        ("Cap shown transparent\n2 x M3 x 10 from below", (0, 0, 300), (.6, .82)),
    ], elev=20, azim=145, ghost=("head_cap",))
    full = {p.name for p in PARTS if p.kind != "cal"}
    make_view("07-shells.png", "Close the shells after checks", full, [
        ("Camera eye\nCheck live image for masking", (48, 27, 264), (.02, .85)),
        ("Open ToF window\nKeep clear of glue and covers", (70, 0, 160), (.57, .68)),
        ("OLED, touch, RGB and buzzer\nFit modules before closing front", (80, 0, 118), (.02, .42)),
        ("4 shell M3 x 10 screws\nAccess from below", (60, 0, 16), (.57, .13)),
    ], elev=12, azim=32)
    opened = full - {"rear_hatch"}
    make_view("08-rear-service.png", "Reach the bank through the rear hatch", opened, [
        ("Wake and movement buttons\nSoftware sleep is not hard-off", (-75, -27, 92), (.02, .6)),
        ("Both output plugs must come out\nbefore micro-USB charging", (-47.5, 0, 54), (.57, .32)),
        ("Rear hatch removed in this view\nOne M3 x 8 + two bottom tongues", (-93, 0, 60), (.02, .12)),
        ("Body switch location is provisional\nSeparate head switch not modelled", (-60, -20, 122), (.57, .83)),
    ], elev=8, azim=180)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="+", choices=[
        "01-drive-base.png", "02-frame.png", "03-bank.png", "04-controller.png",
        "05-neck.png", "06-head.png", "07-shells.png", "08-rear-service.png",
    ], help="regenerate selected figures only")
    ONLY = set(parser.parse_args().only or ())
    main()
