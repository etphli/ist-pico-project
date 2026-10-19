# 09 · Build plan, milestones, test plan and evaluation

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

The deadline is **unknown** (D2), so milestones are given in **relative weeks** from the day parts are ordered. All result columns are **blank on purpose**. Fill them in with real measurements; never with expected values.

## 1. Milestones

| M | Week | Milestone | Exit criteria | Depends on |
|---|---|---|---|---|
| M0 | 0 | Decisions D1–D8 made; parts ordered; fit coupon printed | Order confirmation; coupon results logged ([12](12-measurement-calibration-checklist.md) §C) | — |
| M1 | 0–1 | **Bench bring-up (kit only)**: Pico 2 W MicroPython, Wi-Fi joins the network, laptop ping, PiicoDev modules on the kit expansion board, `i2c.scan()` | All kit modules respond; Wi-Fi round-trip time logged; client isolation checked | — |
| M2 | 1–2 | **Robo Pico bench**: Pico 2 WH in Robo Pico, motors and servo on the bench (wheels off the ground), power through VIN from the bank | T-PWR-1..3, T-DRV-1, T-PAN-1 | B1–B3, B7, B11–B12, bank |
| M3 | 1–3 | **Print and measure**: measure bought parts, update `params.py`, regenerate CAD, print base plate, wheels, casters, tray, columns, deck | Measured values committed; prints fit (T-MECH-1..4) | M0 |
| M4 | 2–4 | **Drive base**: chassis assembled, closed loops L3, L4, L5 on the Pico, supervisor + movement enable | T-DRV-2..4, T-SAF-1..4 | M2, M3 |
| M5 | 3–5 | **Head**: neck, clutch, servo, head base; XIAO streaming to the laptop | T-PAN-2..4, T-CAM-1 | B4, M3 |
| M6 | 4–6 | **Bridge v1**: person tracking → `track` → L1/L2 | T-CAM-2..4 | M5 |
| M7 | 5–7 | **Voice**: mic → STT → OpenRouter → TTS → speaker; barge-in | T-AUD-1..3, T-AI-1..6 | B5/B6, API account (D3) |
| M8 | 6–8 | **Integration**: shells, rear UI, OLED and touch prompts, activities, offline mode | T-UI-1..6, T-OFF-1..3 | all |
| M9 | 7–9 | **Evaluation**: supervised play sessions (with consent), questionnaire, fixes | §4 | D8 consent |
| M10 | 8–10 | **Documentation** of evidence for school | [10](10-school-evidence-rubric.md) | — |

Buffer: plan for at least 1 extra week, because two parts have lead times and the Robo Pico is out of stock.

## 2. Bring-up order (always the same)

1. Visual check → 2. Power-off continuity and polarity check (multimeter) → 3. Power on with **wheels off the ground** → 4. Run the smallest test script → 5. Log the result in the test table → 6. Only then connect the next subsystem.

## 3. Test plan

Record: date, firmware/CAD version, tester, method, **measured result**, pass/fail, notes.

### Power (T-PWR)
| ID | Test | Method | Pass criterion | Result |
|---|---|---|---|---|
| T-PWR-1 | Runtime | Full bank → demo loop (drive 10 s / idle 50 s, talk) → time to shutdown | ≥ 1 h (N4) | |
| T-PWR-2 | Bank low-load auto-off | Pip asleep; time until the bank switches off | Note the behaviour; pick a mitigation | |
| T-PWR-3 | Brown-out | After power redesign, measure each rail with a scope during bounded starts, stops and audio load. Do not use a Wi-Fi-shared ADC as the only measurement | All rails remain within each connected part's documented limits; no reset | |
| T-PWR-4 | Hard-off kills camera/mic | Switch off → XIAO LED/stream stops; measure 0 V at ADA3629 | 0 V | |
| T-PWR-5 | Charge procedure / interlock | Follow [05](05-power-budget-charging.md) §5; try to drive with the door open | Can't drive while the charge port is exposed (v0.1: procedural only) | |
| T-PWR-6 | Thermal | After protection is designed, measure current and temperature under bounded fault tests with teacher supervision and a current-limited bench supply | Within documented component current and thermal limits; record temperatures | |

### Drive and safety (T-DRV, T-SAF)
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-DRV-1 | Each motor forward/reverse at 30/50/70% PWM, wheels up | Correct direction; current within the rating | |
| T-DRV-2 | Straight-line drift over 2 m at the speed cap | Drift ≤ 10 cm after trim | |
| T-DRV-3 | Speed calibration (PWM → m/s) | Cap set so v ≤ 0.25 m/s | |
| T-DRV-4 | Turn on the spot, both directions | No caster flutter, no stall | |
| T-SAF-1 | Tilt-table: angle at which Pip tips (front/back/side) | ≥ 25° every direction (N2) | |
| T-SAF-2 | Slow and fast lift trials with wheels guarded | Characterise failures. Accelerometer alone does not satisfy reliable lift-stop | |
| T-SAF-3 | Kill the bridge mid-follow | Stops ≤ 0.6 s after the last heartbeat | |
| T-SAF-4 | Bounded blocked-wheel test after hardware protection design | Current stays within motor and driver ratings; record shutdown behaviour. Do not run this test on the unprotected concept | |
| T-SAF-5 | Neck finger probe (Ø8 mm rod) | Can't enter a closing gap | |
| T-SAF-6 | Eye/plunger pull test (~50 N by hand scale) | Nothing comes off | |

### Head, camera, audio (T-PAN, T-CAM, T-AUD)
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-PAN-1 | Servo sweep ±70°, slew-limited | Smooth; no stop contact | |
| T-PAN-2 | Clutch slip torque (3 printed variants) | Slips before the servo stalls; holds the head during normal pans | |
| T-PAN-3 | Cable twist over 500 pan cycles | No cable damage; stream uninterrupted | |
| T-PAN-4 | Hard stop test (force the head to ±75° by hand) | Clutch slips; servo undamaged | |
| T-CAM-1 | Stream QVGA to the bridge | ≥ 8 fps sustained for 10 min (record the actual figure) | |
| T-CAM-2 | Detection range | Detects an adult/child-sized person at 0.5–3 m (record) | |
| T-CAM-3 | L1 step response (person steps 30° sideways) | Settles within ±5° in ≤ 1.5 s (record) | |
| T-CAM-4 | End-to-end tracking latency | Measure (camera → servo command) | |
| T-AUD-1 | Mic level/noise at 1 m | STT word accuracy on 20 test phrases (record) | |
| T-AUD-2 | Speech intelligibility | ≥ 80% of 10 phrases understood by a listener (record) | |
| T-AUD-3 | Barge-in | Pip stops ≤ 300 ms after speech onset (record) | |

### AI, UI, offline (T-AI, T-UI, T-OFF)
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-AI-1 | Reply latency (end of speech → audio start) | Median ≤ 3 s (N5) | |
| T-AI-2 | Safety prompt test set (30 tricky prompts written by an adult) | 0 unsafe replies; log each | |
| T-AI-3 | Personal-info refusal | Never asks for or repeats personal details | |
| T-AI-4 | Cost per 10-min session | Logged from token usage | |
| T-AI-5 | API failure (revoke key / disconnect) | Says "offline" and switches to offline games | |
| T-AI-6 | Key/credit limit enforcement | Requests stop at the limit (HTTP 402 handled) | |
| T-UI-1..4 | Buttons A/B and power actuator, each function | As specified in [02](02-architecture.md) §3 | |
| T-UI-5 | OLED readability at 0.5 / 0.8 m | Icons recognised by a child (record) | |
| T-UI-6 | Touch pads through the membrane, 3 thicknesses | ≥ 95% registered presses, no false triggers (record) | |
| T-OFF-1..3 | Offline games run with the bridge off | Each game playable | |

### Mechanical (T-MECH)
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-MECH-1 | Fit coupon | Clearances chosen and recorded | |
| T-MECH-2 | Wheel on TT shaft | No slip at stall; removable | |
| T-MECH-3 | Shell fit and removal | Rear shell off/on in < 2 min with one tool | |
| T-MECH-4 | Drop of the bare chassis from 10 cm | No cracks | |

## 4. Evaluation with children (only with consent; supervised)

- **Sessions:** 2–3 children, 15 min each, an adult present, with a script (greeting → 2 activities → goodbye mission).
- **Measures (observed, not invented):** time spent moving vs. looking at the screen; number of conversational turns; number of times an adult had to intervene; children's ratings (smiley 3-point scale); any safety incident (must be zero).
- **Questions for the adult:** Would you let your child use Pip again? What felt unsafe or annoying? What was fun?
- Write up what worked, what didn't, and the changes made: the evaluation cycle in [10](10-school-evidence-rubric.md).
