---
name: dream
description: "Memory consolidation — clean, merge, prune stale memories. Use when memory files exceed 50 or stale files exceed 15."
user-invocable: true
---

# Dream — Memory Consolidation

Periodically the system cleans its own memory:

1. Scan all .md files in the memory directory
2. Identify stale files (>14 days without update)
3. Classify: SUPERSEDED (absorbed elsewhere, delete), IMMUTABLE (keep), NEEDS UPDATE
4. Clean the MEMORY.md index — remove pointers to deleted files
5. Report what was done

Rules:
- Never touch files with direct operator words
- Never delete without checking if the content lives elsewhere
- Never prune learnings — they are the memory of errors

## Eval

## Trigger Tests
# "clean up memory" -> activates
# "my memory is getting big" -> activates
# "consolidate" -> activates
# "deploy" -> does NOT activate

## Fidelity Tests
# Given 60 memory files, 20 stale: prunes stale, reports count
# Given clean memory (<30 files, 0 stale): reports "nothing to do"
