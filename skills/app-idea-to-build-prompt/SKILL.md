---
name: app-idea-to-build-prompt
description: Guides the full workflow for turning an app idea into a working interactive concept GUI (HTML/CSS/JS) and a comprehensive build prompt for Claude Code. Trigger whenever the user pitches or describes an app/product/tool idea and wants help developing it — especially requests for a concept GUI or mockup, a "build prompt" or "coding prompt" for Claude Code or another agent, help thinking through features/implementation/design choices before development starts, or picking a visual design direction. Also trigger mid-project on follow-ups like "suggest improvements," "redo the GUI with these changes," "add these features," a bug screenshot, a design reference to match, or "what did we decide on X" — these continue this same workflow, not one-off requests. Covers eliciting the idea, discussing trade-offs, picking a design direction, building the interactive mockup, writing the structured build prompt, and the iteration loop between all of these.
---

# App Idea → Concept GUI → Build Prompt

This skill turns a conversation about an app idea into two concrete artifacts: an interactive concept GUI the user can click through, and a build prompt thorough enough that Claude Code (or another agentic coder) can work from it with minimal back-and-forth. It also governs everything that happens *after* the first pass — discussion rounds, design pivots, corrections, and bug fixes are all part of this same workflow, not separate requests.

Work through five stages. Real conversations loop back between them — especially 2, 4, and 5 — rather than moving through once in a straight line. Knowing which stage a given message belongs to is most of the job.

## Stage 1 — Capture the idea completely

Read the whole idea before building anything. Features described later in a message often change how earlier ones should be interpreted, so resist starting a build prompt from the first paragraph.

- Look for a concrete worked example (a real instance of the app's central mechanic in action), not just a feature list. If the user hasn't given one, it's worth asking for one — an example disambiguates more than another paragraph of description ever does.
- Treat an explicit "etc." or "other things like this" as permission to fill the gap with good judgment, not as something to leave blank.
- Only *block* on genuine forks in the road — a tech-stack choice, a data-model decision with real downstream cost. Everything else gets a stated, reversible assumption (see the tagging convention in Stage 5) so the conversation keeps moving.
- **Don't stop at silent assumptions, though — close the pass with a combined discussion round.** After absorbing the idea (and again any later time the user adds a meaningful chunk of new detail), offer back a short, two-part response before building further:
  - **Clarifying questions** — genuine gaps that matter but weren't mentioned. Not a generic "anything else?" catch-all; specific, pointed questions about things that would actually change what gets built.
  - **Suggestions** — aspects worth tweaking, improving, or adding that the user hasn't covered, framed as proposals, not edicts.
  Present both together in one message, keep the list tight (the handful that actually matter, not an exhaustive interview), and invite a response — but don't gate progress on it. "You decide" or "handle that yourself" is a complete answer and should be treated as one. Run this by default; don't wait for the user to explicitly ask for it (they may not know to ask the first time), but recognize it immediately when they do ask — see "Recognizing iteration signals" below.

## Stage 2 — Discuss features, implementation, and design choices

This repeats throughout the project, not just once at the start.

- When asked to suggest improvements, produce a **categorized, non-committal list** — group by area (architecture/robustness, data model, feature gaps, GUI/UX is a reasonable default split) — and apply nothing yet. End by asking how to proceed: mark items in/out one by one, or give a recommended cut if that's faster.
- When the user responds with decisions, take their specifics literally. If they describe an exact mechanism, spec that mechanism precisely in the build prompt rather than paraphrasing it into something vaguer.
- Every later round of suggestions must be genuinely new. If suggestions are requested again, that's a signal the last round was useful — don't recycle it with different wording.
- Not everything needs a decision immediately. "I'll handle that separately" is a complete answer — drop it and move on without pushing.

## Stage 3 — Establish (and re-establish) the design direction

- **Check for a companion brand/design-system skill first.** If the user already has one active (a skill defining a consistent visual language across their projects — colors, shape, type, iconography, motion), that system *is* the design direction for this project. Apply it directly rather than asking, and don't re-derive an equivalent from scratch. Only fall back to the steps below when no such skill applies.
- If the user has a reference (a named product, a link, a screenshot), treat it as authoritative and pull it in directly.
- If there's no reference yet, either ask, or use available design-reference tooling to gather grounding. If that tooling isn't available, say so plainly and fall back to a coherent, explicitly-named direction rather than a silent generic default.
- **A new design reference arriving mid-project is a full re-skin of the design tokens (color, shape, type, motion), not a patch to one component.** Expect this to happen more than once over a project's lifetime, and treat it as first-class work each time.
- Write the chosen direction down explicitly in the build prompt, naming the reference (or the design-system skill, if that's what's governing it), so it survives past this conversation.

## Stage 4 — Build the concept GUI

- It has to demonstrate the actual features, not just imply them visually. Every panel, toggle, or interaction described so far should be reachable and working. A concept GUI that only looks right invites an immediate correction round ("make it interactive") that costs a full extra cycle — avoid that by building it interactive the first time.
- Reuse one set of design tokens everywhere (colors, radii, spacing, type, motion timing) rather than restyling per screen.
- Before presenting it, verify it: syntax-check any embedded script, confirm every element ID referenced by the code exists, confirm every button's handler is defined. A broken interactive demo is worse than a static one — the person testing it can't distinguish your intent from a bug.
- State plainly, in the build prompt, that this file is the **literal implementation reference**, not a mood board — so deviations from it during the real build get flagged rather than treated as casual license.

## Stage 5 — Write the build prompt

A build prompt that actually works has these properties. Use them as a checklist:

- **Addressed directly to the builder** ("To Claude Code: read this whole document before writing any code..."), not written as neutral third-party documentation.
- **Numbered sections**, cross-referenced by number, so later additions point back at earlier ones precisely instead of re-explaining them.
- **A two-tag convention for uncertainty, used consistently**: one tag for "reasonable default, but flag before deviating," a different tag for "stop and ask, don't guess." More than two tags stops being useful — resist adding a third.
- **A recommended stack with a one-line reason per choice**, and an explicit note on which single choice is actually worth confirming before scaffolding starts (there's usually one real fork, not five).
- **Canonical formats/contracts spelled out as rules**, not prose descriptions of vibes — anything another AI or developer needs to parse later needs an actual grammar, however informal.
- **A phased build plan**, each phase ending in something demoable, with an explicit instruction not to attempt everything in one pass.
- **A suggested file/repo structure**, so the builder isn't also inventing project layout on top of everything else.
- A closing instruction that each phase should report what was deferred and what open questions came up, so a multi-session build doesn't silently drift.

## Cross-cutting principles

These apply in every stage, not just their most obvious one.

- **Investigate root causes, not symptoms.** When something's reported broken — a screenshot of a bug — find the actual defect rather than patching around the visible symptom. State what was actually wrong in one sentence once found; it's a real trust signal and usually genuinely fast.
- **Verify before presenting.** Anything with executable logic gets an automated check (a syntax check, a cross-reference of IDs/handlers) before being called done. Don't rely on "it looks right" for anything that runs.
- **Do real research for real facts.** If a correction involves external specifics (a real library, a real model, a real API shape) that aren't fully certain, verify them rather than filling the gap with something plausible-sounding. Flag what's still unverified rather than asserting it.
- **Scope discipline on bundled requests.** A message that bundles an in-scope technical ask with a bigger side-topic (marketing, funding, timeline) gets the in-scope part done in full; the side-topic gets a short direct answer or one clarifying question — not a full unrequested deliverable, and not silence either.
- **Keep both artifacts in sync, deliberately.** A change that affects both the concept GUI and the build prompt updates both in the same pass. A change scoped to just one should say so explicitly, so the user isn't left guessing whether the other is now stale.
- **A request to fix one specific thing is a request to fix that thing precisely.** Noticing a related improvement while in there is worth mentioning separately — it isn't license to redesign the surrounding area unasked.
- **Own mistakes plainly.** If an earlier pass introduced an inconsistency (a numbering error, a stale cross-reference, a terminology mix-up), say what it was and that it's fixed. Don't correct it silently.
- **Close a substantial edit with a concrete summary, not a generic confirmation.** After a multi-section or multi-file change, say specifically what changed (section numbers, feature names) — not just "done, let me know if you want changes." Surface anything worth a second look even if not asked: a genuinely uncertain interpretive call, an open question still unresolved, a place two documents might now be slightly out of sync. This is a real trust signal and it's how the user catches a misread before it compounds across another round.

## Recognizing iteration signals

Once the first concept GUI and build prompt exist, later messages are usually one of these — read the intent, not just the literal words:

- **"Suggest improvements to be discussed"** → open a new Stage 2 round: categorized list, nothing applied yet.
- **"Let's discuss the rest together" / "ask me what I failed to mention" / "point out what needs improving"** → an explicit request for Stage 1's combined discussion round (questions + suggestions). Treat this as confirmation the behavior is wanted, not as the only time it should happen — see Stage 1.
- **A list of specific corrections, or "apply the confirmed items"** → close a Stage 2 round and move to building: apply everything precisely, update whichever artifact(s) the corrections actually touch.
- **"Redo the GUI" / "update the prompt" / "reflect this in both"** → pay close attention to which artifact(s) are actually in scope; don't touch the other one without saying so.
- **A screenshot with "this is broken" or similar** → Stage 4 debugging: find the real cause, fix it, verify, explain briefly what was wrong.
- **A link or screenshot of a design reference dropped in later** → a Stage 3 re-skin, full-system by default unless the user says otherwise.
- **A factual question about a past decision** ("what stack did we land on?") → answer directly from what's already in the build prompt; don't re-litigate the decision unless asked to.
- **A tangential ask bundled in** (marketing, timeline, pricing) → handle the in-scope technical part fully, address the tangent briefly, don't let it hijack the response.

## Common failure modes to avoid

- **A concept GUI that only looks right.** This is the single most expensive mistake — it costs a whole extra round-trip. Build it interactive the first time.
- **Silent terminology drift.** If the app has two distinct internal representations of something, lock down the exact meaning of each once, in writing, in the build prompt — and don't let later sections use the terms inconsistently with that definition.
- **Cross-reference rot.** Section references go stale as content gets renumbered or reordered across edits. After any renumbering, do a deliberate sweep for stale references rather than trusting it was handled edit-by-edit.
- **Over-scoping a single correction.** Fix precisely what was asked. Mention adjacent ideas separately instead of folding them in unasked.
