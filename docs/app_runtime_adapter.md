# App-Hosted Runtime Adapter

> Use this when an AI coding app hosts the agent and exposes local project
> configuration, workspace instructions, hooks, skills, plugins or persistent
> memory surfaces.

## Purpose

Some AI coders run as a terminal or editor extension. Others run inside an app
that adds its own local surfaces around the project. The Seed should not assume
that every runtime installs or executes hooks, skills and memory in the same
way.

This guide describes the neutral adapter path for app-hosted runtimes. It does
not define a new installer mode yet. It explains how the app should present its
environment to Seed so the existing planner can produce a bounded install plan.

## What The App Must Declare

Before running install or update, the app or operator should provide a profile
that declares:

- runtime family: the closest supported runtime, such as `codex`,
  `claude-code`, `cursor` or `generic`;
- host type: `app`;
- project directory;
- local configuration directory used by the app, if any;
- whether workspace instructions are supported;
- whether hooks are supported and which lifecycle events are available;
- whether skills or plugins are native, adapted or only documented;
- whether memory is project-local, app-local or both;
- command execution boundary;
- file write boundary;
- network, secrets, publish and runtime/service boundary.

If any of these are unknown, stay in read-only planning mode.

## Current Installer Posture

Until the planner has a stable `app` runtime family, use the closest existing
runtime profile and add app-host fields as metadata.

For a Codex-like app runtime, start from `profiles/example-app-runtime.json`.
It uses `agent_runtime: "codex"` so the current registry can route
capabilities through the existing Codex adapter, while the extra app fields
record what the host can actually do.

Run:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example-app-runtime.json
node scripts\seed_plan.js profiles\example-app-runtime.json
```

Only proceed to write-mode install after the plan and target boundary are
understood.

## App Surface Contract

An app-hosted runtime may have three separate layers:

```text
Seed source       -> portable capability logic
project install   -> generated project-local memory, hooks, skills and plan
app host surface  -> app-specific instructions, hooks, plugins or state
```

Keep these layers separate.

Seed source should not receive host-specific paths, active local state,
private transcripts, local node names or app session residue.

Project install should receive generated surfaces only inside the target
project boundary selected by the profile.

App host surface may adapt the generated plan into the app's own mechanisms,
but that adaptation belongs to the app or project unless it becomes a proven
portable invariant.

## After Install

After installation, the app-hosted agent should read:

```text
.claude/seed_profile.json
.claude/seed_install_plan.json
.claude/CLAUDE.md
.claude/MEMORY.md
```

Then it should classify each capability:

- native in this app;
- adapted from generated Seed logic;
- documented only;
- unsupported in this app.

Do not claim hook or skill automation until the app host has verified it.

## Promotion Rule

If repeated app-hosted installs show the same stable pattern, promote only the
portable invariant:

- profile fields that describe app-hosted runtimes;
- planner support for a distinct runtime family;
- registry support metadata;
- dry-run tests for generated app surfaces;
- documentation for boundaries and lifecycle events.

Do not promote local app state, machine paths, active packets, temporary
workstreams, private conversations or host-specific names.

## Boundary

This adapter is documentation. It does not authorize global app configuration,
service installation, scheduler setup, publishing, secrets access or runtime
mutation.

The plan and dry-run remain the authority before writes.
