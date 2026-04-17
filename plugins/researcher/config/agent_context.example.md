# Agent Context — [Your Domain]

## Domain

Describe your domain in one paragraph. What are you studying? What data do you
have? What structures matter?

## Key concepts

Define the terms the agent needs. Short definitions, not essays.

- **Concept A** — one-line definition
- **Concept B** — one-line definition

## Tools available

List the experiment files the agent can run:

- `exp_example.py` — what it does, what it outputs
- Your own `exp_*.py` files go here

## Errors to avoid

Patterns you have already seen that look significant but are not:

- False positive pattern #1 — why it is not real
- Anti-pattern #2 — what to watch for

## Guardrails

- Do not generate data from scratch — use existing datasets or compute from raw
- Do not run experiments longer than 10 minutes
- Always compare against a null baseline (shuffle, random, noise)
- Write the report even if the result is null — null is data
