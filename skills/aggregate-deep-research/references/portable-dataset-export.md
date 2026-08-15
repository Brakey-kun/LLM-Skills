# Portable Dataset Export — _portable_data.json

## When to generate

After Phase 3 (HTML Guide), or whenever the user asks for a portable/machine-readable version of the entire research corpus. Also regenerate whenever data changes (new sources, enriched entries, new ideas added). **In the autonomous enrichment pipeline, rebuild after EVERY data-modifying phase (1, 2, 3, 5, 6, 7).**

---

## Schema (Version 2.1)

```json
{
  "_meta": {
    "project": "string",
    "version": "string (semver)",
    "source_dir": "string (absolute path)",
    "total_ideas": "integer",
    "total_categories": "integer",
    "total_patterns": "integer",
    "last_updated": "ISO date (YYYY-MM-DD)",
    "description": "string"
  },
  "summary": {
    "tier_breakdown": {
      "hours": "integer",
      "weekend": "integer",
      "sprint": "integer",
      "platform": "integer"
    },
    "category_breakdown": {
      "cat_key": "integer count"
    },
    "total_source_categories": "integer",
    "total_reports": "integer",
    "twitch_trend_ideas_added": "integer"
  },
  "categories": {
    "cat_key": {
      "label": "Display Label",
      "count": "integer",
      "ideas": ["array of idea ids"]
    }
  },
  "tiers": {
    "tier_key": {
      "label": "Display Label",
      "count": "integer",
      "ideas": ["array of idea ids"]
    }
  },
  "everything": [
    {
      "id": "integer",
      "name": "string",
      "tier": "hours|weekend|sprint|platform",
      "tier_label": "display label",
      "effort": "string (e.g. '2 hrs', '3 days')",
      "category": "cat_key",
      "sources": "string (source citations)",
      "validation": "string (validation approach)",
      "intent_and_origin": "string (full SOURCE section)",
      "design_objective": "string (full SOURCE section)",
      "my_analysis_and_suggestions": "string (full MY ANALYSIS section)"
    }
  ],
  "top_20_quick_start": [
    {
      "id": "integer",
      "name": "string",
      "effort": "string",
      "why_first": "string"
    }
  ],
  "design_patterns": [
    {
      "name": "string",
      "description": "string"
    }
  ],
  "idx_by_id": {
    "1": { "full entry from everything" }
  },
  "idx_by_category": {
    "utility": [1, 3, 7, ...],
    "twitch": [116, 117, ...]
  },
  "idx_by_tier": {
    "hours": [1, 2, 3, ..., 119, 121, ...],
    "weekend": [31, 32, ..., 116, 117, ...]
  }
}
```

---

## Key Constraints

1. **html.unescape() all names and metadata** — `_data.json` often has HTML entities
2. **ensure_ascii=False** when serializing — emoji must survive as literal characters
3. **All entries must be present** — verify count after generation (115 original + 18 Twitch = 133)
4. **Every entry must have all three detail fields** (intent_and_origin, design_objective, my_analysis_and_suggestions) — if any is empty, flag it
5. **Keep in sync with guide.html** — every time data changes, rebuild both
6. **Escape `</script>` in text fields** — when embedding JSON in HTML script tags, replace `</script>` with `<\\/script>` to avoid premature script closure

---

## Python Generation Pattern

```python
import json, re
from html import unescape
from pathlib import Path

def rebuild_portable_json():
    # 1. Parse report-09-detailed-idea-blueprints.md for all ideas
    # 2. Build everything[] array with all fields
    # 3. Compute summaries, indexes
    # 4. Write _portable_data.json with ensure_ascii=False
    # 5. Update _loop_state.json portable_json_version++
    
    # CRITICAL: escape </script> in any text field that may end up in HTML
    for idea in everything:
        for field in ['intent_and_origin', 'design_objective', 'my_analysis_and_suggestions']:
            if field in idea:
                idea[field] = idea[field].replace('</script>', '<\\/script>')
    
    # Write with literal emoji (not \u escapes)
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    Path('_portable_data.json').write_text(json_str, encoding='utf-8')
```

---

## Verification Checklist (Run After Rebuild)

```python
with open('_portable_data.json') as f:
    d = json.load(f)

# 1. Meta consistency
assert d['_meta']['total_ideas'] == len(d['everything'])
assert d['_meta']['total_ideas'] == sum(c['count'] for c in d['categories'].values())
assert d['_meta']['total_ideas'] == sum(t['count'] for t in d['tiers'].values())

# 2. Index completeness
assert len(d['idx_by_id']) == d['_meta']['total_ideas']
for cat, ids in d['idx_by_category'].items():
    assert all(i in d['idx_by_id'] for i in ids)
for tier, ids in d['idx_by_tier'].items():
    assert all(i in d['idx_by_id'] for i in ids)

# 3. Field completeness
for idea in d['everything']:
    assert idea['intent_and_origin'].strip(), f"Idea {idea['id']} missing intent"
    assert idea['design_objective'].strip(), f"Idea {idea['id']} missing design"
    assert idea['my_analysis_and_suggestions'].strip(), f"Idea {idea['id']} missing analysis"
    assert idea['id'] in d['idx_by_id']

# 4. Category coverage
assert 'twitch' in d['categories'], "New twitch category must be present"
assert d['categories']['twitch']['count'] == 18, "Twitch ideas count mismatch"
```

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Forgetting `</script>` escape | HTML guide breaks when JSON embedded | Always replace `</script>` → `<\\/script>` in text fields |
| Double-encoding emoji | `\u0001F3AF` visible on page | Use `ensure_ascii=False` + Python `open(encoding='utf-8')` |
| Missing Twitch category | `idx_by_category` lacks 'twitch' | Ensure category key is 'twitch' not 'twitch-trend' |
| Tier label mismatch | 'Hours (2hr-2d)' vs 'hours' | Use consistent tier_key ('hours', 'weekend', 'sprint', 'platform') |
| Count drift | Meta says 133, everything has 132 | Rebuild from single source (report-09), not incremental patch |
| `_numbers.md` stale | Stats don't match JSON | Add ledger update as explicit step in each phase's protocol |

---

## Phase Integration (Autonomous Enrichment Loop)

In the autonomous pipeline, `_portable_data.json` MUST be rebuilt after:
- Phase 1 (Source Sweep HN) — new sources added to ideas
- Phase 2 (Deep Enrich) — idea analysis fields updated
- Phase 3 (Source Sweep YT) — new YouTube sources
- Phase 5 (Source Sweep Curated) — new curated sources
- Phase 6 (Expand Domain) — 3-5 new ideas added
- Phase 7 (Rebuild HTML + JSON) — full regeneration

Track `portable_json_version` in `_loop_state.json` alongside `html_version`. Increment both together in Phase 7.