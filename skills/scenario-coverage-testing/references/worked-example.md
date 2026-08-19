# Worked Example

A concrete instantiation of the framework, so a new project can be mapped the same way. This example project is a content-generation pipeline app: idea → AI "scripter" agent → script editing → render → render QA → fix → re-render → publish, built with a mix of omp.sh (scaffolding), Claude Code (implementation/scripter agent), and a CLI render worker. This is one instantiation, not the framework itself — a different project (an e-commerce backend, a CLI dev tool, a data pipeline) would produce a completely different matrix and scenario set from the same process in SKILL.md.

## Phase 1 — Discovery (abridged)
- GUI screens: idea board, script editor, render queue/status, render preview, publish flow
- CLI: `omp render`, `omp publish`, agent invocation commands
- Agent integration points: idea → Claude Code "scripter" call (generates script draft); render worker triggered on script approval
- Backend signal: `logs/agent.log` (agent calls), `logs/render.log` (render worker), a `/status` dashboard endpoint
- Persistent state: draft scripts (autosaved), render job queue, published asset registry

## Phase 2 — Coverage matrix (abridged rows)
Idea creation · Scripter agent invocation · Script autosave · Script manual edit · Render trigger · Render queue status polling · Render preview · Render QA (audio/visual check) · Fix-and-rerender · Publish · Agent handoff (scaffold → implement) · Interrupted render recovery · Permission boundary (workspace access) · Backend log signal

## Phase 3-5 — Three sample scenarios (of a full 6-scenario pass)

### Scenario 1 — First-time solo creator (happy-path baseline)
Persona: brand-new user, first project.
Goal: go from a blank idea to a published render with no injected friction — this is the regression baseline.

1. Action: Create new idea "Product demo, 30s" via idea board.
   Expected: Idea saved, appears in queue with status `draft`.
   Monitor: `logs/agent.log` shows no invocation yet (correct — agent hasn't been called).

2. Action: Click "Generate script," which invokes the Claude Code scripter agent.
   Expected: UI shows a waiting/polling state; agent produces a script draft within the expected time window.
   Monitor: `logs/agent.log` for the invocation and completion entries; UI polling state should update, not freeze, while waiting.

3. Action: Review generated script in editor; make no changes; click "Approve."
   Expected: Script status moves to `approved`.
   Monitor: Autosave log entry matches what's shown on screen (state-consistency check).

4. Action: Trigger render.
   Expected: Job enters render queue, status visible and updating.
   Monitor: `logs/render.log`; queue status in UI should match actual worker state, not a stale cached value.

5. Action: Open render preview once complete.
   Expected: Preview matches script content; no visible/audible defects.
   Monitor: Render worker exit code = 0; no warnings in `logs/render.log`.

6. Action: Publish.
   Expected: Asset appears in published registry.
   Monitor: `/status` dashboard shows no residual queued/failed jobs after publish (post-completion check).

Outcome: pass — establishes the clean baseline other scenarios are compared against.

### Scenario 2 — Power user hits a race condition in batch scripting
Persona: power user queues three ideas for scripting back-to-back before any finish.
Goal: get all three scripted, edited, and rendered without cross-contamination between jobs.

1. Action: Create three ideas; trigger "Generate script" on all three within a few seconds of each other.
   Expected: Three independent agent invocations, three independent drafts.
   Monitor: `logs/agent.log` for three distinct invocation IDs.

   Fix-forward:
     Symptom: Script draft for idea #2 briefly showed content from idea #3's draft in the editor after both completed near-simultaneously.
     Root cause: Editor's "latest draft" state was keyed by a global variable instead of per-idea ID, so the last agent response to resolve overwrote the currently-open editor regardless of which idea it belonged to.
     Fix applied: Keyed the editor's draft-loading state by idea ID; agent responses now only update the editor if it's still displaying the matching idea.
     Verified: Re-ran the same three-concurrent-invocation step in isolation five times; each editor consistently showed only its own idea's draft.

2. Action: Approve and render all three.
   Expected: Three independent render jobs, no shared state bleed.
   Monitor: `logs/render.log` job IDs match idea IDs one-to-one; queue UI shows three distinct, correctly-labeled entries.

3. Action: Publish all three.
   Expected: Three distinct published assets, each matching its own idea's script.
   Monitor: Published registry entries cross-checked against original idea titles.

Outcome: pass-with-fixes — one critical state-keying bug found and fixed; regression risk flagged for any other "last response wins" UI state, so the render-status UI (similar pattern) was spot-checked too and found clean.

### Scenario 3 — Interrupted render, recovery, and agent handoff
Persona: user's connection drops mid-render, then later a second agentic tool (a review/QA agent) is invoked on the same asset before publish.
Goal: recover the interrupted render without duplication, then successfully hand off to the QA agent before publishing.

1. Action: Trigger render; kill the network connection mid-job; reconnect after ~30s.
   Expected: On reconnect, UI reflects the render worker's actual current state (still running, or completed while disconnected) — not a stale "failed" or duplicate "queued" state.
   Monitor: `logs/render.log` for a single job ID throughout; confirm no second job was silently queued on reconnect.

2. Action: Once render completes, invoke the QA review agent on the rendered asset (agent handoff).
   Expected: QA agent reads the actual completed render output and returns pass/fail feedback.
   Monitor: `logs/agent.log` for the handoff invocation; confirm the QA agent received the correct, final asset — not a partial file from the interrupted attempt.

   Fix-forward:
     Symptom: QA agent occasionally received a partially-written render file when invoked immediately after the "complete" status appeared.
     Root cause: Render worker flipped status to `complete` before the file write was fsynced/fully flushed to disk — a benign-looking timing gap that only showed up under the interrupted-then-immediately-handed-off sequence.
     Fix applied: Render worker now flips status to `complete` only after confirming the write is fully flushed.
     Verified: Repeated the interrupt-then-immediate-handoff sequence ten times; QA agent consistently received the complete file.

3. Action: Publish after QA agent approval.
   Expected: Publish succeeds; registry entry reflects QA-approved status.
   Monitor: Post-completion check on `/status` — no orphaned render job from the original interrupted attempt remains queued.

Outcome: pass-with-fixes — one timing/handoff bug found and fixed; this scenario's coverage cells (interrupted recovery, agent handoff) were the ones the happy-path baseline in Scenario 1 could never have caught, which is the point of designing scenarios for coverage rather than convenience.

## What this demonstrates
The same discovery → matrix → persona → monitor → fix-forward → report process applies unchanged to a completely different project — swap "idea/scripter/render/publish" for "ticket/codegen/build/deploy" or "dataset/train/eval/release" and the skeleton, the monitoring taxonomy, and the fix-forward discipline all still apply.
