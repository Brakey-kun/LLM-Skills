---
name: project-uphaul
description: Runs a full, dynamic audit-and-overhaul pipeline on a project the user didn't build with a strong model and doesn't know well enough to judge themselves. Sequences meta-skill-router (to find any stack-specific specialist skills worth folding in), then code-overhaul-skill (or ara-rigor-reviewer for research/writing projects) to diagnose and scope what's wrong, then autoresearch-skill to actually execute the fix on a branch. Use this whenever the user asks to "audit," "overhaul," "check the quality of," "review and fix," or "grade and clean up" a project or codebase, says things like "is this actually good," "I don't know if this code is fine," or "this was built with a weaker model, can you check it" — even if they don't name the underlying skills. Trigger on the intent, not the exact words.
---

# project-uphaul

A thin sequencer, not an auditor. All judgment about what "good" looks like lives in the three
skills this one calls, in order. This skill's only job is: classify the project, call the right
skills in the right order, checkpoint with the user between diagnosis and execution, and translate
the output into something a non-expert can actually act on.

**Requires:** `meta-skill-router`, `code-overhaul-skill`, `autoresearch-skill`, and — for
non-code projects — `ara-rigor-reviewer` (or an equivalent research-rigor skill from the same
family). If one of these isn't installed when this skill triggers, say so up front and ask
whether to proceed without it or pause to install it. Never silently skip a stage.

## Stage 0 — Classify the project

Look at the project's contents before doing anything else, don't ask the user to describe it:

- **Code project** — source files, package manifests, build/CI config → code branch
- **Research/writing project** — papers, reports, literature reviews, prose-heavy notebooks → research branch
- **Mixed** — run both branches, each scoped to its own content

Only ask the user if the split is genuinely ambiguous after looking.

## Stage 1 — Route: `meta-skill-router`

This stage is not the audit itself — it's discovering *extra* specialist skills relevant to this
project's specific stack that should feed into Stage 2. Ask it, in effect: "given this project's
stack and domain, which installed skills — or skills worth installing — are relevant to a quality
audit of it?" Examples of what it might surface: a security-scanning skill if the project touches
auth or secrets, a framework-specific linter, a test-coverage skill.

Treat its output as **additive** — folded into Stage 2's checklist, never a replacement for it.
If it flags something not installed, mention it once, briefly, and keep moving — don't block the
pipeline on an install the user didn't ask for.

## Stage 2 — Diagnose

**Code branch:** call `code-overhaul-skill` on the project. Let it choose its own scope tier
(SURGICAL / SYSTEMATIC / FULL AUDIT) from what it finds — don't pre-pick this for it. That
decision *is* the answer to "does this need a big change or a small one," which is the thing the
user came here not knowing. Add any Stage 1 specialist checks alongside its normal
architecture/quality/tests/performance/dependency pass. Its output should land as an impact/effort
matrix: DO FIRST / PLAN CAREFULLY / IF TIME / SKIP.

**Research branch:** call `ara-rigor-reviewer` across its rigor dimensions (evidence relevance,
falsifiability, scope calibration, argument coherence, exploration integrity, methodological
rigor) and get its severity-ranked findings plus its Strong-Accept-to-Reject read.

**Checkpoint (mandatory, not optional):** before touching anything, summarize the diagnosis for
the user in plain language — what's wrong, how severe, what scope of change it implies —
translating out of jargon rather than pasting raw findings, since they don't know the code well
enough to parse a technical report unassisted. Get an explicit go-ahead before Stage 3. If
anything security-sensitive turned up (leaked keys, auth bypass, exposed secrets, injection
risk), flag that separately and immediately — don't let it wait inside the matrix.

## Stage 3 — Overhaul: `autoresearch-skill`

**Code branch:** hand the DO FIRST / PLAN CAREFULLY items from Stage 2 to `autoresearch-skill` as
its goal set. Let its find → fix → simplify loop run on a branch — never main, never overwriting
the original — re-measuring against Stage 2's findings each cycle. Leave IF TIME / SKIP items
alone unless the user asks for them by name.

**Research branch:** feed the rigor findings into whichever revision skill sits alongside
`ara-rigor-reviewer` in its skill family, weakest-scoring dimension first. Work on a separate
draft copy, not the original file.

## Stage 4 — Report back

No raw diff dump. Give the user:

1. What was found, severity-ranked, in plain language
2. What actually got changed, grouped by the Stage 2 matrix category it came from
3. What was deliberately left alone (IF TIME / SKIP) and why
4. Where the result lives (branch name / draft path) and confirmation that nothing merged or
   overwrote the original automatically

## Guardrails

- Never merge to main or overwrite the original without explicit confirmation, every time.
- Never skip the Stage 2 checkpoint, even under pressure to move fast — the entire premise of
  this skill is that the user can't self-check an unreviewed automatic overhaul.
- Security-sensitive findings get surfaced immediately, not batched into Stage 4.
- If the project is small enough that this pipeline is overkill (a short script, a one-page
  draft), say so and offer a direct review instead of running all four stages for their own sake.
- Don't add audit criteria to this file. If you're tempted to, that logic belongs in
  `code-overhaul-skill`, `autoresearch-skill`, or `ara-rigor-reviewer` instead — keep this skill
  a sequencer.
