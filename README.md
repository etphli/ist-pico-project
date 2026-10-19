<img src="assets/icon.svg" width="64" height="64" alt="">

# Pip: a Pico-powered play companion (IST project)

Pip is a friendly, rounded, white companion robot for children aged 5–8 that encourages **off-screen play**. The design: Pip follows a selected child on four wheels, pans its head to look at them, asks questions on a belly screen, takes answers from touch pads or by voice, and talks through a web AI model reached over Wi-Fi via a nearby laptop. It is built around a **Raspberry Pi Pico 2 WH** and the **PiicoDev Starter Kit**, with **no soldering**.

> **Status (2026-10-19): design v0.2. Design only; firmware not implemented. Purchase status: HOLD.**
> No configuration meeting every requirement within the **AU$70 total** was found. The full concept's priced hardware is AU$121.78 before delivery and unpriced items. Reduced-scope options are listed for the user's decision ([docs/08](docs/08-bom-budget-sourcing.md)). The power design has verification gates that must pass before wiring ([docs/05](docs/05-power-budget-charging.md)). The CAD is a parametric prototype with placeholder dimensions for bought parts. Review status: [docs/13](docs/13-design-review.md).

![Pip CAD v0.2 reference elevations](cad/out/preview_front_reference.png)

## Key facts

- **Full concept (over budget, comparison only):**
  - Body: Pico 2 WH on a Kitronik 5331 motor board (DRV8833, with protection stated by Kitronik), 2 TT motors + 2 printed casters, FS90 head servo in a slip-clutch neck.
  - Head: DFRobot ESP32-S3 camera board with mic and speaker amplifier.
  - Rear buttons: two PiicoDev Buttons (wake, movement enable).
  - Display: kit OLED in the belly. Power: USB power bank behind a rear charge door.
- **Closed loops:** camera head tracking, body-yaw assist, ToF follow distance (gated by target selection, freshness, alignment and range plausibility, with a 350 mm stop), tilt-stop heuristic, quiz adaptation ([docs/02](docs/02-architecture.md)).
- **Not claimed:** motor-stall detection, reliable lift detection, edge detection, automatic reversing. Supervised floor use only ([docs/06](docs/06-safety.md)).
- **AI split:** the Pico runs control and safety. The laptop runs tracking and speech locally and calls an LLM on OpenRouter (provider-neutral). No API calls were made and no keys exist in this repo.

## Documentation

| # | Document |
|---|---|
| 00 | [Status, assumptions, decisions](docs/00-status-assumptions-decisions.md) |
| 01 | [Requirements and traceability](docs/01-requirements.md) |
| 02 | [Architecture, closed loops, safety supervisor, interfaces](docs/02-architecture.md) |
| 03 | [AI / camera / audio options](docs/03-ai-camera-audio-feasibility.md) |
| 04 | [Wiring and pin plan (solder-free)](docs/04-wiring-pin-plan.md) |
| 05 | [Power topology, ratings, protection, gates, charging](docs/05-power-budget-charging.md) |
| 06 | [Safety plan (supervised prototype)](docs/06-safety.md) |
| 07 | [Activities and UX](docs/07-activities-ux.md) |
| 08 | [BOM, budget, sourcing, reduced-scope options](docs/08-bom-budget-sourcing.md) · [bom.csv](docs/bom.csv) |
| 09 | [Build plan, milestones, tests](docs/09-build-plan-milestones-tests.md) |
| 10 | [School evidence prompts](docs/10-school-evidence-rubric.md) |
| 11 | [Mechanical design, retention, print and assembly](docs/11-mechanical-design-print-assembly.md) |
| 12 | [Measurement and calibration checklist](docs/12-measurement-calibration-checklist.md) |
| 13 | [Engineering review status](docs/13-design-review.md) |
| — | [Sources](docs/sources.md) |

## CAD

```bash
scripts/cad.sh              # build, check, render (~3 min)
scripts/cad.sh --no-render  # build and check only (seconds)
```

See [cad/README.md](cad/README.md). STLs: `cad/out/stl/`. Check results: `cad/out/validation_report.md`.
