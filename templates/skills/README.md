# Template Skills

This directory can contain skill-shaped material that is not yet an installable
Seed capability.

Installer rule:

```text
template skill directory -> registry capability OR reference-only manifest
```

Do not add a template skill here and assume an installer will copy it. If the
skill is portable and ready, add it to `capabilities/registry.json` with risk,
runtime support and routing metadata. If it is useful but not installable yet,
add it to `templates/skills/reference-only.json` with a reason.

Current reference-only material:

- `geo-seo`: writes public web artifacts and includes nginx runtime guidance;
  promote only after packaging the skill, tool files and deployment boundary.

`youtube-transcript` was promoted to the self-contained installable package at
`plugins/d-nd-core/skills/youtube-transcript` on 2026-08-08.
