# 12 · Measurement and calibration checklist (before printing the full set)

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

Measure with **digital calipers** (borrow from school if needed). Write each value in the "Measured" column, update the named parameter in [`cad/pip_robot/params.py`](../cad/pip_robot/params.py), run `scripts/cad.sh`, and fix anything the validation report flags. Commit the measured values with a short note.

## A. Bought parts: envelopes and features

| # | Part | What to measure | Parameter(s) | Placeholder | Measured |
|---|---|---|---|---|---|
| E1 | Power bank | L × W × H; which end the USB-C **input** is on; port centre height; LED position; button position | `Battery.len/w/t`, `port_z_off`, `led_window` | 100 × 66 × 24 | |
| E2 | Power bank | Does it keep its output on at < 50 mA? Does it have 2 outputs? Max USB-A current (label) | (docs) | unknown | |
| E3 | TT motor | Body L × H × T; shaft position from the gearbox end; shaft Ø and across-flats; shaft length each side; mounting-hole positions; lead exit | `Drive.tt_*` | 70 × 22.5 × 18.8; Ø5.4 / 3.7 flats | |
| E4 | FS90 servo | Body L × W × H; tab span, tab height, tab thickness; spline offset from the body centre; spline height; screw-hole spacing; horn length (double arm) | `Neck.servo_*`, `horn_*` | 22.5 × 12.1 × 22.4 | |
| E5 | Robo Pico | Board W × H × T; hole positions; tallest component **with the Pico 2 WH fitted** | `Boards.robo_*` | 88 × 72; 16 mm | |
| E6 | Robo Pico | GP20 and GP21 button centres and button height | `btn_gp20_uv`, `btn_gp21_uv` | (−35, 8), (−21, 8) | |
| E7 | Robo Pico | **Power switch**: position, slide direction, travel, knob size; Maker Port, servo-port and VIN terminal positions; NeoPixel positions; **motor terminal type** (screw/push) | `switch_uv`, `switch_travel`, `led_strip_uv` | (22, 6), 3 mm | |
| E8 | XIAO ESP32S3 Sense | Stack L × W × H; camera module size and lens height; **mic position**; USB-C position; antenna (included? where does it go?) | `xiao_*`, `cam_*` | 21 × 17.8 × 15 | |
| E9 | USB-C plug overmold | W × H × length of the CE09370 plug | `usb_c_overmold`, `CABLE_SLOT_R` | 12.5 × 7 | |
| E10 | Gravity speaker | Board size, speaker can depth, mounting holes, connector position, **cable pin order vs. the Robo Pico servo header** | `spk`, `spk_depth` | 40 × 40 × 12 | |
| E11 | PiicoDev modules | Board size, hole pitch, OLED glass and active area offsets, touch-pad positions, ToF sensor position, LED positions | `piico*`, `oled_*` | 25.4; 20.32 pitch | |
| E12 | ADA3628 / ADA3629 | Size, for mounting | (add to CAD v0.2) | — | |

## B. Electrical checks before first power

- [ ] Bank USB-A → ADA3628: +5 V on the terminal marked VBUS (multimeter)
- [ ] Red wire on Robo Pico VIN +, black on VIN − (checked twice; VIN is treated as unprotected)
- [ ] Servo plug orientation matches the servo-port silkscreen (S / + / −)
- [ ] Gravity cable order (S / + / −) matches servo port 3. **If it doesn't, don't force it. Re-pin with M/M jumpers.**
- [ ] Servo port 4 V+ → ADA3629 +, GND → ADA3629 −, and that pair only (signal pin unconnected)
- [ ] `i2c.scan()` on I2C1 (GP2/GP3) lists every expected address

## C. Print calibration (fit_test_coupon)

| Fit | Variants on the coupon | Choose | Update |
|---|---|---|---|
| TT shaft bore (snug, no wobble, removable) | +0.0 / +0.1 / +0.2 / +0.3 mm | | `drive_wheel` bore offset (`+0.1` default) |
| Column peg Ø6 | socket +0.0…+0.3 | | `Print.clearance` |
| Tray peg Ø5 | socket +0.0…+0.3 | | `Print.clearance` |
| Caster stem Ø8 (must swivel freely) | bore +0.0…+0.3 | | `Print.clearance` |
| PiicoDev M2.5-hole peg posts | Ø2.0 / 2.2 / 2.4 / 2.6 | | base peg radius in `parts.base_plate` |

Variants are numbered by 1–4 notches on the coupon edge (1 notch = +0.0 mm / smallest peg).

## D. Functional calibration (after assembly)

| Item | Method | Record |
|---|---|---|
| Wheel speed vs. PWM (each side) | 2 m timed run at 30/40/50% | trim factor L/R |
| Speed cap | choose the PWM giving ≤ 0.25 m/s | value |
| Servo centre and ±70° | look at the eyes; adjust the trim offset | µs at −70 / 0 / +70 |
| Clutch slip torque | hold the head, command a move; count clicks per variant | chosen `clutch_arm_t` |
| Camera field of view | person at a known angle → measured pixel offset | deg/pixel for L1 |
| ToF distance offset | known distances 0.3 / 0.6 / 1.0 m | offset |
| Tilt thresholds | tilt table | angles |
| Touch thresholds | per membrane thickness | sensitivity setting |
| Speaker volume cap | sound level at 1 m (phone app is fine) | value |
