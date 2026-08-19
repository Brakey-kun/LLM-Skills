# Monitoring Taxonomy

Used during Phase 4 (execute with continuous monitoring). For every step, check against these categories — not just "did it visibly crash." Most real bugs a full pipeline test is meant to catch are in categories 2-6, not category 1.

## 1. Hard failures (easy to catch)
- Explicit error messages, stack traces, non-zero exit codes
- UI error states, failed HTTP status codes (4xx/5xx)
- Process/agent crash or unexpected termination

**Where to look:** stdout/stderr, browser console, HTTP response status, process exit code.

## 2. Silent/swallowed failures (easy to miss)
- Try/catch blocks that log-and-continue without surfacing anything to the user
- Fallback values silently substituted for a failed operation (empty result treated as "nothing to show" instead of "this failed")
- Partial writes — an operation reports success but only part of the expected state was actually persisted

**Where to look:** compare what the UI/CLI *claims* happened against what actually landed in the backend/database/filesystem/log. This mismatch is the single highest-value thing to check and the easiest thing to skip.

## 3. Timing & performance anomalies
- A step that's normally instant taking noticeably longer
- Growing latency across repeated operations in the same scenario (suggests a leak or unbounded growth somewhere)
- A "wait/poll" step that never resolves, or resolves with stale status

**Where to look:** timestamps in logs, response times, whether a polling UI element (spinner, progress bar, status text) matches actual backend job state.

## 4. State inconsistency
- GUI shows one thing, backend/database shows another
- Two agents/tools in a handoff disagree about the current state of a shared artifact
- Cached/stale data displayed after an update that should have invalidated it

**Where to look:** cross-reference the visible state against the source of truth (database, filesystem, API) after every mutating step, not just at the end.

## 5. Resource & lifecycle issues
- Orphaned background jobs/processes that outlive their triggering action
- Unreleased locks, open connections, growing memory/file-handle counts across repeated operations
- Duplicate side effects on retry (double-write, double-send, double-charge) — especially relevant for the Interrupted/Recovery persona

**Where to look:** process/job lists, resource monitors, idempotency of retried operations (retry the same action twice deliberately and check nothing duplicates).

## 6. Warnings & degraded-mode signals
- Deprecation warnings, retried requests that eventually succeeded (why did they need a retry?), fallback code paths being exercised
- Rate-limit warnings that didn't (yet) become hard failures
- Anything logged at `warn` level — these are often the earliest signal of a problem that will become a hard failure under slightly different conditions

**Where to look:** full log output at `warn` level and above, not just `error`. A clean-looking run with buried warnings is not actually clean.

## 7. Agent-specific signals (Claude Code / Codex / Antigravity CLI / omp.sh / similar)
- Agent output that doesn't match what was actually asked (scope drift, ignored constraints)
- Agent silently modifying files/config outside the expected scope
- Agent re-running on an already-modified artifact and overwriting manual edits from a prior scenario step (see Long-Tail Maintenance persona)
- Credential/permission scope errors specific to the agent's execution context (different from the app's own auth)

**Where to look:** diff the agent's actual file/config changes against what was requested; check the agent's own execution log/transcript if available, not just its final output.

## How to act on a hint
- **Category 1 (hard failure):** always triggers the fix-forward protocol immediately.
- **Categories 2-7:** note it. If it's clearly benign and one-off, log it and continue. If it recurs, worsens, or you can't confirm it's benign, treat it as a confirmed error and trigger fix-forward rather than hoping it resolves itself — silent issues found during testing and *not* investigated defeat the purpose of full-coverage testing.
