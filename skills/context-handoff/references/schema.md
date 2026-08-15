# Handoff Format Specification

This is the canonical grammar for both output files. Follow it exactly — don't invent alternate tags or reorder sections. If you need a block type not listed here, use the closest existing one rather than adding a new tag ad hoc.

## Markdown transcript (`handoff.md`) structure

```
# Conversation Handoff: <conversation name or short descriptive title>

## Usage Instructions for the Receiving AI
<preamble — see "Usage-instructions preamble" below, verbatim structure>

## Metadata
- Scope: <full | partial — from turn N, because ...>
- Turns: <user turn count> user / <claude turn count> claude
- Tokens (estimated): user ~<a>, claude ~<b>  — *estimated from word count, not authoritative*
- Redactions applied: <count> (<types>)
- Generated: <ISO 8601 timestamp>
- Source: <provider/model if known, e.g. "Claude, this conversation">

## Transcript

### Turn <n>
**User:** <verbatim prompt>

**Claude:**
[thought] <reasoning text, or "not visible in context">
[tool_call: <name>] <key parameters, not a full raw dump unless short>
[tool_result: <name>] <summarized result; note if truncated>
[skill: <name>] <what it was invoked for>
[thought] <more reasoning, if interleaved — preserve real order>
**Answer:** <final user-visible response text>
[file: uploaded] <filename> → `assets/<filename>`
[file: generated] <filename> → `assets/<filename>`

### Turn <n+1>
...
```

Block-tag grammar (use exactly these tags, lowercase, square brackets):

| Tag | Meaning |
|---|---|
| `[thought]` | Extended thinking / reasoning text, if present in context |
| `[tool_call: name]` | A tool invocation, with the parameters actually used |
| `[tool_result: name]` | The result returned, summarized if long, noted if truncated |
| `[skill: name]` | A named skill that was consulted/applied |
| `[file: uploaded]` / `[file: generated]` | A real file involved in this turn, bundled into `assets/` |
| `**Answer:**` | The final text actually shown to the user for that turn (not a block tag — always rendered this way, bolded, to stand out from the tagged blocks) |

If a block type happened but its content isn't recoverable, still emit the tag with `[not visible in context]` as the content — never drop it silently.

## Usage-instructions preamble (required, goes first in `handoff.md`)

Always include all of these, adjusting tone/emphasis only if the user named a specific handoff purpose:

1. **Ground-truth rule**: "Treat this document as authoritative for everything it covers. Do not re-derive, second-guess, or silently contradict decisions recorded here."
2. **Don't-relitigate rule**: a short bullet list of decisions already settled in the conversation (pull these from the transcript — things the user explicitly chose or confirmed), so the receiving AI doesn't reopen them.
3. **Open questions**: anything left unresolved at the point of export, explicitly listed, so the receiving AI treats these as open rather than assuming closure.
4. **Coverage caveat, restated**: repeat the scope/coverage line from Metadata here too, in plain language — e.g. "This capture starts at turn 4; earlier turns were no longer in context when this export was generated and are not recoverable from this file."
5. **Estimate caveat**: a one-line reminder that token counts are estimates.
6. **Purpose-specific line** (only if the user stated one): one sentence tailoring intent — e.g. "This handoff is for continuing the same task in a new session," vs. "...for onboarding a teammate who wasn't in the original conversation," vs. "...for sharing across a project team." Default to the first (continuation) if no purpose was stated.

## Canonical JSON (`handoff.json`)

```json
{
  "conversation_name": "string",
  "generated_at": "ISO 8601 timestamp",
  "scope": {
    "coverage": "full | partial",
    "starts_at_turn": 1,
    "note": "string, empty if full coverage"
  },
  "stats": {
    "user_turns": 0,
    "claude_turns": 0,
    "user_tokens_estimated": 0,
    "claude_tokens_estimated": 0,
    "redactions_applied": 0
  },
  "usage_instructions": {
    "ground_truth_rule": "string",
    "settled_decisions": ["string", "..."],
    "open_questions": ["string", "..."],
    "purpose": "continuation | onboarding | team-share"
  },
  "turns": [
    {
      "turn": 1,
      "user_prompt": "verbatim string",
      "blocks": [
        {"type": "thought", "content": "string", "order": 1},
        {"type": "tool_call", "name": "string", "params": {}, "order": 2},
        {"type": "tool_result", "name": "string", "content": "string", "truncated": false, "order": 3},
        {"type": "skill", "name": "string", "purpose": "string", "order": 4},
        {"type": "answer", "content": "string", "order": 5},
        {"type": "file", "direction": "uploaded | generated", "filename": "string", "path": "assets/string", "order": 6}
      ]
    }
  ]
}
```

`blocks` must be sorted by `order` and reflect the true chronological/logical sequence within the turn — this is what lets a reader (human or AI) reconstruct exactly what happened and when, not just what the final answer was. If `handoff.md` and `handoff.json` ever disagree, `handoff.json` is the source of truth.
