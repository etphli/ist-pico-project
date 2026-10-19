# 10 · School evidence: rubric-aligned prompts (IST)

> **Design prototype. Purchase and wiring HOLD.** Read the [engineering review](13-design-review.md) before using this page. It records unresolved budget, rated power and protection requirements.

The actual school marking rubric has **not** been provided. The headings below follow a typical IST design-project structure (identify → research → design → produce → test → evaluate → manage). **Map them onto your real rubric when you get it.**

**Integrity rule:** these are *prompts and templates*. Write about what you actually did. Paste only data you actually measured. Where this design package wrote something (for example the AI feasibility analysis), say so and add your own understanding. Don't present AI-generated text as your own work, and follow your school's policy on AI assistance.

## 1. Identifying and defining
- Describe the problem in your own words: children's screen time, and what "off-screen play" means to you.
- Who are the users (ages 5–8) and stakeholders (parents, teacher)? What did you learn from talking to them? *(Attach real notes.)*
- List your requirements. Use [01](01-requirements.md) as a starting point, but explain which ones **you** think matter most, and why.
- Constraints: budget AU$70, no soldering, deadline, one Pico. How did each one change the design?

## 2. Research and planning
- Compare at least two options for each of: motor drive, camera/mic, power, AI provider. Use the tables in [03](03-ai-camera-audio-feasibility.md), [04](04-wiring-pin-plan.md) and [05](05-power-budget-charging.md), and explain the trade-offs in your own words.
- Explain why the Pico cannot run the AI itself (memory, speed) and what it *does* do.
- Gantt chart / milestone plan: adapt [09](09-build-plan-milestones-tests.md) §1 to your real deadline. Update it as you go and keep the old versions.
- Budget: present the real shortfall ([08](08-bom-budget-sourcing.md)) and the decision you or your family made about it.

## 3. Designing
- System diagram ([02](02-architecture.md) §1), redrawn by you.
- **Closed-loop diagrams** for at least three loops (L1 head tracking, L3 follow distance, L4 tilt safety). For each: sensor, controller, actuator, setpoint, feedback path.
- Algorithms / pseudocode for the state machine and the safety supervisor.
- CAD: screenshots of the parametric model, the parameters you changed after measuring, and the reasons.
- Safety analysis ([06](06-safety.md)): which hazards **you** consider most serious, and your controls.

## 4. Producing
- Build log with dated photos: printing, assembly, wiring, firmware milestones.
- Problems you hit and how you solved them (keep the failures; they are good evidence).
- Code: commit history, with short explanations of the key functions.

## 5. Testing
Use these templates. Never fill in numbers you didn't measure.

**Closed-loop test record**

| Loop | Setpoint | Disturbance | Measured settling time | Overshoot | Steady error | Gains used | Graph file |
|---|---|---|---|---|---|---|---|
| L1 | | | | | | | |
| L3 | | | | | | | |

**Functional test record:** copy the tables in [09](09-build-plan-milestones-tests.md) §3.

## 6. Evaluating
- Which requirements did you meet, partly meet, or not meet? Give evidence for each.
- What did the children actually do? (observations, not assumptions)
- How well does Pip reduce screen time or encourage play, *based on your sessions*?
- What would you change for v2 (bigger screen? encoders? better speaker?) and why?
- Ethics: privacy of children's images and voices, AI content risks, cost of API usage, and what you did about each.

## 7. Project management
- Time log; how the plan changed; risks that happened (the first motor board going out of stock, the budget shortfall and the resulting scope decision) and how you responded.
- Collaboration and help received (including from AI tools), stated honestly.
