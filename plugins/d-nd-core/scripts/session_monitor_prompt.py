#!/usr/bin/env python3
"""
session_monitor_prompt.py — UserPromptSubmit hook (D-ND Seed)

Captures operator message and updates monitor state.
Imports is_question from session_monitor for shared logic.
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

PROJECT_DIR = Path(os.environ.get('DND_PROJECT_DIR', os.getcwd()))
STATE_FILE = PROJECT_DIR / '.claude' / 'hooks' / 'monitor_state.json'

sys.path.insert(0, str(Path(__file__).parent))
from session_monitor import is_question


def main():
    raw = sys.stdin.read()
    try:
        data = json.loads(raw)
        prompt = data.get('user_prompt', data.get('prompt', ''))
    except Exception:
        prompt = raw.strip()

    state = {}
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                state = json.load(f)
        except Exception:
            pass

    state['last_user_message'] = prompt
    state['last_user_is_question'] = is_question(prompt)
    state['last_user_time'] = datetime.now().isoformat()

    try:
        STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except Exception:
        pass

    sys.exit(0)


if __name__ == '__main__':
    main()
