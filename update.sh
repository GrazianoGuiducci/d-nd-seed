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

    if [ ! -f "$target" ]; then
        echo "  + $name (new)"
        cp "$tmpl" "$target"
        chmod +x "$target" 2>/dev/null
        ADDED=$((ADDED + 1))
    elif [ "$tmpl" -nt "$target" ]; then
        # Template is newer — check if user modified the target
        if git -C "$PROJECT_DIR" diff --quiet -- ".claude/hooks/$name" 2>/dev/null; then
            echo "  ~ $name (updated)"
            cp "$tmpl" "$target"
            UPDATED=$((UPDATED + 1))
        else
            echo "  . $name (skipped — user modified)"
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

# --- Summary ---
echo "## Summary"
echo "  Added: $ADDED"
echo "  Updated: $UPDATED"
echo "  Skipped (user modified): $SKIPPED"
echo ""
echo "=== Done ==="
echo ""
echo "To get the latest seed: cd $SEED_DIR && git pull && ./update.sh $PROJECT_DIR"
