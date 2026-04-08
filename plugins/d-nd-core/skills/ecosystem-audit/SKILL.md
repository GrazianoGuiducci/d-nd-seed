---
name: ecosystem-audit
description: Audit the D-ND ecosystem state across all projects, sites, and nodes. Use periodically or after major changes to find gaps, stale content, broken links, and sync issues.
---

# Ecosystem Audit — D-ND Health Check

Run a comprehensive audit across the ecosystem to find gaps and issues.

## Audit Dimensions

### 1. Repo Sync Audit
Check if all repos are pushed and deployed:
```bash
echo "=== Repo Sync Audit ==="
# List your project repos here (auto-detected from DND_PROJECT_DIR subdirs with .git)
for dir in "${DND_PROJECT_DIR}"/*/; do
    if [ -d "$dir/.git" ]; then
        name=$(basename "$dir")
        cd "$dir"
        LOCAL=$(git rev-parse HEAD 2>/dev/null | cut -c1-7)
        REMOTE=$(git rev-parse origin/$(git branch --show-current) 2>/dev/null | cut -c1-7)
        DIRTY=$(git status --porcelain 2>/dev/null | wc -l)
        STATUS="OK"
        [ "$LOCAL" != "$REMOTE" ] && STATUS="UNPUSHED"
        [ "$DIRTY" -gt 0 ] && STATUS="DIRTY($DIRTY)"
        echo "  $name: $LOCAL $STATUS"
    fi
done
```

### 2. VPS Deploy Audit
Check if VPS matches latest commits:
```bash
echo "=== VPS Deploy Audit ==="
# Adapt: check your deployed service matches local commits
ssh root@${DND_VPS_IP} "
    echo 'Host repo:' \$(cd /opt/project && git rev-parse --short HEAD 2>/dev/null || echo 'N/A')
    echo 'Container:' \$(docker exec app-container cat /app/package.json 2>/dev/null | grep version || echo 'check manually')
    echo 'Health:' \$(curl -s localhost:\${DND_VPS_PORT:-3002}/api/status | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"status\",\"?\"), d.get(\"uptime\",\"?\"))' 2>/dev/null)
"
```

### 3. Content Audit
Check pages, translations, i18n coverage (adapt to your content structure):
```bash
echo "=== Content Audit ==="
# Example: check pages.json for bilingual coverage
# Adapt the path and field names to your project
ssh root@${DND_VPS_IP} 'python3 -c "
import json, os
pages_path = os.environ.get(\"DND_PAGES_JSON\", \"/opt/site/data/pages.json\")
with open(pages_path) as f:
    data = json.load(f)
pages = data.get(\"pages\", [])
total = len(pages)
published = sum(1 for p in pages if p.get(\"status\")==\"published\")
bilingual = sum(1 for p in pages if p.get(\"content_en\") and len(p[\"content_en\"])>100)
print(f\"Pages: {total} total, {published} published, {bilingual} bilingual\")
for p in pages:
    ci=len(p.get(\"content\",\"\"))
    ce=len(p.get(\"content_en\",\"\"))
    status=\"OK\" if ci>100 and ce>100 else \"GAP\"
    print(f\"  [{status}] {p.get(\"slug\",\"?\")} IT:{ci} EN:{ce}\")
"'
```

### 4. Seed Integrity Audit
Check d-nd-seed completeness:
```bash
echo "=== Seed Audit ==="
SEED="${DND_PROJECT_DIR}/d-nd-seed"
echo "Coder skills: $(ls $SEED/skills/coder/*.md 2>/dev/null | wc -l)"
echo "Thinker skills: $(ls $SEED/skills/thinker/*/SKILL.md 2>/dev/null | wc -l) (x2 lang)"
echo "Plugin skills: $(ls $SEED/plugins/d-nd-core/skills/*/SKILL.md 2>/dev/null | wc -l)"
echo "Kernels: $(ls $SEED/kernels/*.md 2>/dev/null | wc -l)"
echo "Profiles: $(ls $SEED/profiles/*.json 2>/dev/null | wc -l)"
```

### 5. Messaging Health
Check inter-node communication (if messaging API is configured):
```bash
echo "=== Messaging Health ==="
if [ -n "${DND_API_TOKEN}" ]; then
    curl -s "http://${DND_VPS_IP}:${DND_VPS_PORT:-3002}/api/node-sync?unread=true" \
      -H "X-Auth-Token: ${DND_API_TOKEN}" | python3 -c "
import sys,json
msgs = json.load(sys.stdin)
if isinstance(msgs, list):
    print(f'Unread messages: {len(msgs)}')
    for m in msgs[:5]:
        print(f'  [{m.get(\"from\",\"?\")}→{m.get(\"to\",\"?\")}] {m.get(\"type\",\"?\")} {str(m.get(\"content\",\"\"))[:60]}')
else:
    print(f'Response: {msgs}')
" 2>/dev/null
else
    echo "  No messaging API configured (DND_API_TOKEN not set)."
fi
```

## Output Format

Produce a structured report:
- **CRITICAL**: things broken or data loss risk
- **GAP**: missing content, incomplete translations, stale deploys
- **OK**: things that are aligned and healthy
- **OPPORTUNITY**: potential improvements noted during audit

$ARGUMENTS

## Eval

## Trigger Tests
# Appropriate prompts for this skill -> activates
# Unrelated prompts -> does NOT activate

## Fidelity Tests
# Given valid input: produces expected output
# Given edge case: handles gracefully
# Always reports what was done
