# Coverage Matrix Template

Rows = every surface/feature/tool found during discovery (Phase 1). Columns = scenarios (Phase 3). A cell is checked when a scenario actually exercises that row in a way that would surface a real problem — not just passes near it.

```
| Surface / Feature                          | S1 (persona) | S2 (persona) | S3 (persona) | S4 (persona) | S5 (persona) | Notes |
|----------------------------------------------|:---:|:---:|:---:|:---:|:---:|-------|
| GUI: <screen/flow name>                       |  ✅  |     |  ✅  |     |     |       |
| CLI: <command>                                |     |  ✅  |     |     |  ✅  |       |
| API: <endpoint>                               |  ✅  |     |     |  ✅  |     |       |
| Agent invocation: <tool, e.g. Claude Code>     |  ✅  |     |  ✅  |     |  ✅  |       |
| Agent handoff: <tool A → tool B>               |     |     |  ✅  |     |     |       |
| Background job / queue: <name>                |     |  ✅  |     |     |  ✅  |       |
| State transition: <e.g. draft → published>     |  ✅  |     |     |  ✅  |     |       |
| Error path: <e.g. invalid input rejected>      |     |     |     |     |  ✅  |       |
| Auth/permission boundary: <name>               |     |     |     |  ✅  |     |       |
| Persistence/resume: <name>                     |     |  ✅  |     |     |     |       |
| Backend/log signal: <log or dashboard source>  |  ✅  |  ✅  |  ✅  |  ✅  |  ✅  | every scenario should touch at least one |
```

## Rules for building rows
- One row per **distinct** surface, not per UI label — group trivially similar things (e.g., every form field doesn't need its own row) but never merge things that fail independently (e.g., "create" and "delete" on the same resource are different rows — they fail differently).
- Always include a row per **agentic tool integration point** (every place Claude Code / Codex / Antigravity CLI / omp.sh / any agent is invoked) — these are historically among the highest-risk, least-tested surfaces because they involve non-deterministic output.
- Always include a row per **state transition**, not just per screen — screens can each work in isolation while the transition between them is broken.
- Always include at least one **error path** row per major feature (what happens when it's given bad input, no input, or is interrupted) — a matrix with only happy-path rows isn't full coverage.
- Include a **backend/log signal** row so it's explicit that monitoring itself is being exercised, not just the user-facing action.

## When coverage counts as "full"
- Every row has at least one checked cell.
- Every high-risk row (agent invocations, agent handoffs, state transitions, error paths, permission boundaries) has **at least two** checked cells from *different* scenarios/personas, since a single scenario proves it works for one persona's path, not in general.
- At least one scenario is a clean, unmodified happy path (no injected friction) so there's a baseline to compare against.
- The matrix, not a gut feeling, is what you point to when asked "did we cover X" — if X isn't a row, add it and re-check before declaring done.
