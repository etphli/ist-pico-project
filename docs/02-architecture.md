# 02 · System architecture, closed loops and interfaces

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

Provisional, design only. **No firmware or bridge software has been written.** Power and protection are unresolved; see [review findings](13-design-review.md). This document fixes the responsibilities and interfaces so that work can start later without re-deciding them.

## 1. Block diagram

```
                       Wi-Fi 2.4 GHz (same LAN, or the laptop's hotspot)
   ┌──────────────────────── ROBOT "Pip" ─────────────────────────┐        ┌──────────── LAPTOP "Pip Bridge" ────────────┐
   │                                                               │        │                                              │
   │  HEAD (rotates)                                               │        │  video in  → person detector (local)          │
   │  XIAO ESP32S3 Sense ── camera (JPEG frames) ─────────────────────────► │            → bearing + size of target        │
   │                     └─ PDM mic (16 kHz PCM) ─────────────────────────► │  audio in  → VAD → speech-to-text (local*)    │
   │        ▲ 5 V (switched) via USB-C                              │        │            → dialogue manager + safety filter │
   │        │                                                       │        │            → OpenRouter LLM (text, HTTPS) ───┼──► Internet
   │  BODY                                                         │        │  reply     → text-to-speech (local*)          │
   │  Pico 2 W on Cytron Robo Pico                                 │        │            → audio stream ─────────┐          │
   │   ├ motors L/R (TT) ← Robo Pico H-bridges                     │        │  targets/behaviour cmds ──────────┐│          │
   │   ├ head servo FS90 (servo port 1)                            │ ◄──────┼───────────────────────────────────┘│          │
   │   ├ speaker (Gravity 8002 amp, PWM audio) ◄───────────────────┼────────┼────────────────────────────────────┘          │
   │   ├ I2C chain: OLED, touch, ToF distance, RGB LEDs, buzzer,    │        │  API key lives ONLY here (never on the robot) │
   │   │            accelerometer, colour (floor), atmospheric      │        │  * cloud STT/TTS optional, cost + privacy gate│
   │   ├ rear buttons GP20 (wake) / GP21 (move enable), NeoPixel    │        └──────────────────────────────────────────────┘
   │   └ SAFETY SUPERVISOR (always local, never waits on Wi-Fi)    │
   │  Power: USB power bank → Robo Pico VIN → switch → everything   │
   └───────────────────────────────────────────────────────────────┘
```

## 2. Who does what

| Unit | Runs | Responsibilities | Must keep working when Wi-Fi drops? |
|---|---|---|---|
| **Pico 2 W** (body) | MicroPython (C++ if audio playback needs it) | Motor and servo control, safety supervisor, sensors, OLED, touch, LEDs, buzzer, speaker playback, behaviour state machine, offline games, link to the bridge | **Yes.** Stops motion safely, then offers offline mode. |
| **XIAO ESP32S3 Sense** (head) | Arduino or ESP-IDF (MicroPython optional) | Captures camera frames and mic audio and streams them to the bridge. Obeys "camera on/off" commands. Indicator state is reported to the Pico. | It just stops streaming |
| **Laptop bridge** | Python 3.11+ | Person detection and tracking, voice activity detection, speech-to-text, LLM calls, safety filtering, text-to-speech, activity scripts, logging for evidence | n/a |
| **OpenRouter / LLM** | cloud | Generates the conversation text from a child-safe system prompt | n/a |

Why the split: the RP2350 on the Pico 2 W has **520 KB SRAM, 4 MB flash and runs at up to 150 MHz** (Raspberry Pi product documentation). That is plenty for control loops. It **cannot** run a modern chat model, and it cannot run reliable person detection at a usable frame rate. That is the job of the laptop and the cloud model ([03](03-ai-camera-audio-feasibility.md)).

## 3. Behaviour state machine (Pico)

```
            switch ON
 OFF ───────────────────► BOOT ──► SLEEP ◄──────────── long-press A (2 s) / 10 min idle
  ▲ switch OFF                        │ short-press A (wake)
  │ (charge door open)                ▼
  │                                 AWAKE_STILL  ── talk, quiz, head tracking, NO wheel motion
  │                                   │ press B (movement enable) + safety checks pass
  │                                   ▼
  │                                 AWAKE_MOVING ── follow, games with motion
  │                                   │ press B again / enable timeout (5 min) / lift / tilt /
  │                                   │ link loss while bridge-driven / fault
  │                                   ▼
  └──────────────────────────────── FAULT_STOP (motors coast→brake, servo holds, OLED shows why)
                                      │ press B after cause cleared → AWAKE_STILL
```

Rules:
- Wheel motion is only possible in **AWAKE_MOVING**. The movement-enable flag is **cleared on every boot and every wake**, so a child has to press button B on purpose each time.
- In SLEEP the camera is switched off (command to the XIAO), the OLED blanks, the servo is detached and the motors are off. The camera **hardware** is only powered off by the main switch ([05](05-power-budget-charging.md)).
- NeoPixel/RGB "camera on" indicator: lit whenever the XIAO reports that it is streaming.

## 4. Closed loops (the assignment's core)

All loops log `t, setpoint, measurement, output` to the bridge (or to Pico flash in offline mode) so they can be graphed as evidence. Starting gains are shown, but **all gains are placeholders to tune and record**.

| # | Loop | Sensor → controller → actuator | Control law (start) | Rate | Feedback evidence |
|---|---|---|---|---|---|
| L1 | **Head tracking** | camera → laptop detector gives bearing error e (deg) → Pico → servo | P (+ small I): θ += Kp·e, Kp≈0.4; deadband ±3°; slew ≤ 90°/s | 5–15 Hz (frame rate) | e(t) converging; overshoot |
| L2 | **Body yaw assist** | commanded head angle θ (estimated, not encoder feedback) → Pico → differential wheel speeds | If abs(θ) > 35°: turn the body toward θ while L1 counter-rotates the head | 20 Hz | θ returns inside ±15° |
| L3 | **Follow distance** | ToF distance d → Pico → forward speed v | v = Kp·(d − 0.6 m), clamp 0…0.25 m/s, deadband ±5 cm; v = 0 when the target is lost | 20–30 Hz | d(t) settling near 0.6 m |
| L4 | **Tilt / lift safety** | accelerometer → Pico → motors | Tilt > 25° for 100 ms, or an abnormal acceleration event → FAULT_STOP | 50–100 Hz | stop latency |
| L5 | **Motion anomaly heuristic, not stall protection** | commanded speed vs. accelerometer motion + ToF change → motors | Unexpected acceleration or range behaviour → stop only. No automatic reverse without rear clearance sensing. Constant speed and slow lift are not reliably detectable. | 20 Hz | stall-to-stop time |
| L6 | **Link watchdog** | bridge heartbeat → Pico → motors | No heartbeat for 500 ms while a bridge-driven motion is running → stop | 10 Hz | — |
| L7 | **Turn-taking (barge-in)** | mic VAD → bridge → speaker stream | When the child starts speaking, Pip stops talking within 300 ms | 50 Hz audio frames | latency |
| L8 | **Quiz adaptation** | touch answer → bridge/Pico → next question level | Two right in a row → harder; two wrong → easier + hint | per question | accuracy trend |
| L9 | **Colour-card game** | colour sensor (floor) → Pico → speech, LEDs, wheel "dance" | Hue classification with hysteresis | 10 Hz | correct detections |

L1 + L2 + L3 propose a **person-following controller**, subject to target association and testing: the camera supplies the bearing, the ToF sensor supplies the distance. The ToF sensor measures the nearest reflecting surface in its field, not the identity of the person. Permit forward motion only with a selected, fresh, confident camera target aligned to the body and a valid range. Stop at or below a provisional 350 mm obstacle threshold, on invalid range, or when target data is older than 300 ms. A wall can still produce a valid range; association needs bench validation. No autonomous obstacle bypass or reversing is proposed.

## 5. Safety supervisor (Pico, highest priority)

- Must have bounded timing independent of networking and audio. A cooperative async task alone cannot guarantee this if another task blocks. Use nonblocking I/O, bounded buffers, a motor-command expiry and a hardware watchdog with motor inputs defaulting off. Verify scheduling under network loss and audio load before driving.
- It is the only code path allowed to set motor PWM to a non-zero value. Everything else sends *requests*.
- Hard limits: PWM duty cap (start at 50%), acceleration ramp (≤ 0.5 m/s² equivalent), servo slew limit, servo angle limit ±70° (mechanical stops are at ±75°).
- Triggers FAULT_STOP on: excess tilt, detected anomalies, watchdog, low supply voltage (Pico VSYS reading via ADC3, see [04](04-wiring-pin-plan.md)), I2C bus failure of the accelerometer, or a manual press of B.

## 6. Offline (honest non-AI) mode

If the bridge, Wi-Fi or API is unavailable, Pip **says so** ("I can't think with my cloud brain right now, let's play my own games!"). It then offers games that use only the Pico and its sensors:
1. **Touch quiz** from a question bank stored on the Pico (OLED + buzzer + LEDs)
2. **Colour-card treasure hunt** (colour sensor)
3. **Distance feedback** using the ToF and OLED, stationary. Without camera target association it cannot claim to follow a person.
4. **Freeze dance**: Pip plays tunes on the buzzer and the kids freeze when it stops. Without the camera bridge it cannot check whether they froze.

No feature is presented as "AI" in this mode.

## 7. Interfaces

### 7.1 Network
- The bridge listens on the LAN. Pico and XIAO connect as clients with a **pre-shared token** (in a `secrets.py` that is not committed).
- **The OpenRouter API key exists only on the laptop** (environment variable). It is never sent to the robot.
- Transport (proposal): **WebSocket** for control and telemetry (JSON); **UDP or WebSocket binary** for audio (16 kHz, 16-bit mono, 20 ms frames); **HTTP multipart or WebSocket binary** for JPEG frames (QVGA 320×240, 5–10 fps).

### 7.2 Messages (JSON; `v` = protocol version)

| Direction | Type | Fields (example) |
|---|---|---|
| Pico → bridge | `hello` | `{"v":1,"type":"hello","dev":"pip-body","fw":"0.1"}` |
| Pico → bridge | `telemetry` (10 Hz) | `state, head_deg, dist_mm, tilt_deg, vsys_v, move_enabled, fault` |
| Pico → bridge | `event` | `{"type":"event","name":"touch","pad":"B"}` / `button`, `colour`, `lifted` |
| bridge → Pico | `track` | `{"type":"track","bearing_deg":-12.5,"size":0.31,"conf":0.8,"t":...}` |
| bridge → Pico | `say_begin` / audio frames / `say_end` | speech playback through the body speaker |
| bridge → Pico | `display` | `{"type":"display","icon":"question","text":"Red or blue?","choices":["A","B","C"]}` |
| bridge → Pico | `led`, `buzz`, `behaviour` | e.g. `{"type":"behaviour","name":"follow","on":true}` |
| bridge → Pico | `hb` (heartbeat, 5 Hz) | `{"type":"hb","t":...}` |
| bridge → XIAO | `cam` | `{"type":"cam","on":true,"fps":8,"res":"QVGA"}` |
| XIAO → bridge | frames / audio | binary |

The bridge never commands raw wheel PWM. It sends behaviour targets (`track`, `behaviour`), and the Pico's loops and supervisor turn them into motion.

### 7.3 Bridge internals (proposal, provider-neutral)

```
CameraIn ─► PersonTracker (OpenCV / MediaPipe-class, local) ─► track msgs ─► Pico
MicIn ─► VAD ─► STT (local first) ─► DialogueManager ─► SafetyFilter ─► LLMClient(OpenAI-compatible base_url)
                                           ▲                                   │
                                     ActivityScripts ◄─────────────────────────┘
                                           │
                                     TTS (local first) ─► AudioOut ─► Pico speaker
Logger ─► CSV/JSON logs for evidence (loop data, latency, costs) - no raw audio/video stored by default
```
`LLMClient` takes `base_url`, `model` and `api_key` from configuration, so OpenRouter can be swapped for another compatible endpoint without code changes.
