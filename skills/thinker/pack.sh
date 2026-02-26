#!/bin/bash
# pack.sh — Generate .skill files from SKILL.md sources
# Usage: ./pack.sh [it|en]  (default: both)
#
# Each .skill file is a zip archive: skill-name/SKILL.md
# Upload to Claude.ai → Settings → Profile → Skills

set -e

LANG_FILTER="${1:-both}"
DIST_DIR="dist"

mkdir -p "$DIST_DIR/it" "$DIST_DIR/en"

pack_lang() {
    local lang="$1"
    local src_dir="$lang"
    local out_dir="$DIST_DIR/$lang"
    local count=0

    echo "Packing $lang skills..."

    for skill_dir in "$src_dir"/*/; do
        [ -d "$skill_dir" ] || continue
        skill_name=$(basename "$skill_dir")
        if [ -f "$skill_dir/SKILL.md" ]; then
            (cd "$src_dir" && zip -q "$skill_name.skill" "$skill_name/SKILL.md")
            mv "$src_dir/$skill_name.skill" "$out_dir/"
            count=$((count + 1))
        fi
    done

    echo "  $count skills packed to $out_dir/"
}

if [ "$LANG_FILTER" = "it" ] || [ "$LANG_FILTER" = "both" ]; then
    pack_lang "it"
fi

if [ "$LANG_FILTER" = "en" ] || [ "$LANG_FILTER" = "both" ]; then
    pack_lang "en"
fi

echo "Done. Upload .skill files from dist/ to Claude.ai → Settings → Skills"
