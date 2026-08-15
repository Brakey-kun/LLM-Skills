# Multi-Language Source Mining Patterns — Morocco SaaS Research

**Session:** 2025-07-20 aggregate-deep-research Phase 0
**Skill:** aggregate-deep-research
**Purpose:** Document validated search patterns, source reliability, and language-specific query templates for future sessions

---

## Validated Search Patterns by Language

### French (High Reliability)

| Target | Query Pattern | Example Working URLs |
|--------|---------------|---------------------|
| FrenchWeb Morocco tag | `site:frenchweb.fr Maroc startup` | https://www.frenchweb.fr/tag/maroc/ |
| FrenchWeb specific article | `site:frenchweb.fr "CDG Invest" startup` | https://www.frenchweb.fr/maroc-le-fonds-dinvestissement-cdg-invest-soutient-financierement-7-startups-malgre-la-crise |
| L'Economiste search | `site:leconomiste.com startup SaaS` | Search works on site |
| L'Economiste direct | `site:leconomiste.com "levée de fonds" Maroc` | Works |
| Maddyness (to test) | `site:maddyness.com Maroc startup` | Not yet tested |
| Silicon.fr (to test) | `site:silicon.fr Maroc SaaS` | Not yet tested |

**French Query Templates for Phase 1:**
```
"SaaS vertical" Maroc
"logiciel métier" PME Maroc
"digitalisation" PME Maroc 2024
"startup B2B" Casablanca Rabat
"levée de fonds" SaaS Maroc 2024 2025
Technopark startup SaaS
"Maroc Numeric" startup
```

---

### Spanish (Untested - Priority for Phase 1)

| Target | Query Pattern | Notes |
|--------|---------------|-------|
| Contxto (LatAm tech) | `site:contxto.com SaaS vertical México` | Leading LatAm tech media |
| Forbes México | `site:forbes.com.mx startup B2B software` | Business-focused |
| El Economista América | `site:eleconomistaamerica.com SaaS vertical` | Financial news |
| Emprendedores.es | `site:emprendedores.es SaaS vertical Colombia` | Startup-focused |
| Pulso (Chile) | `site:pulso.cl SaaS vertical` | Chilean business daily |

**Spanish Query Templates for Phase 1:**
```
"SaaS vertical" México PYME
"software especializado" Colombia PYME
"startup B2B" América Latina vertical
"software para restaurantes" México
"software construcción" LatAm
"fintech B2B" México Colombia
```

---

### Arabic/Darija (Limited Direct Search)

| Target | Approach | Notes |
|--------|----------|-------|
| Hespress | Direct article URLs only; search endpoint broken | Use French section: hespress.com/economie |
| L'Economiste Arabic | `site:leconomiste.com/ar startup` | Has Arabic subdomain |
| Facebook Groups | `site:facebook.com/groups "startup Maroc" SaaS` | Manual browse needed |
| LinkedIn | `site:linkedin.com/in "Maroc" "SaaS" "founder"` | People search |
| MoroccoTech | Direct site browse | Community site |

**Arabic Query Templates for Phase 1:**
```
برمجيات متخصصة المغرب
شركات ناشئة مغربية SaaS
برامج محاسبة مغربية سحابية
```

---

### English (High Reliability - HN Algolia)

| Target | Query Pattern | Notes |
|--------|---------------|-------|
| HN Stories | `https://hn.algolia.com/api/v1/search?query=vertical+SaaS+emerging+markets&tags=story&hitsPerPage=50` | Use tags=story |
| HN Comments | `https://hn.algolia.com/api/v1/search?query=Toast+POS+vertical+SaaS&tags=comment&hitsPerPage=50` | Use tags=comment for pain signals |
| Indie Hackers | Search UI only; limited Morocco content | Better for global patterns |
| Disrupt Africa | Direct browse; North Africa section | Good for SSA patterns |

---

## Source Reliability Matrix (Validated This Session)

| Source | Reliability | Language | Access Method | Notes |
|--------|-------------|----------|---------------|-------|
| **HN Algolia API** | ✅✅✅ | English | Direct API (browser_navigate + console) | Best for tech/business; comment mining gold |
| **FrenchWeb.fr** | ✅✅✅ | French | Direct browse | Morocco tag active; startup/funding focus |
| **L'Economiste** | ✅✅✅ | French/Arabic | Direct browse + search | Morocco's #1 business daily; some paywall |
| **Disrupt Africa** | ✅✅✅ | English | Direct browse | North Africa section; funding data |
| **Contxto** | ⚠️⚠️ | Spanish/English | Direct browse (untested) | Top LatAm tech media |
| **Forbes México** | ⚠️⚠️ | Spanish | Direct browse (untested) | Business authority |
| **Hespress** | ⚠️ | Arabic/French | Direct article URLs only | Search broken; high traffic |
| **Maroc.ma** | ❌ | Arabic/French | Blocked | Gov portal; Cloudflare |
| **DDG Lite** | ❌ | Multi | Blocked | Bot detection |
| **Indie Hackers** | ⚠️ | English | Search UI loads, no Morocco results | Good for global patterns only |
| **Maddyness** | ⚠️⚠️ | French | Untested | French startup media |
| **Silicon.fr** | ⚠️⚠️ | French | Untested | French tech B2B |

---

## Comment Mining Patterns (HN Algolia)

### For Industry Pain Signals (Best Practice)

```python
# Pattern: Search comments (not stories) for specific vertical pain
# URL: https://hn.algolia.com/api/v1/search?query={QUERY}&tags=comment&hitsPerPage=50

# Effective queries tested:
"vertical SaaS construction restaurant healthcare legal"
"Toast POS Square Shopify vertical SaaS"
"micro SaaS profitable vertical niche"
"B2B SaaS SMB vertical emerging markets"
"Procore Autodesk construction software vertical"

# For Morocco specifically (low yield):
"Maroc startup SaaS" → 0 hits
"Morocco SaaS" → 1 hit (SEO job post)
```

### Comment Mining Workflow

1. **Run 10-15 targeted comment searches** per vertical/industry
2. **Deduplicate by objectID** (HN comment unique ID)
3. **Extract industry frequency** → heat map of underserved verticals
4. **Surface pricing/pain quotes** verbatim with source IDs
5. **Cross-reference with known vertical SaaS leaders** (Toast, Procore, Shopify, Square, Veeva, etc.)

---

## File Persistence Pattern (Windows/MSYS)

**Constraint:** `terminal` tool fails with `fork: Resource temporarily unavailable` (0xC0000142) on git-bash/MSYS

**Working Pattern:**
```python
# In skill_manage write_file action:
skill_manage(
    action='write_file',
    name='aggregate-deep-research',
    file_path='references/multi-language-search-patterns.md',
    file_content='# Content here...'
)
```

**Do NOT use:** `execute_code` (blocked in this context), `terminal` with heredoc/redirect, `write_file` tool (fork crash)

---

## Phase 1 Decomposition (Planned)

| Aspect | Primary Languages | Priority Sources |
|--------|-------------------|------------------|
| 1. Comparable Market Vertical SaaS Models | English, Spanish, French | HN comments, Contxto, FrenchWeb, Disrupt Africa |
| 2. Morocco Market Structure & Digital Readiness | French, Arabic | L'Economiste, HCP, World Bank, ADD reports |
| 3. Underserved Vertical Sectors in Morocco | French, Arabic, Darija | Founder interviews, CGEM sector reports, LinkedIn |
| 4. Payment/Billing Models for Morocco | French, Arabic | CMI, Payzone, HPS docs, fintech startup cases |
| 5. Go-to-Market for Moroccan B2B SaaS | French, Arabic | Technopark, 212Founders, accelerator alumni |
| 6. Incumbent Gaps & Weak Solutions | French, Arabic | User reviews, integration pain points, founder feedback |

---

## Next Session Quick-Start

1. Load `aggregate-deep-research` skill
2. Read `references/multi-language-search-patterns.md` (this file)
3. Read `references/_environment.md` for capability probe
4. Begin Phase 1 with Aspect 1 + 2 parallel (highest leverage)
5. Use validated FrenchWeb + HN Algolia comment mining first
6. Test Spanish sources (Contxto, Forbes México) early
7. Queue Arabic/Darija sources for targeted manual browse