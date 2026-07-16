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
#   ./update.sh /path/to/project --dry-run
#   ./update.sh /path/to/project --plan
#   ./update.sh /path/to/project --check
#   ./update.sh /path/to/project --legacy-all
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
PLAN_MODE=""
CHECK_MODE=""
LEGACY_ALL=""
DRY_RUN=""

for arg in "$@"; do
    [ "$arg" = "--plan" ] && PLAN_MODE="true"
    [ "$arg" = "--check" ] && CHECK_MODE="true"
    [ "$arg" = "--legacy-all" ] && LEGACY_ALL="true"
    [ "$arg" = "--dry-run" ] && DRY_RUN="true"
done

TEMP_FILES=""
cleanup() {
    if [ -n "$TEMP_FILES" ]; then
        rm -f $TEMP_FILES 2>/dev/null || true
    fi
}
trap cleanup EXIT

make_temp() {
    local f
    f=$(mktemp)
    TEMP_FILES="$TEMP_FILES $f"
    printf '%s\n' "$f"
}

if [ "$PROJECT_DIR" = "--plan" ] || [ "$PROJECT_DIR" = "--check" ] || [ "$PROJECT_DIR" = "--dry-run" ]; then
    PROJECT_DIR="."
fi

require_node() {
    if ! command -v node >/dev/null 2>&1; then
        echo "ERROR: node is required for this command but was not found in PATH"
        exit 1
    fi
}

if [ -n "$CHECK_MODE" ]; then
    require_node
    node "$SEED_DIR/scripts/validate_capability_registry.js"
    exit $?
fi

require_node
node "$SEED_DIR/scripts/validate_capability_registry.js" >/dev/null

UNAME_S="$(uname -s 2>/dev/null || echo unknown)"
WINDOWS_BASH=""
case "$UNAME_S" in
    MINGW*|MSYS*|CYGWIN*) WINDOWS_BASH="true" ;;
esac

if [ -n "$WINDOWS_BASH" ] && [ -z "$DRY_RUN" ] && [ "${DND_SEED_ALLOW_WINDOWS_BASH:-}" != "1" ]; then
    echo "ERROR: Windows Bash runtime detected."
    echo "Refusing to update files unless DND_SEED_ALLOW_WINDOWS_BASH=1 is set."
    echo "Use --plan or --dry-run first, or use Node read-only checks."
    exit 1
fi

if [ -z "$DRY_RUN" ]; then
    case "$PROJECT_DIR" in
        ""|"/"|"\\"|"C:"|"C:\\"|"C:/"|".."|"../"*)
            echo "ERROR: Refusing unsafe project directory: $PROJECT_DIR"
            exit 1
            ;;
    esac
fi

TARGET_POLICY="write"
[ -n "$DRY_RUN" ] && TARGET_POLICY="dry-run"
[ -n "$PLAN_MODE" ] && TARGET_POLICY="read-only"
if ! TARGET_RESULT=$(node "$SEED_DIR/scripts/validate_profile.js" --target-only="$PROJECT_DIR" --target-policy="$TARGET_POLICY" --json); then
    printf '%s' "$TARGET_RESULT" | node -e "const fs=require('fs'); const r=JSON.parse(fs.readFileSync(0,'utf8')); for (const e of r.errors || []) console.error('ERROR: ' + e)"
    exit 1
fi
PROJECT_DIR=$(printf '%s' "$TARGET_RESULT" | node -e "const fs=require('fs'); const r=JSON.parse(fs.readFileSync(0,'utf8')); process.stdout.write(r.resolved_project_dir.replace(/\\\\/g, '/'))")

CLAUDE_TARGET="$PROJECT_DIR/.claude"
NEUTRAL_TARGET="$PROJECT_DIR/.seed"
CLAUDE_PROFILE="$CLAUDE_TARGET/seed_profile.json"
NEUTRAL_PROFILE="$NEUTRAL_TARGET/seed_profile.json"

if [ ! -d "$CLAUDE_TARGET" ] && [ ! -d "$NEUTRAL_TARGET" ]; then
    echo "ERROR: No .seed/ or .claude/ directory found in $PROJECT_DIR"
    echo "Run install.sh first, then use update.sh for subsequent updates."
    exit 1
fi

echo "=== D-ND Seed Updater ==="
echo "Seed: $SEED_DIR"
echo "Project: $PROJECT_DIR"
echo ""

if [ -n "$PLAN_MODE" ]; then
    if [ -f "$NEUTRAL_PROFILE" ]; then
        PROFILE="$NEUTRAL_PROFILE"
    else
        PROFILE="$CLAUDE_PROFILE"
    fi
    if [ ! -f "$PROFILE" ]; then
        echo "ERROR: No saved seed profile found at $PROFILE"
        echo "Run install.sh first, or pass a profile to install.sh --plan."
        exit 1
    fi
    require_node
    node "$SEED_DIR/scripts/validate_profile.js" "$PROFILE" --target-policy=read-only --effective-project-dir="$PROJECT_DIR" >/dev/null
    node "$SEED_DIR/scripts/installer_option_router.js" "$PROFILE"
    exit $?
fi

if [ -f "$NEUTRAL_PROFILE" ]; then
    PROFILE="$NEUTRAL_PROFILE"
else
    PROFILE="$CLAUDE_PROFILE"
fi

if [ -f "$PROFILE" ]; then
    WRITE_POLICY=$(node -e "const p=require(process.argv[1]); process.stdout.write(p.write_policy || 'target_write')" "$PROFILE")
    if [ "$WRITE_POLICY" = "plan_only" ] && [ -z "$DRY_RUN" ]; then
        echo "ERROR: Saved profile write_policy is plan_only."
        echo "Use --plan or --dry-run; this profile cannot invoke updater writers."
        exit 1
    fi
    node "$SEED_DIR/scripts/validate_profile.js" "$PROFILE" --target-policy="$TARGET_POLICY" --effective-project-dir="$PROJECT_DIR" >/dev/null
elif [ -z "$LEGACY_ALL" ]; then
    echo "ERROR: No saved seed profile found at $PROFILE"
    echo "Run install.sh first, or use --legacy-all for compatibility updates."
    exit 1
fi

INCLUDED_PATHS_FILE=""
if [ -z "$LEGACY_ALL" ]; then
    INCLUDED_PATHS_FILE=$(make_temp)
    node "$SEED_DIR/scripts/installer_option_router.js" "$PROFILE" --paths > "$INCLUDED_PATHS_FILE"
    if [ -n "$DRY_RUN" ]; then
        echo "[DRY-RUN] Would save update plan to $CLAUDE_TARGET/seed_update_plan.json"
        echo "[DRY-RUN] Would save neutral update plan to $NEUTRAL_TARGET/seed_update_plan.json"
    else
        mkdir -p "$CLAUDE_TARGET" "$NEUTRAL_TARGET"
        node "$SEED_DIR/scripts/installer_option_router.js" "$PROFILE" --json > "$CLAUDE_TARGET/seed_update_plan.json"
        cp "$CLAUDE_TARGET/seed_update_plan.json" "$NEUTRAL_TARGET/seed_update_plan.json"
    fi
    echo "Registry gate: enabled"
    [ -z "$DRY_RUN" ] && echo "Update plan saved to $CLAUDE_TARGET/seed_update_plan.json"
    [ -z "$DRY_RUN" ] && echo "Neutral update plan saved to $NEUTRAL_TARGET/seed_update_plan.json"
    echo ""
else
    echo "Registry gate: bypassed with --legacy-all"
    echo ""
fi

capability_selected() {
    local rel="$1"
    if [ -n "$LEGACY_ALL" ]; then
        return 0
    fi
    grep -Fxq "$rel" "$INCLUDED_PATHS_FILE"
}

tracked_target_is_unmodified() {
    local rel="$1"
    git -C "$PROJECT_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1 || return 1
    git -C "$PROJECT_DIR" ls-files --error-unmatch -- "$rel" >/dev/null 2>&1 || return 1
    git -C "$PROJECT_DIR" diff --quiet -- "$rel" || return 1
    git -C "$PROJECT_DIR" diff --cached --quiet -- "$rel" || return 1
    return 0
}

UPDATED=0
SKIPPED=0
ADDED=0

# --- Update hook templates ---
echo "## Hooks"
for tmpl in "$SEED_DIR"/templates/hooks/*.tmpl; do
    [ -f "$tmpl" ] || continue
    name=$(basename "$tmpl" .tmpl)
    rel="templates/hooks/$name.tmpl"
    if ! capability_selected "$rel"; then
        echo "  - $name (skipped by registry plan)"
        continue
    fi
    target="$PROJECT_DIR/.claude/hooks/$name"

    # Instantiate template variables if profile exists
    instantiate() {
        local content="$1"
        if [ -f "$PROFILE" ]; then
            local content_file
            content_file=$(make_temp)
            printf '%s' "$content" > "$content_file"
            content=$(node - "$PROFILE" "$content_file" <<'NODE'
const fs = require('fs');
const profile = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
let content = fs.readFileSync(process.argv[3], 'utf8');
const replacements = {
  PROJECT_DIR: profile.project_dir || '.',
  NODE_ID: profile.node_id || 'UNKNOWN'
};
for (const [key, value] of Object.entries(replacements)) {
  content = content.split(`{{${key}}}`).join(String(value));
}
process.stdout.write(content);
NODE
)
        fi
        echo "$content"
    }

    if [ ! -f "$target" ]; then
        echo "  + $name (new)"
        if [ -n "$DRY_RUN" ]; then
            echo "    [DRY-RUN] would create $target"
        else
            mkdir -p "$(dirname "$target")"
            instantiate "$(cat "$tmpl")" > "$target"
            chmod +x "$target" 2>/dev/null
            ADDED=$((ADDED + 1))
        fi
    elif [ "$tmpl" -nt "$target" ]; then
        # Template is newer — check if user modified the target
        if tracked_target_is_unmodified ".claude/hooks/$name"; then
            echo "  ~ $name (updated)"
            if [ -n "$DRY_RUN" ]; then
                echo "    [DRY-RUN] would update $target"
            else
                instantiate "$(cat "$tmpl")" > "$target"
                UPDATED=$((UPDATED + 1))
            fi
        else
            echo "  . $name (skipped — user modified)"
            if [ -n "$DRY_RUN" ]; then
                echo "    [DRY-RUN] would save ${target}.new for manual review"
            else
                instantiate "$(cat "$tmpl")" > "${target}.new"
                echo "    → saved as ${name}.new for manual review"
            fi
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
    if ! capability_selected "plugins/d-nd-core/skills/$name"; then
        echo "  - $name (skipped by registry plan)"
        continue
    fi
    target="$PROJECT_DIR/.claude/skills/$name"

    if [ ! -d "$target" ]; then
        echo "  + $name (new skill)"
        if [ -n "$DRY_RUN" ]; then
            echo "    [DRY-RUN] would copy to $target"
        else
            mkdir -p "$(dirname "$target")"
            cp -r "$skill_dir" "$target"
            ADDED=$((ADDED + 1))
        fi
    fi
done
echo ""

# --- Update projector tools ---
echo "## Projector"
PROJECTOR_SRC="$SEED_DIR/plugins/d-nd-core/scripts"
PROJECTOR_DST="$PROJECT_DIR/d-nd-tools"
if ! capability_selected "plugins/d-nd-core/skills/scenario-projector"; then
    echo "  Projector skipped by registry plan."
elif [ -d "$PROJECTOR_DST" ] && [ -f "$PROJECTOR_SRC/scenario_projector.py" ]; then
    # Existing projector files have no installed-source hash. Preserve them and
    # stage newer Seed versions for explicit review instead of overwriting.
    if [ ! -f "$PROJECTOR_DST/scenario_projector.py" ]; then
        if [ -n "$DRY_RUN" ]; then
            echo "  + scenario_projector.py (would add)"
        else
            cp "$PROJECTOR_SRC/scenario_projector.py" "$PROJECTOR_DST/"
            echo "  + scenario_projector.py (new)"
        fi
        ADDED=$((ADDED + 1))
    elif [ "$PROJECTOR_SRC/scenario_projector.py" -nt "$PROJECTOR_DST/scenario_projector.py" ]; then
        if [ -n "$DRY_RUN" ]; then
            echo "  . scenario_projector.py (would save .new for review)"
        else
            cp "$PROJECTOR_SRC/scenario_projector.py" "$PROJECTOR_DST/scenario_projector.py.new"
            echo "  . scenario_projector.py (saved .new for review)"
        fi
        SKIPPED=$((SKIPPED + 1))
    fi
    if [ -f "$PROJECTOR_SRC/SCENARIO_PROJECTOR_GUIDE.md" ]; then
        if [ ! -f "$PROJECTOR_DST/SCENARIO_PROJECTOR_GUIDE.md" ]; then
            if [ -n "$DRY_RUN" ]; then
                echo "  + SCENARIO_PROJECTOR_GUIDE.md (would add)"
            else
                cp "$PROJECTOR_SRC/SCENARIO_PROJECTOR_GUIDE.md" "$PROJECTOR_DST/"
                echo "  + SCENARIO_PROJECTOR_GUIDE.md (new)"
            fi
            ADDED=$((ADDED + 1))
        elif [ "$PROJECTOR_SRC/SCENARIO_PROJECTOR_GUIDE.md" -nt "$PROJECTOR_DST/SCENARIO_PROJECTOR_GUIDE.md" ]; then
            if [ -n "$DRY_RUN" ]; then
                echo "  . SCENARIO_PROJECTOR_GUIDE.md (would save .new for review)"
            else
                cp "$PROJECTOR_SRC/SCENARIO_PROJECTOR_GUIDE.md" "$PROJECTOR_DST/SCENARIO_PROJECTOR_GUIDE.md.new"
                echo "  . SCENARIO_PROJECTOR_GUIDE.md (saved .new for review)"
            fi
            SKIPPED=$((SKIPPED + 1))
        fi
    fi
    # Add new example seeds
    if [ -z "$DRY_RUN" ]; then
        mkdir -p "$PROJECTOR_DST/examples"
    fi
    for f in "$PROJECTOR_SRC"/examples/*.json "$PROJECTOR_SRC"/examples/*.py "$PROJECTOR_SRC"/examples/*.md; do
        [ -f "$f" ] || continue
        fname=$(basename "$f")
        if [ ! -f "$PROJECTOR_DST/examples/$fname" ]; then
            if [ -n "$DRY_RUN" ]; then
                echo "  + examples/$fname (would add)"
            else
                cp "$f" "$PROJECTOR_DST/examples/"
                echo "  + examples/$fname (new)"
            fi
            ADDED=$((ADDED + 1))
        elif [ "$f" -nt "$PROJECTOR_DST/examples/$fname" ]; then
            if [ -n "$DRY_RUN" ]; then
                echo "  . examples/$fname (would save .new for review)"
            else
                cp "$f" "$PROJECTOR_DST/examples/$fname.new"
                echo "  . examples/$fname (saved .new for review)"
            fi
            SKIPPED=$((SKIPPED + 1))
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
