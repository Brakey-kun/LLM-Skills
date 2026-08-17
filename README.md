# Personal LLM Skills & Workflows

This repository contains custom, modular behaviors and workflows that I've built for my own daily day-to-day interactions and projects with Claude and other agentic LLMs. 

These skills act as extended system instructions or workflows, turning conversational AI into powerful, structured workflow engines for research, design, development, and context management.

## Repository Structure

Each skill is self-contained in its own independent folder and includes its own `SKILL.md` along with any required references or assets. This structure is designed to be highly portable and accommodating to most AI tool architectures (like MCP servers, custom GPTs, Claude Projects, or autonomous agent environments).

```text
.
├── skills/
│   ├── aggregate-deep-research/
│   ├── app-idea-to-build-prompt/
│   ├── context-handoff/
│   ├── context-resume/
│   ├── external-delegation/
│   ├── kiro-spec/
│   ├── project-uphaul/
│   └── yt-deep-extraction/
├── claude-web-skills/
│   └── *.skill (packaged web skills)
└── README.md
```

## Available Skills

### 1. `kiro-spec`
**Spec-Driven Development & Wave DAG Engine**
Injects the Kiro Spec-Driven Development (SDD) workflow and a parallel execution engine natively into the workspace.
- **Documentation First:** Forces the creation of rigorous requirements, architectural designs, and task lists before execution.
- **Wave DAG Execution:** Parses tasks into dependency waves and dynamically schedules them across specialized agents in parallel.
- **Quality & Trackability:** Trades immediate speed for deliberate correctness, allowing drafts to be reviewed and modified before code is written.
*Use this when starting complex, multi-step projects where code quality, architectural integrity, and strict traceability matter more than raw speed.*

### 2. `aggregate-deep-research`
**Multi-Phase Deep Research Pipeline**
A robust, model-agnostic pipeline for comprehensive research. It transforms a simple prompt or topic into a full-fidelity interactive HTML guide through a strict multi-phase process:
- **Capability Probe & Web Research:** Gathering 50-1000 sources.
- **Decomposition:** Breaking the topic down into isolated aspects.
- **Standalone Reports:** Generating specific reports with claim-source bindings and numbers ledgers to prevent hallucinations.
- **Synthesis:** Aggregating data into a master synthesis and a final interactive HTML lesson.
*Ideal for critical personal research or generating comprehensive educational materials.*

### 3. `app-idea-to-build-prompt`
**App Idea → Concept GUI → Build Prompt**
Guides the full workflow for turning a raw app or product idea into concrete artifacts.
- **Concept GUI:** Creates an interactive HTML/CSS/JS concept that you can click through.
- **Build Prompt:** Generates a comprehensive and structured prompt designed to be handed off to an autonomous coding agent (like Claude Code) for the actual build.
*Use this when pitching an idea to flesh out features, make UI/UX design choices, and prepare a solid spec before development starts.*

### 4. `context-handoff`
**Lossless Conversation Exporter**
Exports the current conversation context into a structured, lossless package.
- Creates a human-readable Markdown transcript and a canonical JSON record.
- Bundles any uploaded files or images into a zip.
*Perfect for long conversations hitting context limits, sharing context with team members, or migrating a session to a new AI workspace without starting from scratch.*

### 5. `context-resume`
**Context Loader & Resumer**
The receiving-end counterpart to `context-handoff`.
- Reads the handoff package (`handoff.json`, `handoff.md`, and zip archives).
- Rehydrates the AI's context with all prior decisions, constraints, and files so work can continue seamlessly.
*Triggered at the start of a new conversation by uploading the handoff package to pick up exactly where you left off.*

### 6. `external-delegation`
**Cross-Session AI Handoff Prompt Generator**
Crafts a self-contained delegation prompt for handing off work to another AI session on a different account or platform.
- Translates current context, decisions, and codebase state into an over-specified prompt.
- Ensures the receiving model has exactly what it needs to continue without assumptions.
*Use when you need another model to continue work but the session boundary erases context.*

### 7. `project-uphaul`
**Project Audit & Overhaul Pipeline**
Runs a full, dynamic audit-and-overhaul pipeline on a project or codebase you didn't build or aren't familiar with.
- **Sequences specialist skills:** Calls router, review, and autoresearch skills in a specific order.
- **Diagnosis & Execution:** Classifies the project, scopes what's wrong, checks with the user, and executes the fix on a branch.
- **Bundled Capabilities:** Built using the Meta Skill Router, Code Overhaul Skill, Autoresearch Skill, and ARA Rigor Reviewer.
*Trigger this when you inherit a messy project, want to audit code built by a weaker model, or need a structured quality review.*

### 8. `yt-deep-extraction`
**YouTube Channel Deep Research & Extraction**
Deeply and losslessly extracts everything from a YouTube channel, playlist, or video list.
- Gathers metadata, full transcripts, visuals, chapters, and creator claims.
- Compiles per-video research files, a cross-referenced master report, and an interactive HTML lesson.
- Model and runtime agnostic; operates with whatever tools the host agent has available.
*Use this whenever you want to learn from, archive, build a course from, or mine knowledge out of any YouTube channel or set of videos.*

## How to Use

This repository offers skills in two different formats depending on where you intend to use them:

### 1. Normal Skills (`skills/`)
These are uncompressed, raw directory structures containing the `SKILL.md` and any associated reference files. 
- **Use for:** Terminal-based or CLI harnesses like Claude Code, Hermes, OMP (`omp.sh`), Odysseus, or custom LangChain/Flowise workflows.
- **Why:** They are easily readable by humans, version-controllable, and natively executable by most local autonomous agent environments that scan a local `skills` directory.

### 2. Claude Web Skills (`claude-web-skills/`)
These are packaged `.skill` files (which are actually ZIP archives containing the raw skill directories). 
- **Use for:** The Claude.ai web interface (Claude Projects).
- **Why:** You can upload these `.skill` files directly as project knowledge base attachments, allowing the web version of Claude to read the internal structure and instructions seamlessly.

## Credits

The `project-uphaul` skill bundles and builds upon several fantastic open-source skills:
- **Meta Skill Router** — ananddtyagi/cc-marketplace (Anand Tyagi)
- **Code Overhaul Skill** — ehmo/code-overhaul-skill (Rasty Turek)
- **Autoresearch Skill** — ehmo/autoresearch-skill (Rasty Turek)
- **ARA Rigor Reviewer** — Orchestra-Research/AI-Research-SKILLs (Orchestra Research), originally from ARA-Labs/Agent-Native-Research-Artifact
