# 00 · Status, assumptions and open decisions

User update: the owned bank is a bulky 10,000 mAh model. Capacity does not establish size or output current. Dimensions, mass, port layout and ratings are pending. The current tray and body envelope are placeholders and may need widening before printing.

**Project:** Pip, a companion robot for children aged 5–8 that encourages off-screen play (IST project; closed loop sensor → output → feedback).
**Round:** design v0.2, 2026-10-19. No hardware has been bought, printed, wired or tested. Automated CAD checks have been run.

> **Status: design only. Firmware is not implemented. Purchase status: HOLD.**
> No configuration meeting every requirement within the AU$70 total was found ([08](08-bom-budget-sourcing.md)). Nothing should be ordered until (1) a complete configuration meets the fixed budget, or the user explicitly accepts a reduced scope, (2) stock is re-checked on the day, and (3) the rated-power gates in [05](05-power-budget-charging.md) §5 can be met with the chosen parts. The CAD is a parametric prototype with placeholder dimensions for every bought part. It is not final and not fit-verified.

## 1. Confirmed by the user

| Topic | Answer |
|---|---|
| Controller | One Raspberry Pi Pico 2 WH (owned) |
| Kit | Core Electronics PiicoDev Starter Kit for Raspberry Pi Pico (owned; assumed current v1.2) |
| Users | Children aged 5–8, indoors |
| Functions | 4 wheels; screen in the middle of the body for questions; moving head; two rear buttons (wake, movement enable); rechargeable onboard battery with an accessible port; camera tracking a person; onboard spoken conversation with a web AI over Wi-Fi; reacting to sensors |
| Laptop | A nearby laptop on Wi-Fi is permitted as a bridge |
| AI provider | OpenRouter preferred (provisional; the design is provider-neutral) |
| Soldering | None, for every connection |
| Budget | **Hard cap AU$70 total** for additional hardware **including delivery** (target AU$50) |
| Printing | Unlimited PLA/resin |
| Power bank | Owned; model, port count and ratings unconfirmed. No spare Android phone. |
| Repo / name | Private repo `etphli/ist-pico-project`; robot name Pip |
| Deadline | Unknown |

## 2. Assumptions (confirm or correct)

| # | Assumption | How to confirm |
|---|---|---|
| A1 | Kit is v1.2 (OLED, RGB LED, atmospheric, buzzer, colour, touch, accelerometer, ToF distance, LiPo Expansion Board, Platform, cables) | Label under the barcode |
| A2 | No battery in the kit | Look in the box |
| A3 | A breadboard may be owned. The design does not use one. | — |
| A4 | A micro-USB data cable is owned for programming | Check |
| A5 | A power bank is owned, but suitability is unconfirmed. Wire offcuts, M3/M2.5 screws, strap and O-rings may be owned and are unpriced. | Check at home; any purchase changes the budget |
| A6 | The laptop runs Python 3.11+ and shares a Wi-Fi network with Pip | Test early |
| A7 | The network allows device-to-device traffic (else use the laptop hotspot) | Test early |
| A8 | An adult owns the AI account and key, with a credit limit | Parent |
| A9 | Supervised use only; prototype, not a certified toy | — |
| A10 | FDM printer, 0.4 mm nozzle, PLA | Confirm |

## 3. Decisions needed

| # | Decision | Options | Recommendation |
|---|---|---|---|
| **D1** | **Budget vs scope** | (a) Accept a reduced scope listed in [08](08-bom-budget-sourcing.md) §4 (e.g., R1 drops the onboard camera and voice); (b) keep the full requirements and continue lower-cost sourcing | Decide explicitly. Until then: **HOLD**. Do not split purchases into stages to look compliant. |
| D2 | Deadline | unknown | Milestones are in relative weeks ([09](09-build-plan-milestones-tests.md)) |
| D3 | AI account and who pays | OpenRouter with a per-key limit | Adult-owned |
| D4 | Speech processing | Local on the laptop first | Local first |
| D5 | Power bank compatibility | Owned bank: model, ports and ratings unknown | Check PG1 against its label before selecting a topology |
| D6 | Master disconnect | Accept "unplug both leads" as the master disconnect, or find a solder-free rated switch | Open (PG5) |
| D7 | Laptop OS / hotspot | — | — |
| D8 | School consent for camera/mic with children | — | Ask before any session with children |

## 4. Requirement status (nothing silently dropped)

| Requirement | Full concept (over budget) | Risk / open item |
|---|---|---|
| 4 wheels | 2 TT drive + 2 casters | Low |
| Moving head | FS90, clutch, stops | Servo supply margin (PG2); no position feedback |
| Rechargeable battery, accessible port | Power bank behind the rear door | Bank not selected (PG1) |
| Camera person-tracking | DFR1154 + laptop tracker | Lens position placeholder; 160° lens needs calibration |
| Two rear buttons | 2 PiicoDev Buttons + plungers | Second button address method to confirm |
| Screen in the middle | Kit OLED in the belly | Small (23 × 11 mm active) |
| Onboard spoken conversation | DFR1154 mic + amp + speaker; laptop bridge; OpenRouter | Speaker out of stock; echo not yet tested |
| Follow a person | Camera bearing + ToF range with alignment, freshness and plausibility gates | ToF does not identify the person ([02](02-architecture.md) §4.2) |
| No soldering | All plug, terminal or lever connections | Kitronik GPIO terminals must accept the cable pins (verify) |
| ≤ AU$70 | **Not met** | **HOLD** |
