# 12 · Measurement and calibration checklist (before printing the full set)

User update, 2026-10-20: owned MINISO QW01, 10,000 mAh; approximately 130 × 60 × 10 mm, not exact. Micro-USB charging input and two USB-A outputs, each reported as 5 V / 2 A. Combined simultaneous output, protection, mass and low-load behaviour remain unverified.

CAD v0.3 (2026-10-21) is built around this **approximate** size. The model reserves a fixed 126–134 × 56–64 × 8–16 mm cavity envelope. Fillers and retention still need checking for the measured bank. Printed shims and a spacer take up the difference ([11](11-mechanical-design-print-assembly.md) §2a). The bank-fit regression passes against these envelopes only. **The real bank has not been fitted.** Its size, port positions and mass are still to be measured (§A0).

Only for parts actually bought, after the purchase decision ([08](08-bom-budget-sourcing.md)). Measure with digital calipers, write the value in "Measured", update the named parameter in [`params.py`](../cad/pip_robot/params.py), run `scripts/cad.sh`, and fix anything the report flags.

## A0. MINISO QW01 power bank (owned): measure before printing the tray, shims, spacer or rear shell

Do not open the bank or remove its case. Measure it as it is.

| # | What to measure | Parameter (`params.Battery` unless noted) | CAD value now | Measured |
|---|---|---|---|---|
| Q1 | Length (port end to far end), at the longest point | `len_nom`; must stay within `len_range` | 130 (user approx.); cradle accepts 126–134 | |
| Q2 | Width, at the widest point | `w_nom`; within `w_range` | 60 (user approx.); 56–64 | |
| Q3 | Thickness, at the thickest point (including any feet or bulge) | `t_nom`; within `t_range` | 10 (user approx.); 8–16 | |
| Q4 | Edge and corner rounding | `corner_r` (preview only) | 3 | |
| Q5 | Which end or face carries each port. **Are both USB-A outputs and the micro-USB input on the same end?** | port assumption in `bankfit.py` | all on the rear end, **not confirmed** | |
| Q6 | Each port's centre: distance from the bank's centre line and from its bottom face | `port_y_max`, `port_edge_z` | any centre within ±16 mm and ≥ 3 mm inside the faces | |
| Q7 | Charge-level LED or button position (still visible or reachable with the hatch off?) | — | not modelled | |
| Q8 | Mass, on a kitchen scale | `COMPONENT_MASS_G["power_bank"]` | **unmeasured**, left out of the stability estimate | |
| Q9 | ADA3628 length beyond the port face when fully inserted, plus wire bend room | `plug_out1` | 40 + 8 (from Adafruit's 52 mm overall) | |
| Q10 | USB-A → USB-C cable overmould: length beyond the port face, width and height | `plug_out2` | 32 × 16 × 9, + 12 bend | |
| Q11 | Micro-USB charging plug overmould, same measurements | `plug_charge` | 25 × 11 × 7, + 15 bend | |

After measuring, set the values and run `scripts/cad.sh --bank-fit-only`. It takes seconds. Then run the full `scripts/cad.sh` and reprint the tray fillers.

- **Inside the band:** set `len_nom`, `w_nom` and `t_nom` to the measured values. The shims (31.8 − W/2 mm) and the front spacer (133.8 − L mm) regenerate at the new thickness. The fixed cavity and tray do not change. Near the upper size limits, a filler may become too thin to print; the build rejects shims below 1 mm and front spacers below 1.5 mm. Redesign the fillers and rear keepers in that case rather than bypassing the check.
- **Outside the band, or a port outside the assumed zone:** the regression reports which keep-out is entered. The rails, plug sweep or hatch then need changing. Thinner fillers do not fix that.
- **Micro-USB input on a side or the far end:** the cradle rails would block it. Add a rail window and access before relying on charging. This is not modelled.
- **Port within ~13 mm of a side edge:** the rear corner keeper may foul the plug. Trim the keeper off and check that the two straps alone hold the bank (Q13).

Physical trial, after printing only the tray, the shims, the spacer and a test strip of the rear shell (or the full rear shell):

| # | Check | Pass |
|---|---|---|
| Q12 | Bank drops into the cradle with the fillers fitted, without force. It cannot rock, and the port end sits on the rear edge of the rails. | |
| Q13 | Both straps fitted. Bank does not move when the robot is tilted 30° in each direction and given a firm push by hand. | |
| Q14 | Both robot plugs can be removed, then the charging plug inserted, with fingers through the hatch opening, without touching the rear shell or hatch | |
| Q15 | Hatch closes over both fitted robot plugs without pressing on them. Screw goes in by hand with a screwdriver. | |
| Q16 | Leads route up the robot's left side behind the upright without crossing the rear-button plungers | |

## A. Bought parts

| # | Part | What to measure | Parameter(s) | Placeholder | Measured |
|---|---|---|---|---|---|
| E1 | Power bank (QW01) | See §A0: size, port end and positions, LED, mass, plugs | `Battery.*` | v0.3: 130 × 60 × 10 nominal (user approx.); cradle band 126–134 × 56–64 × 8–16 | User estimate only; MINISO QW01, micro-USB input, two USB-A outputs |
| E2 | Power bank | Label ratings per port and combined; low-load shut-off (PG1) | docs | combined output unknown | User reports 5 V / 2 A per port; shared total not established |
| E3 | TT motor | Body, shaft position, shaft Ø/flats/length, shaft-end screw hole | `Drive.tt_*` | 70 × 22.5 × 18.8; Ø5.4/3.7 | |
| E4 | FS90 | Body, tab span/height/thickness, spline offset/height, horn length | `Neck.servo_*`, `horn_*` | 22.5 × 12.1 × 22.4 | |
| E5 | Kitronik 5331 + Pico 2 WH | Board size; hole spacing; height with the Pico seated; **switch position, travel and slide direction**; terminal positions; terminal accepts PiicoDev cable pins? | `Boards.ctrl_*`, `switch_uv`, `switch_travel` | 63 × 35; holes 55 × 28; 22 mm; switch (−20, 3) | |
| E6 | PiicoDev Button × 2 | Board; **hole positions**; cap height above the board; travel; actual ID-switch setting | `btn_h`, `btn_holes`, `btn_*_yz` | 9.5 mm; holes ±10.16 diagonal; A all OFF, B ID:1 ON | |
| E7 | DFR1154 | Board size and thickness; **lens centre offset**, lens height and diameter; rear component height; **mic position**; USB-C position; speaker socket position; mounting holes | `cam_*`, `MIC_HOLES` | 42 × 42 × 1.6; lens at centre, 5 mm high, Ø6 | |
| E8 | DFR1154 view | Image of a grid at 0.5 m through the printed eye: check vignetting and the usable angle | `cam_fov_design` | 90° | |
| E9 | Speaker | Size; plug fits the DFR1154 socket? | `spk_*` | 30 × 20 × 5 | |
| E10 | USB-C plugs | Overmould size of the switch cable's male end (through the neck slots) | `usb_c_overmold` | 12.5 × 7 | |
| E11 | In-line switch | Switch body size (for a holder, not yet modelled) | — | — | |
| E12 | PiicoDev modules | Board size, hole pitch, OLED glass/active offsets, touch-pad positions, ToF and LED positions | `piico*`, `oled_*` | 25.4; 20.32 | |
| E13 | ADA3628, lever connectors | Size, for a mounting clip | — | — | |
| E14 | Screws | Actual M3/M2.5 thread-forming screws: core diameter → pilot size from the coupon | `M3_PILOT_R` (parts.py) | 2.5 mm pilot | |

## B. Electrical checks before first power

See the connection reference in [04](04-wiring-pin-plan.md) §5, the power-off checks and bring-up prerequisites in [16](16-wire-by-wire-assembly.md) Stages 12–13, and the gates PG1–PG7 in [05](05-power-budget-charging.md) §5. A multimeter is needed (borrow one; not in the BOM).

## C. Print calibration (fit_test_coupon)

| Fit | Variants | Choose | Update |
|---|---|---|---|
| TT shaft bore | +0.0 / +0.1 / +0.2 / +0.3 | | drive_wheel bore offset |
| Column peg Ø6, tray peg Ø5 | socket +0.0…+0.3 | | `Print.clearance` |
| Caster stem Ø8 (must swivel) | +0.0…+0.3 | | `Print.clearance` |
| PiicoDev peg posts | Ø2.0 / 2.2 / 2.4 / 2.6 | | base peg radius |
| M3 pilot | drill test pieces at 2.4 / 2.5 / 2.6 mm with your screws (not on the coupon yet) | | `M3_PILOT_R` |
| Hatch ledge M3 | screw the hatch on and off 10 times; thread must still hold | | `M3_PILOT_R`, ledge thickness in `parts.py` |
| Column jog | load the deck by hand (lift the frame by the deck); no visible bend at the jog | | `COLUMN_R`, walls/infill |

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
