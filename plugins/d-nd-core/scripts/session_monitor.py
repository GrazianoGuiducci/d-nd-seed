#!/usr/bin/env python3
"""
session_monitor.py — PreToolUse guard + periodic seed (D-ND Seed)

Gate strutturale su ogni tool call. Generico: funziona su qualsiasi nodo.
Configurazione via env vars: DND_PROJECT_DIR, DND_NODE_ID, DND_MESSAGING_URL, DND_MESSAGING_TOKEN.

Layer 1 (riflesso):
  1. QUESTION GUARD: domanda + Edit/Write → blocca
  2. BOOT GUARD: sessione fresca + azione senza allineamento → blocca
  3. MEMORY GUARD: scrittura memoria non richiesta → blocca

Layer 2 (appreso):
  4. CORRECTION PATTERNS: situazioni che hanno gia' prodotto errori → blocca

Periodic seed: every ~50 tool calls, writes checkpoint to messaging API (memo type)
+ local active_reasoning.md file.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# --- Configuration via environment ---
PROJECT_DIR = Path(os.environ.get('DND_PROJECT_DIR', os.getcwd()))
NODE_ID = os.environ.get('DND_NODE_ID', 'unknown')
MESSAGING_URL = os.environ.get('DND_MESSAGING_URL', '')
MESSAGING_TOKEN = os.environ.get('DND_MESSAGING_TOKEN', '')

HOOKS_DIR = PROJECT_DIR / '.claude' / 'hooks'
STATE_FILE = HOOKS_DIR / 'monitor_state.json'
CORRECTIONS_FILE = HOOKS_DIR / 'corrections.json'
REASONING_FILE = HOOKS_DIR / 'active_reasoning.md'
SEED_INTERVAL_CALLS = 50


def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {
        'session_start': datetime.now().isoformat(),
        'boot_files_read': [],
        'last_user_message': '',
        'last_user_is_question': False,
        'tool_calls': 0,
    }


def save_state(state):
    try:
        HOOKS_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass


def analyze_input(raw):
    try:
        data = json.loads(raw)
        return data.get('tool_name', ''), data.get('tool_input', {})
    except Exception:
        return '', {}


def is_question(text):
    text = text.strip()
    if not text:
        return False
    lower = text.lower()

    action_verbs = ['fix', 'fixa', 'sistema', 'correggi', 'aggiungi', 'crea',
                    'scrivi', 'modifica', 'cambia', 'deploy', 'committa',
                    'pusha', 'installa', 'build', 'testa', 'lancia', 'esegui',
                    'rimuovi', 'cancella', 'sposta', 'rinomina', 'refactora',
                    'implementa', 'procedi', 'fai', 'metti', 'togli']
    if any(v in lower for v in action_verbs):
        return False
    if text.endswith('?'):
        return True
    interrogativi = ['cosa ', 'come ', 'perche ', 'perché ', 'quando ', 'dove ',
                     'chi ', 'quale ', 'quanto ', 'sai ',
                     'what ', 'how ', 'why ', 'when ', 'where ', 'who ',
                     'which ', 'is it', 'are there']
    return any(lower.startswith(w) for w in interrogativi)


def check_question_guard(tool_name, tool_input, state):
    if not state.get('last_user_is_question', False):
        return None
    if tool_name in ('Edit', 'Write'):
        file_path = tool_input.get('file_path', '')
        return (f"QUESTION GUARD: L'ultimo messaggio e' una domanda. "
                f"Stai per modificare {file_path}. "
                f"Rispondi PRIMA alla domanda, poi chiedi se agire.")
    return None


def check_memory_guard(tool_name, tool_input, state):
    if tool_name not in ('Edit', 'Write'):
        return None
    file_path = tool_input.get('file_path', '')
    if '/memory/' not in file_path and 'MEMORY.md' not in file_path:
        return None
    last_msg = state.get('last_user_message', '').lower()
    memory_keywords = ['ricorda', 'salva', 'memoria', 'remember', 'save', 'memory',
                       'segna', 'annota', 'scrivi in memoria']
    if any(kw in last_msg for kw in memory_keywords):
        return None
    return (f"MEMORY GUARD: Stai scrivendo in memoria ({file_path}) "
            f"ma non e' stato chiesto. "
            f"La memoria si scrive solo su richiesta esplicita o dopo conferma.")


def check_boot_guard(tool_name, tool_input, state):
    tool_calls = state.get('tool_calls', 0)
    if tool_calls > 10:
        return None
    boot_files = state.get('boot_files_read', [])
    required = ['CLAUDE.md', 'MEMORY.md']
    if tool_name in ('Edit', 'Write', 'Bash'):
        missing = [f for f in required if not any(f in bf for bf in boot_files)]
        if missing:
            return (f"BOOT GUARD: Sessione fresca ({tool_calls} tool calls). "
                    f"File non letti: {', '.join(missing)}. "
                    f"Leggi prima di agire.")
    return None


def load_corrections():
    if CORRECTIONS_FILE.exists():
        try:
            with open(CORRECTIONS_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return []


def check_correction_patterns(tool_name, tool_input, state):
    corrections = load_corrections()
    if not corrections:
        return None
    file_path = tool_input.get('file_path', '')
    last_msg = state.get('last_user_message', '').lower()
    for corr in corrections:
        if corr.get('tool') and corr['tool'] != tool_name:
            continue
        trigger = corr.get('trigger', '').lower()
        if trigger and trigger not in last_msg:
            continue
        ctx = corr.get('context_pattern', '').lower()
        if ctx and ctx not in file_path.lower() and ctx not in str(tool_input).lower():
            continue
        return (f"CORRECTION PATTERN: Situazione simile a errore precedente. "
                f"Appreso da: {corr.get('learned_from', '?')}. "
                f"Fermati e verifica.")
    return None


def update_state_from_read(tool_name, tool_input, state):
    if tool_name == 'Read':
        file_path = tool_input.get('file_path', '')
        if file_path and file_path not in state.get('boot_files_read', []):
            state.setdefault('boot_files_read', []).append(file_path)
    state['tool_calls'] = state.get('tool_calls', 0) + 1
    if tool_name in ('Edit', 'Write', 'Bash'):
        action = tool_input.get('file_path', '') or tool_input.get('command', '')[:80]
        recent = state.setdefault('recent_actions', [])
        recent.append(f"{tool_name}: {action}")
        state['recent_actions'] = recent[-10:]


def maybe_save_seed(state):
    tool_calls = state.get('tool_calls', 0)
    last_seed_at = state.get('last_seed_at_calls', 0)
    if tool_calls - last_seed_at < SEED_INTERVAL_CALLS:
        return

    last_msg = state.get('last_user_message', '')
    actions = state.get('recent_actions', [])
    if not actions and not last_msg:
        return

    now = datetime.now()
    content = f"CHECKPOINT {tool_calls} calls | {now.strftime('%Y-%m-%d %H:%M')} | {NODE_ID}"
    if last_msg:
        content += f"\nLast operator: {last_msg[:200]}"
    if actions:
        content += "\nRecent: " + "; ".join(actions[-5:])

    # Write to messaging API as memo (if configured)
    if MESSAGING_URL and MESSAGING_TOKEN:
        try:
            import urllib.request
            import ssl
            ctx = ssl.create_default_context()
            body = json.dumps({
                'from': NODE_ID, 'to': NODE_ID, 'type': 'memo',
                'content': content
            }).encode()
            req = urllib.request.Request(MESSAGING_URL, data=body, method='POST',
                headers={'Content-Type': 'application/json', 'X-Auth-Token': MESSAGING_TOKEN})
            urllib.request.urlopen(req, timeout=3, context=ctx)
        except Exception:
            pass

    # Local file fallback
    seed_lines = [
        '# Active Reasoning', '',
        f'> Periodic seed — {tool_calls} tool calls',
        f'> {now.strftime("%Y-%m-%d %H:%M")} | {NODE_ID}', '',
    ]
    if last_msg:
        seed_lines += ['## Last operator message', last_msg[:300], '']
    if actions:
        seed_lines += ['## Recent actions (last 5)'] + [f'- {a}' for a in actions[-5:]] + ['']

    try:
        REASONING_FILE.write_text('\n'.join(seed_lines) + '\n')
        state['last_seed_at_calls'] = tool_calls
    except Exception:
        pass


def main():
    raw = sys.stdin.read()
    tool_name, tool_input = analyze_input(raw)
    if not tool_name:
        sys.exit(0)

    state = load_state()
    update_state_from_read(tool_name, tool_input, state)
    maybe_save_seed(state)
    save_state(state)

    warnings = []
    for check in [check_question_guard, check_memory_guard, check_boot_guard,
                   check_correction_patterns]:
        result = check(tool_name, tool_input, state)
        if result:
            warnings.append(result)

    if warnings:
        output = {
            'hookSpecificOutput': {
                'hookEventName': 'PreToolUse',
                'additionalContext': ' | '.join(warnings)
            }
        }
        print(json.dumps(output))

    sys.exit(0)


if __name__ == '__main__':
    main()
