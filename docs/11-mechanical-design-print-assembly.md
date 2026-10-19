# 11 · Mechanical design, print plan and assembly (CAD v0.2 prototype)

> **CAD v0.2 is a parametric prototype, not a final design.** Every bought-part dimension, hole position, button, switch and lens position is a **placeholder** (`# MEASURE` in [`params.py`](../cad/pip_robot/params.py)). Do not print the full set until the parts are bought, measured ([12](12-measurement-calibration-checklist.md)) and the model is regenerated. Print the fit-test coupon first.

![Reference elevations](../cad/out/preview_front_reference.png)
![Assembly](../cad/out/preview_assembly.png)
![Internals](../cad/out/preview_xray.png)
![Sections](../cad/out/preview_sections.png)

## 1. Tooling and reproducibility

- Python + [manifold3d](https://github.com/elalish/manifold) (guaranteed-manifold CSG). All dimensions are in `cad/pip_robot/params.py`.
- `scripts/cad.sh` runs everything in a throwaway `uv` environment: build parts, export STLs, re-check the STLs with trimesh, run the geometry checks, render previews. Rendering takes about 3 minutes; `--no-render` skips it.
- **Previews** are drawn by a small per-pixel z-buffer rasteriser (`cad/render.py`) from the exact exported meshes. v0.1 used matplotlib's 3D polygons, which sort whole triangles and drew hidden faces over openings. That produced the "red triangles" on the belly. **That was a renderer artifact; the mesh was correct.** The new previews show openings truthfully. In the front-shell elevation, through-openings show the dark backdrop and thin skins show as plastic. The cross-sections are true slices of the solids.
- No slicer was run, so there are no print-time or support numbers. Nothing has been printed.

## 2. Layout (assembly coordinates: +X forward, +Y robot's left, +Z up, origin on the floor at the centre)

| Item | v0.2 placement |
|---|---|
| Overall | ~300 mm tall; body Ø ~195 mm; head 120 W × 92 D × 86 H |
| Body shell | Revolved egg/bell profile, 2.4 mm wall, split front/rear at X = 0, bottom edge 14 mm above the floor |
| Frame | Base plate (Ø ~184) + 2 front columns + rear upright + top deck with the neck. **Base, columns and deck are screwed together** (4 × M3). |
| Drive | Ø65 printed wheels on TT motors, track 128 mm, axle centred fore-aft; casters front and rear, 1.5 mm above the drive plane |
| Battery | Power bank on the tray, charge port facing the rear door |
| Controller | Kitronik board + Pico on the rear face of the upright, z 110–145, Pico side facing rear (USB reachable with the rear shell off) |
| Rear buttons | Two PiicoDev Buttons on the upright at z 92: A (wake, white plunger) at y −40, B (movement enable, dark plunger) at y −12 |
| Body power switch | Printed push-rod from the rear shell to the controller's slide switch (switch position placeholder) |
| Front (belly) | OLED window z 122 (centre of the body), touch membrane z 92, ToF window z 160, RGB cheek and buzzer holes z 160 |
| Neck | Fixed Ø60 sleeve on the deck; FS90 hangs inside; head skirt hooks under the neck flange; slip clutch; ±75° stops |
| Head | Camera board behind the left eye (lens on the eye axis); 1 W speaker behind a grille under the right eye; eye frame on the head base backs both eyes |

CAD static-stability **estimate** (guessed masses): CG ≈ 102 mm above the floor; tip angles ~32° sideways, ~33°/26° forward/back. Confirm with the tilt-table test T-SAF-1.

## 3. Drive layout

Two driven centre wheels and two swivel casters in a diamond layout. Pip turns on the spot about its own centre (good for "look at the child"). The swivel casters avoid the scrub of skid-steer. The casters sit 1.5 mm high, so Pip rests on both drive wheels plus one caster and keeps traction on both drive wheels. Speed is capped at ≤ 0.25 m/s by calibrated PWM (T-DRV-3). Tyres are O-rings or thick rubber bands in a 3 mm groove.

## 4. Head and neck

- The FS90 hangs on ledges inside the fixed neck sleeve. The head's weight and any pull go into the neck flange, not the servo bearings.
- **Slip clutch:** four spring tongues in the clutch disc click into eight notches in the head floor. They slip before the servo gears are forced. Tune `clutch_arm_t` (print 1.2 / 1.6 / 2.0 mm; T-PAN-2). After a slip, the commanded angle no longer equals the actual angle ([02](02-architecture.md) §4.1).
- **Stops** at ±75° (pin in an arc groove). Firmware limit ±70°.
- **Camera:** the DFR1154 board slides into a cradle on the head base. Its lens front sits 0.5 mm behind the eye frame. The left eye and the frame have a conical aperture for a **90° design FOV**, and the CAD checks that this cone is unobstructed (report §3c). The lens itself is 160° (DFRobot), so the outer field is deliberately masked by the eye. **The lens position on the board is a placeholder.**
- **Speaker:** 30 × 20 × 5 mm speaker in side rails behind the eye frame, grille holes through the frame and cap under the right eye.
- **Cable:** one USB-C lead (camera power) through a slot in the deck, up the neck and through the head floor slot, with service loops (T-PAN-3).

## 5. Shells, openings, service

| Feature | v0.2 |
|---|---|
| Screen | OLED viewing window 24.5 × 12.5 mm through the shell; glass pocket and board pocket behind |
| Touch pads | 1.0 mm membrane over the touch module (blind pocket) with three shallow target rings; test 0.8/1.0/1.2 mm |
| ToF | Open 12 × 7 mm window (no cover, to avoid infrared crosstalk) |
| RGB cheek | 0.8 mm white diffuser skin |
| Buzzer | 7 holes |
| Rear | Two plunger bosses; switch actuator slot; sliding charge-port door with grip; bank LED window; vents |
| Head | Eye sockets; speaker grille; mic holes (placeholder); rear vents |
| Service | Adult turns Pip over and removes the 4 shell screws from underneath, then lifts the shells off. The rear shell exposes the Pico USB, the controller terminals and the bank. |

## 6. Retention and fasteners (every child-reachable or service part)

All screws are **pan-head thread-forming screws for plastics**. They need a screwdriver and are recessed or underneath, so a child cannot open Pip by hand. Pilot holes are 2.5 mm for M3 (tune with the coupon). Screw lengths are chosen so tips stay inside bosses. **Screws are not in the priced BOM** (B16).

| Part | Retained by | Fastener | Tool to remove | Notes / test |
|---|---|---|---|---|
| Front and rear shells | Two ribs in base notches each + **2 screws each from under the base** into rim bosses | 4 × M3 × 10 (counterbored in the base) | Screwdriver, robot turned over | v0.1 roof screws sat under the head and were unreachable; moved |
| Top deck ↔ columns ↔ base plate | Pegs in sockets + **screws at both ends of each column** | 4 × M3 × 12 | Screwdriver (deck screws are under the head: remove the head first) | Lifting Pip by the head cannot pull the deck off |
| Head cap ↔ head base | Cap sits on the base floor; 2 screws up through the floor into cap bosses | 2 × M3 × 10 | Screwdriver; head off first | — |
| Head ↔ neck | 4 snap hooks under the neck flange, hidden inside the body shoulder | — | Adult, shells off | Pull test T-SAF-6 (≥ 50 N by hand scale) |
| Eyes | Inserted **from inside** the cap; inner flange larger than the socket; backed by the head-base eye frame (0.3 mm gap) | — | Head apart | Cannot be pulled out or pushed in once assembled |
| Plungers | Inner collar larger than the shell hole; tip 0.3 mm above the button | — | Shell off | — |
| Switch actuator | Outer grip larger than the slot; inner fork around the switch knob | — | Shell off | Concept; re-model after measuring the switch |
| Charge door | Rails inside the rear shell; grip nub in a slot limits travel | — | Shell off | — |
| Wheels | Press fit on the TT shaft; outer guard wall limits axial travel to ~4 mm, with ≥ 5 mm of shaft still engaged | Optional screw into the shaft end if the motor has a hole (MEASURE; unpriced) | Base access | T-MECH-2 |
| Casters | Stem clip on top of the tower; axle pin with a split snap tip | — | Base access | Small parts under the base: pre-session check |
| Controller board | 4 screws into upright standoffs | 4 × M3 × 8 | Shell off | Kitronik holes are M3 clearance (datasheet) |
| PiicoDev Buttons | 2 screws each into standoffs | 4 × M2.5 × 6 | Shell off | Hole positions placeholder |
| Camera board, speaker | Slots/rails in the head base, enclosed by the cap | — | Head apart | No screws; add a clip if loose |
| Power bank | Tray lip + hook-and-loop strap through tray slots | strap (unpriced) | Shell off | — |
| Motors | Cradle + 4 printed straps held down by the tray | — | Shell + tray off | — |
| Front PiicoDev modules | Pockets/pegs | optional M2.5 | Shell off | Hot glue allowed if loose (not soldering) |

**Fastener total:** 14 × M3 (4 shell, 4 frame, 2 head, 4 controller) and 4 × M2.5. All unpriced.

## 7. Parts list and print settings (PLA, 0.4 mm nozzle)

| Part (STL in `cad/out/stl/`) | Qty | Colour | Layer / walls / infill | Orientation |
|---|---|---|---|---|
| fit_test_coupon + fit_test_pegs | 1+1 | any | 0.2 / 3 / 20% | flat; **print first** |
| base_plate | 1 | grey | 0.2 / 4 / 30% | flat; support only under the caster-tower roofs |
| tray | 1 | grey | 0.2 / 3 / 25% | upside down |
| column_L (used twice) | 2 | grey | 0.2 / 4 / 40% | lying down |
| rear_upright | 1 | grey | 0.2 / 3 / 25% | flat |
| top_deck | 1 | grey | 0.2 / 4 / 30% | deck down |
| front_shell, rear_shell | 1 each | white | 0.2 / 3 / 15% | seam face down; tree supports |
| head_cap | 1 | white | 0.2 / 3 / 15% | open side down |
| head_base | 1 | grey | 0.2 / 3 / 25% | skirt down; supports under the floor overhang, hooks and cradle |
| clutch_disc | 1 (+2 variants) | grey | 0.12 / 3 / 100% | flat |
| eye_left_camera, eye_right | 1 each | black | 0.12 / 3 / 100% | as exported |
| drive_wheel_L / R | 1 each | dark | 0.2 / 4 / 40% | outer face down |
| motor_strap | 4 | grey | 0.2 / 3 / 50% | as exported |
| caster_fork_F / wheel_F / axle_F / clip_F | 2 each | grey/dark | see v0.1 notes | as exported |
| plunger_wake (white), plunger_move (dark) | 1 each | as named | 0.12 / 100% | as exported |
| charge_door, switch_actuator | 1 each | white / dark | 0.12–0.2 / 100% | as exported |

Bed fit (bounding box, from the report): every part fits a 220 × 220 × 250 mm bed. The base plate and both shells do **not** fit a 180 mm bed; split them in the slicer and pin the halves.

## 8. Assembly sequence

1. Coupon → choose clearances → update `params.py` → regenerate.
2. Base: base modules on pegs; motors in cradles with straps; wheels with tyres; casters with clips and axles.
3. Columns into the base, **screwed from below**. Tray and bank with strap. Rear upright into the tray.
4. Controller (with Pico) and both PiicoDev Buttons screwed to the upright. Wiring per [04](04-wiring-pin-plan.md) (only after the gates in [05](05-power-budget-charging.md)).
5. Deck onto the columns and upright, **screwed from above**. Servo onto its ledges. Camera USB lead through the deck slot.
6. Head: eyes into the cap from inside. Camera board and speaker into the head-base cradles. Horn + clutch on the servo (servo centred). Cap onto the base (2 screws from below). Lower the head onto the neck until the hooks snap. Check rotation and stops.
7. Front shell: modules into pockets; connect the touch cable; seat the ribs; screws from below. Rear shell: plungers, door and actuator; seat; screws from below.
8. Bring-up checks in [09](09-build-plan-milestones-tests.md) §2.

## 9. What the CAD checks establish (and what they do not)

Established, on placeholder geometry: closed, valid meshes (manifold3d and trimesh). Bed fit by bounding box. No overlap above 1 mm³ between parts outside a listed set of intended contacts; each intended contact is printed with its overlap volume and reason. Selected gaps, e.g. plunger-to-button 0.30 mm and eye-flange-to-frame 0.30 mm. Caster swivel sampled every 5° and head pan sampled every 5° from −75° to +75°. The 90° camera cone is unobstructed.

**Not established:** real fit of bought parts; that the intended-contact overlaps are correct press/peg fits; continuous motion clearance between samples; cable routing and twist; screw engagement and strength; printability; strength (no FEA); toy compliance; real camera view.

## 10. Known v0.2 limitations

- All bought-part positions are placeholders: controller switch, Buttons, camera lens, mic, USB-C sockets, bank ports.
- Holder for the in-line camera switch is not modelled. Charge-door/switch interlock is not modelled.
- Plain butt seam between the shells (no tongue). The shell top is located by the deck edge only.
- Mass and stability are estimates. Strength is unanalysed.
