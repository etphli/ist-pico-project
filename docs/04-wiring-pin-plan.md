# 04 · Wiring and pin plan (solder-free): full wire-by-wire reference

> **Every circuit in this document is on HOLD.** The body branch's estimated fault current, 3.3–4.1 A, exceeds the QW01's reported 5 V / 2 A per port. The bank's combined output limit is unknown. I2C bus capacity and conditioning are unresolved, the body branch has no selected protection, and no Pip firmware exists ([05](05-power-budget-charging.md) §3–5). This is a reference for a future, cleared build. It does not clear any connection, and no part of it has been physically assembled or tested.
>
> The step-by-step procedure is in [16](16-wire-by-wire-assembly.md). This document is the authority on *what* connects to *what*; 16 covers the order, tools and checks.

## 1. How to read this document

**Logical, not physical.** Every table and diagram here is a *logical* schematic. It says which labelled terminal joins which other labelled terminal. It does **not** say where a terminal sits on a board, which way a connector faces, or the left-to-right order of terminals in a block. Those come from the parts that actually arrive. Read the printed label beside each terminal on the real board, photograph it, and record the physical order in the wiring log ([16](16-wire-by-wire-assembly.md) §16). If a label on the real part does not match a label used here, stop and update this document before wiring.

**Labels.** Terminal names are written as they appear in manufacturer documents: `GP0`, `GP1`, `GP27`, `3V`, `GND` on the Kitronik 5331; `VBUS`, `D+`, `D−`, `GND`, sleeve on the ADA3628. Record the exact printed text on your board.

**GPIO numbers are not header pin numbers.** `GP0` means RP2350 GPIO 0. It is not "pin 0" or "pin 1" of the Pico's header. The Kitronik board's terminals are labelled by GPIO number, so wire and program by GPIO label and never by counting header pins.

**IDs.** `W1`–`W17` are wires or plug-in connections. `W13` is split into four conductors, `W13a`–`W13d`. `C1`–`C9` are PiicoDev module-to-module cables. `B`-numbers are BOM rows ([bom.csv](bom.csv)). `PG`-numbers are power gates ([05](05-power-budget-charging.md) §5). `WO`-numbers are wiring open items (§9). BOM row O1 records the owned cables.

## 2. Ground rules

1. **No soldering.** Every connection is a plug, socket, screw terminal or lever connector. Stripping insulation and cutting wire to length are allowed. Do not cut PCB tracks or PCB jumpers. Restoring a cut PCB jumper needs solder.
2. **Supply current paths.** Motor current flows through the Kitronik driver and the motors' own leads. Main 5 V supply wiring uses the ADA3628, rated stranded wire and lever connectors. No motor or servo current may pass through GPIO pins, the `3V` terminal, PiicoDev cables, breadboards or signal jumper pins. The PiicoDev modules' own 3.3 V load uses `3V` and the SH cables, subject to PG6.
3. **3.3 V logic.** Never connect 5 V to a GPIO terminal or anywhere on the PiicoDev chain. Never feed servo V+ from the `3V` terminal.
4. **One body ground.** The Kitronik board, the Pico and the servo share ground through the lever connector and board (§4). The head needs no added external ground wire to the body.
5. **Two separate USB outputs.** Never join the bank's outputs, use a Y cable or connect one output's wiring to the other's.
6. **All wiring work is done with power removed:** both bank USB-A plugs out, Kitronik switch off, camera in-line switch off, Pico USB cable out.
7. **No breadboard.** The design does not use one, and no supply current may pass through one.

## 3. Pin allocation (Pico 2 WH on Kitronik 5331)

The Pico 2 WH plugs into the Kitronik 5331 and nothing else. Do not stack the kit's PiicoDev expansion board with the Kitronik carrier.

The Kitronik datasheet fixes the motor pins and brings out only `GP0`, `GP1`, `GP27`, `GP28`, `3V` and `GND` on screw terminals. The `3V` terminal is the Pico's 3V3 OUT. A separate regulated supply on the Kitronik board powers the Pico. The current capacity of the `3V` terminal is not stated in the datasheet. The Pico 2 W datasheet recommends keeping the 3V3 OUT load below 300 mA.

| Pico GPIO | Fixed by the board | Pip use | Notes |
|---|---|---|---|
| GP2, GP3 | Motor 1 | Left drive motor | Kitronik truth table: 10 forward, 01 reverse, 00 coast, 11 brake |
| GP6, GP7 | Motor 2 | Right drive motor | Same truth table |
| **GP0** | Terminal | **I2C0 SDA** → PiicoDev chain | W13c, blue conductor |
| **GP1** | Terminal | **I2C0 SCL** → PiicoDev chain | W13d, yellow conductor |
| **GP27** | Terminal | **Head servo signal** (50 Hz PWM) | W8. Acceptance of a 3.3 V signal by the FS90 is not specified; it is checked under PG2 |
| GP28 | Terminal | Spare | Not used in the baseline |
| `3V` | Terminal | PiicoDev chain supply | W13b. Capacity unknown (PG6) |
| `GND` | Terminal | PiicoDev chain ground | W13a |
| All other GPIO | Inside the socket | Not reachable without soldering | — |

**Software pin assignment.** Ordinary PiicoDev kit examples assume the kit's expansion board, which uses GP8 (SDA) and GP9 (SCL). On Pip the bus is on **GP0 (SDA) and GP1 (SCL)**. Firmware must set these pins explicitly. An unmodified kit example will not find the modules.

Audio, camera and microphone are **not** on the Pico. They are on the DFR1154 in the head. The head runs from its own USB branch and talks to the laptop bridge over Wi-Fi. No GPIO wire runs between the body and the head.

## 4. Power topology

![Logical power overview: QW01 output 1 feeds the body through the ADA3628 and two lever connectors; output 2 feeds the head through a USB-A-to-C cable and in-line switch; the micro-USB input is for charging only](images/wiring/01-power-overview.png)

*Logical diagram. It does not show terminal positions or connector orientation.*

```
QW01 USB-A output 1 ─W1─ ADA3628
                          VBUS ─W2─ Lever "+5V" ─W4─ Kitronik power + ─ [board switch] ─ board regulator ─ Pico
                                          └────W6─ servo V+ (pigtail, WO3)
                          GND  ─W3─ Lever "GND" ─W5─ Kitronik power − ─ board GND ─ Pico GND, GND terminal
                                          └────W7─ servo GND (pigtail, WO3)
                          D+, D−, sleeve: unused

Kitronik GP27 ─W8─ servo signal
Kitronik Motor 1 ─W9, W10─ left TT motor      Kitronik Motor 2 ─W11, W12─ right TT motor
Kitronik GND / 3V / GP0 / GP1 ─W13a–d─ B7 cable ─ PiicoDev chain (§6)

QW01 USB-A output 2 ─W14─ USB-A→C cable ─ in-line switch ─W15─ DFR1154 USB-C ─W16─ speaker
QW01 micro-USB input ← charge cable only, both outputs unplugged (§8)
Pico USB ─W17─ laptop, programming only, both outputs unplugged
```

### 4.1 Nets

A *net* is a set of points that are electrically the same. Each lever connector is one net: its three clamping points are a single common potential.

| Net | Points on the net | Feeds |
|---|---|---|
| BODY_5V | ADA3628 `VBUS`, +5V lever (all 3 points), Kitronik power +, servo V+ | Kitronik input and servo, upstream of the board switch |
| BODY_GND | ADA3628 `GND`, GND lever (all 3 points), Kitronik power −, Kitronik `GND` terminal, Pico GND, servo GND, PiicoDev GND | Common body ground |
| 3V3_OUT | Kitronik `3V` terminal, PiicoDev 3.3 V on every module | PiicoDev chain only |
| SDA | Kitronik `GP0`, PiicoDev SDA on every module | I2C data |
| SCL | Kitronik `GP1`, PiicoDev SCL on every module | I2C clock |
| SERVO_SIG | Kitronik `GP27`, servo signal | Servo PWM |
| M1_A | Motor 1 terminal A → W9 → left motor lead A | One side of left motor |
| M1_B | Motor 1 terminal B → W10 → left motor lead B | Other side of left motor |
| M2_A | Motor 2 terminal A → W11 → right motor lead A | One side of right motor |
| M2_B | Motor 2 terminal B → W12 → right motor lead B | Other side of right motor |
| HEAD_5V | VBUS contacts in QW01 output 2 → B11 → B12 switch → DFR1154 USB-C | Head 5 V supply |
| HEAD_GND | USB ground contacts in the same head cable path | Head return; may share BODY_GND internally in the bank |

Motor terminal A/B are logical names for the two distinct outputs, not a claim about printed labels. Never join the two terminals of a motor pair together.

**Ground continuity.** The servo's ground reaches the Pico through W7, the GND lever, W5 and the Kitronik board's own ground. No separate servo-to-Pico ground wire is needed. Head data uses Wi-Fi, so no external body-to-head ground wire is required. The bank's two outputs are not assumed to be galvanically isolated; they may share ground internally.

**The body switch is not a master switch.** The servo taps BODY_5V at the lever connector, upstream of the Kitronik switch. With the Kitronik switch off, the servo branch is still live while output 1 is plugged in. The only hard-off for the whole robot is unplugging **both** USB-A plugs from the bank (PG5, D6 in [00](00-status-assumptions-decisions.md)).

## 5. Connection list W1–W17

![Logical body power split: ADA3628 VBUS and GND to two lever connectors, each feeding the Kitronik power input and the servo](images/wiring/04-body-power-split.png)

![Logical motor and servo wiring: TT motors to Motor 1 and Motor 2 terminal pairs; servo V+ and GND from the lever connectors; servo signal from GP27](images/wiring/05-motors-and-servo.png)

*Logical diagrams. Terminal order, lead colours and connector orientation come from the delivered parts.*

"Conductor" names the part that carries the connection. "End prep" is how each end is prepared. Powered operation remains on HOLD. The status column identifies the few unpowered fit checks and the separate programming connection. Rows with an unresolved part also carry an open-item number.

| ID | From (logical label) | To (logical label) | Conductor | End prep | Status / open items |
|---|---|---|---|---|---|
| W1 | QW01 USB-A output 1 | ADA3628 USB-A plug | ADA3628 itself (B8) | Plug in fully by the plug body | HOLD. Only `VBUS` and `GND` terminals are used |
| W2 | ADA3628 `VBUS` | +5V lever connector, point 1 | Red ~22 AWG stranded copper (B14), ≤ 15 cm | ADA3628 end: strip to suit its screw terminal (check the part). Lever end: **11 mm** | HOLD |
| W3 | ADA3628 `GND` | GND lever connector, point 1 | Black ~22 AWG stranded copper (B14), ≤ 15 cm | As W2 | HOLD |
| W4 | +5V lever connector, point 2 | Kitronik power input + | Red ~22 AWG stranded (B14) | Lever end 11 mm. Kitronik end: strip to suit its terminal (check the part) | HOLD. Kitronik states reverse-polarity protection on this input; check polarity anyway |
| W5 | GND lever connector, point 2 | Kitronik power input − | Black ~22 AWG stranded (B14) | As W4 | HOLD. Also provides the body's common ground |
| W6 | +5V lever connector, point 3 | Servo plug V+ | Rated pre-terminated servo power pigtail, ~22 AWG (**not selected**) | Per the selected pigtail | HOLD, WO3, PG2 |
| W7 | GND lever connector, point 3 | Servo plug GND | Same pigtail as W6 | Per the selected pigtail | HOLD, WO3 |
| W8 | Kitronik `GP27` | Servo plug signal | Signal conductor: B10 M/M jumper as listed, or the selected pigtail's signal conductor | Prepare for the selected harness; terminal fit unconfirmed | HOLD, WO2, WO4, PG2 |
| W9 | Left TT motor, lead A | Kitronik Motor 1, terminal A | Motor's own 28 AWG lead with male pin (B2) | As supplied; secure clamping unconfirmed | HOLD, WO2 |
| W10 | Left TT motor, lead B | Kitronik Motor 1, terminal B | As W9 | As W9 | HOLD |
| W11 | Right TT motor, lead A | Kitronik Motor 2, terminal A | As W9 | As W9 | HOLD |
| W12 | Right TT motor, lead B | Kitronik Motor 2, terminal B | As W9 | As W9 | HOLD |
| W13a | Kitronik `GND` terminal | B7 **black** conductor | B7 PiicoDev prototyping cable (male), CE07796 | Male pin in the terminal; fit unconfirmed | HOLD, WO1, WO2 |
| W13b | Kitronik `3V` terminal | B7 **red** conductor (3.3 V) | B7 | As W13a | HOLD, WO1, WO2, PG6 |
| W13c | Kitronik `GP0` terminal | B7 **blue** conductor (SDA) | B7 | As W13a | HOLD, WO1, WO2 |
| W13d | Kitronik `GP1` terminal | B7 **yellow** conductor (SCL) | B7 | As W13a | HOLD, WO1, WO2 |
| W14 | QW01 USB-A output 2 | B11 USB-A → USB-C cable, A end | B11 (CE09370, 2 A) | Plug-in | HOLD, PG4 |
| W15 | B11 USB-C end → B12 in-line switch USB-C female; B12 USB-C male → DFR1154 USB-C | — | B12 (CE06575, 28 cm) | Plug-in | HOLD, PG4. ~60 mm service loop in the head, ~80 mm in the body (T-PAN-3) |
| W16 | DFR1154 speaker socket (MX1.25) | Supplied speaker | Speaker's own plug | Plug-in | Unpowered plug fit allowed ([14](14-illustrated-assembly-guide.md) Stage 10) |
| W17 | Pico USB | Laptop | User's data cable | Plug-in | Initial programming: Pico alone outside the carrier, with no external loads; both bank outputs unplugged. Mounted programming needs an approved power-path plan ([05](05-power-budget-charging.md) §2) |

### 5.1 Notes on specific rows

- **W1–W5.** The ADA3628 has five screw terminals: `VBUS`, `D+`, `D−`, `GND` and a fifth terminal for the plug's sleeve (shell). The fifth terminal is the sleeve, not an ID pin. Leave `D+`, `D−` and the sleeve empty.
- **Motor lead polarity (W9–W12).** Either lead can go in either terminal of its pair. If a motor turns the wrong way, fix it in firmware or swap that motor's two leads with power removed. Do not assume lead colours from photos.
- **Servo leads (W6–W8).** The FS90's lead colours are not confirmed by any source used here. Identify V+, GND and signal from the documentation supplied with the actual servo before wiring. Do not order or wire from a photo.
- **Servo power tails.** An earlier plan used B10 M/M jumper tails for servo power into the lever connector. The B10 jumpers' gauge and current rating are unspecified, and a thin jumper end may not clamp reliably in a lever connector. That plan is withdrawn. W6 and W7 need a known-rated, pre-terminated servo power pigtail or harness of about 22 AWG that mates with the servo plug. The exact part is not selected or priced (BOM B20, WO3). B10 jumpers are provisional for the W8 signal only; if B20 includes a signal lead, use that instead.
- **W13.** The B7 cable's colour code is confirmed on Core's product page: black GND, red 3.3 V, blue SDA, yellow SCL. Its SH plug goes into Button A, the first module of the chain (§6).
- **W14–W16.** Bank output 2 → USB-A-to-C cable → in-line USB-C switch → DFR1154 USB-C. The speaker connects only to the DFR1154's speaker socket. Both speaker wires are amplifier outputs; neither is ground. Do not connect a speaker wire to GND, a GPIO or any body wire, and do not add an external amplifier.
- **Unused DFR1154 Gravity port.** The DFR1154 has a Gravity connector that looks similar to a PiicoDev socket. It is not used. Never plug a PiicoDev cable into it.

## 6. PiicoDev (I2C0) chain

![Logical breakout: B7 cable from the Kitronik GND, 3V, GP0 and GP1 terminals to Button A](images/wiring/02-piicodev-breakout.png)

*Logical diagram. Terminal order on the real board may differ; follow the printed labels.*

![Logical module chain: B7, then cables C1 to C9 linking Button A, Button B, atmospheric, accelerometer, colour, touch, OLED, buzzer, ToF and RGB LED](images/wiring/03-module-chain.png)

*Logical diagram. Module positions in the robot are in [11](11-mechanical-design-print-assembly.md); cable routing is not modelled.*

### 6.1 How the chain works

Each PiicoDev module has two identical 4-pin SH sockets. Inside the module, the two sockets are wired in parallel: each socket carries the same four conductors (GND, 3.3 V, SDA, SCL). There is no IN or OUT socket, and the chain does not add voltages in series. Every module sees the same 3.3 V supply and the same two bus lines. The order of modules changes only cable routing, not the circuit.

The SH plugs are keyed. They go in one way only. If a plug does not slide in easily, check the orientation; never force it. Unplug by gripping the plug body, never by pulling the wires.

### 6.2 Cable list

Ten modules are planned, joined by the B7 cable and nine standard PiicoDev SH-to-SH cables. The user owns enough standard PiicoDev cables for every link. Use the shortest cable that reaches with a little slack for routing and removal; no extra cable purchase is needed. B7 is a separate male breakout cable, CE07796, AU$0.95. Its ownership is unconfirmed, so it stays in the purchase budget.

| ID | From | To | Module location ([11](11-mechanical-design-print-assembly.md)) | Length |
|---|---|---|---|---|
| B7 (W13a–d) | Kitronik `GND` / `3V` / `GP0` / `GP1` | Button A | Rear upright | 200 mm (fixed by the part) |
| C1 | Button A "wake" | Button B "move enable" | Both on the rear upright, right side | Shortest that fits; record |
| C2 | Button B | Atmospheric | Upright near the vents; **mount not modelled in v0.3** | Record |
| C3 | Atmospheric | Accelerometer | Base plate, behind the colour sensor | Record |
| C4 | Accelerometer | Colour | Base plate, front centre, facing down | Record |
| C5 | Colour | Touch | Front shell. **Front-shell disconnect point** | 200 mm planned; confirm by fit |
| C6 | Touch | OLED | Front shell, belly window | Record |
| C7 | OLED | Buzzer | Front shell, right cheek | Record |
| C8 | Buzzer | ToF distance | Front shell, chest | Record |
| C9 | ToF distance | RGB LED | Front shell, left cheek | Record |

To remove the front shell, unplug C5 at either end. Everything from Touch to RGB LED stays plugged together on the shell.

### 6.3 Addresses

Each module on the bus needs a unique I2C address. Only the two Button addresses below are set by this plan. Do not assume addresses for the other kit modules; record each from a scan (§10, [16](16-wire-by-wire-assembly.md) §14).

Each PiicoDev Button has four ID switches. Core's Button guide gives a no-solder method using these switches. Core's driver code computes the address as `8 + id[0] + 2·id[1] + 4·id[2] + 8·id[3]`, and uses the default 0x42 when all four switches are off.

| Button | Role | ID 1 | ID 2 | ID 3 | ID 4 | Address |
|---|---|---|---|---|---|---|
| A | Wake (white plunger, outer) | OFF | OFF | OFF | OFF | **0x42** (default) |
| B | Movement enable (dark plunger, inner) | **ON** | OFF | OFF | OFF | **0x09** |

Button B's address is 0x09, not 0x43. Change ID switches only with the module unpowered, and power-cycle after a change. A scan confirming 0x09 has no clash with another kit module is still pending.

### 6.4 Bus loading and conditioning

These are unresolved and keep the chain on HOLD (WO1, PG6).

- **Module count.** Core's PiicoDev connection guide warns that more than about six modules can overload the bus. Pip plans ten. Having enough cables does not establish bus capacity: each module and each cable adds capacitance and, where fitted, another pull-up resistor.
- **Pull-ups and series resistors.** Core's B7 cable page describes 4.7 kΩ pull-ups and 120 Ω series resistors in its adapters and recommends considering them for direct wiring. Equivalent conditioning at the Kitronik terminals is not documented in the sources checked. Inventory the modules' fitted pull-ups and calculate their parallel resistance before adding more. No solder-free interface has been selected. B19 may change the direct W13 route; update this reference before building it.
- **Pull-up jumpers.** Do not cut module pull-up jumpers to reduce loading. Restoring them needs solder.
- **Speed.** Use 100 kHz for the initial address scan when bring-up is cleared. Core's Unified driver recommends at least 400 kHz for OLED use. Validate the full bus at its intended operating speed; a successful scan does not prove reliable OLED operation.
- **3.3 V load.** The whole chain draws from the `3V` terminal, whose capacity is unknown (PG6).

## 7. Conductor and terminal reference

| Part | Fact | Source |
|---|---|---|
| Wago 221-413 lever connector (B9 × 2) | 3 clamping points, all one common potential. One connector per net: one for BODY_5V, one for BODY_GND. All 3 points on each are used (W2/W4/W6, W3/W5/W7); there is no spare | Wago 221 data sheet |
| Wago 221-413 | Wire range 24–12 AWG; fine-stranded 0.14–4 mm². Strip length **11 mm** | Wago 221 data sheet |
| Wire for W2–W5 (B14) | ~22 AWG stranded copper, red for 5 V and black for GND | BOM. Within the Wago and ADA3628 ranges |
| ADA3628 USB-A terminal adapter (B8) | Screw terminals accept 26–16 AWG. Terminals: VBUS, D+, D−, GND, sleeve. Only VBUS and GND used | Adafruit product page |
| Strip lengths at other ends | ADA3628 and Kitronik terminals: strip to suit each terminal, from the actual part. Do not apply 11 mm to every end | — |
| B7 prototyping cable (CE07796) | Black GND, red 3.3 V, blue SDA, yellow SCL; male pins; 200 mm | Core product page |
| Male pins in Kitronik screw terminals (B7, W8, motor leads) | Secure clamping not confirmed by any source (WO2). No adaptor part is selected | — |
| Servo power pigtail (W6/W7) | Must be a known-rated, pre-terminated ~22 AWG part mating with the servo plug. Not selected (B20, WO3) | BOM |

## 8. Hard-off, charging and programming

![Logical head branch and charging: output 2 to the head via the in-line switch; micro-USB charging only with both outputs unplugged](images/wiring/06-head-and-charge.png)

*Logical diagram.*

- **Hard-off:** unplug both USB-A plugs from the bank. Neither the Kitronik switch nor the camera in-line switch isolates everything.
- **Charging:** the QW01's micro-USB socket is its only input. Unplug both robot USB-A plugs before connecting the charge cable ([05](05-power-budget-charging.md) §6). Neither USB-A socket nor the head's USB-C cable is a charging path.
- **Programming (W17):** unplug both bank outputs and all robot supplies. For initial programming, remove the Pico from the carrier and attach no external loads. Programming while mounted needs the carrier USB power path and attached loads reviewed in the approved bench plan. USB power does not bypass the HOLD.

## 9. Open items before any connection can be cleared

| # | Item | Blocks | Closed by |
|---|---|---|---|
| WO0 | Protected body power design: body fault estimate 3.3–4.1 A exceeds the 2 A port; combined bank limit unknown | Everything on output 1 | [05](05-power-budget-charging.md) §4; PG1, PG3 |
| WO1 | I2C bus capacity and conditioning for ten modules; pull-up budget; solder-free interface for any added resistors (BOM B19, unselected) | W13, C1–C9 | Calculation and design change; PG6 |
| WO2 | Male pins (B7, W8, motor leads) clamping securely in Kitronik screw terminals | W8–W13 | Inspection of the delivered parts (row E5 in [12](12-measurement-calibration-checklist.md)) |
| WO3 | Servo power pigtail: select, rate and price a ~22 AWG pre-terminated part (BOM B20) | W6, W7 | Part selection |
| WO4 | FS90 lead colours and acceptance of a 3.3 V signal | W6–W8 | Delivered servo's documentation; PG2 |
| WO5 | Atmospheric sensor mount (not modelled in v0.3) | C2, C3 | CAD change |
| WO6 | Kitronik `3V` terminal capacity | W13b | PG6 |
| WO7 | Compatible MicroPython and approved diagnostic code with explicit GP0/GP1 setup; full Pip firmware for robot operation | Powered diagnostics / robot functions respectively | [16](16-wire-by-wire-assembly.md) Stage 14; [14](14-illustrated-assembly-guide.md) Stage 16 |

## 10. Checks and troubleshooting

The full checklists are in [16](16-wire-by-wire-assembly.md) §12–15. In summary:

- **Before first power (power off):** visual inspection against §5, a second person's check, photographs, gentle tug test on screw-terminal and lever connections, and continuity checks with a multimeter on the unpowered circuit only.
- **Prerequisites** for powered tests are a protected power design, known connector pinouts and ratings, a selected bus interface and servo harness, approved diagnostic code, and a teacher-reviewed bench plan. WO4 requires identifying the servo leads and establishing the signal specification or an approved method to evaluate it. The actual PG2 supply/signal response test follows those decisions. Measured gates PG2, PG4, PG6, PG7 and the measured parts of PG1 run under that plan. A gate's result is not a prerequisite for running that same test.
- Never use a multimeter's current range across a supply (for example probes on +5V and GND). That is a short circuit through the meter.

A possible future I2C scan is sketched in [16](16-wire-by-wire-assembly.md) §14. It has not been run and is not Pip firmware.

## 11. Sources

- [Kitronik 5331 datasheet](https://core-electronics.com.au/attachments/localcontent/5331-compact-motor-driver-raspberry-pi-pico-datasheet_30137893d1d.pdf): GPIO terminals GP0, GP1, GP27, GP28; Motor 1 on GP2/GP3, Motor 2 on GP6/GP7; `3V` terminal from Pico 3V3 OUT; separate onboard supply for the Pico; terminal current capacity not stated.
- [Core PiicoDev prototyping cable (B7)](https://core-electronics.com.au/piicodev-breakout-cable-200mm.html): colour code; pull-up and series-resistor recommendation for direct wiring.
- [Core PiicoDev connection guide](https://core-electronics.com.au/guides/piicodev/piicodev-connection-guide/): bus overload warning above about six modules.
- [Core PiicoDev Button guide](https://core-electronics.com.au/guides/piicodev-button-getting-started-guide/) and [driver source](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Switch-MicroPython-Module/main/PiicoDev_Switch.py) (lines 39–41): ID-switch addressing.
- [Wago 221-413 data sheet](https://www.mouser.com/datasheet/2/737/Data_Sheet221_413_-1928674.pdf): strip length, wire range, common-potential clamping points.
- [Adafruit 3628](https://www.adafruit.com/product/3628): terminal wire range and terminal functions.
- [Core Unified driver](https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py): default Pico GP8/GP9 configuration, explicit pin arguments and OLED speed recommendation.
- [Raspberry Pi Pico 2 W datasheet](https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf): 3V3 OUT load recommendation. [DFRobot DFR1154 wiki](https://wiki.dfrobot.com/dfr1154/): USB-C power and speaker socket.

## 12. Editing diagrams

Editable SVGs sit beside the PNGs in [images/wiring](images/wiring/). See the [illustration generator](../illustrations/README.md) for the connection data and regeneration command. Keep wire IDs consistent with §5 and [16](16-wire-by-wire-assembly.md).
