# 04 · Wiring and provisional pin plan (solder-free)

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

> **SUPERSEDED POWER PATH: DO NOT WIRE.** Sections 5–6 record the original concept for review only. W8 and W10/W11 are blocked by rated-voltage issues, and the supply/protection is unresolved. Read [05](05-power-budget-charging.md) and [13](13-design-review.md).

> **Provisional.** Based on the Cytron Robo Pico datasheet (Rev 1.0, Apr 2023), the Raspberry Pi Pico 2 W datasheet and Core Electronics listings. Check every connector's polarity and pin order against the silkscreen **of the parts that actually arrive** before first power-up ([12](12-measurement-calibration-checklist.md)).

## 1. Ground rules

1. **No soldering.** Every connection is a plug, a socket header or a screw terminal.
2. **Motor and servo currents never flow through:** the Pico's 3V3 pin, PiicoDev cables, jumper wires, or a breadboard. Motors connect to the Robo Pico's motor terminals. The servo plugs into a Robo Pico servo port. The 5 V supply enters through the Robo Pico **VIN screw terminal** on 22 AWG wire.
3. Logic is **3.3 V only**. PiicoDev/Qwiic modules are 3.3 V. Never connect 5 V to a GPIO.
4. One common ground. All grounds meet on the Robo Pico.
5. Power the robot **off** (Robo Pico switch) before plugging or unplugging anything.

## 2. Why the Robo Pico, and not the kit's PiicoDev LiPo Expansion Board?

The kit's **PiicoDev LiPo Expansion Board** (schematic Rev v11, checked) has: an MCP73831-type charger, about 220 mA default charge current (440 mA only after **soldering** the FAST_CHG jumper, so not allowed here), a JST-PH battery connector, a P-MOSFET that switches VBAT to VSYS when USB is absent, and the PiicoDev connector on **I2C0 GP8/GP9** with 120 Ω series resistors. **It has no motor or servo drivers.** Adding a separate solder-free driver to it would need power-distribution wiring that, without soldering, ends up going through jumpers or a breadboard (forbidden for motor current). No solder-free 2-channel driver with pre-fitted terminals was found in stock at Core on 2026-10-19.

The **Cytron Robo Pico** takes the Pico 2 WH directly and provides, with no soldering: 2 × DC motor channels (1 A continuous / 1.5 A peak per channel), 4 × servo ports, a power **on/off switch**, a VIN terminal (3.6–6 V), 2 user buttons, a buzzer, NeoPixels, 7 Grove ports and a **JST-SH "Maker Port" compatible with PiicoDev/Qwiic**. Core lists it as compatible with Pico, Pico W and Pico 2. **Pico 2 W compatibility is not listed explicitly.** The pinout is the same as the Pico W, so it is expected to work, but verify (M1 bench test).

Consequence: the kit's LiPo Expansion Board and Platform are **not used in the robot**. They stay useful for bench testing PiicoDev modules.

## 3. Pin allocation (Pico 2 W on Robo Pico)

| Pico GPIO | Robo Pico function (fixed by board) | Pip use | Notes |
|---|---|---|---|
| GP0, GP1 | Grove 1 | spare | |
| **GP2, GP3** | **Maker Port (I2C1 SDA/SCL)**, shared with Grove 2 | **PiicoDev chain** | Don't use Grove 2 |
| GP4, GP5 | Grove 3 | spare | |
| GP6 | Grove 5 | spare | |
| GP7 | Grove 7 | spare | |
| **GP8, GP9** | **Motor 1 A/B** | **Left drive motor** | 20 kHz PWM (slice 4) |
| **GP10, GP11** | **Motor 2 A/B** | **Right drive motor** | 20 kHz PWM (slice 5) |
| **GP12** | **Servo port 1** | **Head pan servo FS90** | 50 Hz PWM (slice 6 A). **Leave GP13 unused**, because it shares slice 6. |
| GP13 | Servo port 2 | **unused** (PWM slice conflict) | |
| **GP14** | **Servo port 3** | **Speaker signal (PWM audio)** | Gravity cable plugs onto the 3-pin servo header: S → GP14, + → V+ (VIN − 0.4 V), − → GND. **Check pin order first.** Slice 7 A at ~60–120 kHz carrier. |
| GP15 | Servo port 4 | signal **not connected** | Only this port's **V+ and GND** pins are used, to feed the XIAO (switched 5 V rail) |
| GP16, GP17 | Grove 4 | spare | |
| GP18 | NeoPixel RGB LEDs (on board) | status / "camera on" indicator | Seen through a hole in the rear shell |
| **GP20** | **User button** | **Rear button A: wake / sleep** | Pressed by a printed plunger |
| **GP21** | **User button** | **Rear button B: movement enable** | Pressed by a printed plunger |
| GP22 | Piezo buzzer (mute switch) | UI beeps | |
| GP26, GP27, GP28 | Grove 6/7 analog | spare | GP28 battery sense needs a **solder jumper**, so it is **not used** |
| GP23, GP24, GP25, GP29 | (Pico 2 W internal: wireless SPI, power) | — | GP29/ADC3 reads VSYS/3 when no wireless SPI transfer is running (Pico 2 W datasheet) |
| WL_GPIO2 | (Pico 2 W) VBUS sense | detects the Pico's own USB cable (programming) | **Not** a charge detector in power option A |

## 4. I2C (PiicoDev) chain on the Maker Port

Kit cables available (v1.2): 4 × 50 mm, 2 × 100 mm, 2 × 200 mm. Proposed daisy chain (8 modules, 8 cables):

```
Robo Pico Maker Port
 └50─ Atmospheric (rear upright, near vents)
      └100─ Accelerometer (base plate, centre-rear)
            └100─ Colour sensor (base plate, front, looking down)
                  └200─ Touch (front shell, belly)            ← unplug here to remove the front shell
                        └50─ OLED (front shell, belly window)
                              └50─ Buzzer (front shell, right chest)   (tight: ~48 mm centre-to-centre, MEASURE)
                                    └50─ Distance ToF (front shell, chest centre)
                                          └200─ RGB LED (front shell, left "cheek", coiled)
```

| Module (kit v1.2) | Expected default 7-bit address | Status |
|---|---|---|
| OLED 128×64 SSD1306 (CE07911) | 0x3C (0x3D with ASW switch on) | from Core listing |
| Distance sensor (CE07741, VL53L1X class) | 0x29 | **verify with `i2c.scan()`** |
| Capacitive touch (CE07816, CAP1203 class) | 0x28 | verify |
| Accelerometer (CE08705) | 0x19 | verify |
| Colour sensor (CE07823) | 0x10 | verify |
| Atmospheric (CE07503) | 0x77 | verify |
| RGB LED (CE07910) | 0x08 | verify |
| Buzzer (CE08219) | 0x5C | verify |

- MicroPython: the PiicoDev drivers accept a bus and pin selection, so use **I2C1, SDA=GP2, SCL=GP3** instead of the PiicoDev default (I2C0 GP8/GP9, which the motors use here). *Check the exact constructor arguments in the current PiicoDev Unified library.*
- **Pull-up load risk:** each PiicoDev module carries its own I2C pull-ups (check the module docs). Eight in parallel may load the bus heavily. Test at 100 kHz first. If the bus is unreliable, shorten the chain or split modules onto Grove 4 (GP16/17 = I2C0) **using a Grove-to-Qwiic adapter cable, which is not in the BOM**. Disabling pull-ups on PiicoDev boards means cutting a trace jumper. That is not soldering, but it can only be undone by soldering, so avoid it.
- **3.3 V budget:** the Robo Pico datasheet limits the total +3V3 output on the Grove/Maker ports to **300 mA**. Keep RGB LED brightness ≤ 30% (see [05](05-power-budget-charging.md)).

## 5. Power wiring (option A: USB power bank, recommended)

```
USB power bank (USB-A out)
  └─ [ADA3628] USB-A male plug → 5-pin screw terminal block
        VBUS(+) ──22 AWG red── Robo Pico VIN +   (screw terminal)
        GND(−)  ──22 AWG black─ Robo Pico VIN −
Robo Pico ON/OFF switch (via printed actuator) gates EVERYTHING below:
  ├─ Pico 2 W (VSYS via Robo Pico)
  ├─ Motor terminals M1, M2 → TT motors (pre-fitted wire leads; male pins clamp in the terminals, or use the board's terminal type)
  ├─ Servo port 1 → FS90 (its own 3-pin plug)
  ├─ Servo port 3 → Gravity speaker (Gravity PH2.0→DuPont cable)
  ├─ Servo port 4 V+/GND → 2 × M/F jumpers → [ADA3629] USB-A female ← terminal block
  │        └─ USB-A → USB-C cable (50 cm) → through the neck → XIAO ESP32S3 Sense (head)
  └─ Maker Port 3V3 → PiicoDev chain
Power-bank USB-C INPUT (charging) ← reached through the rear charge door, robot switched OFF
```

Polarity checks before connecting VIN: read the ADA3628's terminal labels with a multimeter on the bank (+5 V on VBUS). A multimeter is **not in the BOM**. Borrow one from school. The Robo Pico datasheet text checked does **not** state reverse-polarity protection on VIN, so treat VIN as **unprotected**: red to +, black to −, checked twice.

## 6. Connection list (for the build log)

| # | From | To | Conductor | Current class |
|---|---|---|---|---|
| W1 | Bank USB-A | ADA3628 plug | USB | up to bank limit |
| W2/W3 | ADA3628 VBUS/GND | Robo Pico VIN +/− | 22 AWG stranded, ≤ 15 cm, stripped 6–7 mm | **power** |
| W4/W5 | Left TT motor leads | M1A / M1B | motor's own leads (28 AWG per retailer) | motor |
| W6/W7 | Right TT motor leads | M2A / M2B | same | motor |
| W8 | FS90 plug | Servo port 1 | servo lead | servo |
| W9 | Gravity speaker | Servo port 3 | FIT0756 cable | ≤ 0.2 A |
| W10/W11 | Servo port 4 V+ / GND | ADA3629 + / − | M/F jumpers (30 AWG class) | ≤ 0.3 A (XIAO) |
| W12 | ADA3629 USB-A | XIAO USB-C | CE09370 50 cm cable through the neck | ≤ 0.3 A |
| W13 | Maker Port | PiicoDev chain | kit cables | ≤ 0.3 A total 3V3 |
| W14 | Pico micro-USB | Laptop (programming only, shell off) | user's cable | — |

Note on W10/W11: the XIAO's streaming draw (~138 mA average per the Core listing) is well within what a short jumper can carry. Measure the peaks (T-PWR-3).
