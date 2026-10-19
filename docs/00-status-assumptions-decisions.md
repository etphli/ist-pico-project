# 00 · Status, assumptions and open decisions

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

**Project:** Pip, a companion robot for children aged 5–8 that encourages off-screen play (IST semester project, closed loop: sensor → output → feedback).
**Design round:** provisional design v0.1, written 2026-10-19. Nothing has been bought, printed, wired or tested yet.
**Status: reviewable concept only. Purchase status HOLD.** No verified complete build within AU$70 has been found. Rated power distribution, motor protection, stock and hardware fit remain unresolved. See [review findings](13-design-review.md). **The printable models are not final.** The CAD is a parametric v0.1 prototype. Every bought-part dimension in it is a placeholder until it is measured (see [12](12-measurement-calibration-checklist.md)).

## 1. What the user has confirmed

| Topic | Confirmed answer | Where it is used |
|---|---|---|
| Microcontroller | User owns **one Raspberry Pi Pico 2 WH** | [04](04-wiring-pin-plan.md) |
| Kit | User owns the Core Electronics **PiicoDev Starter Kit for Raspberry Pi Pico**. The user says the link is exactly their kit, so we assume the **current v1.2** contents. Don't ask again. | [08](08-bom-budget-sourcing.md) |
| Users | Children **aged 5–8**, **indoors** | [06](06-safety.md), [07](07-activities-ux.md) |
| AI meaning | A **web AI model**. Pip must **follow a person**, hold a **spoken conversation** and **respond to inputs**, all over **Wi-Fi** | [03](03-ai-camera-audio-feasibility.md) |
| Laptop | A nearby laptop on Wi-Fi **is permitted** (as a bridge) | [02](02-architecture.md) |
| AI provider | "probably opencode / open router". Provisional choice: **OpenRouter** (official docs checked). The design stays provider-neutral. | [03](03-ai-camera-audio-feasibility.md) |
| Soldering | **No soldering.** Every connection must be plug-in or screw-terminal. | everywhere |
| Budget | Target **AU$50**. **Hard ceiling AU$70** for all extra hardware **including delivery**. Core Electronics preferred, other suppliers allowed. | [08](08-bom-budget-sourcing.md) |
| Printing | Unlimited PLA / resin. Build volume doesn't matter (parts can be split). | [11](11-mechanical-design-print-assembly.md) |
| Repo | Existing private repo, temporary name OK. Robot name **Pip** (picked by the parent). | — |

## 2. Assumptions (each one must be confirmed or corrected)

| # | Assumption | Why it matters | How to confirm |
|---|---|---|---|
| A1 | The kit is **v1.2** (OLED 128×64, 3× RGB LED, atmospheric, buzzer, colour, capacitive touch, accelerometer, distance sensor, cables, LiPo Expansion Board, Platform) | Pin and I2C plan, sensor choices | "v1.2" is printed under the barcode on the kit box (Core listing) |
| A2 | The kit **does not include a LiPo battery**. The current listing shows none. | Power design | Look in the box |
| A3 | **A breadboard is not in the v1.2 listing.** The user mentioned owning one. **The design does not depend on a breadboard.** Motor and servo current never goes through a breadboard. | Wiring | Confirm whether one is owned (handy for bench tests only) |
| A4 | The user already owns a **micro-USB data cable** for programming the Pico | BOM | Check |
| A5 | The user may already own a **USB power bank**, **jumper wires**, small **M3 screws**, **rubber bands / O-rings** and a **hook-and-loop strap**. The BOM prices these anyway and lists them as "maybe owned". | Budget | Check at home |
| A6 | The laptop can run Python 3.11+ and stays on the **same Wi-Fi network** as Pip during play | Architecture | Test early ([09](09-build-plan-milestones-tests.md) M1) |
| A7 | Home or school Wi-Fi allows device-to-device traffic (no "client isolation") | Architecture | Test early; fallback is the laptop's hotspot |
| A8 | An **adult** holds the OpenRouter account and API key, and the key has a **spending limit** | Safety, cost | Parent sets it up |
| A9 | Pip is used **supervised**. It is a school prototype, **not a certified toy**. | Safety | — |
| A10 | Printer is FDM with a 0.4 mm nozzle printing PLA. Resin is not used for structural or child-handled load-bearing parts. | Mechanical | Confirm printer type |

## 3. Open decisions (needed before final integration)

| # | Decision | Options | Recommendation | Blocks |
|---|---|---|---|---|
| D1 | **Budget vs. features.** The full solder-free feature set costs **at least AU$148.71** at Core Electronics prices checked on 2026-10-19 (including AU$7 standard delivery). That is before a power bank (~AU$14.50, unverified) and some small unpriced items. That is well over the AU$70 ceiling ([08](08-bom-budget-sourcing.md)). | Continue lower-cost sourcing, or explicitly agree a reduced scope. The AU$70 total cap remains fixed. | Do not order the over-budget concept | Ordering |
| D2 | **Deadline** | unknown | — | Milestone dates in [09](09-build-plan-milestones-tests.md) are given as relative weeks |
| D3 | **AI provider and model**, and who pays for API credit | OpenRouter (provisional); any OpenAI-compatible endpoint | OpenRouter with a per-key credit limit; text model only at first | Software integration |
| D4 | Speech-to-text and text-to-speech: on the laptop or in the cloud | local (free, private) vs. cloud audio models (cost, privacy) | **Local on the laptop** first | Bridge software |
| D5 | Power path | A: USB power bank (recommended) · B: protected 1S LiPo on the Robo Pico | A ([05](05-power-budget-charging.md)) | BOM, CAD |
| D6 | Motor driver / Pico carrier | Cytron **Robo Pico** (recommended; out of stock at Core on 2026-10-19) vs. alternatives | Robo Pico, or wait for restock | BOM, CAD |
| D7 | Laptop operating system and whether it can run a hotspot | — | — | Network fallback |
| D8 | School consent and privacy rules for a camera and microphone near children | — | Ask the teacher before any test with children | Testing with children |

## 4. Requirements that are at risk (nothing has been silently dropped)

| Requirement | Status in this design | Risk |
|---|---|---|
| Four wheels | 2 driven wheels + 2 swivel casters | Low |
| Head pans left/right | FS90 servo in a protected neck with a slip clutch and hard stops | Clutch torque needs testing |
| Onboard rechargeable battery with an accessible port | Consumer USB power bank in the base; charge port in the rear shell | Bank size and port position must be measured |
| Camera tracks subjects | XIAO ESP32S3 Sense camera in the head; tracking runs on the laptop | Depends on the laptop and Wi-Fi; latency not yet measured |
| Two rear buttons (wake/power, movement enable) | Two printed plungers acting on the Robo Pico's GP20/GP21 buttons, plus the Robo Pico hard power switch via an actuator | Button and switch positions must be measured |
| Screen in the middle of the body for questions | PiicoDev OLED 128×64 (kit) in the belly, with 3 capacitive answer pads below it | The OLED is small (23 × 11 mm active area). Fine for icons and short words. A larger screen is a later upgrade. |
| Spoken conversation | Onboard mic (XIAO Sense) + onboard speaker (Gravity module) + laptop bridge + web LLM | **Costs more than the cap** (D1) |
| Follow a person | Camera bearing + ToF distance closed loop | Same as above |
| No soldering | All parts chosen to be plug-in or screw-terminal | Two hand-tool steps remain, and neither is soldering: (1) **stripping ~7 mm** off the ends of two 22 AWG hook-up wires for screw terminals; (2) clamping male jumper pins in screw terminals. No USB cable has to be cut in the recommended path. |
| ≤ AU$70 | **Not met** by the sourced concept; no compliant full configuration has been verified | See D1 |
