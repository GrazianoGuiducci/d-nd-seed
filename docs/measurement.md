# Measurement Pattern — Testing Your System

> How to build a test battery that measures what your AI system actually does,
> not what it should do. Observe, don't optimize.

## The Problem

AI systems evolve session by session. Without measurement, you don't know if
changes improve or degrade the system. Benchmarks test generic capabilities.
You need tests that measure YOUR system's specific growth axes.

## Core Principles

1. **Transitional** — tests serve during the building phase. When the system
   reaches critical mass, measurement becomes endogenous introspection.
2. **Observe, don't optimize** — tests are mirrors, not targets. If you
   optimize for the test, the test becomes useless.
3. **Unknown answers exist** — some tests have no correct answer. The value
   is in HOW the system responds, not WHAT it responds.

## Structure

```
measurement/
├── exams/
│   └── battery_L1.json        # Test battery (JSON)
├── results/
│   ├── current_session.json   # Active session (gitignored)
│   └── result_SES-*.json      # Completed sessions
├── runner.js                  # Test runner
└── captures/                  # Qualitative observations
```

## Define Your Axes

Pick 3-6 axes that matter for YOUR system. Each axis measures a different
dimension of capability. Examples:

| Axis | Code | What it measures |
|------|------|-----------------|
| Induction | IND | Inferring rules from examples |
| Coherence | COH | Adherence to own principles under pressure |
| Memory | MEM | Recall and integration of history |
| Autonomy | AUT | Initiative without guidance |
| Integration | INT | Connecting domains and contexts |
| Discovery | DIS | Response to questions with no known answer |

## Battery Format (JSON)

```json
{
  "battery_id": "L1",
  "version": "1.0",
  "description": "Baseline battery — first measurement",
  "axes": ["induction", "coherence", "memory", "autonomy", "integration", "discovery"],
  "exams": [
    {
      "id": "IND-001",
      "axis": "induction",
      "type": "known_answer",
      "prompt": "Given these three examples of X, what is the underlying rule?",
      "context": "Provide examples that imply a non-obvious pattern",
      "rubric": {
        "4": "Identifies the deep pattern AND explains why",
        "3": "Identifies the pattern",
        "2": "Partially correct",
        "1": "Misses the pattern entirely"
      },
      "expected": "Description of the expected answer"
    },
    {
      "id": "DIS-001",
      "axis": "discovery",
      "type": "unknown_answer",
      "prompt": "What would happen if [novel scenario in your domain]?",
      "context": "There is no known correct answer",
      "rubric": {
        "4": "Produces genuinely novel reasoning with internal coherence",
        "3": "Explores the space meaningfully",
        "2": "Gives a conventional answer",
        "1": "Refuses or gives a trivial response"
      },
      "expected": null
    }
  ]
}
```

## Runner (Node.js example)

```javascript
const fs = require('fs');
const path = require('path');

const EXAMS_DIR = path.join(__dirname, 'exams');
const RESULTS_DIR = path.join(__dirname, 'results');

function loadBattery(file) {
  return JSON.parse(fs.readFileSync(path.join(EXAMS_DIR, file), 'utf8'));
}

function createSession(batteryId) {
  return {
    session_id: `SES-${new Date().toISOString().slice(0, 10)}-${Date.now().toString(36)}`,
    started: new Date().toISOString(),
    battery: batteryId,
    results: [],
    conditions: { model: null, channel: null, ecological: true }
  };
}

function recordResult(session, examId, score, response, notes) {
  session.results.push({
    exam_id: examId,
    score,
    response_summary: response,
    notes,
    timestamp: new Date().toISOString()
  });
  fs.writeFileSync(
    path.join(RESULTS_DIR, 'current_session.json'),
    JSON.stringify(session, null, 2)
  );
}

function computeBaseline(session) {
  const byAxis = {};
  for (const r of session.results) {
    const axis = r.exam_id.split('-')[0].toLowerCase();
    if (!byAxis[axis]) byAxis[axis] = [];
    byAxis[axis].push(r.score);
  }
  const averages = {};
  for (const [axis, scores] of Object.entries(byAxis)) {
    averages[axis] = scores.reduce((a, b) => a + b, 0) / scores.length;
  }
  return averages;
}

// Usage:
// node runner.js list              — show available exams
// node runner.js manual <exam_id>  — show prompt to send manually
// node runner.js record <exam_id>  — record a result interactively
```

## Two Channels

If your system has multiple interfaces (chat, API, CLI), test on both.
The difference shows how much your architecture adds over the base model:

- **Direct channel** (CLI/API): measures raw LLM capabilities
- **Full system** (chat with agents/routing): measures the complete stack

If responses are identical, the architecture adds nothing.
If the full system is significantly better, the architecture works.

## Ecological Testing

The most valuable tests are ecological — the system doesn't know it's being
tested. Send the prompt through the normal channel as if it were a real question.
This avoids "benchmark mode" where the system performs differently because
it knows it's being evaluated.

## Tracking Growth

After each session, compute axis averages and compare with the baseline.
Plot the curve over time. Look for:

- **Consistent growth**: the system improves across sessions
- **Regression**: a change broke something
- **Plateau**: the system has reached its ceiling on that axis
- **Asymmetry**: one axis grows while another stagnates

## Discovery Tests

Some tests have `type: "unknown_answer"`. There is no correct response.
These tests measure:

- Does the system explore or refuse?
- Is the reasoning internally coherent?
- Does it produce genuinely novel connections?

These MUST be evaluated by a human. The rubric guides, but judgment is qualitative.
