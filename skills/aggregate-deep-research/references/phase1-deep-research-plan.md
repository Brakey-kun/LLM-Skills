# Phase 1 Deep Research Plan — Morocco SaaS Vertical Opportunity

**Session:** 2025-07-20 aggregate-deep-research
**Status:** Phase 0 Complete → Phase 1 Ready to Execute
**Output Dir:** `C:\Users\amine\hermes-workspace\morocco-saas-vertical-opportunity\` (to be created)

---

## Aspect Decomposition (6 Aspects, Source-Based Strategy)

| Aspect | Focus | Primary Languages | Target Sources (50-200 each) |
|--------|-------|-------------------|------------------------------|
| **1. Comparable Market Vertical SaaS Models** | Successful vertical SaaS in LatAm, SSA, SE Asia, MENA | English, Spanish, French | HN Algolia comments (pain mining), Contxto, Forbes México, FrenchWeb, Disrupt Africa, FrenchWeb LatAm tag |
| **2. Morocco Market Structure & Digital Readiness** | SME landscape, internet penetration, payment infra, regulatory | French, Arabic, English | L'Economiste, HCP (Haut-Commissariat au Plan), World Bank, AFD, ADD, Technopark, CGEM reports |
| **3. Underserved Vertical Sectors in Morocco** | Agritech, tourism, construction, healthcare, artisanal, logistics | French, Arabic, Darija | Founder LinkedIn, Facebook groups, MoroccoTech, 212Founders, sector association sites |
| **4. Payment & Billing Models for Morocco** | Local gateways, mobile money, invoice B2B, dirham pricing | French, Arabic | CMI, Payzone, HPS, Inwi Money, Orange Money, Flouci, Wafacash, fintech startup cases |
| **5. Go-to-Market for Moroccan B2B SaaS** | Direct sales, channel partners, gov tenders, Francophone Africa expansion | French, Arabic | Technopark alumni, 212Founders portfolio, French Tech Casablanca, accelerator programs |
| **6. Incumbent Gaps & Weak Solutions** | Where French/EU imports fail local workflows | French, Arabic | User reviews, integration pain points, founder feedback, CRI regional reports |

---

## Parallel Execution Plan (Phase 1)

### Batch 1: Aspect 1 + Aspect 2 (Highest Leverage)
**Why:** Aspect 1 provides the "what works elsewhere" patterns; Aspect 2 provides the "what fits Morocco" constraints. Together they define the opportunity space.

#### Aspect 1 Search Queries (Parallel)
```
# HN Algolia Comments (English) - Pain Mining
1. "vertical SaaS" "Latin America" OR "LatAm" profitable bootstrap
2. "Toast POS" OR "Procore" OR "Shopify" vertical SaaS emerging markets
3. "SaaS" "Mexico" OR "Colombia" OR "Brazil" vertical B2B SMB
4. "micro SaaS" vertical niche profitable emerging market
5. "B2B SaaS" "Southeast Asia" OR "Indonesia" OR "Vietnam" vertical

# FrenchWeb.fr (French) - Morocco + LatAm coverage
6. site:frenchweb.fr "Maroc" startup SaaS
7. site:frenchweb.fr "Amérique latine" SaaS vertical
8. site:frenchweb.fr "Afrique" SaaS vertical

# Contxto (Spanish) - LatAm tech media
9. site:contxto.com SaaS vertical México
10. site:contxto.com software PYME Colombia

# Disrupt Africa (English) - African patterns
11. site:disruptafrica.com vertical SaaS
12. site:disruptafrica.com Morocco startup
```

#### Aspect 2 Search Queries (Parallel)
```
# L'Economiste (French) - Morocco business daily
1. site:leconomiste.com "startup" "levée de fonds" 2024
2. site:leconomiste.com "digitalisation" PME Maroc
3. site:leconomiste.com "paiement" mobile Maroc
4. site:leconomiste.com Technopark Casablanca

# HCP / World Bank / AFD (English/French) - Macro data
5. site:hcp.ma entreprise PME chiffre
6. site:worldbank.org Morocco digital economy
7. site:afd.fr Maroc numérique

# ADD / Technopark / Maroc Numeric (French)
8. site:add.gov.ma startup
9. site:technopark.ma startup
10. site:marocnumeric.ma
```

---

## Source Index Template (Per Aspect Report)

Each report will open with a **Source Index Table**:

| # | Source Name | Type | Language | Signal ★ | Date Range | Notable Threads/Articles | Access Method |
|---|-------------|------|----------|----------|------------|--------------------------|---------------|
| 1 | HN Algolia comments | Forum | English | ★★★★★ | 2020-2025 | "vertical SaaS LatAm" (47 comments) | API direct |
| 2 | FrenchWeb.fr Morocco tag | Tech media | French | ★★★★☆ | 2019-2025 | CDG Invest, Technopark articles | Direct browse |
| 3 | L'Economiste | Business daily | French/Arabic | ★★★★☆ | 2020-2025 | Startup funding, digitalization | Direct browse |
| 4 | Contxto | LatAm tech media | Spanish/English | ★★★★☆ | 2021-2025 | Series A LatAm SaaS | Direct browse |
| 5 | Disrupt Africa | African tech media | English | ★★★★★ | 2020-2025 | North Africa funding rounds | Direct browse |
| ... | ... | ... | ... | ... | ... | ... | ... |

---

## Numbers Ledger Template (`_numbers.md`)

```
# Morocco SaaS Vertical Opportunity - Numbers Ledger
# Format: value | claim | source | fetched-or-snippet

# Example entries (to be populated during Phase 1):
88% | Internet penetration Morocco 2024 | HCP/ANRT 2024 report | fetched
150k+ | Number of formal SMEs Morocco | CGEM 2023 | fetched
70/30 | Revenue split Marketplace/Creator | Generalist Programmer YT | snippet
$2.3B | LatAm SaaS market 2023 | Contxto/IDC | fetched
...
```

---

## Next Session: Phase 1 Execution

### Required Tools Available
- ✅ `browser_navigate` + `browser_console` (HN Algolia, FrenchWeb, L'Economiste, Disrupt Africa, Contxto)
- ✅ `skill_manage` write_file for reports and references
- ✅ HN Algolia API direct access (most reliable)
- ❌ `execute_code` blocked in skill context (use skill_manage for file I/O)
- ❌ `terminal` fork crash (avoid)

### Execution Order
1. **Run all Aspect 1 searches in parallel** (12+ queries) → collect 100+ sources
2. **Run all Aspect 2 searches in parallel** (10+ queries) → collect 80+ sources
3. **Write report-01-comparable-markets.md** (chunked, ≤150 lines per chunk, self-audit)
4. **Write report-02-morocco-market-structure.md** (same process)
5. **Update `_numbers.md`** after each report
6. **Proceed to Aspects 3-6** in batches of 2

### Browser Session Management
- Batch 6-8 `browser_navigate` calls per turn
- Use `browser_console(expression="document.body.innerText")` to extract JSON/text from API pages
- For HN Algolia: always use `tags=comment` for pain signals, `tags=story` for funding/news
- For French sites: expect paywalls on some L'Economiste articles; use snippets + headlines
- Document every source in Source Index with access date

---

## Research Integrity Checklist (Per Report)

- [ ] Every claim has inline source tag `[SRC-#]`
- [ ] Every `[SRC-#]` exists in Source Index
- [ ] All numbers in `_numbers.md` ledger
- [ ] No retro-citation (citations written at claim-time)
- [ ] Verbatim quotes in blockquotes, paraphrases marked `[paraphrase]`
- [ ] Conflicting data surfaced as `⚠️ conflicting: A says X [src], B says Y [src]`
- [ ] Missing data noted as `∅ no data found for Z after N queries`
- [ ] Self-audit pass completed (3 questions) before finalizing