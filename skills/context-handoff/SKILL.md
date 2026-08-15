---
name: context-handoff
description: Exports the current conversation into a lossless, structured handoff package (Markdown + JSON + bundled files, zipped) so a new conversation — with Claude or any other AI — can continue with full, accurate context instead of a re-derived summary. Use this whenever the user asks to "export," "hand off," "save context," "continue this in a new chat," "summarize for a teammate," or wants to preserve/share this conversation before it's lost. Also proactively OFFER this (don't run it unasked) whenever a long_conversation_reminder appears, the conversation is clearly running very long, or the user mentions running low on context/usage — losing unsaved context is exactly the failure mode this skill exists to prevent, so err toward suggesting it. Trigger even if the user just says something like "I'm about to run out of space" or "I need to move this to a new chat."
---

# Context Handoff

Turns the live conversation in Claude's own context window into a portable handoff package: a human/AI-readable Markdown transcript, a canonical JSON record, and a zip bundling any real files/images that were part of the conversation. The design goal is **losslessness within the bounds of what's actually still in context** — and total honesty about where those bounds are.

Read `references/schema.md` before producing output — it defines the exact block grammar and JSON schema. Don't improvise a different structure.

## Core principle: capture what's real, disclose what isn't

This skill runs *inside* a live conversation, so it can only ever see what's currently in context. It cannot recover turns that scrolled out of the window or were summarized away before this skill ran. That's a hard limit, not a bug — and the output must say so explicitly rather than presenting a partial capture as if it were complete. This honesty is the entire reason a companion browser-extension capture tool (external, DOM/network-level) is planned as a separate, later project: it exists specifically to cover conversations *after* this in-context method can no longer see the whole thing.

## Workflow

### 1. Determine scope

Default to the entire conversation currently visible in context. If the user specifies a range ("just the last part," "from where we started X"), honor that instead. Either way, state the scope explicitly in the output.

### 2. Walk the conversation turn by turn, in order

For each turn, extract, in the order they actually occurred:

- The user's prompt (verbatim — don't paraphrase the user's own words).
- Every distinct block of Claude's turn, tagged per `references/schema.md`'s block grammar: `[thought]`, `[tool_call: name]`, `[tool_result: name]`, `[skill: name]`, `[file: uploaded|generated]`, and the final `Answer:`.
- Preserve the *actual order* blocks occurred in — don't group all tool calls together or all thoughts together if they were interleaved.

If a block type is known to have happened (e.g., you know a tool was called) but its content isn't recoverable from context, still list it with a `[not visible in context]` note rather than silently omitting it — an acknowledged gap is far better than an invisible one.

### 3. Bundle real files, don't just describe them

For every file mentioned in the conversation — user uploads, generated artifacts, images, downloaded outputs — copy the actual file into an `assets/` folder in the export (from `/mnt/user-data/uploads` and `/mnt/user-data/outputs` as appropriate) and reference it by relative path in the Markdown and JSON. Only fall back to a text description when the actual file genuinely isn't recoverable (e.g., it was never saved to disk). This is the direct equivalent of "image-based capture" from the original extension concept: prefer the real artifact over a text summary of it whenever one exists.

### 4. Compute honest stats

- Message counts (user turns, Claude turns) are exact.
- Token counts are NOT exact — Claude has no access to real API token counts client-side. Compute a rough estimate (roughly `words × 1.3`) and label it clearly as an estimate, every time it appears. Never present an estimated number as if it were authoritative.

### 5. Redact obvious secrets

Scan extracted text for common secret patterns (API key prefixes like `sk-`, `ghp_`, `AKIA`, bearer tokens, etc.) and replace matches with `[REDACTED: likely <type>]`. Report a count of redactions performed at the top of the output. This is a heuristic safety net, not a guarantee — say so.

### 6. Write the usage-instructions preamble

Every export starts with a preamble addressed directly to whatever AI reads the file next. Don't skip or shorten this — it's the difference between a handoff and a transcript dump. See `references/schema.md` for the exact required content (treat-as-ground-truth rule, don't-relitigate-settled-decisions rule, open-questions list, coverage caveat restated). Adjust its emphasis slightly by handoff purpose if the user states one (continuing the same task solo vs. onboarding a teammate vs. sharing across a project) — but never omit the core rules.

### 7. Assemble and package — always present all three separately

Write, in a working folder named after the conversation:
- `handoff.md` — the full annotated transcript with the preamble at the top.
- `handoff.json` — the canonical structured record (schema in `references/schema.md`). If the two ever disagree, JSON is the source of truth; say so in the Markdown.
- `assets/` — bundled files from step 3.

Then run `scripts/package_handoff.py <folder>` to zip everything into `<conversation-name>-handoff.zip`.

**Present all three as separate, independently downloadable deliverables — never only the zip.** `handoff.md` and `handoff.json` together are a complete, self-sufficient handoff: a new conversation can be given just those two files and have everything needed to continue accurately (full transcript, structured data, settled decisions, open questions, coverage caveats). The zip is an *additional*, opt-in upgrade for when the user also wants the real bundled files/images for full lossless accuracy — not a requirement to make the handoff usable.

This gives the user a real choice at handoff time:
- **Light handoff** (`handoff.md` + `handoff.json` only): smaller, faster to attach, conserves context in the new conversation — the right default when the original files/images aren't needed for the next task.
- **Full handoff** (add the zip): needed when the next task actually requires the real files/images themselves, not just their record of having existed.

State this choice explicitly to the user when presenting the output — don't make them infer it from which files happen to be attached.

## Proactive offering

When a `long_conversation_reminder` fires, or the conversation has clearly grown very long, or the user signals they're near a usage/context limit: mention, briefly and once, that you can generate a handoff export now while full context is still available, and ask if they'd like that. Don't repeat the offer if they decline. Don't run the export unprompted — only offer it.

## What this skill does not do

- It doesn't reach outside the current context window — no browser access, no re-fetching earlier deleted turns.
- It doesn't guarantee tool-call inputs/outputs are complete if they were large and got truncated in context — flag truncation where you can detect it (e.g., an obviously cut-off block) rather than silently presenting truncated content as whole.
- It doesn't replace the companion `context-resume` skill on the receiving end — that skill governs how the file should actually be *loaded*, this one only governs how it's *produced*.
