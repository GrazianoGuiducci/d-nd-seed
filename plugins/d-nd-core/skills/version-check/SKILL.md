---
name: version-check
description: Check Claude Code version and identify new features relevant to the D-ND ecosystem. Use after Claude Code updates to discover what capabilities have changed.
---

# Version Check — Claude Code Update Awareness

After a Claude Code update, run this to understand what changed and whether the D-ND plugin should adapt.

## Check current version

The system_awareness hook reports Claude Code version at session start. If you see a version change, investigate.

## What to check after an update

1. **New hook events**: Does the new version support hook events we don't use yet?
2. **New tool capabilities**: Are there new tools available?
3. **Plugin system changes**: Has the plugin format evolved?
4. **Performance improvements**: Memory fixes, context window changes?
5. **Security changes**: New permission modes, sandbox changes?

## Investigation procedure

```bash
# Check changelog
# Search web for: "Claude Code [version] changelog"
# Or check: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
```

## Feature mapping (what matters for D-ND)

| Claude Code Feature | D-ND Relevance | Current status |
|--------------------|--------------------|----------------|
| HTTP hooks | Could replace shell hooks for Sinapsi | Not yet used |
| Agent worktree isolation | TM3 experimental branches | Available |
| Fast mode 1M context | Full context in fast mode | Available |
| Background agents | TM3-style async work | Available |
| Plugin marketplace | Public seed distribution | Ready to use |
| Auto-memory | Supplements our MEMORY.md system | Active |
| /simplify command | Post-TM3 code review | Available |
| MCP servers | External tool connections | Available |

## After assessment

1. If new features are useful: update the plugin (bump version in plugin.json)
2. If hooks need updating: modify hooks.json and scripts
3. If new skills are needed: add to skills/
4. Notify operator with findings and recommendations

$ARGUMENTS

## Eval

## Trigger Tests
# Appropriate prompts for this skill -> activates
# Unrelated prompts -> does NOT activate

## Fidelity Tests
# Given valid input: produces expected output
# Given edge case: handles gracefully
# Always reports what was done
