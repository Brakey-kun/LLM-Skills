---
name: context-resume
description: Loads a context-handoff export (a handoff.md / handoff.json / *-handoff.zip produced by the context-handoff skill) at the start of a new conversation so work can continue with full prior context instead of starting cold or asking the user to re-explain everything. Use this whenever the user uploads or references a file named like "*-handoff.zip", "handoff.md", or "handoff.json", says things like "resume this conversation," "continue from this handoff," "load this context," or "here's where we left off," or shares a project handoff file at the start of a session. Always run this before doing any requested work in that conversation, not after.
---

# Context Resume

The receiving-end counterpart to `context-handoff`. Its job is to load a handoff package correctly — respecting its coverage limits and settled decisions — rather than treating it as loose background reading.

## Workflow

### 1. Locate and read the files

Prefer the zip if present; unzip it, then read `handoff.json` first (canonical), then `handoff.md` (human-readable view — cross-check, but JSON wins on any disagreement per the handoff schema).

A handoff is commonly given as just `handoff.md` + `handoff.json` **without** the zip — this is a deliberate "light handoff" choice (see `context-handoff`'s SKILL.md), not a mistake, and it's a complete, usable handoff on its own. In that case:
- Load and follow the two files exactly as normal.
- Any `[file: uploaded]` / `[file: generated]` entries are records that a file existed, not files you have access to — note this plainly if the upcoming task would actually need that file's real content, and ask the user for the zip (or the file directly) at that point rather than proceeding as if the content were available.
- If only a bare `.md` or `.json` was shared (not even the pair), work from what's available and note that the other wasn't provided.

### 2. Read the usage-instructions preamble first, and actually follow it

Before touching the transcript itself:
- Treat the settled-decisions list as closed. Don't re-ask about or silently override anything on it.
- Treat the open-questions list as genuinely open — surface these to the user early rather than guessing at them.
- Note the coverage scope (full vs. partial, and from which turn). If coverage is partial, this changes how confidently you can speak about anything from before the capture starts — say so rather than implying full knowledge of the original conversation.
- Note that any token counts in the file are estimates, not authoritative — don't restate them as exact figures.

### 3. Internalize the transcript

Walk `turns` in order, reconstructing what happened using the block types (`thought`, `tool_call`, `tool_result`, `skill`, `answer`, `file`) in their recorded `order`. Files referenced under `assets/` are real — read them if the upcoming task needs their actual content, don't work from the filename alone.

### 4. Confirm before proceeding

Give the user a short summary before starting any new work: how many turns were loaded, the coverage caveat in plain language, and the open-questions list. This is the checkpoint where a bad or corrupted handoff gets caught immediately instead of quietly propagating into new work. Something like:

> Loaded the handoff — 14 turns, full coverage, generated Aug 14. Two open items carried over: [x], [y]. Ready to continue — want me to pick up on [y] first, or something else?

Keep this brief; it's a confirmation, not a re-summary of the whole conversation back at the user.

### 5. Proceed

Once confirmed (or if the user just says "go ahead"), continue the work using the loaded context as if it were native conversation history — cite specifics from it naturally rather than re-deriving conclusions it already contains.

## Failure handling

- **Malformed or partial file** (JSON doesn't parse, zip is missing expected members): say exactly what's broken and what you *could* still read, rather than silently working from a corrupted partial parse.
- **JSON/Markdown disagreement**: follow JSON, but mention the discrepancy if it's substantive enough to matter for the task at hand.
- **No usage-instructions block found** (e.g., a hand-edited or foreign-format file): don't assume the ground-truth/don't-relitigate rules apply — ask the user how much weight to give the file's contents instead of guessing.
