# 01 · Requirements and traceability

IDs are used in the test plan ([09](09-build-plan-milestones-tests.md)) and evidence prompts ([10](10-school-evidence-rubric.md)). Priority: **M** = must (user requirement), **S** = should (safety/quality), **C** = could. The design responses below are for the **full concept** ([08](08-bom-budget-sourcing.md) §3), which is over budget and on HOLD.

## 1. Purpose

Pip is a small, rounded robot that gets children aged 5–8 playing away from screens. It asks questions, plays movement and colour games, follows a selected child and talks with them. It is also an IST assignment, so it must show **closed-loop control (sensor → output → feedback)** with logged evidence.

## 2. Functional requirements

| ID | Pri | Requirement | Design response (full concept) | Status | Verification |
|---|---|---|---|---|---|
| F1 | M | Built around the user's Pico 2 WH | Pico 2 WH in a Kitronik 5331 motor board | designed | Inspection |
| F2 | M | Four wheels | 2 driven TT wheels + 2 printed swivel casters | designed | T-DRV |
| F3 | M | Head that pans | FS90 in a protected neck, slip clutch, ±75° stops | designed; servo supply gate PG2 | T-PAN |
| F4 | M | Onboard rechargeable battery, accessible charge port | USB power bank in the base; charge input behind the rear door | designed; bank not selected (PG1) | T-PWR |
| F5 | M | Camera tracks a person | DFR1154 camera behind the left eye; tracking on the laptop; L1–L3 | designed | T-CAM |
| F6 | M | Two rear buttons: wake and movement enable | Two PiicoDev Buttons behind printed rear plungers (A white = wake/sleep, B dark = movement enable). The body power switch is separate. | designed | T-UI-1..4 |
| F7 | M | Screen in the middle of the body for questions | Kit OLED 128×64 behind a belly window; 3 touch pads below | designed | T-UI-5..6 |
| F8 | M | Web AI over Wi-Fi: follow a person, spoken conversation, react to sensors | Laptop bridge + OpenRouter; sensor events in prompts | designed | T-AI |
| F9 | M | Microphone and speaker on the robot | DFR1154 mic and amplifier + 1 W speaker in the head | designed; speaker out of stock | T-AUD |
| F10 | M | No soldering | Plug, socket, screw terminal and lever connections only ([04](04-wiring-pin-plan.md)) | designed | Inspection |
| F11 | M | Extra hardware ≤ AU$70 total incl. delivery | **Not met.** Priced hardware AU$121.78 before delivery and unpriced items. No compliant full configuration found. | **not met → HOLD** | [08](08-bom-budget-sourcing.md) |
| F12 | S | Honest non-AI mode when offline | Pico-only games; says it is offline | designed | T-OFF |
| F13 | S | Encourages off-screen play | Tiny prompt-only OLED; physical activities; session timer | designed | User test |
| F14 | S | Motion only after a deliberate enable; stops on detected faults | Supervisor ([02](02-architecture.md) §5). **Not provided:** stall detection, reliable lift detection, edge detection. | designed with stated limits | T-SAF |
| F15 | S | Camera and mic can be hard-powered off | In-line USB-C switch on the camera branch; unplugging is the master disconnect | designed; single master switch open (PG5) | T-PWR-4 |
| F16 | S | Cannot drive while charging | Procedure: robot leads unplugged to charge. **Not an automatic interlock.** | procedural only | T-PWR-5 |
| F17 | C | Talk about the environment | Atmospheric sensor values in prompts | designed | — |
| F18 | C | Colour-card games | Downward colour sensor | designed | T-GAME |

## 3. Non-functional requirements

| ID | Requirement | Target (to be measured) |
|---|---|---|
| N1 | Friendly, rounded, white, upright, dark eyes; original design | ~300 mm tall, Ø195 mm body |
| N2 | Stability | Static tip angle ≥ 25° all directions (CAD estimate 26–33° with guessed masses) |
| N3 | Speed near children | ≤ 0.25 m/s |
| N4 | Runtime | ≥ 1 h play; unknown until a bank is chosen |
| N5 | Reply latency | ≤ 3 s target |
| N6 | Tracking update rate | ≥ 5 Hz target |
| N7 | Serviceability | Shells off with a screwdriver from underneath; modules plug in; Pico USB reachable with the rear shell off |
| N8 | Privacy | No images/audio to the cloud by default; nothing recorded by default; camera-on LED; camera switch |
| N9 | Cost transparency | API spend logged; per-key limit |
| N10 | Materials and retention | PLA; no structural resin; every child-reachable part retained ([11](11-mechanical-design-print-assembly.md) §6) |

## 4. Closed loops for the assignment

At least three loops must be demonstrated with logged setpoint, measurement and output: L1 head tracking, L3 follow distance (with its preconditions), L4 tilt stop, L6 quiz adaptation. Details are in [02](02-architecture.md) §4. In the AU$0 option R0, stationary kit loops such as ToF distance → OLED/LED and touch → feedback can be demonstrated now.

## 5. Out of scope

Running AI on the Pico; toy certification; outdoor use, stairs, deep carpet; unsupervised use; automatic reversing; edge detection.
