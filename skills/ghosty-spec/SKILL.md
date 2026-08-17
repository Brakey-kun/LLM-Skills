---
name: ghosty-spec
description: Injects the Ghosty Spec-Driven Development (SDD) workflow and parallel Wave DAG execution engine natively into any OMP workspace.
---

---
name: ghosty-spec
description: Injects the Ghosty Spec-Driven Development (SDD) workflow and parallel Wave DAG execution engine natively into any OMP workspace.
---

# Ghosty Spec-Driven Development (SDD) & Wave DAG Engine

Use this skill whenever a user wants to execute a project using the **Ghosty SDD Workflow** or requests parallel task execution using **DAG execution waves**.

## 1. The Workflow
If the spec files do not exist, create them in `.kiro/specs/{feature-name}/`:
1. `requirements.md` (EARS-formatted acceptance criteria)
2. `design.md` (Architecture and Correctness Properties)
3. `tasks.md` (Numbered task list and a ```json block defining execution "waves")

## 2. Bootstrapping the Engine
You do not need local scripts. Whenever the user is ready to execute the DAG, run the following Javascript block in a single persistent `eval(language="js")` cell to load the Ghosty engine into memory:

```javascript
class WaveDagEngine {
    constructor(markdownContent, jsonDagBlock) {
        this.tasks = new Map();
        const parsed = JSON.parse(jsonDagBlock);
        this.waves = parsed.waves.sort((a, b) => a.id - b.id);
        this.currentWaveIndex = 0;
        
        // Parse tasks
        const taskRegex = /- (\d+\.\d+)\s+(.*)/g;
        let match;
        while ((match = taskRegex.exec(markdownContent)) !== null) {
            this.tasks.set(match[1], { id: match[1], description: match[2], status: 'queued', waveId: 0 });
        }
        for (const wave of this.waves) {
            for (const taskId of wave.tasks) {
                if (this.tasks.has(taskId)) this.tasks.get(taskId).waveId = wave.id;
            }
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

async function runGhostySpecInOMP(specPath) {
    const markdown = read(`${specPath}/tasks.md`);
    const dagMatch = markdown.match(/```json\n([\s\S]*?)\n```/);
    if (!dagMatch) throw new Error("No DAG JSON found in spec");
    
    const engine = new WaveDagEngine(markdown, dagMatch[1]);

    while (true) {
        const readyTasks = engine.getReadyTasks();
        if (readyTasks.length === 0) break;
        log(`🌊 Executing Wave with ${readyTasks.length} parallel tasks...`);
        
        const thunks = readyTasks.map((task) => async () => {
            task.status = 'in_progress';
            try {
                const ompAgentType = mapGhostyTaskToOMPAgent(task.description);
                const result = await agent(`Task ID: ${task.id}\nDescription: ${task.description}\nSpec: ${specPath}`, { agent: ompAgentType });
                task.status = 'completed';
                return result;
            } catch (error) {
                task.status = 'failed';
                throw error;
            }
        });
        await parallel(thunks);
    }
    log("DAG Execution Complete.");
}
```

## 3. Dispatching
In a *separate*, subsequent `eval` cell, invoke the runner on the current project's spec path:

```javascript
await runGhostySpecInOMP('.kiro/specs/{feature-name}');
```
