# Event-Driven Refresh

> Regenerate derived artifacts **when source material actually changes**, not on a fixed timer.

## The problem with blind cron

A common pattern: a cron job runs every N hours, regenerates a derived file (cache, summary, index, snapshot), writes it, moves on.

This looks efficient. It isn't:

- **Wasted work** — if the source hasn't changed, the regeneration produces an identical file. The filesystem timestamp changes, but the content doesn't.
- **False freshness signals** — downstream consumers see a recent `mtime` and assume the file reflects recent source state. It doesn't.
- **Delayed propagation** — if source changes twice between runs, the intermediate state is invisible. If source changes right after a run, consumers wait the full interval to see it.
- **Cosmetic refresh** — the system looks alive because files keep rotating, but nothing is actually learning or evolving.

## The principle

A refresh should be triggered by **signals that source material has changed enough to matter**, not by the clock.

A detector sits between source and derived artifact. Every interval (or on explicit trigger), it checks a small set of signals. If any threshold is crossed, regeneration fires. If not, the existing artifact is left alone and the system reports "no material change since last refresh".

## Structure

```
source material ─┐
                 ├──> detector ─> threshold reached? ──> regenerate derived artifact
state file ──────┘                └─> no change        ──> skip
```

Three components:

1. **Signals** — measurable deltas in source material. Each signal compares current state to recorded state from the last successful refresh.
2. **State file** — small JSON that records, per signal, the reference value at the last refresh. Persisted to disk so the detector survives process restart.
3. **Thresholds** — per-signal values. A single signal crossing its threshold is enough to trigger. Multiple weak signals may also aggregate, depending on design.

## Example signals

Generic patterns that apply across domains:

| Signal | Example threshold | Triggers when |
|--------|-------------------|---------------|
| New items count | `delta >= 1` | Any new item was added since last refresh |
| Mutation count | `delta >= N` | Enough items were modified to shift the overall picture |
| Distinct-event count | `>= 1` | A specific rare event occurred at all |
| Staleness age | `>= 14 days` | Even without signals, the artifact is too old to trust |

The last signal — pure staleness — is the safety net. It ensures the artifact never ages indefinitely even if the primary signals are quiet.

## The state file

```json
{
  "last_refresh": "2026-01-15T03:30:00Z",
  "reference_values": {
    "items_count": 142,
    "mutations_count": 17,
    "distinct_events": 0
  }
}
```

The detector reads this, computes current values from source, compares, decides. On successful refresh, it updates reference values to current.

## CLI contract

A refresh detector should support at least:

- **default** — check signals, refresh if threshold reached, update state
- **`--dry`** — check signals, print what would happen, do not refresh
- **`--force`** — refresh unconditionally, update state

The dry mode is useful for observability: the operator or another agent can query "what does the detector see right now?" without committing to a refresh.

## When to use this pattern

Use event-driven refresh when:

- The derived artifact is expensive to regenerate
- Source changes are bursty (long quiet periods, then sudden activity)
- Downstream consumers rely on the artifact being meaningful, not just recent
- You want observability into whether the system is still evolving

Do **not** use it when:

- Regeneration is cheap and source is a firehose (regenerate every time)
- The artifact must be refreshed on a fixed schedule for external reasons (compliance, reporting)

## Why this matters

A system that only refreshes when source changes has a visible heartbeat: if the detector never fires, you know the source is quiet. A system on blind cron is always "fresh" — which means the word has lost meaning. You can't tell alive from dead.

Event-driven refresh is the difference between a clock that ticks and a system that breathes.
