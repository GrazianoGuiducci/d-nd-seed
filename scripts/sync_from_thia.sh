#!/bin/bash
# sync_from_thia.sh — Export skills from THIA source to d-nd-seed
#
# Usage: ./scripts/sync_from_thia.sh [--dry-run] [--neutralize]
#
# Source: THIA/.agent/skills/agent_skills_*.md
# Target: d-nd-seed/skills/coder/
#
# --dry-run    Show what would change without writing
# --neutralize Strip THIA-specific references (paths, node IDs, internal APIs)
#
# This is the propagation step: THIA (R&D) → d-nd-seed (distribution)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
THIA_SKILLS_DIR="$(dirname "$REPO_DIR")/THIA/.agent/skills"
TARGET_DIR="$REPO_DIR/skills/coder"

DRY_RUN=false
NEUTRALIZE=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --neutralize) NEUTRALIZE=true ;;
    esac
done

# Validate paths
if [ ! -d "$THIA_SKILLS_DIR" ]; then
    echo "ERROR: THIA skills directory not found at: $THIA_SKILLS_DIR"
    echo "Expected: ../THIA/.agent/skills/ relative to this repo"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "ERROR: Target directory not found: $TARGET_DIR"
    echo "Run from the d-nd-seed repo root."
    exit 1
fi

echo "=== THIA → d-nd-seed Export ==="
echo "Source:      $THIA_SKILLS_DIR"
echo "Target:      $TARGET_DIR"
echo "Neutralize:  $NEUTRALIZE"
echo "Dry run:     $DRY_RUN"
echo ""

# Neutralization function — strips THIA-specific references
neutralize_skill() {
    local content="$1"

    # Replace absolute THIA paths with generic placeholders
    content=$(echo "$content" | sed \
        -e 's|/opt/THIA/|/path/to/project/|g' \
        -e 's|C:\\Users\\metam\\ANTI_G_Project\\THIA\\|/path/to/project/|g' \
        -e 's|C:/Users/metam/ANTI_G_Project/THIA/|/path/to/project/|g' \
        -e 's|\.\./THIA/|./|g')

    # Replace specific node IDs with generic
    content=$(echo "$content" | sed \
        -e 's/TM1 (Origin Node)/YOUR_NODE/g' \
        -e 's/TM3 (Dev Node)/DEV_NODE/g' \
        -e 's/nodo TM1/il tuo nodo/g' \
        -e 's/nodo TM3/il nodo dev/g')

    # Replace VPS-specific endpoints
    content=$(echo "$content" | sed \
        -e 's|31\.97\.35\.9|YOUR_VPS_IP|g' \
        -e 's|:3002|:YOUR_PORT|g' \
        -e 's|:3003|:YOUR_PORT|g')

    # Replace internal API paths with generic
    content=$(echo "$content" | sed \
        -e 's|/api/node-sync|/api/sync|g' \
        -e 's|kthiabot@gmail\.com|your-bot@email.com|g')

    echo "$content"
}

# Count changes
added=0
updated=0
unchanged=0
skipped=0

# Skills to exclude from distribution (THIA-internal only)
EXCLUDE_PATTERN="agent_skills_thia[-_]node[-_]ops|agent_skills_siteman[-_]bridge|agent_skills_siteman\b"

for src_file in "$THIA_SKILLS_DIR"/agent_skills_*.md; do
    [ -f "$src_file" ] || continue
    filename=$(basename "$src_file")

    # Skip THIA-internal skills
    if echo "$filename" | grep -qE "$EXCLUDE_PATTERN"; then
        echo "[SKIP] $filename (THIA-internal)"
        skipped=$((skipped + 1))
        continue
    fi

    dst_file="$TARGET_DIR/$filename"

    # Prepare content (with optional neutralization)
    if [ "$NEUTRALIZE" = true ]; then
        new_content=$(neutralize_skill "$(cat "$src_file")")
    else
        new_content=$(cat "$src_file")
    fi

    if [ ! -f "$dst_file" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "[ADD] $filename"
        else
            echo "$new_content" > "$dst_file"
            echo "[ADD] $filename"
        fi
        added=$((added + 1))
    else
        current_content=$(cat "$dst_file")
        if [ "$new_content" != "$current_content" ]; then
            if [ "$DRY_RUN" = true ]; then
                echo "[UPD] $filename"
            else
                echo "$new_content" > "$dst_file"
                echo "[UPD] $filename"
            fi
            updated=$((updated + 1))
        else
            unchanged=$((unchanged + 1))
        fi
    fi
done

# Check for skills in target that no longer exist in THIA
removed=0
for dst_file in "$TARGET_DIR"/agent_skills_*.md; do
    [ -f "$dst_file" ] || continue
    filename=$(basename "$dst_file")

    # Don't flag excluded skills as removed
    if echo "$filename" | grep -qE "$EXCLUDE_PATTERN"; then
        continue
    fi

    src_file="$THIA_SKILLS_DIR/$filename"
    if [ ! -f "$src_file" ]; then
        echo "[DEL] $filename (no longer in THIA)"
        if [ "$DRY_RUN" = false ]; then
            rm "$dst_file"
        fi
        removed=$((removed + 1))
    fi
done

echo ""
echo "=== Summary ==="
echo "  Added:     $added"
echo "  Updated:   $updated"
echo "  Removed:   $removed"
echo "  Skipped:   $skipped (THIA-internal)"
echo "  Unchanged: $unchanged"
echo "  Total:     $((added + updated + unchanged)) distributable"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "(dry run — no files changed)"
else
    echo ""
    echo "Done. Review changes with: git diff skills/coder/"
    echo "Commit with: git add skills/coder/ && git commit -m 'sync: export from THIA'"
fi
