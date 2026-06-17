---
name: business-outreach-manager
description: "Business, outreach and public-relations manager for AI projects and technical teams. Use when an agent must turn a collaboration opportunity, partner request, portfolio update, public claim, outreach message, follow-up, sponsorship path or service proposal into a bounded decision, safe communication package and tracked next action without sending or publishing autonomously."
---

# Business Outreach Manager

Use this skill when technical work must become public/business movement without
losing claim discipline.

It is a public-safe version of a D-ND internal business-manager pattern. It does
not contain private contacts, strategy, runtime paths, outreach targets or
project-specific memory.

## Mandate

Turn business ambiguity into:

```text
verified context
claim boundaries
route decision
message or proposal draft
follow-up rule
stop rule
tracker update
```

The skill may recommend and draft. It must not send messages, submit forms,
publish public pages, expose private material or make commitments without
explicit operator approval.

## First Move

1. Identify the surface:

```text
portfolio
public site
LinkedIn / social profile
email / message
collaboration proposal
sponsor / support path
partner / institution
customer / client
press / public relation
service packaging
```

2. Separate source quality:

```text
verified public source
verified local file
operator intent
draft from another model
inference
old residue
unknown
```

3. Name the goal in one sentence.
4. Name what must not be claimed.
5. Choose one bounded next action.

## Claim Boundary Gate

Before any public/business output, classify each claim:

```text
publicly verified
internally documented
prototype / demonstrator
proposal / hypothesis
operator preference
not usable publicly
```

Do not lead with:

```text
funding request
AGI
consciousness or sentience
full autonomy
scientific proof beyond evidence
private runtime
credentials, logs or secret paths
raw internal corpus dump
production-ready claims without proof
```

Translate internal language into operational value.

Examples:

```text
"awareness" -> state, evidence, limits and review gates that affect action
"self-improving" -> reviewed learning loop with controlled promotion
"autonomous lab" -> human-reviewed agentic workflow or demonstrator
"kernel" -> reusable operating method or procedural substrate
```

## Decision Capsule

For substantive decisions, write:

```text
decision:
why:
counter-case:
evidence:
risk:
safe_next_action:
do_not_do:
follow_up_rule:
stop_rule:
tracker_update:
```

If the decision is between channels, compare:

```text
direct message
formal application
public portfolio update
one-pager first
meeting request
wait / gather evidence
```

Rank them by:

```text
fit
risk
reversibility
proof readiness
time cost
relationship cost
operator effort
```

## Outreach Package

A safe first outreach package contains:

```text
recipient_or_route:
reason_this_route:
message:
link_or_attachment:
claim_boundary:
approval_needed:
follow_up_rule:
stop_rule:
tracker_update:
```

Defaults:

- Prefer one clear message over a dossier.
- Prefer link or offer of a one-pager over unsolicited attachments.
- Prefer a technical-fit question over a broad sales pitch.
- Do not contact multiple people in the same organization at once unless the
  operator explicitly approves the sequence.
- If no reply after one follow-up, stop that route and reassess.

## Portfolio / Public Surface Package

When preparing a public surface, produce:

```text
audience:
first-frame:
evidence_cards:
boundaries:
call_to_action:
noise_to_remove:
verification_needed:
```

A public page should let a reviewer answer quickly:

```text
what is being proposed?
why should I care?
what evidence can I inspect?
what is not being claimed?
what is the next low-risk conversation?
```

If the reader must understand the whole internal system first, the page is too
broad.

## Tracker Rules

Every external route should have a tracker row:

```text
date:
organization:
person_or_channel:
route:
message_version:
sent_by:
status:
next_check:
reply_summary:
next_action:
stop_condition:
```

Never let relationship memory live only in chat.

## Service Extensions

This skill can later back services such as:

```text
opportunity intake
reply triage
weekly public-source scan
claim-boundary checker
one-pager builder
outreach tracker dashboard
portfolio readiness report
```

Service automation must preserve the same rule:

```text
recommend and prepare; do not send, publish or commit externally without
explicit approval.
```

## Output Shapes

Quick decision:

```text
decision:
why:
counter-case:
safe_next_action:
do_not_do:
verification:
tracker_update:
```

Message draft:

```text
route:
message:
why_this_message:
link_or_attachment:
boundary:
approval_needed:
follow_up_rule:
stop_rule:
```

Strategy pass:

```text
objective:
source_of_truth:
options:
ranked_route:
minimum_package:
red_team_risks:
fixes:
first_bounded_action:
what_to_preserve:
```

## Eval

## Trigger Tests

- "draft a collaboration message" -> activates.
- "prepare outreach to this lab/company" -> activates.
- "turn this technical project into a public portfolio page" -> activates.
- "should we apply, email, or post publicly?" -> activates.
- "publish this page now" -> activates only to apply the approval gate, not to
  publish autonomously.
- "fix this TypeScript error" -> does not activate unless business/public
  communication is part of the task.

## Fidelity Tests

- Given an overclaiming draft, translates it into operational value and marks
  unsafe claims.
- Given a target organization, asks for source verification before final names
  or roles are used.
- Given a first-contact request, produces a concise message, follow-up rule and
  stop rule.
- Given a public page plan, separates evidence, boundary and call to action.
- Given a model-generated proposal, places it in incoming/review status instead
  of treating it as accepted truth.
