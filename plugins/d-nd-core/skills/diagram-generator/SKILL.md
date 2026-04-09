---
name: diagram-generator
description: "Generate conceptual diagrams from article content. Trigger when the operator says 'genera diagramma', 'diagram', 'visual spec', 'conceptual map', or when a page is created/updated and needs a structural visualization."
user-invocable: true
---

# Diagram Generator — From Content to Structure

When an article is created or updated, this skill generates a conceptual diagram
that captures the logical structure: key concepts, directional relations, and
contextual copy for each node.

## When to use

- A new article is published and needs a visual structure
- An existing article is updated and the diagram is stale
- The operator asks for a conceptual map of any content
- The admin panel "Generate Diagram AI" button is clicked

## How it works

1. Read the article content (title + body)
2. Extract 3-7 key concepts as nodes
3. Identify relations: cause→effect, sequence, dependency, tension
4. Generate contextual copy for each node (observer positioning: when → content → result)
5. Produce a DiagramSpec JSON compatible with the renderer

## Two modes

**LLM mode** (default): sends content to LLM API. Best results — understands narrative.
Requires: `GODEL_API_KEY` + `GODEL_API_URL` (or `DIAGRAM_API_KEY` + `DIAGRAM_API_URL`)

**Structural mode**: rule-based extraction from headers and text patterns. No API needed.
Use when: offline, quick generation, or API unavailable.

## CLI

```bash
# LLM mode
python diagram_generator.py --content article.md --json

# Structural mode
python diagram_generator.py --content article.md --structural --json

# From stdin
cat article.md | python diagram_generator.py --stdin --title "Article Title"
```

## As library

```python
from diagram_generator import generate_diagram, generate_diagram_structural

spec = generate_diagram('Title', 'Content...', lang='it')
# spec = {type, entities: [{id, label, color, context, link}], interactions: [{from, to, type}]}
```

## Copy rules for nodes

Every node's `context` field positions the observer:
- When/where this matters (situation)
- What happens (content)
- What comes out (result)

Inclusive language: "we/our" not "you/tu". The visitor is on the same boat.

## Iteration

The first generation is a draft. Review, edit labels and relations, test with a fresh eye.
4 clear nodes > 7 cluttered nodes.

## Complete guide

See `DIAGRAM_GENERATOR_GUIDE.md` in `plugins/d-nd-core/scripts/`.

$ARGUMENTS

## Eval

## Trigger Tests
# "genera diagramma per questo articolo" → activates
# "genera un diagramma concettuale" → activates
# "visual spec per la pagina" → activates
# "come funziona il deploy" → does NOT activate

## Fidelity Tests
# Given article with 5 sections → produces 5 entities + 4 flow interactions
# Given article with cycle keywords → last interaction points to first entity
# Given empty content → returns error or empty spec
# Context copy always inclusive (no "tu/you")
