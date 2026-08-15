# Environment Probe Results

## Capability Probe

| Capability | Test Result | Primary Method | Fallback Used |
|---|---|---|---|
| Shell / code execution | ❌ FAILED (MSYS fork crash on Windows) | native terminal | execute_code (Python subprocess) |
| Outbound network (PyPI) | ❓ UNKNOWN | pip/uv install | N/A - not tested |
| yt-dlp | ❌ NOT TESTED | direct call | N/A - terminal broken |
| youtube-transcript-api | ❌ NOT TESTED | pip install | N/A |
| Browser automation | ✅ WORKING | native browser_navigate/snapshot/click/console | — |
| Vision / image understanding | ❌ NOT AVAILABLE | native multimodal | — |
| Persistent file read/write | ❌ FAILED (write_file broken on MSYS) | native file tools | skill_manage write_file to skill refs/ |
| Long-running background | ❓ UNKNOWN | native background | N/A |

## Operating Tier Declaration

**TIER C — Small context / weaker instruction-following + browser-only fallback**

Adaptations in effect:
- Processing one video fully (fetch → save raw → write report → self-audit) before next
- Target 60–200 lines per video report
- Reading from disk (skill refs) before each subsection
- Master report built incrementally (pairwise merge)
- Visual registry entries tagged `UNVERIFIED (no vision)`
- Transcript extraction via browser DOM only; marked `MISSING` if unavailable

## Key Constraints

- Windows git-bash (MSYS) `fork()` broken → `write_file` and `terminal` tools fail with exit code 3221225794 (0xC0000142)
- Workaround: all file I/O via `execute_code` (Python `open()`/`json.dump()`) or `skill_manage(action='write_file')` to skill references directory
- Browser console `ytInitialData` extraction works reliably for metadata, description, chapters
- YouTube transcript panel: "Subtitles/closed captions unavailable" on this video → transcript `MISSING`