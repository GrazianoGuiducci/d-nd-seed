# Installer Option Router

> How the seed can keep evolving without turning installation into a noisy
> dump of every historical capability.

## Problem

The seed contains stable invariants, recent improvements, domain tools,
plugins, hooks, skills, templates, and patterns imported from live systems such
as THIA. If every promoted capability is presented equally, installation
becomes confusing:

- new ideas can hide foundational rules;
- old ideas can remain visible after a better pattern exists;
- profile-specific tools can look universal;
- experimental functions can be mistaken for defaults;
- an operator cannot quickly see what should be installed for a given context.

The installer needs a routing layer. It should not only ask "what exists?", but
"what is the best option for this node, now, with this intent and risk level?"

## Principle

Treat installable material like a targeted funnel:

1. identify the observer/context;
2. show the invariant base first;
3. recommend the current stable path for that context;
4. expose recent or advanced capabilities with clear maturity;
5. hide deprecated or superseded material unless migration/recovery needs it.

The seed can evolve quickly if every capability carries enough metadata to be
ranked, filtered, and explained.

## Capability Strata

| Stratum | Meaning | Installer behavior |
|---|---|---|
| `core_invariant` | Foundational rule or guard that should survive across nodes | Always visible, installed by default unless explicitly disabled |
| `stable_default` | Mature capability recommended for common installs | Recommended for matching profiles/intents |
| `contextual` | Useful only for specific roles, domains, or workflows | Shown when profile or intent matches |
| `recent_candidate` | Newer pattern that fits the current system direction but needs more use | Highlighted as recent, opt-in by default |
| `experimental` | Promising but not yet validated outside its source context | Expert/advanced only, clear warning |
| `legacy_or_superseded` | Older pattern kept for migration, audit, or recovery | Hidden by default, visible in migration mode |

## Metadata Each Capability Should Carry

Use this shape for skills, hooks, plugins, templates, docs, and Lab patterns
when they become installable choices.

```json
{
  "id": "memory-system",
  "type": "skill",
  "stratum": "stable_default",
  "maturity": "established",
  "profiles": ["coder", "researcher", "operator"],
  "intents": ["memory", "continuum", "reentry"],
  "risk": "safe",
  "visibility": "recommended",
  "introduced": "2026-03-06",
  "reviewed": "2026-05-26",
  "supersedes": [],
  "superseded_by": null,
  "requires": [],
  "conflicts_with": [],
  "why": "Preserves useful state across sessions and compaction."
}
```

Minimum required fields:

- `id`: stable name used by installer and docs;
- `type`: `hook`, `skill`, `plugin`, `template`, `doc`, `lab_pattern`, or
  `kernel`;
- `stratum`: one of the strata above;
- `maturity`: `established`, `stable`, `emerging`, `candidate`,
  `experimental`, or `deprecated`;
- `profiles`: roles that naturally need it;
- `intents`: work intents it supports;
- `risk`: `safe`, `writes_files`, `uses_network`, `uses_secrets`,
  `publishes`, `runtime`, or `destructive`;
- `visibility`: `default`, `recommended`, `optional`, `advanced`, or
  `hidden`;
- `why`: one sentence explaining why this capability is offered.

## Installer Modes

| Mode | Purpose | Includes |
|---|---|---|
| `minimal` | Birth a safe node with the least moving parts | `core_invariant` only |
| `recommended` | Default mode for most users | `core_invariant` + matching `stable_default` |
| `contextual` | Build for a declared role or workflow | Recommended set plus matching `contextual` capabilities |
| `recent` | Review what recently changed | Matching defaults plus visible `recent_candidate` items |
| `expert` | Operator review of advanced functions | All non-hidden capabilities except deprecated by default |
| `migration` | Upgrade an older install | Deprecated/superseded mapping, `.new` outputs, review notes |

## Context Axes

The installer should route by these axes:

- `profile`: coder, researcher, thinker, operator, dev-node, lab, publisher,
  team;
- `intent`: coding, research, Lab generation, site/copy, SEO/AI visibility,
  inter-node coordination, publishing, business/support;
- `surface`: local project, VPS/runtime, public site, private Lab, operator
  workspace;
- `agent_runtime`: claude-code, codex, cursor, generic;
- `risk_tolerance`: safe only, file writes, network, secrets, publish/runtime;
- `freshness`: stable only, include recent, include experimental;
- `language`: docs/copy language where relevant.

Profiles can remain simple at first. A profile that does not declare these
fields should receive `recommended` behavior with conservative risk.

## Sorting Rule

When multiple options match:

1. prefer `core_invariant`;
2. prefer matching `stable_default`;
3. prefer more specific profile/intent matches;
4. prefer newer `reviewed` date only within the same maturity;
5. demote anything with higher risk than the selected mode;
6. hide items with `superseded_by` unless in migration mode.

Newer is not automatically better than foundational. Newer is highlighted when
it is useful for review, but invariants keep priority.

## Output Contract

The installer should show an install plan before writing:

```text
Profile: researcher
Intent: research, lab
Mode: recommended

Will install:
- core boot/reentry hooks [core_invariant, safe]
- memory-system [stable_default, safe]
- researcher plugin [contextual, writes_files]

Available but not installed:
- godel [contextual, optional, reason: profile did not request inversion tool]
- paper-deployer [advanced, publishes]

Hidden unless migration mode:
- old semantic sync hook [legacy_or_superseded, superseded_by: semantic-bridge]
```

Every included item should explain why it is included. Every excluded advanced
or risky item should explain why it is withheld.

## Promotion Workflow

When a THIA/Lab/node function is promoted into the seed:

1. use `THIA_SEED_PROMOTION.md` to extract the portable invariant;
2. use `evolution_transfer_protocol.md` if the source is another context;
3. assign stratum, maturity, profile, intent, risk, visibility, and date;
4. mark what it supersedes or what supersedes it;
5. update the capability registry before making it an installer default;
6. run installer dry-run for at least `minimal`, `recommended`, and one
   matching contextual profile.

## First Implementation Step

The first implementation is now a planning layer. It does not change what the
installer writes unless the operator proceeds with the normal install command.

Files:

- `capabilities/registry.json`: machine-readable capability registry;
- `scripts/installer_option_router.js`: reads a profile and prints a routed
  install plan;
- `profiles/*.json`: can declare `intent`, `install_mode`, and
  `risk_tolerance`;
- `profiles/*.json`: can declare `agent_runtime` (`claude-code`, `codex`,
  `cursor`, or `generic`);
- `install.sh --plan`: shows the routed plan without writing anything.
- normal `install.sh` and `update.sh` use the routed plan as their default
  capability gate;
- `--legacy-all`: explicit compatibility bypass for older broad installs.

Examples:

```bash
./install.sh profiles/example.json --plan
./install.sh profiles/example-researcher.json --plan
./install.sh profiles/example-publisher.json --plan
./install.sh --check
./update.sh /path/to/project --plan
./update.sh --check
./install.sh profiles/example.json --legacy-all
node scripts/installer_option_router.js profiles/example-dev-node.json --mode=recent
node scripts/installer_option_router.js profiles/example.json --agent=codex
node scripts/installer_option_router.js profiles/example-codex.json
```

Validation:

- `install.sh --check` validates the local Seed registry;
- `update.sh --check` does the same from the updater entrypoint;
- `scripts/validate_capability_registry.js --strict-coverage` also fails if
  installable hooks, core skills, or plugins are not represented in the
  registry.

Enforcement:

- install/update validate the registry before normal operation;
- install/update derive selected capability paths from the planner;
- selected hooks and skills are installed/updated;
- unselected hooks and skills are skipped with a visible message;
- the active plan is saved in `.claude/seed_install_plan.json` or
  `.claude/seed_update_plan.json`;
- bypass requires the explicit `--legacy-all` flag.

## Boundary

The router decides what to present and recommend. It does not decide truth,
runtime authority, deployment, or public copy. It is an installation guide
layer, not a replacement for operator judgment or live validation.
