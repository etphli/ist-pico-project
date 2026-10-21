# 13 · Engineering review status

Round history:
1. Claude Opus 5.5 produced the v0.1 documentation and CAD. The parent agent reviewed it, corrected the budget framing and control claims, and rebuilt the CAD.
2. **v0.2 (19 October)**, also by Claude Opus 5.5, responds to the review objections listed below.

**Release: design prototype only. Firmware not implemented. Purchases, final printing and electrical assembly: HOLD.**

## Previous review findings

| # | Objection | v0.2 response | Status |
|---|---|---|---|
| 1 | Budget: no recommending a raised cap or staged buying; research cheaper no-solder routes seriously | Re-sourced from Core's live catalogue: the motor board, preassembled camera/mic/amp board, PiicoDev Buttons, lever connectors and short wire replace spools and 10-packs. The v0.2 full concept's priced hardware fell from AU$148.71 (with delivery) to **AU$121.78 before delivery**. The 21 October supplied-speaker correction reduces the current subtotal to AU$116.98. **No compliant full configuration found.** See [08](08-bom-budget-sourcing.md) and [15](15-cost-reduction-options.md). | **Open: HOLD; user decision D1** |
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
7. **Supplied speaker** package and physical mount unconfirmed. The manufacturer package includes one, so the separately priced spare is no longer required. The CAD retains its old spare-speaker envelope until the supplied speaker is measured.
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

## Illustrated guide and viewer review, 21 October

Claude Opus 5.5 at medium reasoning wrote the [illustrated assembly guide](14-illustrated-assembly-guide.md). The main agent, GPT-6.1 Sol, read it against the CAD source, pin plan, power gates, fastener list and test plan, then corrected it. A GPT-6.1 Sol subagent wrote the [section viewer](../cad/viewer/README.md), which the main agent reviewed independently.

The review changed the following:

- Removed provisional viewer wording and clarified how GitHub HTML downloads open locally.
- Added the missing servo tab and horn hardware as unpriced B18. The 15 M3 count covers frame, shells, controller, head and hatch only.
- Removed image-title numbers that conflicted with guide stage numbers. Added provisional caster print settings, clarified that STL files do not contain print settings, and corrected the column orientation wording.
- Kept servo centring behind the electrical hold. A loose camera switch is only an unpowered fit trial, not completed retention.
- Corrected the supplied-speaker purchase. The current priced subtotal is AU$116.98 before extras. [The conditional AU$92.27 option](15-cost-reduction-options.md) still needs button, mounting and cable validation and exceeds the cap.

The review found an additional assembly risk. The [straight insertion-path probe](../cad/check_assembly_paths.py) reproduces collisions against the base: motor drop, 99.90 mm³ at +36 mm; lateral wheel press, 2989.51 mm³ at +11 mm; wheel raised from below, 110.17 mm³ at −14 mm. These are sampled placeholder-geometry paths, not an exhaustive proof that no sequence exists. Stage 5 blocks final base printing until a complete sequence is proved or the base changes. The earlier collision checks only established clearance at assembled positions.

The viewer's final browser script passed 23 checks at 1280 × 800, including changes in the rendered pixels when cuts, direction and caps change. The main agent inspected its desktop quarter cut and 390 × 844 phone layout. Every embedded vertex and triangle index matches the current CAD. See [viewer evidence and limits](../cad/viewer/VERIFICATION.md). Mouse-pan and touch feel, and a downloaded file opened through a local file URL, were not automated.

The guide was rendered from Markdown for review. All eleven linked images loaded and the desktop layout had no horizontal overflow. The main agent read all stages and inspected the labelled CAD images. `python3 scripts/check_docs.py` checks local links, PNG files, BOM maths and viewer freshness. Physical assembly, electrical operation and firmware remain untested. The atmospheric module mount, camera switch holder, servo hardware, insertion sequence, power protection and budget remain open.

The preview update changes display shading and image layout, not the mechanical geometry. The main agent added crease-preserving smooth normals, softer edge lines, larger panels and higher-resolution output. The CAD checks and viewer source hashes still apply to the same geometry.


## Wire-by-wire guide and additional illustrations, 21 October

Claude Opus 5.5 at medium reasoning wrote the expanded [connection reference](04-wiring-pin-plan.md) and [beginner wiring tutorial](16-wire-by-wire-assembly.md). A separate Opus task produced editable diagrams and additional assembly illustrations. GPT-6.1 Sol reviewed the text against manufacturer sources and integrated the material into the existing guide.

The review corrected the following:

- Split each motor's two driver outputs into distinct nets. Joining both outputs together would short the driver.
- Replaced the old approximately 7 mm generic stripping instruction with Wago's specified 11 mm at Wago ends only. Other terminal ends follow their own requirements.
- Confirmed B7 colours, ADA3628 sleeve function, the Button ID-switch method and Core's GP8/GP9 defaults from the makers. Pip instead specifies GP0/GP1.
- Clarified that the two bank branches may share an internal ground. Wi-Fi means no external head-to-body signal ground wire is needed; it does not mean isolated power supplies.
- Withdrew unknown-gauge jumper tails for servo power. A rated compatible preterminated harness is now unselected B20. B10 remains provisional signal-only wiring.
- Added the unresolved ten-module bus load and conditioning as B19 and extended PG6. A 100 kHz address scan does not validate full OLED operation; Core recommends at least 400 kHz for OLED use.
- Separated paper prerequisites from measured bring-up results so a gate does not require its own successful result before it can be run. Initial programming uses the Pico alone, outside the carrier and without external loads. Mounted programming needs the carrier USB power path reviewed.
- Moved the insertion-path print prerequisite ahead of the full-print table. The later Stage 5 STOP must be read and cleared before printing the base.

Unlimited owned standard PiicoDev SH-to-SH cables cover C1–C9 at AU$0. They do not establish ownership of the male breakout, jumpers, USB cables or rated power wire. The priced subtotal stays AU$116.98 because no additional module-cable purchase was previously included. B19 and B20 are unpriced, so the subtotal is still incomplete.

No hardware was connected, powered or tested in this documentation update. Power protection, bus capacity, physical connector fit, atmospheric mount, insertion sequence, firmware and budget remain unresolved.

The illustration task reached a Claude provider rate limit after writing its assets. GPT-6.1 Sol continued from those files, finished the programming diagram and label corrections, and ran the final build and checks. The new set contains six wiring diagrams and thirteen assembly details, including eight renders of the existing CAD. All six wiring diagrams and five code-drawn assembly sheets include editable SVGs; the CAD close-ups regenerate from Python layouts.

Final checks on 21 October: `scripts/illustrations.sh --strict` regenerated all 19 new images and exited 0, with no reported label overlaps or off-canvas labels. `python3 scripts/check_docs.py` passed 22 documents, 293 local links, 27 PNGs, 11 editable SVGs, BOM arithmetic and viewer-source freshness. The separate viewer mesh check passed all 44 entries and every vertex/index. Rendered Markdown for 04, 14 and 16 loaded all 6, 26 and 6 linked images respectively, with no horizontal overflow at 1280 × 800. Python compilation and `git diff --check` passed. The main agent inspected all new illustrations at full size and checked the corrected callouts. These checks do not establish physical fit, electrical operation or firmware behaviour.

The staged Git check caught trailing spaces in Matplotlib-generated SVG path data. The generator now removes them, and the documentation checker detects them before staging. The eleven vector sheets were regenerated with strict checks after that fix; their image content is unchanged.
