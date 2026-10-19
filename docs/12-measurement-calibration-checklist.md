# 12 · Measurement and calibration checklist (before printing the full set)

User update, 2026-10-20: owned MINISO QW01, 10,000 mAh; approximately 130 × 60 × 10 mm, not exact. Micro-USB charging input and two USB-A outputs, each reported as 5 V / 2 A. Combined simultaneous output, protection, mass and low-load behaviour remain unverified. The current CAD still uses the older 100 × 66 × 24 mm placeholder. A placement check of the approximate footprint found tray/frame overlap, so fit is not approved.

Only for parts actually bought, after the purchase decision ([08](08-bom-budget-sourcing.md)). Measure with digital calipers, write the value in "Measured", update the named parameter in [`params.py`](../cad/pip_robot/params.py), run `scripts/cad.sh`, and fix anything the report flags.

## A. Bought parts

| # | Part | What to measure | Parameter(s) | Placeholder | Measured |
|---|---|---|---|---|---|
| E1 | Power bank | L × W × H; charge-input end; port heights; LED position; **two USB-A outputs?** | `Battery.*` | CAD remains 100 × 66 × 24 | User estimate 130 × 60 × 10, not fit-verified; MINISO QW01, micro-USB input, 2 USB-A outputs |
| E2 | Power bank | Label ratings per port and combined; low-load shut-off (PG1) | docs | combined output unknown | User reports 5 V / 2 A per port; shared total not established |
| E3 | TT motor | Body, shaft position, shaft Ø/flats/length, shaft-end screw hole | `Drive.tt_*` | 70 × 22.5 × 18.8; Ø5.4/3.7 | |
| E4 | FS90 | Body, tab span/height/thickness, spline offset/height, horn length | `Neck.servo_*`, `horn_*` | 22.5 × 12.1 × 22.4 | |
| E5 | Kitronik 5331 + Pico 2 WH | Board size; hole spacing; height with the Pico seated; **switch position, travel and slide direction**; terminal positions; terminal accepts PiicoDev cable pins? | `Boards.ctrl_*`, `switch_uv`, `switch_travel` | 63 × 35; holes 55 × 28; 22 mm; switch (−20, 3) | |
| E6 | PiicoDev Button × 2 | Board; **hole positions**; cap height above the board; travel; address-change method (no solder?) | `btn_h`, `btn_holes`, `btn_*_yz` | 9.5 mm; holes ±10.16 diagonal | |
| E7 | DFR1154 | Board size and thickness; **lens centre offset**, lens height and diameter; rear component height; **mic position**; USB-C position; speaker socket position; mounting holes | `cam_*`, `MIC_HOLES` | 42 × 42 × 1.6; lens at centre, 5 mm high, Ø6 | |
| E8 | DFR1154 view | Image of a grid at 0.5 m through the printed eye: check vignetting and the usable angle | `cam_fov_design` | 90° | |
| E9 | Speaker | Size; plug fits the DFR1154 socket? | `spk_*` | 30 × 20 × 5 | |
| E10 | USB-C plugs | Overmould size of the switch cable's male end (through the neck slots) | `usb_c_overmold` | 12.5 × 7 | |
| E11 | In-line switch | Switch body size (for a holder, not yet modelled) | — | — | |
| E12 | PiicoDev modules | Board size, hole pitch, OLED glass/active offsets, touch-pad positions, ToF and LED positions | `piico*`, `oled_*` | 25.4; 20.32 | |
| E13 | ADA3628, lever connectors | Size, for a mounting clip | — | — | |
| E14 | Screws | Actual M3/M2.5 thread-forming screws: core diameter → pilot size from the coupon | `M3_PILOT_R` (parts.py) | 2.5 mm pilot | |

## B. Electrical checks before first power

See [04](04-wiring-pin-plan.md) §5 and the gates PG1–PG7 in [05](05-power-budget-charging.md) §5. A multimeter is needed (borrow one; not in the BOM).

## C. Print calibration (fit_test_coupon)

| Fit | Variants | Choose | Update |
|---|---|---|---|
| TT shaft bore | +0.0 / +0.1 / +0.2 / +0.3 | | drive_wheel bore offset |
| Column peg Ø6, tray peg Ø5 | socket +0.0…+0.3 | | `Print.clearance` |
| Caster stem Ø8 (must swivel) | +0.0…+0.3 | | `Print.clearance` |
| PiicoDev peg posts | Ø2.0 / 2.2 / 2.4 / 2.6 | | base peg radius |
| M3 pilot | drill test pieces at 2.4 / 2.5 / 2.6 mm with your screws (not on the coupon yet) | | `M3_PILOT_R` |

## D. Functional calibration (after assembly, after the gates)

| Item | Method | Record |
|---|---|---|
| Wheel speed vs PWM | 2 m timed runs at several duty values | trim L/R; duty for ≤ 0.25 m/s |
| Servo centre and ±70° | eyes vs a straight-ahead target | µs at −70 / 0 / +70 |
| Clutch slip | hold the head, command a move | chosen `clutch_arm_t` |
| Camera bearing map | target at known angles (wide-angle lens) | pixel → bearing table |
| Camera size → range | person at 0.5 / 1 / 2 m | box-size → range curve (plausibility check) |
| ToF offset and valid flag | targets at 0.3 / 0.6 / 1.0 m | offset |
| Tilt threshold | tilt table | angle |
| Touch | per membrane thickness | sensitivity |
| Volume cap | sound level at 1 m | value |
