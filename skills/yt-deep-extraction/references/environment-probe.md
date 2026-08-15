# Environment Capability Probe Template

Use this at the start of every extraction (Phase −1). Fill in the Status column for your runtime.

## Capability Table

| Capability | Status | Notes |
|------------|--------|-------|
| Web search | Partial | browser_navigate works; may CAPTCHA |
| YouTube page access | Works | browser_navigate + browser_console |
| yt-dlp (metadata) | Varies | `uv run yt-dlp` if terminal works |
| youtube_transcript_api | Varies | `uv run youtube_transcript_api` if terminal works |
| Terminal/shell | Varies | git-bash MSYS fork bug on Windows (exit 3221225794) |
| browser_vision | Varies | Provider upstream errors may occur |
| File write | Varies | Fails if terminal is broken (uses shell under the hood) |
| skill_manage write_file | Works | Alternative when write_file fails |
| JavaScript in browser | Works | browser_console(expression=...) |
| execute_code | Varies | May be blocked in cron/sandbox modes |

## Adaptations Decision Tree

```
Can I run `uv run yt-dlp --dump-json`?
  YES → Use yt-dlp for metadata + youtube_transcript_api for transcripts
  NO  → Fall back to browser-only extraction:
        1. browser_navigate(video URL)
        2. Expand description (...more button)
        3. Extract from document.body.innerText
        4. Try "Show transcript" button click
        5. skill_manage write_file for output storage

Can I use `write_file`?
  YES → Write to output directory (~/hermes-workspace/yt-extraction-{slug}/)
  NO  → Use skill_manage(write_file) → references/ directory
        → Deliver content inline in final message
        → Ask user for alternative output path if needed
```

---

## Session: Quant Guild Extraction (2025-07-17)

**Runtime**: Hermes Desktop on Windows 10 (git-bash/MSYS)
**Model**: nemotron-3-ultra-free (opencode-zen)
**Terminal Status**: **BROKEN** — MSYS fork crash (exit 3221225794 / 0xC0000142)
**Browser**: WORKING — browser_navigate, browser_console, browser_click, browser_snapshot
**File Write**: PARTIAL — write_file fails; skill_manage write_file WORKS
**Operating Tier**: **C** (small context, browser-only, free model)

### Filled Probe Table (This Session)

| Capability | Status | Method | Fallback Used | Notes |
|---|---|---|---|---|
| Shell / code execution | **FAILED** | terminal() | execute_code (also blocked) | MSYS fork crash — Windows git-bash broken |
| Outbound network (PyPI) | UNKNOWN | pip install --dry-run yt-dlp | N/A | Cannot test — shell broken |
| yt-dlp | **FAILED** | yt-dlp --version | N/A | Shell broken |
| youtube_transcript_api | **FAILED** | python import | N/A | Shell broken |
| Browser automation | **WORKS** | browser_navigate + browser_console | — | Primary extraction method |
| Vision / image understanding | UNKNOWN | browser_vision | — | Not tested; assume unavailable on free model |
| Persistent file read/write | **PARTIAL** | write_file / skill_manage | skill_manage write_file | skill_manage to references/ is reliable |
| Long-running / background | UNKNOWN | cronjob / terminal background | N/A | Not tested |

### Operating Tier Declaration

**Tier C — Small context / weaker instruction-following** (free model, ~8K-32K context, browser-only extraction)

**Adaptations for Tier C:**
- Target 60–200 lines per video report instead of 100–500
- Process one video fully (fetch → save raw → write report → self-audit) before next
- Merge master report incrementally (pairwise) rather than single-pass synthesis
- Re-read on-disk files before each subsection instead of trusting context
- Use skill_manage write_file for ALL persistence (write_file unreliable)
- Browser-only pipeline: metadata from DOM, transcripts via "Show transcript" click, screenshots via browser if available

---

## Session: Mark Tilbury Extraction (2026-07-17)

**Runtime**: Hermes Desktop on Windows 10 (git-bash/MSYS)
**Model**: nemotron-3-ultra-free (opencode-zen)
**Terminal Status**: **BROKEN** — MSYS fork crash (exit 3221225794 / 0xC0000142)
**Browser**: WORKING — browser_navigate, browser_console, browser_click, browser_snapshot, browser_vision
**File Write**: **WORKS via execute_code (Python open())** — terminal and write_file tool fail, but execute_code file I/O is reliable
**Operating Tier**: **A** (full capability via execute_code workaround)

### Filled Probe Table (This Session)

| Capability | Status | Method | Fallback Used | Notes |
|---|---|---|---|---|
| Shell / code execution | **BROKEN** | terminal() | **execute_code + subprocess** | MSYS fork crash — use execute_code for ALL shell needs |
| Outbound network (PyPI) | **WORKS** | pip install via execute_code subprocess | N/A | yt-dlp + youtube-transcript-api installed successfully |
| yt-dlp | **WORKS** | execute_code subprocess.run([\"yt-dlp\", ...]) | N/A | Full metadata + auto-captions + descriptions extracted for 102 videos |
| youtube_transcript_api | NOT NEEDED | yt-dlp --write-auto-sub --sub-format json3 | N/A | yt-dlp's built-in caption download supersedes separate API |
| Browser automation | **WORKS** | browser_navigate + browser_console + browser_click | — | Channel recon, playlist structure, video list extraction |
| Vision / image understanding | AVAILABLE | browser_vision | — | Not used this session (transcripts sufficient) |
| Persistent file read/write | **WORKS** | execute_code (Python open()) | skill_manage write_file | execute_code file I/O is the primary reliable write path |
| Long-running / background | AVAILABLE | cronjob / terminal(background=true) | execute_code async | Not tested |

### Operating Tier Declaration

**Tier A — Full capability** (via execute_code workaround for broken terminal)

**Adaptations for this environment (Windows/MSYS with broken fork):**
- **Primary shell**: execute_code with subprocess.run() — replaces all terminal() calls
- **Primary file I/O**: execute_code with Python open() — replaces write_file tool
- **Package installs**: execute_code subprocess.run([\"pip\", \"install\", ...]) — works reliably
- **yt-dlp usage**: execute_code subprocess.run([\"yt-dlp\", \"--dump-json\", ...]) — 100% success rate for 102 videos
- **Transcript extraction**: yt-dlp --write-auto-sub --sub-format json3 --skip-download — no separate API needed
- **Browser**: Used for channel recon only (playlists, video list pagination) — not for per-video metadata
- **Persistence**: All raw data saved to disk via execute_code before any synthesis

### Key Workaround Discovered

**Windows/MSYS fork crash (0xC0000142) is bypassed entirely by execute_code**. The tool runs in a clean Python subprocess without the MSYS bash fork issue. This is now the **recommended primary approach** for this environment:

```python
# Pattern used throughout this extraction:
import subprocess, json, os

# Package install
subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)

# Metadata extraction
result = subprocess.run(["yt-dlp", "--dump-json", url], capture_output=True, text=True, timeout=120)
meta = json.loads(result.stdout)

# Transcript extraction (auto-captions in json3 format)
subprocess.run(["yt-dlp", "--write-auto-sub", "--skip-download", "--sub-format", "json3", "--sub-lang", "en", "-o", f"{outdir}/%(id)s.%(ext)s", url], timeout=60)

# File write (all raw data)
with open(f"{outdir}/{vid}.meta.json", "w") as f:
    json.dump(meta, f, indent=2)

# File read
with open(f"{outdir}/{vid}.meta.json", "r") as f:
    meta = json.load(f)
```

This pattern should be the default for Windows/MSYS environments in future extractions.
