---
name: yt-deep-extraction
description: "Deeply and losslessly extract everything from a YouTube channel, playlist, or video list — metadata, full transcripts, visuals, chapters, and the creator's actual claims — into per-video research files, a lossless cross-referenced master report, and an interactive HTML lesson. Use this whenever the user wants to learn from, archive, build a course from, mine knowledge/strategies out of, or turn into notes any YouTube channel or set of videos — even if they just say 'go through this channel' or 'learn everything from these videos' without using the words 'extract' or 'research.' Self-contained: does not depend on any other skill being installed. Built to run unmodified across different agent runtimes and model sizes, including small/free/local models with no vision and small context windows, and engineered to never fabricate a fact when a tool fails or data is missing — critical for personal and high-stakes research where fidelity to the source matters more than a complete-looking report."
version: 2.0.0
author: Hermes Agent
tags: [youtube, research, extraction, transcripts, vision, html, guide, pipeline, fidelity, model-agnostic, offline-capable]
platforms: [windows, linux, macos]
runtimes: [hermes, omp.sh/oh-my-pi, odysseus, claude, opencode-zen, any-agent-with-shell-or-browser-or-file-tools]
compatibility:
  minimum: "A model that can read/write text files. Everything above that (shell, browser, vision, package installs) is optional and detected at runtime — see Phase -1."
  degrades_gracefully: true
triggers:
  - deeply extract all data from this youtube channel
  - extract everything from this channel into a research document
  - learn everything from this youtube channel
  - turn this youtube channel into a comprehensive lesson
  - deep research this youtube channel
  - go through every video on this channel and build me notes
  - build a course/knowledge base from this creator's videos
---

# YouTube Deep Extraction Pipeline

## When to Use

Any time you need to deeply extract all knowledge, data, insights, visual material, and information from a YouTube channel or specific videos — producing individual per-video research files, a lossless master aggregation, and a polished interactive HTML lesson document that preserves every detail, faithfully and without invention.

This skill is topic-agnostic: it works the same way whether the channel is about quant finance, cooking, history, or anything else. Nothing about Phases 0–4 assumes a subject matter — only the *content* of the reports does.

---

## The Non-Negotiables (read this even if nothing else)

These six rules override every other instruction in this file if they ever conflict. They are short on purpose, so they survive even if a small model's context gets crowded out later in a long run.

1. **Never fabricate.** If a tool fails, a page won't load, or a fact can't be found, write that down as a failure or a gap. A blank or a "TOOL FAILURE" line is always correct; a plausible-sounding guess presented as fact is always wrong.
2. **Raw output hits disk before it hits prose.** Anything a tool returns (JSON, transcript, description) is saved to disk unmodified first. Reports are written by reading those files back, never by recalling what a tool "said" a few turns ago.
3. **Every claim cites its source** — a video ID/title plus a timestamp, or a raw file. No citation, no claim (unless it's clearly labeled as the agent's own synthesis).
4. **Tag confidence on everything**: `CONFIRMED` / `TRANSCRIBED` / `INFERRED` / `UNVERIFIED` / `MISSING`. See §Phase −1.4.
5. **Report what the creator said, not what you think of it.** Keep the creator's claims, opinions, and framing intact in source-derived sections, however you feel about them or however contested they are. Your own analysis goes only in clearly separated "Synthesis" subsections.
6. **Work in small, checkpointed steps and re-read from disk to resume** — never guess at prior progress from memory, and never assume the next phase can just be inferred; re-read the plan.

Everything below exists to make these six rules easy to execute in practice, across wildly different tools and model sizes.

---

## How to Call It

Replace `{CHANNEL_URL}` with the YouTube channel URL (handle or channel ID) — or a list of specific video URLs.
Replace `{OBJECTIVE}` with what you want to achieve (e.g. "learn professional quant trading", "build trading software", "archive everything this creator has said about X").
Replace `{SELECTION_STRATEGY}` with one of:
- `"targeted"` — deeply extract only videos relevant to the objective/context
- `"boundary-sweep"` — extract ALL videos from newest to oldest until hitting an out-of-context topic boundary
- `"all"` — extract everything regardless

```
Use yt-deep-extraction skill on:
Channel: {CHANNEL_URL}
Objective: {OBJECTIVE}
Selection Strategy: {SELECTION_STRATEGY}
```

If the caller doesn't specify a selection strategy, default to `"targeted"` and state that assumption explicitly in `_extraction-plan.md`.

---

## Reference Files

This skill ships with reference files in the `references/` and `assets/` directories that document real extraction sessions and reusable patterns. Load them with `skill_view(name="yt-deep-extraction", file_path="references/<filename>")`:

| File | What it covers |
|------|---------------|
| `assets/channel-overview.md` | Concrete example: Quant Guild channel reconnaissance result |
| `references/environment-probe.md` | Capability probe template + adaptations decision tree |
| `references/channel-recon.md` | Channel mapping and playlist structure reconnaissance |
| `references/notebook-extraction.md` | Extracting companion Jupyter notebooks from GitHub via browser |

These are living reference files — update them as new extraction patterns emerge.

---

## Reading This Skill on a Small-Context Model

If your effective context window is small (roughly under ~32K tokens — common on free/local models), do **not** try to hold this entire file in context for the whole run. Instead:

1. Read the **Non-Negotiables** and **Phase −1** once, at the very start of the run, and write a one-paragraph summary of them into `_environment.md` so you can re-derive them cheaply later without re-reading this whole file.
2. When you move to a new phase (0, 1, 2, 3, 4), re-read only that phase's section headed `## Phase N: ...` — the phases are written to be self-contained and don't require holding earlier phases' full text in context.
3. Treat on-disk files (`_environment.md`, `_extraction-plan.md`, `_numbers.md`, `raw/*`, `video-*.md`) as your real memory. Re-read them rather than trusting what you remember writing.
4. If you genuinely cannot execute the full pipeline (no shell, no persistence, tiny context) see **Phase −1.3, Tier D** for a degraded single-shot mode — it's a legitimate, explicitly-labeled fallback, not a failure.

---

## Phase −1: Environment & Model Adaptation Layer

Before any extraction work, spend one short step figuring out what you're actually working with, and write the results to `_environment.md`. This phase is fully self-contained — it does not require any other skill to be installed.

### −1.1 Capability Probe

Test each row below with the cheapest possible check, record the result, and note which fallback tier you'll operate in. Don't assume — different runtimes and different models within the same runtime vary wildly.

| Capability | Quick test | Primary method | Fallback 1 | Fallback 2 | If nothing works |
|---|---|---|---|---|---|
| Shell / code execution | run a trivial command | native shell/bash tool | Python REPL tool if separate from shell | — | Read-only mode: metadata comes only from pages you can fetch or the user pastes |
| Outbound network to package registries | `pip install --dry-run yt-dlp` or similar | pip/uv/npm install | check if `yt-dlp`/`ffmpeg` are already on PATH | vendored copy if the skill bundle ships one | Use a page-fetch or browser tool for raw HTML only; note reduced metadata fidelity |
| `yt-dlp` | `yt-dlp --version` | call directly | install via pip/uv/pipx (`--break-system-packages` if needed) | download a static release binary if binary-hosting domains are reachable | Fall back to browser DOM scraping for metadata |
| Transcript access | fetch one transcript | `youtube-transcript-api` (`pip install youtube-transcript-api`) | `yt-dlp --write-auto-sub --skip-download --sub-format vtt/json3` | browser: open the transcript panel and read/extract the DOM (e.g. reader-mode/`extract_readable`-style tools) | Mark transcript `MISSING`; extract only from description, chapters, comments |
| Browser automation | navigate to any URL | native browser tool (navigate/click/type/scroll/screenshot/evaluate) | a headless-automation library if code execution is available (Playwright/Puppeteer/Selenium) | — | Text-only pipeline: metadata + transcript + description only, no screenshots — say so in every affected report |
| Vision / image understanding | pass a screenshot to the model itself | native multimodal input | — (most free/local text models do not have this even when a browser tool exists) | — | Log every visual element as `UNVERIFIED (no vision)`; describe it only from surrounding transcript/description text, never invent what's on screen |
| Persistent file read/write | write a file, then read it back in a later step | native file tools | shell redirection/heredoc | in-memory for this turn only | If there's truly no persistence, skip the multi-file pipeline and produce one condensed report at the end — state this limitation up front |
| Long-running / background execution | check for an async/background/cron primitive | native background mode or scheduler | manual pattern: "re-run with the same output dir to resume" | — | Process fewer videos per invocation; rely entirely on the state file to pick up where you left off |

Write the outcomes as a short table in `_environment.md`, plus a one-line "operating tier" declaration (see −1.3).

### −1.2 Runtime Notes (informational — always trust the probe over this table)

These are current, observed tendencies as of this writing, not guarantees — tool surfaces change fast. Use them to guess where to look first, then confirm with the probe above.

| Runtime | Tends to have | Tends to lack / watch for |
|---|---|---|
| OpenCode (Zen free models: Big Pickle, Nemotron 3 Super/Ultra, MiniMax, MiMo, etc.) | Strong shell/file-edit tool use — great for driving `yt-dlp`/Python directly | Free models mostly lack vision; small free models often run 8K–32K context — plan for Tier C/D below by default |
| omp.sh / oh-my-pi (`omp`) | Native headless-browser automation (navigate/click/type/scroll/screenshot/evaluate/reader-mode extraction), subagents, background execution mode | Vision depends on whichever underlying model is configured, not on the harness — check per session |
| Odysseus | Shell/files/web/memory tools, MCP support, a built-in multi-step "Deep Research" module, can run fully local models | Local models on modest/no-GPU hardware can be slow and drop instructions mid-task — favor smaller chunks and more frequent checkpoints |
| Hermes | Cron/scheduling primitives (useful for the Autonomous Enrichment Loop below) | Verify browser + vision availability per deployment; don't assume |
| Anything else / unknown | — | Run the Capability Probe. It's cheap and it's the source of truth. |

### −1.3 Model-Tier Adaptation

Based on the probe results and how the model is actually performing (drifting off instructions, losing earlier context, timing out), declare one operating tier in `_environment.md` and follow its adaptations for the rest of the run. Re-declare it if conditions change mid-run (e.g. a rate limit appears).

- **Tier A — Full capability** (shell + browser + vision + comfortably large context): run the full pipeline exactly as specified in Phases 0–4.
- **Tier B — Strong text, no vision**: run the full pipeline, but every visual-registry entry is built from transcript/description/chapter context only, tagged `UNVERIFIED (no vision)`. Still take screenshots if a browser tool exists (they're useful to the human later), just don't describe their contents as if you'd seen them.
- **Tier C — Small context / weaker instruction-following** (typical small free/local models): shrink the unit of work.
  - Target 60–200 lines per video report instead of 100–500.
  - Process one video fully (fetch → save raw → write report → self-audit) before touching the next; don't try to hold several videos' data in context at once.
  - In Phase 2, merge video reports into the master report pairwise/sequentially rather than trying to synthesize all of them in one pass.
  - Re-read the relevant on-disk file before every subsection instead of trusting what's still "in view."
  - Prefer copying tool output straight into files over having the model retype it from memory (see Fidelity Protocol §1).
- **Tier D — No code execution / chat-only, or no persistence at all**: you cannot run the multi-file pipeline. Say so plainly, then do the best available version:
  - If the user can paste transcripts/descriptions, work from what they paste.
  - If only a page-fetch tool exists, use it for the video's page and description.
  - Produce a single well-organized conversational report instead of the file tree, and note explicitly which phases (visual capture, master aggregation, HTML lesson) were skipped and why.

### −1.4 The Fidelity Protocol

This is the operational core of the Non-Negotiables above. Apply it to every single unit of work, regardless of tier.

1. **Raw-First Persistence.** Before writing or synthesizing anything, save each tool's raw output to disk unmodified: `raw/{video_id}.meta.json`, `raw/{video_id}.transcript.<ext>`, `raw/{video_id}.description.txt`, `raw/{video_id}.screenshot-{timestamp}.png`. Every later phase reads from these files. Never rely on the model's memory of what a tool printed several turns ago — that's exactly where hallucination creeps in.
2. **Claim–Source Binding.** Every factual sentence in a report names where it came from: a video ID/title plus timestamp, or a `raw/` filename. No source, no claim in a source-derived section.
3. **No Retro-Citation.** Write the citation inline at the moment you write the claim — don't write a paragraph first and go back to add sources from memory afterward.
4. **Verbatim Quarantine.** When quoting the creator, copy the exact substring from the raw transcript file — pipe it, don't retype it from memory if the tool surface allows a direct copy.
5. **Confidence Tags.** Tag every extracted data point with exactly one of:
   - `CONFIRMED` — read directly from a successful tool call's raw output
   - `TRANSCRIBED` — read visually off a screenshot/frame (small transcription-error risk)
   - `INFERRED` — the agent's own synthesis or interpretation, not a literal source statement
   - `UNVERIFIED` — the tool partially worked or the result is ambiguous
   - `MISSING` — the data could not be obtained at all
6. **Tool-Failure Protocol.** If a tool call errors, times out, or returns empty/null, do not proceed as if it worked, and do not fill the gap with a plausible guess. Write `TOOL FAILURE: {tool} — {error text or "empty result"}` at that exact point, tag the field `MISSING`, and continue. This is the single most important rule for weak/free models, which are prone to quietly inventing data when a call fails silently.
7. **Numbers Ledger.** Every statistic, percentage, formula parameter, date, and count gets one line in `_numbers.md` with its confidence tag and source.
8. **Neutral-Scribe Rule.** Report what the creator said, claimed, showed, or argued — in their framing — even if it's opinionated, controversial, contested, or something the agent disagrees with or thinks is wrong. Don't soften, hedge, or moralize inside source-derived sections; that's editorializing, not extraction. The agent's own commentary, caveats, or disagreement belong only in clearly labeled "Synthesis" or "Notes" subsections. This applies regardless of the channel's subject matter — it's what makes the pipeline trustworthy for research that actually matters.
9. **Chunked Writing with Checkpoints.** Write in small, structurally bounded sections. After each one, re-read the relevant on-disk file before continuing — especially on Tier C/D models.
10. **Context-Loss Recovery.** If a session restarts or resumes, or you notice signs of having forgotten earlier instructions, re-read `_environment.md`, `_extraction-plan.md` (or `_loop_state.json` in cron mode), and the most recent report file from disk before doing anything else. Never guess at prior progress.
11. **Uncertainty Is Written, Not Resolved.** If something is ambiguous, contradictory, or unknown, write that down plainly instead of silently picking the "most likely" answer and presenting it as settled fact.
12. **Self-Audit Pass.** After each report, walk it once and check: does every non-Synthesis sentence have a citation; does every ledger figure have a confidence tag; does every failed tool call show up as `TOOL FAILURE` rather than silently-filled data? Fix anything that doesn't before moving on.

### −1.5 Browser-Only Fallback (When CLI/Terminal is Unavailable)

If the runtime's terminal/shell is non-functional (e.g. git-bash MSYS fork crash on Windows, sandbox restrictions, `uv pip install` exits 254), fall back to a **pure browser-based** extraction pipeline:

1. **Channel Recon**: `browser_navigate("{channel}/videos")` → scroll to load more → extract video list from `document.body.innerText`. Navigate to `{channel}/playlists` for content structure.
2. **Metadata**: `browser_navigate(video URL)` → expand description (click `"...more"` ref in snapshot) → extract full description from `document.body.innerText`, including chapters, timestamps, links, and resources.
   ### −1.5 Browser-Only Fallback (When CLI/Terminal is Unavailable)

   If the runtime's terminal/shell is non-functional (e.g. git-bash MSYS fork crash on Windows, sandbox restrictions, `uv pip install` exits 254), fall back to a **pure browser-based** extraction pipeline:

   1. **Channel Recon**: `browser_navigate("{channel}/videos")` → scroll to load more → extract video list from `document.body.innerText`. Navigate to `{channel}/playlists` for content structure.
   2. **Metadata**: `browser_navigate(video URL)` → expand description (click `"...more"` ref in snapshot) → extract full description from `document.body.innerText`, including chapters, timestamps, links, and resources.
      - **Reliable ytInitialData paths** (extract via `browser_console`):
        - Description: `window.ytInitialData.contents.twoColumnWatchNextResults.results.results.contents[1].videoSecondaryInfoRenderer.attributedDescription.content`
        - Chapters: `window.ytInitialData.engagementPanels[].engagementPanelSectionListRenderer.content[].macroMarkersListRenderer.contents[]` — each has `title.simpleText` and `timeDescription.simpleText`
   3. **Transcripts**: Click the `"Show transcript"` button. Button ref varies per page layout — use `browser_snapshot` first to find it. If unavailable, note transcript gap and extract what you can from description + metadata + screenshots.
   4. **Visual Data**: `browser_vision` for screenshots at chapter start times. If vision provider errors, share the screenshot path via `MEDIA:path` for the user to view.
   5. **Comments**: Scroll down → extraction via `document.body.innerText`.
   6. **File Output Fallback**: When `write_file` fails (often caused by a broken terminal fork), use `skill_manage(action='write_file', name='yt-deep-extraction', file_path='references/<name>.md', file_content='...')` to store outputs within the skill's directory, OR deliver inline in the chat.

   **Known limitation**: YouTube transcript button DOM selector is unreliable across page layouts. If clicking fails after 2 attempts, document transcript as `MISSING` and proceed.

   **Playlist URL Discovery**: On the channel's `/playlists` page, each playlist card has a "View full playlist" / "View full course" link. Click it, then read the URL from the browser address bar (format: `https://www.youtube.com/playlist?list=PL...`). The playlist ID is needed for direct navigation. Alternatively, extract playlist IDs from the page source via `browser_console` with a targeted query.

### −1.6 Windows/MSYS Terminal Workaround (Git-Bash Fork Crash)

On Windows with git-bash (MSYS), the `fork()` system call is broken, causing `write_file` and `terminal` tools to fail silently or with exit code 3221225794 (0xC0000142). This is a runtime environment issue, not a skill bug.

**Workaround** (tested and working):
1. Use `execute_code` with Python's native `open()` / `json.dump()` for all file I/O — this bypasses the broken shell fork entirely
2. For `yt-dlp` and other CLI tools, call via `subprocess.run()` inside `execute_code` instead of `terminal`
3. When `write_file` tool fails, use `skill_manage(action='write_file', name='yt-deep-extraction', file_path='references/<topic>.md', file_content='...')` as a scratch space — this writes to the skill directory and works even when the primary write mechanism fails
4. For final deliverables outside the skill directory (master reports, HTML), either:
   - Deliver inline in the chat response, or
   - Ask the user for an alternative output path they can access

**Key insight**: Python's `subprocess` works fine inside `execute_code`; it's only the direct shell/terminal tool that fails due to the MSYS fork bug. Structure all extraction logic as Python scripts run via `execute_code`.

---

## Phase 0: Setup & Channel Context Gathering

### 0.1 Channel Initial Reconnaissance

1. **Fetch channel metadata** (per the Capability Probe's chosen method for this run):
   - `yt-dlp --dump-json "https://www.youtube.com/{channel_url}"`, or
   - browser navigation + DOM extraction.
   - Save the raw output to `raw/_channel.meta.json` before writing anything derived from it.
   - Record: channel name, subscriber count, total videos, description, categories, related channels.

2. **Get the video listing with metadata**:
   ```bash
   yt-dlp --flat-playlist --dump-json "https://www.youtube.com/{channel_url}/videos" > raw/_channel.videos.jsonl
   ```
   This yields video IDs, titles, duration, upload dates, and view counts per video. Save the raw listing before processing it.

### 0.2 Automated Full-Channel Video Extraction (Reusable Script)

**Script location**: `scripts/quantguild_extractor.py` (within skill directory)

This Playwright-based script is the **recommended primary method** for full-channel extraction when `yt-dlp` is unavailable or when browser-only fallback is needed (Tier C/D). It works on any YouTube channel.

**Usage**:
```bash
# From skill's scripts/ directory
python quantguild_extractor.py --channel "@QuantGuild" --headless --max-scrolls 500 --scroll-pause 2.0
```

**Parameters**:
| Parameter | Description | Default |
|-----------|-------------|---------|
| `--channel` | Channel handle (e.g., "@QuantGuild") or full URL | Required |
| `--headless` | Run browser headless | False |
| `--max-scrolls` | Maximum scroll attempts | 500 |
| `--scroll-pause` | Pause between scrolls (seconds) | 2.0 |
| `--output-dir` | Output directory | quantguild_extraction/ |

**What it does**:
1. Navigates to `https://www.youtube.com/{channel}/videos`
2. Extracts initial video list from `window.ytInitialData` (immediate, no scroll needed)
3. Scrolls to bottom loading all videos (handles YouTube's infinite scroll)
4. Extracts metadata from DOM for any lazy-loaded items
5. Deduplicates by `videoId`
6. Outputs JSON + CSV with: `videoId`, `title`, `duration`, `views`, `date`, `link`

**Output files**:
- `{channel}_videos_{timestamp}.json` — full metadata
- `{channel}_videos_{timestamp}.csv` — spreadsheet-ready

**Integration with Phase 0**:
- Run this script **before** Phase 0.3 to get the complete video catalog
- Use its output to populate `_extraction-plan.md` queue
- Raw JSON output serves as `raw/_channel.videos.json` (equivalent to yt-dlp flat-playlist)

**Fallback for saved HTML**: If you can't run Playwright, save the channel page HTML and use `scripts/extract_ytinitialdata.py`:
```bash
python extract_ytinitialdata.py path/to/saved_channel_page.html
```
   **Critical**: The `/videos` endpoint only returns the first pagination batch (~100 videos). The channel root URL returns the complete catalog (all 353+ videos including Shorts). Save the raw listing before processing it.

   If yt-dlp fails or returns incomplete results, fall back to browser scrolling:
   - Navigate to `{channel_url}/videos` with `browser_navigate`
   - Scroll repeatedly with `browser_scroll` until video count matches the channel's stated total
   - Extract video IDs/URLs from `document.querySelectorAll('a[href*="/watch?v="]')`

3. **Categorize the channel's content** by analyzing video titles, descriptions, and tags across a representative sample (~50 videos, or all of them if the channel is small):
   - Main themes/topics
   - Skill progression (beginner → advanced), if any
   - Content categories (tutorials, theory, code builds, reviews, interviews)
   - Typical video length pattern and publishing frequency

### 0.2 Create Output Directory

```
~/{workspace}/yt-extraction-{channel-slug}/
```

Write `_environment.md` (Phase −1 results) and `_channel-overview.md` (channel metadata + content map — see the format below; keep this structure stable, since it's what later phases and any human reviewer will expect):

```markdown
# Channel Overview: {Creator Name} (@{handle})

## Channel Metadata
- Channel, Handle, URL, Joined date, Subscribers, Total Videos, Total Views, Location

## Channel Description
Verbatim, from raw metadata.

## Content Categories (from playlists/sections)
| # | Playlist/Category | Videos | Focus |

## Content Themes Identified
Numbered list.

## Extraction Strategy
- Objective, Strategy, First batch
```

### 0.3 Decompose by Selection Strategy

#### Strategy A: Targeted Extraction
- Identify which video categories/themes serve the user's objective.
- Select only videos from those categories.
- Create a prioritized extraction queue (most foundational → most advanced).

#### Strategy B: Boundary-Sweep Extraction
- Start from the **newest video**; extract fully, then move to the next oldest.
- Continue until a video's **primary topic** falls outside the stated objective's domain.
- Document the boundary decision (which video, why it's out of scope) with a citation to what made it out-of-scope.
- If there's a clear era shift in the channel, mark the transition point.

#### Strategy C: Complete Extraction
- Extract ALL videos from the channel.
- **Hard limits enforced by this skill**:
  - **Minimum**: 30 videos (if the channel has fewer than 30, extract everything available and note the small-channel constraint)
  - **Maximum**: 150 videos (if the channel has more than 150, prioritize the 150 most recent — or the most relevant per the objective if explicitly stated — and note the cap and why the cutoff was applied)
- Useful for archiving, complete knowledge bases, or channels in the 30–150 video range.

### 0.4 Write the Extraction Plan

Save as `_extraction-plan.md`:
- Total videos to extract, selection strategy used (and whether it was a default assumption)
- Ordered extraction queue (video title, URL, video ID, duration, priority)
- Estimated content volume per video, and the declared model tier from Phase −1.3 (this affects how you'll chunk Phase 1)

### 0.5 Automation Note for Future Runs

The script at `scripts/quantguild_extractor.py` is **generic** — it accepts any channel handle via `--channel`. For a new channel:
```bash
python scripts/quantguild_extractor.py --channel "@NewChannel" --headless --max-scrolls 500
```
This replaces manual `yt-dlp` calls and works in browser-only environments. The script is part of this skill and should be copied/adapted for any channel extraction.

---

## Phase 1: Per-Video Deep Extraction

For **each video** in the extraction queue, produce an individual research file: `video-{NN}-{slug}.md`. On Tier C/D, fully finish one video (through its self-audit) before starting the next.

### 1.1 Fetch Raw Metadata

```bash
yt-dlp --dump-json "https://youtube.com/watch?v={ID}" > raw/{ID}.meta.json
```
(or the browser-navigation fallback from Phase −1.1)

If this call fails, apply the Tool-Failure Protocol immediately — don't proceed to synthesis with partial/guessed metadata.

From the saved raw file, record in the report header: video ID, title, URL, upload date, duration, view/like/comment counts, channel name, full verbatim description, chapters (timestamps + titles), tags, heatmap (audience-retention peaks, if present), available caption languages, thumbnail URL, related videos linked in the description.

### 1.2 Fetch Full Transcript

```python
from youtube_transcript_api import YouTubeTranscriptApi
transcript = YouTubeTranscriptApi.get_transcript(VIDEO_ID)
```
Save the raw result to `raw/{ID}.transcript.json` (or `.vtt`) **before** writing any prose from it.

- If only auto-captions exist (no manual captions), note that explicitly.
- If no captions exist at all, apply the Tool-Failure Protocol: tag transcript `MISSING`, and extract what you can from metadata, description, and chapters alone.
- For long videos (roughly >30 min or whatever your Tier C/D chunk budget allows), don't load the whole transcript into context — read it off disk in sequential chunks (e.g. by line range or a fixed word count per chunk), writing the corresponding report section before moving to the next chunk.
- **Browser-only (Tier C/D) limitation**: The internal `get_transcript` API requires POST with a continuation token; `browser_console` cannot make network requests. The public `timedtext` endpoints (`/api/timedtext?v=ID&fmt=json3/srv3`) often return empty for videos without manual captions. If transcript extraction fails in browser-only mode, document as `TOOL FAILURE: transcript — browser-only POST blocked / timedtext empty`, tag `MISSING (browser-only)`, and proceed with description + chapters + metadata. Do not fabricate.

### 1.3 Visual Data Extraction (Key Frames)

Only attempt this at Tier A/B (browser tool available). At Tier C/D without a browser tool, skip this and say so.

Identify key visual moments to capture:
1. **Chapter markers** — navigate to each chapter start time, take a screenshot.
2. **Code/graph/simulation outputs** — whenever the presenter shows code, formulas, charts, or simulation results.
3. **Key diagrams or frameworks** — any whiteboard, slide, or diagram.
4. **Results/tables** — benchmark results, comparison tables, numerical outputs.
5. **Formula/equation screens** — mathematical derivations shown on screen.

Save each screenshot to `raw/{ID}.screenshot-{timestamp}.png`. For each one, document: timestamp, what it shows, why it's important, and any legible text/data (transcribed, tagged `TRANSCRIBED`).

- If vision isn't available (Tier B), still capture and save the screenshot for the human's later use, but describe its content only from surrounding transcript/description context, tagged `UNVERIFIED (no vision)` — never assert what's pixel-visible.
- If `browser_vision`-equivalent tooling fails or is unavailable entirely, apply the Tool-Failure Protocol and extract as much as possible from transcript + description alone.

### 1.4 Synthesize Video Content

Produce a structured analysis for each video:

#### Header
```markdown
# Video {NN}: {Title}
- **URL**: https://youtube.com/watch?v={ID}
- **Uploaded**: {date} | **Duration**: {MM:SS}
- **Views**: {N} | **Likes**: {N}
- **Chapters**: {N}
```

#### Metadata Summary
Channel, description excerpt, categories, tags, heatmap peaks — each with its confidence tag.

#### Transcript-Derived Content
Organize by chapter/topic shift (use YouTube's chapters as natural section dividers):

```markdown
## [00:00 – 04:44] Chapter: {Chapter Title}

### Key Claims / Knowledge
- Bullet-point knowledge items, each with a [TIMESTAMP] reference and confidence tag
- Formulas rendered as LaTeX or inline math
- Definitions and core concepts, in the creator's own framing

### Data Points & Statistics
As recorded in the numbers ledger, with the same tags.

### Code / Techniques Shown
- Libraries used, parameters, key implementation details — tagged per §1.3/1.4 above

### Visual Elements
- Description of graphs/simulations shown, what they demonstrated, parameter ranges used
```

#### Visual Elements Registry
Every graph, chart, diagram, or simulation: timestamp, type, what it shows, key visible features, data ranges/notable patterns — each entry tagged.

#### Key Takeaways
- Core argument/thesis of the video, in the creator's terms
- Actionable techniques or insights the creator presented
- Connections to other videos in the channel

Add a clearly separated **### Synthesis / Agent Notes** subsection at the end for anything that's the agent's own interpretation, critique, or connective analysis — keep this fully out of the sections above.

### 1.5 Write and Audit the Per-Video Report

Save as `video-{NN}-{slug}.md`. Length target depends on tier (100–500 lines at Tier A/B, 60–200 at Tier C), video length, and density.

Run the Fidelity Protocol's Self-Audit Pass (§−1.4.12) before moving to the next video:
- Does every claim have a timestamp or raw-file citation?
- Does every referenced value appear in `_numbers.md` with a tag?
- Are transcript quotes copied verbatim from the raw file?
- Does every failed tool call appear as `TOOL FAILURE`, not silently-filled data?

---

## Phase 2: Master Aggregation

After all planned per-video reports are complete (or, in cron mode, after each new batch):

### 2.1 Read All Reports
Re-read every `video-{NN}-*.md` file from disk — don't rely on memory of writing them.

### 2.2 Produce `master-report.md`
A lossless, cross-referenced aggregation of the channel's knowledge, organized by **concept**, not by video. On Tier C/D, build this incrementally: merge one new video report into the existing master report at a time, rather than attempting to synthesize everything in a single pass.

Structure:

#### Executive Summary
Channel overview, total videos extracted, thematic organization.

#### Thematic Knowledge Sections
For each major theme identified in Phase 0:
1. Core Concepts & Definitions
2. Mathematical/Technical Framework (formulas, derivations, equations — as applicable to the subject matter)
3. Methodology / Parameters (code patterns, library usage, parameters, techniques)
4. Key Results & Visualizations (with per-video cross-references)
5. Practical Techniques & Workflows
6. Tools & Resources named (versions, usage patterns)
7. Pitfalls & Warnings (what the creator advises against)
8. Progression Path (recommended learning order across videos)

#### Numbers & Statistics Ledger
Full `_numbers.md`: every statistic, percentage, parameter, duration, and metric from every video, with source references and confidence tags.

#### Visual Catalog
Every visual element across all videos, organized by category (chart types, simulation/diagram types, code patterns), each with its confidence tag.

#### Cross-Reference Table
| Concept | First Introduced | Deepest Coverage | Related Videos |
|---------|-------------------|-------------------|-----------------|

#### Knowledge Gap Analysis
- Topics covered shallowly vs. deeply
- Prerequisites the channel assumes
- External resources the creator recommends
- Any `MISSING`/`TOOL FAILURE` entries that limit completeness — be explicit about what's absent and why, not just what's present.

### 2.3 Preserve EVERY Detail
The master report is **lossless** — nothing from any per-video report is omitted, and nothing is silently smoothed over. Every formula, parameter, data point, code excerpt, and insight appears somewhere in the master report. Use cross-references like `[VIDEO-03 §4.2]` to point back to the original video report for full context, and keep confidence tags intact through the merge — don't let an `UNVERIFIED` item quietly become presented as `CONFIRMED` once it's aggregated.

---

## Phase 3: Interactive HTML Lesson Document

Transform `master-report.md` into a single self-contained interactive HTML document. Skip this phase entirely at Tier D (no persistence/no code execution) and say so.

### 3.1 Design Rules

- **Visual–Text Coupling** — every visual (chart, formula card, screenshot, diagram) sits directly adjacent to the text that discusses it, not in a disconnected gallery at the end. If a reader has to scroll away from the discussion to find the visual it's about, it's in the wrong place.
- **Full-Fidelity Requirement** — nothing from `master-report.md` is dropped for space. If a section is long, make it collapsible/expandable rather than cutting it; every master-report section needs an HTML home.
- **CSS Architecture** — one self-contained file, CSS custom properties (`--variables`) for color/spacing/typography rather than repeated inline styles, no external dependencies beyond what's explicitly allowed by the runtime, and layouts that work at both desktop and narrow/mobile widths.
- **No fabricated polish** — don't invent chart data, screenshots, or numbers to make a section look more complete than the source material actually was; a `MISSING`/gap note rendered honestly is better design than a fabricated-looking placeholder.

#### Structure
1. **Hero** — channel name, subscriber count, video count, extraction scope, high-level summary stats.
2. **Channel Overview** — what the channel covers, skill progression, content map.
3. **Thematic Modules** — one section per major theme: concept explanations (synthesized across videos), formulas rendered as styled HTML (not images), visual registry with video cross-references, code patterns in monospace blocks.
4. **Video Catalog** — full listing of extracted videos with chapter breakdowns and click-to-expand detail.
5. **Quantitative Data** — the numbers ledger as tables/stat callouts, with confidence tags visible or filterable.
6. **Navigation** — sticky table of contents, theme jump-links, search.
7. **Methodology Panel** — extraction approach, limitations, source quality notes, and an honest accounting of every `MISSING`/`TOOL FAILURE` item.

#### Interactive Components (include at least 3)
1. Video Catalog Tabs — filter by theme, difficulty, or series.
2. Formula Cards — expandable, showing derivation, parameters, and video context.
3. Concept Network — clickable tag clusters showing connections between videos.
4. Cross-Reference Browser — searchable table of every concept mapped to videos.
5. Timeline Explorer — publishing timeline, color-coded by theme.

#### Verification
1. Re-read `_numbers.md` and verify every value appears in the HTML.
2. Section cross-check: every master-report section has a corresponding HTML section.
3. Spot-check 5 random claims back to their source video/raw file.
4. Verify the HTML actually renders (browser tool if available; otherwise a static structural check — see Phase 4.2).

### 3.2 File Architecture

```
{output-dir}/
  _environment.md
  _channel-overview.md
  _extraction-plan.md
  _numbers.md
  _loop_state.json          (cron mode only)
  raw/
    _channel.meta.json
    _channel.videos.jsonl
    {ID}.meta.json
    {ID}.transcript.<ext>
    {ID}.description.txt
    {ID}.screenshot-{timestamp}.png
  video-01-{slug}.md
  video-02-{slug}.md
  ...
  master-report.md
  lesson.html
```

---

## Phase 4: Verification & Delivery

### 4.1 Fidelity Audit
1. Re-read `_numbers.md` — every value in the HTML must exist in the ledger with a matching tag.
2. Count: number of videos extracted = number of `video-*.md` files = number of entries in the extraction plan (accounting for any explicitly-skipped ones).
3. Section cross-check: every master-report section has an HTML equivalent.
4. Spot-check: random claims in the HTML trace back to the original video report and its `raw/` file.
5. Count `TOOL FAILURE` and `MISSING` occurrences across all reports; make sure this count is reflected honestly in the Methodology Panel — a clean-looking report with zero gaps on a long, messy extraction run is itself a red flag worth double-checking.

### 4.2 Rendering Audit
If browser tools are available: navigate to the HTML, click interactive features, verify layout and any dark-theme/emoji rendering.
Without visual tools: static fallback — check tag balance, verify UTF-8/emoji didn't get double-escaped, confirm the file opens without console errors if any execution tool is available.

### 4.3 Deliverables Summary

| File | Description |
|------|-------------|
| `_channel-overview.md` | Channel metadata and content map |
| `_extraction-plan.md` | Extraction queue and strategy |
| `_numbers.md` | Complete statistics ledger with confidence tags |
| `raw/*` | Unmodified tool output — the ground truth everything else is built from |
| `video-{NN}-{slug}.md` | Per-video deep extraction (one per video) |
| `master-report.md` | Lossless, cross-referenced aggregation |
| `lesson.html` | Interactive HTML lesson document |

---

## Autonomous Enrichment Loop (Cron / Scheduled Mode)

When the user wants this to run as a recurring job for continuous enrichment:

### Architecture

Run every 1–6 hours (or whatever cadence the runtime supports). Each iteration executes ONE action from the cycle below, updating `_loop_state.json`.

| # | Phase | Action |
|---|-------|--------|
| 0 | Watch for New Videos | Check the channel for uploads since the last check. If found, add to the queue at highest priority. |
| 1 | Extract Next Queued Video | Run Phase 1 on the next unprocessed video. |
| 2 | Visual Enrichment | For already-extracted videos lacking screenshots (and where a browser tool is available), capture key frames. |
| 3 | Cross-Reference Audit | Verify all cross-references in `master-report.md` are still consistent. |
| 4 | Deep Enrichment | For the least-dense video report, add 2–3 more detail dimensions. |
| 5 | Missing-Data Sweep | For videos where transcript/metadata was `MISSING`, retry with an alternate method (different language, alternate tool). |
| 6 | Rebuild Master Report | Regenerate `master-report.md` from all video reports. |
| 7 | Rebuild HTML | Regenerate `lesson.html`, verify it, deliver an update notification. |

### State File (`_loop_state.json`)
```json
{
  "version": 1,
  "channel_url": "...",
  "total_iterations": 0,
  "action_cycle_position": 0,
  "videos_extracted": [],
  "videos_queue": [],
  "last_check_date": "2026-01-01",
  "next_video_index": 5,
  "html_version": 1,
  "tool_failure_count": 0,
  "current_phase": "watch_new"
}
```

### Scheduling — use whatever your runtime provides

This skill doesn't assume a specific scheduler. Pick the mechanism the Capability Probe found:
- **Hermes**: native cron primitive, e.g. `hermes cron create --name "yt-enrich-{slug}" --schedule "every 2h" --prompt "Run yt-deep-extraction enrichment loop on {CHANNEL_URL} in {OUTPUT_DIR}. Read _loop_state.json, execute next phase, update state." --skills yt-deep-extraction`
- **omp.sh**: background mode (e.g. `/background`) plus an external OS-level cron/systemd-timer calling the same prompt.
- **Odysseus**: its scheduled-agent-task feature, pointed at the same prompt.
- **Anything else**: fall back to an OS-level cron/Task Scheduler entry that re-invokes the agent with the same prompt and output directory; the state file is what makes this safe to interrupt and resume.

---

## Known Pitfalls

1. **Transcript unavailability** — some videos have no captions at all. Document this and extract what you can from metadata + visual data + description alone.
2. **Long video transcripts** — videos >60 min produce very large transcripts. Process in overlapping chunks read from disk, not from context memory.
3. **Channel pagination** — YouTube channels may require scrolling/pagination to load all videos. Prefer a flat-playlist/CLI listing method over manual scrolling when available.
4. **Visual extraction limits** — browser/vision tools may fail on CAPTCHA, age-restricted, or private videos. Note the failure (Tool-Failure Protocol) and proceed.
5. **Emoji/unicode in file writes** — on runtimes where the write tool double-escapes unicode, prefer a code-execution write (e.g. Python `open()`) for the HTML file, or apply a repair pass afterward.
6. **Channel boundary detection** — for boundary-sweep strategy, document the "out of context" threshold clearly. If a video is ambiguous, extract it anyway and note the ambiguity rather than silently excluding it.
7. **Video ordering drift** — YouTube may reorder listings over time. Always reference by video ID, not by position in a playlist.
8. **Context window limits** — for large channels (50+ videos), process in small batches, documenting progress in the state file regardless of whether you're in cron mode.
9. **Transcript API failures** — the primary transcript method may fail for some videos even when captions exist. Fall back through the chain in the Capability Probe rather than giving up after one method.
10. **Browser/playback rate limits** — extended browser automation against YouTube may hit rate limits. Rest between extractions if you see this.
11. **Silent-fabrication-on-failure** — the single highest-risk failure mode for smaller/free models: when a tool call fails, they sometimes produce a plausible-looking transcript, statistic, or description anyway rather than reporting the failure. This is exactly what the Tool-Failure Protocol (§−1.4.6) exists to prevent — if you notice yourself doing this, stop and go back to write the failure explicitly instead.
12. **Local-hardware slowness** — on self-hosted runtimes running local models on modest or GPU-less hardware, inference can be slow enough that long multi-step reasoning fails partway through. Favor the Tier C adaptations (§−1.3) by default in these environments even if the probe suggests more capability is technically available.
13. **Package-install sandboxing** — some runtimes restrict outbound network access to a fixed allowlist that doesn't include PyPI/npm. If `pip`/`uv`/`npm` installs fail for this reason, don't retry indefinitely — fall back to whatever's already on PATH or to the browser method, and note the constraint in `_environment.md`.
14. **Broken terminal environments (Windows/MSYS)** — on Windows with git-bash (MSYS), the `fork()` system call is broken, causing `write_file` and `terminal` tools to fail silently or with exit code 3221225794 or 0xC0000142. Workaround: use `skill_manage(action='write_file', name='yt-deep-extraction', file_path='references/<topic>.md', file_content='...')` to save data within the skill directory. For output files outside the skill (master reports, HTML), deliver inline or ask the user for an alternative output path.
15. **browser_console character limits** — large outputs (full notebook JSONs, long transcripts, base64 PNG data) may be truncated at ~4–12K characters. Fetch in chunks, extract only relevant portions via targeted queries, or use `fetch()` with `Blob.text()` to get the full payload.
16. **Notebook companion extraction** — when a video references a Jupyter notebook on GitHub: navigate to the raw JSON URL (`raw.githubusercontent.com/...`) and extract cells programmatically via `JSON.parse(document.body.textContent).cells`. Output cells containing plots are base64-encoded PNGs that exceed console limits — extract `text/plain` and `text/html` representations instead.
17. **Skill directory as scratch space** — when no other write mechanism works, use `skill_manage(action='write_file', ...)` with `file_path: references/` for interim outputs. This works even when the `write_file` tool fails. Clean up reference files after the extraction is complete.
18. **yt-dlp `/videos` endpoint pagination limit** — `yt-dlp --flat-playlist "https://www.youtube.com/@handle/videos"` only returns the first pagination batch (~100 videos). To get the complete catalog including Shorts, use the channel root URL: `yt-dlp --flat-playlist "https://www.youtube.com/@handle"` (without `/videos`). This returns all 353+ videos in a single JSONL dump. If the channel URL fails, fall back to browser scrolling on the `/videos` page until the count matches the channel's stated total.

19. **Browser-only transcript extraction is severely limited** — In Tier C/D (browser-only, no shell), the YouTube internal transcript API (`/youtubei/v1/get_transcript`) requires a POST request with a continuation token, which `browser_console` cannot make due to browser security policies. The public `timedtext` endpoints (`/api/timedtext?v=ID&fmt=json3/srv3`) frequently return empty responses for videos without manual captions. **Result**: In browser-only mode, transcripts are often `MISSING` even when captions exist. Mitigations: (a) Use the `quantguild_extractor.py` Playwright script (which can intercept network requests) for full-channel extraction; (b) If a transcript is critical, note it as `MISSING (browser-only limitation)` and extract maximum info from description + chapters + metadata; (c) Do not fabricate transcript content — a documented gap is always correct, a fabricated transcript is always wrong.

---

## What Changed in v2.0

For anyone comparing against the earlier draft of this skill:

- **Fully self-contained.** Phase −1's capability probe and the fidelity protocol used to be inherited by reference from a separate `aggregate-deep-research` skill. That's now inlined here in full, so this file works standalone on any runtime, even one where that other skill was never installed.
- **Raw-First Persistence** (§−1.4.1) is new and is probably the single biggest fidelity improvement: tool output is saved to disk before any prose is written, so reports are built by reading files back rather than by a model "recalling" what a tool said several turns earlier — the most common source of drift on weaker models.
- **Tool-Failure Protocol** (§−1.4.6) is new: an explicit instruction to write failures down rather than silently substituting plausible-looking invented data, which is a well-documented failure mode for smaller/free models under tool uncertainty.
- **Confidence tagging** (`CONFIRMED`/`TRANSCRIBED`/`INFERRED`/`UNVERIFIED`/`MISSING`) is new — a small, closed vocabulary that's easy for weak models to apply consistently, replacing vaguer "note the uncertainty" prose instructions.
- **Neutral-Scribe Rule** (§−1.4.8) is new: keeps the creator's original claims and framing intact in source-derived sections regardless of subject matter, with the agent's own analysis clearly quarantined to "Synthesis" subsections — important for research where fidelity to the source matters more than a smoothed-over summary.
- **Model-Tier Adaptation** (§−1.3) is new: concrete, different behavior for Tier A (full capability) through Tier D (chat-only, no persistence), instead of one pipeline assumed to fit every model.
- **Runtime Notes** (§−1.2) is new: a quick-reference, explicitly-hedged table of what's typically available on Hermes, omp.sh/oh-my-pi, Odysseus, and OpenCode Zen's free models, to speed up the capability probe without replacing it.
- **Low-context reading mode** is new: guidance on reading this file section-by-section rather than all at once when the model's context is small.
- **Browser-Only Fallback** (§−1.5) and pitfalls 14–17 were added from real-world Windows/MSYS/Mac testing where terminal and write_file tools fail for reasons unrelated to the skill's logic.
- **Reference Files section** added: directs users to load concrete extraction examples from `assets/` and `references/` via `skill_view()`.
