# Data-Driven HTML Generation

## When to Use

When Phase 2/3 involves converting **large collections of items** (50-300+) from markdown reports into an interactive HTML guide. The naive approach of hand-writing each HTML card/row doesn't scale — use a data-driven pipeline instead.

## The 3-Step Pipeline

```
Phase 1 Reports (.md)  ──►  Phase 2: Parse to JSON  ──►  Phase 3: Generate HTML from data
```

### Step 1: Parse Source Reports into Structured Data

Use `execute_code` with regex to extract all items from the master report (or sub-reports) into Python dictionaries:

```python
import re, json

# Parse tier table from markdown
def parse_tier_table(text):
    items = []
    for line in text.split('\n'):
        line = line.strip()
        if line.startswith('| ') and '---' not in line and line.count('|') >= 4:
            parts = [p.strip() for p in line.split('|')[1:-1]]
            if len(parts) >= 5 and parts[0].isdigit():
                items.append({
                    'num': int(parts[0]),
                    'name': parts[1],
                    'effort': parts[2],
                    'sources': parts[3],
                    'validation': parts[4]
                })
    return items
```

For sub-reports with richer detail (Problem/Solution/Stack fields), extract from `### N.NN Title` headers:

```python
items_details = {}
current_num = None
current_data = {}
for line in report_text.split('\n'):
    m = re.match(r'^###\s+(\d+\.\d+)\s+(.+)', line)
    if m:
        if current_num and current_data:
            items_details[current_num] = current_data
        current_num = m.group(1)
        current_data = {'title': m.group(2).strip()}
    elif current_num:
        fm = re.match(r'^\*\*(Problem|Solution|Why unsolved|Validation|Build time|Stack):\*\*\s*(.*)', line)
        if fm:
            current_data[fm.group(1).lower().replace(' ', '_')] = fm.group(2).strip()
```

### Step 2: Save Intermediate JSON

Write the structured data to `_data.json` in the output directory. This lets you inspect the parsed data before generating HTML, and provides a checkpoint:

```python
with open(os.path.join(base, "_data.json"), "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)
```

### Step 3: Generate HTML from Data

Build the HTML using Python string concatenation with `str.replace()` template pattern (NOT f-strings with CSS braces — see Phase 3 Architecture):

```python
# Generate card HTML for each item
cards_html = []
for item in t1:
    name = safe_to_html(item['name'])       # escaped text with <b>/<i> support
    effort = simple_escape(item['effort'])  # plain escaped text
    cards_html.append(f'''  <div class="idea-card" data-num="{item['num']}" data-cat="{item['category']}">
    <div class="idea-card-header">
      <span class="idea-num">#{item['num']}</span>
      <span class="idea-name">{name}</span>
      <div class="idea-badges">
        <span class="badge-effort">{effort}</span>
        <span class="badge-cat {item['category']}">{item['category']}</span>
        <span class="expand-icon">&#9660;</span>
      </div>
    </div>
    <div class="idea-card-body">
      <div class="idea-card-body-inner">
        <div class="sources-line">{simple_escape(item['sources'])}</div>
        <div class="detail-section">
          <h4><span class="tag-src">SOURCE</span> Intent &amp; Origin</h4>
          <p>{safe_to_html(item['intent'])}</p>
        </div>
        ...
      </div>
    </div>
  </div>''')

cards_html_str = '\\n'.join(cards_html)

# Use template-replacement pattern (avoids CSS brace conflicts)
template = open('template.html').read()
html = template.replace('TPL_CARDS', cards_html_str)
```

## Interactive Pattern: Event Delegation (NOT Inline onclick)

**Do not use `onclick="tc(this)"` on each card** — inline handlers may fail in sandboxed browsers (Hermes, headless) and create hard-to-debug scope issues.

Instead, use **event delegation** on the parent grid, with a single listener in the `<script>` block:

```javascript
// Single handler on grid container (event delegation)
document.querySelectorAll('.ideas-grid').forEach(function(grid){
  grid.addEventListener('click', function(e){
    var card = e.target.closest('.idea-card');
    if(!card) return;
    // Close other expanded cards
    document.querySelectorAll('.idea-card.expanded').forEach(function(c){
      if(c!==card) c.classList.remove('expanded');
    });
    card.classList.toggle('expanded');
  });
});
```

This approach:
- Works in sandboxed/restricted browser environments
- Handles any number of cards without per-element event binding
- Eliminates `eval()` dependencies from `onclick` attributes
- Gracefully handles clicks on child elements (badges, icons) via `e.target.closest()`

## Full Content Escaping Protocol

When converting parsed text (LLM-generated content, markdown descriptions) into HTML, use a **two-pass escape → reformat** approach:

```python
from html import escape as esc
import re

def simple_escape(txt):
    """Escape text for safe HTML insertion (no formatting)."""
    return esc(txt.strip())

def safe_to_html(txt):
    """Convert markdown bold/italic + SOURCE tags to safe HTML.
    Step 1: escape ALL HTML special chars.
    Step 2: re-apply safe formatting via regex on escaped text.
    """
    txt = txt.strip()
    txt = esc(txt)                                    # & < > " ' → entities
    txt = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', txt)  # **bold** → <b>
    txt = re.sub(r'_(.*?)_', r'<i>\1</i>', txt)        # _italic_ → <i>
    txt = re.sub(r'\[SOURCE\]', r'<span class="tag-src">SOURCE</span>', txt)
    txt = re.sub(r'\[MY ANALYSIS\]', r'<span class="tag-my">MY ANALYSIS</span>', txt)
    txt = txt.replace('\n', ' ')
    return re.sub(r'  +', ' ', txt)
```

**Why two-pass?** If you escape first and then apply formatting, `<b>` tags survive because `esc()` turns `<` into `&lt;`, then the regex re-adds literal `<b>`. The entities from esc() that are NOT formatting patterns stay safe.

## `</script>` Safety in Embedded JSON

When embedding data as JSON inside a `<script>` block, any `</script>` literal in the data will **break the page** — the browser interprets it as closing the script tag:

```python
import json

json_str = json.dumps(data, ensure_ascii=False)
# CRITICAL: escape closing script tag sequences
json_str = json_str.replace('</script>', '<\\/script>')
json_str = json_str.replace('</Script>', '<\\/Script>')  # case variants

html += f'<script>const DATA={json_str};</script>'
```

Without this, a description like `"Embed with one <script> tag"` produces `</script>` in the JSON value, which prematurely closes the outer `<script>` block.

## Verification After Generation

When converting parsed text into HTML content, you need to escape HTML special characters. But **don't double-escape**:

**Bad** — produces `&amp;quot;` in the browser:
```python
def esc_text(s):
    return s.replace('"', '&quot;')  # then f-string wraps in HTML...
```

**Good** — produces actual `"` on screen:
```python
def esc_text(s):
    # Only escape < and & — leave quotes for f-string context boundaries
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
```

Then use `{esc_text(name)}` inside HTML context and `{name}` (unescaped) inside `onclick` or `data-*` attributes.

**Alternative**: Use literal quotes in content and rely on the browser to render them. If you get `&amp;quot;` on screen, the root cause is double-escaping: `.replace('"', '&quot;')` produced HTML entities, then Python's f-string or the `write_file` tool added another layer. Fix by finding and removing the extra replacement.

## Mapping Master Items to Sub-Report Detail

Master report items are numbered sequentially (#1, #2, #3...). Sub-report items use hierarchical numbering (1.01, 1.02, 2.01...). Map them:

```python
# For T1 items (master #1-#12 map to sub-report 1.01-1.12)
def get_detail_for_t1(master_num):
    key = f"1.{master_num:02d}"
    return items_details.get(key, None)
```

For T2 items, offset by the T1 count:
```python
key = f"2.{master_num - 30:02d}"  # if T1 has 30 items
```

## Verification After Generation

After writing the HTML, run these checks inside `execute_code`:

```python
# 1. Count items per tier
t1_count = len(re.findall(r'class="idea-card"', html))
t2_rows = len(re.findall(r'<tr class="idea-row"', html))

# 2. Verify every item number is present
for i in range(1, 31):
    assert f'#{i:02d}</span>' in html, f"Missing T1 item #{i}"

# 3. Check for double-encoding
assert '&amp;quot;' not in html, "Double-encoded entities found!"

# 4. Check for script safety — no raw </script> in content areas
#    (The only </script> should be the one closing the <script> block)
script_close_count = html.count('</script>')
assert script_close_count == html.count('<script>'), \
    f"Mismatched script tags: {html.count('<script>')} open vs {script_close_count} close"
# Extra check: look for </script> in non-script contexts (inside embedded JSON)
body_scripts = re.findall(r'<body>.*?</script>', html, re.DOTALL)
for match in body_scripts:
    if match.count('</script>') > 1:
        print("WARNING: multiple </script> in body — possible JSON injection")

# 5. Check for unescaped angle brackets in visible content
#    (scan for < and > that aren't part of valid HTML tags)
tag_pattern = re.findall(r'[^<]</?[a-z]', html)  # rough check
```

Then verify visually with `browser_navigate` + `browser_vision`.
