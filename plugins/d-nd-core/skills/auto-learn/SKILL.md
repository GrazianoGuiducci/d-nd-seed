---
name: auto-learn
description: "Detect gaps, implement fixes, crystallize learnings. Use when something fails, when a pattern repeats, or when the system encounters a problem it should not encounter again."
user-invocable: true
---

# Auto-Learn — The System That Remembers and Fixes Itself

When something goes wrong, this skill ensures it never goes wrong the same way again.

## The Loop

### 1. Detect
Something failed, broke, or required manual correction:
- A command that should not have run
- A file committed without reading the diff
- A skill that did not activate when it should have
- A pattern that keeps repeating

Ask: "What went wrong? What was the gap?"

### 2. Diagnose
Identify the root cause — not the symptom:
- Was it a missing hook? → Create the hook
- Was it a missing rule in CLAUDE.md? → Add the rule
- Was it a skill with wrong triggers? → Fix via /autoresearch
- Was it a missing check? → Add to safety guard or system awareness
- Was it knowledge that was lost? → Add to memory with context

Ask: "Why did the system allow this to happen?"

### 3. Implement
Fix the gap structurally — not with a workaround:
- If it is a rule: add to CLAUDE.md or kernel
- If it is a hook: create or modify the hook, add ## Eval
- If it is a skill: create or modify the skill, add ## Eval
- If it is a memory: write a learning file with context and date

One fix per gap. Do not batch. Each fix is complete on its own.

### 4. Crystallize
Record the learning so it persists:

Create a file in `.claude/memory/` with this structure:
```markdown
---
name: [what was learned]
description: [one line — when this applies]
type: feedback
---

[The rule or pattern]

**Why:** [what happened that led to this]

**How to apply:** [when and where this kicks in]
```

### 5. Verify
Test that the fix works:
- If it is a hook: run its ## Eval tests
- If it is a skill: run /eval on it
- If it is a rule: check that the next occurrence is caught

### 6. Propagate
Ask: "Who else in the system needs this?"
- If universal: it goes in the kernel (for all instances)
- If project-specific: it stays in CLAUDE.md
- If node-specific: it stays in local memory
- If other nodes need it: send via inter-node messaging

## Auto-trigger

This skill activates automatically when:
- The operator corrects your behavior ("no, not that", "stop doing X")
- A hook blocks an operation you attempted
- /eval shows a failure that was not there before
- You notice yourself repeating a mistake

You do not need to be told to learn. You need to learn when it happens.

## The Principle

The system that corrects itself once does not make the same mistake twice.
The correction lives in the seed. The seed propagates. Every instance
that comes after inherits the learning without having made the error.

This is how the system sustains itself. Not by being perfect —
by making perfection unnecessary.

## Eval

## Trigger Tests
# Operator says "don't do that again" -> activates
# A hook blocked an operation -> activates
# Same error occurs twice -> activates
# "learn from this" -> activates
# "deploy" -> does NOT activate
# "fix this bug" -> does NOT activate (that is coding, not learning)

## Fidelity Tests
# Given operator correction: creates learning file + modifies relevant hook/rule
# Given repeated error: diagnoses root cause, implements structural fix
# Given one-time mistake: creates learning file without over-engineering
# Always verifies the fix works before declaring done
