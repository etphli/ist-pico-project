# 05 · QW01 power topology, limits and charging

Design v0.3, 2026-10-21. **Electrical assembly remains on HOLD.** The mechanical revision accommodates the owned bank's approximate size. It does not establish electrical compatibility or approve the over-budget parts list.

## 1. Owned source and evidence

| Property | Recorded value | Evidence and limit |
|---|---|---|
| Bank | MINISO QW01, 10,000 mAh | User report, 20 October |
| Size | Approximately 130 × 60 × 10 mm | User estimate, not caliper measurements |
| Charging input | Micro-USB | User report; input rating not provided |
| Outputs | Two USB-A sockets | User confirmed wide rectangular sockets |
| Output rating | **5 V / 2 A each**, or 10 W per port | User transcribed the label and clarified "each" |
| Combined simultaneous output | **Unknown** | Two individually rated ports do not establish 4 A or 20 W combined |
| Mass, protection, low-load shutdown | **Unknown** | No exact manufacturer datasheet located; requires verification |

Do not substitute another MINISO model's specifications. Do not join the two USB outputs together, use a Y cable to combine current, or open the bank. Capacity in mAh does not specify output current. Runtime remains unmeasured.

## 2. Proposed branch layout

The branch assignment is retained so the camera/audio load has its own USB lead. It is a reference layout pending the load and protection work below.

```
MINISO QW01, intact and strapped in the revised cradle
  USB-A output 1, reported 5 V / 2 A
    → USB-A terminal adapter → rated power wire and lever connectors
      → Kitronik 5331 power terminal → board switch → Pico + sensor chain + motor driver
      → FS90 servo power; GP27 supplies its signal, with a common body ground

  USB-A output 2, reported 5 V / 2 A
    → ordinary USB-A-to-USB-C cable → camera power switch
      → DFR1154 camera/microphone/audio board → plug-in speaker

  Micro-USB INPUT
    ← charge cable only after BOTH robot output leads are unplugged
```

The USB outputs remain separate power branches. The body needs a common signal ground between its Pico, driver and servo. No motor current passes through GPIO, Pico 3V3, a breadboard or PiicoDev cables. Every power connector and conductor must have a known current rating. Verify servo power leads rather than assuming any jumper wire is sufficient.

**Hard-off:** unplug both robot USB-A leads. The body switch does not disconnect the servo branch upstream of it, and it does not disconnect the head. The head has a separate camera power switch. Software sleep stops streaming and motion but is not a hardware disconnect. A single all-branch power switch remains unresolved and unpriced.

**Programming:** with the rear shell removed, disconnect both bank output leads before plugging the Pico into a laptop. Do not assume the carrier prevents backfeeding from simultaneous supplies.

## 3. Per-branch voltage and current budget

| Load or branch | Voltage requirement | Current evidence | QW01 assessment |
|---|---|---|---|
| Kitronik 5331 | 3–10 V, manufacturer datasheet | Logic-regulator capacity not published in the checked document | Nominal 5 V is in range; logic and sensor-chain capacity remains a gate |
| Two TT motors | 3–6 V, retailer copy of Adafruit data | Example stall figures: 1.2 A each at 4.5 V, 1.5 A each at 6 V | Two simultaneous stalls can exceed one 2 A port before logic and servo loads are added |
| FS90 | 4.8–6 V, retailer listing | About 0.8 A at stall, retailer listing | Only about 0.2 V nominal supply margin. Wiring loss or a bank voltage dip can take it below rating |
| **Body branch, output 1** | Nominal 5 V | Previous fault estimate **3.3–4.1 A** including motors, servo and logic | **Exceeds the reported 2 A port limit. Not cleared for assembly** |
| DFR1154 and speaker, output 2 | USB-C 5 V, DFRobot | Simultaneous streaming, microphone and audio-playback draw not established | Must be measured and remain within 2 A, with operating margin |
| Both outputs together | Nominal 5 V | Shared bank limit unknown | Cannot approve simultaneous operation from the individual port labels alone |

The body fault estimate is not a measured consumption value. Normal play could draw less, but that does not establish safe fault behaviour. Soft starts and PWM speed caps reduce demand in some conditions; they are not a dependable current limit.

The speaker, motor, servo and bank limits must be considered separately. A supply cutoff intended to protect the bank does not establish that motor windings, driver, leads or servo remain within their limits.

## 4. Protection and outstanding redesign

Kitronik states that its DRV8833 has short-circuit, over-current and thermal protection. This is driver protection. It does not establish a safe sustained motor-stall duration. The board's maximum channel figure is not a motor-current limit selected for this robot.

Before this bank can power the complete concept, select and document a solder-free means of keeping the body branch within the source and component limits. Possible approaches include lower-stall-current motors or suitable hardware current limiting with a validated stop response. No such replacement or limiter has been selected, priced or approved in v0.3. Do not connect the existing body concept and rely on the bank to trip.

Moving the servo to the camera branch would reduce output-1 demand but would not, by itself, solve two simultaneous motor stalls or the unknown combined limit. It is not adopted as an unverified fix. Do not parallel the bank outputs.

The current mechanical and functional design is preserved while these electrical choices remain open. New electrical parts must also fit the no-soldering requirement and AU$70 total budget. The existing AU$121.78 comparison BOM already exceeds that cap.

## 5. Gates before wiring and driving

All results are pending. These gates are acceptance conditions for a future build, not claims of completed tests.

| Gate | Check | Pass condition |
|---|---|---|
| PG1 | Record both individual output limits, the combined limit, charging-input rating and low-load behaviour of this QW01 | Documented source limits and a complete branch budget with margin. The 2 A individual ratings alone do not pass this gate |
| PG2 | Servo rail during motor starts and head motion, after a suitable protected power design exists | Remains inside the servo's 4.8–6 V rating throughout; no brownouts |
| PG3 | Source, motor, driver and servo protection | Selected hardware and documented continuous/transient limits. A teacher reviews a guarded, current-limited bench test plan. No sustained-stall or hand-held wheel tests on the unprotected concept |
| PG4 | Camera rail during video, microphone and speaker load | Within the board's documented input limits and the port's 2 A limit, with margin. No resets; both-output demand within the verified shared limit |
| PG5 | Master disconnect and charge procedure | Both USB-A leads can be reached and unplugged; no hidden live servo or head branch is mistaken for off. A single-switch solution remains optional unresolved work |
| PG6 | Kitronik logic regulator and Pico sensor-chain capacity | Known ratings exceed peak measured logic and sensor current with margin; do not infer a regulator rating from a short successful test |
| PG7 | Reset and watchdog behaviour | Motors remain off through boot/reset; motion enable clears; network and audio cannot hold motor outputs on |

A multimeter and suitable guarded/current-limited bench equipment are school tools to borrow, not assumed purchases in the BOM. Do not test beyond a known component rating to discover its limit.

## 6. Charging and service access

The bank's **micro-USB input** is the only designated charging connection. The head's USB-C cable is an output load from the bank, not a way to charge the bank. There is no pass-through charging design.

1. Disable movement and switch off the body and head.
2. Undo the rear hatch's M3 screw with adult supervision, tilt the hatch out and lift it off the bottom tongues.
3. Unplug **both** robot output leads from the bank.
4. Connect the bank's micro-USB charging cable, following its own input rating and instructions.
5. Leave the hatch off while charging on a hard surface under adult supervision. The hatch has no charging-cable notch.
6. Disconnect the charge cable before reconnecting robot power. Route the leads up the left side behind the upright, refit the hatch tongues, and secure its screw before use.

No automatic charging interlock is claimed. Physical disconnection of both output leads is the procedural isolation. The revised opening must allow actual plug removal without forcing the connectors or pinching cables.

## 7. Mechanical acceptance

The approximate 130 × 60 × 10 mm size drives the v0.3 cradle design. Accommodation space, strap retention, frame changes and connector clearance are described in [11](11-mechanical-design-print-assembly.md). Exact charge/output positions were not supplied. Open service access and adjustable placement must not be described as a measured port fit.

Before printing the final set, measure length, width, thickness, mass, port positions and the plugs that will actually be used. Update the parameters and rerun the CAD checks. The generated report establishes geometry checks against modelled envelopes only; it does not prove the bank fits in real life.

## 8. Technical references

- [Kitronik 5331 datasheet](https://core-electronics.com.au/attachments/localcontent/5331-compact-motor-driver-raspberry-pi-pico-datasheet_30137893d1d.pdf), reviewed in the previous design round.
- [DFRobot DFR1154 documentation](https://wiki.dfrobot.com/SKU_DFR1154_ESP32_S3_AI_CAM), USB power and audio/camera interfaces.
- [FS90 retailer listing](https://core-electronics.com.au/feetech-fs90-1-5kgcm-micro-servo-9g.html), voltage and stall-current figures are retailer evidence.
- [TT motor retailer listing](https://core-electronics.com.au/dc-gearbox-motor-tt-motor-200rpm-3-to-6vdc.html), example current figures are not tolerance bounds.

The earlier Robo Pico voltage correction remains recorded in [13](13-design-review.md): VIN-only supply uses VIN on its servo rail; the 0.4 V reduction applied to USB supply. That board is not the current selected carrier.
