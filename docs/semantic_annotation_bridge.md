# Semantic Annotation Bridge

> When a system produces numerical or low-level findings and a higher-level semantic graph exists separately, a bridge makes the two coherent. One side stops being disconnected from the other.

## The problem

Many systems have two layers that evolve in parallel but don't talk to each other:

- A **measurement layer** that produces low-level findings: experiment results, metrics, deltas, observations, raw discoveries.
- A **semantic layer** that organizes concepts: entities, relationships, annotated graph, curated knowledge.

Without a bridge:

- The measurement layer accumulates results that nobody reads because they live in a separate store with a separate vocabulary.
- The semantic layer goes stale because curation takes effort and new findings don't surface there automatically.
- Downstream consumers (UI, API, other agents) see one layer or the other, never both. The picture is partial.

The measurement layer is generating real signal. The semantic layer is the organized map. They should feed each other — but typically they don't, because the vocabularies don't match.

## The principle

A **bridge** is a mapping + a synchronization process. It translates findings from measurement vocabulary into annotations on the semantic graph, so that what gets discovered numerically becomes visible semantically.

Structure:

```
measurement layer ─┐
                   ├──> [mapping] ──> [sync] ──> semantic layer (annotated)
findings store ────┘
```

Three components:

1. **Mapping file** — human-curated: for each measurement-layer concept, which semantic-layer entities does it touch? This is the vocabulary translation. Kept separate from the bridge code so it can be validated and updated independently.
2. **Bridge process** — reads findings, looks up the mapping, generates annotations on semantic graph nodes/edges. Idempotent: running twice produces the same result.
3. **Validator** (optional but recommended) — reads the mapping against the actual texts in the measurement layer, using a deterministic lexicon check. Flags mappings that disagree with what the texts say. System validates its own translation.

## Properties a good bridge has

- **Deduplication**: the same finding should not annotate the same semantic target twice. Dedup keys should be deterministic (e.g., `(date, source_id, target_id)`).
- **Capped accumulation**: annotations per target should be bounded. Old or less-mature annotations get evicted when the cap is reached. Without this, the semantic layer grows until it becomes noise.
- **Graceful degradation**: if mapping is missing for a finding, the bridge skips it with a trace, not a crash. Missing mapping is a signal to curate, not a failure.
- **Normalized keys**: if the semantic layer has pairs, triples, or ordered tuples, the bridge must canonicalize before lookup (e.g., always alphabetical order). Case-sensitivity bugs at this layer are silent and hard to detect.

## Where curation lives

The mapping file is curated, not derived. Someone (human or a dedicated agent) decides which measurement-layer concept maps to which semantic-layer entity. This is deliberate:

- Auto-derivation from text tends to produce plausible but wrong mappings. A term that appears in a paragraph is not necessarily the concept the paragraph is about.
- Curation is slow but correct. The bridge then becomes fast and trusted.
- When the operator is unsure, the validator can be run first: it reads source texts and suggests a mapping based on a lexicon. The operator accepts, rejects, or edits.

## Eviction with maturity

Not all findings deserve permanent presence on the semantic graph. Annotations can carry a **maturity** tag:

- **Established** — the finding has survived scrutiny. Never evicted.
- **Emerging** — the finding is recent, plausible, not yet validated. Evictable under cap pressure.
- **Candidate** — the finding is a hypothesis. Always evictable when something stronger arrives.

When the cap is reached, the bridge removes the lowest-maturity annotations first. This keeps the semantic layer growing in quality, not just quantity.

## Why this matters

Without a bridge, a system can be productive (the measurement layer keeps discovering) and organized (the semantic layer is well-curated) and still be incoherent: the two parts don't recognize each other. The discoveries never enter the map. The map never gains from the discoveries.

A bridge closes that loop. The map grows from what the system actually finds. The findings gain meaning from the map. Both evolve together.
