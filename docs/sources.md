# Sources (accessed 2026-10-19)

Verification status:
- **V** = read directly from the page or document that day.
- **S** = taken from a search-engine extract of the page (may be stale).
- **X** = page could not be fetched (blocked or timed out), so the value is unverified.

| # | Source | Used for | Status |
|---|---|---|---|
| 1 | Core Electronics, PiicoDev Starter Kit for Raspberry Pi Pico (CE08256): https://core-electronics.com.au/piicodev-starter-kit-for-raspberry-pi-pico.html | Kit v1.2 contents, version history, AU$86.50 | V |
| 2 | Core Electronics, PiicoDev LiPo Expansion Board (CE07693): https://core-electronics.com.au/piicodev-lipo-expansion-board-for-raspberry-pi-pico.html | ~220/440 mA charge, JST-PH, I2C0 GP8/GP9, 120 Ω, 51×51 mm | V |
| 3 | PiicoDev LiPo Expansion Board schematic Rev v11 (CoreElectronics GitHub, `Documents/schematic.pdf`) | P-MOSFET power path, charger PROG network, FAST_CHG jumper | V (PDF read) |
| 4 | Raspberry Pi, Pico-series documentation: https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html | Pico 2 W: RP2350, 520 KB SRAM, 4 MB flash, 150 MHz, CYW43439, 2.4 GHz n | V (page also shows a conflicting dual-band line) |
| 5 | Raspberry Pi, Pico 2 W datasheet: https://datasheets.raspberrypi.com/picow/pico-2-w-datasheet.pdf | VSYS 1.8–5.5 V; 3V3 load < 300 mA recommended; VBUS→VSYS Schottky; WL_GPIO2 VBUS sense; GPIO29 VSYS/3 | V (PDF text extracted) |
| 6 | Cytron, Robo Pico datasheet Rev 1.0 (Apr 2023), DigiKey-hosted PDF: https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6147/Robo_Pico.pdf | Pin map, VIN 3.6–6 V, Vmotor/Vservo table, 1 A/1.5 A per channel, 300 mA 3V3, switch, buttons GP20/21 | V (PDF text extracted) |
| 7 | Core Electronics, Robo Pico (CE11203): https://core-electronics.com.au/robo-pico-simplifying-robotics-with-raspberry-pi-pico-pico-w.html | AU$27.90, out of stock, 88×72 mm, Maker Port = PiicoDev compatible, included items | V |
| 8 | Pakronics, Robo Pico: https://www.pakronics.com.au/products/robo-pico-simplifying-robotics-with-raspberry-pi-pico-pico-w-pakr-a0558 | A$26.22, out of stock | V |
| 9 | element14 AU, Robo Pico 4415368: https://au.element14.com/cytron/robo-pico/robo-pico-board-rpi-pico-pico/dp/4415368 | AU$17.73 inc GST | S / X (fetch timed out) |
| 10 | Core Electronics, TT gearmotor ADA3777: https://core-electronics.com.au/dc-gearbox-motor-tt-motor-200rpm-3-to-6vdc.html | AU$7.35; pre-fitted 200 mm leads; 150 mA no-load; 1.1–1.5 A stall; 70×22×18 mm; 30.6 g | V |
| 11 | Core Electronics, Feetech FS90 CE09376: https://core-electronics.com.au/feetech-fs90-1-5kgcm-micro-servo-9g.html | AU$5.70; 4.8–6 V; 800 mA stall; 22.5×12.1×22.4 mm | V |
| 12 | Core Electronics, Micro Servo SG92R ADA169: https://core-electronics.com.au/micro-servo.html | Alternative servo AU$12.75 | V |
| 13 | Core Electronics, XIAO ESP32S3 Sense SS113991115: https://core-electronics.com.au/seeed-studio-xiao-esp32s3-54467.html | AU$30.60; lead time; currents; size | V |
| 14 | Pakronics, XIAO ESP32S3 Sense pre-soldered: https://www.pakronics.com.au/products/seeed-studio-xiao-esp32s3-sense-pre-soldered-ss102010635 | A$32.99 | S |
| 15 | Core Electronics, Gravity Digital Speaker FIT0449: https://core-electronics.com.au/gravity-digital-speaker-module.html | AU$9.51; module only listed | V |
| 16 | DFRobot wiki FIT0449: https://wiki.dfrobot.com/fit0449/ | 2.0–5.5 V, 0.5 W 8 Ω, 40×40 mm, GND/VCC/Signal | V |
| 17 | Core Electronics, Gravity digital cable 10-pack FIT0756: https://core-electronics.com.au/gravity-digital-sensor-cable-for-arduino-50cm-10-pack.html | AU$11.60 | S |
| 18 | Core Electronics, USB-A male → terminal ADA3628: https://core-electronics.com.au/usb-a-male-plug-to-5-pin-terminal-block.html | AU$9.65, no soldering | V |
| 19 | Core Electronics, USB-A female → terminal ADA3629: https://core-electronics.com.au/usb-a-female-socket-to-5-pin-terminal-block.html | AU$9.65, lead time | V |
| 20 | Core Electronics, 50 cm USB-A→C CE09370: https://core-electronics.com.au/50cm-usb-a-usb-c-cable.html | AU$3.25 | S |
| 21 | Core Electronics, jumper M/F 40 CE09130: https://core-electronics.com.au/male-female-jumper-wire-40-20cm.html | AU$3.95; delivery "Standard from $7, Express from $11" | S |
| 22 | Core Electronics, jumper M/M 40 CE08574: https://core-electronics.com.au/jumper-wire-20cm-ribbon-of-40pcs.html | AU$3.95 (not in the final BOM) | S |
| 23 | Core Electronics, 22 AWG hook-up wire red PRT-08865 / black PRT-08867 | AU$7.80 / AU$7.40 | S |
| 24 | Core Electronics, PiicoDev OLED CE07911: https://core-electronics.com.au/piicodev-oled-display-module-128x64-ssd1306.html | 25.4×25.4 mm, glass 27×19.5, active 23×11, 0x3C/0x3D | S |
| 25 | Core Electronics, PiicoDev Button CE08500: https://core-electronics.com.au/piicodev-button.html | AU$8.05 (considered, not used) | S |
| 26 | Core Electronics, LiPo 2000 mAh CE04378 | AU$14.45, protection, leads rated 1 A (option B only) | S |
| 27 | Little Bird Electronics, L298N board; DRV8833 carrier listings | Rejected drivers (soldering / voltage drop) | S |
| 28 | Kmart, 10000 mAh USB-A & C 20 W power bank 43277094: https://www.kmart.com.au/product/portable-charger-10000mah-usba-and-c-20w-43277094 | AU$14.50 ("was $39") | S / X (page blocked) |
| 29 | OpenRouter Quickstart: https://openrouter.ai/docs/quickstart | Endpoint, Bearer auth, OpenAI-compatible | V |
| 30 | OpenRouter FAQ: https://openrouter.ai/docs/faq | USD credits, 5.5% (min $0.80) fee, free-model limits 50/1000 per day, no logging by default | V |
| 31 | OpenRouter audio guide: https://openrouter.ai/docs/guides/overview/multimodal/audio | `input_audio`, audio output needs streaming | V |
| 32 | OpenRouter limits / key docs: https://openrouter.ai/docs/api/reference/limits | Per-key credit limit, HTTP 402 | S |
| 33 | Reference image (user attachment) | Visual style only: rounded white upright companion, dark eyes. Not copied. | inspected |

Not checked this round: OpenRouter Terms of Service (age, child-directed use); OpenCode plan terms; AS/NZS toy standards text; PiicoDev module default I2C addresses (except the OLED); Robo Pico charge current and JST-PH polarity; Pico 2 W compatibility statement for the Robo Pico.

Parent review 2026-10-19: Seeed XIAO getting-started documentation https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/ and Waveshare combined camera/audio documentation https://docs.waveshare.com/ESP32-S3-CAM-OVxxxx were read. The latter is an unpriced alternative candidate only.
