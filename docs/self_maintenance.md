# Self-Maintenance Pattern — Autonomous System Health

> How to build a custodian that keeps your system healthy without human
> intervention, while respecting boundaries of what it can touch.

## The Problem

Systems drift. Hooks get modified during sessions and diverge from templates.
Dependencies go stale. Logs accumulate. Config files develop inconsistencies.
Manual maintenance doesn't scale — you forget, you're busy, you don't notice.

## Core Principles

1. **Orchestrate, don't reimplement** — the custodian composes existing tools
   (monitors, fixers, validators), it doesn't rewrite them.
2. **Three tiers of autonomy** — not everything should be auto-fixed.
3. **Cooldown** — if a fix fails, back off. Don't retry the same fix every cycle.
4. **Ignore list** — some files must NEVER be touched automatically.

## Three Tiers

| Tier | What | Example | Action |
|------|------|---------|--------|
| **Tier 1: Auto** | Safe, reversible fixes | Restart a service, sync a config file | Fix automatically, report |
| **Tier 2: Notify** | Needs human judgment | Dependency upgrade, structural change | Report finding, suggest fix, wait |
| **Tier 3: Escalate** | Dangerous or unclear | Data migration, breaking change | Alert immediately, do nothing |

## Structure

```
tools/
├── custode.js           # Orchestrator (main cycle)
├── proactive_monitor.js # Health checks (read-only)
├── proactive_fixer.js   # Fix engine (write, controlled)
└── data/
    ├── custode_cooldown.json   # Failed fix tracking
    └── custode_report_*.json   # Cycle reports
```

## Custodian Skeleton (Node.js)

```javascript
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

class Custode {
  constructor({ dryRun = true, maxFixes = 10 } = {}) {
    this._dryRun = dryRun;
    this._maxFixes = maxFixes;
    this._cooldown = this._loadCooldown();
    this._ignoreList = [
      'core/*',           // Never touch core
      'boot.js',          // Never touch entry point
      'data/secrets.json' // Never touch secrets
    ];
  }

  async runCycle() {
    const report = { timestamp: new Date().toISOString(), sections: {} };

    // 1. Infrastructure audit (read-only)
    report.sections.infra = await this._auditInfrastructure();

    // 2. Apply safe fixes (Tier 1 only)
    if (!this._dryRun) {
      report.sections.fixes = await this._applySafeFixes(report.sections.infra);
    }

    // 3. Check capability drift (hooks vs templates)
    report.sections.drift = await this._checkCapabilityDrift();

    // 4. Report
    this._saveReport(report);
    this._notify(this._formatSummary(report));

    return report;
  }

  async _auditInfrastructure() {
    const checks = [];

    // Disk space
    checks.push(this._check('disk', () => {
      const df = execSync('df -h / | tail -1').toString();
      const usage = parseInt(df.match(/(\d+)%/)?.[1] || 0);
      return { ok: usage < 90, value: `${usage}%`, threshold: '90%' };
    }));

    // Git status (uncommitted changes)
    checks.push(this._check('git-clean', () => {
      const status = execSync('git status --porcelain').toString().trim();
      return { ok: status === '', value: status ? 'dirty' : 'clean' };
    }));

    // Service health
    checks.push(this._check('service', () => {
      try {
        execSync('curl -s -o /dev/null -w "%{http_code}" http://localhost:3002/health');
        return { ok: true, value: 'responding' };
      } catch {
        return { ok: false, value: 'unreachable' };
      }
    }));

    return { checks, anomalies: checks.filter(c => !c.ok).length };
  }

  async _checkCapabilityDrift() {
    // Compare installed hooks against templates
    // Hash both, report mismatches
    const drifts = [];
    const templateDir = 'templates/hooks/';
    const installedDir = 'hooks/';

    // For each template, check if installed version matches
    const templates = fs.readdirSync(templateDir).filter(f => f.endsWith('.tmpl'));
    for (const tmpl of templates) {
      const installed = tmpl.replace('.tmpl', '');
      const installedPath = path.join(installedDir, installed);
      if (!fs.existsSync(installedPath)) {
        drifts.push({ file: installed, status: 'missing' });
        continue;
      }
      // Compare hashes (simplified — real implementation renders template first)
      const tmplHash = this._hash(fs.readFileSync(path.join(templateDir, tmpl), 'utf8'));
      const instHash = this._hash(fs.readFileSync(installedPath, 'utf8'));
      if (tmplHash !== instHash) {
        drifts.push({ file: installed, status: 'drifted', template: tmplHash, installed: instHash });
      }
    }
    return { drifts, total: drifts.length };
  }

  _check(id, fn) {
    try {
      const result = fn();
      return { id, ...result };
    } catch (e) {
      return { id, ok: false, value: 'error', error: e.message };
    }
  }

  _isIgnored(filepath) {
    return this._ignoreList.some(pattern => {
      if (pattern.endsWith('/*')) {
        return filepath.startsWith(pattern.slice(0, -2));
      }
      return filepath === pattern;
    });
  }

  _loadCooldown() {
    const p = 'data/custode_cooldown.json';
    if (fs.existsSync(p)) return JSON.parse(fs.readFileSync(p, 'utf8'));
    return {};
  }

  _inCooldown(checkId) {
    const entry = this._cooldown[checkId];
    if (!entry) return false;
    const elapsed = Date.now() - new Date(entry.lastFailed).getTime();
    // Exponential backoff: 1h, 4h, 16h, 64h...
    const backoff = Math.pow(4, entry.failures - 1) * 3600000;
    return elapsed < backoff;
  }

  _hash(str) {
    let h = 0;
    for (let i = 0; i < str.length; i++) {
      h = ((h << 5) - h + str.charCodeAt(i)) | 0;
    }
    return h.toString(16);
  }

  _saveReport(report) {
    const filename = `custode_report_${report.timestamp.slice(0, 10)}.json`;
    fs.writeFileSync(path.join('data', filename), JSON.stringify(report, null, 2));
  }

  _notify(msg) { console.log(msg); }
  _formatSummary(report) { return JSON.stringify(report, null, 2); }
}

// Run nightly via cron:
// 0 3 * * * cd /your/project && node tools/custode.js
if (require.main === module) {
  const dryRun = !process.argv.includes('--live');
  new Custode({ dryRun }).runCycle().catch(console.error);
}

module.exports = Custode;
```

## Cron Setup

```bash
# /etc/cron.d/custode
0 3 * * * cd /path/to/project && node tools/custode.js --live >> logs/custode.log 2>&1
```

## Capability Drift — The Loop Problem

A common issue: the custodian syncs hooks from templates, but the system
evolves hooks during sessions. Next night, the custodian detects drift
and overwrites. Solution:

1. **locallyManaged flag** — hooks evolved by the system get flagged.
   The custodian skips them.
2. **Template versioning** — only sync when the template version changes,
   not when the hash changes.
3. **Merge, don't overwrite** — diff the changes and apply only the
   template's new parts, preserving local adaptations.

## Report Format

```json
{
  "timestamp": "2026-03-06T03:00:01Z",
  "dryRun": false,
  "sections": {
    "infra": { "checks": [...], "anomalies": 0 },
    "fixes": { "applied": 2, "failed": 0 },
    "drift": { "drifts": [], "total": 0 }
  },
  "duration": 4200
}
```
