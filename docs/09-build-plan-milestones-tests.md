# 09 · Build plan, milestones, test plan and evaluation

**Status: design only. Firmware not implemented. Purchases on HOLD** ([00](00-status-assumptions-decisions.md) D1). The deadline is unknown, so milestones are in relative weeks. All result columns are **blank on purpose**: fill them only with real measurements.

## 1. Milestones

| M | Week | Milestone | Exit criteria | Needs |
|---|---|---|---|---|
| M0 | now | **AU$0 bench loops (option R0)**: Pico 2 W MicroPython, Wi-Fi to the laptop, kit modules on the kit expansion board; ToF → OLED/LED and touch → feedback loops logged | Logged setpoint/measurement/output for 2 loops; Wi-Fi round-trip time; client isolation checked | Owned parts only |
| M1 | 0 | Decision D1 (scope vs budget); stock re-checked; parts ordered **only if** compliant with the decision | Written decision; order within the accepted budget | User |
| M2 | 0–1 | Fit coupon printed; parts measured; `params.py` updated; CAD regenerated | [12](12-measurement-calibration-checklist.md) §A/§C filled | M1 |
| M3 | 1–2 | **Power gates** PG1–PG7 on the bench, wheels off the ground ([05](05-power-budget-charging.md) §5) | All gates pass or the design is changed | M1 |
| M4 | 1–3 | Print and assemble the frame, drive base and shells | T-MECH-1..4 | M2 |
| M5 | 2–4 | Supervisor + drive: motion expiry, watchdog, enable, tilt heuristic, speed cap | T-DRV-1..4, T-SAF-1..4 | M3, M4 |
| M6 | 3–5 | Head: neck, clutch, servo; camera streaming to the laptop | T-PAN-1..4, T-CAM-1 | M3 |
| M7 | 4–6 | Bridge v1: tracking, target selection → L1/L2; then L3 with all preconditions | T-CAM-2..5, T-SAF-5..7 | M6 |
| M8 | 5–7 | Voice: turn-based mic → STT → LLM → TTS → head speaker | T-AUD-1..3, T-AI-1..6 | API account (D3) |
| M9 | 6–8 | Integration: UI, activities, offline mode | T-UI, T-OFF | all |
| M10 | 7–9 | Supervised evaluation with consent | §4 | D8 |

## 2. Bring-up order (every subsystem)

Visual check → polarity/continuity with power off → power on with wheels off the ground → smallest test script → log the result → only then add the next subsystem.

## 3. Test plan

Record: date, firmware/CAD version, tester, method, **measured result**, pass/fail, notes.

### Power (gates PG1–PG7 are in [05](05-power-budget-charging.md) §5)
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-PWR-1 | Runtime: full bank → demo loop until shutdown | ≥ 1 h (N4) | |
| T-PWR-2 | Bank low-load behaviour with Pip asleep | Recorded; mitigation chosen | |
| T-PWR-3 | Rail voltages during motor start/reverse, servo slew and audio | Servo ≥ 4.8 V (PG2); no resets | |
| T-PWR-4 | Camera switch off → stream stops, camera LED off | Off | |
| T-PWR-5 | Charging procedure: both robot leads unplugged before charging | Procedure followed; drive impossible with leads unplugged | |

### Drive and safety
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-DRV-1 | Each motor fwd/rev at low duty, wheels up | Correct direction | |
| T-DRV-2 | Straight-line drift over 2 m at the cap | ≤ 10 cm after trim | |
| T-DRV-3 | Speed calibration | Duty set so v ≤ 0.25 m/s | |
| T-DRV-4 | Turn on the spot | No caster flutter | |
| T-SAF-1 | Tilt table | Static tip ≥ 25° all directions; tilt stop triggers | |
| T-SAF-2 | Lift trials (slow and fast), wheels guarded | **Characterise only.** Slow lifts are expected to be missed. Confirms rule "press B before lifting". | |
| T-SAF-3 | Kill the bridge mid-follow, **while camera streams and speech plays** | Stops ≤ 0.6 s after the last heartbeat | |
| T-SAF-4 | Freeze the main loop on purpose (debug flag) | Motor commands expire ≤ 0.2 s; watchdog reset; no motion during reset (PG7) | |
| T-SAF-5 | Wall test: walk away from Pip toward a wall during follow | Stops at ToF ≤ 350 mm; never reverses | |
| T-SAF-6 | Target switch: second person crosses between Pip and the target | Pip stops or stays on the selected id; never drives toward the second person | |
| T-SAF-7 | Target loss: target leaves view | v = 0 within 0.3 s; leaves follow mode after 5 s | |
| T-SAF-8 | Neck finger probe Ø8 mm | No closing gap | |
| T-SAF-9 | Pull test ~50 N on eyes, plungers, head, wheels | Nothing comes off | |

### Head, camera, audio
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-PAN-1 | Sweep ±70°, slew-limited | Smooth; no stop contact | |
| T-PAN-2 | Clutch variants; head-straight check after a forced slip | Slips before the servo stalls; re-centre procedure works | |
| T-PAN-3 | Cable twist, 500 pan cycles | No damage; stream uninterrupted | |
| T-PAN-4 | Force the head to the stops by hand | Clutch slips; servo undamaged | |
| T-CAM-1 | Stream QVGA for 10 min | Record fps (target ≥ 8) | |
| T-CAM-2 | Pixel → bearing map; box size → range curve | Tables recorded | |
| T-CAM-3 | L1 step response (30° step) | Record settling and overshoot | |
| T-CAM-4 | End-to-end latency camera → servo command | Record | |
| T-CAM-5 | ToF vs camera range plausibility with the target aligned | Agreement within ±35% recorded | |
| T-AUD-1 | STT accuracy, 20 phrases at 1 m | Record | |
| T-AUD-2 | Intelligibility, 10 phrases | ≥ 80% understood | |
| T-AUD-3 | Echo: does Pip's own speech trigger VAD? | Must pass before barge-in is enabled | |

### AI, UI, offline
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-AI-1 | Reply latency | Median ≤ 3 s | |
| T-AI-2 | 30 tricky prompts | 0 unsafe replies | |
| T-AI-3 | Personal-info refusal | Never asks for or repeats details | |
| T-AI-4 | Cost per 10-min session | From token logs | |
| T-AI-5 | API failure | Says offline; offline games | |
| T-AI-6 | Key limit reached | HTTP 402 handled | |
| T-UI-1..4 | Button A short/long, Button B, body switch | As [02](02-architecture.md) §3 | |
| T-UI-5 | OLED readability at 0.5/0.8 m | Record | |
| T-UI-6 | Touch through 0.8/1.0/1.2 mm | ≥ 95% presses, no false triggers | |
| T-OFF-1..3 | Offline games | Playable | |

### Mechanical
| ID | Test | Pass criterion | Result |
|---|---|---|---|
| T-MECH-1 | Fit coupon + screw pilot test | Clearances chosen | |
| T-MECH-2 | Wheel on shaft | No slip; removable | |
| T-MECH-3 | Shells off/on from underneath | < 3 min, one screwdriver | |
| T-MECH-4 | 10 cm drop of the bare chassis | No cracks | |
| T-MECH-5 | Lift the assembled robot by the head (motors off) | Deck stays on the columns; head stays on | |

## 4. Evaluation with children (consent; supervised; only after T-SAF passes)

2–3 children, 15 min each, adult present, scripted (greeting → 2 activities → goodbye mission). Record observed numbers only: time moving vs looking at the screen, conversational turns, adult interventions, smiley ratings, safety incidents (must be zero). Ask the adult what was fun, annoying or unsafe. Write up the changes made ([10](10-school-evidence-rubric.md)).
