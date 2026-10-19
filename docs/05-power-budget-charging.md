# 05 · Power topology, ratings, protection and charging

User update, 2026-10-20: owned MINISO QW01, 10,000 mAh; approximately 130 × 60 × 10 mm, not exact. Micro-USB charging input and two USB-A outputs, each reported as 5 V / 2 A. Combined simultaneous output, protection, mass and low-load behaviour remain unverified. The current CAD still uses the older 100 × 66 × 24 mm placeholder. A placement check of the approximate footprint found tray/frame overlap, so fit is not approved.

> **Wiring HOLD.** This page defines the revised power topology for the full concept in [08](08-bom-budget-sourcing.md) §3 and the **gates** it must pass. Nothing here authorises running any part outside its rating. If a gate fails, that branch stays unbuilt and the design changes. Running it "to see" is not an option.

## 1. Corrections to the first concept

| First concept said | What the manufacturer documents say | Consequence |
|---|---|---|
| Robo Pico servo/motor rail = VIN − 0.4 V ≈ 4.6 V | Cytron Robo Pico datasheet, spec table row 6: with **only VIN or only LiPo** connected, Vmotor & Vservo = **VIN**. The − 0.4 V drop applies when powered from the Pico's **USB** (rows 5, 7, 8). | The 4.6 V figure was wrong for VIN supply. The Robo Pico is dropped anyway (out of stock; 1 A continuous per channel is below the TT motor's stall current; no driver protection stated). |
| XIAO powered from a servo-port rail via jumpers | Seeed: XIAO ESP32S3 USB-C input "5V". DFRobot: DFR1154 USB-C input "5V DC". | The camera board is now fed by an **ordinary USB cable from a bank USB-A port**, the way it is meant to be powered. No rail-derived 5 V is used. |
| Firmware stall loop (L5), PWM caps and soft starts protect against stall | PWM and ramps limit average drive. They do not limit current into a stalled motor at the commanded duty, and they cannot detect a stall. There is no current sensing and no wheel encoder. | Stall protection must be **hardware** (§4). No firmware stall detection is claimed. |

## 2. Revised topology (full concept)

```
           USB power bank (2 x USB-A outputs; charge input behind the rear door)
             │ port 1 (USB-A)                                │ port 2 (USB-A)
        [B8 ADA3628 USB-A plug → screw terminals]       [B11 USB-A → USB-C 50 cm]
             │ +5 V / GND on ~22 AWG (B14)                   │
        [B9 lever connectors: +5 V, GND]                [B12 USB-C in-line power switch]  ← camera/mic hard-off
          │                    │                             │ (power pins only)
          │                    │                        DFR1154 camera board USB-C (head, through the neck)
          │                    │                             └ MX1.25 → 8 Ω speaker (head)
   Kitronik 5331 power    FS90 servo V+ / GND
   terminal (3–10 V)      (jumper tails into servo plug)
     │ on-board switch (body power) ← printed rear actuator
     ├ DRV8833 → TT motor L, TT motor R
     ├ 3 V regulator → Pico 2 WH (40-way socket) → Pico 3V3 OUT → PiicoDev chain (10 modules incl. 2 buttons)
     └ GP27 → servo signal (jumper)
   Common ground: both bank ports share the bank's ground. The body and camera are also tied through the USB grounds. The servo ground returns on the body ground.
```

**Master disconnect:** no solder-free switch rated for the whole robot's current was found in the checked catalogue. The interim master disconnect is **unplugging both USB-A plugs from the bank**. They sit in the charge-door bay, which only an adult opens. The Kitronik switch is the everyday "body power" switch, and the in-line switch is the "camera/mic" switch. **Gap:** the Kitronik switch does **not** cut the servo branch (the servo sits upstream of it). With the Pico off the servo receives no control pulses, but it stays connected to the bank. A single switch for all branches remains an **open item** (G-PWR-5).

## 3. Rating check per branch

| Branch | Load rating (source) | Supply in this topology | Status |
|---|---|---|---|
| Kitronik 5331 supply | 3–10 V (Kitronik datasheet) | Bank USB 5 V nominal | Within rating with wide margin |
| TT motors ADA3777 | 3–6 V (listing) | DRV8833 output ≤ supply ≈ 5 V | Within rating |
| DRV8833 channel current | 1.5 A max per channel (Kitronik datasheet) | TT stall 1.2 A at 4.5 V, 1.5 A at 6 V (Adafruit bench figures on the Core listing) | The figures are examples, not tolerance bounds. A 1.5 A maximum is not proof of a permissible continuous stall. Confirm continuous ratings and a motor-protection strategy before load tests (PG3). |
| FS90 servo | 4.8–6 V (Core listing; Feetech page not checked) | Bank USB 5 V nominal minus plug, wire and lever-connector drops | Nominal 5 V is inside the rating, but the **margin is only ~0.2 V**. Gate **PG2**: the measured voltage at the servo plug must stay ≥ 4.8 V during the worst-case load test. **If it does not, the head servo stays disconnected.** No servo with a manufacturer-stated lower minimum was found. |
| DFR1154 camera board | USB-C 5 V DC (DFRobot); VIN range conflicts between sources (Core 5–12 V, DFRobot wiki 3.7–15 V), so VIN is **not used** | Standard USB cable from a bank port | Within rating as an ordinary USB-powered device. Gate **PG4** records the voltage at its USB-C under load. |
| Pico 2 WH | Powered by the Kitronik 3 V regulator through the socket (Kitronik datasheet) | — | **Regulator current capacity is not stated** by Kitronik. The Pico 2 W radio plus 10 PiicoDev modules must fit within it. Gate **PG6**: ask Kitronik or measure. HOLD until known. |
| PiicoDev chain | 3.3 V modules | Pico 3V3 OUT (Pico 2 W datasheet recommends < 300 mA load on 3V3) | Keep RGB brightness low. Measure the chain current (PG6). |
| Bank | MINISO QW01: user reports 5 V / 2 A on each of two USB-A outputs | Combined limit unknown | Each port is 10 W nominal. Do not infer 4 A / 20 W combined. PG1 is not passed; the original ≥ 2.1 A per-port criterion is not met by the reported 2 A rating. Reconcile measured load and protection with the actual limits before adopting this bank. |

## 4. Current budget and hardware protection

| Load | Typical (estimate unless noted) | Worst case | Hardware that limits or interrupts it |
|---|---|---|---|
| TT motor × 2 | 0.15 A no-load each (listing); 0.2–0.4 A driving, estimate | 1.2–1.5 A **each** at stall (listing) | **DRV8833 over-current and thermal protection** (stated by Kitronik). This protects the **driver**, not the motor windings. No motor stall-duration rating is published. |
| FS90 | 0.12 A no-load at 6 V (listing) | 0.8 A stall (listing) | **None in hardware.** Mechanical: the neck slip clutch slips before the gear train is loaded to stall ([11](11-mechanical-design-print-assembly.md) §4), and firmware limits travel to ±70° against ±75° stops. The 250 mA PTC at Core (RXE025) is below normal servo current and was rejected. A suitable PTC was not found in stock and is unpriced (open item). |
| Pico 2 W + PiicoDev chain | 0.1–0.3 A, estimate | measure | Kitronik regulator (rating not stated) |
| DFR1154 + speaker | Not published. Seeed's comparable XIAO streaming figures (≈ 0.14 A average, 0.35 A peak) are a guide only. | measure | Bank port 2 protection (bank-specific) |
| **Port 1 worst case** | ~1 A | **≈ 3.3–4.1 A** (both motors stalled + servo stalled + logic) | **Bank port over-current protection, if the chosen bank has it.** Verify from the bank maker's data, then by gate PG3. |

**What this means, stated plainly:**

1. The worst case on port 1 (≈ 3.3–4.1 A) is **above** what most single USB-A ports supply. If the bank's own protection trips, the whole body loses power. The Pico restarts with **movement disabled** ([02](02-architecture.md) §3), so the robot stops. A reset must leave movement disabled, but this is **not a verified motor-protection strategy**. A bank may sustain a damaging motor stall below its trip threshold. Gate PG3 checks it.
2. **No dependable motor-stall detection is claimed.** With no current sensor and no encoders, the Pico cannot tell "stalled against a wall" from "driving at constant speed". The accelerometer sees neither, because constant velocity and standstill both read ~1 g. The ToF sensor may be blocked or reading something else. The motion-anomaly heuristic in [02](02-architecture.md) is **advisory logging only**.
3. **PWM duty limits and soft starts are kept** to limit speed and inrush. They are **not** stall protection.
4. A sustained stall heats the TT motors at up to 1.5 A each until the driver's thermal protection cycles or the bank trips. Controls: adult supervision; motion only in short, enabled bursts with a time-out (enable expires after 5 min, any motion command expires after 0.2 s); stop if movement is commanded while the ToF reads below the stop threshold. Do not deliberately sustain a stall on this prototype. PG3 remains blocked until protection and component limits are established.

## 5. Gates before wiring and before driving

Every gate is a pass/fail **verification of a rated condition**. None authorises out-of-rating operation.

| Gate | What | Method | Pass |
|---|---|---|---|
| PG1 | Bank suitability | Read the maker's label/datasheet: two USB-A outputs, per-port and combined current, protection, low-load behaviour. Then a 10 min test at ~50 mA load. | Two A ports; per-port ≥ 2.1 A stated; stays on |
| PG2 | Servo supply | Wheels off the ground. Meter (or a scope if borrowed) at the servo plug while both motors start and reverse at the speed cap and the servo slews. | **Never below 4.8 V.** Fail → servo stays disconnected; redesign the servo supply. |
| PG3 | Overload behaviour | Before testing, a teacher reviews continuous component limits and hardware protection. Use a current-limited bench supply and guarded fixture, never hold a powered wheel by hand. Define fault duration from manufacturer limits. Without those limits and protection, keep this gate blocked. | Within documented current, duration and thermal limits; reset leaves motion disabled. A touch test alone cannot pass this gate. |
| PG4 | Camera supply | Meter at the DFR1154 USB-C (USB-C breakout or USB meter, borrowed) while streaming and playing audio | Record; continuous streaming without brown-out resets for 10 min |
| PG5 | Master disconnect | Decide a single all-branch switch, or accept the unplug procedure | User decision; recorded |
| PG6 | Logic supply | Kitronik regulator rating (ask Kitronik) vs measured Pico + chain current at peak Wi-Fi | Known rating ≥ measured peak with margin |
| PG7 | Reset state | Hold the Pico in reset, then reboot it, with motors connected and wheels off the ground | Motors do not move during reset or boot |

## 6. Battery and charging

The owned bank is the MINISO QW01 described above. Its charging input is micro-USB, not USB-C. The charging opening, connector clearance and retention must be revised after exact measurements. PG1 remains open.

- **Option chosen:** a finished consumer power bank (its own charge and protection electronics). No loose lithium cells. The kit's PiicoDev LiPo Expansion Board is a 1-cell charger for the Pico. It has no motor or servo supply and is not used in the robot.
- **Charge port access:** the bank's charge input sits behind the sliding rear door (CAD `charge_door`).
- **Runtime:** unmeasured for the owned QW01. A bank's mAh label is the internal cell capacity, not the amount delivered at 5 V. Measure (T-PWR-1).
- **Charging with the robot unable to drive:** the Pico cannot sense the bank charging. **No automatic interlock exists in this design.** Procedure: switch the body off, open the door, **unplug both robot leads from the bank**, then plug in the charger. With both leads unplugged the robot cannot drive. That is a procedural control, not an interlock. A mechanical interlock, where the door can only open with the switch off, is not modelled (open item).
- Charge on a hard surface, supervised by an adult, following the bank maker's instructions.

## 7. Reduced-scope option R1 power (if chosen)

R1 replaces B8 with a spare USB-A cable cut and stripped into the lever connectors. Cutting and stripping is not soldering. The cable's conductor gauge is unknown and must carry the port-1 worst case. Use only a cable whose gauge can be identified, and repeat gates PG1–PG3 and PG6–PG7. There is no camera branch in R1.

## 8. Owned-bank update and fit check, 2026-10-20

The brand, model, capacity, approximate size, input type and individual output ratings above are user-reported. No MINISO manufacturer datasheet for this exact model was located. Per-port ratings do not establish simultaneous combined capacity or protection behaviour. The bank must not be opened or modified.

The current body's estimated 3.3–4.1 A port-1 fault demand exceeds this bank's reported 2 A individual output. Its second port does not add current to port 1. Do not parallel the outputs. A lower-current/protected drive arrangement or different power distribution is still required for the concept; no compatibility pass is claimed.

A conservative rectangular 130 × 60 × 10 mm envelope, at the existing bank rear-face position and tray-top height, was checked against the current CAD. Approximate intersections were 510 mm³ with the tray and 907 mm³ with a front frame column. No intersection with the two body shells was found at that placement. This is a diagnostic placement check only, not a fit certificate: rounded corners, plugs, tolerances and straps were omitted. Exact dimensions and port positions are needed before revising the tray and frame. The existing STL set is unchanged.
