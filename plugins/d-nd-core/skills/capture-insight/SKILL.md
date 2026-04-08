---
name: capture-insight
description: Quickly capture operator insights without breaking current workflow. Auto-routes to appropriate team/node. Use when the operator shares observations, ideas, or strategic thoughts mid-session.
---

# Capture Insight — Quick Capture & Route

When the operator shares an insight, observation, or strategic thought during a work session:

## Protocol (30 seconds max)

1. **Capture**: Append a 2-3 line note to `memory/brand_voice.md` or relevant memory file
2. **Route**: If actionable, create a one-line task entry in `memory/backlog.md` or send to the relevant node via messaging
3. **Ack**: Reply "Noted: [1-line summary]. Back to [current task]."
4. **Continue**: Return immediately to the current work

## DO NOT
- Deep-dive into the insight
- Write long analyses
- Create new files
- Change current priorities
- Stop what you're doing for more than 30 seconds

## Routing rules
- **Brand/copy/voice** → `brand_voice.md` + backlog if actionable
- **Technical idea** → backlog + optionally delegate to another node
- **Strategic/commercial** → `hub_vision.md` + backlog
- **Architecture/pattern** → `evolution.md` or CLAUDE.md

The insight will be processed properly in its own dedicated session, not mid-flow.

$ARGUMENTS

## Eval

## Trigger Tests
# Appropriate prompts for this skill -> activates
# Unrelated prompts -> does NOT activate

## Fidelity Tests
# Given valid input: produces expected output
# Given edge case: handles gracefully
# Always reports what was done
