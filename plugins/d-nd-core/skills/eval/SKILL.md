---
name: eval
description: "Evaluate skills — trigger accuracy, fidelity, and value. Use when asked to test skills, run evals, or check if skills work."
user-invocable: true
---

# Eval — Skill Testing

Every skill has a section ## Eval with:
- **Trigger Tests**: given a prompt, should the skill activate? YES/NO
- **Fidelity Tests**: given an input, is the behavior correct?

To test: read every SKILL.md, find ## Eval, verify each test case.
Output per skill: Trigger X/Y, Fidelity X/Y, Issues found.

## Eval

## Trigger Tests
# "test my skills" -> activates
# "run eval" -> activates
# "check skill health" -> activates
# "deploy to production" -> does NOT activate

## Fidelity Tests
# Given skill with 5 trigger tests: reports 5/5 or X/5 with details
# Given skill without ## Eval: reports NO EVAL warning
# Given all skills passing: reports summary with 0 issues
