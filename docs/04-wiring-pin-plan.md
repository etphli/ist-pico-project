# 04 · Wiring and pin plan (solder-free) — full concept

> **Wiring HOLD** until the gates in [05](05-power-budget-charging.md) §5 pass and the purchase decision in [08](08-bom-budget-sourcing.md) is made. Sources: Kitronik 5331 datasheet, Raspberry Pi Pico 2 W datasheet, DFRobot DFR1154 wiki, Core product pages. Check every terminal label, polarity and connector against the parts that actually arrive ([12](12-measurement-calibration-checklist.md)).

## 1. Ground rules

This v0.3 plan uses the owned MINISO QW01. Its micro-USB socket is the charging input, while its two USB-A sockets supply the body and camera separately. Each output is reported as 5 V / 2 A; the shared total remains unknown. The present body branch's fault estimate exceeds 2 A, so the connection list below is not cleared for assembly. Bank ports, plug clearance and lead routing must match the revised [mechanical layout](11-mechanical-design-print-assembly.md).

1. **No soldering anywhere.** Every connection is a plug, a socket, a screw terminal or a lever connector. Stripping insulation is allowed. Cutting is allowed only where stated (option R1).
2. Motor current flows only through the Kitronik terminals and the motors' own leads. Body supply current flows only through the ADA3628 terminals, ~22 AWG wire and the lever connectors. **No motor or supply current** goes through the Pico's pins, PiicoDev cables, breadboards or jumper pins. The servo's own current goes through jumper tails into its plug; ≤ 0.8 A at stall (listing). Check the jumper gauge on delivery.
3. Logic is 3.3 V. Never connect 5 V to a GPIO or to the PiicoDev chain.
4. One common ground ([05](05-power-budget-charging.md) §2).
5. Body switch off and both bank plugs out before changing any connection. Do not join the USB outputs together or add a Y cable to combine their current.

## 2. Pin allocation (Pico 2 WH on Kitronik 5331)

The Kitronik board fixes the motor pins and breaks out only GP0, GP1, GP27, GP28, 3V and GND on terminals (Kitronik datasheet).

| Pico GPIO | Fixed by board | Pip use | Notes |
|---|---|---|---|
| GP2, GP3 | Motor 1 | Left drive motor | Kitronik truth table: 10 forward, 01 reverse, 00 coast, 11 brake |
| GP6, GP7 | Motor 2 | Right drive motor | same |
| **GP0, GP1** | terminal | **I2C0 SDA / SCL → PiicoDev chain** | via B7 prototyping cable (male pins into the terminal block). 3V and GND terminals feed the chain. |
| **GP27** | terminal | **Head servo signal (50 Hz PWM)** | 3.3 V logic. FS90 logic-level input is not specified by the listing. Core's own Pico servo guide drives servos directly from Pico GPIO. Verify on the bench. |
| GP28 | terminal | spare | |
| all others | inside the socket | not reachable without soldering | — |

Audio, camera and microphone are **not** on the Pico. They are on the DFR1154 in the head, which talks to the laptop bridge over Wi-Fi.

## 3. PiicoDev (I2C0) chain

```
Kitronik GP0/GP1/3V/GND terminals ── B7 prototyping cable (male pins)
 └ Button A "wake" (rear upright)  ─ Button B "move enable" (rear upright)
   └ Atmospheric (upright, near vents) ─ Accelerometer (base, rear) ─ Colour (base, front, facing down)
     └200─ Touch (front shell)   ← unplug here to remove the front shell
       └ OLED (belly window) ─ Buzzer ─ Distance ToF (chest) ─ RGB LED (left cheek)
```

- 10 modules on one bus. Each PiicoDev module carries pull-up resistors. Test at 100 kHz first, and record the bus behaviour with all 10 connected.
- The two Buttons share a default address (0x42, Core listing). One must be changed, using the method in Core's PiicoDev Button documentation. Confirm that the method needs no soldering. If it needs a solder jumper, stop and re-plan.
- Default addresses of the other modules: check with `i2c.scan()` (only the OLED's 0x3C was checked against its listing).
- Kit cables: 4 × 50, 2 × 100, 2 × 200 mm. Lengths for the upright → base → front-shell runs must be measured. Extra 200 mm PiicoDev cables cost AU$0.98 each at Core and are **not** in the BOM.
- The 3V terminal comes from the Pico's 3V3 OUT. The Pico 2 W datasheet recommends keeping the 3V3 load below 300 mA. Measure the chain (gate PG6).

## 4. Connection list

| # | From | To | Conductor | Notes |
|---|---|---|---|---|
| W1 | Bank USB-A port 1 | ADA3628 | USB plug | |
| W2/W3 | ADA3628 VBUS / GND | Lever connector +5 V / GND | ~22 AWG stranded, ≤ 15 cm, strip 7 mm | Check VBUS with a meter before connecting anything else |
| W4/W5 | Lever +5 V / GND | Kitronik power terminal + / − | ~22 AWG | Kitronik states reverse-polarity protection on its power input. Check polarity anyway. |
| W6/W7 | Lever +5 V / GND | FS90 plug V+ / GND | M/M jumper tail (stripped end in the lever; pin in the plug) | Servo branch; gate PG2 |
| W8 | Kitronik GP27 terminal | FS90 plug signal | M/M jumper | |
| W9–W12 | Left / right TT motor leads | Kitronik Motor 1 / Motor 2 terminals | Motor's own 28 AWG leads with male pins | Swap the leads to reverse a motor's direction |
| W13 | Kitronik GP0 / GP1 / 3V / GND terminals | PiicoDev chain | B7 prototyping cable | Pin order: check the cable colour code |
| W14 | Bank USB-A port 2 | USB-C in-line switch (B12) | B11 USB-A → USB-C cable | In-line switch mounted in the rear-upper body (holder not yet modelled) |
| W15 | In-line switch USB-C male (28 cm) | DFR1154 USB-C | up through the deck slot and neck | ~60 mm service loop in the head, ~80 mm in the body (cable twist test T-PAN-3) |
| W16 | DFR1154 speaker socket | Speaker | speaker's 1.25 mm plug | Confirm plug fit (B5) |
| W17 | Pico USB | Laptop (programming only, rear shell off) | user's cable | Programming without the bank connected is preferred |

## 5. First-power checklist

1. Meter on the ADA3628 terminals with only the bank connected: +5 V on VBUS.
2. Connect W4/W5 with the Kitronik switch off. Wheels off the ground. Switch on: power LED on, Pico boots, motors still.
3. Run `i2c.scan()` on I2C0 (GP0/GP1) and confirm every expected address.
4. Connect the servo (W6–W8) only after gate PG2 has been prepared. Run gates PG2, PG3, PG6 and PG7 ([05](05-power-budget-charging.md)).
5. Connect the camera branch (W14–W16) and run PG4.
