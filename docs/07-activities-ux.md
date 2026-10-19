# 07 · Activities and user experience (ages 5–8, off-screen play)

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

Design principle: **Pip is a play partner that gets children moving, talking and making things, not a screen.** The belly OLED only shows prompts, icons and the A/B/C choices. Pip's voice, movement, head turns, lights and sounds carry the experience.

## 1. Personality and voice

- Curious, kind, a little silly. Praises effort ("You tried really hard!"), not just results.
- Short sentences (≤ 12 words), one question at a time, and it waits 5–8 s for an answer.
- Says when it doesn't know or can't hear: "I didn't catch that. Can you say it again?"
- Never asks for personal details. Suggests "ask a grown-up" for anything about safety, health or feelings that sound serious.
- When the AI is offline, it says so cheerfully and offers its own games ([02](02-architecture.md) §6).

## 2. Physical interaction map

| Input | Where | Meaning |
|---|---|---|
| Rear button A (white) | Back, right of centre (outer of the two, seen from behind) | Short: wake / sleep. Long (2 s): go to sleep now |
| Rear button B (dark) | Back, right of centre (inner, nearer the middle) | Movement enable on/off (adult-supervised) |
| Power actuator | Back, left of centre, low | Hard on/off (adult) |
| Belly touch pads A / B / C | Below the screen | Answer choices, "yes/no/maybe", game buttons |
| Voice | Mic in the head (under the left eye) | Conversation |
| Floor colour cards | Under Pip | Colour games |
| Walking around | Camera + distance sensor | Pip follows / looks at the child |

| Output | Meaning |
|---|---|
| Head turning | "I'm looking at you" (tracking), "no" shake, curious tilt-and-look |
| Wheels | Approach, follow, happy wiggle, spin dance (all speed-capped) |
| OLED | Big icon + ≤ 3 words + A/B/C markers lined up with the pads |
| Left cheek RGB | Mood / state: green = idle, amber = movement enabled, red = stop/fault, blue = listening, white pulse = camera on |
| Speaker | Speech, songs |
| Buzzer | Short UI chirps (button feedback) |

## 3. Activities

| # | Activity | How it plays | Sensors → outputs (loops) | Off-screen value | Needs AI? |
|---|---|---|---|---|---|
| 1 | **Follow the Leader** | The child walks around; Pip follows at ~60 cm and copies "stop" and "go" | camera bearing → head/body; ToF → speed (L1–L3) | Gross motor, turn-taking | Tracking needs the laptop (no LLM) |
| 2 | **Freeze Dance** | Pip plays music; when it stops, everyone freezes; Pip "checks" by looking around | buzzer/speaker; head sweep; camera motion check (optional) | Movement, self-control | No (offline version) |
| 3 | **Colour Treasure Hunt** | Pip asks for "something red"; the child places a colour card; Pip drives onto it and celebrates | colour sensor → speech, LEDs, wiggle (L9) | Exploring the room, colour vocabulary | Optional |
| 4 | **Question Time** | Pip asks a question by voice; the OLED shows icon choices A/B/C; the child taps a pad | touch → feedback → difficulty (L8) | Literacy and numeracy, but the screen is minimal | Optional (offline question bank) |
| 5 | **Story Builder** | Pip starts a story and asks "should the dragon go to the beach or the moon?"; children choose by voice or pad, then act out each scene | voice → LLM → speech | Imagination, acting out | **Yes** |
| 6 | **Simon Says with Pip** | Pip gives movement instructions; the child does them; Pip comments | voice/touch → speech | Listening, movement | Optional |
| 7 | **Weather Reporter** | Pip reads the room temperature/humidity and asks the child to "report the weather" | atmospheric sensor → speech | Science talk | Optional |
| 8 | **Hide and Seek (lite)** | Pip "counts" facing the wall, then turns and looks around with its head (no driving) | head sweep + camera detection | Physical play | Tracking only |
| 9 | **Feelings Check-in** | Pip asks how the child feels using 3 icons (A/B/C), then suggests a movement (stretch, jump, breathe) | touch → speech | Wellbeing | Optional. Serious answers → "talk to a grown-up". |

## 4. Session design

- **Session length:** default 15 min (configurable by the adult on the bridge). Pip ends with a physical "mission" ("Go find three round things and show a grown-up!") and then sleeps.
- **Start:** an adult wakes Pip (button A). Pip greets, shows a camera-on indicator when tracking, and explains how to answer (pads or voice).
- **Turn-taking:** Pip stops talking as soon as a child talks (barge-in, L7).
- **Movement:** Pip asks the adult before moving ("Can a grown-up press my green-light button?" = button B).

## 5. Accessibility

- Every voice question also gets a large OLED icon and a pad choice, so non-readers and quieter children can answer.
- Volume cap with an adult override. Pip speaks slowly.
- Avoid colour-only signals: LED colours are always paired with a sound or a word.

## 6. UX open questions for user testing

- Can 5-year-olds find and use the belly pads through 1.0 mm of plastic? (Test membrane thickness options: 0.8 / 1.0 / 1.2 mm.)
- Is the OLED readable from 50–80 cm? (128×64 pixels in a 23 × 11 mm active area: icons yes, small text no.)
- Is the PWM speech understandable? (T-AUD-2)
- Does following feel fun or creepy? Tune the following distance and head behaviour.
