#!/usr/bin/env python3
"""
affinatore.py — Reflective observer on the step itself.

Runs AFTER the scientific report is written. Reads the session jsonl, the
report, and the health. Launches a separate AI instance that observes the
QUALITY of the step — not the result. Produces `evolution/evolution_{TS}.md`
with structural proposals on the system, not on the experiment outcome.

Degrades gracefully: if the LLM call fails (timeout, rate limit, anything),
the scientific report is already saved. The health file is marked
`affinatore_status: pending` — the next night's autopsy sees the signal.

This script CAN time out (it makes an LLM call). That is a different failure
form than the cycle itself. The autopsy runs BEFORE the cycle; the affinatore
runs AFTER. If the affinatore dies, the cycle already delivered value.
"""

import json
import sys
import os
import subprocess
import argparse
from datetime import datetime, timezone
from pathlib import Path

# === CONFIG (parameterized at install) ==============================
ROOT = Path(os.environ.get("RESEARCHER_DATA_ROOT",
                           str(Path(__file__).parent.parent / "data")))
REPORTS = ROOT / "reports"
HEALTH = ROOT / "lab_health.json"
EVOLUTION_DIR = ROOT / "evolution"

# AI CLI binary — defaults to claude, adapt if you use another.
AI_CLI = os.environ.get("RESEARCHER_AI_CLI", "claude")

# Project root (where the agent is invoked from)
PROJECT_ROOT = Path(os.environ.get("RESEARCHER_PROJECT_ROOT",
                                   str(Path(__file__).parent.parent.parent)))

# Budget for the affinatore call (seconds). 300 is generous for reflection;
# it is NOT the cycle budget. Tune if needed.
AFFINATORE_BUDGET = int(os.environ.get("RESEARCHER_AFFINATORE_BUDGET", "300"))
# ====================================================================


AFFINATORE_PROMPT = """You are the Affinatore (Refiner) of the Researcher cycle.
Your role is to observe the STEP, not the result.

The scientific report was already written by the nightly producer. You do not
re-evaluate it. You observe the quality of the PATH: where it produced
superfluous latency, where the system could have inverted earlier, which
relational condition was missing at the regressive node, which possibilities
emerge from the step itself.

Apply Regressive Repair: if you see a failure or friction, do NOT propose
patches on the present (raise timeout, add retries, reactive guards = det=+1).
Walk back to the node where the condition was missing and propose there
(det=-1).

Apply Refinement: evolutionary proposals enter consecutio — they do not
interrupt the producer's cycle, they add direction for the next cycle.

Write a brief, clear evolution report. Structure:

## Observation of the step
What the step did — as a trajectory, not a list of actions.

## Superfluous latency or friction
Where the system spent energy without producing. If none: "none — clean step".

## Regressive node (if failure or friction)
Where the relational condition was missing. The fix lives there, not in
the present of the bug.

## Emerging possibilities
Concrete directions the step opened — for the next cycle. Specific, not generic.

## Consecutio
One line: where the next cycle could continue, if it chooses.

Be concise. Half a page beats a full page. Do not repeat the experiment —
observe it.

---

Context of the run just concluded:

{context}

---

Write the evolution report:
"""


def build_context(ts: str) -> str:
    """Assemble the context the affinatore reads."""
    parts = []

    if HEALTH.exists():
        parts.append("## Autopsy health\n\n```json\n" +
                     HEALTH.read_text() + "\n```\n")

    report_md = REPORTS / f"agent_{ts}.md"
    if report_md.exists():
        parts.append(f"## Scientific report of the run\n\n{report_md.read_text()[:6000]}\n")
    else:
        parts.append("## Scientific report\n\n_Not present — the run did not complete._\n")

    try:
        health = json.loads(HEALTH.read_text())
        stats = health.get("session_stats", {})
        parts.append(
            f"## Session stats\n"
            f"- tool_use: {stats.get('tool_use')}\n"
            f"- tool_result: {stats.get('tool_result')}\n"
            f"- thinking: {stats.get('thinking')}\n"
            f"- text: {stats.get('text')}\n"
            f"- unanswered_tool_use: {stats.get('unanswered_tool_use')}\n"
            f"- duration: {stats.get('duration_s')}s\n"
        )
        last_text = stats.get("last_text")
        if last_text:
            parts.append(f"## Last text produced by the agent\n\n{last_text}\n")
    except Exception:
        pass

    return "\n".join(parts)


def mark_pending(ts: str, reason: str):
    """Mark affinatore as pending in health file — degrade gracefully."""
    try:
        if HEALTH.exists():
            h = json.loads(HEALTH.read_text())
        else:
            h = {}
        h["affinatore_status"] = "pending"
        h["affinatore_reason"] = reason
        h["affinatore_ts"] = ts
        HEALTH.write_text(json.dumps(h, indent=2, ensure_ascii=False))
    except Exception:
        pass


def run_affinatore(ts: str, dry_run: bool = False) -> int:
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    out_path = EVOLUTION_DIR / f"evolution_{ts}.md"

    context = build_context(ts)
    prompt = AFFINATORE_PROMPT.format(context=context)

    if dry_run:
        print(prompt[:2500])
        print(f"\n[dry-run] would write to {out_path}")
        return 0

    try:
        result = subprocess.run(
            [
                "timeout", "--kill-after=30", str(AFFINATORE_BUDGET),
                AI_CLI,
                "--permission-mode", "acceptEdits",
                "-p", prompt,
                "--max-turns", "3",
            ],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout.strip()
        if output and len(output) > 50:
            out_path.write_text(output)
            print(f"affinatore: evolution report written → {out_path}")
            return 0
        else:
            print(f"affinatore: empty or too short output (exit {result.returncode})",
                  file=sys.stderr)
            mark_pending(ts, f"empty output (exit {result.returncode})")
            return 1
    except Exception as e:
        print(f"affinatore: call failed: {e}", file=sys.stderr)
        mark_pending(ts, f"exception: {e}")
        return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="Run timestamp YYYYMMDD_HHMM; default = latest from health")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print prompt instead of calling LLM")
    args = ap.parse_args()

    if args.run:
        ts = args.run
    else:
        if not HEALTH.exists():
            print("affinatore: no health file — run autopsy.py first", file=sys.stderr)
            return 1
        h = json.loads(HEALTH.read_text())
        ts = h.get("run_timestamp")
        if not ts:
            print("affinatore: no run_timestamp in health", file=sys.stderr)
            return 1

    return run_affinatore(ts, dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
