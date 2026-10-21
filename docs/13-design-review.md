# 13 · Engineering review status

Round history:
1. Claude Opus 5.5 produced the v0.1 documentation and CAD. The parent agent reviewed it, corrected the budget framing and control claims, and rebuilt the CAD.
2. **v0.2 (19 October)**, also by Claude Opus 5.5, responds to the review objections listed below.

**Release: design prototype only. Firmware not implemented. Purchases, final printing and electrical assembly: HOLD.**

## Previous review findings

| # | Objection | v0.2 response | Status |
|---|---|---|---|
| 1 | Budget: no recommending a raised cap or staged buying; research cheaper no-solder routes seriously | Re-sourced from Core's live catalogue: the motor board, preassembled camera/mic/amp board, PiicoDev Buttons, lever connectors and short wire replace spools and 10-packs. The full concept's priced hardware fell from AU$148.71 (with delivery) to **AU$121.78 before delivery**. It is still over. **No compliant full configuration found.** Reduced scopes are listed only as options needing acceptance ([08](08-bom-budget-sourcing.md) §4). | **Open: HOLD; user decision D1** |
| 2a | Servo at 4.6 V below the FS90's 4.8 V minimum | Cytron's own table shows Vservo = VIN on VIN-only supply, so the 4.6 V figure was wrong. Regardless, the topology changed: the servo is fed from the bank's 5 V nominal. The ~0.2 V margin is a **gate** (PG2 ≥ 4.8 V measured). Failing it means the servo stays disconnected, not that it is run out of rating. | **Open: gate PG2**. No lower-voltage servo with a manufacturer rating found. |
| 2b | XIAO USB fed 4.6 V | The camera board is now powered by an ordinary USB cable from a bank port, through an in-line switch | Resolved in design; PG4 records it |
| 2c | Stall current vs bank rating; PWM and sensors are not protection | Driver with stated over-current and thermal protection (DRV8833, Kitronik). Example motor stall figures approach the board's stated maximum; continuous limits and motor protection remain unresolved. Bank protection must be documented but cannot substitute for a motor-protection strategy (PG3). No firmware stall detection is claimed. | **Open:** bank protection unverified; servo branch has no hardware current limit |
| 2d | No auto-reverse; accelerometer heuristic; supervised floor only | Written into [02](02-architecture.md) §4–5 and [06](06-safety.md) | Resolved in documents |
| 2e | ToF ≠ person range; alignment, validity, stop threshold, target selection and loss timeout; commanded vs actual head angle | [02](02-architecture.md) §4.1–4.2 | Resolved in documents; thresholds untested |
| 2f | Local watchdog independent of audio and network | 0.2 s motor-command expiry, hardware watchdog, 500 ms heartbeat. Audio moved off the Pico. | Resolved in design; T-SAF-3 under load |
| 3 | Preview showed red triangulated "openings"; check apertures, FOV, retention | Renderer replaced with a per-pixel z-buffer, which shows through-openings truthfully. The mesh was unchanged by the render fix. Added front/rear reference elevations, true cross-sections and a camera FOV-cone check. Retention: base–column–deck screwed frame; shell screws moved under the base (the v0.1 roof screws were unreachable under the head); eyes now inserted from inside and backed by a frame. Screws listed and unpriced. | Resolved in CAD; physical retention untested |
| 4 | "Ready to order" wording; interim USB-motor-power claims | Removed. The Robo Pico USB path is no longer used. | Resolved |
| 5 | Wording; manufacturer sources; no API calls | Status lines simplified. Technical facts are from manufacturer documents where obtainable (Cytron, Kitronik, DFRobot, Seeed, Raspberry Pi). Retailer-only facts are marked. No API calls; no secrets. | Resolved; Feetech and Adafruit manufacturer pages not checked (marked in sources) |
| 6 | Bed-fit comparison; candid geometry limits | `fits_bed()` compares sorted dimensions elementwise, with a self-test including the lexicographic trap. Report §5 lists what the checks do not establish. Motion checks are labelled as samples. | Resolved |

## Still unresolved (blocking purchase)

1. **Budget** (D1): over the cap.
2. **Power bank** owned: MINISO QW01, approximate 130 × 60 × 10 mm; two USB-A outputs each reported 5 V / 2 A. Combined output, protection, low-load behaviour and fit are unverified (PG1, PG3). The v0.3 mechanical revision addresses the earlier footprint/frame clash; actual bank fit is still untested.
3. **Servo voltage margin** (PG2) and **no servo-branch current limit**.
4. **Kitronik regulator capacity** for the Pico 2 W plus 10 PiicoDev modules is not published (PG6).
5. **Single master disconnect** not found solder-free (PG5). Interim: unplug both leads.
6. **Charging interlock**: procedural only.
7. **Speaker** out of stock; plug fit to the DFR1154 socket unconfirmed.
8. Unpriced items: wire, screws, strap, O-rings, delivery for the full cart. Owned bank is AU$0 if compatible.
9. All bought-part dimensions are placeholders ([12](12-measurement-calibration-checklist.md)).

## What the CAD checks do and do not establish

See `cad/out/validation_report.md` §5. In short: mesh validity, bed fit (bounding box), overlaps above 1 mm³ outside listed contact pairs (each listed with its volume and reason), selected gaps, **sampled** caster/head motion, and a geometric FOV cone. Not established: real fit, continuous motion clearance, cable routing, fastener strength, printability, toy compliance, real camera field of view.

## Work possible now at AU$0

Kit-only stationary closed loops (option R0): ToF distance → OLED/LED/buzzer, touch → feedback, tilt → alarm, with logged setpoint, measurement and output. This builds assignment evidence. It does not replace the requested robot.

Parent review of v0.2: confirmed Cytron VIN-only servo-rail correction against its datasheet. Removed the proposed hand-held and sustained-stall tests because protection and motor thermal limits remain unknown. PG3 stays blocked pending documented limits and a guarded current-limited test plan. CAD rebuild, local Markdown links and full-concept BOM arithmetic checked.

## v0.3 QW01 revision, 2026-10-21

The user requested the complete design be updated around the owned bank and pushed to main. The model is MINISO QW01, 10,000 mAh, approximately 130 × 60 × 10 mm. Charging is micro-USB; the two USB-A outputs are each reported as 5 V / 2 A. Shared simultaneous capacity is unknown. These remain user-reported values, not a manufacturer-certified envelope.

The mechanical revision replaces the older bank placeholder and must eliminate the previously reproduced tray and frame-column clashes, provide retention and actual unplugging/charging access, and regenerate the STL and preview set. See the generated report for the modelled accommodation envelope and its checks. Exact measurements and a physical fit test remain required.

The electrical documentation now uses 2 A per port as the reported limit and removes the earlier generic 2.1 A acceptance threshold. Acceptance depends on a load budget and protection within the actual limits. The existing body-branch fault estimate of 3.3–4.1 A exceeds the reported 2 A rating; the bank cannot yet be cleared for that circuit. No limiter, replacement motor or all-branch master switch has been selected or added to the BOM. The two outputs must not be paralleled.

The AU$70 total cap, no-soldering requirement and requested functions remain unchanged. The historical comparison BOM remains over budget. A mechanically updated prototype is not a purchase-ready or electrically validated robot.

Parent verification of v0.3: `scripts/cad.sh --no-render` and `scripts/cad.sh --bank-fit-only` passed. The legacy bank/column collision is detected while the new accommodation envelope clears the model. Fixed cavity bounds are independent of the nominal measured size: a 132 × 61 × 12 mm variant passed with resized fillers, while a 20 mm-thick variant was rejected. The full generated set contains 28 STL files, six preview PNGs, assembly metadata and the bank-fit report. Physical fit, strength and electrical operation remain untested.
