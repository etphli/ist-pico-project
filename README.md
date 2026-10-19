<img src="assets/icon.svg" width="64" height="64" alt="">

# Pip: a Pico-powered play companion (IST project)

Pip is a friendly, rounded, white companion robot for children aged 5–8 that encourages **off-screen play**. The proposed robot follows a selected person, pans its head to look at them, asks questions on a small belly screen, takes answers from touch pads or by voice, and talks through a web AI model reached over Wi-Fi via a nearby laptop. It is built around a **Raspberry Pi Pico 2 WH** and the **PiicoDev Starter Kit**, with **no soldering**.

> **Status (2026-10-19): provisional design v0.1.** No hardware has been bought, printed or tested. CAD geometry checks have been run. The CAD is a **parametric prototype with placeholder dimensions for bought parts**. Firmware and the laptop bridge are not implemented. **Purchase status: HOLD.** The power topology is unresolved; see [review findings](docs/13-design-review.md). Open decisions, including a **budget shortfall**, are listed in [docs/00](docs/00-status-assumptions-decisions.md).

![Pip CAD v0.1 preview](cad/out/preview_assembly.png)

## Key facts

- **Closed loops:** camera-based head tracking, body-yaw assist, ToF follow distance, tilt detection, motion watchdog, conversational barge-in, adaptive quiz ([docs/02](docs/02-architecture.md)).
- **AI split:** the Pico runs control and safety. A laptop bridge runs person tracking and speech locally and calls an LLM on **OpenRouter** (provisional, provider-neutral). Pip says honestly when it is offline and plays non-AI games instead ([docs/03](docs/03-ai-camera-audio-feasibility.md)).
- **Hardware added to the owned Pico + kit:** Cytron Robo Pico carrier, 2 TT gearmotors, FS90 servo, XIAO ESP32S3 Sense (camera + mic), Gravity speaker, USB power bank, and plug-in power adapters.
- **Budget:** the full solder-free build is **≈ AU$148.71 at Core Electronics (incl. delivery) + a power bank**. That is **over the AU$70 ceiling**. This is an incomplete concept estimate, not a working or budget-compliant build. Alternatives and missing costs are recorded in [docs/08](docs/08-bom-budget-sourcing.md).

## Documentation

| # | Document |
|---|---|
| 00 | [Status, assumptions, open decisions](docs/00-status-assumptions-decisions.md) |
| 01 | [Requirements and traceability](docs/01-requirements.md) |
| 02 | [Architecture, closed loops, interfaces](docs/02-architecture.md) |
| 03 | [AI / camera / audio feasibility and cost gates](docs/03-ai-camera-audio-feasibility.md) |
| 04 | [Wiring and pin plan (solder-free)](docs/04-wiring-pin-plan.md) |
| 05 | [Power budget, charging and interlock](docs/05-power-budget-charging.md) |
| 06 | [Safety plan (supervised prototype, not a certified toy)](docs/06-safety.md) |
| 07 | [Activities and UX](docs/07-activities-ux.md) |
| 08 | [BOM, budget and sourcing](docs/08-bom-budget-sourcing.md) · [bom.csv](docs/bom.csv) |
| 09 | [Build plan, milestones, tests, evaluation](docs/09-build-plan-milestones-tests.md) |
| 10 | [School evidence prompts](docs/10-school-evidence-rubric.md) |
| 11 | [Mechanical design, print and assembly plan](docs/11-mechanical-design-print-assembly.md) |
| 12 | [Measurement and calibration checklist](docs/12-measurement-calibration-checklist.md) |
| 13 | [Engineering review and blocking findings](docs/13-design-review.md) |
| — | [Sources with access date and verification status](docs/sources.md) |

## CAD

Parametric Python CAD (manifold3d). To rebuild the STLs, checks and previews:

```bash
scripts/cad.sh
```

See [cad/README.md](cad/README.md). Printable STLs are in `cad/out/stl/`, and the check results are in `cad/out/validation_report.md`.
