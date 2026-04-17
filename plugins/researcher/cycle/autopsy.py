#!/usr/bin/env python3
"""
autopsy.py — Regressive autopsy of the previous nightly run.

Reads the previous run's session jsonl + raw_log + scientific report.
Classifies outcome. Identifies the regressive node where the relational
condition was missing. Writes `data/lab_health.json` which `build_field.py`
injects into the next run's living field.

Design principle (det=-1 on the repair system itself):
- Pure I/O: file read + parse + classify + write. No LLM calls. No network.
- Timeout structurally impossible for the same reason the cycle can time out
  (the cycle's failure form is not available here — different machinery).
- Idempotent: can be rerun without side effects.
- Degrades gracefully: on internal error, writes `status: autopsy_failed`
  and the cycle starts anyway with minimal context.

The failure categories:
- `completed` — report written, tool_use matches tool_result
- `timeout_during_tool` — an unanswered tool_use at the tail (the classic
  "agent regenerated something from scratch inside one tool call and ran
  past the budget")
- `api_error` — explicit error entries in the session
- `report_missing` — session finished but no report file
- `no_start` — no session found (launcher never initialized properly)
- `autopsy_failed` — this script itself crashed (signal to investigate here,
  but the cycle continues with empty context)

Configuration: set ROOT to your project data dir via env or edit below.
"""

import json
import sys
import os
import re
import argparse
from datetime import datetime, timezone
from pathlib import Path

# === CONFIG (parameterized at install) ==============================
# ROOT is the directory containing `reports/` and where `lab_health.json`
# will be written. The installer adapts this.
ROOT = Path(os.environ.get("RESEARCHER_DATA_ROOT",
                           str(Path(__file__).parent.parent / "data")))
REPORTS = ROOT / "reports"
HEALTH = ROOT / "lab_health.json"

# SESSIONS_DIR points to where the AI coder persists its session jsonl files.
# For Claude Code this is ~/.claude/projects/<encoded-path>/.
# The installer writes the correct path based on your environment.
SESSIONS_DIR = Path(os.environ.get("RESEARCHER_SESSIONS_DIR",
                                   str(Path.home() / ".claude" / "projects")))
# ====================================================================


def find_session_jsonl(ts: str) -> Path | None:
    """Find the jsonl session whose first timestamp is near the run timestamp."""
    if not SESSIONS_DIR.exists():
        return None
    try:
        run_dt = datetime.strptime(ts, "%Y%m%d_%H%M").replace(tzinfo=timezone.utc)
    except ValueError:
        return None

    candidates = []
    # Search across all project subdirs — the session could be under any
    # encoded-path prefix depending on cwd at launch.
    for f in SESSIONS_DIR.rglob("*.jsonl"):
        try:
            with open(f) as fh:
                for line in fh:
                    try:
                        d = json.loads(line)
                        t = d.get("timestamp", "")
                        if t:
                            first = datetime.fromisoformat(t.replace("Z", "+00:00"))
                            delta = abs((first - run_dt).total_seconds())
                            if delta < 600:  # within 10 min of run start
                                candidates.append((delta, f))
                            break
                    except Exception:
                        continue
        except Exception:
            continue
    if not candidates:
        return None
    return sorted(candidates)[0][1]


def parse_session(jsonl: Path) -> dict:
    """Parse jsonl session, extract counts and tail signals."""
    tu = tr = th = tx = 0
    first_ts = last_ts = None
    last_tool_use = None
    last_text = None
    error_entries = []
    tool_use_ids = []
    tool_result_ids = set()

    for line in open(jsonl):
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("timestamp", "")
        if t:
            if not first_ts:
                first_ts = t
            last_ts = t

        msg = d.get("message", {})
        if not isinstance(msg, dict):
            continue
        content = msg.get("content", [])
        if not isinstance(content, list):
            continue

        for c in content:
            if not isinstance(c, dict):
                continue
            ty = c.get("type", "")
            if ty == "tool_use":
                tu += 1
                tool_use_ids.append(c.get("id", ""))
                last_tool_use = {
                    "id": c.get("id", ""),
                    "name": c.get("name", ""),
                    "input_preview": str(c.get("input", ""))[:400],
                    "timestamp": t,
                }
            elif ty == "tool_result":
                tr += 1
                tool_result_ids.add(c.get("tool_use_id", ""))
            elif ty == "thinking":
                th += 1
            elif ty == "text":
                tx += 1
                last_text = c.get("text", "")[:500]

        if d.get("type") == "error" or msg.get("type") == "error":
            error_entries.append(t)

    unanswered_ids = [tid for tid in tool_use_ids if tid not in tool_result_ids]
    unanswered_count = len(unanswered_ids)

    duration_s = None
    if first_ts and last_ts:
        try:
            a = datetime.fromisoformat(first_ts.replace("Z", "+00:00"))
            b = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
            duration_s = int((b - a).total_seconds())
        except Exception:
            pass

    return {
        "tool_use": tu,
        "tool_result": tr,
        "thinking": th,
        "text": tx,
        "unanswered_tool_use": unanswered_count,
        "last_tool_use": last_tool_use if unanswered_count else None,
        "last_text": last_text,
        "first_ts": first_ts,
        "last_ts": last_ts,
        "duration_s": duration_s,
        "error_entries": error_entries,
    }


def classify(session: dict | None, raw_log: Path, report_md: Path) -> dict:
    """Classify run outcome and name the regressive node."""
    report_exists = report_md.exists() and report_md.stat().st_size > 0
    raw_log_size = raw_log.stat().st_size if raw_log.exists() else 0

    if session is None:
        return {
            "status": "no_start",
            "regressive_node": (
                "launcher: AI coder CLI failed to initialize (auth, binary "
                "missing, environment, or credentials)"
            ),
            "recommendation": (
                "verify CLI health, env vars, credentials. The fix lives in "
                "the launcher environment, not in the cycle timeout."
            ),
        }

    unans = session["unanswered_tool_use"]
    duration = session["duration_s"] or 0
    errors = session["error_entries"]

    if errors:
        return {
            "status": "api_error",
            "regressive_node": "upstream API failure during run",
            "recommendation": (
                "verify provider API status. If recurrent, the regressive "
                "node is the retry/backoff policy in the launcher — not the "
                "cycle budget."
            ),
            "error_timestamps": errors[:3],
        }

    if report_exists and unans == 0:
        return {
            "status": "completed",
            "regressive_node": None,
            "duration_s": duration,
        }

    if unans > 0:
        last = session.get("last_tool_use") or {}
        tool_name = last.get("name", "?")
        preview = last.get("input_preview", "")
        return {
            "status": "timeout_during_tool",
            "regressive_node": (
                f"living field did not contain the pre-computed input the "
                f"agent needed; the agent had to regenerate from scratch "
                f"inside a single tool_use ({tool_name}) that did not "
                f"complete within residual budget. The fix does not live "
                f"in the timeout value — it lives in the missing field "
                f"condition upstream."
            ),
            "last_tool_use": {
                "name": tool_name,
                "input_preview": preview,
            },
            "duration_s": duration,
            "recommendation": (
                "pre-compute the dataset the agent tends to rebuild "
                "(baselines, normalizations, heavy transforms) and include "
                "a pointer in the next run's field. The agent will detect "
                "the cached input and branch accordingly. Do NOT raise the "
                "timeout (det=+1 — accumulation)."
            ),
        }

    if not report_exists and unans == 0:
        return {
            "status": "report_missing",
            "regressive_node": (
                "agent finished the tool sequence but did not emit the "
                "final report file — likely last action was code execution "
                "not followed by a Write step to `reports/agent_{TS}.md`."
            ),
            "recommendation": (
                "reinforce in the prompt: after the experiment, MUST write "
                "report to `reports/agent_{TS}.md` as final step."
            ),
            "duration_s": duration,
        }

    return {
        "status": "unknown",
        "regressive_node": "autopsy could not classify this run from available signals",
        "duration_s": duration,
        "raw_log_size": raw_log_size,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", help="Run timestamp YYYYMMDD_HHMM; default = latest")
    ap.add_argument("--output", default=str(HEALTH), help="Output path for health json")
    args = ap.parse_args()

    try:
        if args.run:
            ts = args.run
        else:
            raw_logs = sorted(REPORTS.glob("agent_*_raw.log"),
                              key=lambda p: p.stat().st_mtime, reverse=True)
            if not raw_logs:
                out = {
                    "status": "no_run_found",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
                Path(args.output).write_text(json.dumps(out, indent=2))
                print(f"autopsy: no run found → {args.output}")
                return 0
            m = re.search(r"agent_(\d{8}_\d{4})_raw\.log", raw_logs[0].name)
            if not m:
                print(f"autopsy: cannot parse timestamp from {raw_logs[0].name}",
                      file=sys.stderr)
                return 1
            ts = m.group(1)

        raw_log = REPORTS / f"agent_{ts}_raw.log"
        report_md = REPORTS / f"agent_{ts}.md"
        jsonl = find_session_jsonl(ts)

        session = parse_session(jsonl) if jsonl else None
        result = classify(session, raw_log, report_md)

        health = {
            "run_timestamp": ts,
            "autopsy_run_at": datetime.now(timezone.utc).isoformat(),
            "jsonl_path": str(jsonl) if jsonl else None,
            "raw_log_bytes": raw_log.stat().st_size if raw_log.exists() else 0,
            "report_present": report_md.exists() and report_md.stat().st_size > 0,
            "session_stats": session,
            **result,
        }

        Path(args.output).write_text(json.dumps(health, indent=2, ensure_ascii=False))
        print(f"autopsy: {ts} → {result['status']}")
        if result.get("regressive_node"):
            print(f"  regressive node: {result['regressive_node'][:120]}")
        return 0

    except Exception as e:
        # Degrade gracefully
        try:
            fallback = {
                "status": "autopsy_failed",
                "error": str(e),
                "autopsy_run_at": datetime.now(timezone.utc).isoformat(),
                "regressive_node": (
                    "the autopsy script itself failed — signal to investigate "
                    "autopsy.py. The cycle continues with empty context."
                ),
            }
            Path(args.output).write_text(json.dumps(fallback, indent=2))
        except Exception:
            pass
        print(f"autopsy: FAILED ({e})", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
