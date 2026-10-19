# 01 · Requirements and traceability

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

IDs are referenced in the test plan ([09](09-build-plan-milestones-tests.md)) and the evidence prompts ([10](10-school-evidence-rubric.md)).
Priority: **M** = must (user requirement), **S** = should (safety or quality), **C** = could.

## 1. Purpose

Pip is a small rounded robot that **gets children aged 5–8 to play away from screens**. It asks questions, plays movement and colour games, follows a child around a room, and talks with them. It is also an IST assignment, so it must clearly show **closed-loop control (sensor → output → feedback)**.

## 2. Functional requirements

| ID | Pri | Requirement (from the user brief unless noted) | Design response | Verification |
|---|---|---|---|---|
| F1 | M | Built around the user's **Raspberry Pi Pico 2 WH** | Pico 2 WH is the body controller on a Cytron Robo Pico carrier | Inspection |
| F2 | M | **Four wheels** | 2 driven wheels (TT gearmotors) + 2 printed swivel casters, diamond layout ([11](11-mechanical-design-print-assembly.md) §3) | Inspection, T-DRV tests |
| F3 | M | **Head pans left/right** | FS90 servo in the neck, ±75° hard stops, slip clutch | T-PAN-1..4 |
| F4 | M | **Onboard rechargeable battery with an accessible charge port** | USB power bank in the base; USB-C input reachable through a rear door | T-PWR-1..5 |
| F5 | M | **Camera that tracks subjects** | XIAO ESP32S3 Sense camera in the left eye; person detection on the laptop; head-pan and body-yaw loops | T-CAM-1..4 |
| F6 | M | **Two rear buttons: wake/power and movement enable** | Rear button A = wake/sleep (GP20); rear button B = movement enable (GP21); hard power via the Robo Pico switch through a printed actuator | T-UI-1..4 |
| F7 | M | **Screen in the middle of the body for questions** | Kit OLED 128×64 behind a belly window; three capacitive answer pads (A/B/C) below it | T-UI-5..6 |
| F8 | M | **Web AI**: follow a person, spoken conversation, respond to inputs, all over Wi-Fi | Laptop bridge + OpenRouter LLM; mic and speaker are **on the robot** | T-AI-1..6 |
| F9 | M | **Onboard microphone and speaker.** No tether to the laptop. A laptop mic/speaker is only an optional temporary fallback, and only if the user accepts it. | XIAO Sense digital mic (head); DFRobot Gravity speaker (body) | T-AUD-1..3 |
| F10 | M | **No soldering** | Plug-in or screw-terminal parts only ([04](04-wiring-pin-plan.md)) | Inspection |
| F11 | M | Extra hardware **≤ AU$70 including delivery** (target AU$50) | **Not met** by the full feature set; unresolved sourcing and scope options in [08](08-bom-budget-sourcing.md) | BOM |
| F12 | S | Works in a **reduced, honest non-AI mode** when the laptop, Wi-Fi or API is unavailable | Pico-only behaviours ([02](02-architecture.md) §6) | T-OFF-1..3 |
| F13 | S | Encourages **off-screen** play | The OLED is small and used only for prompts and icons; activities are physical ([07](07-activities-ux.md)); session timer | User test |
| F14 | S | Movement is only possible after a deliberate "enable", and stops on detected excessive tilt, fault or lost link. Reliable lift detection requires additional hardware | Safety supervisor on the Pico ([02](02-architecture.md) §5) | T-SAF-1..6 |
| F15 | S | The camera and microphone are powered off whenever Pip is switched off | Requires a switched, rated 5 V camera supply; unresolved ([05](05-power-budget-charging.md)) | T-PWR-4 |
| F16 | S | Pip cannot drive while charging | Charge-door / power-switch interlock (concept, [05](05-power-budget-charging.md) §6) plus a written procedure | T-PWR-5 |
| F17 | C | Sense the environment for conversation ("it's warm today") | Kit atmospheric sensor | — |
| F18 | C | Colour-card floor games | Kit colour sensor facing down | T-GAME-2 |

## 3. Non-functional requirements

| ID | Pri | Requirement | Target (provisional; to be measured) |
|---|---|---|---|
| N1 | S | Size and look: friendly, rounded, white, upright, dark eyes. **Original design.** The reference image's product and branding are not copied. | ~300 mm tall, Ø190 mm base |
| N2 | S | Stability | Static tip angle ≥ 25° in every direction (CAD estimate ~28–34°, [11](11-mechanical-design-print-assembly.md)) |
| N3 | S | Speed limit near children | ≤ 0.25 m/s in normal play (PWM cap); hard limit set in firmware |
| N4 | S | Runtime | ≥ 1 h of play per charge (estimate in [05](05-power-budget-charging.md); must be measured) |
| N5 | S | Reply latency (child stops talking → Pip starts answering) | Target ≤ 3 s; measure |
| N6 | S | Tracking update rate | Target ≥ 5 Hz bearing updates; measure |
| N7 | S | Serviceability | Rear shell comes off with 1 screw; every module plugs in; the Pico's USB port is reachable for programming |
| N8 | S | Privacy | No image or audio leaves the laptop by default; nothing is recorded by default; visible camera-active indicator |
| N9 | S | Cost transparency | API spend tracked separately from hardware; per-key credit limit |
| N10 | S | Materials | PLA for all v0.1 parts; no structural resin; no small loose parts the child can reach |

## 4. Closed-loop requirements (assignment focus)

At least three loops must be demonstrated with **logged** evidence (setpoint, measurement, output over time). See [02](02-architecture.md) §4 for the full list.

| Loop | Sensor | Output | Feedback measured |
|---|---|---|---|
| L1 head tracking | camera bearing of the person | servo angle | bearing error shrinking toward 0 |
| L2 follow distance | ToF distance | wheel speed | distance error shrinking toward the setpoint |
| L3 safety | accelerometer tilt/lift | motors stop | tilt event → stop latency |
| L4 conversation turn-taking | mic voice activity | speech output starts or stops | barge-in stop latency |
| L5 quiz | touch pad answer | speech, LED, buzzer feedback; next question difficulty | correct-answer rate |

## 5. Out of scope for v0.1

- Running a chatbot or person-detection model **on the Pico itself** (not feasible: [03](03-ai-camera-audio-feasibility.md) §1)
- Certification as a toy
- Outdoor use, stairs, carpets with deep pile
- Unsupervised use
