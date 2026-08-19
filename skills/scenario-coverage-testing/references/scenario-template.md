# Scenario Template

Copy this structure for every scenario. A scenario is not done until the persona reaches their actual end goal (pipeline stage 9-10) — don't stop at "the interesting part."

```
### Scenario N — <short title>

Persona: <one of the persona-library archetypes, adapted>
Goal: <what this persona is trying to accomplish, end to end, in plain language>
Entry point: <exact starting screen / CLI command / API call>
Tools & agents involved: <e.g., Claude Code (implementation), omp.sh (scaffold), backend logs at ...>
Coverage tags: <matrix rows this scenario is designed to hit>
Deliberate friction point: <which stage/step this scenario is expected to stress, and why>

Steps:

1. Action: <precise, reproducible action — exact command, exact click path, exact input>
   Expected: <what should happen if everything is healthy>
   Monitor: <where to look — which log file, which console, which response field, which UI element — and what a bad sign looks like there>

2. Action: ...
   Expected: ...
   Monitor: ...

   [If a step fails during execution, do NOT delete/rewrite it after the fact.
    Insert a "Fix-forward" sub-block right after the step it interrupted:]

   Fix-forward:
     Symptom: <what was actually observed>
     Root cause: <confirmed cause, not a guess>
     Fix applied: <the change made>
     Verified: <how the fix was confirmed before resuming>
   [Then continue with the next numbered step as originally planned — the
    scenario resumes, it does not restart.]

...

N. Action: <final step reaching the persona's actual goal>
   Expected: <completion state>
   Monitor: <post-completion check — logs clean, no orphaned jobs, no leaked resources>

Outcome: <pass / pass-with-fixes / blocked, plus one-line summary>
```

## Writing good steps
- **Be exact, not vague.** "User edits the script" is not a step. "User opens `scene_3.json` in the editor, changes `duration_ms` from 4000 to 6000, and saves" is a step.
- **Every step needs a Monitor line**, even ones that look purely cosmetic — the whole point of continuous monitoring is that unglamorous steps are exactly where silent failures hide.
- **Expected results must be falsifiable.** "It should work" isn't checkable. "HTTP 200, response body contains `status: complete`, and a new row appears in the `renders` table" is checkable.
- **Don't skip the waiting/polling steps.** If the real workflow has the user wait on a long-running agent job, the scenario must actually wait (or explicitly simulate the wait) and check what the UI/CLI shows *during* the wait, not just after — this is a common place for stuck spinners, silent timeouts, and stale status text.
- **End every scenario at the real finish line** — export, deploy, publish, commit, merge, whatever "done" means for this persona — plus a post-completion check that the backend is actually clean afterward.
