#!/usr/bin/env python3
"""
build_field.py — Assemble the living field for the nightly agent.

This is NOT a static template. It generates a fresh markdown document every
run from the actual state of the system:

- Autopsy of the previous run (injected FIRST — the agent learns from it)
- Current seed (plan, direction, tensions)
- Convergence map (where multiple tensions point to the same place)
- Last N scientific reports (what has been found, what is open)
- Operator observations (if configured)
- Pending affinatore signal (if previous evolution report is pending)

The agent reads this and cannot do anything but build on what is here.
The structure forces consecutio — each run starts from where the previous
one arrived.

Regressive Repair is operative here: if the previous run failed, the
regressive node and recommendation appear at the top of the field. The agent
does not need to ask "what happened" — it reads.
"""

import json
import os
import glob
from pathlib import Path

# === CONFIG (parameterized at install) ==============================
ROOT = Path(os.environ.get("RESEARCHER_DATA_ROOT",
                           str(Path(__file__).parent.parent / "data")))
AGENT_CONTEXT_PATH = os.environ.get("RESEARCHER_AGENT_CONTEXT",
                                    str(Path(__file__).parent / "AGENT_CONTEXT.md"))
RECENT_REPORTS_N = int(os.environ.get("RESEARCHER_RECENT_REPORTS", "3"))
# ====================================================================


def load_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return None


def recent_reports(n: int) -> list[dict]:
    """Parse the last N scientific reports for title / findings / verdict."""
    pattern = str(ROOT / "reports" / "agent_*.md")
    files = sorted(glob.glob(pattern),
                   key=lambda p: os.path.getmtime(p), reverse=True)[:n]
    out = []
    for f in files:
        try:
            content = Path(f).read_text()
        except Exception:
            continue
        title = ""
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
        # Heuristic: first line or title
        out.append({
            "file": Path(f).name,
            "title": title,
            "preview": content[:500],
        })
    return out


def convergence_map(seed: dict) -> str:
    """Find keywords shared across multiple tensions — where potential concentrates."""
    tensions = seed.get("tensioni", [])
    if not tensions:
        return ""
    # Simple heuristic: tokens that appear in claim of >= 2 tensions
    tokens = {}
    for t in tensions:
        claim = str(t.get("claim", "")).lower()
        # crude token split — users can replace with their own convergence logic
        for tok in set(claim.split()):
            if len(tok) < 4:
                continue
            tokens.setdefault(tok, []).append(t.get("id", "?"))
    hot = [(tok, ids) for tok, ids in tokens.items() if len(ids) >= 2]
    hot.sort(key=lambda x: -len(x[1]))
    if not hot:
        return ""
    lines = []
    for tok, ids in hot[:5]:
        lines.append(f'  "{tok}" → {", ".join(ids)}')
    return "\n".join(lines)


def build_field() -> str:
    seed = load_json(ROOT / "seed.json") or {}
    health = load_json(ROOT / "lab_health.json") or {}

    parts = []

    # Reference to static agent context
    if Path(AGENT_CONTEXT_PATH).exists():
        parts.append(f"Read `{AGENT_CONTEXT_PATH}` for the domain model, rules, and errors to avoid.\n")

    # ─── Autopsy of previous run (Regressive Repair) ──────────────
    # This comes FIRST so the agent starts aware.
    if health:
        status = health.get("status", "unknown")
        if status == "completed":
            duration = health.get("duration_s", "?")
            parts.append(f"## Previous run: completed ({duration}s) — continue from consecutio.\n")
        elif status in ("timeout_during_tool", "api_error", "report_missing",
                        "no_start", "autopsy_failed"):
            parts.append("## ATTENTION — Previous run did not complete")
            parts.append(f"- Status: **{status}**")
            rn = health.get("regressive_node")
            if rn:
                parts.append(f"- Regressive node: {rn}")
            rec = health.get("recommendation")
            if rec:
                parts.append(f"- Recommendation: {rec}")
            last_tu = health.get("last_tool_use")
            if last_tu:
                parts.append(f"- Last interrupted tool: {last_tu.get('name')} — input: `{str(last_tu.get('input_preview',''))[:200]}`")
            parts.append("")
            parts.append(
                "Apply Regressive Repair: do NOT repeat the same shape of failure. "
                "If the regressive node is 'field without pre-computed data', "
                "do NOT regenerate from scratch inside a single tool call. "
                "If the node is 'scope too wide for budget', reduce scope, "
                "do not extend time.\n"
            )
        if health.get("affinatore_status") == "pending":
            parts.append(f"_Affinatore of previous run: pending ({health.get('affinatore_reason','?')})_\n")

    # ─── Current state: plan, direction ──────────────────────────
    plan = seed.get("piano", "?")
    direction = seed.get("direzione", "?")[:200]
    parts.append(f"## Plan {plan} — {direction}\n")

    # ─── Active tensions ─────────────────────────────────────────
    tensions = seed.get("tensioni", [])[:8]
    if tensions:
        parts.append("## Active tensions")
        for t in tensions:
            intensity = t.get("intensita", t.get("intensità", "?"))
            claim = str(t.get("claim", ""))[:180]
            parts.append(f"- [{t.get('id','?')}] ({intensity}) {claim}")
        parts.append("")

    # ─── Convergence map ─────────────────────────────────────────
    conv = convergence_map(seed)
    if conv:
        parts.append("## Convergence — where multiple tensions point to the same place")
        parts.append(conv)
        parts.append("This is where potential concentrates. Do not ignore it.\n")

    # ─── Last reports — consecutio base ──────────────────────────
    reports = recent_reports(RECENT_REPORTS_N)
    if reports:
        parts.append(f"## Last {len(reports)} runs — where you are continuing from")
        for r in reports:
            parts.append(f"### {r['title'] or r['file']}")
            if r["preview"]:
                parts.append(f"Preview: {r['preview'][:300]}...")
            parts.append("")
        parts.append("Do not repeat these experiments. Continue from where they arrived — the consecutio.\n")

    return "\n".join(parts)


if __name__ == "__main__":
    print(build_field())
