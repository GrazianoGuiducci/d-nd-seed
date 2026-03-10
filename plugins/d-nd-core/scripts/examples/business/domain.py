#!/usr/bin/env python3
"""
Business Domain — Domandatore Configuration

Vocabulary, experiment bodies, and banks for business decision analysis.
Install: copy this file and seed.json to your project, then run:

  python domandatore.py --seed seed.json --domain domain.py

Or import directly:

  from domain import PRELUDE, VOCABULARY, BODIES, CATALOG
  engine = Domandatore(seed_path='seed.json', vocabulary=VOCABULARY, ...)
"""

import numpy as np
import json

# ============================================================
# PRELUDE — Shared code injected into every experiment
# ============================================================

PRELUDE = '''
import numpy as np
import json

def simulate_cohort(n_customers, churn_rate, months=12):
    """Simulate customer cohort over time."""
    cohort = [n_customers]
    for _ in range(months - 1):
        cohort.append(int(cohort[-1] * (1 - churn_rate)))
    return cohort

def revenue_curve(price, n_customers, growth_rate, months=12):
    """Monthly revenue with growth."""
    rev = []
    n = n_customers
    for _ in range(months):
        rev.append(price * n)
        n = int(n * (1 + growth_rate))
    return rev

def feature_dilution(n_features, core_value=1.0, dilution_per_feature=0.05):
    """How much core value remains as features are added."""
    return core_value * (1 - dilution_per_feature) ** max(0, n_features - 1)
'''


# ============================================================
# VOCABULARY — Measurable quantities
# ============================================================

VOCABULARY = {
    'ltv_ratio': {
        'desc': 'Ratio of lifetime value between flat and per-seat pricing',
        'codice': '''
prices = {'flat': 99, 'per_seat_5': 15*5, 'per_seat_20': 15*20}
ltv_flat = prices['flat'] * 24  # 24 month average lifetime
ltv_small = prices['per_seat_5'] * 18
ltv_large = prices['per_seat_20'] * 30
result = {'flat': ltv_flat, 'small_team': ltv_small, 'large_team': ltv_large}
print(json.dumps(result))
''',
        'target': 'per_seat captures 2x+ from large customers',
    },
    'churn_by_features': {
        'desc': 'Churn rate as function of feature count',
        'codice': '''
results = {}
for n_feat in [3, 5, 8, 12, 20]:
    core = feature_dilution(n_feat)
    # Churn increases as core value dilutes
    churn = 0.03 + (1 - core) * 0.15
    remaining = simulate_cohort(1000, churn, 12)
    results[f'features_{n_feat}'] = remaining[-1]
print(json.dumps(results))
''',
        'target': 'fewer features = more retention',
    },
    'breakeven_hire': {
        'desc': 'Months to breakeven for early vs late hire',
        'codice': '''
salary = 8000  # monthly cost
early_boost = 1.3  # 30% growth boost from early hire
late_boost = 1.15  # 15% efficiency boost from late hire
base_revenue = 10000
results = {}
# Early hire: spend now, grow faster
cumulative_early = 0
for m in range(1, 25):
    rev = base_revenue * early_boost ** (m/12) - salary
    cumulative_early += rev
    if cumulative_early > 0 and 'early_breakeven' not in results:
        results['early_breakeven'] = m
# Late hire: grow slow, hire when profitable
cumulative_late = 0
hire_month = 6
for m in range(1, 25):
    if m >= hire_month:
        rev = base_revenue * late_boost ** ((m-hire_month)/12) * 1.2 - salary
    else:
        rev = base_revenue
    cumulative_late += rev
    if m >= hire_month and cumulative_late > 0 and 'late_breakeven' not in results:
        results['late_breakeven'] = m
results['early_cumulative_12m'] = round(cumulative_early, 0)
results['late_cumulative_12m'] = round(cumulative_late, 0)
print(json.dumps(results))
''',
        'target': 'context-dependent — neither is universally better',
    },
    'channel_roi': {
        'desc': 'ROI comparison: content vs paid over 12 months',
        'codice': '''
months = 12
# Content: slow start, compounds
content_cost = 3000  # monthly
content_leads = [int(5 * (1.15 ** m)) for m in range(months)]
# Paid: immediate, linear
paid_cost = 5000  # monthly
paid_leads = [50] * months  # constant
content_total_cost = content_cost * months
content_total_leads = sum(content_leads)
paid_total_cost = paid_cost * months
paid_total_leads = sum(paid_leads)
results = {
    'content_roi': round(content_total_leads / content_total_cost * 1000, 2),
    'paid_roi': round(paid_total_leads / paid_total_cost * 1000, 2),
    'content_month12_leads': content_leads[-1],
    'paid_month12_leads': paid_leads[-1],
    'crossover_month': next((m for m in range(months) if content_leads[m] > paid_leads[m]), None),
}
print(json.dumps(results))
''',
        'target': 'content overtakes paid after crossover',
    },
}


# ============================================================
# BODIES — Experiment code blocks
# ============================================================

BODIES = {
    'ltv_ratio': (VOCABULARY['ltv_ratio']['codice'], 'per_seat captures 2x+ from large customers'),
    'churn_by_features': (VOCABULARY['churn_by_features']['codice'], 'fewer features = more retention'),
    'breakeven_hire': (VOCABULARY['breakeven_hire']['codice'], 'context-dependent'),
    'channel_roi': (VOCABULARY['channel_roi']['codice'], 'content overtakes paid after crossover'),
}


# ============================================================
# CATALOG — Named experiment banks
# ============================================================

def bank_pricing(tid):
    """Pricing model comparison experiments."""
    return {
        'id': f'PRICING_{tid}',
        'domain': 'pricing',
        'code': PRELUDE + VOCABULARY['ltv_ratio']['codice'],
        'criterion': 'Per-seat captures more value from larger customers',
    }

def bank_feature_scope(tid):
    """Feature dilution experiments."""
    return {
        'id': f'FEATURE_{tid}',
        'domain': 'product',
        'code': PRELUDE + VOCABULARY['churn_by_features']['codice'],
        'criterion': 'Core value dilutes with feature count',
    }

def bank_hiring(tid):
    """Hiring timing experiments."""
    return {
        'id': f'HIRE_{tid}',
        'domain': 'operations',
        'code': PRELUDE + VOCABULARY['breakeven_hire']['codice'],
        'criterion': 'Breakeven depends on growth rate and timing',
    }

def bank_channels(tid):
    """Marketing channel comparison."""
    return {
        'id': f'CHANNEL_{tid}',
        'domain': 'marketing',
        'code': PRELUDE + VOCABULARY['channel_roi']['codice'],
        'criterion': 'Content compounds, paid is linear',
    }

CATALOG = {
    'pricing': (bank_pricing, ['pricing', 'price', 'revenue', 'seat', 'flat', 'tier']),
    'features': (bank_feature_scope, ['feature', 'scope', 'churn', 'retention', 'product', 'dilution']),
    'hiring': (bank_hiring, ['hire', 'hiring', 'team', 'salary', 'growth', 'headcount']),
    'channels': (bank_channels, ['content', 'paid', 'marketing', 'channel', 'acquisition', 'seo']),
}
