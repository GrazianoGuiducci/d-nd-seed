#!/bin/bash
# sync_from_thia.sh — Sync skill files from THIA source to this catalog
#
# Usage: ./scripts/sync_from_thia.sh [--dry-run]
#
# Source: THIA/.agent/skills/agent_skills_*.md
# Target: skill/agent_skills_*.md (flat catalog)
#
# This script copies all skill files from the THIA source directory,
# reports what changed, and optionally commits the result.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
THIA_SKILLS_DIR="$(dirname "$REPO_DIR")/THIA/.agent/skills"

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
fi

# Validate paths
if [ ! -d "$THIA_SKILLS_DIR" ]; then
    echo "ERROR: THIA skills directory not found at: $THIA_SKILLS_DIR"
    echo "Expected: ../THIA/.agent/skills/ relative to this repo"
    exit 1
fi

echo "=== THIA → Skill Catalog Sync ==="
echo "Source: $THIA_SKILLS_DIR"
echo "Target: $REPO_DIR"
echo ""

# Count changes
added=0
updated=0
unchanged=0

for src_file in "$THIA_SKILLS_DIR"/agent_skills_*.md; do
    [ -f "$src_file" ] || continue
    filename=$(basename "$src_file")
    dst_file="$REPO_DIR/$filename"

    if [ ! -f "$dst_file" ]; then
        if [ "$DRY_RUN" = true ]; then
            echo "[ADD] $filename"
        else
            cp "$src_file" "$dst_file"
            echo "[ADD] $filename"
        fi
        added=$((added + 1))
    elif ! diff -q "$src_file" "$dst_file" > /dev/null 2>&1; then
        if [ "$DRY_RUN" = true ]; then
            echo "[UPD] $filename"
            diff --unified=0 "$dst_file" "$src_file" | head -20
            echo ""
        else
            cp "$src_file" "$dst_file"
            echo "[UPD] $filename"
        fi
        updated=$((updated + 1))
    else
        unchanged=$((unchanged + 1))
    fi
done

# Check for files in catalog that no longer exist in THIA
removed=0
for dst_file in "$REPO_DIR"/agent_skills_*.md; do
    [ -f "$dst_file" ] || continue
    filename=$(basename "$dst_file")
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
echo "  Unchanged: $unchanged"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "(dry run — no files changed)"
fi
