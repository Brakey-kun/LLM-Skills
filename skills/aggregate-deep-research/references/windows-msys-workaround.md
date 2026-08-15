# Windows/MSYS Terminal Fork Failure Workaround

## Problem
On Windows with git-bash/MSYS (the default shell for Hermes `terminal` tool), commands frequently fail with:
```
fork: Resource temporarily unavailable
exit code 0xC0000142
dofork: child -1 - forked process XXXX died unexpectedly
```

This is a known MSYS limitation: the fork() emulation on Windows hits process table limits quickly, especially under load.

## Impact on aggregate-deep-research Pipeline
The pipeline requires heavy filesystem I/O:
- Creating output directories (`mkdir -p`)
- Writing 10+ large markdown reports (10-20KB each)
- Writing HTML guide (60KB+)
- Writing JSON exports
- Reading files for verification

All of these fail randomly when using `terminal` tool on Windows/MSYS.

## Mandatory Solution: Use `execute_code` for All Filesystem Operations

### Directory Creation
```python
import os
output_dir = os.path.expanduser("~/hermes-workspace/your-project")
os.makedirs(output_dir, exist_ok=True)
# Also create subdirectories
for subdir in ["reports", "references", "data"]:
    os.makedirs(os.path.join(output_dir, subdir), exist_ok=True)
```

### File Writing (UTF-8, handles emoji correctly)
```python
import os

path = os.path.join(output_dir, "reports", "report-01.md")
with open(path, "w", encoding="utf-8") as f:
    f.write(content)  # content can include literal emoji, no escaping needed
```

### File Reading
```python
import os

path = os.path.join(output_dir, "reports", "report-01.md")
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
```

### JSON Writing (ensure_ascii=False for emoji)
```python
import json

path = os.path.join(output_dir, "_portable_data.json")
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

## When to Still Use `terminal`
Reserve `terminal` only for operations that MUST run in shell:
- `git` commands
- Package managers (`pnpm`, `cargo`, `npm`)
- Build commands (`cargo build`, `pnpm build`)
- Process management
- Network commands (`curl` for API calls if not using `execute_code` + `urllib`)

## Verification Pattern
After writing files via `execute_code`, verify with a quick read:
```python
import os
path = os.path.join(output_dir, "guide.html")
size = os.path.getsize(path)
exists = os.path.exists(path)
print(f"guide.html: {size} bytes, exists: {exists}")
```

## Integration with Pipeline
1. **Phase −1 Capability Probe**: Detect Windows/MSYS → record workaround in `_environment.md`
2. **Phase 0 Setup**: Use `execute_code` for directory creation
3. **Phase 1 Reports**: Use `execute_code` for all report writes
4. **Phase 2 Master**: Use `execute_code` for synthesis write
5. **Phase 3 HTML**: Use `execute_code` for HTML + JSON writes
6. **Phase 4 Verification**: Use `execute_code` for static checks (grep equivalent in Python)

## Example: Complete File Write with Verification
```python
import os, json
from html import escape

output_dir = os.path.expanduser("~/hermes-workspace/algo-academy-platform")

# Write HTML guide
html_path = os.path.join(output_dir, "guide.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

# Write build prompt
prompt_path = os.path.join(output_dir, "BUILD_PROMPT.md")
with open(prompt_path, "w", encoding="utf-8") as f:
    f.write(prompt_content)

# Verify
for p in [html_path, prompt_path]:
    size = os.path.getsize(p)
    print(f"{os.path.basename(p)}: {size} bytes, exists: {os.path.exists(p)}")
```

## Why This Works
- `execute_code` runs in the same Python process (no fork)
- Python's `open()` is native, not shell-dependent
- UTF-8 encoding handled correctly (no double-escaping)
- Large content (>100KB) writes reliably
- Cross-platform: same code works on Linux/macOS too

## Anti-Pattern: Never Do This on Windows/MSYS
```bash
# DON'T - will fail randomly
mkdir -p ~/hermes-workspace/project
cat > file.md << 'EOF'
content
EOF
echo "content" > file.md
```