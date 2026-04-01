---
name: cascade
description: "When something changes, identify what else must change. Propagate updates across skills, hooks, configs, documentation, other nodes. Activate after every significant modification."
user-invocable: true
---

# Cascade — Conscious Propagation of Changes

When something in the system changes, other things must change as a consequence.
This skill identifies the consequences and propagates them.

## When it activates

- After adding/modifying a function or tool
- After adding/modifying a skill or hook
- After crystallizing a lesson or correction
- After modifying a config file (CLAUDE.md or equivalent)
- When the operator says "cascade" or "propagate"

## The cascades

### New function/tool
```
Function created
  → Does it belong in the seed? If yes: create neutral version
  → Does it need documentation? If yes: write guide
  → Does it need a hook/skill? If yes: create and install
  → Does the config need updating? If yes: update references
  → Do other nodes need to know? If yes: message them
```

### New lesson/correction
```
Correction received
  → Executable rule (when X → do Y)
  → Save in local memory
  → Does it apply to all nodes? If yes: propagate to shared rules
  → Does it belong in the seed? If yes: update kernel or skill
```

### Config change
```
Config modified
  → Which other configs depend on this?
  → Do other nodes need the same change?
  → Does the seed need updating?
```

### New skill/hook
```
Skill or hook created/modified
  → Is it installed in the active path?
  → Does it have eval tests?
  → Should it be in the seed? If yes: add neutral version
  → Does the settings file need updating?
```

## Quick checklist

After every significant modification:

- [ ] Does the seed need to reflect this?
- [ ] Does a config file need updating?
- [ ] Do other nodes need to know?
- [ ] Is there a skill/hook affected?
- [ ] Is local memory updated?

## The principle

Every change carries the information of where it must propagate.
The cost of not propagating is higher than the cost of propagating.

## Eval

## Trigger Tests
# "cascade" or "propagate" -> activates
# New function created -> activates
# Config modified -> activates
# "deploy" -> does NOT activate

## Fidelity Tests
# Given a new function: identifies all cascade targets
# Given a correction: traces to memory + config
# Never misses the seed check
