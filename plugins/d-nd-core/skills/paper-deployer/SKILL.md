---
name: paper-deployer
description: Deploy paper content from MM_D-ND site_ready files to d-nd.com VPS. Handles md-to-HTML conversion, bilingual merge, figure path resolution, and pages.json update.
---

# Paper Deployer — MM_D-ND → d-nd.com Pipeline

Deploy updated paper content from source (MM_D-ND/papers/site_ready/) to the live site.

## Prerequisites

- Paper source files in `MM_D-ND/papers/site_ready/paper_X_IT.md` and `paper_X_EN.md`
- Figure SVGs in `MM_D-ND/papers/figures/` (already converted from PDF)
- VPS access via SSH

## Deployment Steps

### Step 1 — Check source files
```bash
ls ${DND_PROJECT_DIR}/MM_D-ND/papers/site_ready/paper_*_{IT,EN}.md 2>/dev/null
ls ${DND_PROJECT_DIR}/MM_D-ND/papers/figures/*.svg 2>/dev/null | wc -l
```

### Step 2 — Convert and merge
The conversion pipeline:
1. Read IT and EN markdown from site_ready/
2. Convert to HTML (preserve LaTeX `$...$` for MathJax)
3. Convert markdown images `![alt](src)` to `<figure><img>` HTML
4. Resolve figure wildcard paths (`fig_C1_*.svg` → `fig_C1_actual_name.svg`)
5. Merge into pages.json: IT → `content`, EN → `content_en`

### Step 3 — Deploy figures to VPS
```bash
scp ${DND_PROJECT_DIR}/MM_D-ND/papers/figures/*.svg root@${DND_VPS_IP}:/opt/d-nd_com_site/papers/figures/
```

### Step 4 — Update pages.json on VPS
```bash
# The pages.json served by nginx is at /opt/site_repo/data/pages.json
# The container bind-mounts this same file
# Update in place — changes are immediately live (nginx no-cache)
ssh root@${DND_VPS_IP} 'python3 << "PYEOF"
import json
with open("/opt/site_repo/data/pages.json") as f:
    data = json.load(f)
# ... merge logic here ...
with open("/opt/site_repo/data/pages.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)
PYEOF'
```

### Step 5 — Verify
```bash
# Check the deployed content
ssh root@${DND_VPS_IP} 'python3 -c "
import json
with open(\"/opt/site_repo/data/pages.json\") as f:
    data = json.load(f)
for p in data[\"pages\"]:
    if \"paper\" in p.get(\"slug\",\"\").lower():
        ci=len(p.get(\"content\",\"\"))
        ce=len(p.get(\"content_en\",\"\"))
        print(f\"{p[\"slug\"]} IT:{ci} EN:{ce}\")
"'
```

## Important Notes

- **Two pages.json files exist on VPS**: `/opt/site_repo/data/pages.json` (served by nginx, authoritative) and `/opt/d-nd_com_site/data/pages.json` (bundled in dist, fallback). Always update site_repo.
- **Container bind mount**: `/opt/site_repo` is mounted as `/app/site` in the container. They share the same filesystem.
- **Siteman Consumer**: writes to the same file via bind mount. Preserves all fields on write. Safe.
- **Markdown images in HTML**: The frontend (`PageComponent.tsx`) converts `<p>![alt](src)</p>` to `<figure>` at render time. But prefer proper HTML in source.

$ARGUMENTS

## Eval

## Trigger Tests
# Appropriate prompts for this skill -> activates
# Unrelated prompts -> does NOT activate

## Fidelity Tests
# Given valid input: produces expected output
# Given edge case: handles gracefully
# Always reports what was done
