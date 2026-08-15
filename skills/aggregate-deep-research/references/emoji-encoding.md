# Emoji/Unicode Encoding in HTML Artifacts

## The Problem

When writing self-contained HTML in Hermes, emoji and Unicode characters can end up as literal `\UXXXXXXXX` text instead of rendered characters:

1. **`write_file` double-escapes**: the tool escapes `\u` and `\U` sequences, so they become literal text in the file.
2. **Python raw strings**: `r"""..."""` strings do NOT interpret `\UXXXXXXXX` escape sequences.

## The Fix

### Use `execute_code` with direct Unicode (preferred)

```python
html = '...🎯...🇲🇦...🎨...'  # literal emoji in the string
with open(path, "w", encoding="utf-8") as f:
    f.write(html)
```

### Post-write regex repair (fallback)

If the file was already written with literal `\UXXXXXXXX` text:

```python
import re
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(r'(?<!\\)\\U([0-9a-fA-F]{8})', lambda m: chr(int(m.group(1), 16)), content)
content = re.sub(r'(?<!\\)\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
```

### Detection

Use `browser_vision` and ask: "Are emoji rendering as proper graphic characters or as literal `\U` text?"
