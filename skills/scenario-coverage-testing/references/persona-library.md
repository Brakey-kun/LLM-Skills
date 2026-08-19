# Persona Library

Generic, reusable persona archetypes. Adapt each to the real project's real screens/commands — don't reuse steps verbatim across projects. Pick a subset (usually 5-8) whose combination maximizes coverage-matrix breadth, not the same failure mode repeated.

Each entry: who they are, why they're a distinct coverage source, and what kinds of bugs they tend to surface.

## 1. First-Time / Onboarding User
Never used the project before. Follows the "happy path" literally as documented, with zero tribal knowledge.
- **Surfaces:** onboarding flow, setup/install/config, default states, empty states, first agentic-tool invocation (auth/API key setup for Claude Code / Codex / omp.sh / Antigravity CLI), documentation accuracy.
- **Typical bugs found:** missing default config, unclear/broken setup steps, crashes on empty state, first-run race conditions (e.g., agent invoked before auth finishes propagating).

## 2. Power User / Batch Operator
Experienced, moves fast, does many operations back-to-back or in parallel/batch.
- **Surfaces:** concurrency, queueing, rate limits, batch endpoints/commands, resource cleanup between rapid operations.
- **Typical bugs found:** race conditions, resource exhaustion, rate-limit handling, stale cache/state bleeding between operations, UI not reflecting rapid backend changes.

## 3. Multi-Agent Handoff User
Uses more than one agentic tool in the same workflow (e.g., scaffolds with omp.sh, implements with Claude Code, reviews/tests with Codex, deploys via Antigravity CLI).
- **Surfaces:** hand-off points between tools/agents, shared state/config each tool reads or writes, format/schema compatibility between agent outputs, credential/permission scope across tools.
- **Typical bugs found:** one agent's output silently breaking assumptions the next agent makes; config drift; partial writes left by one tool that confuse the next.

## 4. Interrupted / Recovery User
Gets interrupted mid-task — closes the app, loses connection, process crashes, machine sleeps — then comes back.
- **Surfaces:** persistence/autosave, checkpointing, resumability, idempotency of retried operations, orphaned background jobs.
- **Typical bugs found:** lost work, duplicate side effects on resume (double-charged, double-rendered, double-committed), zombie processes/jobs that never clean up.

## 5. Edge-Case / Stress User
Deliberately pushes inputs to extremes — very large input, very long-running operation, unusual characters/formats, minimal/empty input, malformed input.
- **Surfaces:** input validation, timeouts, token/size limits, error messaging quality, graceful degradation vs. hard crash.
- **Typical bugs found:** silent truncation, unhandled timeouts, unhelpful/opaque error messages, crashes instead of graceful rejection.

## 6. Permissions / Security-Boundary User
Operates with restricted credentials, tries to access things they shouldn't, switches accounts/workspaces mid-session.
- **Surfaces:** auth boundaries, authorization checks on every surfaced action (not just the ones with visible gates), session/token expiry handling, multi-tenant isolation.
- **Typical bugs found:** missing authorization checks on secondary paths, stale session tokens accepted, cross-tenant data leakage.

## 7. Long-Tail Maintenance User
Returns to an existing project days/weeks later to modify, upgrade a dependency, or extend it — not building fresh.
- **Surfaces:** backward compatibility, migrations, versioned configs/schemas, agentic tool re-invocation on an already-modified codebase (does the agent respect prior manual edits?).
- **Typical bugs found:** migrations that assume a clean slate, agent tools overwriting manual edits, version-skew bugs between what the agent last generated and what the human since changed.

## 8. Collaborative / Concurrent-Editor User
Two or more actors (human + human, or human + agent) touching the same artifact around the same time.
- **Surfaces:** conflict resolution, locking, merge behavior, real-time sync (if applicable).
- **Typical bugs found:** lost updates, silent overwrite of one actor's changes by another, inconsistent views between actors.

## Combining personas for coverage
When selecting scenarios for a pass, favor combinations that:
- Include exactly one clean happy-path baseline (usually persona 1 or 2) to catch regressions against "nothing weird happened."
- Include at least one multi-agent handoff scenario whenever the project genuinely uses more than one agentic tool.
- Include at least one interruption/recovery scenario whenever the project has any long-running or stateful operation.
- Weight edge-case and permissions scenarios higher for anything pre-launch or handling user data.
