---
name: propagator
description: "Knowledge propagation engine. Knows what goes where when something changes. Use after any significant change to ensure all downstream targets are updated."
---

# Propagator — Change Propagation Engine

When a change happens in one part of the system, this skill ensures all downstream targets are updated.

## Propagation Rules

### Rule 1: Skill changed → seed repo
```bash
# Sync updated skills to the seed repository for distribution
cd "${DND_PROJECT_DIR}" && bash d-nd-seed/scripts/sync_from_thia.sh
```
After sync: check diff, commit, push, notify other nodes.

### Rule 2: Content updated → site deploy
```bash
# Build and deploy site changes
cd "${DND_PROJECT_DIR}/site" && npm run build
# Deploy via your mechanism (scp, rsync, webhook, CI/CD)
```

### Rule 3: Seed package updated → notify nodes
```bash
# After pushing to the seed repo, notify other nodes
curl -s -X POST "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/node-sync" \
  -H "Content-Type: application/json" \
  -H "X-Auth-Token: ${DND_API_TOKEN}" \
  -d '{"from":"'${DND_NODE_ID}'","to":"ALL","type":"info","content":"Seed updated. Run git pull to get latest."}'
```

### Rule 4: Runtime changed → deploy sequence
```bash
# Deploy runtime changes to your server
# Adapt to your infrastructure (Docker, systemd, PM2, etc.)
git pull && docker cp . ${DND_CONTAINER_NAME}:/app/ && docker restart ${DND_CONTAINER_NAME}
```

## Propagation Checklist

After ANY significant change, ask:
- [ ] Does this affect skills? → Sync to seed
- [ ] Does this affect the site? → Deploy
- [ ] Does this affect the seed package? → Notify nodes
- [ ] Does this affect runtime? → Deploy sequence
- [ ] Does this affect documentation? → Update docs
- [ ] Does this affect operating rules? → Update kernel, propagate to all nodes
- [ ] Who else in the system needs this? (Awareness at every level)

## Anti-pattern

Do NOT propagate without verification:
1. **Change** → make the change
2. **Verify** → test/check locally
3. **Commit** → read the diff, then commit with clear message
4. **Propagate** → run appropriate rules
5. **Confirm** → verify downstream targets received the change

$ARGUMENTS

## Eval

## Trigger Tests
# "I changed a skill, what else needs updating?" -> activates
# "propagate this change" -> activates
# "who else needs to know?" -> activates
# "fix this typo" -> does NOT activate

## Fidelity Tests
# Given skill change: suggests sync to seed + notify nodes
# Given site change: suggests build + deploy
# Given no downstream impact: reports "no propagation needed"
