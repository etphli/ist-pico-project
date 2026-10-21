# 15 · Reduce cost while keeping Pip's functions

Checked 21 October 2026. Keep the camera, microphone, speaker, four wheels, panning head, screen and both rear buttons. These options preserve the intended functions. Equivalent reliability and performance still need physical testing.

The current baseline is AU$116.98 before delivery and unpriced items. Combining the proposed button and cable substitutions gives AU$92.27 before resistors, mounts, wire, screws, straps, tyres, delivery and any required power-protection parts. This is a comparison, not a complete order or an AU$70 build.

The user confirmed unlimited standard PiicoDev module cables on 21 October. The nine proposed SH-to-SH links therefore cost AU$0 to obtain. They were not included as an extra purchase in the subtotal, so this does not subtract another amount from it. The male-ended B7 breakout, USB leads and rated power wiring are separate. The later wiring review adds unpriced B19 bus-interface work and B20 servo-harness selection. B10 remains a provisional signal-only pack and can be removed if B20 provides that lead.

## Use the supplied speaker

I counted an extra speaker in the earlier BOM. [DFRobot's DFR1154 shipping list](https://www.dfrobot.com/product-2899.html) includes a speaker and a Gravity cable. Confirm Core supplies that standard package, then use the supplied speaker. It removes the separate AU$4.80 purchase without removing voice output.

This correction is reflected in [bom.csv](bom.csv). B5 is an optional spare with quantity zero. The original subtotal was AU$121.78. The corrected subtotal is AU$116.98, using the other prices recorded on 19 October.

The current CAD speaker pocket still uses the earlier spare's 30 × 20 × 5 mm envelope. Measure the supplied speaker, plug and lead. Update `Boards.spk_l`, `spk_h` and `spk_t` in [params.py](../cad/pip_robot/params.py), then check its mount and regenerate. Do not force a differently shaped speaker into that pocket.

## Replace the expensive button interfaces

Two PiicoDev Buttons cost AU$16.10 in the baseline. Core lists [breadboard-friendly mini pushbuttons](https://core-electronics.com.au/mini-push-button-switch.html) at AU$0.52 each, including GST, checked 21 October. Two switches cost AU$1.04, saving AU$15.06 before resistors, wiring and a secure mount.

Both physical buttons remain. A resistor network lets the Pico distinguish them on one analogue input. This uses the available GP28 terminal because GP27 drives the head servo. [Raspberry Pi's Pico 2 datasheet](https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf) identifies GP28 as an ADC-capable pin.

The proposed circuit has a 10 kΩ pull-up from GP28 to 3V3. Button A connects GP28 to ground through a separate 10 kΩ resistor. Button B connects GP28 to ground through a 22 kΩ resistor. Use 1% resistors. Nominal readings with a 3.3 V rail are approximately 3.30 V released, 1.65 V for A, 2.27 V for B and 1.34 V for both. These are calculations, not measured thresholds. Never connect this circuit to 5 V.

Before adopting this option:

1. Confirm each switch's connected terminal pairs with a continuity meter.
2. Prototype the circuit on the owned breadboard with motor power disconnected.
3. Measure the four reading bands, including noise and repeated presses.
4. Add debounce and separated acceptance bands in firmware. Treat both pressed, invalid readings and detected faults as movement disabled.
5. Test release, held buttons, reset, Wi-Fi loss and loose connections. Boot must leave movement disabled.
6. Design a clamped mount so the breadboard and switches cannot move under the rear plungers.
7. Update the upright, plungers, wiring plan, tests and guide together before using this variant.

This change is not implemented in the v0.3 CAD or firmware. An analogue reading cannot detect every wiring fault. Do not describe the circuit as a safety-rated stop or assume it has the same reliability as the original interface without testing. A breadboard is appropriate only for these low-current signals, never motor or main supply current.

## Reuse a suitable USB lead for the body feed

The baseline USB-A screw-terminal adapter costs AU$9.65. A spare, suitably rated USB-A lead can replace it if its power conductors can be identified, stripped and secured in compatible connectors. This requires cutting and stripping, but no soldering.

Saving the whole AU$9.65 assumes you already own a suitable lead. A lead bought for this purpose reduces the saving. Verify its conductor size, current rating, polarity, strain relief and loaded voltage drop. Insulate unused data wires separately. Recheck hatch clearance with its actual plug and wire bend. An unknown thin charging cable is not a verified substitute.

This full-concept substitution is proposed only. [The baseline wiring plan](04-wiring-pin-plan.md) still specifies the adapter. Its allowance for cutting a cable under reduced-scope R1 does not establish that any cable suits the complete robot.

## Check the arithmetic and the remaining gap

The combined comparison uses the recorded baseline and the newly checked switch price:

```text
Original baseline                                AU$121.78
Remove duplicate speaker                              -4.80
Corrected baseline                                  116.98
Replace AU$16.10 button modules with AU$1.04 switches  -15.06
Use an already-owned, verified USB power lead          -9.65
Conditional priced subtotal                           92.27
```

The proposed subtotal is AU$29.51 below the original list. It remains AU$22.27 above the AU$70 cap before the unpriced items. The earlier example delivery quote of AU$6.25 is historical. Core's current button page advertises standard delivery from AU$7, but the complete cart and postcode need an actual quote.

Borrowing school wire offcuts, resistors, screws or straps can reduce purchasing costs only after availability is confirmed. Buying one combined order can avoid repeated shipping charges. Neither saving changes motor, camera or AI performance.

Keep the current driver and camera choices until an alternative passes the same electrical, audio, tracking and no-soldering checks. Lower-stall-current motors or a protected power revision could change both cost and performance. No such replacement is approved here. The unresolved QW01 power limits in [05](05-power-budget-charging.md) still apply to every cost variant.

## Edit this estimate

Update [bom.csv](bom.csv) for adopted baseline parts and [08](08-bom-budget-sourcing.md) for the matching totals. Keep unimplemented options on this page. Record the price date, quantity, delivery quote and what must be owned or borrowed. Do not count an unpriced item as zero.
