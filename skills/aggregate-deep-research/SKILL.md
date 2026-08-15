---
name: aggregate-deep-research
description: "Multi-phase deep research pipeline: capability probe → web research → decompose into aspects → standalone deep-research reports per aspect (50–1000 sources, claim–source binding, numbers ledger) → master synthesis → full-fidelity interactive HTML guide/lesson (frontend-design enforced). Model-agnostic and runtime-agnostic: mechanical anti-hallucination protocol makes output fidelity independent of model strength, and an environment adaptation layer maps the pipeline onto whatever tools the host agent has. Use for any subject, from a title-only brief to full context, including critical personal research."
version: 2.0.0
author: Hermes Agent (agent-agnostic — usable by any tool-capable model/runtime)
tags: [research, writing, html, guide, pipeline, reports, design, education, fidelity, agent-agnostic]
platforms: [windows, linux, macos]
runtimes: [hermes, omp.sh, odysseus, claude, opencode, any-agent-with-web+file-tools]
triggers:
  - research and create a guide on
  - deep research on
  - turn this into a report and html guide
  - make a comprehensive guide about
  - research then build an interactive lesson on
  - critical research on
---

# Aggregate Deep Research Pipeline

## When to Use

Any time you need to deeply research a subject, produce structured reports covering every angle, synthesize into a master document, and deliver a polished interactive HTML guide/lesson. Works from a title-only brief (will research first) or from full context you provide.

## How to Call It

Replace `{SUBJECT}` with your topic (title, phrase, or detailed brief).
Replace `{SUBJECT_DETAILS}` with any specific angles, constraints, or context (optional).
Replace `{GOAL_INTENT}` with what you want to **achieve** with the research output — this steers orientation, data gathering, synthesis, and HTML design (optional, but strongly recommended for targeted outcomes).
Replace output directory if desired (default: `~/hermes-workspace/{slug}/`).

```
I want to use the aggregate-deep-research skill on:
Subject: {SUBJECT}
Subject Details (optional): {SUBJECT_DETAILS}
Goal/Intent (optional): {GOAL_INTENT}
```

**Goal/Intent deep dive** (see [Cardinal Principles §5](#5-goalintent-driven-research-orientation) for full details):

The goal is what drives the entire pipeline beyond just the subject matter. A same subject with different goals produces different research, different synthesis, and different HTML:

| Same Subject → Different Goals | Impacts |
|-------------------------------|---------|
| Subject: "Solar panels" | |
| → Goal: "Find a business model for residential installation" | Research: market sizing, competitor pricing, customer acquisition costs. HTML: startup-focused. |
| → Goal: "Understand the science to teach high schoolers" | Research: physics of photovoltaics, efficiency curves, installation diagrams. HTML: lesson-plan oriented. |
| → Goal: "Identify the best consumer brand for my home" | Research: brand comparisons, reliability data, ROI calculators. HTML: buyer's-guide format. |

When no goal is provided, the pipeline defaults to **open-ended comprehensive research** — covering all angles equally.

The agent will automatically execute the full pipeline below.

---

## Phase −1: Environment & Model Adaptation Layer (RUN FIRST, ALWAYS)

This skill must produce the **same fidelity of output regardless of which model runs it** (frontier models, or free/smaller models such as OpenCode Zen free tiers) and **regardless of which agent runtime hosts it** (Hermes, omp.sh, Odysseus, Claude, or any other tool-capable agent). To achieve that, the pipeline begins with an explicit self-calibration step. Do not skip it.

### A. Capability Probe (before any research)

Enumerate the tools actually available in the current runtime and record the result in a short `_environment.md` note in the output directory. Probe for each capability by name-agnostic function, not by tool name (different runtimes name tools differently):

| Capability | Look for (any of) | If ABSENT, fallback |
|------------|-------------------|---------------------|
| **Web search** | `web_search`, `search`, `browser_navigate`+search engine, curl/fetch of search APIs | Use direct-URL fetching of known-reliable sources (HN Algolia, curated lists); declare reduced coverage in `_environment.md` and in the final report's methodology section |
| **Page fetch** | `web_fetch`, `browser_navigate`, `curl`/`wget` via shell | Rely on search snippets only; mark every snippet-only claim as `[snippet-only]` in source index |
| **File write** | `create_file`, `write_file`, shell heredoc, Python `open()` | Emit full file contents in chat, clearly delimited, with filenames, for manual saving |
| **Code execution** | `execute_code`, `bash`, `python` | Skip data-driven HTML generation; hand-write HTML but MANDATORY: run the manual item-count checklist (Phase 4) line by line |
| **Visual verification** | `browser_vision`, screenshot tools, headless render | Substitute with static checks: grep for `\U`/`\u` literals, `&amp;quot;`, unclosed tags, count of `class="idea-card"` vs. expected N |
| **Parallel tool calls** | batched calls in one turn | Run queries sequentially; reduce per-round query count to avoid rate limits; extend rounds instead |

**Rule**: The pipeline's *quality bar never lowers* when a capability is missing — only the *method* changes, and every substitution is disclosed in the methodology/`_environment.md`. Missing tools reduce speed and breadth honestly, never silently.

### B. Model-Robustness Protocol (anti-hallucination, model-agnostic)

Smaller/free models drift, invent, and paraphrase loosely under long contexts. These rules are **mandatory mechanical procedures**, not suggestions, precisely so that a weaker model following them mechanically produces output as faithful as a stronger model:

1. **Claim–Source Binding**: Every factual claim written into any report MUST be written in the same breath as its source reference (e.g. `[HN-14]`, `[YT-03]`). If you are about to write a claim and cannot name its source index entry, DO NOT write the claim. There is no "common knowledge" exemption inside research reports — unsourced background may appear only in clearly-labeled `> Context (agent knowledge, unverified):` blockquotes.
2. **No retro-citation**: Never write prose first and "add citations later". Citations are written inline at claim-time. Retro-citation is how hallucinated sources happen.
3. **Verbatim quarantine**: Anything inside quotation marks or a blockquote must be copy-paste verbatim from a fetched page that is still in context. If the page has scrolled out of context, re-fetch before quoting, or convert the quote to an attributed paraphrase marked `[paraphrase]`.
4. **Numbers ledger**: Maintain a running `_numbers.md` ledger: every statistic, price, count, date, or percentage gets one line: `value | claim | source | fetched-or-snippet`. Before Phase 2 synthesis, re-read the ledger; any number not in the ledger may not appear in the synthesis or HTML.
5. **Chunked writing with checkpoints**: Weak models degrade over long generations. Write reports in ≤150-line chunks, and after each chunk re-read the report's own Source Index before continuing. Never generate a 500-line report in one pass.
6. **Self-audit pass (mandatory per report)**: After finishing each Phase 1 report, perform one adversarial re-read with exactly three questions: (a) does every claim have an inline source tag? (b) does every source tag exist in the Source Index? (c) do the numbers match the `_numbers.md` ledger? Fix or delete anything that fails. Deletion is always preferable to an unsourced claim.
7. **Uncertainty is written, not resolved**: If sources conflict or data is missing, write `⚠️ conflicting: A says X [src], B says Y [src]` or `∅ no data found for Z after N queries`. Never fill gaps with plausible-sounding estimates. An honest hole is a valid research finding.
8. **Context-loss recovery**: If at any point the agent is unsure what was already researched (context truncation, session resume), re-read the on-disk reports and `_numbers.md` before writing anything new. Files on disk are the ground truth, not the model's memory of them.

### C. Critical Research Mode

When the user marks the research as **critical** (personal decisions, health, finance, legal, safety, or explicitly says "critical research"), tighten the protocol further:

- Minimum **2 independent sources** for any claim that could influence a decision; single-source claims are tagged `[single-source]` prominently.
- Primary sources preferred and tagged: `[primary]` (official docs, filings, datasets, the person/company itself) vs `[secondary]` (press, blogs) vs `[tertiary]` (aggregators, forums).
- Dates on everything: every claim carries its source's publication date; stale data (older than the domain's typical churn rate) is flagged `[stale: YYYY-MM]`.
- The HTML gets a visible **Methodology & Confidence panel**: source counts, verification level per section, and a plainly-worded limitations list. In critical mode this panel is not optional and not hidden in a footer.

### D. Runtime Adaptation Notes (known environments)

- **Hermes**: full toolset; use `execute_code` + `browser_vision` paths as written below. Source-reliability table below reflects Hermes browser behavior.
- **omp.sh / Odysseus / other CLI agents**: probe for shell + fetch. If no visual browser, use the static-check fallbacks (grep-based HTML verification). If workspace path `~/hermes-workspace/` doesn't exist or isn't conventional, use the runtime's working directory or `./research-output/{slug}/` — never hardcode a path that fails; create-and-verify the directory in Phase 0.
- **Claude (claude.ai / Claude Code)**: use native `web_search`/`web_fetch` (more reliable than browser emulation — the source-reliability table's CAPTCHA caveats mostly don't apply), bash for generation/verification, and output-directory conventions of the host (`/mnt/user-data/outputs` on claude.ai).
- **Unknown runtime**: run the Capability Probe, write `_environment.md`, proceed with the closest matching profile.

### E. Windows/MSYS Terminal Workaround (Critical for Hermes on Windows)

When running on Windows with git-bash/MSYS, the `terminal` tool frequently fails with `fork: Resource temporarily unavailable` / `exit code 0xC0000142` due to process spawn limits. This affects:
- Directory creation (`mkdir`)
- File writing via shell heredoc/redirect
- Any shell command that forks

**Mandatory workaround**: Use `execute_code` with Python stdlib for ALL filesystem operations:
```python
# Directory creation
import os
os.makedirs(path, exist_ok=True)

# File writing (handles large content, UTF-8, emoji safely)
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

# File reading
with open(path, "r", encoding="utf-8") as f:
    content = f.read()
```

**Never use `terminal` for file I/O on Windows/MSYS**. Reserve `terminal` only for: git, package managers, build commands, processes that must run in shell. This workaround is now part of the Environment Adaptation Layer — probe for it in Phase −1 and record in `_environment.md`.

---

## Cardinal Principles: Data Fidelity & Neutrality

These principles apply to **every phase** of the pipeline — raw data collection, summarization, synthesis, visualization, and final HTML output.

### 1. Represent Reality, Not Intent or Bias

> **Never let a desired outcome, personal opinion, or prevailing online sentiment distort what the data actually says.**

- **Pessimistic data** → represent as pessimistic. Do not spin negative findings into silver linings.
- **Optimistic data** → represent as optimistic. Do not undermine positive findings with "yes, but" caveats that come from your own skepticism, not from the data.
- **Neutral/mixed data** → represent as neutral/mixed. Do not force a directional reading.
- **Contradictory data** → surface the contradiction honestly with both sides represented, rather than picking a side.

Rule of thumb: If you find yourself adding words like "unfortunately", "sadly", "luckily", "promisingly", or "interestingly" as editorial framing, **stop** — those signal that your voice is replacing the data's voice. Let the facts speak with their own weight.

### 2. Neutrality on External Opinions

> **Do not adopt or amplify the bias of any source, community, or expert — even when the source's opinion is strong.**

- When citing online opinions (Reddit threads, HN comments, expert takes), **report what was said, neutrally**, without amplifying the sentiment or dismissing it. Use attributive framing: "X community expressed concern about Y" rather than "Y is terrible" or "Y is amazing".
- **Do not cherry-pick** supportive or dismissive quotes to fit a narrative. If multiple viewpoints exist, represent the range.
- **Omit editorializing** — the phrase "notably" before a finding, "importantly" before your own insight, or "of course" before something you consider obvious are all signals that the agent is substituting judgment for data.

### 3. Accuracy Mandate Across All Outputs

This principle applies equally to:

| Output Type | What Accuracy Means |
|-------------|-------------------|
| **Textual data/summaries** | Every claim is traceable to a cited source. No hallucinated statistics. No invented quotes. |
| **Visual data (charts, graphs, infographics)** | Axes are scaled honestly (no misleading truncation). Proportions are exact. Color coding is accessible and value-neutral (green does not always mean "good", red does not always mean "bad" — use labels). |
| **Interactive elements** | Toggle states, filter results, and computed summaries must reflect the underlying data exactly. Do not hardcode "top N" lists with invented values. |
| **Synthesis & conclusions** | The synthesis must reflect the balance of evidence, not a single thread. If 70% of sources say X and 30% say Y, say that — do not state X as fact and bury Y in a footnote. |
| **Raw data excerpts** | When quoting original data, quote verbatim. Do not paraphrase in a way that changes meaning. Use blockquotes for verbatim extracts. |

### 4. Visual-Text Coupling Rule

> **Every visual or interactive element MUST be paired with text that explains, details, or contextualizes the data that visual represents.**

A chart, grid, or filterable list without adjacent explanatory text is incomplete — the reader must be able to understand **what** they're seeing, **why** it matters, and **how** it connects to the research.

Implementation:
- **Charts/graphs**: preceded by 2-3 sentences explaining what the chart shows and what key takeaway to draw.
- **Filterable cards/tables**: preceded by a brief instruction/context paragraph and followed by a legend or key if symbols are used.
- **Stat callouts**: each stat callout card is accompanied by a prose sentence giving the source/context of the number.
- **Pattern grids**: each card has a self-contained title + description; the grid section has a section-intro paragraph.

Exception: A purely decorative visual (hero illustration, divider, background glow) needs no paired text. But any visual that **conveys data** needs text.

### 5. Goal/Intent-Driven Research Orientation

> **The pipeline's research orientation, data gathering strategy, synthesis structure, and HTML design are steered by an optional "goal/intent" field — not just the research theme/title.**

The goal is what the end user actually wants to **achieve** with the research output. It transforms a generic research brief into a purpose-driven investigation:

| Field | Purpose | Example |
|-------|---------|---------|
| **Theme/Title** | What the research is *about* (subject) | "App ideas" |
| **Details (optional)** | Constraints, angles, scope | "Web apps, ready-to-build, solving real problems" |
| **Goal/Intent (optional)** | What the user wants to *achieve* with the result | "Find an app idea I can make using AI + personal knowledge to help people globally, gain reputation as a successful developer, and generate 400k+ USD net via single-purchase pricing ($5-$40)" |

When a goal is provided:
- **Research orientation** shifts toward what serves the goal (e.g. "single-purchase viable apps → research pricing models, indie success stories, market gaps")
- **Data gathering** prioritizes sources most relevant to the goal (e.g. for single-purchase: Steam, Itch.io, Gumroad, indie dev post-mortems)
- **Synthesis structure** is organized by goal-aligned criteria (e.g. "viability as single-purchase" instead of pure complexity ranking)
- **HTML design** frames the narrative around the goal (e.g. hero section speaks to the user's ambition, filters are goal-relevant)

If no goal is provided, the pipeline defaults to open-ended comprehensive research.

### 6. Adaptation to the Research's Own Constraints, Theme & Context

> **The pipeline adapts its form to the subject — never the subject to the pipeline's form.**

The templates in this skill (tiers, tab bars, dark theme, source categories) are defaults, not straitjackets. Before Phase 1, explicitly decide and record in `_environment.md`:

- **Domain-appropriate source mix**: an academic subject weights papers/preprints/official datasets over Reddit; a consumer-product subject weights reviews/forums over papers; a local/regional subject weights local-language sources and official portals. The 8–10-category distribution rule still applies — the *categories themselves* change per subject.
- **Domain-appropriate structure**: the 4-tier complexity classification fits build-effort subjects; a medical or historical subject needs its own natural axes (evidence level, chronology, mechanism). Invent the axes the data itself suggests; never force ideas-mining structure onto non-ideas subjects.
- **Theme-appropriate presentation**: the dark SaaS aesthetic is the default, but a somber, sensitive, or formal subject (health outcomes, historical tragedy, legal analysis) must drop playful elements (confetti, emoji-heavy badges, "surprise & delight") in favor of restrained, respectful presentation. Fidelity includes *tonal* fidelity.
- **Language & locale**: research and present in the language(s) where the subject's best data lives; if the user's context implies a locale, include locale-relevant sources and units, clearly labeled.
- **User constraints are hard constraints**: budget, timeframe, legal jurisdiction, hardware, skill level stated in Details/Goal filter what counts as an actionable finding — but they never distort what the data says (Principle 1 still wins: a constraint can exclude an option from recommendations, but the excluded option's data is still reported accurately).

---

## Pipeline Steps

The agent follows exactly these phases in order. Each phase must complete before the next begins — no skipping, no merging.

### PHASE 0: Setup & Scout — Context Gathering

> **Context gathering default**: **Normal Search** (10–50 sources) — enough to decompose the subject, identify aspects, collect initial links.
> **Upgrade to Deep Research** (50–1000 sources) if the subject is complex, niche, or has scattered/obscure data.

1. Run the **Capability Probe** (Phase −1) if not already done; write `_environment.md`.
2. Create the output directory at the runtime's convention (`~/hermes-workspace/{slug}/` on Hermes; `./research-output/{slug}/` or the host's output dir elsewhere) and verify it exists before proceeding.
3. Search the web for the subject using multiple parallel queries covering different angles (sequential rounds if the runtime lacks parallel calls).
4. **Choose decomposition strategy** — two valid approaches:
   - **Aspect-based** (default): Identify 4-7 natural aspect categories covering the subject comprehensively. Best for technical/explanatory subjects.
   - **Source-based** (alternative): Identify 4-7 distinct information sources or communities known to discuss the topic. Best for mining opinions, problems, ideas, or trends from the internet (e.g. forums, social media, Q&A sites, curated lists).
5. List the decomposition and confirm before proceeding.

#### Research Depth Definitions

Two explicit research modes, defined at the pipeline level:

| Mode | Sources per Aspect | Purpose | Output Characteristics |
|------|-------------------|---------|----------------------|
| **🔬 Normal Search** | **10–50 sources** | General context, background understanding, link gathering, quick information retrieval | 1–2 paragraphs per unit. Broad overview. Used ONLY for contextual gathering (Phase 0 setup). |
| **🧪 Deep Research** | **50–1000 sources** | Deep, comprehensive, well-organized, deeply detailed analysis | Full report per aspect (≥300 lines). Rich source index tables. Actionable insights, data points, pitfall analysis. **REQUIRED for every aspect/sub-research in the pipeline.** |

**Minimum per-aspect target**: 50 sources. **Suggested target**: ~200 sources. **Maximum**: 1000 sources per aspect.

**Source-counting honesty**: a "source" is a distinct page/thread/video/document actually retrieved (or its snippet actually read) — not a search-results page, not a duplicate URL, not an imagined community. The Source Index count must equal the number of real entries; never inflate counts to hit the floor. If the floor is genuinely unreachable for a niche aspect after exhaustive enrichment sweeps, record the real count with an explicit `⚠️ floor not met after N sweeps` note — an honest 37 beats a fabricated 50.

#### Context Gathering Mode

Contextual gathering (Phase 0 scout queries) uses **Normal Search (10–50 sources)** by default — enough to decompose the subject, identify aspects, and collect initial links for deeper drilling.

However, if the subject is **complex, niche, or has scattered/obscure data**, upgrade context gathering to **Deep Research (50–1000 sources)** — the subject is too poorly indexed or specialized to rely on quick link gathering alone. Triggers:
- Academic/esoteric/arcane topics
- Very new or rapidly evolving domains (few canonical sources)
- Subjects where information is spread across many small, specialized sources
- Anti-pattern: assuming a general topic is niche when it's not. Use judgment.

#### Scaling Strategy: Normal → Deep

The pipeline always starts with context gathering (Normal Search), then transitions to Deep Research for every aspect:

1. **Context gathering** (Phase 0): Normal Search (10–50 sources) → unless complex/niche/scattered → Deep Research (50–1000 sources).
2. **Each aspect report** (Phase 1): **ALWAYS Deep Research** (50–1000 sources). No aspect is done with Normal Search.
3. **Iterative enrichment**: If after Deep Research an aspect is shallow (< 50 unique sources cited), run additional sweeps targeting uncovered source categories until the floor is met.

| Phase | Default Mode | Source Range | Exception |
|-------|-------------|--------------|-----------|
| Phase 0 (Setup & Scout) | Normal Search | 10–50 | Complex/niche/scattered → Deep Research |
| Phase 1 (Aspect Reports) | Deep Research | **50–1000** | Never Normal Search for any aspect |
| Phase 2 (Master Synthesis) | Aggregation | All phase 1 sources | N/A |
| Phase 3 (HTML Guide) | Derived | N/A | N/A |

#### Source Distribution Requirement

When scaling to 50+ sources per aspect, distribute across AT LEAST 8-10 distinct categories (Reddit subs, HN queries, YouTube, podcasts, curated lists, Q&A forums, review platforms, social media, publications, real-life domains) to avoid source bias.

**Iterative enrichment pattern**: Start with deep research per aspect → check coverage → if shallow (<50 sources), run additional targeted sweeps. Each enrichment round adds more sources merged into the master.

**HN Comment-Mining Pattern for Industry Pain Research**: When researching industry-specific problems or underserved markets, move beyond story/thread search and mine **comments** directly. HN comments contain high-signal pain signals that story titles miss:

```python
# Search HN comments (not stories) for industry-specific pain signals
# Use a different endpoint: tags=comment instead of tags=story
def fetch_hn_comments(query, hits=50):
    url = f"https://hn.algolia.com/api/v1/search?query={quote(query)}&tags=comment&hitsPerPage={hits}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())['hits']
```

This pattern is especially effective for:
- Finding underserved industries (legal, insurance, healthcare) — commenters name the exact software they hate and why
- Surface pricing pain points ("Adobe is too expensive", "QuickBooks is terrible for freelancers")
- Discovering niche verticals (veterinary, pharmacy, elder care, addiction recovery)

After collecting comments across 10-15 targeted industry queries, deduplicate by `objectID`, extract industry frequency counts, and surface the most-mentioned pain points. This yields a "heat map" of industry opportunity that story-only search misses.

#### Research Source Reliability (Agent Browser Context)

> Scope: this table reflects **browser-emulation runtimes** (Hermes). Runtimes with native search/fetch APIs (Claude web_search, API-backed agents) largely bypass the CAPTCHA problems — on those, Reddit/Google content is reachable via the native search index and the ❌ rows below relax to ⚠️ or ✅. Re-probe per runtime; record findings in `_environment.md`.

Not all web sources are equally accessible. Based on observed behavior with browser-based research:

| Source | Typical Reliability | Notes |
|--------|-------------------|-------|
| **HN Algolia** (`hn.algolia.com`) | ✅ High | Reliable, no CAPTCHA, excellent search API |
| **YouTube** (`youtube.com`) | ✅ High | Works for search and video description reading |
| **DuckDuckGo Lite** (`lite.duckduckgo.com`) | ⚠️ Mixed | Sometimes works, sometimes CAPTCHAs |
| **Bing** (`bing.com`) | ⚠️ Mixed | Works initially, CAPTCHAs after several queries |
| **Curated lists** (blogs, IndieHackers, Budibase, etc.) | ✅ High | Direct site access works when you have the URL |
| **Reddit** (`reddit.com`, `old.reddit.com`) | ❌ Low | Cloudflare/JS challenge blocks almost always |
| **Google** (`google.com`) | ❌ Low | CAPTCHA blocks on automated access |
| **Product Hunt** (direct) | ⚠️ Mixed | Sometimes blocks, sometimes works |

**Fallback strategy**: When primary search is blocked:
- HN Algolia is the most reliable for tech/business topics
- YouTube search works consistently
- Curated list articles (known URLs) load reliably
- Agent's knowledge of community patterns is a legitimate fallback for well-known communities (HN, Reddit, etc.)
- Try alternate search queries or DDG lite before giving up on a source

#### Parallel Research Queries

Launch searches in parallel (within the same tool call batch) to maximize coverage before any single source gets rate-limited:

```python
# Example parallel search pattern
queries = [
    "site:reddit.com app ideas simple problem",
    "what small inconvenience needs an app",
    "\"wish this existed\" tool website",
    "micro saas ideas collection",
    "simple app solves everyday problem"
]
```

#### Browser-Based Data Extraction Technique

When hitting search or API endpoints (like HN Algolia, GitHub API, or Bing), the `browser_snapshot` often shows only generic markup — the actual content is in the DOM text or a JSON tree, not the accessibility tree. Use these patterns:

1. **`browser_console` with JS expression** — after `browser_navigate`, extract text via `document.body.innerText.substring(0, N)` to get the full JSON response text or visible page text that the snapshot missed. For list pages, use `Array.from(...)` to extract structured data:

   ```javascript
   // Extract YouTube video titles + URLs from search results
   Array.from(document.querySelectorAll('#video-title'))
     .slice(0,20)
     .map(v => v.textContent.trim() + ' | ' + v.href)
     .join('\n')
   
   // Get total item count from a result page
   document.querySelectorAll('ytd-video-renderer').length + ' videos'
   ```

2. **`browser_console` for JSON API pages** — when the URL returns raw JSON (e.g. `hn.algolia.com/api/v1/...`), use `document.body.innerText` to capture the full JSON body, then `JSON.parse()` in `execute_code`:

   ```python
   # Fetch results via browser_navigate + console extraction
   # (Use this when terminal/curl is unreliable; otherwise prefer execute_code with urllib.request)
   ```

3. **Preferred approach for stable APIs**: use `execute_code` with Python's `urllib.request` to fetch JSON APIs directly — this is more reliable than browser navigation for data-heavy sweeps:

   ```python
   import json, urllib.request, urllib.parse
   url = f"https://hn.algolia.com/api/v1/search?query={urllib.parse.quote(q)}&tags=story&hitsPerPage=50"
   req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   with urllib.request.urlopen(req, timeout=15) as resp:
       data = json.loads(resp.read().decode())
   ```

**Rule of thumb**: Use `browser_navigate` + `browser_console(expression=...)` when you need visual context or the page uses JS to render content. Use `execute_code` with `urllib.request` when the endpoint returns JSON and you need to process many pages/entries.

### PHASE 1: Deep Research Reports — One Per Decomposition Unit

> **Requirements**: Every aspect/sub-research MUST be **Deep Research** (50–1000 sources per aspect), written under the **Model-Robustness Protocol** (Phase −1 §B): claim–source binding, verbatim quarantine, numbers ledger, chunked writing, and the per-report self-audit pass are all mandatory regardless of model strength. No aspect is done with Normal Search. Phase 0 context gathering may have been Normal Search, but Phase 1 is always Deep Research. If an aspect has fewer than 50 unique sources cited after initial sweeps, run additional enrichment sweeps across uncovered source categories until the 50-source floor is met.

For each identified unit (aspect or source), write a comprehensive Markdown report saved as `report-0{N}-{slug}.md`.

Each report MUST include:
- **Executive Summary** (3-5 bullet points at the top)
- **Source Index table** — numbered source catalog at the top listing every distinct source mined in that report, with columns for source name, type, signal rating (★), and a "Notable Threads/Posts" column. This becomes the cross-reference key for all citations in the report body.
- **Deep Analysis** (structured with subheadings — trace the logic end to end)
- **Actionable Guidance** (how to apply or implement — this is not just theory)
- **Data Points** (statistics, benchmarks, pricing ranges, market sizes — cite specific numbers, not vague estimates)
- **Tools & Resources** (specific tools, platforms, methods with names)
- **Common Pitfalls** (what goes wrong and how to avoid it)

#### Source Index Notation System

When mining ideas/opinions/recommendations across multiple sources, use a numbered, cited cross-reference system:

```
| # | Idea | Sources | Effort | Validation |
|---|------|---------|--------|------------|
| 33 | Receipt Splitter with Photo | Reddit[2][3], App Reviews | 1-2 days | Test with friend group |
```

The brackets reference entries in the Source Index table at the top of the report (e.g. `Reddit[2]` = entry #2 in the source index, which is r/AppIdeas). This lets readers trace every idea back to its originating source without breaking the reading flow.

For reports with >50 items, group ideas into complexity/effort tiers with sub-headings (e.g. "TIER 1 — Static / Single-Page Tools", "TIER 2 — Simple Backend", "TIER 3 — Dynamic Web App", "TIER 4 — Full Platform"). Within each tier, items are ordered from simplest to most complex.

Reports should be 300-800 lines each depending on depth. No vague filler — every paragraph should carry information density.

### PHASE 2: Master Synthesis Report

1. Read all phase 1 reports.
2. Choose synthesis format based on subject type:
   - **Narrative synthesis** (default): Weaves all aspects into a coherent story showing interconnections, cross-reference table linking sub-topics, ends with a phased roadmap. Best for explanatory/technical subjects.
   - **Ordered-by-simplicity synthesis** (alternative): All ideas/items merged into a single ranked list from simplest to most complex, with clearly defined complexity tiers. Use this 4-tier classification:

     | Tier | Name | Build Time | Characteristics |
     |------|------|-----------|-----------------|
     | T1 ⚡ | Hours | 2 hrs - 2 days | Static HTML, no backend, single file or Vercel deploy |
     | T2 🛠️ | Weekend | 1 - 7 days | Simple backend, 1-2 APIs, PWA or CRUD app |
     | T3 🏗️ | Sprint | 1 - 3 weeks | Full-stack, auth, database, real-time or AI integration |
     | T4 🏢 | Platform | 2 weeks - 1+ months | Two-sided marketplace, multi-API, complex workflows |

     Within each tier, items are listed from fastest to slowest build time. Include effort estimates per item (e.g. "3 days", "1-2 weeks").

     Include these additional sections after the tier lists:
     - **Top 20 / Top N Quick-Start Ranking** — Highest demand-to-simplicity ratio items selected across all tiers. Each entry: name, effort badge, and a one-line "why first" explanation.
     - **Cross-Cutting Pattern Analysis** — 5-10 repeating themes extracted by comparing ideas across all sources (e.g. "Photo as universal input", "Privacy as competitive moat"). These patterns should be shorter and sharper than report content — each is 2-3 sentences with a bolded title.
     - **Full Source Catalog** — Consolidated table of every source category, count, signal level, and representative examples. Used as trust/transparency anchor.
3. Write `master-report.md` with the chosen format:

### PHASE 3: Interactive HTML Guide/Lesson

> **Core interaction pattern (mandatory for idea-mining subjects):** Every idea should expand **inline** inside the HTML guide when clicked, showing full Intent & Origin [SOURCE], Design Objective [SOURCE], and My Analysis & Suggestions [MY ANALYSIS]. This replaces the separate-document pattern from Phase 5 — the deep-dive content lives inside the interactive guide itself. If both formats are desired, the markdown blueprint report is supplementary; the HTML guide is the primary delivery mechanism.

> **Critical technical rule:** ALL idea content MUST be HTML-escaped before insertion into the HTML document. Unescaped angle brackets (`<script>`, `</style>`, `<div>`) in idea descriptions will break the entire page. Use `html.escape()` (Python) or equivalent. Additionally, when embedding JSON data inside a `<script>` block, escape any `</script>` literal to `<\/script>` — otherwise the browser interprets it as the end of the script tag.

#### Card Expansion Implementation (Event Delegation Pattern)

For interactive expandable cards, **do NOT use inline `onclick` handlers** on each card or card-header element. Instead, use **event delegation** on the parent grid container. This is more robust across browser sandboxes, avoids `eval()` security restrictions, and handles dynamically-added cards:

```javascript
// Recommended: event delegation on grid
document.querySelectorAll('.ideas-grid').forEach(function(grid){
  grid.addEventListener('click', function(e){
    var card = e.target.closest('.idea-card');
    if(!card) return;
    // Close other expanded cards
    document.querySelectorAll('.idea-card.expanded').forEach(function(c){
      if(c!==card) c.classList.remove('expanded');
    });
    card.classList.toggle('expanded');
  });
});
```

**Script initialization**: When the `<script>` block is at the end of `<body>` (after all HTML), use a simple IIFE — no need for `DOMContentLoaded`, since all DOM elements already exist at execution time:

```javascript
// Script at end of <body> — IIFE is sufficient
(function(){
  // Event delegation, card init, etc.
})();
```

**Card HTML structure** for full deep-dive expansion:

```html
<div class="idea-card" data-num="1" data-cat="utility">
  <!-- Collapsed header: always visible -->
  <div class="idea-card-header">
    <span class="idea-num">#1</span>
    <span class="idea-name">WiFi Password QR Generator</span>
    <div class="idea-badges">
      <span class="badge-effort">2 hrs</span>
      <span class="badge-cat utility">utility</span>
      <span class="expand-icon">▼</span>
    </div>
  </div>
  <!-- Expandable body: hidden by default, revealed on .expanded toggle -->
  <div class="idea-card-body">
    <div class="idea-card-body-inner">
      <div class="sources-line">Reddit[3], App Store reviews</div>
      <div class="detail-section">
        <h4><span class="tag-src">SOURCE</span> Intent &amp; Origin</h4>
        <p>Description of the core frustration...</p>
      </div>
      <div class="detail-section">
        <h4><span class="tag-src">SOURCE</span> Design Objective</h4>
        <p>Original design brief...</p>
      </div>
      <div class="detail-section">
        <h4><span class="tag-my">MY ANALYSIS</span> Suggestions</h4>
        <p>UX strategy, monetization, differentiation...</p>
      </div>
    </div>
  </div>
</div>
```

**CSS for expand/collapse** (use `max-height` transition for smooth animation):

```css
.idea-card{cursor:pointer}
.idea-card-body{max-height:0;overflow:hidden;transition:max-height 0.35s ease}
.expanded .idea-card-body{max-height:3000px}
.expand-icon{transition:transform 0.2s ease}
.expanded .expand-icon{transform:rotate(180deg)}
```

#### Copy-to-Clipboard Feature (Standard on Every Card)

When displaying actionable items (app ideas, resources, code snippets) inside interactive cards, add a **copy button** that lets the user grab all details with one click. This is now a standard feature — every card gets one.

**Implementation (see also `frontend-design` skill for the detailed reference):**

The button lives in each card's badge area. Critical: it must NOT toggle the card when clicked — use `event.stopPropagation()` and check for it in the card's event delegation handler:

```javascript
// In the card's click delegation handler:
grid.addEventListener('click', function(e){
  if(e.target.closest('.copy-btn')) return; // short-circuit before toggling
  var card = e.target.closest('.idea-card');
  if(!card) return;
  // toggle logic...
});

// On the button itself:
onclick="event.stopPropagation();copyCard(this,`...data...`)"
```

**Clipboard API with fallback** — use both methods:
- Primary: `navigator.clipboard.writeText(text).catch(fallback)`
- Fallback: `document.execCommand('copy')` with a temporary textarea

**Copy format** (compact, paste-friendly into notes/docs/AI prompts):
```text
🎯 WiFi Password QR Generator (#1)
⏱️ Effort: 2 hrs | 📂 Category: utility
📖 Sources: Reddit[3], App Store reviews

💡 Intent & Origin: The core frustration...
🎨 Design Objective: Original design brief...
✍️ My Analysis: User Experience: Single-purpose utility...
```

**Visual states:** Default (dim) → Hover (accent tint) → Copied (green tint with "✓ Copied!" text) → Reset after 2 seconds.

**Text escaping for JavaScript embedding:** When building the copy string, escape backticks, `${}`, and newlines to prevent template literal breakage:

```python
clip_js = clip.replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${').replace('\n', '\\n')
```

#### JSON Data Embedding Safety

When embedding idea/entry data as a JSON object inside `<script>` for client-side use:

```python
import json
json_str = json.dumps(ideas_dict, ensure_ascii=False)
# CRITICAL: escape </script> in the JSON data or the browser interprets it as closing the script tag
json_str = json_str.replace('</script>', '<\\/script>')
html += f'<script>const IDEAS={json_str};</script>'
```

This applies whenever a content field (description, analysis text, source citations) could contain `</script>`, `</style>`, or any HTML-close-sequence.

#### HTML Content Escaping Protocol for Idea Descriptions

When building HTML from LLM-generated content or markdown reports, apply this pipeline:

1. **First**: escape ALL HTML entities with `html.escape()` (Python stdlib)
2. **Then**: re-apply safe formatting tags (`<b>`, `<i>`, `<span class="...">`) via regex on the already-escaped text
3. **Verify**: scan the final HTML for any unescaped `<script>`, `</style>`, `</textarea>` sequences
4. **Bonus**: check for `&amp;quot;` double-encoding (symptom: quote characters showing as literal entities on screen)

```python
from html import escape as esc

def safe_markdown_to_html(txt):
    """Convert markdown bold/italic to safe HTML with proper escaping."""
    txt = txt.strip()
    # Step 1: escape ALL HTML special chars
    txt = esc(txt)
    # Step 2: re-apply allowed formatting from escaped equivalents
    txt = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', txt)  # **bold**
    txt = re.sub(r'_(.*?)_', r'<i>\1</i>', txt)          # _italic_
    txt = re.sub(r'\[SOURCE\]', r'<span class="tag-src">SOURCE</span>', txt)
    txt = re.sub(r'\[MY ANALYSIS\]', r'<span class="tag-my">MY ANALYSIS</span>', txt)
    txt = txt.replace('\n', ' ')  # collapse newlines
    return re.sub(r'  +', ' ', txt)  # collapse spaces
```

> **Cardinal Rule**: The HTML document must contain **every single detail from the aggregate/markdown reports** — no information is lost in the conversion. But it must NOT blindly paste markdown text into HTML. Every piece of information must be evaluated for **visualization potential first, text second**.

#### Visualization Hierarchy (Fidelity-First)

When converting aggregate data to HTML, apply this decision hierarchy — from most to least preferred — for every piece of information:

| Priority | Method | When | Example |
|----------|--------|------|---------|
| 1 🥇 | **Interactive component** | Data has discrete items > 3 that benefit from filtering, sorting, or toggling | Tier filter tabs with expandable cards (click to reveal details) |
| 2 🥈 | **Sandbox / live tool** | Data can be manipulated or explored in-place by the reader | Live search filter, sliders to adjust parameters, rating scale |
| 3 🥉 | **Structured visual layout** | Information has hierarchy, categories, or parallel relationships | Grid cards, tables with hover states, timeline steps, comparison columns |
| 4 | **Data visualization (chart/graph)** | Quantitative or comparative data with clear relationships | Bar chart comparing effort tiers, heatmap of source coverage, radar of pattern signals |
| 5 | **Embellished text with visual anchors** | Rich text where visual framing adds comprehension | Quote callout, key stat callout, emoji-bulleted lists with highlight backgrounds |
| 6 ❌ | **Plain unstyled text** | When visualization would misrepresent, over-simplify, or lose nuance | Nuanced caveats, conditional statements, context-dependent explanations |

**Rule**: Never default to plain text. Ask "can I visualize this?" before accepting text for any block of information. Only fall to text when the data is genuinely impossible to visualize faithfully (contextual disclaimers, conditional logic, subjective nuance).

**Anti-clutter mandate**: Visualization must not create clutter. Every visual element must earn its place. If a visualization adds more cognitive load than the equivalent text, use text instead. Clean beats clever.

#### Visual-Text Coupling (Mandatory)

Every visual or interactive element MUST be backed by explanatory text — the two form a single unit of communication:

| Visual/Interactive Element | Required Text Pairing |
|----------------------------|----------------------|
| **Charts, graphs, data visualizations** | 2-3 sentence intro: what the chart shows, the key takeaway, the source of the data. Axis labels and legends do NOT count as pairing — add prose context. |
| **Filterable tables or card grids** | Section intro paragraph explaining the scope and how to use the filters. Followed by a count indicator or legend if symbols are used. |
| **Expandable cards with detail panels** | Each collapsed card must show enough context (title + tag + rank) to understand what the detail will contain. The detail panel content is itself the paired text. |
| **Interactive sandbox (search, sliders, toggles)** | Brief instruction text above the sandbox explaining what it does + a reset/clear affordance. Include a live count indicator showing how many items match the current filter. |
| **Timeline steps** | Each step number must have a title in the primary layout; the detail content revealed on click is the paired text. |
| **Stat callout / number highlight** | 1 sentence of source/context next to or below the number. A bare number floating without context is not acceptable. |

Exception: Purely decorative visuals (hero gradients, dividers, background patterns) need no text pairing. **Any visual that conveys data requires text.**

#### Full-Fidelity Requirement

The HTML must be a **complete representation** of the aggregate research. Before finalizing:
1. Read every section of all sub-reports and the master report.
2. Map each data block to a visual/HTML component.
3. Cross-check: for every sub-report section header, there must be a corresponding HTML section.
4. Verify: no data point, idea, statistic, or insight from the markdown is absent from the HTML.
5. **Do NOT skip items** because they're too numerous — batch them into the appropriate tier/table/card component.

The HTML is NOT a summary. It's the full research, re-presented for interactive consumption.

> **For collections of 50+ items**: use the **data-driven HTML generation** pattern (see `references/data-driven-html-generation.md`). Parse sub-report data into structured JSON → generate HTML components programmatically → verify counts. This prevents missing items, inconsistent card structure, and hand-editing errors.

#### Fun & Flow Requirements

The HTML must be **enjoyable to browse** — not a chore:

- **Scannable hierarchy**: Clear section labels (pill badges), visual breathing room between sections, consistent heading levels.
- **Logical flow**: Information should be sequenced from foundational → applied, or general → specific, or simplest → most complex. The reader should never wonder "why is this here?"
- **Parallel where parallel, sequential where sequential**: Items of equal weight sit in side-by-side grids (comparison cards, tier tables). Sequential processes use timelines or numbered steps.
- **Surprise & delight**: Small moments of polish — hover transforms on cards, micro-animations on tab switches, a confetti or celebration element on final sections. Not gratuitous, but intentional.
- **Zero friction**: No tiny text, no wall-of-text paragraphs, no ambiguous navigation, no elements that look clickable but aren't. Every interactive element clearly signals its affordance (cursor, border change, shadow lift).

#### File Architecture (Must Follow Exactly)

- Single `.html` file with embedded `<style>` and `<script>`.
- External dependencies: only Google Fonts CDN (Inter + JetBrains Mono). If the viewing environment may be offline, the file must still degrade gracefully to the system font stack.
- **Write mechanism (runtime-dependent)** — the invariant is: *the bytes on disk must be UTF-8 with literal emoji, no `\\U`/`\\u` escape text, no double-encoded entities*. Achieve it via whichever path the runtime offers:
  - Code execution available (Hermes/Claude/CLI): Python `open(path, "w", encoding="utf-8")` or shell heredoc — NOT a `write_file`-style tool that double-escapes Unicode sequences.
  - Only a file-write tool available: write, then read back and grep for `\\\\U[0-9a-fA-F]{8}`, `\\\\u[0-9a-fA-F]{4}`, and `&amp;quot;`; if found, apply the regex repair from `references/emoji-encoding.md` or replace emoji with plain-text labels rather than shipping broken glyph escapes.
- Place literal emoji characters directly in the Python string (e.g. `"🎯"`, `"🇲🇦"`), never escape sequences like `\\U0001F3AF`.
- If using a raw Python string (`r"""..."""`), note that `\\UXXXXXXXX` sequences are NOT interpreted — after writing, apply: `re.sub(r'(?<!\\\\)\\\\U([0-9a-fA-F]{8})', lambda m: chr(int(m.group(1), 16)), content)`
- **Template-replacement pattern for data-driven HTML generation**: When generating large HTML files in Python, **do NOT use f-strings or `.format()`** for the outer template structure — CSS uses `{}` for selectors, which creates fatal brace conflicts. Instead, embed `TPL_` placeholder markers in a plain string template and use `str.replace()` to inject snippet content:

  ```python
  template = """<!DOCTYPE html><style>.card { background: var(--bg); }</style>...TPL_CARDS...</html>"""
  cards_html = build_card_snippets()
  html = template.replace('TPL_CARDS', cards_html).replace('TPL_COUNT', str(count))
  ```

  This keeps the template readable (no escape escaping), avoids all brace-conflict debugging, and makes it trivial to spot-check the template separately from the injected data. Use this pattern whenever the HTML contains CSS `{}` syntax.
- Verify visually if the runtime allows (`browser_navigate` + `browser_vision`, screenshot, headless render). If no visual tool exists, run the static-check fallback (Phase 4) — never skip verification entirely.

#### CSS Architecture (Copy These Tokens Exactly)

```css
:root {
  --bg: #0d0f12;
  --bg-elevated: #14181d;
  --bg-hover: #1a1f26;
  --bg-card: #181c22;
  --fg: #e4e6ea;
  --fg-muted: #8b919a;
  --fg-dim: #5c616a;
  --accent: #6c8cff;
  --accent-muted: #2d3a5e;
  --accent-glow: rgba(108,140,255,0.15);
  --amber: #f59e0b;
  --amber-muted: #2a2410;
  --border: #2a2f3a;
  --border-subtle: rgba(255,255,255,0.06);
  --success: #10b981;
  --error: #ef4444;
  --radius-sm: 4px;
  --radius: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --shadow-card: 0 0 0 1px rgba(255,255,255,0.06), 0 2px 8px rgba(0,0,0,0.3);
  --shadow-card-hover: 0 0 0 1px rgba(108,140,255,0.2), 0 8px 24px rgba(0,0,0,0.4);
  --shadow-glow: 0 0 24px -4px rgba(108,140,255,0.15);
  --transition-fast: 120ms ease;
  --transition: 200ms ease;
  --transition-slow: 300ms ease;
}
```

- MUST include `@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0s !important; animation-duration: 0s !important; } }`
- Dark theme only. No light theme unless explicitly requested.
- All borders on dark backgrounds use semi-transparent white: `rgba(255,255,255,0.05)` to `rgba(255,255,255,0.08)`. Never use solid dark border colors.
- Elevation is communicated via luminance stepping (each level slightly lighter bg), NOT via dark box-shadows which are invisible on dark backgrounds.

#### Typography Rules

- Font stack: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Mono class: `'JetBrains Mono', ui-monospace, SFMono-Regular, Consolas, monospace`
- Hero heading: `font-weight: 800`, `letter-spacing: -0.04em`, `font-size: clamp(2.5rem, 8vw, 5rem)`
- Section headings: `font-size: clamp(1.75rem, 4vw, 2.5rem)`, `font-weight: 700`
- Body text: `color: var(--fg-muted)`, lighter weight for comfortable reading
- Gradient text (`.gt` utility): use sparingly — hero title and key numbers only, never on body text
- Step labels: small, uppercase, letter-spaced, accent-colored pill badges

#### Layout Patterns (Must Follow)

- **Hero**: Min 85vh, centered single-column, radial-gradient ambient glow at top, CTA buttons in a flex row with wrap
- **Section container**: `max-width: 1200px`, `margin: 0 auto`, `padding: 5rem 1.5rem` (reduced to `3rem 1rem` at 768px)
- **Card grids**: `display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 0.75rem` — max 4 columns
- **Split content layouts**: `grid-template-columns: 2fr 1fr` for main + sidebar, or `1fr 1fr` for equal comparison
- **Tab bars**: Horizontal flex row, `overflow-x: auto`, hidden scrollbar. Buttons get `.active` class for current selection
- **Timeline**: Left `border-left: 2px solid rgba(108,140,255,0.15)`, `::before` circular dots at 12px, step numbers centered. Active step: accent background + glow shadow
- **Stats bar**: Horizontal grid or flex row on the hero, stat value in large gradient text, label in small muted text below
- **Pricing/data cards**: Bordered container with tinted background, tier badge top-left, price prominent, description below
- **Responsive breakpoint**: `@media (max-width: 768px)` collapses padding, gaps, and reduces grid to single column where appropriate

#### Interactive Patterns (Must Include at Least 2 of These 3)

1. **Clickable Category Cards** — clicking a card toggles `.active` (border + glow + tint) and reveals paired detail content below by swapping `display: none/block` on matching `.arch-d` divs
2. **Tabbed Content Panels** — horizontal tab bar, clicking a tab sets it `.active` and shows its paired `.tp` panel, hides others
3. **Timeline Steps** — clicking a step sets `.active` with glow dot and reveals detail content in a paired detail panel to the right

All interactive elements use event delegation on parent containers where possible, with CSS class toggling for active state. Reserve inline `onclick` only for standalone buttons (filter/category toggles in tab bars, search bar) that cannot bubble up from a child card or grid item. No frameworks, no imports.

#### Navigation Structure

- Sticky nav: `position: sticky; top: 0; z-index: 50; backdrop-filter: blur(16px)`
- Logo on left, horizontal links on right with `overflow-x: auto` and hidden scrollbar
- Links scroll to section IDs (`#archetypes`, `#services`, etc.)
- Active/hover: `color` transitions, no underlines

#### Section Content Rules

- Each major section opens with a `sec-label` pill badge (e.g. "STEP 1", "STEP 2", etc.)
- Use `sec-label` styling: `display: inline-block; padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.7rem; letter-spacing: 0.1em; text-transform: uppercase; background: var(--accent-muted); color: var(--accent); border: 1px solid rgba(108,140,255,0.15)`
- Minimum formatting — avoid over-bolding. Prose for explanations, lists for structured data, tables only for comparisons.
- Interleave data cards and stats inline with the text that motivates them.
- Every section label, heading, and data point must be intentional — nothing is filler.

#### Components to Include

- **Hero stats/metrics** as highlighted numbers
- **Pricing or data cards** showing tiers/ranges with badges
- **Tool stack / resource lists** in sidebar panels
- **Phased action plan / roadmap** as a 3-column grid at the bottom
- **Footer** with summary tagline and version info

#### Ordered-by-Simplicity HTML Components (for idea/product mining subjects)

When the master report uses the "ordered-by-simplicity" synthesis format, the HTML guide MUST include these additional components:

1. **Tier Tab Bar** — Horizontal flex row of 4 filter tabs (⚡ Hours, 🛠️ Weekend, 🏗️ Sprint, 🏢 Platform) with item counts in badges. Each tab toggles visibility of its paired ideas grid. Active tab gets accent-colored border + bg. JS: `querySelectorAll + toggle('active')`.

2. **Tier 1 Full Cards** — Interactive expandable cards. Each card shows rank + title + effort tag + category tag in a compact row. On click (via event delegation — never inline `onclick`), a detail panel slides open revealing: Problem (1-2 sentences), Solution (1-2 sentences), source cross-references, and validation strategy. CSS: `max-height` transition from `0` to `600px` on class toggle. Each card gets `cursor:pointer` and hover border change.

3. **Tiers 2-4 Compact Table** — Table format (not cards) to save vertical space. Columns: #, Idea Name + Effort, Sources, Validation. The table header freezes conceptually (no scroll CSS needed in single page). Each row gets a subtle hover highlight.

4. **Top 20 Start-Here Section** — Ranked list displayed as a responsive grid of cards (2 columns on desktop, 1 on mobile). Each card: rank number (large, accent-colored), title + description, effort pill badge. This section lives BEFORE the full tier grids as a "build first" suggestion.

5. **Pattern Cards Grid** — Cross-cutting patterns from the master report rendered as a responsive card grid. Each card: emoji icon, short title, 2-3 sentence explanation. `grid-template-columns: repeat(auto-fill, minmax(240px, 1fr))`.

6. **Source Catalog Table** — Full-width table at the bottom of the HTML showing every source category, its count, signal level, and representative examples. Serves as a trust anchor and methodology disclosure. Includes a TOTAL row with grand sum. Styled with the same border/hover as other tables.

### PHASE 4: Verification (two audits — fidelity, then rendering)

**4A. Fidelity audit (mandatory, runtime-independent):**
1. Re-read `_numbers.md`; grep the HTML for each ledger value — every number displayed must exist in the ledger, and every headline stat in the ledger must appear in the HTML.
2. Count items: number of cards/rows per tier in HTML must equal the counts in the master report. Assert programmatically if code execution exists; count manually otherwise.
3. Section cross-check: every sub-report section header has a corresponding HTML section (Full-Fidelity Requirement).
4. Spot-check 5 random claims in the HTML back to their Source Index entries.

**4B. Rendering audit (adapt to runtime):**
- *With visual tools*: navigate to the HTML, click at least 2 interactive features, run vision check confirming emoji render as graphics (not `\U` text), dark theme consistent, layout clean.
- *Without visual tools (static fallback)*: grep for `\\U[0-9a-fA-F]{8}` / `\\u[0-9a-fA-F]{4}` literals, `&amp;quot;` / `&amp;amp;` double-encoding, unclosed tags (crude: count `<div` vs `</div`), and confirm every `onclick` target class exists in the `<script>`. State plainly in the deliverables summary that visual verification was unavailable.

5. Report any issues found and their resolution. A failed fidelity audit blocks delivery — fix, don't annotate around it.

### PHASE 5 (Optional): Deep-Dive Blueprint Analysis — Per-Item Enrichment

> **When to use**: After Phases 0-4, when the user asks for detailed per-item analysis where each idea/entry gets expanded with design intent, source-derived context, and tagged personal opinion. Produces a standalone report alongside the existing ones.

> **Delivery format**: By default, produce a standalone markdown report (`report-09-detailed-idea-blueprints.md`). However, when the user expects clicking on items in the HTML guide to expand them inline with full detail, **integrate the blueprint content directly into the HTML guide cards** (see Phase 3: Interactive Card Expansion pattern) instead of (or in addition to) the separate file. The trigger phrase "clicking on an app idea or concept should expand its area" means inline expansion is the primary delivery, not a separate document.

**Trigger phrases**: "get more into detail for each", "explain the intent", "base this from original sources and your own opinion", "clearer vision for each", "your own suggestion on each aspect".

#### Step 1: Extract Full Idea Catalog

Load `_data.json` which contains all ideas with tier, name, effort, sources, and validation metadata. Decode HTML entities with `html.unescape()`.

#### Step 2: Merge with Detailed Source Context

Parse sub-reports (especially report-01) for detailed idea blocks using regex. The Reddit report uses `### TIER.SEQ` heading structure with `**Problem:**`, `**Solution:**`, `**Why unsolved:**`, `**Stack:**` fields. Map to global numbers via `{1:0, 2:30, 3:60, 4:90}` offset dict.

#### Step 3: Classify Ideas by Category (Word-Boundary-Safe)

Use a **two-pass approach** to avoid false positives (e.g. `'ip'` matching inside `'recipe'`):

- **Pass 1**: Long/multi-word phrases checked via simple substring (unique enough to never false-match).
- **Pass 2**: Short keywords use regex `\bword\b` word boundaries.

See `references/idea-blueprint-analysis.md` for the full 9-category classification map.

Common categories: utility, finance, time, dev, ai, social, health, home, learn, general.

#### Step 4: Produce Category-Targeted Analysis

Define analysis per category covering three dimensions: **UX strategy**, **monetization model**, **differentiation approach**. Tag origins:

- `[SOURCE]` = derived from original research reports
- `[MY ANALYSIS]` = personal opinion / constructive suggestion

See `references/idea-blueprint-analysis.md` for the full template map.

#### Step 5: Write the Blueprint Report

For each of N ideas, write a self-contained section:

```
### #{num}: {name}
**Effort:** {effort}
**Category:** {category}
**Sources:** {sources}

#### Intent & Origin [SOURCE]
Core frustration from original research. Validation approach.

#### Design Objective [SOURCE]
Original design brief, proposed solution, why existing solutions fail.

#### My Analysis [MY ANALYSIS]
UX strategy, monetization model, differentiation approach.
```

Every claim carries either `[SOURCE]` or `[MY ANALYSIS]`. Close with 10 cross-cutting design principles in an appendix.

#### Step 6: Cross-Reference & Integrate

1. Add section to `master-report.md` describing the new blueprint report.
2. Add nav link + hero callout in `guide.html` pointing to the blueprint file.
3. Verify the blueprint is discoverable from the main guide.

#### Step 7: Verify Blueprint Quality

- Count `[SOURCE]` tags: expect >350 for 115 ideas
- Count `[MY ANALYSIS]` tags: expect >100
- Spot-check 3-5 entries (each needs all 3 analysis subsections)
- Verify no short-keyword false positives in classification
- Confirm report size >100 KB for 115+ ideas

#### Blueprint Pitfalls

1. **Short-keyword false positives**: `'ip'` matches inside `'recipe'`, `'eat'` in `'feature'`. Use two-pass word-boundary-safe classifier (the details are in `references/idea-blueprint-analysis.md`).
2. **Entity decoding**: Always use `html.unescape()` on idea names from `_data.json`.
3. **Source absence**: Not every idea has full `**Problem:**` fields in report-01. Derive a reasonable design direction from the generic sources string.
4. **Tier numbering**: report-01 uses `TIER.SEQ` headings (1.01 → global #1, 2.03 → global #33). Map via offset dict `{1:0, 2:30, 3:60, 4:90}`.
5. **Content size**: 115 entries at ~800 chars each = ~92 KB minimum, expect 120-180 KB. Write section by section to avoid context drift.
6. **Template misapplication**: Ideas that bridge categories (e.g. AI-powered recipe app = both 'health' and 'ai') should use the primary category's template, broad enough to cover the overlap.

### PHASE 6 (Optional): Portable Dataset Export — `_portable_data.json`

> **When to use**: After Phase 3 (HTML Guide), or whenever the user asks for a machine-readable, transportable version of the entire research corpus. Also regenerate whenever data changes (new sources, enriched entries, new domains added). The user's trigger phrase is "save all data with details and names and titles and sources in a json file I can move anywhere."

#### Why generate a portable JSON

The HTML guide is the primary delivery for humans. The portable JSON is the companion delivery for machines — it allows the user to:
- Import into databases, spreadsheets, or other apps
- Feed into AI prompts as structured context
- Build their own visualization or exploration tools
- Move the entire dataset between machines without loss

#### Schema

The JSON follows this structure (see `references/portable-dataset-export.md` for the full reference):

```json
{
  "_meta": { "project", "version", "total_ideas", "last_updated" },
  "summary": { "tier_breakdown", "category_breakdown" },
  "categories": { "category_name": { "label", "count", "ideas": [id, ...] } },
  "tiers": { "tier_name": { "label", "count", "ideas": [id, ...] } },
  "everything": [ { "id", "name", "tier", "tier_label", "effort", "category", "sources", "validation", "intent_and_origin", "design_objective", "my_analysis_and_suggestions" } ],
  "top_20_quick_start": [ { "id", "name", "effort", "why_first" } ],
  "design_patterns": [ { "name", "description" } ],
  "idx_by_id": { "1": { full entry }, ... },
  "idx_by_category": { "utility": [1, 2, 3], ... },
  "idx_by_tier": { "hours": [1, 2, 3], ... }
}
```

#### Key constraints

1. **`html.unescape()` all names and metadata** — `_data.json` typically has HTML entities that need decoding
2. **`ensure_ascii=False`** when serializing — emoji must survive as literal characters
3. **All entries must be present** — verify count after generation (e.g. 115)
4. **Every entry must have all three detail fields** (intent_and_origin, design_objective, my_analysis_and_suggestions) — flag any that are empty
5. **Keep in sync with guide.html** — every time data changes, rebuild both files
6. Add a JSON download link in guide.html's footer pointing to the file

#### Integrity checks (run after generation)

1. `len(everything) == total_ideas` (matches expected count)
2. Every entry has non-empty detail fields
3. `len(idx_by_id) == total_ideas`
4. Sum of category counts == total_ideas
5. Sum of tier counts == total_ideas
6. JSON parses cleanly (no unescaped control characters, no broken UTF-8)

#### Python generation pattern

```python
import json, os
from html import unescape

# 1. Parse report-09 for all entries
# 2. Merge with _data.json metadata (tier, effort, sources, validation)
# 3. Build master_json dict with all sections
# 4. Validate every entry has complete fields
# 5. Write via open(path, 'w', encoding='utf-8')
# 6. Run integrity checks
```

#### Continuous enrichment integration

When running an autonomous enrichment pipeline (see Autonomous Enrichment Loop below), the JSON MUST be rebuilt after **every** data-modifying action — not just after HTML rebuilds. Track `portable_json_version` in the pipeline's state file alongside `html_version`.

---

### Autonomous Enrichment Loop (Continuous Pipeline)

> **When to use**: After the initial pipeline (Phases 0-6) is complete and the user wants the corpus to keep improving autonomously. The user's trigger phrase is "make a cron job to keep loop executing the research enrichment and improvement project continuously and autonomously."

#### Architecture

The pipeline runs as a **cron job** (every 1-6 hours depending on scope). Each iteration executes ONE action from an 8-phase cycle, then updates a state file (`_loop_state.json`) so the next iteration picks up where the last left off:

| # | Phase | Purpose |
|---|-------|---------|
| 0 | **Quality Audit** | Verify random entries, check source tags, check for JS errors in HTML, validate data integrity |
| 1 | **Source Sweep HN** | Find 1-3 new sources via HN Algolia for the least-sourced idea |
| 2 | **Deep Enrich** | Add 2-3 new sentences to one idea's Intent & Origin and My Analysis sections |
| 3 | **Source Sweep YT** | Find 1-3 new sources via YouTube search |
| 4 | **New Representation** | Add a new visual/interactive feature to the HTML (category chart, random button, copy feature, etc.) |
| 5 | **Source Sweep Curated** | Find 2-3 new sources via DuckDuckGo Lite from blogs/curated lists |
| 6 | **Expand Domain** | Research a new domain not yet covered, add 3-5 new ideas. When a Twitch/trend/gimmick content-creator domain is available, prioritize it (see `references/twitch-trend-gimmick-sweep.md`). |
| 7 | **Rebuild HTML + JSON** | Regenerate both deliverable formats with all accumulated changes, verify with browser |

#### State file (`_loop_state.json`)

```json
{
  "version": 1,
  "total_iterations": 42,
  "action_cycle_position": 3,
  "last_idea_worked": 87,
  "last_domain_swept": "legal-tech",
  "html_version": 7,
  "portable_json_version": 7,
  "ideas_enriched_count": 87,
  "sweeps_done_count": 15,
  "quality_audit_score": 0.95,
  "last_audit_iteration": 40,
  "current_phase": "deep_enrich",
  "actions_completed": ["quality_audit", "source_sweep_hn", "deep_enrich", ...],
  "handoff_note": null
}
```

#### Skills to load each iteration

The cron job loads BOTH `aggregate-deep-research` and `frontend-design` on every tick, since each iteration may touch either data (reports) or presentation (HTML).

#### Handoff mechanism

When context runs low mid-iteration:
1. Save complete state to `_loop_state.json` with a `handoff_note` describing exactly what remains
2. Use `delegate_task` with `goal="Continue enrichment work"` and context containing the current phase, remaining work description, and project directory path
3. The subagent completes the work in its own isolated context
4. After return, verify that expected state updates were made, reconcile handoff_note

#### Sync rule: JSON after every change

The `_portable_data.json` must be rebuilt after **any** data-modifying action (Phase 1, 2, 3, 5, 6, 7), not just after Phase 7. This ensures the user always has an up-to-date portable export.

#### Pitfalls

1. **Re-processing the same idea**: Track `last_idea_worked` in state. Ideas at indices < `last_idea_worked` should not be re-enriched unless new sources were found for them.
2. **HTML gets out of sync with data**: Always rebuild HTML + JSON together in Phase 7. Never rebuild one without the other.
3. **Cron prompt gets stale**: The cron job prompt must be self-contained (no dependence on conversation history). Include the full cycle description, skill requirements, and file paths.
4. **Context handoff loss**: When using delegate_task, the subagent needs absolute file paths and the exact phase description. Include the full `_loop_state.json` content in the handoff context.
5. **Infinite growth**: After all 115 ideas are enriched, Phase 2 has nothing to do. In that case, skip to the next phase and set `last_idea_worked` back to 0 to start a new enrichment pass (Level 2 depth).

---

## DELIVERABLES

The agent ends with a summary table of all files created:

| File | Size | Description |
|------|------|-------------|
| `report-01-{aspect}.md` | XXX B | Aspect research report |
| `report-02-{aspect}.md` | XXX B | Aspect research report |
| ... | ... | ... |
| `_environment.md` | XXX B | Capability probe + runtime adaptations used |
| `_numbers.md` | XXX B | Statistics ledger (value → claim → source) |
| `master-report.md` | XXX B | Master synthesis |
| `guide.html` | XXX B | Interactive HTML guide |
| `_portable_data.json` | XXX B | Portable JSON dataset (all entries, indexes, machine-readable) — see `references/portable-dataset-export.md` |

Plus the absolute path to the output directory.

## Known Pitfalls

1. **Unicode double-escaping**: `write_file` tool double-escapes `\u` and `\U` sequences. Always use `execute_code` with Python `open()` for HTML files containing emoji.
2. **Raw string trap**: Python `r"""..."""` does NOT interpret `\UXXXXXXXX` escapes — they become literal text. Either use direct strings with literal emoji, or apply the regex fix after writing.
3. **Entity double-encoding**: When escaping HTML special characters for use inside f-strings, do NOT also rely on the HTML context to do another pass of the same encoding. Applying `str.replace('"', '&quot;')` and then putting the result inside an HTML element means browsers see `&amp;quot;` on screen (the `&` in `&quot;` gets escaped again). **Fix**: use raw literal quote characters in content that lives inside HTML elements, or apply entity encoding only once at the very final write stage. Symptom: `&amp;quot;` visible on rendered cards.
4. **Shadow blindness**: Dark box-shadows are invisible on dark backgrounds. Use luminance stepping (lighter bg) + semi-transparent white borders instead.
5. **Card column overflow**: More than 4 columns in a card grid makes cards too narrow. Use `auto-fit, minmax(220px, 1fr)` which naturally caps at 4.
6. **Browser verification required (when available)**: Always verify with `browser_vision` — accessibility tree snapshots don't catch visual rendering bugs like broken emoji or misaligned grids. Without a browser, run the static-check fallback (Phase 4B).
7. **Long-generation drift (weak models)**: models degrade over long outputs — sources invented, numbers rounded "from memory", tone drifting into editorializing. Countermeasure: chunked writing + per-chunk Source Index re-read + the self-audit pass (Phase −1 §B). Never trust memory over the on-disk ledger.
8. **Count inflation**: the 50-source floor tempts padding the Source Index with unretrieved or duplicate entries. The floor is a research-effort target, not a vanity metric — see Source-counting honesty rule.
12. **Unescaped HTML content breaks the page**: If idea descriptions, analysis text, or any user-facing content contains literal angle brackets (`<script>`, `</style>`, `<div>` tags in prose), the entire HTML page breaks — the browser interprets them as real tags. **Always `html.escape()` all content before inserting into an HTML template**, then re-apply allowed formatting via regex on the escaped string. This is especially critical for LLM-generated content which frequently produces `<script>` or `</script>` in prose. Also escape `</script>` to `<\/script>` in JSON embedded inside `<script>` blocks.

13. **Inline onclick failure in sandboxed browsers**: Some browser-based runtimes (Hermes, headless) restrict inline `onclick` handlers. Use event delegation (`element.addEventListener('click', handler)`) with `e.target.closest()` instead. This is more robust and avoids `eval()`-related restrictions.

14. **Template overfitting**: forcing the 4-tier/idea-mining structure onto subjects it doesn't fit (history, medicine, policy). Choose axes from the data (Cardinal Principle 6).

## Related Skills

- **`frontend-design`** — Intentional UI design rules (this skill embeds the key mandates)
- **`voidflow-design-system`** — Full dark-theme CSS token system
- **`popular-web-designs`** — 54 real design system templates if you want a specific brand-inspired look
- **`deep-research-pipeline`** — Significant overlap. `deep-research-pipeline` has more operational detail on search fallbacks (Bing HTTP fetch, Windows git-bash workarounds); `aggregate-deep-research` has the complete frontend-design CSS token set embedded. The two cover the same 4-phase pipeline; prefer this one when you need a polished HTML guide with design-system enforcement, and `deep-research-pipeline` for raw research-heavy tasks where the HTML is secondary.
- **`plan`** — Use before calling this skill to scope the research plan

## Reference Files (in `references/`)

| File | Purpose |
|------|---------|
| `app-ideas-research-sources.md` | Source catalog for app ideas research |
| `data-driven-html-generation.md` | Programmatic HTML build pattern |
| `emoji-encoding.md` | Unicode/emoji handling for HTML artifacts |
| `idea-blueprint-analysis.md` | Category classification & analysis templates |
| `portable-dataset-export.md` | `_portable_data.json` schema, rebuild, verification |
| `quality-audit-checklist.md` | Phase 0 quality audit protocol |
| `twitch-trend-gimmick-sweep.md` | Twitch/trend/gimmick idea sweep patterns |
