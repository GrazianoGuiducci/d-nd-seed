# How to Install Skills from the Seed

Skills are operational patterns. They activate when conditions are met. A skill that must be remembered to be used is not integrated.

## Quick Install

```bash
# Clone the seed
git clone https://github.com/GrazianoGuiducci/d-nd-seed.git

# Copy a skill to your project
mkdir -p .claude/skills/autologica
cp d-nd-seed/plugins/d-nd-core/skills/autologica/SKILL.md .claude/skills/autologica/SKILL.md
```

The AI coder reads `.claude/skills/*/SKILL.md` automatically. The skill is active.

## Install All Core Skills

```bash
SEED="d-nd-seed/plugins/d-nd-core/skills"
LOCAL=".claude/skills"

for skill in $(ls $SEED); do
  mkdir -p "$LOCAL/$skill"
  cp "$SEED/$skill/SKILL.md" "$LOCAL/$skill/SKILL.md"
done
```

## What Each Skill Does

| Skill | When it activates | What it does |
|-------|-------------------|--------------|
| **autologica** | Direction unclear, corrections, loops | Ask the right question before acting |
| **auto-learn** | Something fails or repeats | Detect gap → diagnose → fix → crystallize |
| **cec** | Significant decision needed | 6-step sieve: observe → structure → expand → invert → crystallize |
| **capture-insight** | Operator shares strategic observation | Quick capture without breaking workflow |
| **memory-system** | Memory grows or gets stale | Compress, merge, archive by P6 principle |
| **system-check** | Need to verify infrastructure | Health checks: APIs, services, containers |
| **integrate-pattern** | New research function available | Extract universal pattern → operational use |
| **assertion-verifier** | Need to verify claims about the system | Define testable assertions → run → report |
| **eval** | Test if skills work correctly | Trigger accuracy + fidelity tests |
| **dream** | Memory exceeds thresholds | Consolidate, clean, prune stale memories |
| **autoresearch** | Skill tests show failures | Mutate-verify optimization loops |
| **propagator** | Something new produced | Cascade to all downstream targets |
| **version-check** | After AI coder updates | Map new features to system relevance |
| **cascade** | Something changed | Three levels: internal, external, emergent |

## Making Skills Auto-Activate

A skill file tells the AI coder *when* to activate. But the AI coder might forget. Two approaches:

### 1. Hooks (recommended)

Create a hook that detects the condition and injects the skill activation:

```bash
# .claude/hooks/my_trigger.sh (PostToolUse or UserPromptSubmit)
# Detect condition → inject skill activation message
```

Register in `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "bash \".claude/hooks/my_trigger.sh\"",
        "timeout": 3000
      }]
    }]
  }
}
```

### 2. Orchestrator (Gyroscope pattern)

A single PostToolUse hook that accumulates signals (errors, write/read ratio, content changes) and activates the right skill when thresholds are crossed. One hook, many skills.

The accumulator pattern:
- State file tracks session signals (persists across tool calls)
- After each action: update signals, check thresholds
- Threshold crossed → inject skill activation
- Each skill fires once per session (no repeats)

## Skill Structure

Every skill follows this structure:

```markdown
---
name: skill-name
description: "When to use this skill"
user-invokable: true
---

# Title

## What it does
## When it activates
## How it works
## Eval (trigger tests + fidelity tests)
```

The `description` field in frontmatter is what the AI coder uses to decide whether to activate. Write it as a trigger condition, not a feature description.

## Verifying Installation

```bash
# List installed skills
ls .claude/skills/*/SKILL.md

# Check if the AI coder sees them
# In Claude Code: the skills appear in the system-reminder as available skills
```

## The Principle

The skill is not the file. The skill is the pattern of behavior that the file encodes. If the behavior activates when needed without anyone remembering, the skill is integrated. If someone must remember, it is documentation — not a skill.
