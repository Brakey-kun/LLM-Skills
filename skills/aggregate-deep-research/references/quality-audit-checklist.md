# Quality Audit Checklist for Autonomous Enrichment Pipeline

## When to Use
Phase 0 of the autonomous enrichment cycle — runs at `action_cycle_position: 0` in `_loop_state.json`. Executes before any source sweeps or enrichment actions.

---

## Project Structure Verification

### Core Files Must Exist
| File | Purpose | Size Check |
|------|---------|------------|
| `_loop_state.json` | Pipeline state machine | > 300 bytes, valid JSON |
| `_portable_data.json` | Machine-readable dataset | > 100 KB, valid JSON, `total_ideas` matches |
| `_numbers.md` | Statistics ledger | > 1 KB, all headline numbers present |
| `guide.html` | Interactive HTML guide | > 200 KB, zero JS errors |
| `report-09-detailed-idea-blueprints.md` | Deep-dive markdown | > 100 KB, all 3 sections per idea |
| `_twitch_seed.json` | Twitch ideas seed data | > 10 KB, 18 entries |
| `master-report.md` | Master synthesis | > 10 KB |

### Data Consistency Checks
1. **Idea Count**: `_portable_data.json._meta.total_ideas` == count of entries in `everything` array == sum of category counts == sum of tier counts == `_loop_state.json.twitch_ideas_added` + 115
2. **Category Completeness**: Every entry in `everything` has non-empty `intent_and_origin`, `design_objective`, `my_analysis_and_suggestions`
3. **Tag Integrity**: In `guide.html`, verify `[SOURCE]` and `[MY ANALYSIS]` tags appear in rendered content (grep for `tag-src` and `tag-my` classes)
4. **Copy Feature**: 133 copy buttons present (`document.querySelectorAll('.copy-btn').length === 133`)

---

## HTML Verification Protocol

### Browser-Based (Preferred)
```javascript
// 1. Console errors
console.error/console.warn: must be empty

// 2. Visual emoji rendering
document.body.innerText.includes('\uD83C') === false  // no raw surrogate pairs

// 3. Interactive elements
document.querySelectorAll('.idea-card').length === 133
document.querySelectorAll('.copy-btn').length === 133

// 4. Event delegation works
// Click a card → expands; Click copy button → copies, doesn't expand
```

### Static Fallback (No Browser Tools)
```bash
# 1. Emoji double-encoding
grep -c '\\\\U[0-9a-fA-F]\\{8\\}' guide.html  # must be 0
grep -c '"' guide.html               # must be 0

# 2. Unclosed tags (crude)
grep -o '<div' guide.html | wc -l  vs  grep -o '</div' guide.html | wc -l

# 3. Script tag closure safety
grep -c '</script>' guide.html  # must be 0 (should be <\/script> in JSON)
```

---

## Portable JSON Integrity Checks

```python
import json
with open('_portable_data.json') as f:
    data = json.load(f)

# 1. Count integrity
assert len(data['everything']) == data['_meta']['total_ideas']
assert sum(len(v['ideas']) for v in data['categories'].values()) == data['_meta']['total_ideas']
assert sum(len(v['ideas']) for v in data['tiers'].values()) == data['_meta']['total_ideas']
assert len(data['idx_by_id']) == data['_meta']['total_ideas']

# 2. Field completeness
for idea in data['everything']:
    assert idea['intent_and_origin'].strip()
    assert idea['design_objective'].strip()
    assert idea['my_analysis_and_suggestions'].strip()
    assert idea['id'] in data['idx_by_id']

# 3. Category coverage
assert 'twitch' in data['categories']  # new category present
assert data['categories']['twitch']['count'] == 18
```

---

## Numbers Ledger (`_numbers.md`) Audit

Every statistic cited in any report or HTML must have a corresponding row in `_numbers.md`:

| Value | Claim | Source | Verification |
|-------|-------|--------|-------------|
| 133 | Total ideas | _data.json | programmatic |
| 18 | Twitch ideas added | _twitch_seed.json | programmatic |
| 40 | Hours tier count | _portable_data.json | programmatic |
| ... | ... | ... | ... |

**Action**: After any data modification, update `_numbers.md` with new claims before rebuilding HTML/JSON.

---

## Phase 0 Pass/Fail Criteria

| Check | Weight | Pass Threshold |
|-------|--------|----------------|
| Zero JS console errors | Critical | 0 |
| 133 ideas in all indexes | Critical | Exact |
| All 3 detail fields populated | Critical | 100% |
| Copy buttons functional | High | 133/133 |
| Emoji render as glyphs | High | 0 escaped sequences |
| Numbers ledger current | High | All headline stats present |
| Source tags in HTML | Medium | >100 `[SOURCE]` tags |

**If any Critical fails**: Fix immediately, rebuild artifacts, re-audit.
**If High fails**: Fix before next phase, but can proceed with note.
**If Medium fails**: Log and fix in next HTML rebuild (Phase 7).

---

## Common Issues & Fixes

| Symptom | Root Cause | Fix |
|---------|------------|-----|
| `"` visible on cards | Double entity encoding | Use raw quotes in Python string; escape only at final HTML write |
| `\U0001F3AF` literal text | Raw string `r\"\"\"` trap | Use literal emoji in Python strings, or apply regex fix after write |
| Copy button toggles card | Event bubbles to card handler | Add `event.stopPropagation()` on button + `if(e.target.closest('.copy-btn')) return;` in card handler |
| Tier counts mismatch | JSON rebuilt without sync | Always rebuild JSON AND HTML together; verify counts after each |
| `_numbers.md` stale | Forgot to update after sweep | Add ledger update as explicit step in each phase's protocol |

---

## Automation Note

When terminal is impaired (Windows git-bash fork errors), use browser tools for verification:
1. `browser_navigate('file:///C:/path/guide.html')`
2. `browser_console(expression='document.body.innerText')` for JSON extraction
3. `browser_console(expression='console.error...')` for error capture
4. `browser_vision()` for visual confirmation