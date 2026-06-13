# Agent Runtime Translators

> The seed carries one logic, but each agent runtime needs a local adapter.

## Purpose

Claude Code, Codex, app-hosted AI coders, Cursor, Copilot, Gemini, and
chat-only models can all read project files, but they do not all execute the
same surfaces natively.

The Seed is not the `.claude` directory. Installed Seed has a neutral `.seed`
manifest for recognition and plan reading. `.claude` is the native Claude Code
target and compatibility surface. The portable Seed source is the capability
logic in this repository. See
`docs/agent_neutral_seed_surface.md` for the agent-neutral layer model.

The Seed should not pretend these runtimes are identical. It should transmit the
same capability logic through the right local form:

- Claude Code can use `.claude/`, hooks, settings, and skills natively.
- Codex can read the same files and execute shell/code tasks, but needs an
  explicit guide that translates `.claude` behavior into Codex workflow.
- App-hosted AI coders may expose workspace instructions, app-local
  configuration, lifecycle hooks, skills, plugins or memory surfaces. Use
  `docs/app_runtime_adapter.md` to classify those surfaces before install.
- Generic chat runtimes can use the docs and thinker skills, but usually cannot
  run hooks.

## Support Status

Each installable capability can declare `agent_support`:

```json
{
  "agent_support": {
    "claude-code": { "status": "native" },
    "codex": {
      "status": "adapter",
      "adapter": "docs/agent_runtime_translators.md#codex-reading-claude-surfaces"
    },
    "generic": { "status": "documented" }
  }
}
```

Statuses:

- `native`: the runtime can use this capability directly.
- `adapter`: the runtime can use the logic through a documented translation.
- `documented`: the runtime can read the capability as guidance, but it is not
  mechanically wired.
- `unsupported`: the capability should not be selected for that runtime.

## Codex Reading Claude Surfaces

When Codex enters a Seed-enabled repo:

1. Read `README.md`, `GUIDE.md`, and `llms.txt` for orientation.
2. If `.seed/seed_install_plan.json` exists, treat it as the installed
   capability map. Fall back to `.claude/seed_install_plan.json` only for
   older installs.
3. Read `.seed/seed_profile.json` to know node identity, intent, risk, and
   install mode. Fall back to `.claude/seed_profile.json` only for older
   installs.
4. Read `.claude/skills/*/SKILL.md` as capability manuals, not as automatic
   native skill activation.
5. Treat `.claude/hooks/*.sh` as executable reference workflows. Do not assume
   they have fired automatically.
6. Before doing work that a hook would normally guard, manually apply the hook's
   logic:
   - safety guard before destructive shell operations;
   - system awareness before broad action;
   - system awareness snapshot before plans or edits on broad, public,
     post-compact, correction, field-reentry, or multi-repo work;
   - pre/post compact logic before context transitions;
   - cascade checks after public/site/docs changes.
7. If a capability has `agent_support.codex.status = adapter`, follow its
   adapter notes before acting.

Codex should not rewrite `.claude` files into a separate Codex identity unless
the operator asks. The first translation is behavioral: read the same source,
execute the equivalent discipline.

## Claude Code Reading Codex Surfaces

When Claude Code enters a repo previously operated by Codex:

1. Read `AGENTS.md`, `tm7` packets, or local Codex notes if present.
2. Distinguish Codex session memory from Seed invariants.
3. Import only reusable methods into `.claude` memory or skills.
4. Keep Codex-specific tool assumptions out of native Claude hooks unless a
   portable shell implementation exists.
5. Use the capability registry to decide whether a Codex-derived behavior
   becomes:
   - native Claude Code hook/skill;
   - adapter note;
   - documentation only;
   - unsupported.

## Planner Behavior

The installer planner accepts an agent runtime:

```bash
node scripts/installer_option_router.js profiles/example.json --agent=codex
node scripts/installer_option_router.js profiles/example.json --agent=claude-code
```

If no agent is declared, the default is `claude-code` for backward
compatibility.

Profiles can declare:

```json
{
  "agent_runtime": "codex"
}
```

The same capability can remain selected for both runtimes, but its support
status tells the agent how to use it.

Ready profiles:

- `profiles/example-claude-code.json`: native `.claude` hooks/settings/skills;
- `profiles/example-codex.json`: Codex reads `.claude` as source logic and uses
  this guide as adapter;
- `profiles/example-app-runtime.json`: app-hosted runtime using the closest
  supported adapter plus explicit app-host metadata;
- `profiles/example-publisher.json`: public-surface work, usable by either
  runtime when paired with `--agent=...` or `agent_runtime`.

## Rosetta Rule

Do not duplicate the capability into one file per agent unless the mechanics
really diverge. Prefer this translation order:

1. one capability entry in `capabilities/registry.json`;
2. one source implementation/doc/skill/hook;
3. `agent_support` statuses for each runtime;
4. an adapter note when mechanics differ;
5. separate runtime-specific implementation only when native behavior cannot be
   represented by the common source.

The source of truth remains the capability. The runtime adapter is the
pronunciation.

## Recognition Rule

An agent should be able to recognize the Seed even if it does not use `.claude`
natively:

```text
read Seed source docs -> read selected capability map -> classify runtime
support -> map native/adapted/documented/unsupported surfaces -> act through
the local runtime boundary
```

If an agent sees `.claude` files, it should treat them as generated or
installed Seed surfaces, not as proof that it must identify as Claude Code.
Claude Code uses them natively; other runtimes translate them.

## Boundary

Translators do not create false equivalence. A hook that Claude Code runs
automatically may be only a manual checklist for Codex. A Codex workflow that
uses patch/shell tools may be only a documented method for Claude Code unless a
native hook or skill exists.
