# Engineering review and release status

Reviewed 2026-10-19. Claude Opus 5.5 at medium reasoning produced the initial documentation and parametric CAD. Its second revision stopped at an API rate limit. The parent agent reviewed the artifacts, corrected the budget framing and control claims, and rebuilt the CAD.

**Release: design prototype only. Purchases, final printing and electrical assembly are on hold.** The requested finished design is not yet achieved within the AU$70 total budget. No hardware, firmware, camera stream or AI conversation has been tested.

## What this package provides

- A requirements map, closed-loop architecture, network message proposals, activities and an evidence-based school test plan.
- A rounded body with a belly display, two driven wheels and two caster wheels, a servo-driven head, rear buttons and service access.
- Editable Python CAD, 25 distinct STL files including fit coupons, preview images and a reproducible geometry report. Quantities in the part registry matter; some STLs must be printed more than once.
- A priced comparison concept showing why this particular parts selection exceeds the budget. It is not a verified cheapest build.

## Blocking findings

| Finding | Evidence | Required resolution |
|---|---|---|
| Budget | Concept Core subtotal AU$148.71 with minimum advertised delivery, plus an unverified bank and unpriced fasteners. | Find a complete delivered solder-free BOM at or below AU$70, or obtain explicit agreement to change scope. Buying in stages does not change the total cap. |
| Servo voltage | FS90 listing gives 4.8–6 V; proposed carrier rail is about 4.6 V from a nominal 5 V input. | Select a rated servo or a regulated supply arrangement within every connected part's limits. Testing below the rating does not establish compliance with the rating. |
| Camera power | The original proposal feeds XIAO USB from the reduced carrier rail. USB power is specified as 5 V. | Supply the camera from a documented regulated 5 V source with sufficient headroom and suitable switching. Do not connect the original W10/W11 path. |
| Supply and stall protection | Estimated combined stall load is about 4.2 A, above the proposed bank's 2.4 A minimum. The driver has finite channel limits. | Document hardware current limiting, protection and branch ratings. Do not assume PWM caps, a thermal shutdown or motion estimation protect a stalled motor. |
| Charging interlock | Mechanical door-to-switch blocking is not modelled; the Pico cannot sense bank charging. | Model and test an actual interlock or choose a documented charge-detection topology. A procedure is not an automatic interlock. |
| Fit and retention | Board positions and mounting dimensions are placeholders. Expected-contact collision exclusions allow some overlaps. | Measure actual hardware, check every excluded contact, test retention and cable paths, update CAD and print coupons before full printing. |
| Stock | Proposed Robo Pico is out of stock in the checked Core listing. | Verify stock and Pico 2 WH compatibility before selecting it. |

The nominal power topology to investigate is a protected battery system with separate appropriately rated branches for the motor carrier, regulated servo supply and regulated camera supply, a common ground, and a master disconnect that powers off all branches. This is a design target, not a wiring diagram. Every connector, regulator and protective device must be solder-free and included in the budget before adoption. Never raise carrier VIN above its rating to compensate for a voltage drop.

## Limits of the proposed control system

- The camera supplies bearing. The distance sensor measures a reflecting surface, not person identity. Target selection, freshness, alignment and obstacle thresholds must gate forward motion.
- Servo position is a command estimate. There is no independent head-angle feedback or wheel encoder in this concept.
- An accelerometer detects tilt and some acceleration events. It cannot reliably detect a slow lift or distinguish steady motion from rest. No reliable lift or motor-stall protection is claimed.
- Stop on uncertainty. Do not automatically reverse away from a stall because there is no rear obstacle sensor. There is no validated cliff detector. Use only on an enclosed, clear floor away from stairs.
- Audio playback and networking must not delay motor-command expiry. Test the watchdog while streaming audio and breaking the network connection.
- Continuous conversation and simultaneous camera/audio streaming are software integration goals. They have not been demonstrated. Begin with turn-based listening to avoid speaker feedback; add barge-in only after echo rejection is validated.
- The design has two rear wake/movement buttons plus a separate hard-off switch. Combining hard-off and wake into one button would need extra power-control circuitry. This is a disclosed interpretation of the requested controls.

## CAD checks actually performed

Run `scripts/cad.sh` from the repository root. It checks generated mesh validity, exported mesh watertightness and winding, selected clearances, overlaps above 1 mm³ outside excluded contact pairs, sampled caster/head positions and reference printer-bed dimensions. It estimates stability using guessed component masses.

These checks do not establish continuous collision clearance, camera field of view, cable flexibility, printability, fastener strength, toy compliance or actual component fit. The three-quarter raster preview can show triangle sorting artifacts around apertures; inspect the STL in a slicer before assessing the cutout edges. The red shapes are generic sensor envelopes, not an OLED screen rendering.

## Work possible within the current constraints

Use the owned Pico and kit to demonstrate stationary sensor feedback, such as measuring distance and changing OLED prompts or LEDs. Log setpoint, sensor reading and output. This develops the assignment's closed-loop evidence without spending money. It does not replace the requested complete mobile companion.

The deadline, laptop OS, confirmed owned power bank/cables and API account remain unknown. The hard AU$70 cap and no-soldering requirement remain unchanged.
