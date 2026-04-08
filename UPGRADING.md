# Upgrading d-nd-seed

## From v2.2 to v3.0 (2026-04-08)

This release makes the seed fully provider-neutral and removes all internal infrastructure references. If you're running the seed on a node, read this before pulling.

### Breaking Changes

#### 1. Nine coder skills removed

These skills were specific to one system's infrastructure. If you reference them in custom triggers or routing, remove the references:

| Removed skill | Was | Replace with |
|---------------|-----|-------------|
| `agent_skills_dev_delegate.md` | Task delegation to a specific node | Use your own delegation pattern |
| `agent_skills_design-dnd.md` | Site visual design for one project | Use `architect` for structural analysis |
| `agent_skills_thia_node_ops.md` | Multi-node operations for one system | Use generic node patterns in docs/ |
| `agent_skills_research_lab.md` | Research workflow for one model | Build your own research skill |
| `agent_skills_field-awareness.md` | Field sensing via hardcoded URLs | Use `ecosystem-audit` |
| `agent_skills_siteman.md` | CMS management for one site | Use your CMS tooling |
| `agent_skills_publisher.md` | Content publishing to one platform | Use `social-publisher` for social |
| `agent_skills_conductor.md` | Orchestrator for one system (duplicate) | Use `conductor-claude` |
| `agent_skills_siteman-bridge.md` | Bridge to one CMS | Not needed — generic patterns exist |

**Action**: if your `catalog.json` or routing config references these, update it.

#### 2. Godel bridge — new env vars

The Godel bridge is now provider-neutral. Old env vars still work as fallback.

| Old | New | Notes |
|-----|-----|-------|
| `ANTHROPIC_API_KEY` | `GODEL_API_KEY` | Legacy still works |
| (hardcoded URL) | `GODEL_API_URL` | Required for new setup |
| (auto-detected) | `GODEL_API_FORMAT` | `anthropic` or `openai`, auto-detected from URL |

**Action**: set `GODEL_API_KEY` and `GODEL_API_URL`. Or do nothing — legacy env vars still work.

```bash
# New way (any provider)
export GODEL_API_KEY=your-key
export GODEL_API_URL=https://api.your-provider.com/v1/chat/completions

# Old way (still works)
export ANTHROPIC_API_KEY=sk-ant-...
```

#### 3. Profiles renamed

| Old | New |
|-----|-----|
| `profiles/tm1.json` | `profiles/example-origin-node.json` |
| `profiles/tm3.json` | `profiles/example-dev-node.json` |

**Action**: if your install script references `profiles/tm1.json` or `profiles/tm3.json`, update the path. The profile `example.json` is unchanged.

#### 4. Naming: Sinapsi → node-messaging

All docs and templates now use "node messaging" / "inter-node communication" instead of "Sinapsi". The API endpoints in templates changed from `/api/node-sync` to `/api/sync`.

**Action**: if you have custom hooks that reference "Sinapsi" or `/api/node-sync`, update them. The installed hooks (generated from templates) will use the new names on next install.

### Non-Breaking Changes

#### Eleven coder skills neutralized

Generic patterns preserved, internal references removed. If you use these skills, they now work for any project:

`transcriber`, `coherence`, `extractor`, `optimizer`, `social_publisher`, `triage`, `deploy_pipeline`, `conductor_claude`, `forgia`, `architect`, `geo_seo`

No action needed — they work as before, just cleaner.

#### Four cognitive files evolved

Updated with latest thinking (honesty rules, cascata, cognitive cycle integration):

- `memory-system/SKILL.md` — honesty rules in memory, cascade awareness, concrete compression verification
- `kernel_coder_en.md` — cascata (3 levels), auto-evolutionary principle, proactive post-compaction
- `autonomous-cycle/SKILL.md` — piano defined, decision ordering justified, auto-learn feedback, cognitive cycle flow
- `integrate-pattern/SKILL.md` — extraction method specified, cascade after integration

No action needed — pull and the AI reads the updated versions.

#### New: Scenario Projector complete guide

`plugins/d-nd-core/scripts/PROJECTOR_COMPLETE_GUIDE.md` — unified guide covering configuration, 5 integration patterns, real examples, creating new domains.

### How to upgrade

```bash
cd your-project
cd d-nd-seed  # or wherever you cloned it
git pull

# If you use Godel, update env vars:
export GODEL_API_KEY=your-key
export GODEL_API_URL=https://api.your-provider.com/v1/chat/completions

# If you want to regenerate hooks/skills from updated templates:
./install.sh profiles/your-profile.json

# If you just want the updated skills and kernels:
# Nothing to do — the AI reads them from the seed directory on next session
```

### Version history

| Version | Date | Summary |
|---------|------|---------|
| v3.0 | 2026-04-08 | Provider-neutral, fully public, cognitive evolution |
| v2.2 | 2026-04-06 | Projector + structural lenses + automation pattern |
| v2.1 | 2026-04-01 | CEA hook, operator interaction guide, safe update mode |
