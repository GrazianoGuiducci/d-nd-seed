---
name: assertion-verifier
description: Define testable claims about your project, run them, and crystallize results into a seed. Use when you need to verify that theory matches implementation, track what passes and what breaks, and identify where potential is blocked.
---

# Assertion Verifier — Claims Meet Reality

Register testable assertions about your project. Each assertion has an ID, a claim, and a test function. The verifier runs them all and produces a structured report: PASS / FAIL / SKIP.

## Assertion Format

Each assertion is a dict:

```python
{
    "id": "AUTH_01",
    "claim": "Login endpoint returns 200 for valid credentials",
    "test": lambda: check_login_endpoint(),  # -> (bool, detail_string)
    "source": "API spec v2.1",
    "group": "auth"  # optional grouping
}
```

The test function must return `(passed: bool, detail: str)`. If it raises an exception, the assertion is marked SKIP.

## Integration with Seed Cycle

The assertion verifier feeds directly into `seed_cycle.py`:

```python
from seed_cycle import ASSERTIONS, run_cycle

ASSERTIONS.extend([
    {"id": "DB_01", "claim": "Migration is up to date", "test": check_migration},
    {"id": "API_01", "claim": "Health endpoint responds", "test": check_health},
])

run_cycle(update=True)  # runs assertions, crystallizes into seed
```

## What the Results Mean

| Status | Meaning | Seed Effect |
|--------|---------|-------------|
| **PASS** | Claim confirmed by data | If ALL pass: "suspicious symmetry" tension |
| **FAIL** | Claim contradicted by data | High-priority "contradiction" tension |
| **SKIP** | Test can't run (missing prerequisite) | "Blocked potential" entry |

## Usage Patterns

**Nightly verification:**
```bash
python -c "
from seed_cycle import ASSERTIONS, verify_assertions, crystallize_seed, load_seed
# ... register assertions ...
results = verify_assertions()
crystallize_seed(results, load_seed())
"
```

**Interactive check:**
```
> verify my assertions
```
The coder runs all registered assertions and reports results.

## Key Principle

Add tests that CAN fail. If everything always passes, you're testing tautologies. The value is in the FAIL and SKIP results — they show where the system's real edges are.

$ARGUMENTS
