# 03 · AI, camera and audio: feasibility and options

**Status: design only. Firmware and bridge software are not implemented. No model API calls were made and no API keys were created in this design round.**

## 1. What "AI" honestly means here

| Capability | On the Pico 2 W alone? | Where it runs |
|---|---|---|
| Spoken conversation | No (RP2350: 520 KB SRAM, 4 MB flash; Raspberry Pi docs) | Cloud LLM via the laptop bridge |
| Person detection and tracking | Not at a useful rate | Laptop (local model), from the robot's camera stream |
| Speech-to-text / text-to-speech | No | Laptop (local first) |
| Control loops, safety, games, UI | **Yes** | Pico |

Suggested wording for school evidence: *"Pip's conversation text comes from a cloud language model reached through a laptop bridge. Pip's camera, microphone and speaker are on the robot. Its movement, control loops and safety run on the Raspberry Pi Pico 2 W."* When the bridge is unavailable Pip says so and plays non-AI games ([02](02-architecture.md) §6).

## 2. Camera, microphone and speaker on the robot (solder-free)

| Option | Camera | Mic | Speaker drive | Price (Core, 2026-10-19) | Verdict |
|---|---|---|---|---|---|
| **DFRobot ESP32-S3 AI Camera DFR1154** (full concept) | OV3660, 2 MP, 160° wide-angle, IR-sensitive with IR LEDs (DFRobot) | PDM mic on board | MAX98357 I2S amp, MX1.25 speaker socket (speaker not listed as included) | 37.23 + speaker 4.80 (out of stock) | Selected: one preassembled board, USB-C powered, 42 × 42 mm fits behind an eye |
| Seeed XIAO ESP32S3 Sense | OV5640 on current Sense boards (Seeed wiki) | digital mic | none: needs a separate speaker module and cable | 30.60 + ≥ 9.51 | Second choice. More parts and more cost. |
| ESP32-CAM-type boards | yes | no | no | not priced | Rejected: no mic |
| Waveshare ESP32-S3 2" display board with camera | yes | not listed | not listed | 30.45 | Rejected: no mic listed |
| Laptop webcam/mic/speaker | — | — | — | 0 | Fails "onboard" (F9). Use only as a temporary software-development fallback, with the user's OK. |
| Spare Android phone as the head (option R3) | phone | phone | phone | 0 if owned | Only if the user owns a spare phone. Needs a head redesign; app behaviour not verified. |

DFR1154 notes:
- **Power:** use the USB-C "5V DC" input ([05](05-power-budget-charging.md)). DFRobot's and Core's VIN ranges conflict (3.7–15 V vs 5–12 V), so VIN is not used.
- **160° lens:** the head's eye aperture keeps a **90° design cone** clear and deliberately masks the outer field (CAD check in `cad/out/validation_report.md` §3c). The bridge must correct the wide-angle lens: map pixel → bearing with a calibration (T-CAM-2), not a linear deg/pixel factor.
- **IR LEDs:** keep them off (firmware). They are not needed indoors and would reflect inside the eye bore.
- **Current draw** is not published. Measure it (gate PG4).

## 3. Web AI provider: OpenRouter (provisional, provider-neutral)

From OpenRouter's documentation, checked 2026-10-19:
- Endpoint `https://openrouter.ai/api/v1/chat/completions`, OpenAI-compatible, `Authorization: Bearer <key>`. The bridge's `LLMClient` takes `base_url`, `model` and the key from configuration, so the provider can be swapped.
- Prepaid USD credit; a 5.5% fee (US$0.80 minimum) when buying credit. Per-key credit limits exist (HTTP 402 when used up). **Set a small limit.**
- Free models have daily request limits and can be withdrawn. Don't rely on them for a demo.

An **adult** creates the account and holds the key on the laptop. "OpenCode" is a coding client, not an API credit source for the bridge.

## 4. Pipeline and cost gates

| Stage | Default (cheapest, most private) | Upgrade only if measured to be needed |
|---|---|---|
| Person tracking | Local on the laptop. Images never leave it. | — |
| Speech-to-text | Local (Whisper-class) | Cloud STT if local fails the accuracy/latency test (G2) |
| Conversation | OpenRouter text model, ≤ 2 short sentences, child-safe system prompt, output filter | Larger model (G3) |
| Text-to-speech | Local voice | Cloud TTS (G2) |
| Turn-taking | Turn-based: Pip does not listen while it is speaking | Barge-in, only after echo is measured not to self-trigger |

| Gate | Pass criterion |
|---|---|
| G0 | Hardware purchase decision made ([08](08-bom-budget-sourcing.md)) |
| G1 | Adult-owned account, per-key credit limit set |
| G2 | Local STT/TTS measured too poor (word errors with children's speech, latency > 3 s, or speech not understood) |
| G3 | Answer quality rated too poor in the evidence log |

Ongoing API cost is **not estimated**. The bridge logs token usage per turn. Report the cost per 10-minute session from those logs.

## 5. Privacy and child safety

- By default no images or raw audio go to the cloud; only transcribed text does. Nothing is recorded by default.
- System prompt: friendly companion for ages 5–8, short answers, never asks for personal details, refers worries to "a grown-up", encourages physical play.
- Laptop-side output filter (blocklist + length limit) and a parent "end session" control.
- Camera-on indicator (RGB LED) and a physical camera/mic switch ([05](05-power-budget-charging.md)).
- Teacher and parent consent before any session that processes a child's image or voice.

## 6. Network notes

- Pico 2 W and ESP32-S3 are 2.4 GHz devices. School networks often block device-to-device traffic. The fallback is the laptop's hotspot.
- Rough bandwidth: QVGA JPEG at 8 fps ≈ 0.5–1.5 Mbit/s, plus ~0.25 Mbit/s each way for audio. Measure it (T-CAM-1).
