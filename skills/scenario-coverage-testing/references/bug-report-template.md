# Bug / Incident Report Template

Log one of these for every confirmed error hit during a scenario run, whether fixed or left open.

```
### Incident <ID> — <one-line summary>

Scenario: <which scenario, which persona>
Pipeline stage: <which of the 10 universal stages, e.g. "5 - Validation">
Step: <the exact step number/action from the scenario>
Category: <from monitoring-taxonomy.md, e.g. "Silent/swallowed failure">

Symptom:
  <what was actually observed — exact error text, log excerpt, or the
   mismatch between claimed and actual state>

Root cause:
  <the confirmed underlying cause — not a symptom description. If not
   yet confirmed, say so explicitly rather than guessing.>

Fix applied:
  <the specific change made — file(s), what changed, why this is the
   minimal correct fix rather than a workaround>

Verification:
  <how the fix was confirmed — the isolated re-check, then the resumed
   scenario step that passed afterward>

Regression risk / related cells:
  <other coverage-matrix rows that touch the same code path and should
   be re-checked because of this fix, if any>

Status: Fixed and verified / Fixed, verification pending / Open — blocked on <reason>
Severity: Critical / High / Medium / Low
```

## Severity guide
- **Critical** — data loss, security boundary violated, or the persona cannot reach their goal at all.
- **High** — persona reaches their goal but with wrong output, duplicated side effects, or a broken path they'd hit routinely.
- **Medium** — recoverable friction (bad error message, confusing state) that doesn't block completion.
- **Low** — cosmetic, or a warning-level signal not yet causing user-visible harm.

## End-of-pass roll-up
After all scenarios are run, summarize:
- Total incidents found, by severity
- Total fixed and verified vs. still open
- Any coverage-matrix cells flagged for re-check due to a fix elsewhere
- A one-paragraph plain-language verdict: is this project in a state a human should feel confident shipping/continuing, and what (if anything) still needs a human decision rather than another test pass
