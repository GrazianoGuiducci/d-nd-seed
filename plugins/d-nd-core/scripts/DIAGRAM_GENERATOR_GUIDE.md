# Conceptual Diagram Generator — Complete Guide

## What it does

The diagram generator reads article content and produces an interactive diagram specification. The diagram captures the logical structure: key concepts as nodes, relations as arrows, and contextual copy for each node that positions the observer.

The output is a JSON spec that any renderer can consume — SVG, React, HTML canvas, or static image generators.

**Principle**: the diagram contains the article. The visitor sees the structure first (how things connect), then the content (the full narrative). Understanding starts from form, not from text.

---

## Quick start

```bash
# LLM mode (needs API key)
export GODEL_API_KEY=your-key
export GODEL_API_URL=https://api.your-provider.com/v1/chat/completions
python diagram_generator.py --content article.md

# Structural mode (no LLM, works offline)
python diagram_generator.py --content article.md --structural

# JSON output
python diagram_generator.py --content article.md --json

# From stdin
cat article.md | python diagram_generator.py --stdin --title "My Article"
```

No dependencies. Pure Python. Works anywhere.

---

## The spec format

```json
{
  "type": "flow",
  "title": {"it": "Titolo", "en": "Title"},
  "entities": [
    {
      "id": "concept_id",
      "label": "Short Label",
      "color": "#c084fc",
      "context": {
        "it": "Quando X accade, Y è ciò che vediamo. Il risultato è Z.",
        "en": "When X happens, Y is what we see. The result is Z."
      },
      "link": "/optional-page-slug",
      "group": "optional_container_id"
    }
  ],
  "interactions": [
    {
      "from": "concept_1",
      "to": "concept_2",
      "type": "flow",
      "label": {"it": "causa", "en": "causes"}
    }
  ]
}
```

### Entity fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier |
| `label` | Yes | Short display label (2-4 words) |
| `color` | No | Hex color from neon palette (auto-assigned if missing) |
| `context` | No | Observer-positioning copy: when/where → content → result. Bilingual {it, en} |
| `link` | No | Deep link URL to a related page |
| `group` | No | Container group ID — entities with the same group are visually contained |

### Interaction fields

| Field | Required | Description |
|-------|----------|-------------|
| `from` | Yes | Source entity ID |
| `to` | Yes | Target entity ID |
| `type` | Yes | `flow` (sequence), `converge`, `oppose`, `transform`, `connect` |
| `label` | No | Relation description. Bilingual {it, en} |

### Diagram types

| Type | When to use | Layout |
|------|------------|--------|
| `flow` | Sequential or cyclic processes | Horizontal left-to-right |
| `network` | Non-linear relationships, many cross-connections | Grid/force layout |

---

## Two modes

### LLM mode (default)

Sends the article content to an LLM with a system prompt that enforces:
- 3-7 nodes (clarity over completeness)
- Inclusive copy (we/our, noi/facciamo — never you/tu)
- Observer positioning (when → content → result)
- Directional relations (cause→effect, sequence, dependency)
- Neon color palette
- Cycle detection (last node → first if the content describes a cycle)
- Group detection (container relationships)

**When to use**: always, if you have an LLM API. Produces the best results because it understands the narrative structure.

**Configuration**:
```bash
# Primary
export DIAGRAM_API_KEY=your-key
export DIAGRAM_API_URL=https://api.provider.com/v1/chat/completions

# Or reuse Godel env vars
export GODEL_API_KEY=your-key
export GODEL_API_URL=https://api.provider.com/v1/chat/completions

# Optional: model override
export DIAGRAM_MODEL=claude-sonnet-4-20250514
```

Supports both Anthropic and OpenAI-compatible API formats (auto-detected from URL).

### Structural mode (--structural)

Rule-based extraction from text patterns. No LLM needed. Works offline.

Extracts:
- Section headers (##, ###, `<h2>`, `<h3>`) as nodes
- Sequential flow between sections
- Context sentences from the text following each header
- Cycle indicators from keywords (ciclo, cycle, ricomincia, loop)

**When to use**: when no LLM API is available, or for quick local generation. Less intelligent — captures structure but not meaning.

---

## Usage as library

```python
from diagram_generator import generate_diagram, generate_diagram_structural

# LLM mode
spec = generate_diagram(
    title='The Cognitive Sieve',
    content='When a tension does not resolve...',
    lang='it',
    slug='cec',
)

# Structural mode
spec = generate_diagram_structural(
    title='The Cognitive Sieve',
    content='## Conditions\nObserve without judgment...',
    lang='it',
)

# Use the spec
for entity in spec['entities']:
    print(f"{entity['label']}: {entity.get('context', {}).get('it', '')}")
```

---

## Integration patterns

### Pattern 1: CLI tool

Generate diagram specs from the command line. Save as JSON, review, edit, then use.

```bash
python diagram_generator.py --content my-article.md --json > diagram_spec.json
# Review and edit the spec if needed
# Then pass to your renderer
```

### Pattern 2: Build-time generation

Run the generator when content is created or updated. Save the spec alongside the content.

```python
from diagram_generator import generate_diagram
import json

# In your CMS pipeline
article = load_article('my-slug')
spec = generate_diagram(article['title'], article['content'], 'it')
article['visual_spec'] = spec
save_article(article)
```

### Pattern 3: API endpoint

Expose as a REST endpoint for admin tools.

```javascript
// Express.js example
app.post('/api/pages/diagram', auth, async (req, res) => {
    const { title, content, lang } = req.body;
    // Call the Python script or port the logic to JS
    const spec = await generateDiagram(title, content, lang);
    res.json({ success: true, spec });
});
```

### Pattern 4: Admin UI toggle

Add a "Generate Diagram" button in the content editor. When clicked, send the article content to the generator, display the result, let the editor review/edit, then save.

```
[Article Editor]
  ├── Toggle: Auto-generate diagram ☐
  ├── Button: Generate Diagram AI 🔄
  │     └── POST /api/pages/diagram
  │     └── Display preview
  │     └── Save as visual_spec
  └── Article content
```

---

## The neon color palette

| Color | Hex | Suggested use |
|-------|-----|---------------|
| Purple | `#c084fc` | Entry points, origins, tensions |
| Cyan | `#22d3ee` | Active elements, projections, live data |
| Green | `#4ade80` | Results, outputs, what survives |
| Amber | `#fbbf24` | Expansion, exploration, questions |
| Red | `#f87171` | Inversions, risks, contradictions |
| Blue | `#60a5fa` | Seeds, persistence, memory |
| Violet | `#a78bfa` | Structure, invariants, foundations |
| Pink | `#f472b6` | Connections, bridges, relations |

---

## Copy rules for diagram nodes

Each node's `context` follows the observer-positioning principle:

1. **Position the observer**: when does this matter? In what situation?
2. **The content**: what happens here, what this does
3. **The result**: what comes out, what changes

**Good**: "When a tension does not resolve, the sieve filters through six phases. Only what survives becomes material for deciding."

**Bad**: "The sieve is a six-phase filtering tool." (describes the tool, doesn't position the observer)

**Inclusive language**: always "we/our" (English) or "noi/facciamo" (Italian). The visitor is on the same boat — not being told what to do.

---

## Iterating on diagrams

The first generation is a starting point, not the final version.

1. **Generate** → review the spec
2. **Edit** → adjust labels, relations, context copy
3. **Test** → does a visitor who knows nothing understand the structure?
4. **Refine** → remove nodes that don't carry weight, add missing relations

A diagram with 4 clear nodes is better than one with 7 cluttered nodes.

---

## Related tools

| Tool | Relationship |
|------|-------------|
| Scenario Projector | Projector analyzes tensions structurally. Diagram generator visualizes any article. |
| Domandatore | Generates 5 angles on a tension. Diagram generator captures existing article structure. |
| CEC | The sieve processes tensions. Diagram generator shows how the sieve works visually. |
| UniversalDiagram (renderer) | The diagram generator produces the spec. UniversalDiagram renders it. |
