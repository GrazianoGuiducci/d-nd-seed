#!/usr/bin/env python3
"""
diagram_generator.py — Conceptual Diagram Generator

Reads article content and generates an interactive diagram specification.
The diagram captures the logical structure: key concepts, relations,
directions, and contextual copy for each node.

The output spec is compatible with any SVG/React renderer that understands:
- entities: [{id, label, color, context, link, group}]
- interactions: [{from, to, type, label}]

Two modes:
1. LLM mode (default): sends content to an LLM API for intelligent extraction
2. Structural mode (--structural): rule-based extraction from text patterns

Usage:
    # LLM mode (requires DIAGRAM_API_KEY + DIAGRAM_API_URL env vars)
    python diagram_generator.py --content article.md
    python diagram_generator.py --content article.md --lang en
    python diagram_generator.py --title "My Article" --content article.md --json

    # Structural mode (no LLM needed)
    python diagram_generator.py --content article.md --structural

    # From stdin
    cat article.md | python diagram_generator.py --stdin

As library:
    from diagram_generator import generate_diagram, generate_diagram_structural
    spec = generate_diagram(title, content, lang='it')        # LLM mode
    spec = generate_diagram_structural(title, content, lang='it')  # rule-based

No external dependencies. Pure Python.

Author: D-ND project
"""

import json
import re
import sys
import os
from pathlib import Path

# --- Neon color palette ---
NEON_COLORS = [
    '#c084fc',  # purple
    '#22d3ee',  # cyan
    '#4ade80',  # green
    '#fbbf24',  # amber
    '#f87171',  # red
    '#60a5fa',  # blue
    '#a78bfa',  # violet
    '#f472b6',  # pink
]

# --- System prompt for LLM ---
SYSTEM_PROMPT = """You are a conceptual diagram generator.

Given an article, extract its logical structure as an interactive diagram specification.

RULES:
- Extract 3-7 key concepts as nodes (not more — clarity over completeness)
- For each node: a short label (2-4 words), a context sentence that positions the observer, and optionally a link to a related page
- Identify directional relations between nodes: cause→effect, sequence, dependency, tension
- Choose appropriate colors from this neon palette: #c084fc (purple), #22d3ee (cyan), #4ade80 (green), #fbbf24 (amber), #f87171 (red), #60a5fa (blue), #a78bfa (violet), #f472b6 (pink)
- Context copy must be inclusive (we/our in English, noi/facciamo in Italian), never "you/tu"
- Context copy must position the observer BEFORE giving the content: when X happens → Y is what we see → Z is the result
- If concepts form a cycle, indicate it with the last interaction pointing back to the first
- If concepts have a container/group relationship, use the "group" field

OUTPUT: Valid JSON only, no markdown, no explanation. Schema:
{
  "type": "flow" or "network",
  "title": {"it": "...", "en": "..."},
  "entities": [
    {"id": "concept_id", "label": "Short Label", "color": "#hex", "context": {"it": "...", "en": "..."}, "link": "/optional-slug", "group": "optional_group_id"}
  ],
  "interactions": [
    {"from": "id1", "to": "id2", "type": "flow", "label": {"it": "...", "en": "..."}}
  ]
}"""


def generate_diagram(title: str, content: str, lang: str = 'it',
                     slug: str = '', api_key: str = '', api_url: str = '') -> dict:
    """
    Generate a diagram spec using an LLM API.

    Args:
        title: Article title
        content: Article content (text or HTML — the LLM handles both)
        lang: Primary language ('it' or 'en')
        slug: Optional page slug for self-reference
        api_key: LLM API key (falls back to DIAGRAM_API_KEY or GODEL_API_KEY env)
        api_url: LLM API URL (falls back to DIAGRAM_API_URL or GODEL_API_URL env)

    Returns:
        DiagramSpec dict with type, entities, interactions
    """
    key = api_key or os.environ.get('DIAGRAM_API_KEY') or os.environ.get('GODEL_API_KEY', '')
    url = api_url or os.environ.get('DIAGRAM_API_URL') or os.environ.get('GODEL_API_URL', '')

    if not key or not url:
        print('[diagram] No API key/URL — falling back to structural mode', file=sys.stderr)
        return generate_diagram_structural(title, content, lang)

    user_message = f"""Generate a conceptual diagram spec for this article.

Title: {title or 'Untitled'}
Language: {lang}
{f'Slug: {slug}' if slug else ''}

Article content:
{content[:4000]}"""

    import urllib.request
    import urllib.error

    # Detect API format from URL
    is_anthropic = 'anthropic.com' in url

    if is_anthropic:
        body = json.dumps({
            'model': os.environ.get('DIAGRAM_MODEL', 'claude-sonnet-4-20250514'),
            'max_tokens': 4096,
            'system': SYSTEM_PROMPT,
            'messages': [{'role': 'user', 'content': user_message}],
        }).encode()
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': key,
            'anthropic-version': '2023-06-01',
        }
    else:
        # OpenAI-compatible
        body = json.dumps({
            'model': os.environ.get('DIAGRAM_MODEL', 'anthropic/claude-sonnet-4-20250514'),
            'messages': [
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': user_message},
            ],
            'max_tokens': 4096,
        }).encode()
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}',
        }

    req = urllib.request.Request(url, data=body, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f'API error {e.code}: {e.read().decode()[:200]}')

    # Extract reply
    if is_anthropic:
        reply = ''.join(b.get('text', '') for b in data.get('content', []))
    else:
        reply = data.get('choices', [{}])[0].get('message', {}).get('content', '')

    # Parse JSON from reply
    try:
        spec = json.loads(reply)
    except json.JSONDecodeError:
        match = re.search(r'\{[\s\S]*\}', reply)
        if match:
            spec = json.loads(match.group())
        else:
            raise RuntimeError(f'LLM did not return valid JSON: {reply[:200]}')

    _validate_spec(spec)
    return spec


def generate_diagram_structural(title: str, content: str, lang: str = 'it') -> dict:
    """
    Generate a diagram spec using rule-based text analysis.
    No LLM needed — works offline. Less intelligent but always available.

    Extracts: section headers as nodes, sequential flow, keyword-based relations.
    """
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()

    # Extract section headers (## or ### in markdown, or <h2>/<h3> patterns)
    headers = re.findall(r'(?:^|\n)\s*#{2,3}\s+(.+?)(?:\n|$)', content)
    if not headers:
        # Try HTML headers
        headers = re.findall(r'<h[23][^>]*>([^<]+)</h[23]>', content)
    if not headers:
        # Fall back to sentence-initial bold patterns
        headers = re.findall(r'\*\*([^*]{3,40})\*\*', content)

    # Limit to 3-7 concepts
    concepts = headers[:7] if headers else _extract_key_sentences(text)[:5]

    if len(concepts) < 2:
        return {'type': 'flow', 'entities': [], 'interactions': []}

    entities = []
    for i, label in enumerate(concepts):
        label_clean = label.strip()[:40]
        # Extract a context sentence — the sentence following the header
        ctx = _find_context_after(text, label_clean)
        entities.append({
            'id': f'n{i}',
            'label': label_clean,
            'color': NEON_COLORS[i % len(NEON_COLORS)],
            'context': {lang: ctx} if ctx else None,
        })

    # Sequential interactions
    interactions = []
    for i in range(len(entities) - 1):
        interactions.append({
            'from': f'n{i}',
            'to': f'n{i+1}',
            'type': 'flow',
        })

    # Check for cycle indicators
    cycle_words = ['ciclo', 'cycle', 'ricomincia', 'restarts', 'ritorna', 'returns', 'loop']
    if any(w in text.lower() for w in cycle_words):
        interactions.append({
            'from': f'n{len(entities)-1}',
            'to': 'n0',
            'type': 'flow',
            'label': {lang: 'il ciclo ricomincia' if lang == 'it' else 'the cycle restarts'},
        })

    return {
        'type': 'flow',
        'title': {'it': title, 'en': title} if title else None,
        'entities': entities,
        'interactions': interactions,
    }


def _extract_key_sentences(text: str, n: int = 5) -> list:
    """Extract the first N significant sentences as fallback concepts."""
    sentences = re.split(r'[.!?]\s+', text)
    result = []
    for s in sentences:
        s = s.strip()
        if len(s) > 20 and len(s) < 80:
            result.append(s)
            if len(result) >= n:
                break
    return result


def _find_context_after(text: str, label: str) -> str:
    """Find the first sentence after a label mention in the text."""
    idx = text.lower().find(label.lower()[:20])
    if idx < 0:
        return ''
    # Find the next sentence after the label
    after = text[idx + len(label):]
    # Skip punctuation and whitespace
    after = re.sub(r'^[\s:.\-—]+', '', after)
    # Take first sentence
    match = re.match(r'([^.!?]{10,150}[.!?])', after)
    return match.group(1).strip() if match else after[:120].strip()


def _validate_spec(spec: dict):
    """Validate minimal DiagramSpec structure."""
    if not isinstance(spec.get('entities'), list) or len(spec['entities']) == 0:
        raise ValueError('Invalid spec: no entities')
    for e in spec['entities']:
        if 'id' not in e or 'label' not in e:
            raise ValueError(f'Entity missing id or label: {e}')


# --- CLI ---

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate conceptual diagram from article content')
    parser.add_argument('--content', type=str, help='Path to article file (text, markdown, or HTML)')
    parser.add_argument('--stdin', action='store_true', help='Read content from stdin')
    parser.add_argument('--title', type=str, default='', help='Article title')
    parser.add_argument('--lang', type=str, default='it', help='Language (it/en)')
    parser.add_argument('--slug', type=str, default='', help='Page slug')
    parser.add_argument('--structural', action='store_true', help='Use rule-based extraction (no LLM)')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    args = parser.parse_args()

    if args.stdin:
        content = sys.stdin.read()
    elif args.content:
        content = Path(args.content).read_text(encoding='utf-8')
    else:
        parser.error('Provide --content <file> or --stdin')

    if args.structural:
        spec = generate_diagram_structural(args.title, content, args.lang)
    else:
        spec = generate_diagram(args.title, content, args.lang, args.slug)

    if args.json:
        print(json.dumps(spec, ensure_ascii=False, indent=2))
    else:
        # Pretty print
        entities = spec.get('entities', [])
        interactions = spec.get('interactions', [])
        print(f'--- DIAGRAM ({spec.get("type", "flow")}) ---')
        print(f'  {len(entities)} nodes, {len(interactions)} relations')
        print()
        for e in entities:
            ctx = ''
            if e.get('context'):
                c = e['context']
                ctx = c.get(args.lang, c.get('it', c.get('en', ''))) if isinstance(c, dict) else c
                ctx = f' — {ctx[:60]}...' if len(ctx) > 60 else f' — {ctx}'
            print(f'  [{e.get("color", "?")}] {e["label"]}{ctx}')
        print()
        for inter in interactions:
            label = ''
            if inter.get('label'):
                lb = inter['label']
                label = f' ({lb.get(args.lang, lb) if isinstance(lb, dict) else lb})'
            print(f'  {inter["from"]} → {inter["to"]}{label}')


if __name__ == '__main__':
    main()
