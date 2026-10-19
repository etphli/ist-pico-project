# 06 · Safety plan: supervised prototype, NOT a certified toy

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

Pip is a **school prototype**. It has **not** been designed, tested or certified to any toy safety standard (for example the AS/NZS ISO 8124 toy-safety series). Use it **only under adult supervision**, for short sessions, with the rules below. This is a hazard analysis for a prototype, not a compliance claim.

## 1. Supervision rules (print these and keep them with Pip)

1. An adult is present and watching for the whole session. The adult switches Pip on and off.
2. Use on a clear, flat indoor floor. Keep Pip away from stairs, table edges, water and pets.
3. Movement is enabled only by the adult (or by the child with the adult's OK), and only for the game in progress.
4. Don't let children pick Pip up while it is moving. An accelerometer cannot reliably detect a slow lift. Disable movement before handling.
5. No sitting on, standing on or throwing Pip.
6. Only the adult charges the bank, with Pip switched OFF, on a hard surface, and supervised ([05](05-power-budget-charging.md) §5).
7. Stop and switch off if Pip smells hot, makes grinding noises, has cracked parts or loose wires, or the bank is warm or swollen.
8. Before each session, the adult checks: shells closed and screwed; eyes, plungers and caster clips present; no sharp print edges.

## 2. Hazard register

| # | Hazard | Who / when | Design controls | Residual risk / actions |
|---|---|---|---|---|
| H1 | **Small parts / choking** (eye inserts, plunger caps, caster clips and axles, servo horn screws) | Child pulls parts off | Eyes press-fit **from the inside** with a flange outside; plungers retained by an inner collar; caster clips under the body; the servo and its screws are inside the head; shell held by a screw (tool needed) | Ages 5–8 are older than the typical under-3 small-parts rule, but **check before every session** that nothing is loose. Pull-test the eyes (T-SAF-6). |
| H2 | **Pinch: wheels** | Fingers near tyres | Wheels sit inboard of the skirt with printed guard wells; 14 mm ground gap; speed cap ≤ 0.25 m/s; low-torque TT gearmotors | The tyre contact patch is still reachable from below. Lift detection is not reliable; movement must be disabled before handling. |
| H3 | **Pinch: neck / head** | Fingers between the head and the body | Shell opening hugs the neck (≈1.5 mm radial gap); the rotating skirt has no closing gap (motion is tangential); slow servo slew; clutch slips; hard stops at ±75° | Test with a finger probe (T-SAF-5) |
| H4 | **Tip-over / falling robot** | Pip ~1 kg (estimate), ~300 mm tall | Battery low in the base; static tip angle estimated 28–34° (CAD); speed and acceleration limits | Tilt-table test (T-SAF-1); tilt-stop loop L4 |
| H5 | **Battery fire / thermal** | Charging, damage | Suitable protected consumer power bank, certification not verified inside a rigid tray; no bare LiPo pouch in Option A; charging only while switched off and supervised | Inspect the bank; replace if damaged. Option B (bare LiPo) is blocked until its charging is documented. |
| H6 | **Electrical** | Service | 5 V only; no mains inside; an adult does all wiring with power off | Low |
| H7 | **Motor or driver overheating** | Stall | Unresolved: select documented current-limiting hardware matched to the motors. PWM and acceleration sensing do not enforce a current limit. | Temperature check after a 10-minute stall-prone game (T-PWR-6) |
| H8 | **Entanglement / cords** | Charging cable, USB cables | No external cords during play; charging only while off | Low |
| H9 | **Sharp edges / print defects** | Handling | Rounded design; deburr and sand edges; PLA only | Inspection |
| H10 | **Resin parts** | Uncured resin is a skin sensitiser; brittle failures | **No resin parts** in v0.1. If resin is used later: decorative only, fully washed and post-cured, never structural or load-bearing. | — |
| H11 | **Noise / hearing** | Speaker near ears | 0.5 W module; firmware volume cap | Low |
| H12 | **Privacy** (camera + mic of children) | Every session | Local vision; text-only to the cloud; nothing recorded by default; camera-on indicator; hard-off switch also kills the camera power | Consent from parents and the teacher (D8) |
| H13 | **AI content** (inappropriate, wrong or manipulative replies) | Conversation | Child-safe system prompt, laptop-side output filter, short replies, an adult can mute or end the session from the bridge, adult-owned key with a credit limit | Content review in the evidence log; any unsafe reply → stop and fix the prompt/filter |
| H14 | **Over-attachment / screen substitution** | Long use | Session timer (default 15–20 min) ends with "let's go play"; the OLED is tiny and prompt-only; activities push physical play | Observe in user tests |
| H15 | **Lost link → uncontrolled motion** | Wi-Fi drop | Pico supervisor watchdog (500 ms), motion only via local loops | T-SAF-3 |

## 3. Safety-critical firmware requirements (summary)

- Supervisor owns motor PWM. Defaults on boot: motors off, movement disabled, servo detached.
- Stop triggers: excessive tilt or detected acceleration anomaly, lost heartbeat (bridge-driven motion), low VSYS, accelerometer bus error, button B.
- Limits: PWM ≤ 50% (calibrate to ≤ 0.25 m/s), ramp limits, servo ±70° and slew-limited.
- A visible state indication at all times: OLED icon + NeoPixel colour (green = still, amber = moving enabled, red = fault, blue/white = camera streaming).

## 4. Before a session with children

- [ ] Teacher and parent consent for camera/mic use (D8)
- [ ] All T-SAF tests passed on this build ([09](09-build-plan-milestones-tests.md))
- [ ] API key limit set; bridge filter on; kill switch tested
- [ ] Play area cleared; adult briefed on these rules
