# Evolution Transfer Protocol

> Transfer evolved logic without importing the wrong active state.

## Purpose

Use this protocol when a project, node, repo, agent, Lab, or previous session
has learned something useful and another context needs to inherit it.

The goal is not to copy everything. The goal is to transfer the part that can
live in the receiving context without breaking identity, authority, or current
work.

## When To Use

Use this when:

- importing methods from another node or agent;
- updating local boot from a shared system;
- promoting a Lab or project lesson into the seed;
- reading a recent packet/commit from another active workstream;
- turning a correction into a reusable rule;
- moving from local adapter knowledge to portable seed knowledge.

Do not use it as an excuse for broad sync. If the task is a simple local edit,
verify locally and proceed.

## The Loop

```text
1. identify the source line
2. read/fetch without merging active state
3. classify the material
4. extract portable logic
5. park foreign active work and residue
6. adapt to the receiver identity/function
7. update boot, memory, guard, or docs
8. verify local reentry
9. record the transfer
10. promote to seed only if the pattern is general
```

## Classification

Before using anything, classify it:

| Class | Meaning | Action |
|---|---|---|
| `portable_method` | General procedure or guard | Adapt locally |
| `source_evidence` | Useful history/fact | Cite as evidence, not command |
| `foreign_active_work` | Current work owned elsewhere | Keep read-only unless opened |
| `runtime_state` | Live service/data state | Verify locally before relying |
| `residue` | Visible but not active | Park, do not route from it |
| `secret_sensitive` | Token/private/auth material | Do not copy into memory/docs |

## Receiver Questions

Ask before transfer:

```text
Who produced this?
What did it solve there?
What is method vs state vs authority?
Who receives it here?
What must remain foreign?
What local boot or guard changes?
What exact check proves the receiver still knows who it is?
```

## Safe Output Forms

Good outputs:

- local configuration guide;
- boot/router update;
- memory pointer;
- guard document;
- local adapter;
- transfer packet;
- seed proposal.

Risky outputs:

- silent merge;
- workstream switch by recency;
- identity overwrite;
- public claim from foreign evidence;
- runtime/deploy action;
- copying secrets or private transcripts.

## Verification

At minimum:

```text
git status --short --branch
diff/stat review
syntax or test for changed tools
boot/reentry check if boot changed
clear record of what was imported and what was left out
```

If the receiving system has a boot router, run it with the transfer signal and
confirm the identity/role is still local to the receiver.

## Promotion Rule

Promote to seed only when the pattern is general:

```text
not tied to one path
not tied to one operator secret
not tied to one runtime state
prevents a recurring error
can be parameterized for a new project
has a generic verification shape
```

Local memory can teach the seed, but local memory is not the seed.

## Minimal Transfer Record

```text
source:
receiver:
why:
portable imported:
foreign/residue parked:
files changed:
verification:
what was not done:
next safe move:
```

## Relation To Boot Router

The boot router classifies the reentry.

The evolution transfer protocol classifies the inheritance.

Together:

```text
boot -> identify receiver -> read source -> classify inheritance -> adapt -> verify -> record
```

## Example

A VPS node adds improved boot functions. A local node should not merge the VPS
current workstream. It should:

```text
read the VPS branch
extract portable boot functions
leave VPS runtime work foreign
adapt paths and identity to local node
run local boot checks
record the transfer
```

Result:

```text
the local node evolves without becoming the VPS node.
```
