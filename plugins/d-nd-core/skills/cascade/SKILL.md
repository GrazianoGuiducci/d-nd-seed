---
name: cascade
description: "Three levels of propagation: internal (within the change), external (binding: seed, site, nodes), emergent (discoveries during propagation). Activate after every significant modification."
user-invocable: true
---

# Cascade — Three-Level Propagation

When something changes, three things happen:
1. The change matures within itself (internal)
2. The change propagates where it must (external)
3. During propagation, new possibilities emerge (emergent)

## Level 1 — Internal Cascade

Before propagating, the change must mature.

**Questions to ask:**
- Is this a semi-duplicate of something else? → Unify or distinguish
- Does it make something obsolete? → Update or remove the old
- Does it open new possibilities? → Note as emergent, don't implement yet
- Is a tool maturing into an entity? → Evaluate if full automation is warranted
- Do existing skills/hooks need updating? → Update descriptions, triggers, evals
- Is the system's self-description still correct? → Update instruction files

## Level 2 — External Cascade (binding)

The change must arrive where it needs to. These are mandatory.

```
Function/skill/hook created or modified
  ├─ In the seed? → neutral version, zero specific references
  ├─ On the site? → spec to the responsible node
  ├─ Config files? → update references
  ├─ Other nodes? → message via collaboration channel
  ├─ Shared rules? → if applicable to all nodes
  ├─ Local memory? → update memory files
  └─ Settings? → if it's a hook, verify registration
```

**Corrections:**
```
Correction received
  ├─ Executable rule (when X → do Y)
  ├─ Local memory → update
  ├─ Seed kernel? → if universal
  ├─ Other nodes? → if cross-node
  └─ /auto-learn → activate
```

## Level 3 — Emergent Cascade

During propagation, reading files to evaluate where to propagate, you may discover:

- **Refinements**: the file you're reading suggests an improvement
- **Maturation**: a script becoming a skill, a skill becoming an autonomous entity
- **Unification**: two things that did almost the same thing merge
- **New entities**: combining existing functions produces something new
- **Logic refinements**: the system can automate more at that point

These are NOT implemented immediately. Note them as potential and evaluate
after the current cascade is complete. Otherwise: infinite cascade.

**Rule**: complete the current cascade, then return to the emergents.

## The three levels feed each other

```
Internal → External → Emergent → (new) Internal
```

The cascade is a cycle. But each round must complete before the next.

## Quick checklist

**Internal:**
- [ ] Is it a duplicate? Unify
- [ ] Does it make something obsolete? Update
- [ ] Do existing skills/hooks need adjustment?

**External:**
- [ ] Does the seed need this (neutral version)?
- [ ] Does a config file need updating?
- [ ] Do other nodes need to know?
- [ ] Is local memory updated?

**Emergent:**
- [ ] Did I notice something during propagation? Note it, don't implement now.

## Boot knowledge — two levels

The system has two levels of knowledge:

1. **What you must know** — loaded in memory, read at boot. The modus, anti-patterns, current direction. Small, essential.
2. **Where to find it** — pointers. Don't load the full architecture at boot. Know it exists and where to find it when needed.

The memory index (MEMORY.md or equivalent) should clearly separate these two levels.

## Eval

## Trigger Tests
# "cascade" or "propagate" -> activates
# New function created -> activates
# Config modified -> activates
# Operator correction -> activates
# "deploy" -> does NOT activate

## Fidelity Tests
# Given a new function: identifies all 3 cascade levels
# Given a correction: traces to memory + seed + config
# Emergent discoveries are NOTED, not implemented during cascade
# Cascade completes before starting a new one
