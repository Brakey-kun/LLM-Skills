# Interactive HTML Guide Patterns for aggregate-deep-research

> Reusable patterns for building the Phase 3 interactive HTML guides. Extracted from the Algo Academy algorithm-expansion guide (July 2026).

## 1. Expandable Card Grid (Event Delegation Pattern)

### HTML Structure
```html
<div class="cards-grid">
  <div class="card" data-num="1" data-cat="algorithms">
    <div class="card-header">
      <span class="card-number">1</span>
      <div class="card-badges">
        <span class="badge badge-effort">2 hrs</span>
        <span class="badge badge-field">algorithms</span>
      </div>
    </div>
    <div class="card-title">Two Pointers & Array Manipulation</div>
    <div class="card-desc">Partition, two-pointer technique, in-place reversal...</div>
    <div class="card-expanded">
      <div class="detail-section">
        <h4><span class="tag tag-src">SOURCE</span> Intent & Origin</h4>
        <p>Core frustration: students struggle with pointer manipulation...</p>
      </div>
      <div class="detail-section">
        <h4><span class="tag tag-src">SOURCE</span> Design Objective</h4>
        <p>Teach the mental model of left/right pointers converging...</p>
      </div>
      <div class="detail-section">
        <h4><span class="tag tag-my">MY ANALYSIS</span> Suggestions</h4>
        <p>Start with visual animation before code. Use physical analogy...</p>
      </div>
    </div>
  </div>
  <!-- more cards... -->
</div>
```

### CSS (Critical: max-height transition)
```css
.card { cursor: pointer; }
.card-expanded { max-height: 0; overflow: hidden; transition: max-height 0.35s ease; }
.card.expanded .card-expanded { max-height: 3000px; }
```

### JavaScript (Event Delegation - NOT inline onclick)
```javascript
document.querySelectorAll('.cards-grid').forEach(grid => {
  grid.addEventListener('click', e => {
    // Don't expand when clicking buttons (copy, etc.)
    if (e.target.closest('.copy-btn')) return;
    const card = e.target.closest('.card');
    if (card) card.classList.toggle('expanded');
  });
});
```

## 2. Card Copy-to-Clipboard (Standard Feature)

### Button in Card Header
```html
<div class="card-badges">
  <span class="badge badge-effort">2 hrs</span>
  <span class="badge badge-field">algorithms</span>
  <button class="copy-btn" onclick="event.stopPropagation(); copyCard(this, '...data...')">
    📋
  </button>
</div>
```

### Copy Handler (Clipboard API + Fallback)
```javascript
function copyCard(btn, text) {
  const clean = text.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\${/g, '\\${').replace(/\n/g, '\\n');
  
  // Visual feedback
  btn.textContent = '✓';
  btn.style.background = 'var(--success)';
  
  navigator.clipboard.writeText(text).catch(() => {
    // Fallback
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
  });
  
  setTimeout(() => {
    btn.textContent = '📋';
    btn.style.background = '';
  }, 2000);
}
```

## 3. Chapter Map Visualization (Progress Rings)

### HTML
```html
<div class="chapter-map">
  <div class="tier">
    <div class="tier-label">TIER 1: Foundations</div>
    <span class="chapter complete-mythical">1</span>
    <span class="chapter complete-gold">2</span>
    <span class="chapter unlocked">3</span>
    <span class="chapter locked">4</span>
  </div>
  <!-- more tiers... -->
</div>
```

### CSS
```css
.chapter {
  display: inline-block;
  width: 2.5rem; height: 2.5rem;
  border-radius: 50%;
  text-align: center; line-height: 2.5rem;
  margin: 0.25rem; font-weight: 700; font-size: 0.75rem;
  transition: var(--transition-fast);
}
.chapter.complete-mythical {
  background: linear-gradient(135deg, var(--bg-elevated), var(--accent-muted));
  border: 2px solid var(--accent);
  box-shadow: var(--shadow-glow);
  color: var(--accent);
}
.chapter.complete-gold { border: 2px solid var(--amber); color: var(--amber); }
.chapter.unlocked { border: 2px solid var(--accent); color: var(--accent); background: var(--bg-card); }
.chapter.locked { border: 2px solid var(--border-subtle); color: var(--fg-dim); background: var(--bg); opacity: 0.5; }
```

## 4. Phase Cards (Three-Phase Loop Visualization)

### HTML
```html
<div class="phase-cards">
  <article class="phase-card phase1">
    <div class="phase-icon">1</div>
    <h3>Phase 1: Understand</h3>
    <p style="color: var(--fg-muted); margin-bottom: 1rem;">Interactive slides + block-based construction + guided trace</p>
    <ul>
      <li>8-15 slides per chapter (concept → visualization → guided trace → construct)</li>
      <li>Step-through animation with variable inspector & call stack</li>
      <li>Drag-and-drop algorithm building (blocks → pseudocode → target language)</li>
      <li>Hidden sidebar with constraints & hints</li>
    </ul>
  </article>
  <!-- phase2, phase3... -->
</article>
```

### CSS
```css
.phase-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  position: relative;
}
.phase1 { border-top: 3px solid var(--accent); }
.phase2 { border-top: 3px solid var(--amber); }
.phase3 { border-top: 3px solid #8b5cf6; }
.phase-icon {
  width: 48px; height: 48px;
  border-radius: var(--radius);
  display: flex; align-items: center; justify-content: center;
  font-size: 1.5rem; margin-bottom: 1rem;
}
.phase1 .phase-icon { background: var(--accent-muted); color: var(--accent); }
.phase2 .phase-icon { background: var(--amber-muted); color: var(--amber); }
.phase3 .phase-icon { background: rgba(139,92,246,0.15); color: #8b5cf6; }
```

## 5. Three-Phase Flow Diagram (ASCII Art in HTML)

```html
<pre class="arch-diagram"><span class="box">┌─────────────────────────────────────────────────────────────────┐
│                    ALGO ACADEMY VISUALIZATION ENGINE           │
├─────────────────────────────────────────────────────────────────┤
│  CONTENT LAYER (JSON Schema)                                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ Chapter     │  │ Algorithm   │  │ Visualiz.   │             │
│  │ Spec        │  │ Spec        │  │ Spec        │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              RENDERING ENGINE (React + Canvas/WebGL)  │       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐  │       │
│  │  │Pseudocode│ │  Code    │ │  Canvas  │ │Variable│  │       │
│  │  │  Panel   │ │  Editor  │ │  View    │ │Inspector│  │       │
│  │  └──────────┘ └──────────┘ └──────────┘ └────────┘  │       │
│  └─────────────────────────────────────────────────────┘       │
│                          │                                      │
│         ┌────────────────┼────────────────┐                     │
│         ▼                ▼                ▼                     │
│  ┌──────────┐      ┌──────────┐    ┌──────────┐                │
│  │  Python  │      │  C/C++   │    │   C#     │   (WASM)       │
│  │  Tracer  │      │  Tracer  │    │  Tracer  │                │
│  │ (Pyodide)│      │(Emscript)│    │ (Blazor) │                │
│  └──────────┘      └──────────┘    └──────────┘                │
└─────────────────────────────────────────────────────────────────┘</span></pre>
```

### CSS
```css
.arch-diagram {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  padding: 2rem;
  margin: 2rem 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  line-height: 1.6;
  overflow-x: auto;
  white-space: pre;
  color: var(--fg-muted);
}
.arch-diagram .box { color: var(--accent); }
.arch-diagram .arrow { color: var(--amber); }
.arch-diagram .label { color: var(--fg); }
```

## 6. Statistics Bar (Hero Metrics)

```html
<div class="stats-bar">
  <div class="stat">
    <div class="stat-value">42</div>
    <div class="stat-label">Chapters</div>
  </div>
  <div class="stat">
    <div class="stat-value">12.8K+</div>
    <div class="stat-label">Problems</div>
  </div>
  <div class="stat">
    <div class="stat-value">3</div>
    <div class="stat-label">Phases</div>
  </div>
  <div class="stat">
    <div class="stat-value">15+</div>
    <div class="stat-label">Domains</div>
  </div>
  <div class="stat">
    <div class="stat-value">3</div>
    <div class="stat-label">Languages</div>
  </div>
</div>
```

```css
.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}
.stat {
  text-align: center;
  padding: 1.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
}
.stat-value {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  background: linear-gradient(135deg, var(--accent) 0%, #a8b8ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
}
.stat-label { color: var(--fg-muted); font-size: 0.875rem; margin-top: 0.5rem; }
```

## 7. Timeline (Phased Roadmap)

```html
<div class="timeline">
  <div class="timeline-item active">
    <div class="timeline-title">Phase 0: Foundation (Weeks 1-4)</div>
    <div class="timeline-desc">Tauri + React monorepo, JSON Schema v1.1, design tokens, Pyodide tracer...</div>
  </div>
  <div class="timeline-item">
    <div class="timeline-title">Phase 1: Visualization Engine (Weeks 5-8)</div>
    <div class="timeline-desc">Array, Graph, Tree renderers + step slider + variable inspector + call stack</div>
  </div>
  <!-- more items... -->
</div>
```

```css
.timeline {
  position: relative;
  padding-left: 2rem;
  border-left: 2px solid rgba(108,140,255,0.15);
}
.timeline::before {
  content: '';
  position: absolute; left: -6px; top: 0;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--accent);
  box-shadow: 0 0 0 4px var(--bg), 0 0 0 6px var(--accent-glow);
}
.timeline-item { position: relative; padding-bottom: 2rem; }
.timeline-item::before {
  content: '';
  position: absolute; left: -2rem; top: 0.25rem;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--bg);
  border: 2px solid var(--border);
  transition: var(--transition);
}
.timeline-item.active::before {
  background: var(--accent);
  border-color: var(--accent);
  box-shadow: 0 0 0 4px var(--accent-glow);
}
.timeline-title { font-weight: 700; margin-bottom: 0.25rem; }
.timeline-desc { color: var(--fg-muted); font-size: 0.9375rem; }
```

## 8. Mermaid-Style Flowchart (Pure HTML/CSS)

```html
<div class="flowchart">
  <div class="flow-row">
    <div class="flow-box primary">120ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Micro: hover, focus</div>
  </div>
  <div class="flow-row">
    <div class="flow-box primary">200ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Standard: panels, cards</div>
  </div>
  <div class="flow-row">
    <div class="flow-box primary">300ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Major: phase transition, sidebar</div>
  </div>
  <div class="flow-row">
    <div class="flow-box secondary">Spring</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Delight: medal reveal, particles</div>
  </div>
  <div class="flow-row">
    <div class="flow-box" style="background: var(--error); color: white;">0ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Reduced motion: instant, no animation</div>
  </div>
</div>
```

```css
.flowchart {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8125rem;
}
.flow-row { display: flex; align-items: center; gap: 0.75rem; }
.flow-box {
  padding: 0.5rem 1rem;
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  min-width: 140px;
  text-align: center;
}
.flow-box.primary { border-color: var(--accent); background: var(--accent-muted); }
.flow-box.secondary { border-color: var(--amber); background: var(--amber-muted); }
.flow-arrow { color: var(--fg-dim); font-size: 1.25rem; }
```

## 9. Color Swatches (Design Token Display)

```html
<div class="cards-grid">
  <div class="card" style="text-align: center;">
    <div style="width: 60px; height: 60px; border-radius: var(--radius); background: #0d0f12; border: 2px solid var(--border); margin: 0 auto 1rem;"></div>
    <div class="card-title">Background</div>
    <code style="font-size: 1rem;">#0D0F12</code>
    <p style="margin-top: 0.5rem; font-size: 0.875rem;">Deep obsidian — not pure black</p>
  </div>
  <div class="card" style="text-align: center;">
    <div style="width: 60px; height: 60px; border-radius: var(--radius); background: #6c8cff; margin: 0 auto 1rem;"></div>
    <div class="card-title">Accent</div>
    <code style="font-size: 1rem;">#6C8CFF</code>
    <p style="margin-top: 0.5rem; font-size: 0.875rem;">Electric blue — insight, action</p>
  </div>
  <div class="card" style="text-align: center;">
    <div style="width: 60px; height: 60px; border-radius: var(--radius); background: #f59e0b; margin: 0 auto 1rem;"></div>
    <div class="card-title">Amber</div>
    <code style="font-size: 1rem;">#F59E0B</code>
    <p style="margin-top: 0.5rem; font-size: 0.875rem;">Gold — mastery, achievement</p>
  </div>
  <div class="card" style="text-align: center;">
    <div style="width: 60px; height: 60px; border-radius: var(--radius); background: #14181d; border: 2px solid var(--border); margin: 0 auto 1rem;"></div>
    <div class="card-title">Elevated</div>
    <code style="font-size: 1rem;">#14181D</code>
    <p style="margin-top: 0.5rem; font-size: 0.875rem;">Cards, panels — luminance stepping</p>
  </div>
</div>
```

## 10. Typography Scale Reference

```html
<div class="table-wrapper">
  <table>
    <thead><tr><th>Role</th><th>Font</th><th>Size/Weight</th></tr></thead>
    <tbody>
      <tr><td>Hero</td><td>Inter</td><td>clamp(2.5rem, 8vw, 5rem) / 800 / -0.04em tracking</td></tr>
      <tr><td>Section</td><td>Inter</td><td>clamp(1.75rem, 4vw, 2.5rem) / 700</td></tr>
      <tr><td>Body</td><td>Inter</td><td>1rem / 400 / color: var(--fg-muted)</td></tr>
      <tr><td>Code/Mono</td><td>JetBrains Mono</td><td>0.875rem / 500 / tabular-nums</td></tr>
      <tr><td>Labels/Badges</td><td>Inter</td><td>0.7rem / 700 / uppercase / 0.1em tracking</td></tr>
    </tbody>
  </table>
</div>
```

## 11. Animation Philosophy (Reference)

```html
<div class="flowchart">
  <div class="flow-row">
    <div class="flow-box primary">120ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Micro: hover, focus</div>
  </div>
  <div class="flow-row">
    <div class="flow-box primary">200ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Standard: panels, cards</div>
  </div>
  <div class="flow-row">
    <div class="flow-box primary">300ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Major: phase transition, sidebar</div>
  </div>
  <div class="flow-row">
    <div class="flow-box secondary">Spring</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Delight: medal reveal, particles</div>
  </div>
  <div class="flow-row">
    <div class="flow-box" style="background: var(--error); color: white;">0ms</div>
    <div class="flow-arrow">→</div>
    <div class="flow-box">Reduced motion: instant, no animation</div>
  </div>
</div>
```

## Key Differentiators (Not "AI-Looking")

1. **No pure black (#000)** — Deep obsidian `#0D0F12`
2. **No neon/cyberpunk** — Electric blue `#6C8CFF` with subtle glow
3. **No gradient-everything** — Gradient only on hero title + key numbers
4. **Luminance elevation** — Cards lighter than bg, borders semi-transparent white
5. **Geometric medals** — Triangle/square/pentagon/star, not generic badges
6. **Purposeful motion** — Every animation communicates state change
7. **Respects `prefers-reduced-motion`** — Instant transitions when enabled

---

## Usage in Pipeline

These patterns are used in **Phase 3 (HTML Guide)** of the aggregate-deep-research pipeline. When generating the interactive guide:

1. Use **Card Grid + Event Delegation** for all idea/concept listings
2. Use **Phase Cards** for three-phase loop visualization
3. Use **Chapter Map** for curriculum overview
4. Use **Timeline** for roadmap/phased rollout
5. Use **Arch Diagram** (ASCII in styled block) for architecture
6. Use **Flowchart** for decision trees / animation philosophy
7. Use **Color Swatches** for design token documentation
8. Include **Copy-to-Clipboard** on every actionable card

All patterns respect the design tokens in `packages/ui/tokens.css` and the CSS architecture from the main skill.