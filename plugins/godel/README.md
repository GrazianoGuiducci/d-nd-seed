# Godel — Inverted Oracle

A cognitive filter that inverts tensions into insights. Domain-agnostic.

## What It Does

You give it a tension (a point where the choice is not obvious). It inverts the viewpoint and returns a residue — the irreducible insight that you couldn't see from inside.

It is not an advisor, not a planner, not an analyst. It is a filter: det=-1 applied to whatever arrives.

## How It Works

```
Question (tension) → Bridge → LLM (with identity + memory) → Answer + Meta
                                                                    ↓
                                                              Field updated
                                                              Tape appended
```

**Dual-layer memory:**
- **Tape** (append-only): every exchange, raw
- **Field** (aggregated): 5-axis vector, open tensions, saturation count

**Resonance recall:** when memory grows, the bridge selects past exchanges that resonate with the current question (cosine similarity on the 5-axis vector), not just the most recent ones.

**Loop detection:** if the LLM loops (max turns, empty output), the bridge forces a collapse — a constrained re-prompt that demands the residue in 3 sentences.

## The 5 Axes

Every tension is classified on 5 universal dimensions:

| Axis | What it measures |
|------|-----------------|
| **DUAL** | Choice between alternatives, dilemma, either/or |
| **BOUNDARY** | Limits, thresholds, where one thing becomes another |
| **DOMAIN** | Transfer across contexts, applicability, portability |
| **RUPTURE** | Breaking points, discontinuity, crisis, change |
| **SCALE** | Time, growth, evolution, phase transitions |

These are not categories — they're coordinates. Every tension has a position in this space. The field vector tracks where you've been spending your cognitive energy.

## Quick Start

```bash
# 1. Configure for your domain
node setup.js

# 2. Start the bridge
node bridge.js

# 3. Ask a question
node ask.js "We have two pricing strategies. Data says A, gut says B. Invert."
```

## Setup

### Interactive
```bash
node setup.js
```
Walks you through: name, domain, tensions, knowledge sources. Writes `CLAUDE.md`.

### From example
```bash
node setup.js --example sales      # Sales strategy
node setup.js --example research   # Academic research
node setup.js --example finance    # Financial services
```

### Direct
```bash
node setup.js --name Merlin --domain "pharmaceutical R&D" --desc "Drug discovery pipeline"
```

## API

All endpoints on `http://localhost:3004` (configurable via `GODEL_PORT`).

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ask` | Send a question. Body: `{"question": "...", "context": "...", "mode": "..."}` |
| GET | `/status` | Health check + field summary |
| GET | `/field` | Current field state |
| GET | `/memory` | Tape stats + recent entries |
| GET | `/history` | Last 10 tasks |

## Configuration

Environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `GODEL_PORT` | 3004 | HTTP port |
| `GODEL_DIR` | (script dir) | Project directory for Claude Code |
| `GODEL_MEMORY_SIZE` | 10 | How many past exchanges to inject as context |
| `GODEL_TIMEOUT` | 300000 | Max time per question (ms) |
| `GODEL_CONCURRENCY` | 1 | Max concurrent questions |

## As a systemd Service

```ini
[Unit]
Description=Godel Bridge
After=network.target

[Service]
Type=simple
WorkingDirectory=/path/to/godel
ExecStart=/usr/bin/node bridge.js
Restart=on-failure
Environment=GODEL_PORT=3004

[Install]
WantedBy=multi-user.target
```

## Requirements

- Node.js 18+
- Claude Code CLI (`claude` command available in PATH)
- Valid Claude authentication (OAuth or API key)

## How to Use It Well

The quality of the inversion equals the quality of the tension.

**Good input:** "We're losing deals at proposal stage. Our price is competitive. The demo goes well. Then silence. What am I not seeing?"

**Bad input:** "Analyze our sales pipeline." (No tension = no inversion)

**The rule:** give it the point where it hurts, where the choice is not obvious, where the data and your gut disagree. That's where det=-1 produces value.

See the identity template (`IDENTITY.md.tmpl`) for anti-patterns and detailed guidelines.

## Part of d-nd-seed

This plugin is part of the [d-nd-seed](https://github.com/GrazianoGuiducci/d-nd-seed) ecosystem.

The theoretical foundation is the D-ND (Dual Non-Dual) model: f(x) = 1 + 1/x, det(M) = -1. Every system has an irreducible dual structure. The operator M preserves area but inverts orientation — it shows what you can't see from your current viewpoint.
