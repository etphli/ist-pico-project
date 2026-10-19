# 11 · Mechanical design, print plan and assembly (CAD v0.1 prototype)

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

> **CAD v0.1 is a parametric PROTOTYPE.** Its geometry passes automated checks: valid closed meshes, no unexpected interferences, key clearances ([`cad/out/validation_report.md`](../cad/out/validation_report.md)). It is built from **placeholder dimensions** for every bought part. **Don't print the full set until the measurement checklist ([12](12-measurement-calibration-checklist.md)) is done** and `params.py` has been updated. Print the **fit-test coupon first**.

![Assembly preview](../cad/out/preview_assembly.png)
![Internals x-ray](../cad/out/preview_xray.png)

## 1. Tooling used and reproducibility

- OpenSCAD, FreeCAD and Blender are **not installed** on the design machine, so the model is written in **Python with [manifold3d](https://github.com/elalish/manifold)** (a guaranteed-manifold CSG kernel). It is fully parametric: all dimensions are in [`cad/pip_robot/params.py`](../cad/pip_robot/params.py).
- `scripts/cad.sh` creates a **throwaway** environment with `uv` (nothing installed system-wide). It builds all parts, exports STLs, re-checks every STL with trimesh, runs the interference/clearance/stability checks, and renders the PNG previews.
- **Not done:** slicing (no slicer installed), so there are **no print-time or support-volume numbers**, and no physical test prints yet.

## 2. Overall layout (assembly coordinates: +X forward, +Y left, +Z up, origin on the floor at the centre)

| Item | Position / size (v0.1) |
|---|---|
| Overall | ~300 mm tall; body Ø ~195 mm max; head 120 W × 92 D × 86 H mm |
| Body shell | Revolved "egg/bell" profile, 2.4 mm wall, split **front/rear at X = 0**; bottom edge 14 mm above the floor |
| Base plate | Ø ~184 mm × 4 mm at Z 14–18, with integrated wheel guard wells, motor cradles and caster towers |
| Drive wheels | Ø65 × 18 mm printed, track 128 mm, axle Z = 32.5, **centred fore-aft (X = 0)** |
| TT motors | Lying flat along X, shaft at X = 0, gearmotor body pointing rearward to X ≈ −59 |
| Swivel casters | Front and rear at X = ±66, Ø22 wheels, 8 mm trail, **set 1.5 mm above the drive-wheel plane** |
| Power bank | On the tray at Z 49–73, X −84…+16, charge port facing the rear door |
| Robo Pico | Vertical on the rear upright, component side facing rear, lower edge Z = 78 |
| Rear UI | Buttons at Z ≈ 86 (plungers), switch actuator at Z ≈ 84, charge door at Z ≈ 50–72 |
| Front UI | OLED window Z 122; touch membrane Z 92; speaker grille Z 62; ToF window Z 160; RGB cheek and buzzer holes Z 160 at Y ±30 |
| Neck | Fixed sleeve Ø60 on the top deck (Z 185–213); FS90 hangs on ledges inside; head skirt snaps under the neck flange |
| Head | Floor at Z 214; XIAO + camera cradle behind the left eye (Y +22); mic holes under the left eye |

Static stability estimate (validation report): CG ≈ 97 mm above the floor; tip angles ~33° sideways and ~28–34° fore/aft. **These are estimates with guessed component masses.** Confirm with T-SAF-1.

## 3. Drive train: why 2 driven wheels + 2 swivel casters

The requirement is **four wheels**. The options:

| Layout | Steering | Scrub / losses | Parts and budget | Verdict |
|---|---|---|---|---|
| **A. 2 driven (centre) + 2 swivel casters (front/rear), "diamond"** | Differential, turns on the spot about its own centre. Ideal for "turn to look at the child". | **No scrub**: the casters swivel | 2 motors, 1 two-channel driver | **Chosen** |
| B. 2 driven (rear) + 2 front swivel casters | Differential, but pivots about the rear axle, so the front sweeps sideways when turning | No scrub | Same parts | Worse for tracking: the camera translates when turning |
| C. 4 fixed wheels, 2 motors (skid-steer) | Turning requires the wheels to **skid sideways** | **High scrub**: turning torque and current rise a lot, odometry gets poor, and it marks floors. Worse with short wheelbase-to-track ratios on carpet. | 2 motors | Rejected: stall currents near the 1 A/channel rating |
| D. 4 driven wheels (skid-steer or mecanum) | As C, or holonomic with mecanum | C: scrub; mecanum: needs 4 channels and special wheels | Robo Pico has only 2 motor channels → a second driver, 2 more motors, power wiring | Rejected: budget and solder-free wiring |

**Static indeterminacy:** any four ground contacts on a rigid chassis rock on an uneven floor. Pip's casters sit **1.5 mm higher** (`Caster.lift`) than the drive wheels, so Pip rests on both drive wheels plus whichever caster the CG favours (slightly rear, CG x ≈ −8 mm). It rocks a fraction of a degree onto the other caster when braking. Both drive wheels stay loaded, which is what traction needs. Tune the lift with printed shims under the caster towers if Pip rocks noticeably.

**Speed:** TT 200 RPM at 6 V (spec) on Ø65 wheels ≈ 0.68 m/s. At ≈ 4.6 V it will be lower. The firmware caps the speed at ≤ 0.25 m/s (T-DRV-3).

**Traction:** printed PLA wheels with an **O-ring or thick rubber-band tyre** in a 3 mm groove (groove Ø59 mm). Use a TPU tyre if TPU can be printed.

## 4. Protected neck (head pan)

- The FS90 hangs by its tabs on two ledges **inside a fixed Ø60 neck sleeve** (servo screws come with the servo).
- The head's weight and any push or pull from a child go into the **neck flange and skirt hooks**, **not** into the servo's bearings.
- The servo drives the head through a **slip clutch**: the horn sits in a `clutch_disc` whose four spring tongues click into eight notches in the head floor. If a child twists the head, the clutch slips before the servo's plastic gears strip. Tune `clutch_arm_t` (print 1.2 / 1.6 / 2.0 mm and test T-PAN-2). Trim the double-arm horn to 24 mm (`horn_len`).
- **Hard stops** at ±75°: a pin on the neck top runs in an arc groove in the head floor. They limit cable twist and stop the head over-rotating (firmware limit ±70°).
- **Wire routing:** the only cable to the head is the 50 cm USB-A→C lead. It goes through a 14 × 7.5 mm slot in the deck and up through the neck sleeve beside the servo, then through a matching slot in the head floor. Leave a ~60 mm service loop in the head and ~80 mm in the body (T-PAN-3). The servo lead exits down through the deck.

## 5. Shells, service access and openings

| Feature | Implementation |
|---|---|
| Separate shells | Front and rear shells, each located by two ribs in base-plate notches and held by **one M3 screw** through the shoulder into a deck boss (needs a tool, so it is child-resistant) |
| Service | Remove the rear shell → Pico USB, Robo Pico terminals, bank, cables. Remove the front shell → front modules (unplug the PiicoDev cable at the touch module) |
| Screen | OLED glass pocket behind a 24.5 × 12.5 mm window, 1.2 mm skin around it |
| Touch pads | Pocket leaves a **1.0 mm membrane** over the CAP1203 pads, with three shallow target rings outside (test 0.8–1.2 mm) |
| Speaker | 9 × 9 grid of Ø2.5 holes within a circle, module pocket behind |
| Distance (ToF) | **Open** 12 × 7 mm aperture (no cover: avoids infrared crosstalk) |
| RGB "cheek" | 0.8 mm white diffuser skin |
| Camera | Ø7 aperture in the left eye insert; camera board behind it |
| Mic | 5 × Ø1.6 holes under the left eye (move to match the real mic position) |
| Buttons | Two plungers (different colours) through Ø9.7 holes with guide bosses |
| Power | Switch actuator slot (concept) |
| Charging | USB-C port window + sliding inner door with a grip nub; bank LED window |
| Ventilation | Slots near the rear-left (atmospheric sensor) and rear head vents |
| Rounded edges | Revolved body, hull-rounded head, chamfered tyres. Sand print edges. |

**Not yet modelled (v0.2):** the door/switch mechanical interlock ([05](05-power-budget-charging.md) §6); a seam tongue between the shells; labels and icons; cable clips; touch-pad and mic positions matched to the real modules.

## 6. Parts list and print settings (PLA, 0.4 mm nozzle)

| Part (STL in `cad/out/stl/`) | Qty | Colour | Layer / walls / infill | Orientation and supports |
|---|---|---|---|---|
| fit_test_coupon + fit_test_pegs | 1+1 | any | 0.2 / 3 / 20% | flat; **print first** |
| base_plate | 1 | grey | 0.2 / 4 / 30% | flat; support enforcer under the caster tower roofs only |
| tray | 1 | grey | 0.2 / 3 / 25% | upside down (lip on the bed); support under the plate |
| column_L (used ×2) | 2 | grey | 0.2 / 4 / 40% | lying down |
| rear_upright | 1 | grey | 0.2 / 3 / 25% | flat |
| top_deck (with neck) | 1 | grey | 0.2 / 4 / 30% | deck down; check the ledge bridges |
| front_shell, rear_shell | 1 each | **white** | 0.2 / 3 (2.4 mm wall ≈ 6 perimeters at 0.4) / 15% | seam face down; tree supports |
| head_cap | 1 | white | 0.2 / 3 / 15% | open side down; tree supports for the roof |
| head_base | 1 | grey | 0.2 / 3 / 25% | skirt ring down; supports under the floor overhang and the hooks |
| clutch_disc | 1 (+2 variants) | grey | **0.12** / 3 / 100% | flat |
| eye_left_camera, eye_right | 1 each | **black** | 0.12 / 3 / 100% | plug down, flange up (as exported) |
| drive_wheel_L/R | 1 each | dark | 0.2 / 4 / 40% | flat on the outer face |
| motor_strap | 4 | grey | 0.2 / 3 / 50% | flat, peg up |
| caster_fork_F (used ×2) | 2 | grey | 0.16 / 4 / 60% | arms down, stem up (as exported) |
| caster_wheel_F | 2 | dark | 0.2 / 3 / 40% | flat |
| caster_axle_F | 2 | grey | 0.12 / 4 / 100% | lying on its side (as exported) so the layers run along the pin |
| caster_clip_F | 2 | grey | 0.12 / 100% | flat |
| plunger_wake (white), plunger_move (dark) | 1 each | as named | 0.12 / 100% | cap down, standing; small support under the retaining collar |
| charge_door | 1 | white | 0.2 / 100% | flat |
| switch_actuator | 1 | dark | 0.12 / 100% | standing; **concept, re-model after measuring** |

All parts fit a 220 × 220 × 250 mm bed (largest: shells ≈ 177 × 195 × 97 mm). For a 180 mm bed, split the shells with the slicer's cut tool along Z and pin them.

**Resin:** not used in v0.1. If used later, only for decorative non-load-bearing parts (e.g. glossy eye pupils), fully washed and cured.

## 7. Assembly sequence

1. **Coupon:** print `fit_test_coupon`; choose the clearances; update `Print.clearance`, the bore and peg values; regenerate.
2. **Base:** press the colour sensor and accelerometer onto their peg posts. Put the motors in the cradles (leads to the rear), fit the straps (pegs into the cradle walls, tongues into the guard-wall slots). Fit the wheels onto the shafts through the guard holes, with O-ring tyres on.
3. **Casters:** fork stem up through the tower; fit the clip on top. Wheel into the fork; push the axle pin through until the split tip snaps.
4. **Tray:** legs into the base sockets. Bank on the tray with the charge port at the rear; strap through the slots.
5. **Columns:** pegs into the base sockets through the tray holes.
6. **Rear upright:** legs into the tray sockets. Mount the Robo Pico (with the Pico 2 WH plugged in) on the standoffs. Fit the ADA3629 (USB female terminal) on the upright with a cable tie (cable ties are not in the BOM) or hook-and-loop.
7. **Wiring:** follow [04](04-wiring-pin-plan.md) §5–6. Do the motor leads, VIN, servo port 3 speaker cable and servo port 4 jumpers now. Run the PiicoDev chain to the base modules and the atmospheric sensor.
8. **Deck + neck:** feed the servo lead and the USB-C cable through the deck slots. Seat the deck on the column pegs and the upright tabs. Screw the servo onto the ledges (spline centred).
9. **Head:** trim the horn and press it onto the servo with the servo centred (90°). Put the clutch disc on the horn. Route the USB-C lead through the head floor slot and plug it into the XIAO in its cradle. Press the head base down until the skirt hooks snap under the neck flange; check rotation and the stops. Fit the eyes from inside the cap (flange outside). Fit the cap and screw it from below with 2 × M3.
10. **Front shell:** press the modules into their pockets (OLED, touch, ToF, RGB, buzzer, speaker). Connect the 200 mm PiicoDev lead to the touch module. Lower the shell onto the base notches; roof screw.
11. **Rear shell:** fit the plungers from the inside, the door into its rails and the switch actuator into its slot (engage the switch fork). Lower the shell; roof screw.
12. Run the bring-up checks in [09](09-build-plan-milestones-tests.md) §2 before the first drive.

## 8. Known v0.1 limitations

- Module, button, switch, port and hole positions on bought parts are **placeholders**.
- The interlock is not modelled. The switch actuator is a concept.
- Shells use a plain butt seam. There are no snap fits between the shells yet.
- PiicoDev boards are retained by friction on pegs and in pockets. Add printed clips or a dab of hot glue (a hot-glue gun is not soldering) if loose.
- The stability and mass figures are estimates. Strength has not been analysed (no FEA). Rely on test prints and T-MECH tests.
