# 02 · System architecture, closed loops and interfaces

**Status: design only. Firmware and the laptop bridge are not implemented.** This page fixes the responsibilities, control loops, safety limits and message formats for the full concept ([08](08-bom-budget-sourcing.md) §3). Purchases and wiring are on HOLD.

## 1. Block diagram

Power source: owned MINISO QW01, approximately 130 × 60 × 10 mm. Micro-USB is the charge input only. The two USB-A outputs are reported as 5 V / 2 A each. They remain separate branches; no output paralleling or assumed 4 A combined supply is allowed. The topology below is a comparison concept until the bank/load checks in [05](05-power-budget-charging.md) pass.

```
                      Wi-Fi 2.4 GHz (same LAN, or the laptop's hotspot)
 ┌──────────────────────── ROBOT "Pip" ─────────────────────────┐       ┌──────────── LAPTOP "Pip Bridge" ────────────┐
 │ HEAD (pans)                                                   │       │ video in → person detector + tracker (local)  │
 │  DFR1154 camera board: camera ──JPEG frames────────────────────────► │   → target bearing, box size, track id, age   │
 │                        PDM mic ──16 kHz audio─────────────────────► │ audio in → VAD → speech-to-text (local first) │
 │                        I2S amp + speaker ◄──speech audio──────────── │   → dialogue manager → safety filter          │
 │  USB-C 5 V from bank port 2 via in-line camera switch         │       │   → OpenRouter LLM (text, HTTPS) ──────────────┼──► Internet
 │                                                               │       │ reply → text-to-speech (local first)          │
 │ BODY                                                          │       │ behaviour targets, heartbeat ──┐             │
 │  Pico 2 WH on Kitronik 5331 (DRV8833)                         │ ◄─────┼────────────────────────────────┘             │
 │   ├ TT motors L/R (GP2/3, GP6/7)                              │       │ API key only here (never on the robot)       │
 │   ├ head servo FS90 (GP27)                                    │       └──────────────────────────────────────────────┘
 │   ├ I2C0 (GP0/1): rear Buttons A/B, OLED, touch, ToF,         │
 │   │   accelerometer, colour, atmospheric, RGB LED, buzzer     │
 │   └ SAFETY SUPERVISOR: local, never waits on Wi-Fi            │
 │  Body power: bank port 1 → lever connectors → Kitronik + servo │
 └───────────────────────────────────────────────────────────────┘
```

## 2. Who does what

| Unit | Responsibilities | If Wi-Fi drops |
|---|---|---|
| **Pico 2 W** (body) | Motor and servo commands, safety supervisor, sensors, OLED, touch, LEDs, buzzer, behaviour state machine, offline games, link to the bridge | Stops motion within the heartbeat timeout, then offers offline games |
| **DFR1154** (head) | Streams camera frames and mic audio to the bridge; plays speech audio from the bridge; obeys camera on/off commands | Stops streaming; the Pico shows "offline" |
| **Laptop bridge** | Person detection and tracking, target selection, VAD, speech-to-text, LLM calls, safety filter, text-to-speech, activity scripts, evidence logs | n/a |
| **OpenRouter model** | Conversation text from a child-safe system prompt | n/a |

The RP2350 (520 KB SRAM, 4 MB flash, 150 MHz; Raspberry Pi documentation) suits control loops. It cannot run a chat model or reliable person detection. Moving audio to the DFR1154 also keeps audio buffering off the Pico, which keeps the supervisor's timing simpler.

## 3. Behaviour state machine (Pico)

```
 body switch ON → BOOT (motors coast, movement disabled, servo detached) → SLEEP
 SLEEP ──Button A short press──► AWAKE_STILL   (talk, quiz, head tracking; NO wheel motion)
 AWAKE_STILL ──Button B + all motion preconditions true──► AWAKE_MOVING
 AWAKE_MOVING ──Button B again │ enable expired (5 min) │ any stop trigger (§5)──► STOPPED (motors coast then brake)
 STOPPED ──Button B after the cause clears──► AWAKE_STILL
 any state ──Button A long press (2 s) │ 10 min idle──► SLEEP (camera told to stop; servo detached)
```

- Movement-enable is cleared on every boot, wake and stop. A child cannot start motion by accident. Pressing B is a deliberate act, normally by the adult.
- SLEEP is software only. The camera hardware is powered off only by the in-line camera switch or by unplugging ([05](05-power-budget-charging.md) §2).
- The RGB LED shows the state: green = awake still, amber = movement enabled, red = stopped/fault, white pulse = camera streaming (reported by the DFR1154 via the bridge).

## 4. Closed loops

All loops log `t, setpoint, measurement, output` for evidence. All gains and thresholds are starting points to tune and record.

| # | Loop | Sensor → controller → actuator | Control law (start) | Feedback evidence |
|---|---|---|---|---|
| L1 | **Head tracking** | Camera bearing of the **selected** target (bridge) → Pico → servo command | θcmd += Kp·e (Kp≈0.4), deadband ±3°, slew ≤ 90°/s, limited to ±70° | Bearing error e(t) → 0. The camera rides on the head, so e is measured relative to the **actual** head direction, even if the clutch has slipped. |
| L2 | **Body yaw assist** | θcmd (commanded head angle) → differential wheel speeds | If abs(θcmd) > 35°, turn the body toward it while L1 re-centres the head | θcmd returns within ±15° |
| L3 | **Follow distance** | ToF range d (chest) → forward speed v | v = Kp·(d − 0.6 m), clamp 0…0.25 m/s, deadband ±5 cm. **Allowed only when all preconditions in §4.1 hold.** | d(t) settling near 0.6 m |
| L4 | **Tilt stop (heuristic)** | Accelerometer → motors | Static tilt > 25° for 100 ms → STOPPED | Stop latency on a tilt table |
| L5 | Turn-taking | Mic VAD (bridge) → speech playback | Turn-based first (Pip does not listen while speaking). Barge-in is added only after echo rejection is measured. | Reply latency; barge-in latency once enabled |
| L6 | Quiz adaptation | Touch answer → next question level | Two right → harder; two wrong → easier + hint | Accuracy trend |
| L7 | Colour-card game | Colour sensor (floor) → speech, LEDs, short wiggle | Hue classification with hysteresis | Correct detections |

### 4.1 Head angle: commanded vs actual

The FS90 has **no position feedback** available to the Pico. `head_deg` in telemetry is always the **commanded** angle. The actual angle can differ: during slewing, under load, and permanently after the slip clutch has slipped. L1 does not depend on it, because it measures error in the camera image. L2 and the ToF alignment check below use θcmd as an **estimate**. Re-centre procedure: after a clutch slip is suspected (tracking offset that persists with the target straight ahead), command 0° and have the adult turn the head by hand until it clicks into the centre notch. A "head straight" check (a target held straight ahead of the body) is part of T-PAN-2.

### 4.2 Following a person: what the sensors can and cannot do

- The **camera** (via the bridge) gives the bearing, box size and track ID of detected people. The bridge selects **one target**: the person the adult points Pip at when following starts. It keeps that track ID and drops the target when the track is lost.
- The **ToF sensor** measures the distance to the nearest reflecting surface in its narrow field. **It does not know who or what it is measuring.** A wall, a chair or a different child gives a valid reading too.
- Forward motion (L3) is therefore permitted **only when all of these hold**, checked every cycle:
  1. Movement enabled (Button B) and no stop trigger active.
  2. A selected target exists, its track is **younger than 300 ms**, and its confidence is above the threshold.
  3. **Alignment:** abs(θcmd) ≤ 10° **and** the target's image bearing ≤ ±8°. The person is then on the body axis that the ToF sensor looks along.
  4. The ToF reading is **valid** (sensor status OK, value updated within 100 ms).
  5. **Plausibility:** the ToF range agrees within ±35% with the camera's box-size range estimate (calibrated per T-CAM-2). Disagreement means the ToF is probably seeing something else.
- **Immediate stop threshold:** any valid ToF range **≤ 350 mm** → v = 0, regardless of target status.
- **Target loss:** no fresh target for 300 ms → v = 0. Lost for 5 s → leave follow mode, say so, and wait for the adult.
- Pip only drives **forward or turns on the spot**. It never reverses automatically, because there is no rear sensor. It has no cliff or edge sensing. Use only on a clear, level, enclosed floor with no stairs or drops.

### 4.3 Accelerometer limits

An accelerometer measures tilt well when the robot is still. During motion and handling it measures tilt plus acceleration. **It cannot reliably detect a slow, gentle lift, and it cannot distinguish steady motion from rest, or a stalled wheel from a moving one.** L4 is a **heuristic**. Pip is designed for **supervised floor use only**. The adult disables movement (Button B) before anyone picks it up.

## 5. Safety supervisor (Pico)

- **Single owner of motor outputs.** All other code sends requests with an expiry time.
- **Local watchdogs, independent of network and audio:**
  - Every motor command expires after **200 ms** unless the supervisor renews it from fresh local loop data. On expiry the outputs go to coast.
  - The RP2350 **hardware watchdog** resets the Pico if the supervisor stops running. Motor pins are then undriven. Gate PG7 checks that the motors stay still through a reset.
  - **Bridge heartbeat:** any bridge-dependent motion (L1–L3 driven by camera targets) stops if no heartbeat arrives for **500 ms**.
  - Networking uses non-blocking sockets with bounded buffers. The supervisor runs at fixed priority, so a stalled Wi-Fi call cannot hold the motors on. Verify under load: T-SAF-3 with the camera streaming and audio playing.
- **Stop triggers:** Button B, enable expiry, tilt heuristic, ToF ≤ 350 mm while moving forward, target loss, heartbeat loss, I2C bus error (accelerometer, ToF or Buttons not readable), supervisor overrun.
- **Limits:** speed cap ≤ 0.25 m/s (PWM duty calibrated in T-DRV-3), acceleration ramp, servo ±70° and slew-limited.
- **Not provided:** stall detection, lift detection guarantee, cliff detection, obstacle detection outside the ToF beam, reversing. Hardware motor protection remains unresolved ([05](05-power-budget-charging.md) §4). Do not treat the bank's cutoff as a motor-current limit.

## 6. Offline mode

If the bridge, Wi-Fi or API is unavailable, Pip says so ("My cloud brain is asleep, let's play my own games!") and offers Pico-only games: touch quiz (OLED + buzzer + LED), colour-card hunt, and stationary distance games (ToF → OLED/LED). **It does not follow anyone offline**, because there is no camera target without the bridge. Nothing offline is presented as AI.

## 7. Interfaces

### 7.1 Network
- The bridge listens on the LAN. The Pico and the DFR1154 connect as clients with a pre-shared device token kept in an uncommitted `secrets.py`.
- **The OpenRouter API key lives only on the laptop** (environment variable). It is never sent to the robot or committed to the repo. No API calls were made, and no keys were created, in this design round.
- Transport (proposal): WebSocket JSON for control and telemetry. WebSocket binary for audio (16 kHz 16-bit mono, 20 ms frames) and JPEG frames (QVGA, 5–10 fps).

### 7.2 Messages (JSON, `v` = protocol version)

| Direction | Type | Fields (example) |
|---|---|---|
| Pico → bridge | `telemetry` (10 Hz) | `state, head_cmd_deg, dist_mm, dist_valid, tilt_deg, move_enabled, stop_reason` |
| Pico → bridge | `event` | `{"type":"event","name":"touch","pad":"B"}`, `button`, `colour` |
| bridge → Pico | `track` | `{"type":"track","id":7,"bearing_deg":-12.5,"size":0.31,"range_est_m":0.9,"conf":0.8,"age_ms":80}` |
| bridge → Pico | `display`, `led`, `buzz`, `behaviour`, `hb` | as before; `hb` at 5 Hz |
| bridge → camera | `cam`, audio frames | `{"type":"cam","on":true,"fps":8,"res":"QVGA"}`; speech audio |
| camera → bridge | frames, audio, `status` | `status` reports streaming on/off |

The bridge never commands wheel PWM. It sends targets and behaviours, and the Pico's loops and supervisor decide motion.

### 7.3 Bridge internals (proposal, provider-neutral)

```
CameraIn ─► PersonTracker (local) ─► TargetSelector (id, age, conf, range_est) ─► track msgs ─► Pico
MicIn ─► VAD ─► STT (local first) ─► DialogueManager ─► SafetyFilter ─► LLMClient(base_url, model, key from env)
TTS (local first) ─► SpeakerOut (to DFR1154)      Logger ─► CSV/JSON (numbers and redacted text; no recordings by default)
```
