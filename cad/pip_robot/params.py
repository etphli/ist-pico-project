"""Pip companion robot - CAD v0.1 parameters (millimetres).

EVERY dimension tagged `# MEASURE` is a placeholder taken from a datasheet,
retailer listing or a typical part. It MUST be checked against the physical part
before printing anything other than fit-test coupons. See
docs/12-measurement-calibration-checklist.md.

Coordinate system (assembly): origin on the floor under the robot centre,
+X = forward (the face/screen side), +Y = robot's left, +Z = up.
"""

from dataclasses import dataclass, field

VERSION = "0.1-prototype"


@dataclass(frozen=True)
class Print:
    clearance: float = 0.30        # general sliding/fit clearance per side
    press: float = 0.10            # press-fit interference allowance per side
    wall: float = 2.4              # default PLA wall
    shell: float = 2.4             # body / head shell thickness
    touch_membrane: float = 1.0    # thinned shell over capacitive pads  # TEST
    led_diffuser: float = 0.8      # thinned white shell over RGB LEDs   # TEST
    segs: int = 96                 # circular resolution for large parts
    segs_small: int = 40


@dataclass(frozen=True)
class Body:
    base_r: float = 95.0           # base plate radius
    base_z: float = 14.0           # underside of base plate above floor (ground clearance)
    base_t: float = 4.0
    # Revolved "egg/bell" outer profile of the body shell: (z, outer radius)
    profile: tuple = (
        (14.0, 95.0), (30.0, 97.0), (60.0, 97.5), (90.0, 95.0), (120.0, 89.0),
        (145.0, 79.0), (165.0, 67.0), (178.0, 56.0), (185.0, 47.0), (189.0, 38.0),
        (191.0, 32.5),
    )
    top_deck_z: float = 180.0      # underside of top deck
    top_deck_t: float = 5.0
    tray_z: float = 46.0           # underside of battery tray (above motors)
    tray_t: float = 3.0
    shell_tab_w: float = 14.0
    shell_tab_h: float = 6.0


@dataclass(frozen=True)
class Drive:
    # Adafruit/Core ADA3777 "TT" gearmotor envelope (retailer: 70 x 22 x 18 mm)  # MEASURE
    tt_len: float = 70.0           # along X
    tt_h: float = 22.5             # along Z
    tt_t: float = 18.8             # along Y
    tt_shaft_from_end: float = 11.0   # shaft centre to gearbox end face   # MEASURE
    tt_shaft_d: float = 5.4        # TT double-D shaft across round      # MEASURE
    tt_shaft_flat: float = 3.7     # across flats                        # MEASURE
    tt_shaft_len: float = 9.0      # shaft protrusion per side            # MEASURE
    wheel_d: float = 65.0          # printed drive wheel incl. tyre
    wheel_w: float = 18.0
    tyre_groove_d: float = 3.0     # O-ring / rubber-band tyre groove depth
    track: float = 128.0           # wheel centre-to-centre (Y)
    hub_gap: float = 4.0           # wheel inner face -> motor outer face (guard wall sits between)
    wheel_well_wall: float = 2.0
    wheel_well_gap: float = 4.0    # radial gap tyre->guard


@dataclass(frozen=True)
class Caster:
    x: float = 66.0                # +/- X position of front/rear swivel casters
    wheel_d: float = 22.0
    wheel_w: float = 9.0
    axle_d: float = 5.0            # printed axle pin
    trail: float = 8.0
    stem_d: float = 8.0
    fork_t: float = 3.0
    lift: float = 1.5              # casters sit this much ABOVE the drive-wheel plane
                                   # (rocker behaviour, avoids 4-point indeterminacy)
    tower_r: float = 25.0


@dataclass(frozen=True)
class Battery:
    # Consumer USB power bank, placeholder for a slim 10 000 mAh class bank.  # MEASURE
    len: float = 100.0             # along X
    w: float = 66.0                # along Y
    t: float = 24.0                # along Z
    rear_x: float = -84.0          # rear (charge-port) face X position
    port_z_off: float = 12.0       # charge-port centre above bank underside   # MEASURE
    port_w: float = 13.0           # USB-C plug overmold clearance window
    port_h: float = 8.0
    led_window: tuple = (8.0, 4.0)  # bank charge-level LED window          # MEASURE


@dataclass(frozen=True)
class Boards:
    # Cytron Robo Pico datasheet/listing: 88 x 72 mm, 4x M3 holes.            # MEASURE
    robo_w: float = 88.0           # along Y
    robo_h: float = 72.0           # along Z when mounted vertically
    robo_t: float = 1.6
    robo_comp_h: float = 16.0      # tallest component incl. Pico socket+Pico  # MEASURE
    robo_hole_inset: float = 4.0   # M3 hole centre inset from edges            # MEASURE
    robo_bottom_z: float = 78.0    # board lower edge height in assembly
    robo_back_x: float = -40.0     # X of board rear (component-side) face plane
    # Positions on Robo Pico (board coords: u along Y from board centre, v up from lower edge)
    btn_gp20_uv: tuple = (-35.0, 8.0)    # MEASURE (soft wake / sleep)
    btn_gp21_uv: tuple = (-21.0, 8.0)    # MEASURE (movement enable)
    switch_uv: tuple = (22.0, 6.0)       # MEASURE  on/off slide switch (rotate board so it sits low)
    switch_travel: float = 3.0           # MEASURE
    led_strip_uv: tuple = (0.0, 66.0)    # MEASURE  NeoPixel / status LEDs
    # PiicoDev modules (Core listing: 25.4 x 25.4 mm, M2.5 holes)
    piico: float = 25.4
    piico_hole_pitch: float = 20.32      # MEASURE
    oled_glass: tuple = (27.0, 19.5)     # Core CE07911 listing
    oled_active: tuple = (23.0, 11.0)    # Core CE07911 listing
    # Gravity speaker module FIT0449: 40 x 40 mm (DFRobot wiki)
    spk: float = 40.0
    spk_depth: float = 12.0              # MEASURE (module + speaker can)
    # XIAO ESP32S3 Sense stack (Core listing 21 x 17.8 x 15 mm with expansion board)
    xiao_l: float = 21.0
    xiao_w: float = 17.8
    xiao_h: float = 15.0
    cam_board: float = 8.5               # MEASURE  camera module body
    cam_aperture_d: float = 7.0          # lens clearance hole in eye
    usb_c_overmold: tuple = (12.5, 7.0)  # MEASURE  cable plug overmold W x H


@dataclass(frozen=True)
class Neck:
    # Feetech FS90 (Core CE09376 listing: 22.5 x 12.1 x 22.4 mm)               # MEASURE
    servo_l: float = 22.5
    servo_w: float = 12.1
    servo_h: float = 22.4
    servo_tab_span: float = 32.5          # MEASURE  overall length across mounting tabs
    servo_tab_z: float = 15.5             # MEASURE  tab underside above servo base
    servo_tab_t: float = 2.5
    servo_shaft_off: float = 5.6          # MEASURE  spline axis offset from body centre (X)
    servo_spline_above: float = 4.0       # MEASURE  spline top above body top
    horn_len: float = 32.0                # MEASURE  double-arm horn tip-to-tip
    horn_w: float = 6.0
    horn_t: float = 2.0
    od: float = 60.0                      # fixed neck sleeve
    wall: float = 3.0
    h: float = 28.0
    stop_deg: float = 75.0                # mechanical pan stops +/-
    clutch_teeth: int = 8
    clutch_arm_t: float = 1.6             # TUNE: thicker = higher slip torque
    clutch_arm_len: float = 14.0


@dataclass(frozen=True)
class Head:
    w: float = 120.0     # Y
    d: float = 92.0      # X
    h: float = 86.0      # Z
    r: float = 28.0      # corner radius
    eye_ring_od: float = 34.0
    eye_ring_id: float = 22.0
    eye_y: float = 27.0
    eye_z_off: float = 46.0   # eye centre above head floor
    gap_above_neck: float = 1.0


@dataclass(frozen=True)
class Front:
    oled_z: float = 122.0
    touch_z: float = 92.0
    spk_z: float = 62.0
    dist_z: float = 160.0
    rgb_z: float = 160.0
    rgb_y: float = 30.0


@dataclass(frozen=True)
class Params:
    pr: Print = field(default_factory=Print)
    body: Body = field(default_factory=Body)
    drive: Drive = field(default_factory=Drive)
    caster: Caster = field(default_factory=Caster)
    bat: Battery = field(default_factory=Battery)
    boards: Boards = field(default_factory=Boards)
    neck: Neck = field(default_factory=Neck)
    head: Head = field(default_factory=Head)
    front: Front = field(default_factory=Front)


P = Params()

# Rough masses (g) used ONLY for the static tip-angle estimate in validate.py.
# Sources: ADA3777 listing 30.6 g; others are estimates -> weigh real parts.
COMPONENT_MASS_G = {
    "power_bank": (190.0, "estimate - weigh yours"),
    "tt_motor_L": (30.6, "Core ADA3777 listing"),
    "tt_motor_R": (30.6, "Core ADA3777 listing"),
    "fs90_servo": (9.0, "estimate (9 g class)"),
    "robo_pico_with_pico": (45.0, "estimate"),
    "speaker_module": (15.0, "estimate"),
    "xiao_sense": (8.0, "estimate"),
    "piicodev_modules_x6": (24.0, "estimate"),
    "cables": (40.0, "estimate"),
}
PLA_DENSITY = 1.24          # g/cm3
EFFECTIVE_FILL = 0.55       # walls+infill fraction for estimate only
