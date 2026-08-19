---
name: scenario-coverage-testing
description: Full end-to-end QA methodology for software built or maintained with agentic AI coding tools (Claude Code, Codex, Antigravity CLI, omp.sh, or similar). Generates realistic multi-step user scenarios that walk an entire workflow A-to-Z (not isolated feature checks), executes them while continuously monitoring GUI, CLI, and backend/logs for errors or instability, and fixes problems in place before resuming the scenario. Use whenever the user asks for "full coverage testing," "scenario-based testing," "end-to-end QA," a "debugging pass," to "stress test" or "break" an app/project, wants realistic user journeys tested against their product, or is prepping to ship something built with an AI coding agent and wants confidence nothing is broken. Applies to ANY software project — web apps, CLIs, APIs, data/ML pipelines, mobile apps, browser extensions — not one domain. Trigger even on vague symptoms ("things feel flaky," "not sure what's broken," "want to catch bugs before launch").
---

# Scenario-Based Full-Coverage Testing

A methodology for testing any software project — especially one built or evolved with agentic AI coding tools — by simulating realistic end-to-end user journeys instead of isolated feature checks, while continuously watching for instability and fixing problems without abandoning the journey in progress.

This skill is domain-agnostic by design. It does not assume a video app, a web app, or any particular product. It gives Claude a repeatable process for turning **any** project into a coverage matrix, a set of distinct personas walking full A-to-Z journeys, and a monitor-and-fix-forward execution loop.

## Core Philosophy

1. **Test journeys, not features.** A feature works in isolation but breaks in sequence (stale state, race conditions, handoff failures between agents/tools). Every scenario is a complete story: entry → work → obstacle → resolution → completion. No scenario stops at step 3 just because step 3 "worked."
2. **Coverage is designed, not accidental.** Before writing scenarios, enumerate every surface (GUI screens, CLI commands, API endpoints, agent/tool integrations, background jobs, states) in a matrix. Then design the minimum set of scenarios whose union hits every cell. Coverage is a deliverable, not a hope.
3. **Monitor continuously, not just at the end.** Every step of every scenario is a checkpoint. Watch logs, console output, network responses, and process exit codes after every action — not only when something visibly breaks on screen. Many failures are silent (swallowed exceptions, degraded fallbacks, partial writes) until they surface three steps later as someone else's bug.
4. **Fix-forward, never restart-and-hope.** When something breaks, don't quietly retry or wait to see if it goes away, and don't abandon the scenario. Stop, diagnose the root cause, apply the smallest correct fix, verify the fix in isolation, then **resume the same scenario from the point of failure** so the persona's journey stays continuous and realistic. Log the incident either way.
5. **Every agentic-AI project shares a skeleton.** Regardless of domain, work that flows through an AI coding agent (Claude Code, Codex, Antigravity CLI, omp.sh, or similar) tends to follow the same underlying pipeline shape. Use it as scaffolding, then adapt the concrete steps to the real project.

## The Universal Pipeline

Map the real project's actual steps onto this generalized skeleton. Not every project has all ten stages, and some projects loop through stages 2-8 multiple times in one scenario — that's expected and realistic.

| # | Stage | What it looks like across domains |
|---|-------|-------------------------------------|
| 1 | **Intake** | User states a goal/task/idea/bug — a feature request, a prompt, a spec, a ticket |
| 2 | **Agent planning/generation** | The AI agent (Claude Code, Codex, Antigravity CLI, omp.sh, etc.) plans and produces an artifact — code, config, content, a script, a plan |
| 3 | **Wait / poll** | User waits on a long-running op — background generation, a build, a queued job — and the system must surface status honestly |
| 4 | **Review & edit** | User inspects the agent's output and manually edits it — a diff, a draft, a config file, a script |
| 5 | **Validation** | The edited output is run for real — build, render, deploy, test suite, preview, execution |
| 6 | **Issue detection** | Something is wrong — visible error, wrong output, silent misbehavior, perf regression |
| 7 | **Fix cycle** | User or agent fixes it — code edit, re-prompt, config change, dependency fix, permission fix |
| 8 | **Re-validation** | Re-run validation to confirm the fix actually resolved it and introduced nothing new |
| 9 | **Finalization** | Commit, merge, export, publish, deploy, release |
| 10 | **Post-completion check** | Confirm backend/logs/monitoring are clean after the fact — no residual errors, no orphaned jobs, no leaked resources |

A scenario is a specific persona's walk through this skeleton, instantiated with the real project's real screens, commands, and tools — not a generic description of the skeleton itself.

## Workflow

### Phase 0 — Establish scope and mode
Determine, quickly (ask the user only if genuinely unclear, otherwise infer and state your assumption):
- **What is the project?** Repo, app, CLI, pipeline — get its name/purpose in one line.
- **Which agentic tools are in its loop?** Claude Code, Codex, Antigravity CLI, omp.sh, custom agents, CI bots — anything that autonomously generates or modifies artifacts as part of the workflow.
- **What execution mode am I in?** This changes everything downstream:
  - **Live execution** — you have bash/terminal, browser/computer-use, or API access to the actual running project. You will *actually perform* each scenario step and observe *real* output/logs.
  - **Scripted QA deliverable** — you don't have hands-on access (or the user wants a shareable test plan). You produce a rigorous, step-by-step scenario document precise enough for a human or another agent to execute faithfully, with explicit "expected result" and "check here" instructions at every step.
  - Default to live execution whenever the necessary tools are available; don't ask permission to use read-only/observational tools, but do confirm before anything destructive (deploys, deletions, prod writes).

### Phase 1 — Discover the system under test
Build an inventory before writing a single scenario. Don't skip this — scenarios written without discovery reliably miss whole subsystems.
- Read the README, package manifest, routing/CLI-command definitions, and directory structure to enumerate: GUI screens/flows, CLI commands/flags, API endpoints, background jobs/queues, and every point where an agentic tool is invoked (a "scripter" call, a codegen step, a build agent, etc.).
- Identify where backend signal lives: log files, a monitoring dashboard, process exit codes, error-tracking service, database state — whatever "backend monitoring" means for this project.
- Identify state that persists across steps (auth sessions, saved drafts, job queues, caches) — these are exactly where multi-step scenarios catch bugs that single-feature tests don't.
- If you can't discover something programmatically, ask the user one targeted question rather than guessing silently.

### Phase 2 — Build the coverage matrix
List every surface/feature/tool discovered in Phase 1 as rows. Scenarios (designed next) become columns. See `references/coverage-matrix-template.md`. The matrix is what proves "full coverage" — it's not full coverage until every row has at least one checked cell, and the riskiest rows (state transitions, agent handoffs, error paths) have more than one.

### Phase 3 — Design personas and scenarios
Design a minimum of 5-6 scenarios, each built around a distinct persona, together covering the full matrix. Use `references/persona-library.md` for reusable archetypes (first-time user, power/batch user, multi-agent handoff user, interrupted/recovery user, edge-case/stress user, permissions/security user, long-tail maintenance user) and adapt them to the real project — don't reuse a persona's exact steps from one project on another.

Diversify scenarios along these axes so they don't overlap:
- **Entry point** — different starting screens/commands/API calls
- **Tool combination** — different agentic tools or handoffs between them (e.g., omp.sh scaffolds, Claude Code implements, Codex reviews)
- **Data scale** — trivial input vs. large/edge-case input
- **Failure injection point** — each scenario should be *likely* to surface a different class of bug (see the monitoring taxonomy) — don't inject the same failure mode five times
- **Happy-path vs. adversarial** — include at least one scenario that behaves exactly as intended start-to-finish (regression baseline) and several that hit friction

Write each scenario with `references/scenario-template.md`: persona, goal, tools involved, a numbered step list where every step has an Action, an Expected Result, and a Monitor note (what to watch, where).

### Phase 4 — Execute with continuous monitoring
Run each scenario step by step. For every single step:
1. **Act** — perform the step for real (live execution) or specify it precisely (scripted deliverable).
2. **Observe** — capture the actual output: screen state, CLI output, HTTP response, log lines, process exit code.
3. **Check against the monitoring taxonomy** (`references/monitoring-taxonomy.md`) — not just "did it crash," but the quieter hints: warnings, retried requests, growing latency, memory/handle growth, inconsistent state between GUI and backend, truncated output, silently-swallowed errors.
4. **Branch:**
   - Clean → log the step as passed, continue to the next step.
   - Hint of instability but not yet broken → note it, keep going, but flag it for a closer look if it recurs.
   - Confirmed error → invoke the fix-forward protocol (Phase 5) before continuing the scenario.

Never silently skip a step because it's inconvenient to reach, and never mark a step "passed" on faith without checking output.

### Phase 5 — Fix-forward protocol (on any confirmed error)
1. **Stop** the scenario at the exact step that failed. Don't move on and don't restart from step 1.
2. **Diagnose** the root cause — read the actual error/log/stack trace; don't guess. Use whatever tools are available (read source, re-run in isolation, add temporary logging) to confirm the cause before touching code.
3. **Fix** the smallest correct change that addresses the root cause, not a symptom (e.g., fix the race condition, not "add a retry that hides it" — unless a retry genuinely is the correct fix).
4. **Verify in isolation** — confirm the specific failing action now succeeds on its own.
5. **Resume the scenario at the failed step** (not from the top), so the persona's end-to-end journey stays intact — this is what proves the fix works in context, not just in a unit check.
6. **Log the incident** using `references/bug-report-template.md`: what broke, evidence, root cause, fix, verification, and whether it might recur elsewhere in the matrix (if so, flag those cells for re-check).
7. Continue the scenario to completion (stage 9-10 of the pipeline) — a scenario isn't done until the persona reaches their actual goal and post-completion checks are clean.

### Phase 6 — Report
Deliver three things at the end of a full pass:
- **Coverage matrix**, filled in, showing what was actually exercised.
- **Bug log**, every incident found and fixed (or, if unfixable in scope, clearly flagged as open with severity and reproduction steps).
- **Verdict summary** — plain-language health assessment: what's solid, what's still risky, what needs a human decision (e.g., a product/design tradeoff, not a bug).

## Reference files
- `references/persona-library.md` — reusable persona archetypes and the diversity axes to combine them on
- `references/scenario-template.md` — the fill-in structure for writing a rigorous, executable scenario
- `references/coverage-matrix-template.md` — matrix template and how to know when coverage is actually "full"
- `references/monitoring-taxonomy.md` — the categories of error hints to watch for beyond obvious crashes, and where to look for each
- `references/bug-report-template.md` — incident log format used during fix-forward
- `references/worked-example.md` — a complete worked example (a content-generation pipeline app tested with this method) showing the abstract framework instantiated concretely, for pattern reference on any new project

Read the relevant reference file at the point you need it rather than all at once — Phase 3 needs the persona library and scenario template; Phase 4 needs the monitoring taxonomy; Phase 5 needs the bug report template.
