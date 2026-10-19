# 08 · Bill of materials, budget and sourcing

> **Purchase status: HOLD. Do not order anything from this page.** No complete configuration was found that meets every requirement within the **AU$70 total** (hardware plus delivery). The full concept below is an **over-budget alternative for comparison only**. The reduced-scope options in §4 drop requested functions. They are listed only so the user can decide whether to accept one. None of them is the requested robot.

Prices are AU$ including GST, read on **2026-10-19** from Core Electronics' live catalogue (product pages and catalogue search, both generated from Core's live stock system). Later the same day Core stopped responding, so the full-concept cart could not be quoted end to end. Stock changes daily. Machine-readable version: [`bom.csv`](bom.csv).

## 1. Already owned (AU$0)

- Raspberry Pi Pico 2 WH
- PiicoDev Starter Kit for Raspberry Pi Pico, assumed v1.2 ([00](00-status-assumptions-decisions.md) A1): OLED 128×64, RGB LED, atmospheric sensor, buzzer, colour sensor, capacitive touch, accelerometer, distance (ToF) sensor, PiicoDev LiPo Expansion Board, Platform, cables
- Unlimited PLA/resin printing

**Confirmed owned:** MINISO QW01 10,000 mAh power bank. Approximate size 130 × 60 × 10 mm, micro-USB input and two USB-A outputs, each reported 5 V / 2 A. Combined output and fit remain unverified. No spare Android phone.

**Not confirmed as owned:** small screws, wire, a hook-and-loop strap and two O-rings or rubber bands. The full concept needs two suitable USB-A outputs; ownership alone does not establish compatibility. See [00](00-status-assumptions-decisions.md) A4–A5.

## 2. What changed from the first concept, and why

| First concept | Revised | Reason (source) |
|---|---|---|
| Cytron Robo Pico carrier, AU$27.90 | **Kitronik Compact Motor Driver Board 5331** (Core CE07855), AU$19.95 | Robo Pico out of stock at Core. Kitronik states the board's DRV8833 has **built-in short-circuit, over-current and thermal protection** and **1.5 A max per channel**. Supply 3–10 V, reverse-polarity protected, on/off switch, powers the Pico (Kitronik datasheet). Cytron's Robo Pico datasheet states 1 A continuous / 1.5 A peak (< 5 s) and no driver protection, which is below the TT motor's stall current. |
| XIAO ESP32S3 Sense AU$30.60 + Gravity speaker AU$9.51 + 10-pack cable AU$11.60 | **DFRobot ESP32-S3 AI Camera DFR1154**, AU$37.23, + 8 Ω 1 W speaker with 1.25 mm plug, AU$4.80 | One preassembled board with camera (OV3660, 160°), PDM mic, MAX98357 I2S amplifier and an MX1.25 speaker socket (DFRobot wiki). It is powered by its own USB-C 5 V input, so it no longer hangs off a reduced motor rail. |
| Robo Pico on-board buttons GP20/GP21 | **2 × PiicoDev Button** (CE08500), AU$16.10 | The Kitronik board exposes only 4 GPIOs. The buttons plug into the PiicoDev chain and are debounced on board (Core). |
| 22 AWG spools AU$15.20, 10-pack Gravity cables AU$11.60 | Short lengths of wire (unpriced, see B14), 10 cm jumper pack AU$3.20, 2 lever connectors AU$2.80 | Avoids buying whole spools and packs for a few connections. |
| ADA3629 USB-A socket fed from a servo-port rail (≈4.6 V) | Camera fed **directly from a bank USB-A port** through a USB cable and an in-line USB-C power switch (CE06575, AU$3.45) | The camera gets an ordinary USB 5 V supply. The switch gives a camera/mic hard-off ([05](05-power-budget-charging.md)). |

## 3. Full-function concept: over budget, comparison only

Every requirement is addressed by a part. The power design is still subject to the gates in [05](05-power-budget-charging.md).

| ID | Item | Core SKU | Qty | Unit | Ext. | Stock 2026-10-19 | Notes |
|---|---|---|---|---|---|---|---|
| B1 | Kitronik Compact Motor Driver Board for Pico (5331) | CE07855 | 1 | 19.95 | 19.95 | in stock (3 today, more 8–10 days) | Pico 2 WH plugs in; screw terminals; switch |
| B2 | TT gearmotor 200 RPM 3–6 V, 200 mm leads with male pins | ADA3777 | 2 | 7.35 | 14.70 | in stock | Stall 1.2 A at 4.5 V, 1.5 A at 6 V (Adafruit bench figures on the listing) |
| B3 | Feetech FS90 servo 4.8–6 V | CE09376 | 1 | 5.70 | 5.70 | in stock | Voltage gate PG2 in [05](05-power-budget-charging.md) |
| B4 | DFRobot ESP32-S3 AI Camera (camera, mic, I2S amp) | DFR1154 | 1 | 37.23 | 37.23 | in stock (16 today) | Speaker **not** listed as included |
| B5 | Mini oval speaker 8 Ω 1 W, Molex PicoBlade 1.25 mm plug | ADA3923 | 1 | 4.80 | 4.80 | **out of stock** | Plug fit to the DFR1154 "MX1.25" socket not yet confirmed |
| B6 | PiicoDev Button | CE08500 | 2 | 8.05 | 16.10 | in stock | Second unit needs a different I2C address (check method) |
| B7 | PiicoDev Prototyping Cable (male pins) 200 mm | CE07796 | 1 | 0.95 | 0.95 | catalogue | I2C from Kitronik GP0/GP1/3V/GND terminals to the chain |
| B8 | USB-A male plug → 5-pin screw terminal block | ADA3628 | 1 | 9.65 | 9.65 | in stock | Bank port 1 → body power |
| B9 | Wago 221-413 3-conductor lever connector | WG-221-413 | 2 | 1.40 | 2.80 | in stock | +5 V and GND split: controller + servo |
| B10 | Jumper wire 10 cm M/M (40) | CE09607 | 1 | 3.20 | 3.20 | catalogue | Servo signal and servo power tails |
| B11 | USB-A → USB-C cable 50 cm, 2 A | CE09370 | 1 | 3.25 | 3.25 | in stock | Bank port 2 → camera switch |
| B12 | USB-C in-line power switch cable 28 cm (C female → C male, ≤ 3 A) | CE06575 | 1 | 3.45 | 3.45 | in stock | Camera/mic hard-off |
| | **Priced subtotal (hardware)** | | | | **121.78** | | |
| B13 | Delivery | Core | 1 | — | **not quoted** | — | Core quoted AU$6.25 standard to example postcode 2000 for two smaller test carts the same day. Delivery depends on the cart and postcode. |
| B14 | Stranded wire ~22 AWG, ~0.3 m red + ~0.3 m black | — | — | — | **unpriced** | — | No cheaper verified short pack found. Do not buy two spools for 30 cm. |
| B15 | Power bank, **2 × USB-A out**, combined ≥ 3 A preferred, stays on at low load | — | 1 | — | **owned, AU$0 if compatible** | — | Core's AU$26.95 5000 mAh bank has one output, so it does not suit this topology. An owned bank must be checked ([05](05-power-budget-charging.md)). |
| B16 | Screws: 14 × M3 × 10–12 pan-head thread-forming for plastic, 4 × M2.5 × 6 | — | — | — | **unpriced** | — | List and locations in [11](11-mechanical-design-print-assembly.md) §6 |
| B17 | Hook-and-loop strap (bank), 2 O-rings ~60 mm ID (tyres) | — | — | — | **unpriced** | — | maybe owned |

**Result:** priced hardware alone is AU$121.78, before delivery, wire, screws and strap. The owned bank adds no purchase cost if it proves compatible. That is **AU$51.78 over the cap before the unpriced items**. Status: **over budget, HOLD.**

## 4. Is there a configuration at or under AU$70?

**No configuration was found** that meets all requirements (moving 4-wheel base, panning head, onboard camera tracking, onboard mic and speaker for conversation, two rear buttons, rechargeable onboard battery) within AU$70. This is a finding of this search, not a proof that none exists.

What was searched (all solder-free, Core live catalogue unless noted):

| Function | Cheapest solder-free option found | AU$ | Rejected cheaper options |
|---|---|---|---|
| Two DC motors from the Pico | Kitronik 5331 | 19.95 | Makerverse 2-ch driver AU$6.60: Core's own guide says its terminals and headers mount on **unsoldered pads**. Pimoroni Motor SHIM: solder-on header. Pololu DRV8833 carrier: header not fitted. Robo Pico AU$27.90: out of stock. |
| Drive motors | ADA3777 × 2 | 14.70 | Feetech TT 50 RPM CE09390 AU$2.50 each: rated **3 V**, so a 5 V supply exceeds its rating. Its JST-PH plug would also need cutting. |
| Camera + mic + speaker drive | DFR1154 (+ speaker) | 37.23 + 4.80 | XIAO Sense AU$30.60 has no amplifier, so a speaker module and cable are extra (≥ AU$40 total). Waveshare ESP32-S3 2" display board AU$30.45 has no microphone listed. ESP32-CAM boards have no microphone. |
| Head servo | FS90 | 5.70 | No servo with a manufacturer-stated minimum below 4.8 V was found at Core. FT90B listings conflict (3–4.8 V vs 3–6 V) and none is a manufacturer page. |
| Rear buttons | 2 × PiicoDev Button | 16.10 | With the Kitronik board only GP27/GP28 remain free. Loose tactile switches need soldering or a breadboard. |

**Minimum essentials** (driver, motors, servo, camera board, speaker) already total **AU$82.38** before buttons, power connections or delivery.

### Reduced-scope options (each needs the user's explicit acceptance; none is the requested robot)

| Option | What it would do | What it drops | Priced hardware | Fits AU$70? |
|---|---|---|---|---|
| **R0 Bench loops, AU$0** | Kit-only closed loops on the bench: ToF distance → OLED/LED/buzzer, touch → feedback, tilt → alarm. Laptop Wi-Fi link for text prompts. | Wheels, head, camera, voice, onboard battery | 0 | yes |
| **R1 Mobile body, no onboard camera or voice** | B1 + B2 + B3 + 2 × B6 + B7 + 2 × B9 + B10. Driving, head pan, rear buttons, OLED quiz, ToF stop/approach, colour games, tilt stop. Text conversation through the laptop. | Onboard camera tracking, onboard mic and speaker (F5, F9), so no person following and no spoken conversation on the robot | **63.40** + delivery (AU$6.25 if the example quote applied = **69.65**) | **only if** the bank, a spare USB-A cable to cut and strip for the 5 V feed (replacing B8), wire and screws are already owned. Any extra purchase breaks the cap. |
| R2 Stationary talking head | B3 + B4 + B5 + 2 × B6 + B11 + B12 | Driving | 70.53 + delivery | **no** |
| R3 R1 plus an owned spare Android phone as the head | R1 hardware plus a phone streaming camera/mic and playing speech | Unavailable: user confirmed no spare phone. A phone head redesign is not selected. | as R1 | **unavailable with confirmed inventory** |

Recommendation: **keep purchases on HOLD** and ask the user to choose: (a) accept a reduced scope such as R1 or R3, knowing which requested functions are dropped, or (b) keep the full requirement set and continue sourcing. The current concept exceeds the cap. Do not split the full concept into "stages" to appear compliant. The total is what counts.

## 5. Where to look next (not yet verified)

- **Robo Pico** elsewhere (element14 AU, Cytron direct) — prices not verified live; out of stock at Core and Pakronics.
- **Overseas marketplaces** (e.g., AliExpress modules with factory-fitted terminals): landed prices, GST, delivery time and whether terminals are pre-soldered could not be verified. No total is given for them.
- **School or club parts** (wire offcuts, screws, spare USB cables) cost AU$0 only once actually agreed.

## 6. Ongoing costs (separate from hardware)

| Item | Basis | Amount |
|---|---|---|
| OpenRouter credit | Prepaid USD credit, 5.5% purchase fee (US$0.80 min) (OpenRouter FAQ) | Not estimated. Measure from bridge token logs ([03](03-ai-camera-audio-feasibility.md) §5). Set a per-key credit limit. |
| Filament | owned | ~0.6 kg PLA for one set (CAD volume × 1.24 g/cm³ × 55% fill estimate; no slicer run) |

All sources: [sources.md](sources.md).
