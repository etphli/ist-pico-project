# Sources (accessed 2026-10-19)

Type: **M** = manufacturer document (used for technical facts); **R** = retailer live page (used for price/stock, and for technical facts only where marked "retailer only"); **S** = search-engine extract (not relied on for decisions).
Status: **V** = read directly that day; **X** = could not be fetched.

## Technical (manufacturer)

| # | Source | Used for | Type/Status |
|---|---|---|---|
| 1 | Cytron, Robo Pico datasheet Rev 1.0 (DigiKey-hosted PDF): https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/6147/Robo_Pico.pdf | VIN 3.6–6 V; **Vmotor & Vservo = VIN with only VIN connected** (row 6), VUSB − 0.4 V on USB (rows 5, 7, 8); 1 A continuous / 1.5 A peak < 5 s per channel; no driver protection stated | M/V (PDF text) |
| 2 | Kitronik, Compact Motor Driver Board for Pico 5331 datasheet (Core-hosted): https://core-electronics.com.au/attachments/localcontent/5331-compact-motor-driver-raspberry-pi-pico-datasheet_30137893d1d.pdf | DRV8833 with built-in short-circuit, over-current and thermal protection; 3–10 V; 1.5 A max per channel; motor pins GP2/3, GP6/7; GPO terminals GP0, GP1, GP27, GP28; 3V/GND out; reverse-polarity protected power; on/off switch; 3 V regulator powers the Pico; 63 × 35 mm, 11.6 mm tall, M3-clearance holes | M/V (PDF text) |
| 3 | DFRobot wiki, ESP32-S3 AI CAM DFR1154: https://wiki.dfrobot.com/SKU_DFR1154_ESP32_S3_AI_CAM | 42 × 42 mm; Type-C 5 V; VIN 3.7–15 V (conflicts with Core's 5–12 V; VIN not used); OV3660 160°; PDM mic; MAX98357; MX1.25 speaker socket; recommended speaker 4 Ω 1.5 W or 8 Ω 1 W; package list not given | M/V |
| 4 | Seeed wiki, XIAO ESP32S3 getting started: https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/ | Type-C input 5 V; Sense streaming ≈ 140 mA average, ≈ 347 mA peak at 5 V; OV5640 on current Sense | M/V |
| 5 | Raspberry Pi, Pico-series documentation and Pico 2 W datasheet | RP2350 520 KB SRAM, 4 MB flash, 150 MHz; 2.4 GHz radio; 3V3 load < 300 mA recommended | M/V (previous round) |
| 6 | PiicoDev LiPo Expansion Board schematic (CoreElectronics GitHub) | Charger only; no motor/servo supply | M/V (previous round) |
| 7 | Core Electronics guide, Makerverse Motor Driver 2-channel application guide | Terminals and headers fit **unsoldered pads**, hence rejected | M (Core is the maker)/V |
| 8 | OpenRouter docs: quickstart, FAQ, limits | Endpoint, auth, credit fee 5.5% (US$0.80 min), per-key limits/HTTP 402, free-model limits | M/V (previous round) |

## Price, stock and retailer-only technical facts (Core Electronics live catalogue)

| # | Page | Used for | Type/Status |
|---|---|---|---|
| 10 | Kitronik Motor Driver Board CE07855 | AU$19.95; in stock (3 today) | R/V |
| 11 | TT motor ADA3777 | AU$7.35; 3–6 V; 28 AWG leads; Adafruit bench figures: stall 1.1 A at 3 V, 1.2 A at 4.5 V, 1.5 A at 6 V (**retailer copy of Adafruit's text; Adafruit page not checked**) | R/V |
| 12 | Feetech FS90 CE09376 | AU$5.70; **4.8–6 V; 800 mA stall (retailer only; Feetech page not checked)** | R/V |
| 13 | DFR1154 | AU$37.23; in stock (16) | R/V |
| 14 | Mini Oval Speaker ADA3923 | AU$4.80; **out of stock**; PicoBlade 1.25 mm plug; 30 × 20 × 5 mm | R/V |
| 15 | PiicoDev Button CE08500 | AU$8.05; I2C 0x42 default, user-selectable; 25.4 mm; 2 × M2.5 | R/V (Core is the maker) |
| 16 | USB-A male → terminal ADA3628 | AU$9.65; no soldering | R/V |
| 17 | USB-C in-line power switch CE06575 | AU$3.45; power pins only; not with smart USB-C chargers; ≤ 3 A; 28 cm | R/V |
| 18 | USB-A → USB-C 50 cm CE09370 | AU$3.25; 2 A | R/V |
| 19 | Catalogue search results (generated from the live catalogue): PiicoDev prototyping cable CE07796 AU$0.95; Wago 221-413 AU$1.40; jumper 10 cm M/M CE09607 AU$3.20; PTC COM-08357 (RXE025, 250 mA) AU$2.95; Battery Bank 5000 mAh AD0505B AU$26.95 (one 2.1 A output) | Prices | R/V |
| 20 | Robo Pico CE11203 | AU$27.90, out of stock; Core lists Pico 2 compatibility | R/V |
| 21 | Makerverse 2-ch driver CE08038; TT 50 RPM CE09390 | Rejected options (solder pads; 3 V rating) | R/V |
| 22 | Core cart quotes (example postcode 2000) | Standard delivery AU$6.25 for two smaller test carts. The full-concept cart could not be quoted: Core stopped responding later that day. | R/V |
| 23 | Search extracts: Kitronik Mini 180 servo, Feetech FT90B voltage listings (conflicting), Kitronik Robotics Board prices | Not relied on | S |

## Not checked this round

Feetech and Adafruit manufacturer pages (the servo and motor facts above are retailer copies); TI DRV8833 datasheet (over-current threshold), whose download failed; Kitronik 3 V regulator current rating, not stated in its datasheet; DFR1154 current draw and lens position; PiicoDev Button address-change method; any power bank; element14/Cytron/marketplace prices; OpenRouter terms beyond the facts above.

## Previous-round sources still referenced

Kit contents (Core CE08256 page), PiicoDev OLED dimensions (CE07911), XIAO and Gravity speaker listings (now comparison only). See git history of this file.

## Owned power bank, user report 2026-10-20

MINISO QW01, 10,000 mAh, approximately 130 × 60 × 10 mm; micro-USB charging input, two wide rectangular USB-A output sockets. The user reports 5 V / 2 A **each**. These are transcribed reports, not independently read label values. Combined simultaneous output, mass and protection behaviour are not established. A bounded manufacturer-document search did not find an exact QW01 datasheet; specifications from other MINISO models were not substituted.
