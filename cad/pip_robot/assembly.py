"""Part registry: what is printed, how many, in which orientation, and which bought
(reference) parts are placed in the assembly for clearance checks and previews."""

from dataclasses import dataclass
from typing import Callable

from . import parts as pt


@dataclass
class Part:
    name: str
    make: Callable
    kind: str                 # "print" or "ref"
    qty: int = 1
    material: str = "PLA"
    colour: str = "#f2f2f0"
    print_rot: tuple = (0, 0, 0)    # rotation applied before dropping onto the bed
    notes: str = ""


WHITE, DARK, GREY, REF = "#f4f3ef", "#202326", "#9aa3ad", "#e0a040"

PARTS = [
    Part("fit_test_coupon", pt.fit_test_coupon, "cal", 1, colour=GREY,
         notes="PRINT FIRST. Clearance variants for shaft/peg/stem fits; record results in docs/12."),
    Part("fit_test_pegs", pt.fit_test_pegs, "cal", 1, colour=GREY, notes="Pegs to try in the coupon."),
    Part("base_plate", pt.base_plate, "print", 1, colour=GREY,
         notes="Flat side down. Support ON for caster tower roofs only (enforcer)."),
    Part("tray", pt.tray, "print", 1, colour=GREY, print_rot=(180, 0, 0),
         notes="Upside down (lip on bed, legs up); support under the plate. Hook-and-loop strap through slots."),
    Part("column_L", pt.column, "print", 2, colour=GREY, print_rot=(0, 90, 0),
         notes="Print lying down for bending strength. Same part used left/right."),
    Part("rear_upright", pt.rear_upright, "print", 1, colour=GREY, print_rot=(0, 90, 0),
         notes="Print flat. Carries the controller board (4x M3) and two PiicoDev Buttons (M2.5)."),
    Part("top_deck", pt.top_deck, "print", 1, colour=GREY,
         notes="Deck down, neck up. Servo ledges are bridges - check first layers."),
    Part("front_shell", pt.front_shell, "print", 1, colour=WHITE, print_rot=(0, -90, 0),
         notes="Print seam-face down. Needs tree supports for the shoulder. White PLA."),
    Part("rear_shell", pt.rear_shell, "print", 1, colour=WHITE, print_rot=(0, 90, 0),
         notes="Print seam-face down. Tree supports. White PLA."),
    Part("head_cap", pt.head_cap, "print", 1, colour=WHITE,
         notes="Open side down; tree supports for the top. White PLA."),
    Part("head_base", pt.head_base, "print", 1, colour=GREY,
         notes="Skirt ring down; supports under the floor overhang and the snap hooks."),
    Part("clutch_disc", pt.clutch_disc, "print", 1, colour=GREY, print_rot=(180, 0, 0),
         notes="Print 3 variants of clutch_arm_t (1.2/1.6/2.0) and test slip torque."),
    Part("eye_left_camera", lambda: pt.eye(1), "print", 1, colour=DARK, print_rot=(0, -90, 0),
         notes="Black PLA. Inserted from inside the cap. Camera FOV aperture."),
    Part("eye_right", lambda: pt.eye(-1), "print", 1, colour=DARK, print_rot=(0, -90, 0),
         notes="Black PLA. Inserted from inside the cap."),
    Part("drive_wheel_L", lambda: pt.drive_wheel(1), "print", 1, colour=DARK, print_rot=(-90, 0, 0),
         notes="Fit O-ring / thick rubber band tyre in groove, or TPU tyre if available."),
    Part("drive_wheel_R", lambda: pt.drive_wheel(-1), "print", 1, colour=DARK, print_rot=(90, 0, 0)),
    Part("motor_strap", pt.motor_strap, "print", 4, colour=GREY, print_rot=(180, 0, 0)),
    Part("caster_fork_F", lambda: pt.caster_fork(1), "print", 2, colour=GREY,
         notes="Same part front/rear."),
    Part("caster_wheel_F", lambda: pt.caster_wheel(1), "print", 2, colour=DARK, print_rot=(90, 0, 0)),
    Part("caster_axle_F", lambda: pt.caster_axle(1), "print", 2, colour=GREY,
         notes="Exported lying on its side (layers along the pin). PETG preferred if available."),
    Part("caster_clip_F", lambda: pt.caster_clip(1), "print", 2, colour=GREY),
    Part("plunger_wake", lambda: pt.plunger(0), "print", 1, colour=WHITE, print_rot=(0, -90, 0),
         notes="Rear button A: wake/sleep (PiicoDev Button, I2C)."),
    Part("plunger_move", lambda: pt.plunger(1), "print", 1, colour=DARK, print_rot=(0, -90, 0),
         notes="Rear button B: movement enable (PiicoDev Button, I2C). Different colour on purpose."),
    Part("charge_door", pt.charge_door, "print", 1, colour=WHITE, print_rot=(0, 90, 0)),
    Part("switch_actuator", pt.switch_actuator, "print", 1, colour=DARK, print_rot=(0, 90, 0),
         notes="CONCEPT - fork geometry must be re-made after measuring the switch."),
    # mirrored assembly instances (geometry only, not exported separately)
    Part("column_R", lambda: pt.column().mirror((0, 1, 0)), "inst", 1, colour=GREY),
    Part("caster_fork_R", lambda: pt.caster_fork(-1), "inst", 1, colour=GREY),
    Part("caster_wheel_R", lambda: pt.caster_wheel(-1), "inst", 1, colour=DARK),
    Part("caster_axle_R", lambda: pt.caster_axle(-1), "inst", 1, colour=GREY),
    Part("caster_clip_R", lambda: pt.caster_clip(-1), "inst", 1, colour=GREY),
    Part("motor_strap_2", lambda: pt.motor_strap().translate((-35, 0, 0)), "inst", 1, colour=GREY),
    Part("motor_strap_3", lambda: pt.motor_strap().mirror((0, 1, 0)), "inst", 1, colour=GREY),
    Part("motor_strap_4", lambda: pt.motor_strap().mirror((0, 1, 0)).translate((-35, 0, 0)), "inst", 1, colour=GREY),
    # bought parts (envelopes) - for clearance checks and preview only
    Part("ref_power_bank", pt.ref_power_bank, "ref", colour=REF),
    Part("ref_tt_motor_L", lambda: pt.ref_tt_motor(1), "ref", colour="#e8c000"),
    Part("ref_tt_motor_R", lambda: pt.ref_tt_motor(-1), "ref", colour="#e8c000"),
    Part("ref_controller", pt.ref_controller, "ref", colour="#2a7a3a"),
    Part("ref_buttons", pt.ref_buttons, "ref", colour="#c03030"),
    Part("ref_servo", pt.ref_servo, "ref", colour="#3060c0"),
    Part("ref_cam_board", pt.ref_cam_board, "ref", colour="#2a7a3a"),
    Part("ref_head_speaker", pt.ref_head_speaker, "ref", colour="#e0a040"),
    Part("ref_front_modules", pt.ref_front_modules, "ref", colour="#c03030"),
    Part("ref_base_modules", pt.ref_base_modules, "ref", colour="#c03030"),
]

# Pairs that are SUPPOSED to touch/overlap slightly (press fits, pegs in sockets,
# parts captured against each other). Interference between any other pair is a
# design error and is reported by validate.py.
EXPECTED_CONTACT = {
    frozenset(p) for p in [
        ("base_plate", "front_shell"), ("base_plate", "rear_shell"),
        ("front_shell", "rear_shell"),
        ("column_L", "base_plate"), ("column_R", "base_plate"),
        ("column_L", "top_deck"), ("column_R", "top_deck"),
        ("tray", "base_plate"), ("rear_upright", "tray"), ("rear_upright", "top_deck"),
        ("rear_upright", "ref_controller"), ("rear_upright", "ref_buttons"),
        ("ref_tt_motor_L", "drive_wheel_L"), ("ref_tt_motor_R", "drive_wheel_R"),
        ("caster_fork_F", "caster_axle_F"), ("caster_fork_R", "caster_axle_R"),
        ("caster_wheel_F", "caster_axle_F"), ("caster_wheel_R", "caster_axle_R"),
        ("caster_fork_F", "caster_clip_F"), ("caster_fork_R", "caster_clip_R"),
        ("ref_servo", "clutch_disc"), ("ref_servo", "top_deck"),
        ("head_cap", "head_base"),
        ("motor_strap", "base_plate"), ("motor_strap_2", "base_plate"),
        ("motor_strap_3", "base_plate"), ("motor_strap_4", "base_plate"),
        ("ref_base_modules", "base_plate"),
        ("plunger_wake", "rear_shell"), ("plunger_move", "rear_shell"),
        ("charge_door", "rear_shell"), ("switch_actuator", "rear_shell"),
        ("switch_actuator", "ref_controller"),
        ("clutch_disc", "head_base"), ("ref_power_bank", "tray"),
        ("ref_cam_board", "head_base"), ("ref_head_speaker", "head_base"),
    ]
}

# Why each excluded pair is allowed to overlap. build.py prints the measured overlap
# volume for every pair so each one can be checked against this list.
EXPECTED_REASON = {
    "base_plate|front_shell": "shell ribs sit in plate notches",
    "base_plate|rear_shell": "shell ribs sit in plate notches",
    "front_shell|rear_shell": "butt seam at X=0 (0.3 mm gap expected; any overlap is an error)",
    "column_L|base_plate": "peg in socket", "column_R|base_plate": "peg in socket",
    "column_L|top_deck": "peg in socket", "column_R|top_deck": "peg in socket",
    "tray|base_plate": "legs in sockets", "rear_upright|tray": "legs in sockets",
    "rear_upright|top_deck": "tabs in sockets",
    "rear_upright|ref_controller": "board sits on standoffs",
    "rear_upright|ref_buttons": "modules sit on standoffs",
    "ref_tt_motor_L|drive_wheel_L": "shaft in wheel bore", "ref_tt_motor_R|drive_wheel_R": "shaft in wheel bore",
    "caster_fork_F|caster_axle_F": "axle in fork", "caster_fork_R|caster_axle_R": "axle in fork",
    "caster_wheel_F|caster_axle_F": "axle in wheel", "caster_wheel_R|caster_axle_R": "axle in wheel",
    "caster_fork_F|caster_clip_F": "clip on stem groove", "caster_fork_R|caster_clip_R": "clip on stem groove",
    "ref_servo|clutch_disc": "horn in clutch pocket", "ref_servo|top_deck": "servo tabs on ledges",
    "head_cap|head_base": "cap sits on floor", "clutch_disc|head_base": "disc in pocket",
    "motor_strap|base_plate": "strap peg in cradle", "motor_strap_2|base_plate": "strap peg in cradle",
    "motor_strap_3|base_plate": "strap peg in cradle", "motor_strap_4|base_plate": "strap peg in cradle",
    "ref_base_modules|base_plate": "modules on peg posts",
    "plunger_wake|rear_shell": "plunger in guide boss", "plunger_move|rear_shell": "plunger in guide boss",
    "charge_door|rear_shell": "door in rails", "switch_actuator|rear_shell": "actuator in slot",
    "switch_actuator|ref_controller": "fork around switch knob",
    "ref_power_bank|tray": "bank on tray",
    "ref_cam_board|head_base": "board in cradle slot", "ref_head_speaker|head_base": "speaker in cradle",
}
