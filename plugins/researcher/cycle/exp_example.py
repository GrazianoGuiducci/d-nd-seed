#!/usr/bin/env python3
"""
exp_example.py — Template experiment.

A self-contained experiment the nightly agent can run. Copy this file to
`exp_{your_name}.py`, adapt to your domain, and let the agent pick it up.

Convention:
- Self-contained: no setup step outside this file
- Budget: runs in 5-15 minutes max (nightly cycle has ~20 min total;
  the agent spends part of it reading, thinking, writing the report)
- Output: `data/exp_{name}.json` with raw results
- Null baseline: every claim is compared against shuffle, random, or noise.
  "Interesting" without null = artifact.
- No network, no external API, no live data — everything in repo

The agent can write new exp_*.py files when a tension calls for one that
doesn't exist. They stay as reusable tools.
"""

import json
import os
import random
from pathlib import Path
from datetime import datetime

# === CONFIG ========================================================
EXPERIMENT_NAME = "example"
DATA_ROOT = Path(os.environ.get("RESEARCHER_DATA_ROOT",
                                str(Path(__file__).parent.parent / "data")))
OUTPUT = DATA_ROOT / f"exp_{EXPERIMENT_NAME}.json"
# ===================================================================


def load_domain_data():
    """
    Replace this with how you load your domain data.
    Example: read a JSON / CSV / HDF5 / whatever.
    Must NOT hit the network — data lives in the repo.
    """
    # Placeholder: a synthetic sequence (replace with your actual data)
    return [random.gauss(0, 1) for _ in range(1000)]


def compute_observable(data):
    """
    Compute the quantity you claim is structural.
    Example: lag-1 autocorrelation, entropy, spectral slope, whatever.
    Return a number or a dict of numbers.
    """
    # Placeholder: mean and lag-1 correlation
    n = len(data)
    if n < 2:
        return {"mean": 0.0, "lag1": 0.0}
    mean = sum(data) / n
    centered = [x - mean for x in data]
    num = sum(centered[i] * centered[i + 1] for i in range(n - 1))
    den = sum(c * c for c in centered)
    lag1 = num / den if den > 0 else 0.0
    return {"mean": mean, "lag1": lag1}


def null_baseline(data, n_surrogates=20):
    """
    Compute the observable on surrogates (shuffle or random).
    The claim holds only if the observed value is outside the surrogate
    distribution. Otherwise it is artifact.
    """
    results = []
    for _ in range(n_surrogates):
        shuffled = data[:]
        random.shuffle(shuffled)
        results.append(compute_observable(shuffled))
    return results


def z_score(observed: float, surrogates: list[float]) -> float:
    n = len(surrogates)
    if n < 2:
        return 0.0
    mean = sum(surrogates) / n
    var = sum((s - mean) ** 2 for s in surrogates) / (n - 1)
    std = var ** 0.5
    return (observed - mean) / std if std > 0 else 0.0


def main():
    data = load_domain_data()

    observed = compute_observable(data)
    surrogates = null_baseline(data, n_surrogates=20)

    # Compute z-scores for each observable vs the surrogate distribution
    z_scores = {}
    for key in observed:
        surr_values = [s[key] for s in surrogates]
        z_scores[key] = z_score(observed[key], surr_values)

    result = {
        "experiment": EXPERIMENT_NAME,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "n_data": len(data),
        "n_surrogates": len(surrogates),
        "observed": observed,
        "surrogates_mean": {
            k: sum(s[k] for s in surrogates) / len(surrogates)
            for k in observed
        },
        "z_scores": z_scores,
        "verdict": (
            "Structural" if any(abs(z) > 3 for z in z_scores.values())
            else "Indistinguishable from null"
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    print(f"exp_{EXPERIMENT_NAME}: {result['verdict']}")
    for k, z in z_scores.items():
        print(f"  {k}: observed={observed[k]:.4f}, z={z:.2f}")
    print(f"→ {OUTPUT}")


if __name__ == "__main__":
    main()
