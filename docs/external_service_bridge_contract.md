# External Service Bridge Contract

> Status: recent candidate / optional Seed capability.
> Scope: neutral API/service contract for repos and external systems.

## Purpose

External systems may need to request a service from another repo, node or
provider. In D-ND deployments, one provider may be THIA. The Seed may describe
the neutral contract, but it must not expose or activate provider runtime.

This document defines the boundary for future API-like bridges.

## Non-Goals

This contract does not define:

```text
live endpoints;
auth secrets;
THIA runtime topology;
private service names;
background jobs;
automatic repo-to-repo writes;
deployment behavior;
public pricing or product claims.
```

## Call Principle

A repo should not call or mutate another system by path knowledge or implicit
trust. It should create a bounded service request that the provider can accept,
reject, prepare or execute behind a gate.

Default behavior is:

```text
read/observe first;
prepare before execute;
execute only with provider-side authority;
return a receipt for every accepted side effect.
```

## Request Shape

```text
request_id:
requester:
provider:
service_id:
intent:
mode: observe | plan | prepare | execute_with_gate
input_contract:
data_classification: public | neutral | private | secret-adjacent | secret
allowed_data:
forbidden_data:
auth_scope:
rate_or_budget_limit:
side_effects_requested:
expected_output:
receipt_required:
rollback_or_retraction:
```

## Response Shape

```text
request_id:
status: accepted | rejected | needs_gate | prepared | executed | failed
result:
evidence:
side_effects_performed:
mutations:
provider_gate:
next_action:
errors:
receipt_id:
```

## Provider Gate

The provider owns the final authority for:

```text
write access;
publication;
deployment;
runtime service calls;
credential use;
network calls;
billing-impacting calls;
private data exposure.
```

The requester may propose or prepare these actions, but cannot assume them.

## THIA Compatibility

When a THIA-owned deployment implements a service bridge, THIA should expose
only the reviewed service contract and provider gate. The Seed carries the
portable contract so external systems can prepare compatible requests without
knowing private THIA internals.

## Receipts

Every accepted request should produce a receipt:

```text
what_was_requested:
what_was_done:
what_was_not_done:
source_of_authority:
evidence:
side_effects:
rollback_or_retraction:
next_verification:
```

Receipts let external systems coordinate without merging their memory, identity
or authority boundaries.
