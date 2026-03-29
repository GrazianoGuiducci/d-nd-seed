---
name: autoresearch
description: "Auto-optimize skills through mutate-verify loops. Use when skill tests show failures or when asked to optimize a skill."
user-invocable: true
---

# Autoresearch — Skill Self-Optimization

The system improves its own skills through iterative loops.

## Process

### 1. Baseline
Run /eval on the target skill. Record trigger accuracy and fidelity.

### 2. Diagnosis
For each failure:
- Trigger miss → description too narrow
- False trigger → description too broad
- Fidelity fail → instructions in body incorrect

### 3. Mutation
ONE change per iteration. Never more than one variable at a time.
- For trigger: modify the description
- For fidelity: modify the body
- For stale eval: update the tests

### 4. Re-eval
Run /eval again. Compare with baseline:
- Improved? Keep the mutation.
- Same or worse? Revert, try a different mutation.

### 5. Report
Baseline → final score, what changed, how many iterations.

## Rules
- One variable at a time
- The eval is the judge, not your opinion
- Max 5 iterations — if it does not converge, flag for human review
- Never change the purpose of the skill — only refine trigger/fidelity

## Eval

## Trigger Tests
# "optimize my deploy skill" -> activates
# "skill X is failing tests" -> activates
# "improve skill accuracy" -> activates
# "run eval" -> does NOT activate (that is /eval)
# "deploy" -> does NOT activate

## Fidelity Tests
# Given skill with 2 trigger failures: mutates description, re-tests, reports improvement
# Given skill with 0 failures: reports "already optimal, no mutations needed"
# Given skill that does not converge in 5 iterations: flags for human review
