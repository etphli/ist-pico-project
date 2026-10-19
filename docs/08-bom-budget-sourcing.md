# 08 · Bill of materials, budget and sourcing

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

Prices are **AU$ including GST**, checked **2026-10-19**. "Verified" means read from the live product page that day. "Snippet" means taken from a search-engine extract of the retailer page, which may be stale. Machine-readable version: [`bom.csv`](bom.csv). **Re-check every price and stock level in the cart before ordering.** This is a sourced estimate, **not a purchase-ready quote**.

## 1. Already owned (AU$0)

- Raspberry Pi Pico 2 WH (user)
- PiicoDev Starter Kit for Raspberry Pi Pico, **assumed v1.2** (Core CE08256, listed at AU$86.50): OLED 128×64, 3× RGB LED (listing wording; check whether this is one 3-LED module or three modules), atmospheric sensor, buzzer, colour sensor, capacitive touch, accelerometer, distance sensor, PiicoDev LiPo Expansion Board, Platform, 10 cables (4×50, 2×100, 2×200 mm). **No battery is listed. A breadboard is not listed** (the user mentioned one, so confirm; the design does not need it).
- Unlimited PLA printing

## 2. Over-budget concept BOM (not approved for purchase)

| ID | Item | Supplier / SKU | Qty | Ext. AU$ | Price status | Stock 2026-10-19 |
|---|---|---|---|---|---|---|
| B1 | Cytron **Robo Pico** carrier (motor + servo drive, switch, buttons, PiicoDev port) | Core CE11203 | 1 | 27.90 | verified | **out of stock** |
| B2 | TT gearmotor 200 RPM 3–6 V, **pre-fitted leads** | Core ADA3777 | 2 | 14.70 | verified | in stock |
| B3 | Feetech FS90 micro servo | Core CE09376 | 1 | 5.70 | verified | in stock |
| B4 | Seeed **XIAO ESP32S3 Sense** (camera + mic + Wi-Fi) | Core SS113991115 | 1 | 30.60 | verified | lead time (est. Oct 27–29) |
| B5 | DFRobot Gravity Digital Speaker Module | Core FIT0449 | 1 | 9.51 | verified | in stock |
| B6 | Gravity PH2.0→DuPont cable 50 cm (10-pack) | Core FIT0756 | 1 | 11.60 | snippet | check |
| B7 | USB-A **male** → screw terminal block | Core ADA3628 | 1 | 9.65 | verified | in stock |
| B8 | USB-A **female** → screw terminal block | Core ADA3629 | 1 | 9.65 | verified | lead time (est. Oct 27–Nov 02) |
| B9 | USB-A → USB-C cable 50 cm | Core CE09370 | 1 | 3.25 | snippet | in stock |
| B10 | Jumper wires M/F 20 cm (40) | Core CE09130 | 1 | 3.95 | snippet | in stock (cached) |
| B11 | 22 AWG stranded wire, red | Core PRT-08865 | 1 | 7.80 | snippet | in stock (cached) |
| B12 | 22 AWG stranded wire, black | Core PRT-08867 | 1 | 7.40 | snippet | in stock (cached) |
| B13 | Core standard delivery | Core | 1 | **7.00** | "from $7"; exact amount at cart | — |
| | **Core subtotal incl. delivery** | | | **148.71** | | |
| B14 | USB power bank 10 000 mAh, USB-A + USB-C, 20 W | Kmart 43277094 | 1 | 14.50 | **unverified** (snippet "was $39"; page blocked) | unknown |
| B15–B17 | M3 screws ×2–6, hook-and-loop strap, 2 O-rings/rubber bands | hardware store | — | **not priced** | — | — |
| B18 | micro-USB data cable | assumed owned | 1 | 0 | — | — |
| | **Total with power bank (excl. B15–B17)** | | | **≈ 163.21** | | |

**Against the AU$70 hard ceiling: short by at least AU$78.71 without the power bank, or ≈ AU$93.21 with it.** This concept **does not fit** the budget. A complete cheaper configuration has not been verified. This is a real constraint, not an omission. Nothing has been dropped silently.

## 3. Where the money goes (and why each item is needed)

| Need (requirement) | Concept part(s) | AU$ |
|---|---|---|
| Drive two wheels and pan the head without soldering (F2, F3, F10) | B1 Robo Pico + B2 motors + B3 servo | 48.30 |
| On-robot camera + mic over Wi-Fi (F5, F8, F9) | B4 XIAO Sense + B9 cable | 33.85 |
| On-robot speaker (F9) | B5 + B6 | 21.11 |
| Robust motor power path (≈2 A+ peaks) without jumpers or breadboard | B7 + B11 + B12 | 24.85 |
| Camera/mic hardware-off with the main switch (F15 privacy) | B8 + B10 | 13.60 |
| Battery + accessible charge port (F4) | B14 (or owned) | 14.50 / 0 |
| Delivery | B13 | 7.00 |

## 4. Budget decision: hold purchases

The user's **AU$70 total cap is fixed**. Splitting an AU$162.71 order into stages does not meet that cap. Raising the budget is not the selected solution.

No complete, solder-free, delivered configuration meeting all requirements has been verified within AU$70. That is a limit of this sourcing work, not proof that no cheaper configuration exists. The table above is a comparison concept, not a minimum possible price. Its power system also needs revision, so AU$163.21 is not a complete build quote.

Further sourcing should check these specific savings before choosing hardware:

- A speaker supplied with its matching cable, rather than a ten-pack of cables.
- Short lengths of suitable wire from school, rather than two full spools. Treat borrowing as confirmed only once agreed.
- A preassembled combined camera, microphone and speaker board. The [Waveshare ESP32-S3-CAM family](https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx) integrates camera and audio electronics. A matching speaker, actual connector, delivered AU price and power requirements still need checking. It is a candidate, not a selected substitute.
- A solder-free motor carrier in stock, with suitable current limits and a rated supply path. A cheap listing with bare solder pads does not satisfy the requirement.
- An already-owned power bank, only if its voltage, output current, size and low-load behaviour meet the eventual design.

A reduced-scope robot with sensor games and laptop AI could cost less, but removing camera tracking or onboard voice would change the user's requirements. No such change is assumed here. The existing kit can already demonstrate a distance-to-display or touch-to-feedback loop without buying parts. This is a useful bench milestone, not the finished robot.

## 5. Ongoing costs (separate from hardware)

| Item | Basis | Amount |
|---|---|---|
| OpenRouter credit | prepaid USD credit, 5.5% purchase fee (US$0.80 min) | **Not estimated.** Measure from bridge token logs ([03](03-ai-camera-audio-feasibility.md) §5). Set a per-key limit. |
| Free OpenRouter models | 50 requests/day without credits; 1000/day after buying ≥ 10 credits | Can be rate-limited; don't rely on them for a demo |
| Filament | owned | AU$0 to the user. Rough CAD estimate ~0.6 kg PLA for one full set (volume × 1.24 g/cm³ × 55% effective fill; no slicer was run). Budget ~1 kg including reprints. |

## 6. Sourcing notes and supply risks

- **Robo Pico is out of stock** at Core (and at Pakronics, AU$26.22). Ask Core for an ETA, or check element14 AU. Don't design around a substitute until one is actually available. If none, re-open D6.
- XIAO Sense and ADA3629 have **lead times** of about 1–2 weeks.
- Core delivery: "Standard from $7, Express from $11" (listing text). Heavier orders may cost more. LiPo cells can't go by air (not relevant for Option A).
- Kmart and element14 pages could not be fetched directly (blocked). Treat their prices as unverified.
- All sources are in [sources.md](sources.md).
