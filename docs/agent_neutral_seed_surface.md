# Agent-Neutral Seed Surface

> Scope: how any AI coding system can recognize and consume Seed capability
> logic without needing to identify as Claude Code first.

## Problem

Seed supports multiple runtimes conceptually and now writes a neutral manifest,
but much of the executable install surface is still Claude-shaped:

```text
.seed/seed_profile.json
.seed/seed_install_plan.json
.seed/adapter_notes.md
.claude/CLAUDE.md
.claude/MEMORY.md
.claude/hooks/
.claude/skills/
.claude/seed_install_plan.json
```

That works well for Claude Code, but it can hide the system from agents that
could use the same logic through another runtime shape. Codex, Cursor, Copilot,
OpenCode, Gemini, OpenRouter/eHermes-backed agents, app-hosted AI coders and
generic file-reading agents should not need to "pretend to be Claude" in order
to recognize the Seed.

The goal is capability parity at the logic level, not false equivalence at the
mechanics level.

## Core Rule

```text
Seed source is agent-neutral.
Runtime surfaces are adapters.
Claude Code receives `.claude` natively.
Other coders consume the same capability logic through their own adapter.
```

Do not duplicate the capability per runtime unless mechanics truly diverge.
The portable source remains one; the runtime adapter is the pronunciation.

## Layer Model

Use five layers when deciding where Seed information belongs:

| Layer | Meaning | Examples |
|---|---|---|
| `seed_source` | Portable capability logic in this repo | `docs/`, `capabilities/`, `templates/`, `plugins/`, `kernels/` |
| `install_manifest` | Runtime-neutral installed capability map | `seed_profile`, `seed_install_plan`, selected capability ids |
| `runtime_adapter` | How the host consumes the manifest | Claude hooks, Codex manual gates, app-local plugin/skill surfaces |
| `project_memory` | Project-specific current state | local boot/current-state files inside the target project |
| `shared_or_portable` | Cross-node coordination or new Seed capability | TM7 packet, future Seed promotion |

The installation flow should be understood as:

```text
seed_source -> install_manifest -> runtime_adapter -> project_memory
```

not:

```text
Seed == .claude
```

## Current Compatibility Position

The writer scripts generate `.seed` as the runtime-neutral recognition surface
and `.claude` as the native Claude Code target and compatibility carrier.
Treat `.claude` as an adapter, not as the identity of the Seed.

For non-Claude runtimes:

```text
read README/GUIDE/llms
read docs/agent_runtime_translators.md
read .seed/seed_install_plan.json if present
classify native/adapted/documented/unsupported capabilities
map generated Claude-shaped surfaces into local runtime behavior
```

Codex may manually consume the hook discipline. App-hosted coders may map it to
app workspace instructions, plugin surfaces, skills, or memory. Generic agents
may consume it as documented operating protocol.

## Target Direction

Installer work should continue separating neutral manifest generation from
runtime-specific emission.

Current minimal shape and recommended expansion:

```text
.seed/
  seed_profile.json
  seed_install_plan.json
  seed_update_plan.json
  adapter_notes.md
  memory/
  capabilities/

.claude/
  CLAUDE.md
  MEMORY.md
  hooks/
  skills/

.codex/
  AGENTS.md or app-local equivalent
  skills/plugins/config when supported

other runtime target:
  host-supported instruction, memory, hook or plugin surface
```

This is a target architecture, not a claim that current scripts already write
all of these surfaces.

## Runtime Parity Contract

Every runtime should be able to answer:

```text
runtime:
native_surfaces:
adapted_surfaces:
documented_only:
unsupported:
selected_capabilities:
manual_equivalents:
verification_before_action:
memory_location:
update_boundary:
```

The answer may differ by runtime. The invariant should not.

Examples:

```text
Claude Code:
  native: .claude hooks/settings/skills
  manual_equivalent: usually not needed for native hooks

Codex:
  native: repo files, shell, local tools, app skills/plugins when available
  adapted: read Seed logic and manually apply hook gates

App-hosted coder:
  native: whatever the app exposes
  adapted: map Seed manifest to app workspace instructions/plugins/memory

Generic/OpenRouter/eHermes-backed coder:
  native: prompt/file reading, maybe tool calls through host
  documented: operating discipline, gates, verification, memory placement
```

## Memory Placement

Use the narrowest correct consumer:

```text
project_local:
  project current state, page/source truth, local QA state

workspace_root:
  cross-project entry gate and coordination rules

coder_adapter:
  runtime-specific behavior: .claude, .codex, app-local config, etc.

shared_coordination:
  cross-node packets, validation notices, delivery receipts

portable_capability:
  normalized reusable invariant in Seed after proof
```

Do not store project current state in Seed. Do not store portable capability
truth only inside a runtime adapter. Do not copy one runtime's private state into
another runtime's global memory.

## Migration Rule

When changing Seed install behavior:

1. Keep Claude Code compatibility.
2. Add neutral manifest/read path before changing writer targets.
3. Add runtime-specific emission only after dry-run validation.
4. Mark each capability as native, adapted, documented or unsupported per
   runtime.
5. Do not claim hooks run automatically unless the host proves it.

## Boundary

This document does not authorize a mass installer rewrite. It defines the
target organization so future work can make Seed easier for every agent to
recognize while preserving the current Claude Code path.
