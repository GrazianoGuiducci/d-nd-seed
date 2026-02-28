---
name: propagator
description: Knowledge propagation engine. Knows what goes where when something changes. Use after any significant change to ensure all downstream targets are updated.
---

# Propagator — D-ND Change Propagation Engine

When a change happens in one part of the ecosystem, this skill knows where it needs to propagate.

## Propagation Rules

### Rule 1: THIA skill changed → d-nd-seed
```bash
# From ANTI_G_Project root:
cd "${DND_PROJECT_DIR}" && bash d-nd-seed/scripts/sync_from_thia.sh
```
After sync: check diff, commit d-nd-seed, push, notify TMx via Sinapsi.

### Rule 2: Paper updated in MM_D-ND → d-nd.com (VPS)
```bash
# 1. Convert site_ready md to pages.json entry
# 2. Merge into VPS pages.json
ssh root@${DND_VPS_IP} 'python3 -c "
import json
# Read current pages
with open(\"/opt/site_repo/data/pages.json\") as f:
    data = json.load(f)
# Show paper status
for p in data[\"pages\"]:
    if \"paper\" in p.get(\"slug\",\"\").lower():
        ci=len(p.get(\"content\",\"\"))
        ce=len(p.get(\"content_en\",\"\"))
        print(f\"{p[\"slug\"]} IT:{ci} EN:{ce}\")
"'
```

### Rule 3: d-nd.com code changed → VPS deploy
```bash
cd "${DND_PROJECT_DIR}/WEBSITE/d-nd_com" && npx vite build && scp -r dist/* root@${DND_VPS_IP}:/opt/d-nd_com_site/
```

### Rule 4: seed-landing changed → VPS deploy
```bash
cd "${DND_PROJECT_DIR}/seed-landing" && scp -r * root@${DND_VPS_IP}:/opt/seed-d-nd/
```

### Rule 5: d-nd-seed updated → notify TMx
```bash
# After push to d-nd-seed:
curl -s -X POST "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/node-sync" \
  -H "Content-Type: application/json" \
  -H "X-THIA-Token: ${DND_API_TOKEN}" \
  -d '{"from":"TM1","to":"ALL","type":"info","content":"d-nd-seed updated. Run git pull to get latest skills/plugins."}'
```

### Rule 6: Container needs update → deploy sequence
```bash
ssh root@${DND_VPS_IP} "cd /opt/THIA && git pull && docker cp . thia-neural-kernel:/app/ && docker restart thia-neural-kernel"
```

## Propagation Checklist

After ANY change, ask yourself:
- [ ] Does this affect skills? → Rule 1
- [ ] Does this affect papers? → Rule 2
- [ ] Does this affect the site frontend? → Rule 3
- [ ] Does this affect the seed landing? → Rule 4
- [ ] Does this affect the seed package? → Rule 5
- [ ] Does this affect THIA runtime? → Rule 6
- [ ] Does this affect documentation? → Check d-nd.com, seed-landing, THIA/docs
- [ ] Does this affect axioms P0-P8? → Update: MM_D-ND, kernels, seed-landing, d-nd.com

## Anti-pattern

Do NOT propagate without verification. The sequence is always:
1. **Change** → make the change
2. **Verify** → test/check locally
3. **Commit** → git commit with clear message
4. **Propagate** → run appropriate rules
5. **Confirm** → verify downstream targets received the change

$ARGUMENTS
