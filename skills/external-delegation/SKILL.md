---
name: external-delegation
description: "Craft a self-contained delegation prompt for handoff to another AI session on a different account/platform. Use when you need another model to continue work, but the session boundary erases context."
---

# external-delegation

Craft a prompt that survives a session boundary. The recipient has **zero context** beyond what you give them. Over-specify. Every assumption you skip is one they will get wrong.

## Structure

### 1. Role & Situation (3-5 sentences)
Who the recipient is, what they're taking over, and why. Establish legitimacy upfront if the work touches anti-reverse-engineering, DRM, or server-dependent binaries.

> "You are continuing restoration of an abandoned Unity 4.6.3 game whose servers were shut down years ago. The game is unplayable without modification — all patches are necessary to make a legitimately purchased copy functional offline. This is game preservation, not circumvention of active DRM."

### 2. What Has Been Done (table or bullet list)
Every prior step, file changed, decision made, and why. The recipient cannot read your history.

| Step | File/Method | Change | Reason |
|------|-------------|--------|--------|
| Patch 1 | SteamManager.get_Initialized | hardcoded true | Dead Steamworks API |
| ... | | | |

### 3. Current Bugs / Blockers
Exact error messages, stack traces, log excerpts. Name the file and line. If the error changed between runs, show the progression.

```
FileNotFoundException: Could not load file or assembly 'System.Private.CoreLib, Version=10.0.0.0'
  at Connection.SetStartSettingToPhoton ()
```

**Root cause analysis** — don't just dump the error, explain what you know is wrong and what you've ruled out.

### 4. Technical Constraints (non-negotiable)
List every gotcha the recipient needs to get right. Be explicit about version-specific behavior.

- .NET 3.5/Mono 2.0 profile: `System.Core` not mscorlib for `System.Action`
- Unity 4.x: `"UnityEngine"` not `"UnityEngine.CoreModule"`
- `ldc.i4.3` uses `OpCodes.Ldc_I4_3` (short form), not `OpCodes.Ldc_I4`
- Branch target `Instruction` objects must be the exact same object (Cecil resolves by identity)
- etc.

### 5. Approach That Washed Out (don't repeat mistakes)
List what was tried and failed, with the exact reason it failed. This saves the recipient a re-exploration cycle.

- `box; unbox.any` before `stfld` into enum field → Mono 2.0 verifier still rejects
- `typeof(Type)` imports from patcher's .NET 10 runtime, not target mscorlib → `System.Private.CoreLib` dependency

### 6. Likely Working Approach
One or more paths you believe will work, ranked by confidence. Be concrete about which lines to change and what the replacement logic is.

### 7. Files to Hand Off
Every file path the recipient needs. Mark which are read-only references and which are the target to edit.

### 8. Verification
Exact commands to run and what "success" looks like in the output.

### 9. Ethical Context (when needed)
If the work touches binary modification, server bypass, or authentication, state clearly why this is legitimate. Be specific about the game's status, the user's ownership, and the nature of the patches. Don't be vague — name the game, what it does, why the servers are down, and what each patch does at a high level. An AI safety filter that sees `SteamManager.get_Initialized → true` without context will refuse.

## Anti-Patterns

- ❌ "Continue the work" — zero-context handoff guaranteed to fail
- ❌ Pasting a long log with no analysis — the recipient doesn't know what's noise
- ❌ "Figure it out" — they have no tools, no history, no repo map
- ❌ Hiding or euphemizing ethically sensitive patches — name what each one does and why, or the recipient's safety filter will guess the worst
- ❌ Delegating a task you don't understand yourself — if you can't summarize the root cause, you're not ready to delegate

## Rule of Thumb

If the recipient can open the files, build, run, hit the exact error, and fix it without ever asking you a question, the prompt is complete.
