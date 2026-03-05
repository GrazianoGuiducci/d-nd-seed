#!/usr/bin/env python3
"""
seed_cycle.py — Generic Seed-Driven Autonomous Decision Engine

Extracted from MM_D-ND tools (dnd_next.py + dipartimento.py) by TM3.
Generalized for any project that uses the D-ND seed pattern.

The cycle: load seed -> load sources -> analyze -> decide -> execute -> verify -> update seed

Usage:
    python seed_cycle.py                # show decision
    python seed_cycle.py --detail       # with source details
    python seed_cycle.py --execute      # decide AND act
    python seed_cycle.py --update       # update seed after
    python seed_cycle.py --json         # structured output

Configuration:
    Set PROJECT_DIR, DATA_DIR, and register your sources/assertions/executors
    before calling main(). See __main__ block for example.
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timedelta


# === CONFIGURATION (override before calling main) ===

PROJECT_DIR = Path(".")
DATA_DIR = Path("./data")

# Source loaders: name -> callable() returning dict
SOURCES = {}

# Assertions: list of {id, claim, test: callable() -> (bool, str), source, group}
ASSERTIONS = []

# Executors: decision_type -> callable(decision, analysis) -> dict
EXECUTORS = {}

# Artifact metadata: id -> {title, target, core_claim}
ARTIFACT_META = {}


# === SEED ===

def load_seed():
    """Load the project seed (tensions, direction, potential)."""
    path = DATA_DIR / "seed.json"
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)


def save_seed(seed):
    """Persist the seed."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "seed.json"
    with open(path, "w") as f:
        json.dump(seed, f, indent=2, ensure_ascii=False, default=str)
    return path


# === GENERIC SOURCE LOADERS ===

def load_recent_commits(repo_dir=None, days=7, max_count=20):
    """Recent commits from a git repo."""
    cwd = str(repo_dir or PROJECT_DIR)
    try:
        since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        result = subprocess.run(
            ["git", "log", f"--since={since}", f"-{max_count}",
             "--format=%H|%s|%ai", "--no-merges"],
            capture_output=True, text=True, cwd=cwd
        )
        commits = []
        for line in result.stdout.strip().split("\n"):
            if "|" in line:
                hash_, msg, date = line.split("|", 2)
                commits.append({"hash": hash_[:8], "msg": msg.strip(), "date": date.strip()})
        return commits
    except Exception:
        return []


def load_recent_data(data_dir=None, hours=48):
    """Data files modified within the last N hours."""
    ddir = data_dir or DATA_DIR
    results = []
    cutoff = datetime.now().timestamp() - hours * 3600
    if not ddir.exists():
        return results
    for path in ddir.glob("*.json"):
        if path.stat().st_mtime > cutoff:
            results.append({
                "file": path.stem,
                "size_kb": round(path.stat().st_size / 1024, 1),
                "modified": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
            })
    return sorted(results, key=lambda x: x["modified"], reverse=True)


# === ASSERTION VERIFICATION ===

def verify_assertions(assertions=None):
    """
    Run all registered assertions. Each must have:
      id, claim, test (callable -> (bool, detail_str)), source, group (optional)

    Returns list of {id, claim, status: PASS|FAIL|SKIP, detail, group}
    """
    assertions = assertions or ASSERTIONS
    results = []
    for ass in assertions:
        try:
            passed, detail = ass["test"]()
            status = "PASS" if passed else "FAIL"
        except Exception as e:
            status = "SKIP"
            detail = str(e)
        results.append({
            "id": ass["id"],
            "claim": ass["claim"],
            "status": status,
            "detail": detail,
            "group": ass.get("group"),
        })
    return results


# === ANALYSIS ===

def analyze_from_seed(seed):
    """Analyze research/project state from the seed."""
    if not seed:
        return {"status": "unknown", "direction": "No seed. Run verification first.",
                "urgency": 0, "hot_discoveries": [], "open_tensions": []}

    tensions = seed.get("tensioni", [])
    blocked = seed.get("potenziale_bloccato", [])
    variance = seed.get("varianza", [])
    verifica = seed.get("verifica", {})

    stallo = any("stallo" in str(v).lower() for v in variance)
    contradictions = [t for t in tensions if t.get("tipo") == "contraddizione"]
    hot = [t for t in tensions
           if t.get("tipo") in ("scoperta_confermata", "scoperta")
           and t.get("intensita", 0) >= 0.8]
    open_t = [t for t in tensions
              if t.get("tipo") == "tensione_aperta"
              and t.get("intensita", 0) >= 0.5]

    total = verifica.get("total", 1) or 1
    pass_rate = verifica.get("pass", 0) / total

    urgency = 0
    if contradictions: urgency += 0.4
    if stallo: urgency += 0.3
    if pass_rate < 0.7: urgency += 0.2
    if len(blocked) >= 3: urgency += 0.1
    if hot: urgency += 0.15

    return {
        "status": "stallo" if stallo else "active",
        "direction": seed.get("direzione", "?"),
        "piano": seed.get("piano", 0),
        "contradictions": len(contradictions),
        "blocked": len(blocked),
        "pass_rate": pass_rate,
        "urgency": min(urgency, 1.0),
        "hot_discoveries": hot,
        "open_tensions": open_t,
    }


def analyze_activity(commits, recent_data, area_keywords=None):
    """Analyze recent activity from commits and data."""
    area_keywords = area_keywords or {
        "artifact": ["paper", "page", "doc"],
        "tool": ["tool", "script", "fix", "feat"],
        "data": ["data", "result", "report"],
    }
    areas = {k: 0 for k in area_keywords}
    areas["other"] = 0

    for c in commits:
        msg = c["msg"].lower()
        matched = False
        for area, keywords in area_keywords.items():
            if any(w in msg for w in keywords):
                areas[area] += 1
                matched = True
                break
        if not matched:
            areas["other"] += 1

    return {
        "commits_7d": len(commits),
        "areas": areas,
        "fresh_data": [r for r in recent_data if r["size_kb"] > 1][:5],
        "momentum": "high" if len(commits) > 10 else "medium" if len(commits) > 3 else "low",
    }


# === DECISORE ===

def decide(analysis, activity, extra_reasons=None):
    """
    The decision. Not a list -- ONE thing to do.

    Priority stack:
    1. Contradiction (0.9+)
    2. Crystallize hot discovery (0.88)
    3. Integrate fresh results (0.75)
    4. Explore open tension (0.65)
    5. Unblock potential (0.5)
    6. Pivot from stasis (0.45)
    7. Publish (0.35)
    """
    reasons = []

    # 1. Contradictions
    if analysis["contradictions"] > 0:
        reasons.append({
            "action": f"RESEARCH: {analysis['direction']}",
            "why": f"Open contradiction (N={analysis['contradictions']}). Inconsistent until resolved.",
            "priority": 0.9 + 0.1 * analysis["contradictions"],
            "type": "research",
        })

    # 2. Hot discoveries
    for disc in analysis.get("hot_discoveries", []):
        intensity = disc.get("intensita", 0)
        reasons.append({
            "action": f"CRYSTALLIZE: {disc.get('id', '?')} -- {disc.get('claim', '?')[:60]}",
            "why": f"Confirmed discovery ({intensity:.0%}) not yet integrated.",
            "priority": 0.88 * intensity,
            "type": "crystallize",
        })

    # 3. Fresh results not integrated
    tool_commits = activity.get("areas", {}).get("tool", 0)
    artifact_commits = activity.get("areas", {}).get("artifact", 0)
    if activity.get("fresh_data") and tool_commits > artifact_commits:
        reasons.append({
            "action": "INTEGRATE: Fresh results into relevant artifacts",
            "why": f"Tool commits ({tool_commits}) > artifact commits ({artifact_commits}). Results accumulating.",
            "priority": 0.75,
            "type": "integrate",
        })

    # 4. Open tensions
    for tens in analysis.get("open_tensions", []):
        intensity = tens.get("intensita", 0)
        reasons.append({
            "action": f"EXPLORE: {tens.get('id', '?')} -- {tens.get('claim', '?')[:60]}",
            "why": f"Open tension at {intensity:.0%}. Uncrystallized potential.",
            "priority": 0.65 * intensity,
            "type": "explore",
        })

    # 5. Blocked potential
    if analysis["blocked"] > 0:
        reasons.append({
            "action": f"UNBLOCK: {analysis['blocked']} items waiting for prerequisites",
            "why": "Blocked potential = energy that can't flow.",
            "priority": 0.5,
            "type": "unblock",
        })

    # 6. Stasis
    if analysis["status"] == "stallo":
        reasons.append({
            "action": "PIVOT: Same tensions as last cycle. Change angle.",
            "why": "Stasis detected. Repetition won't break through.",
            "priority": 0.45,
            "type": "pivot",
        })

    # Extra reasons from project-specific logic
    if extra_reasons:
        reasons.extend(extra_reasons)

    reasons.sort(key=lambda x: x["priority"], reverse=True)

    if not reasons:
        return {
            "decision": "EXPLORE: No urgent action. Look for new questions.",
            "why": "System in good shape. Time to think, not to do.",
            "alternatives": [],
            "confidence": 0.5,
        }

    return {
        "decision": reasons[0]["action"],
        "why": reasons[0]["why"],
        "priority": reasons[0]["priority"],
        "type": reasons[0]["type"],
        "alternatives": reasons[1:4],
        "confidence": min(reasons[0]["priority"], 0.95),
    }


# === EXECUTOR ===

def execute_decision(decision, analysis, seed):
    """
    Execute the decision, respecting autonomy levels.
    Dispatches to registered EXECUTORS by decision type.
    """
    dtype = decision.get("type", "")
    action = decision.get("decision", "")
    result = {"type": dtype, "action": action, "executed": False, "outcome": None}

    executor = EXECUTORS.get(dtype)
    if executor:
        try:
            result = executor(decision, analysis)
            result.setdefault("executed", True)
        except Exception as e:
            result["outcome"] = f"error: {e}"
    else:
        result["outcome"] = f"no_executor_for_{dtype}"

    # Verify: did the seed advance?
    seed_after = load_seed()
    if seed_after and seed:
        if seed_after.get("piano", 0) > seed.get("piano", 0):
            result["piano_advanced"] = True

    return result


# === SEED CRYSTALLIZATION ===

def crystallize_seed(verification_results, previous_seed=None):
    """
    From verification results, produce a NEW seed.

    A seed is not a report (what happened).
    A seed is a direction (where the potential points).
    """
    tensioni = []
    potenziale = []

    # FAIL = contradiction
    for r in verification_results:
        if r["status"] == "FAIL":
            tensioni.append({
                "tipo": "contraddizione",
                "id": r["id"],
                "claim": r["claim"],
                "dettaglio": r.get("detail", ""),
                "intensita": 1.0,
                "nota": "Theory and data diverge."
            })

    # SKIP = blocked potential
    for r in verification_results:
        if r["status"] == "SKIP":
            potenziale.append({
                "tipo": "bloccato",
                "id": r["id"],
                "claim": r["claim"],
                "dettaglio": r.get("detail", ""),
                "nota": "Potential exists but can't flow -- missing prerequisite."
            })

    # All PASS = suspicious symmetry
    n_pass = sum(1 for r in verification_results if r["status"] == "PASS")
    n_total = len(verification_results)
    if n_pass == n_total and n_total > 5:
        tensioni.append({
            "tipo": "simmetria_sospetta",
            "id": "META",
            "claim": f"All {n_total} tests pass. Are we only testing tautologies?",
            "intensita": 0.5,
            "nota": "Perfect symmetry is suspicious. Add tests that CAN fail."
        })

    # Variance from previous cycle
    varianza = []
    if previous_seed:
        prev_ids = {t["id"] for t in previous_seed.get("tensioni", [])}
        curr_ids = {t["id"] for t in tensioni}
        new = curr_ids - prev_ids
        resolved = prev_ids - curr_ids
        if new: varianza.append(f"New tensions: {new}")
        if resolved: varianza.append(f"Resolved: {resolved}")
        if not new and not resolved:
            varianza.append("Same tensions as last cycle -- possible stasis")

    # Direction from tensions
    direction = _direction_from_tensions(tensioni, potenziale)

    seed = {
        "timestamp": datetime.now().isoformat(),
        "piano": (previous_seed.get("piano", 0) + 1) if previous_seed else 1,
        "tensioni": sorted(tensioni, key=lambda t: t.get("intensita", 0), reverse=True),
        "potenziale_bloccato": potenziale,
        "varianza": varianza,
        "direzione": direction,
        "verifica": {
            "pass": n_pass,
            "fail": sum(1 for r in verification_results if r["status"] == "FAIL"),
            "skip": sum(1 for r in verification_results if r["status"] == "SKIP"),
            "total": n_total,
        }
    }

    save_seed(seed)
    return seed


def _direction_from_tensions(tensioni, potenziale):
    """Extract direction from the highest-potential tension."""
    if not tensioni and not potenziale:
        return "No tensions, no blocked potential -- seek new questions"

    for t in tensioni:
        if t["tipo"] == "contraddizione":
            return f"Resolve contradiction {t['id']}: {t['claim'][:50]}"
    if potenziale:
        return f"Unblock {potenziale[0]['id']}: {potenziale[0].get('dettaglio', '')[:50]}"
    for t in tensioni:
        if t["tipo"] == "simmetria_sospetta":
            return "Add tests that can FAIL -- perfect symmetry is suspicious"

    return "Continue the spiral"


# === OUTPUT ===

def format_decision(decision, analysis, activity, detail=False):
    """Human-readable decision output."""
    lines = []
    lines.append(f"\n{'='*60}")
    lines.append(f"  SEED CYCLE -- {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"{'='*60}")
    lines.append(f"\n  DECISION: {decision['decision']}")
    lines.append(f"  WHY: {decision['why']}")
    lines.append(f"  CONFIDENCE: {decision.get('confidence', 0):.0%}")

    if decision.get("alternatives"):
        lines.append(f"\n  Alternatives:")
        for i, alt in enumerate(decision["alternatives"], 1):
            lines.append(f"    {i}. {alt['action']}")

    if detail:
        lines.append(f"\n{'_'*60}")
        lines.append(f"  STATE (Piano {analysis.get('piano', '?')})")
        lines.append(f"    Status: {analysis['status']} | Pass rate: {analysis['pass_rate']:.0%}")
        lines.append(f"    Contradictions: {analysis['contradictions']} | Blocked: {analysis['blocked']}")
        lines.append(f"    Direction: {analysis['direction']}")
        lines.append(f"\n  ACTIVITY (7d)")
        lines.append(f"    Commits: {activity['commits_7d']} | Momentum: {activity['momentum']}")

    lines.append(f"\n{'='*60}\n")
    return "\n".join(lines)


def save_execution_report(decision, exec_result, analysis):
    """Save execution report to data/reports/."""
    reports_dir = DATA_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    report = {
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "execution": exec_result,
        "piano": analysis.get("piano", 0),
    }
    path = reports_dir / f"cycle_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
    with open(path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)
    return path


# === MAIN ===

def run_cycle(execute=False, update=False, detail=False, as_json=False):
    """
    Run the full cycle. Call this after configuring PROJECT_DIR, DATA_DIR,
    SOURCES, ASSERTIONS, and EXECUTORS.
    """
    # Load seed
    seed = load_seed()

    # Load sources
    commits = load_recent_commits()
    recent_data = load_recent_data()

    # Run any registered source loaders
    extra_state = {}
    for name, loader in SOURCES.items():
        try:
            extra_state[name] = loader()
        except Exception as e:
            extra_state[name] = {"error": str(e)}

    # Verify assertions if any are registered
    verification = verify_assertions() if ASSERTIONS else []

    # If we have new verification results and want to update seed
    if verification and update:
        seed = crystallize_seed(verification, seed)

    # Analyze
    analysis = analyze_from_seed(seed)
    activity = analyze_activity(commits, recent_data)

    # Decide
    decision = decide(analysis, activity)

    # Output
    if as_json and not execute:
        output = {"decision": decision, "analysis": analysis, "activity": activity}
        if verification:
            output["verification"] = verification
        print(json.dumps(output, indent=2, ensure_ascii=False, default=str))
        return decision

    if not execute:
        print(format_decision(decision, analysis, activity, detail=detail))
        return decision

    # Execute
    print(format_decision(decision, analysis, activity, detail=False))
    exec_result = execute_decision(decision, analysis, seed)
    save_execution_report(decision, exec_result, analysis)

    # Update seed after execution if requested
    if update and not verification:
        # Re-run verification after execution to capture changes
        post_verification = verify_assertions() if ASSERTIONS else []
        if post_verification:
            crystallize_seed(post_verification, seed)

    return decision


# === CLI ===

if __name__ == "__main__":
    # Example: standalone usage with no project-specific config
    # For real use, import this module and configure before calling run_cycle()

    detail = "--detail" in sys.argv
    as_json = "--json" in sys.argv
    do_update = "--update" in sys.argv
    do_execute = "--execute" in sys.argv

    run_cycle(execute=do_execute, update=do_update, detail=detail, as_json=as_json)
