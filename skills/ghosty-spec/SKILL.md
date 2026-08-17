---
name: ghosty-spec
description: Injects the Ghosty Spec-Driven Development (SDD) workflow and parallel Wave DAG execution engine natively into any OMP workspace. Produces and consumes specs in the exact on-disk format used by the Kiro IDE (.kiro/specs/), so specs are fully interoperable in both directions.
---

# Ghosty Spec-Driven Development (SDD) & Wave DAG Engine

Use this skill whenever a user wants to execute a project using the **Ghosty SDD Workflow**, requests parallel task execution using **DAG execution waves**, or references an existing `.kiro/specs/` folder (including one created by the Kiro IDE itself).

Ghosty is a from-scratch reimplementation of the Kiro spec format for OMP. It writes and reads the same `.kiro/` directory structure, the same document sections, the same EARS acceptance-criteria grammar, and the same task checkbox/dependency-graph conventions as the Kiro app — a spec produced by Ghosty opens and resumes cleanly in Kiro, and a spec produced by Kiro resumes cleanly under Ghosty. Never invent a parallel `.ghosty/` folder or a divergent schema; the whole point is drop-in interoperability.

## 1. Directory Layout

All specs live at `.kiro/specs/{feature-name}/` (kebab-case feature name), containing:

```
.kiro/specs/{feature-name}/
├── .config.kiro       # spec metadata (JSON, see below)
├── requirements.md    # or bugfix.md — see specType
├── design.md
└── tasks.md
```

Project-wide (not per-spec) guidance optionally lives in `.kiro/steering/*.md` — free-form Markdown documents (e.g. product context, tech stack, conventions) that should be loaded into context alongside a spec whenever they exist, the same way `PROJECT_CONSTITUTION.md` would be.

## 2. Spec Metadata — `.config.kiro`

Every spec directory MUST contain a `.config.kiro` file (create it up front, before the documents):

```json
{
  "specId": "<generate a uuid v4>",
  "workflowType": "design-first",
  "specType": "feature"
}
```

- **`workflowType`** — `"requirements-first"` or `"design-first"`. Controls generation *and resume* order:
  - `requirements-first`: `requirements.md` (or `bugfix.md`) → `design.md` → `tasks.md`
  - `design-first`: `design.md` → `requirements.md` → `tasks.md`
  When resuming a spec, always check `.config.kiro` first and continue at whichever document in that order is missing or incomplete — never assume `requirements-first`.
- **`specType`** — `"feature"` or `"bugfix"`. A `"bugfix"` spec replaces `requirements.md` with `bugfix.md` (same EARS-acceptance-criteria grammar, but scoped to reproduction steps, root cause, and fix criteria instead of user stories). A `"feature"` spec always uses `requirements.md`.

## 3. The Workflow — Document by Document

Generate (or resume) documents strictly in the order `.config.kiro.workflowType` dictates. Each document is written whole, then explicitly checkpointed with the user before moving to the next — this is the "write the essay, then proofread it before continuing" discipline that makes the workflow trade speed for correctness. If the user gives you a substantial correction to an earlier document mid-workflow, edit that document in place (don't append deltas) and re-check every later document it invalidates before resuming forward.

### 3a. `requirements.md` / `bugfix.md`

Structure, matching Kiro's real spec documents exactly:

```markdown
# Requirements Document

## Introduction
<1-2 paragraphs: what this feature/fix is, why it exists, the guiding design philosophy>

## Glossary
- **Term**: definition. One entry per domain term, acronym, or system name introduced anywhere in this spec — every later document reuses these terms verbatim, never redefines them.

## Requirements

### Requirement 1: <short title>
**User Story:** As a <role>, I want <capability>, so that <benefit>.

#### Acceptance Criteria
1. WHEN <trigger/event> THE <system or component> SHALL <required behavior>.
2. IF <precondition> THEN THE <system or component> SHALL <required behavior>.
3. WHILE <ongoing state> THE <system or component> SHALL <required behavior>.

### Requirement 2: <short title>
...
```

This is EARS (Easy Approach to Requirements Syntax). Every acceptance criterion MUST be a single testable `WHEN`/`IF`/`WHILE` + `SHALL` sentence — never a vague goal, never multiple behaviors chained in one criterion. Number requirements sequentially; later documents (`design.md` correctness properties, `tasks.md` `_Requirements:_` tags) reference these numbers, so renumbering after the fact is a breaking change to the whole spec — append new requirements instead of renumbering existing ones once `design.md` exists.

For a `bugfix.md`, keep the same `## Introduction` / `## Glossary` / numbered-requirements skeleton, but each requirement's user story becomes a reproduction statement ("As a user running X, I observe Y instead of Z") and acceptance criteria describe the fix's observable behavior, not new capability.

### 3b. `design.md`

Structure:

```markdown
# Design Document: {feature-name}

## Overview
<what is being built/changed and the core design philosophy in 1-3 paragraphs>

## Architecture
<a mermaid diagram (graph/flowchart/sequence) showing the major components and how they relate>

## Components
<one subsection per component: responsibility, interfaces, key pseudocode/schema>

## Correctness Properties
<numbered, falsifiable properties the implementation must satisfy — these become the property tests referenced from tasks.md>

## Audit-Derived Ground Truth (when working against an existing codebase)
| Assumed Name (Spec) | Real Name / Location | Status |
|---|---|---|
| ... | ... | CONFIRMED / VERIFY FIRST |
```

The "Audit-Derived Ground Truth" table is not decorative: whenever the spec depends on facts about an existing codebase (a config key's real name, whether a primitive exists, a file's real path), verify it against the actual repository before writing `design.md`, record the verified fact in this table, and mark anything unverified `[AUDIT-REQUIRED]` rather than guessing. Tasks that depend on an `[AUDIT-REQUIRED]` fact must not be scheduled into an execution wave until it's resolved.

### 3c. `tasks.md`

Structure:

```markdown
# Implementation Plan: {feature-name}

## Overview
<1 paragraph: what this task list implements and any global constraints>

## Tasks

- [ ] 1. <top-level task title>
  - <sub-bullet: concrete action>
  - <sub-bullet: concrete action>
  - _Requirements: 1.1, 1.2_

  - [ ] 1.1 <child task title>
    - <concrete action>
    - _Requirements: 1.3_

- [x] 2. <a completed top-level task>
  ...

## Notes
<any global notes: optional tasks, test frameworks used, ordering dependencies between phases>

## Task Dependency Graph

​```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2"] },
    { "id": 1, "tasks": ["2.1", "2.2", "3.1"] }
  ]
}
​```
```

Rules that keep this machine-parseable by both Ghosty and the real Kiro app:
- Task IDs are dot-separated hierarchical numbers (`1`, `1.1`, `2.3`) — never re-used, never renumbered after `tasks.md` is checkpointed.
- Checkbox status markers are exactly one of:
  - `- [ ]` — not started
  - `- [x]` — completed
  - `- [-]` — in progress
  Do not invent other markers (e.g. `[~]`); Kiro's own parser and the `WaveDagEngine` below only recognize these three.
  - A parent task's checkbox reflects its own status, independent of its children's — mark a parent `[x]` only once all its children are also `[x]`.
  - Every leaf task SHOULD end with a `_Requirements: X.Y, ..._` line back-referencing the `requirements.md` acceptance criteria it satisfies. This backlink is what makes the spec traceable end to end (requirement → design property → task → diff) instead of just a to-do list.
- The **Task Dependency Graph** JSON block at the end is mandatory once execution (not just planning) begins. `waves` are ordered by `id`; every task ID in a wave is assumed satisfiable only once every task in all lower-numbered waves is `completed`. A task ID appearing in `tasks.md` but omitted from every wave is never scheduled by the engine — treat that as a bug in the plan, not an intentional exclusion, unless the task is explicitly marked optional in `## Notes`.

## 4. Resuming an Existing Spec

Before writing anything, check whether `.kiro/specs/{feature-name}/` already exists:
1. Read `.config.kiro` to get `workflowType` and `specType`.
2. Read whichever documents exist. Treat `tasks.md` checkbox state as ground truth for progress — do not re-plan or re-derive status from conversation memory.
3. Continue at the first missing/incomplete document in the `workflowType` order (§2). If all three documents exist and `tasks.md` has unfinished tasks, skip straight to execution (§6).
4. This applies identically whether the spec was authored by Ghosty or by the Kiro IDE — the format has no Ghosty-specific extensions that would make a Kiro-authored spec unreadable, and vice versa.

## 5. Bootstrapping the Wave DAG Engine

You do not need local scripts. Whenever the user is ready to execute the DAG, run the following Javascript block in a single persistent `eval(language="js")` cell to load the Ghosty engine into memory:

```javascript
class WaveDagEngine {
    constructor(markdownContent, jsonDagBlock) {
        this.tasks = new Map();
        const parsed = JSON.parse(jsonDagBlock);
        this.waves = parsed.waves.sort((a, b) => a.id - b.id);
        this.currentWaveIndex = 0;

        // Parse tasks, including their on-disk checkbox status so resumed specs
        // pick up exactly where they left off instead of re-running finished work.
        const taskRegex = /^\s*-\s*\[([ xX\-])\]\s*(\d+(?:\.\d+)*)\.?\s+(.*)$/gm;
        let match;
        while ((match = taskRegex.exec(markdownContent)) !== null) {
            const marker = match[1].toLowerCase();
            const status = marker === 'x' ? 'completed' : marker === '-' ? 'in_progress' : 'queued';
            this.tasks.set(match[2], { id: match[2], description: match[3].trim(), status, waveId: 0 });
        }
        for (const wave of this.waves) {
            for (const taskId of wave.tasks) {
                if (this.tasks.has(taskId)) this.tasks.get(taskId).waveId = wave.id;
            }
        }
        // Fast-forward past any wave that is already fully completed on disk.
        while (this.currentWaveIndex < this.waves.length &&
               this.waves[this.currentWaveIndex].tasks.every(id => this.tasks.get(id)?.status === 'completed')) {
            this.currentWaveIndex++;
        }
    }

    getReadyTasks() {
        if (this.currentWaveIndex >= this.waves.length) return [];
        const currentWave = this.waves[this.currentWaveIndex];
        const readyTasks = [];
        let allCompleted = true;
        for (const taskId of currentWave.tasks) {
            const task = this.tasks.get(taskId);
            if (!task) continue;
            if (task.status === 'queued') { task.status = 'ready'; readyTasks.push(task); allCompleted = false; }
            else if (task.status !== 'completed' && task.status !== 'failed') { allCompleted = false; }
        }
        if (allCompleted) { this.currentWaveIndex++; return this.getReadyTasks(); }
        return readyTasks;
    }
}

function mapGhostyTaskToOMPAgent(description) {
    const desc = description.toLowerCase();
    if (desc.includes("research") || desc.includes("investigate")) return "explore";
    if (desc.includes("architect") || desc.includes("plan")) return "plan";
    if (desc.includes("ui") || desc.includes("css") || desc.includes("frontend")) return "designer";
    if (desc.includes("review") || desc.includes("test")) return "reviewer";
    if (desc.includes("api") || desc.includes("external")) return "librarian";
    if (desc.includes("debug") || desc.includes("optimize")) return "oracle";
    if (desc.includes("typo") || desc.includes("lint")) return "quick_task";
    return "task";
}

// Writes a task's new checkbox status back into tasks.md on disk, so the spec
// file itself (not just in-memory state) stays the resumable source of truth —
// this is what lets the Kiro IDE (or a future Ghosty session) resume correctly.
function writeTaskStatus(specPath, taskId, marker) {
    const path = `${specPath}/tasks.md`;
    const content = read(path);
    const escapedId = taskId.replace(/\./g, '\\.');
    const lineRegex = new RegExp(`^(\\s*-\\s*)\\[[ xX\\-]\\](\\s*${escapedId}\\.?\\s+.*)$`, 'm');
    write(path, content.replace(lineRegex, `$1[${marker}]$2`));
}

async function runGhostySpecInOMP(specPath) {
    const markdown = read(`${specPath}/tasks.md`);
    const dagMatch = markdown.match(/```json\n([\s\S]*?)\n```/);
    if (!dagMatch) throw new Error("No DAG JSON found in spec");

    const engine = new WaveDagEngine(markdown, dagMatch[1]);

    while (true) {
        const readyTasks = engine.getReadyTasks();
        if (readyTasks.length === 0) break;
        log(`Executing wave with ${readyTasks.length} parallel task(s)...`);

        const thunks = readyTasks.map((task) => async () => {
            task.status = 'in_progress';
            writeTaskStatus(specPath, task.id, '-');
            try {
                const ompAgentType = mapGhostyTaskToOMPAgent(task.description);
                const result = await agent(`Task ID: ${task.id}\nDescription: ${task.description}\nSpec: ${specPath}`, { agent: ompAgentType });
                task.status = 'completed';
                writeTaskStatus(specPath, task.id, 'x');
                return result;
            } catch (error) {
                task.status = 'failed';
                writeTaskStatus(specPath, task.id, ' ');
                throw error;
            }
        });
        await parallel(thunks);
    }
    log("DAG execution complete.");
}
```

## 6. Dispatching

In a *separate*, subsequent `eval` cell, invoke the runner on the current project's spec path:

```javascript
await runGhostySpecInOMP('.kiro/specs/{feature-name}');
```

Because `runGhostySpecInOMP` writes real `[x]`/`[-]`/`[ ]` checkbox updates back into `tasks.md` as it goes (not just in-memory state), the on-disk spec is always an accurate, resumable snapshot — closing the OMP session mid-run and reopening the same spec in the Kiro IDE (or a fresh Ghosty session) shows exactly which tasks completed, which were in flight, and which are still queued.
