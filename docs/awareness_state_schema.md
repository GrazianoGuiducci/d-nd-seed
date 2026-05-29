# Awareness State Schema

> Scope: canonical state contract for D-ND awareness orchestration.
> Purpose: give hooks, skills, boot routers, plans, and runtime adapters one
> shared language before action.

Awareness is not a feeling and not a long briefing. It is the minimum state a
node exposes so the next move can be chosen, verified, and remembered.

## Contract

Every broad, public, reentry, correction, multi-repo, or seed-changing action
should be able to produce this state:

```json
{
  "schema": "dnd.awareness_state.v1",
  "timestamp": "YYYY-MM-DDTHH:mm:ssZ",
  "node": {
    "id": "node-id",
    "runtime": "claude-code|codex|cursor|generic",
    "profile": ["coder", "operator"],
    "intent": ["coding", "maintenance"]
  },
  "transition": {
    "boot_class": "new_instance|post_compact|post_crash|unexpected_correction|field_reentry|pre_compact|unclassified",
    "action_gate": "observe_only|stop_for_validation|diagnose_only|act_one_bounded_step|escalate_to_operator|publish_blocked",
    "trigger": "operator message, hook event, compact return, crash signal, or runtime event"
  },
  "surface": {
    "active": "repo, site, service, dataset, document, or unknown",
    "source_of_truth": "path, URL, registry, profile, or operator statement",
    "adjacent": ["related surfaces that may need cascade"],
    "boundary": ["what must not be touched from this state"]
  },
  "evidence": {
    "verified": ["facts read or tested in this session"],
    "memory": ["facts remembered but possibly stale"],
    "inferred": ["claims derived from named evidence"],
    "unknown": ["gaps that must not be filled by invention"]
  },
  "capabilities": {
    "available": ["capability ids visible in the install plan or local context"],
    "selected": ["capabilities chosen for this move"],
    "blocked": [
      {
        "capability": "id",
        "reason": "risk, missing source, unsupported runtime, or operator gate"
      }
    ]
  },
  "risk": {
    "side_effects": ["files, repos, services, public surfaces, secrets"],
    "regression": ["known ways this can break"],
    "privacy": ["private material that cannot propagate"],
    "confidence": "low|medium|high"
  },
  "movement": {
    "possibility_field": ["paths still open before collapse"],
    "non_possible": ["paths blocked by evidence, boundary, or operator rule"],
    "next_move": "smallest safe next move",
    "verification": "test, readback, diff, smoke check, or operator validation",
    "cascade_targets": ["docs", "tests", "registry", "memory", "public copy"]
  },
  "memory_update": {
    "needed": false,
    "kind": "none|lesson|correction|handoff|seed_candidate",
    "condition": "what must be true before writing memory"
  }
}
```

## Required Fields

The full JSON shape is useful for automation, but the minimum human-readable
snapshot is:

```text
boot_class:
action_gate:
active_surface:
operator_intent:
source_of_truth:
verified:
unknown:
boundary:
selected_capabilities:
risk:
next_move:
verification:
cascade_targets:
```

If one of these fields is unknown, write `unknown` and name what would make it
known. Do not substitute memory.

## Action Gates

| Gate | Meaning | Opens When |
|---|---|---|
| `observe_only` | read, inspect, map, no mutation | surface is unclear or first contact |
| `stop_for_validation` | pause before action | source/gate/operator intent is not validated |
| `diagnose_only` | inspect failure and bound side effects | crash, timeout, broken run, unexpected result |
| `act_one_bounded_step` | make one scoped change | source, boundary, and verification are clear |
| `escalate_to_operator` | ask the operator | missing authority, private boundary, high ambiguity |
| `publish_blocked` | no public release | claim/copy/security/review gate failed |

Gates are not bureaucracy. They are how the system prevents a powerful next
move from becoming blind.

## Capability State

A capability should not be treated as active just because it exists. It is
active only when:

1. it is selected by the install plan or local context;
2. the runtime can execute or adapt it;
3. its trigger matches the event;
4. its required evidence is available;
5. its risk does not exceed the current gate.

Otherwise it remains available, blocked, or deferred.

## Autologic Update

After action and verification, update the state:

```text
result -> what changed -> what failed or held -> missing condition ->
guard/rule/cascade candidate -> next state
```

This is the self-application loop. The state observes the work, then updates
the conditions for the next work.

## Eval

Trigger tests:

- new instance or day-start -> state includes `new_instance` and
  `stop_for_validation`;
- operator correction -> state includes `unexpected_correction` and
  selected `autologica` / `assertion-verifier` when installed;
- public copy change -> state includes public side effects and
  `publish-safe` or `assertion-verifier` when installed;
- private source candidate -> state includes `private-to-seed` boundary and
  no raw private content in `verified`.

Fidelity tests:

- unknown fields remain explicit unknowns;
- every selected capability appears in the available capability set or is
  marked as adapted from local context;
- every act gate names its verification;
- private material is represented by invariant only, not copied content.

