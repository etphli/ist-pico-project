# 06 · Safety plan: supervised prototype, not a certified toy

Pip is a school prototype. It has **not** been designed, tested or certified to any toy safety standard. Use it **only under adult supervision, on the floor, in a cleared indoor area**. This is a hazard analysis for a prototype, not a compliance claim.

## 1. Supervision rules (keep with Pip)

1. An adult is present and watching for the whole session. The adult switches Pip on and off and holds movement-enable (Button B).
2. **Floor only:** a clear, level, enclosed floor. **No stairs, steps, table tops, ramps or drops nearby.** Pip has no edge (cliff) sensing and cannot reverse safely.
3. Movement is enabled only for the game in progress and times out after 5 minutes.
4. **Press B (movement off) before anyone touches or lifts Pip.** Pip cannot reliably detect a slow lift.
5. No sitting on, standing on or throwing Pip. Keep fingers away from the wheels while movement is enabled.
6. Only the adult charges the bank: body off, both robot leads unplugged from the bank, on a hard surface, following the bank maker's instructions ([05](05-power-budget-charging.md) §6).
7. Stop and switch off if Pip smells hot, grinds, keeps pushing against something, has cracked parts or loose wires, or the bank is warm or swollen.
8. Pre-session check: shells screwed on; eyes, plungers, caster clips and wheels present; no sharp edges; camera switch in the intended position.

## 2. Hazard register

| # | Hazard | Design controls | Limits and actions |
|---|---|---|---|
| H1 | Small parts / choking | Eyes inserted from **inside** the head and backed by the eye frame. Plungers held by inner collars. Shells, head cap and frame screwed (tool needed). Caster clips under the base. Full retention list in [11](11-mechanical-design-print-assembly.md) §6. | Ages 5–8, but check before every session. Pull test T-SAF-9. |
| H2 | Wheel pinch | Wheels inside guard wells; 14 mm ground gap; speed cap ≤ 0.25 m/s | Contact patch reachable from below. Rule 4/5. |
| H3 | Neck pinch | ~1.5 mm radial gap at the shell opening; tangential skirt motion; slow slew; slip clutch | Finger-probe test T-SAF-8 |
| H4 | Tip-over | Bank low in the base; CAD stability estimate in the generated report (bank mass and other masses unmeasured); speed/acceleration limits | Tilt-table T-SAF-1; L4 tilt heuristic |
| H5 | Battery fire/thermal | Finished consumer power bank in a tray; no loose cells; supervised charging with the robot leads unplugged | Inspect; replace a damaged bank |
| H6 | **Motor stall / overheating** | DRV8833 over-current and thermal protection (Kitronik statement); speed cap; motion commands expire in 0.2 s; movement-enable time-out; stop when ToF ≤ 350 mm | **No stall detection is claimed.** Pushing against a wall at constant speed is not detected. A sustained stall heats the motors until the driver or the bank cuts out. Supervision and gate PG3 ([05](05-power-budget-charging.md)). |
| H7 | Servo overload | Slip clutch; ±70° firmware limit vs ±75° stops | No hardware current limit on the servo branch (open item) |
| H8 | Uncontrolled motion after a software hang or lost link | Local motor-command expiry (0.2 s), RP2350 hardware watchdog, 500 ms bridge heartbeat for bridge-driven motion; movement disabled after every reset | T-SAF-3 under network loss **and** audio/camera load; PG7 reset test |
| H9 | Driving into a person or object | Forward motion only with an aligned, fresh, selected target and a valid ToF range; stop at ToF ≤ 350 mm; no reversing | The ToF beam is narrow. Objects beside it are not seen. Supervision. |
| H10 | Driving off an edge | None in hardware | **Rule 2.** No guarantee. |
| H11 | Sharp edges / print defects | Rounded design; deburr; PLA | Inspection |
| H12 | Resin | Not used for v0.3 parts; decorative only if ever used, fully cured | — |
| H13 | Noise | Small 1 W speaker; firmware volume cap | Low |
| H14 | Privacy | Local vision; text-only to the cloud; no recordings by default; camera-on LED; physical camera/mic switch | Consent (D8) |
| H15 | AI content | Child-safe prompt, laptop output filter, short replies, adult end-session control, key with credit limit | Review logs; fix on any unsafe reply |
| H16 | Over-attachment / screen time | Session timer ends with a physical "mission"; tiny prompt-only OLED | Observe |
| H17 | Electrical | 5 V only, no mains; the adult wires with everything unplugged | Polarity checks ([04](04-wiring-pin-plan.md) §5) |

## 3. Before a session with children

- [ ] Purchase/wiring gates PG1–PG7 passed and recorded ([05](05-power-budget-charging.md))
- [ ] T-SAF tests passed on this build ([09](09-build-plan-milestones-tests.md))
- [ ] Teacher and parent consent for camera/mic (D8)
- [ ] API key limit set; filter on; end-session control tested
- [ ] Floor area cleared and enclosed; adult briefed on §1

## 4. QW01-specific limits

The user reports 2 A per USB-A output; simultaneous combined capacity is not known. The estimated body fault current exceeds one port's rating. A second socket does not raise that branch's limit. Keep electrical assembly on HOLD until the branch load and motor protection are redesigned or verified against documented limits. Do not open, alter, drill or clamp hard onto the power bank. Secure it with the cradle and two straps, leaving the intended removal and unplugging access clear. Micro-USB charging is performed with both robot output leads removed.
