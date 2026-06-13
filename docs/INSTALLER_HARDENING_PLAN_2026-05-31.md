# Installer Hardening Plan - 2026-05-31

Status: active plan
Scope: `install.sh`, `update.sh`, hook templates, profile validation, runtime
adapters, installer documentation
Boundary: do not execute write-mode install/update on Windows during this work.

Current-status note, 2026-06-13:

```text
This plan is historical/partially superseded. Current install behavior includes
a neutral `.seed/` manifest for profile/plan/adapter notes and keeps `.claude/`
as the Claude Code adapter/compatibility surface. For current behavior, prefer
README.md, GUIDE.md, docs/agent_neutral_seed_surface.md and
docs/installer_option_router.md.
```

## Purpose

Seed is now presented to AI coders as an installable operating substrate. That
raises the bar for the installer: it must not surprise the host runtime, trust
profile input as shell code, write outside the intended project, or claim a
universal path where only Bash-native behavior exists.

This plan integrates the gaps found after the first hardening pass and orders
the next fixes.

## Persistence Crystals

```text
Windows is not incidental.
Profiles are not trusted shell input.
Read-only planning must stay read-only.
Registry routing is the install contract.
Bash-native is not universal.
Hooks that parse arbitrary tool input must not use shell eval.
An AI coder may run examples too literally unless the installer blocks it.
```

## Current State

Pass 1 already changed:

- `install.sh` no longer uses shell `eval` for profile parsing or Godel setup.
- write-mode Windows Bash install/update is blocked unless
  `DND_SEED_ALLOW_WINDOWS_BASH=1` is set deliberately.
- `update.sh` has `--dry-run`.
- temp files are cleaned through traps.
- `youtube-transcript` no longer bypasses registry routing.
- README/GUIDE distinguish Node read-only checks from Bash-native install.

Verified without running installers:

```powershell
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
node scripts\installer_option_router.js profiles\example-codex.json
node scripts\installer_option_router.js profiles\example-claude-code.json
git diff --check -- install.sh update.sh README.md GUIDE.md docs\SEED_REPO_AUDIT_2026-05-31.md
```

## Integrated Gaps

### Gap 1 - Hook Template `eval`

Remaining templates still parse arbitrary hook input through shell `eval`:

```text
templates/hooks/cascade_check.sh.tmpl
templates/hooks/modus_copy.sh.tmpl
```

Risk:

```text
tool input, command output, file paths or content preview can contain shell
syntax that breaks parsing or becomes unsafe.
```

Target:

```text
replace shell eval with direct Node/Python extraction into temp JSON or plain
newline-safe files; never turn arbitrary JSON fields into shell assignment text.
```

### Gap 2 - Inline Python/JSON With Quoted Paths

Several hooks call Python with values interpolated into source strings:

```text
cea_hook.sh.tmpl
pattern_decay_check.sh.tmpl
system_awareness.sh.tmpl
```

Risk:

```text
paths containing quotes or unusual characters can break the inline program.
```

Target:

```text
pass paths through environment variables or argv, not string interpolation.
```

### Gap 3 - Cross-Platform Installer Boundary

The current write-mode installer remains Bash-native. That is acceptable only
if the runtime is explicit.

Target:

```text
Node read-only planning is universal.
Bash install is Bash-native.
Windows write-mode requires explicit opt-in.
Future cross-platform install should be Node/PowerShell-aware.
```

### Gap 4 - Profile Schema And Target Boundary

Pass 1 rejects obvious unsafe profile values, but there is no full profile
schema validator.

Target:

```text
add profile validation for required fields, runtime, install_mode, risk,
project_dir, repo entries, plugin blocks and path policy.
```

Path policy must distinguish:

- placeholder path;
- relative target path;
- absolute target path;
- parent traversal;
- root/system path;
- Windows drive path under Git Bash/WSL;
- target equal to Seed repo itself;
- target outside intended workspace.

### Gap 5 - Registry Coverage

`youtube-transcript` no longer installs unconditionally, but template skills are
not fully represented in registry coverage.

Known template skill areas:

```text
templates/skills/youtube-transcript
templates/skills/geo-seo
```

Target:

```text
either promote each installable template skill into capabilities/registry.json
or mark it explicitly as non-installed/reference material.
```

### Gap 6 - Update Protection Is Still Partial

`update.sh` protects hooks better than skills/projector files. It can still add
or update some copied assets without the same user-modified-file discipline.

Target:

```text
update plan must list every intended write; dry-run must cover every write;
normal update must avoid overwriting user-modified files or write .new.
```

### Gap 7 - Generated Hook Runtime Assumptions

Generated settings call Bash hooks. Some hooks assume Unix tools:

```text
bash
python3
stat -c
df
curl
docker
systemctl
claude
```

Target:

```text
runtime translators must mark each generated capability as native, adapter,
documented or unsupported for the selected runtime.
```

### Gap 8 - Test Matrix Is Not Yet Real Enough

Current checks validate registry and router output, not installer behavior in a
throwaway target.

Target:

```text
add scripted tests using temporary target directories and profile fixtures.
No writes outside temp. No Windows Bash write-mode without opt-in.
```

### Gap 9 - Line Endings And Executable Bits

Windows reports LF-to-CRLF warnings on shell files. Shell scripts should remain
LF when committed.

Target:

```text
add or verify .gitattributes for *.sh, hook templates and scripts that require
LF; preserve executable semantics where relevant.
```

## Plan

### Phase 0 - Freeze And Verify Pass 1

Goal:

```text
prove current modified state is coherent before deeper changes.
```

Actions:

- read current diff for `install.sh`, `update.sh`, `README.md`, `GUIDE.md`;
- confirm no `eval` remains in `install.sh` or `update.sh`;
- confirm Node read-only commands still pass;
- confirm docs record Windows/Bash boundary.

Validation:

```powershell
rg -n "eval" install.sh update.sh
node scripts\validate_capability_registry.js
node scripts\installer_option_router.js profiles\example.json
git diff --check -- install.sh update.sh README.md GUIDE.md docs\SEED_REPO_AUDIT_2026-05-31.md
```

### Phase 1 - Remove Hook `eval`

Status: applied in current working tree.

Goal:

```text
arbitrary hook input must not become shell assignment text.
```

Files:

```text
templates/hooks/cascade_check.sh.tmpl
templates/hooks/modus_copy.sh.tmpl
```

Approach:

- parse hook JSON with Python;
- write needed values into a temporary directory as plain files;
- read those files into shell variables without `eval`;
- keep current behavior and rate limits.

Validation:

```powershell
rg -n "eval" templates\hooks\cascade_check.sh.tmpl templates\hooks\modus_copy.sh.tmpl
node scripts\validate_capability_registry.js
git diff --check -- templates\hooks\cascade_check.sh.tmpl templates\hooks\modus_copy.sh.tmpl
```

Applied notes:

```text
cascade_check.sh.tmpl:
  TOOL_NAME, FILE_PATH, COMMAND and STDOUT now come from temp files.

modus_copy.sh.tmpl:
  TOOL_NAME, FILE_PATH and CONTENT_PREVIEW now come from temp files.
```

### Phase 2 - Add Profile Validator

Status: applied in current working tree.

Goal:

```text
profiles must be validated before install/update logic interprets paths or
runtime intent.
```

New file candidate:

```text
scripts/validate_profile.js
```

Responsibilities:

- validate JSON parse;
- validate allowed `agent_runtime`, `install_mode`, `risk_tolerance`;
- validate `project_dir`;
- validate repo entries;
- validate plugin blocks;
- expose `--target-policy=read-only|dry-run|write`;
- return machine-readable JSON for installer use.

Installer change:

```text
install.sh calls validate_profile.js before reading profile values.
update.sh validates saved .claude/seed_profile.json before update.
```

Applied notes:

```text
scripts/validate_profile.js now validates target policy, install mode, risk,
agent runtime, shell-control characters, project_dir, repo entries and plugin
blocks.

install.sh calls it for --plan, --dry-run and write paths.
update.sh calls it for --plan, --dry-run and write paths.
```

Validation:

```powershell
node scripts\validate_profile.js profiles\example.json --target-policy=read-only
node scripts\validate_profile.js profiles\example-codex.json --target-policy=read-only
node scripts\validate_profile.js profiles\example-claude-code.json --target-policy=read-only
```

### Phase 3 - Registry Coverage For Template Skills

Goal:

```text
every installable asset is either in the capability registry or explicitly
non-installed reference material.
```

Actions:

- inspect `templates/skills/youtube-transcript`;
- inspect `templates/skills/geo-seo`;
- decide whether each is:
  - registry capability;
  - plugin skill;
  - reference template;
  - deprecated residue.
- update `capabilities/registry.json` only if selected as installable.

Validation:

```powershell
node scripts\validate_capability_registry.js --strict-coverage
```

Note: strict coverage currently checks hooks/core skills/plugins, not all
template skills. Extend it if template skills become installable.

Status:

```text
applied on 2026-05-31
```

Decision:

- `youtube-transcript` remains reference-only because it depends on a
  project-local `tools/youtube_transcript.js` implementation that Seed does not
  package.
- `geo-seo` remains reference-only because it writes public web artifacts and
  includes nginx runtime guidance; it needs a complete promotion package before
  installer exposure.

Changes made:

- added `templates/skills/reference-only.json`;
- added `templates/skills/README.md`;
- extended `scripts/validate_capability_registry.js --strict-coverage` so
  template skill directories must be either registered or explicitly
  reference-only.

Validation:

```powershell
node scripts\validate_capability_registry.js --strict-coverage
```

### Phase 4 - Make Update Planning Complete

Goal:

```text
update.sh --dry-run should describe every write normal update can make.
```

Actions:

- ensure hooks, skills, projector and plan writes all have dry-run branches;
- write `.new` instead of overwriting where user modification is plausible;
- ensure parent directories are created only outside dry-run;
- consider a JSON update manifest.

Validation:

```text
run update.sh --dry-run only inside a temporary fixture, never active project.
compare file tree before/after; it must be identical.
```

Static pass applied on 2026-05-31:

- `--dry-run` is documented in usage;
- normal write-mode rejects obvious unsafe update targets such as `/`, drive
  roots and parent traversal;
- `.new` hook review files now receive instantiated profile values instead of
  raw template placeholders.
- `install.sh --dry-run` now exits with an explicit dry-run completion message
  instead of reporting a completed install.

Deferred validation:

```text
fixture-based update dry-run tree comparison
```

### Phase 5 - Cross-Platform Planner/Installer Split

Goal:

```text
separate universal planning from Bash-native file writing.
```

New file candidates:

```text
scripts/seed_plan.js
scripts/seed_install.js
```

Target shape:

```text
seed_plan.js: read-only, cross-platform, emits plan JSON/text.
seed_install.js: optional future cross-platform writer with explicit target
validation and dry-run manifest.
install.sh: Bash wrapper around the same Node planner/writer or legacy Bash
writer with clear runtime gate.
```

Status:

```text
partial read-only split applied on 2026-05-31
```

Implemented:

- added `scripts/seed_plan.js`;
- it validates the registry;
- it validates the profile with `validate_profile.js`;
- it emits the routed plan through `installer_option_router.js`;
- it supports `--json` and `--paths` without contaminating stdout with
  validation summaries;
- it never invokes `install.sh` or `update.sh`.

Boundary:

```text
seed_plan.js is not a writer and does not authorize install.
```

Validation:

```powershell
node scripts\seed_plan.js profiles\example.json
node scripts\seed_plan.js profiles\example-codex.json --json
node scripts\seed_plan.js profiles\example-claude-code.json --paths
```

### Phase 6 - Runtime Translator Alignment

Goal:

```text
generated capabilities must not claim native behavior in runtimes where hooks do
not actually fire.
```

Actions:

- review `docs/agent_runtime_translators.md`;
- ensure README/GUIDE use the same runtime states;
- add table for Claude Code, Codex, generic/OpenCode-like runtimes:
  native / adapter / documented / unsupported.

### Phase 7 - Sandbox Test Harness

Goal:

```text
test the installer in disposable targets, not by trusting docs or live paths.
```

New test candidates:

```text
scripts/test_installer_safety.js
tests/fixtures/profiles/
```

Test cases:

- valid profile read-only plan;
- placeholder path refused in write mode;
- root/parent traversal refused;
- Windows Bash write blocked without env opt-in;
- `--dry-run` creates no target files;
- update dry-run creates no files;
- registry-selected assets only;
- malformed profile rejected;
- profile values with shell-control characters rejected;
- no `eval` in installer/update/high-risk hooks.

Status:

```text
applied on 2026-05-31 as a Node-only safety harness
```

Implemented:

- `scripts/test_installer_safety.js`;
- registry strict coverage check;
- clean `seed_plan.js --json` and `--paths` checks;
- read-only fixture check proving `seed_plan.js` does not mutate the target;
- negative profile tests for placeholder paths, parent traversal, shell-control
  characters and Seed-repo target;
- static no-`eval` check for install/update/hooks;
- static dry-run messaging checks for install/update.

Boundary:

```text
the harness does not run install.sh or update.sh on this Windows node
```

Remaining future hardening:

```text
Bash dry-run tree comparison inside a controlled Unix/Git-Bash fixture.
```

## Stop Conditions

Stop before code changes if:

- a fix would require running write-mode installer on this Windows node;
- target path policy needs operator decision;
- registry promotion of template skills is semantically unclear;
- a hook behavior cannot be preserved without changing its intended function;
- Node cross-platform installer would become a broad rewrite instead of a
  bounded phase.

## Next Safe Move

```text
Phase 7.
```

Meaning:

1. read the full diff;
2. decide whether to add a Bash fixture runner later on a controlled runtime;
3. commit only after diff review and operator approval;
4. keep any future `seed_install.js` writer blocked until write-mode fixture
   tests exist.
