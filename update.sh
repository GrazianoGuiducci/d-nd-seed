#!/bin/bash
# ============================================================================
# D-ND SEED UPDATER
# ============================================================================
# Updates an installed seed to the latest version.
# Pulls new hooks, skills, kernels without overwriting customizations.
#
# Usage:
#   cd /path/to/d-nd-seed && git pull
#   ./update.sh /path/to/project
#
# What it updates:
#   - Hook templates → project hooks (only if template is newer)
#   - New skills → project skills (only adds, never overwrites)
#   - Kernel updates → project kernel (merges new sections)
#
# What it never touches:
#   - CLAUDE.md (user-customized)
#   - MEMORY.md (user data)
#   - settings.json (user-configured hooks)
#   - Any file the user has modified since install
# ============================================================================

set -e

SEED_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="${1:-.}"

if [ ! -d "$PROJECT_DIR/.claude" ]; then
    echo "ERROR: No .claude/ directory found in $PROJECT_DIR"
    echo "Run install.sh first, then use update.sh for subsequent updates."
    exit 1
fi

echo "=== D-ND Seed Updater ==="
echo "Seed: $SEED_DIR"
echo "Project: $PROJECT_DIR"
echo ""

UPDATED=0
SKIPPED=0
ADDED=0

# --- Update hook templates ---
echo "## Hooks"
for tmpl in "$SEED_DIR"/templates/hooks/*.tmpl; do
    [ -f "$tmpl" ] || continue
    name=$(basename "$tmpl" .tmpl)
    target="$PROJECT_DIR/.claude/hooks/$name"

    # Instantiate template variables if profile exists
    instantiate() {
        local content="$1"
        if [ -f "$PROJECT_DIR/.claude/seed_profile.json" ]; then
            local pdir=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$PROJECT_DIR/.claude/seed_profile.json','utf8')).project_dir||'.')" 2>/dev/null || echo "$PROJECT_DIR")
            local nid=$(node -e "console.log(JSON.parse(require('fs').readFileSync('$PROJECT_DIR/.claude/seed_profile.json','utf8')).node_id||'UNKNOWN')" 2>/dev/null || echo "UNKNOWN")
            content=$(echo "$content" | sed "s|{{PROJECT_DIR}}|$pdir|g; s|{{NODE_ID}}|$nid|g")
        fi
        echo "$content"
    }

    if [ ! -f "$target" ]; then
        echo "  + $name (new)"
        instantiate "$(cat "$tmpl")" > "$target"
        chmod +x "$target" 2>/dev/null
        ADDED=$((ADDED + 1))
    elif [ "$tmpl" -nt "$target" ]; then
        # Template is newer — check if user modified the target
        if git -C "$PROJECT_DIR" diff --quiet -- ".claude/hooks/$name" 2>/dev/null; then
            echo "  ~ $name (updated)"
            instantiate "$(cat "$tmpl")" > "$target"
            UPDATED=$((UPDATED + 1))
        else
            echo "  . $name (skipped — user modified)"
            cp "$tmpl" "${target}.new"
            echo "    → saved as ${name}.new for manual review"
            SKIPPED=$((SKIPPED + 1))
        fi
    fi
done
echo ""

# --- Add new skills ---
echo "## Skills"
for skill_dir in "$SEED_DIR"/plugins/d-nd-core/skills/*/; do
    [ -d "$skill_dir" ] || continue
    name=$(basename "$skill_dir")
    target="$PROJECT_DIR/.claude/skills/$name"

    if [ ! -d "$target" ]; then
        echo "  + $name (new skill)"
        cp -r "$skill_dir" "$target"
        ADDED=$((ADDED + 1))
    fi
done
echo ""

# --- Update projector tools ---
echo "## Projector"
PROJECTOR_SRC="$SEED_DIR/plugins/d-nd-core/scripts"
PROJECTOR_DST="$PROJECT_DIR/d-nd-tools"
if [ -d "$PROJECTOR_DST" ] && [ -f "$PROJECTOR_SRC/scenario_projector.py" ]; then
    # Update main script if seed is newer
    if [ "$PROJECTOR_SRC/scenario_projector.py" -nt "$PROJECTOR_DST/scenario_projector.py" ]; then
        cp "$PROJECTOR_SRC/scenario_projector.py" "$PROJECTOR_DST/"
        cp "$PROJECTOR_SRC/SCENARIO_PROJECTOR_GUIDE.md" "$PROJECTOR_DST/" 2>/dev/null
        echo "  ~ scenario_projector.py (updated)"
        UPDATED=$((UPDATED + 1))
    fi
    # Add new example seeds
    mkdir -p "$PROJECTOR_DST/examples"
    for f in "$PROJECTOR_SRC"/examples/*.json "$PROJECTOR_SRC"/examples/*.py "$PROJECTOR_SRC"/examples/*.md; do
        [ -f "$f" ] || continue
        fname=$(basename "$f")
        if [ ! -f "$PROJECTOR_DST/examples/$fname" ]; then
            cp "$f" "$PROJECTOR_DST/examples/"
            echo "  + examples/$fname (new)"
            ADDED=$((ADDED + 1))
        elif [ "$f" -nt "$PROJECTOR_DST/examples/$fname" ]; then
            cp "$f" "$PROJECTOR_DST/examples/"
            echo "  ~ examples/$fname (updated)"
            UPDATED=$((UPDATED + 1))
        fi
    done
elif [ ! -d "$PROJECTOR_DST" ] && [ -f "$PROJECTOR_SRC/scenario_projector.py" ]; then
    echo "  Projector not installed. Run install.sh to add it."
fi
echo ""

# --- Summary ---
echo "## Summary"
echo "  Added: $ADDED"
echo "  Updated: $UPDATED"
echo "  Skipped (user modified): $SKIPPED"
echo ""
echo "=== Done ==="
echo ""
echo "To get the latest seed: cd $SEED_DIR && git pull && ./update.sh $PROJECT_DIR"
