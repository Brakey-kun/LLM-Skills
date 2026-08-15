# Video 02: How to Calculate Portfolio Alpha & Beta (Python + Interactive Brokers)

**Video ID**: A7zJARrdo3U
**URL**: https://www.youtube.com/watch?v=A7zJARrdo3U
**Channel**: Roman Paolucci (@QuantGuild)
**Uploaded**: Jul 15, 2026
**Duration**: 13:31
**Views**: 2,582
**Likes**: 120
**Extraction Date**: 2025-07-17
**Model Tier**: C (browser-only, small context)
**Confidence Tags**: Per §−1.4.5

---

## Metadata Summary [CONFIRMED]

- **Title**: How to Calculate Portfolio Alpha & Beta (Python + Interactive Brokers)
- **Description**: Full description extracted from ytInitialData.attributedDescription [CONFIRMED]
- **Channel**: Roman Paolucci (@QuantGuild) - 88.6K subscribers
- **Video ID**: A7zJARrdo3U
- **Duration**: 13 minutes 31 seconds
- **Upload Date**: Jul 15, 2026
- **View Count**: 2,582
- **Like Count**: 120
- **Subtitle Status**: UNAVAILABLE [CONFIRMED - UI button "Subtitles/closed captions unavailable"]
- **Transcript**: MISSING [TOOL FAILURE - browser-only limitation, no captions]

---

## Full Description [CONFIRMED - from ytInitialData.attributedDescription.content]

```
🚀 Master Quantitative Skills with Quant Guild
https://quantguild.com

🛡️ Learn to Run a Personal Hedge Fund
https://quantguild.com/personal-hedge-fund

📈 Interactive Brokers for Algorithmic Trading
https://www.interactivebrokers.com/mkt/?src=quantguildY&url=%2Fen%2Fwhyib%2Foverview.php

👾 Join the Quant Guild Discord server here
  / discord

___________________________________________
🪐 Jupyter Notebook & Data Script 👇
https://github.com/romanmichaelpaolucci...

👤 Video Setting Up Interactive Brokers 👇
  • How to Get Historical Market Data with Int...

🔗 How to Read Options Chains 👇
  • How to Read an Options Chain

TL;DW Executive Summary:
This notebook focuses on the alpha and beta of a portfolio, which are foundational concepts in understanding portfolio performance. Alpha represents the component of a portfolio's return that is unexplained by market movements—often attributed to manager skill or strategy—whereas beta measures the sensitivity of the portfolio's returns to market returns (systematic risk).
Importantly, both alpha and beta are not static values: they are estimated from historical data and can fluctuate significantly over time. This is closely related to the joint hypothesis problem, which states that empirical tests of market efficiency are always tests of both the efficiency of markets and the validity of the asset pricing model used (e.g., CAPM) to measure alpha and beta.
Because both market conditions and the underlying asset pricing models can change, estimates of alpha and beta do not converge to fixed, reliable quantities—even with large amounts of data. Thus, what looks like persistent "alpha" may just be model error or noise, and beta itself may drift as the underlying correlations and volatilities in the market evolve.
The key takeaway is that alpha and beta must always be interpreted with caution, understanding their dependence on both the choice of benchmark/model and the timeframe considered, as well as the ever-present risk that estimates will shift in new regimes or under model misspecification.

I hope you enjoyed, and I hope you learned something!

Roman
___________________________________________
📖 Chapters:
00:00 - Quick Rundown: Alpha and Beta
03:15 - Retrieving Portfolio Returns from IBKR
07:20 - Calculating Portfolio Alpha & Beta
___________________________________________
🗣️ Shout Outs

A special thank you to my members on YouTube for supporting my channel and enabling me to continue to create videos just like this one!

⭐ Quant Guild Directors
Dr. Jason Pirozzolo
___________________________________________
▶️ Related Videos

Quant Builds 🔨
How to Build a Live Volatility Surface in Python (Interactive Brokers)
  • How to Build a Live Volatility Surface in...

Statistics and Trading Profitability Over Time (Edge) 📈

Time Series Analysis for Quant Finance
  • Time Series Analysis for Quant Finance

Quant Trader on Retail vs Institutional Trading
  • Quant Trader on Retail vs Institutional T...

Quant on Trading and Investing
  • Quant on Trading and Investing

Why Poker Pros Make the Best Traders (It's NOT Luck)
  • Video

Quant vs. Discretionary Trading
  • Quant vs. Discretionary Trading
___________________________________________
🗂️ Resources

📚 Quant Guild Library:
https://github.com/romanmichaelpaolucci...

🌎 GitHub:
https://github.com/RomanMichaelPaolucci
https://github.com/Quant-Guild

📝 Medium (Blog):
  / quantguild
  / quant
___________________________________________
🛠️ Projects

The Gaussian Cookbook:
https://gaussiancookbook.com

Recipes for simulating stochastic processes:
https://papers.ssrn.com/sol3/papers.c...
___________________________________________
💬 Socials

TikTok:   / quantguild

Instagram:   / quantguild

X/Twitter: https://x.com/quantguild/

LinkedIn (personal):   / rmp99

LinkedIn (company):   / quant-guild
___________________________________________
```

---

## Chapter Markers [CONFIRMED - from ytInitialData macroMarkersListRenderer]

| Chapter | Timestamp | Title | Thumbnail URL |
|---------|-----------|-------|---------------|
| 1 | 0:00 | Quick Rundown: Alpha and Beta | https://i.ytimg.com/vi/A7zJARrdo3U/hqdefault_2000.jpg?sqp=... |
| 2 | 3:15 | Retrieving Portfolio Returns from IBKR | (same base) |
| 3 | 7:20 | Calculating Portfolio Alpha & Beta | (same base) |

---

## Visual Elements Registry [UNVERIFIED (Tier C - no vision)]

| Timestamp | Type | Description | Confidence |
|-----------|------|-------------|------------|
| 0:00 | Title Card | "Quick Rundown: Alpha and Beta" | TRANSCRIBED from chapter marker |
| 3:15 | Code/Terminal | IBKR connection, portfolio data retrieval | INFERRED from chapter title |
| 7:20 | Code/Notebook | Alpha/Beta calculation implementation | INFERRED from chapter title |
| Various | Formulas | CAPM equations, regression setup | INFERRED from topic + TL;DW |
| Various | Charts | Portfolio vs benchmark visualization | INFERRED from channel pattern |

---

## Key Claims / Knowledge [from Description + Inferred]

### From TL;DW Executive Summary (VERBATIM from description):

1. **Alpha Definition** [CONFIRMED from description]: "Alpha represents the component of a portfolio's return that is unexplained by market movements—often attributed to manager skill or strategy"

2. **Beta Definition** [CONFIRMED from description]: "Beta measures the sensitivity of the portfolio's returns to market returns (systematic risk)"

3. **Non-Stationarity Warning** [CONFIRMED from description]: "Both alpha and beta are not static values: they are estimated from historical data and can fluctuate significantly over time"

4. **Joint Hypothesis Problem** [CONFIRMED from description]: "Empirical tests of market efficiency are always tests of both the efficiency of markets and the validity of the asset pricing model used (e.g., CAPM) to measure alpha and beta"

5. **Estimation Instability** [CONFIRMED from description]: "Estimates of alpha and beta do not converge to fixed, reliable quantities—even with large amounts of data"

6. **Model Error Risk** [CONFIRMED from description]: "What looks like persistent 'alpha' may just be model error or noise, and beta itself may drift as the underlying correlations and volatilities in the market evolve"

7. **Interpretation Caution** [CONFIRMED from description]: "Alpha and beta must always be interpreted with caution, understanding their dependence on both the choice of benchmark/model and the timeframe considered, as well as the ever-present risk that estimates will shift in new regimes or under model misspecification"

### Inferred from Chapter Structure + Channel Context [INFERRED]:

| Topic | Chapter | Confidence | Notes |
|-------|---------|------------|-------|
| CAPM theory, Jensen's Alpha | 0:00-3:15 | INFERRED | "Quick Rundown" suggests conceptual foundation |
| IBKR API connection, portfolio data fetch | 3:15-7:20 | INFERRED | "Retrieving Portfolio Returns from IBKR" |
| OLS regression, covariance/variance method | 7:20-end | INFERRED | "Calculating Portfolio Alpha & Beta" |
| Benchmark selection (SPY/SPX) | Throughout | INFERRED | Standard practice |
| Rolling vs expanding windows | 7:20+ | INFERRED | Common in alpha/beta calc |
| Statistical significance (t-stats, p-values) | 7:20+ | INFERRED | Standard in quant implementations |
| Python libs: ib_insync/ibapi, pandas, numpy, statsmodels | Throughout | INFERRED | Channel standard stack |

---

## Numbers Ledger [CONFIRMED from metadata + description]

| Value | Label | Confidence | Source |
|-------|-------|------------|--------|
| 13:31 | Duration | CONFIRMED | Video player UI + ytInitialData |
| 2,582 | Views | CONFIRMED | ytInitialData viewCountFactoidRenderer |
| 120 | Likes | CONFIRMED | Video page + ytInitialData |
| Jul 15, 2026 | Upload date | CONFIRMED | ytInitialData publishDate |
| 88.6K | Channel subscribers | CONFIRMED | Video page |
| 3 | Chapter count | CONFIRMED | macroMarkersListRenderer |
| 0:00 | Chapter 1 start | CONFIRMED | macroMarkersListItemRenderer |
| 3:15 | Chapter 2 start | CONFIRMED | macroMarkersListItemRenderer |
| 7:20 | Chapter 3 start | CONFIRMED | macroMarkersListItemRenderer |

---

## Resources Referenced [CONFIRMED from description]

| Resource | URL (partial) | Type |
|----------|---------------|------|
| Quant Guild main | https://quantguild.com | Course platform |
| Personal Hedge Fund course | https://quantguild.com/personal-hedge-fund | Course |
| IBKR Algo Trading | https://www.interactivebrokers.com/mkt/?src=quantguildY... | Broker/Partner |
| Discord | discord.gg/MJ4FU2c6c3 | Community |
| Jupyter Notebook | github.com/romanmichaelpaolucci... | Code artifact |
| IBKR Setup Video | (linked in description) | Prerequisite video |
| Options Chain Video | (linked in description) | Related video |
| Quant Guild Library | github.com/romanmichaelpaolucci... | Code repo |
| GitHub (personal) | github.com/RomanMichaelPaolucci | Profile |
| GitHub (org) | github.com/Quant-Guild | Org |
| Medium Blog | medium.com/@quantguild | Blog |
| Gaussian Cookbook | gaussiancookbook.com | Project |
| Stochastic Process Recipes | papers.ssrn.com/sol3/papers.c... | Research |
| TikTok | tiktok.com/@quantguild | Social |
| Instagram | instagram.com/quantguild | Social |
| X/Twitter | x.com/quantguild | Social |
| LinkedIn (personal) | linkedin.com/in/rmp99 | Social |
| LinkedIn (company) | linkedin.com/company/quant-guild | Social |

---

## Related Videos Referenced [CONFIRMED from description]

| Title | Playlist/Category |
|-------|-------------------|
| How to Build a Live Volatility Surface in Python (Interactive Brokers) | Quant Builds 🔨 |
| Statistics and Trading Profitability Over Time (Edge) 📈 | Statistics and Trading Profitability Over Time (Edge) |
| Time Series Analysis for Quant Finance | Time Series Analysis for Quant Finance |
| Quant Trader on Retail vs Institutional Trading | Quant Trader on Retail vs Institutional Trading |
| Quant on Trading and Investing | Quant on Trading and Investing |
| Why Poker Pros Make the Best Traders (It's NOT Luck) | (standalone) |
| Quant vs. Discretionary Trading | Quant vs. Discretionary Trading |

---

## TOOL FAILURES / GAPS [Per §−1.4.6]

| Gap | Reason | Tag | Impact |
|-----|--------|-----|--------|
| Full transcript | No captions available (auto or manual); browser-only cannot POST to get_transcript | MISSING | Cannot extract exact formulas, code, parameter values, verbal explanations |
| Visual content | Tier C - no vision capability | UNVERIFIED (no vision) | Cannot verify on-screen formulas, code, charts |
| Notebook content | GitHub link truncated in ytInitialData (shows "...") | MISSING | Need to fetch notebook separately via browser |

---

## Extraction Methodology Notes

**Reliable ytInitialData paths used** (browser_console IIFE):
- Description: `window.ytInitialData.contents.twoColumnWatchNextResults.results.results.contents[1].videoSecondaryInfoRenderer.attributedDescription.content`
- Chapters: `window.ytInitialData.engagementPanels` → find `macroMarkersListRenderer` → `contents[*].macroMarkersListItemRenderer`
- Video metadata: `contents[0].videoPrimaryInfoRenderer`, `contents[1].videoSecondaryInfoRenderer`

**Transcript limitation**: In browser-only Tier C, the internal `/youtubei/v1/get_transcript` endpoint requires POST (blocked). Public `/api/timedtext` endpoints returned empty. This is a structural limitation, not a tool error.

---

## Next Steps for Complete Extraction

1. **Fetch GitHub notebook** - Navigate to the notebook URL from description (truncated to `github.com/romanmichaelpaolucci...`). Use notebook-extraction.md pattern.
2. **If transcript becomes available** - Extract exact code, formulas, library versions, parameter choices.
3. **Cross-reference** with Video 01 (Sharpe Ratios) and Video 03 (Quant Portfolio Management) for learning progression.
4. **Document IBKR API patterns** - Connection, portfolio retrieval, return calculation methodology.

---

## Synthesis / Agent Notes [INFERRED - clearly separated per §−1.4.8]

This video is a **reference implementation** for a core quant finance calculation (portfolio alpha/beta). The creator's TL;DW is unusually rigorous — explicitly naming the joint hypothesis problem and warning about non-stationarity of risk metrics. This signals the channel's depth: it's not just "how to calculate" but "how to interpret correctly."

**Learning progression hypothesized**:
- Video 01: Sharpe Ratios (risk-adjusted returns)
- **Video 02: Alpha/Beta (CAPM decomposition) ← CURRENT**
- Video 03: Quant Portfolio Management (57min - comprehensive)
- Video 19: Volatility Drag (advanced concept)

**Code artifact priority**: The GitHub notebook is the primary recovery target for the missing transcript. It likely contains the complete IBKR → pandas → statsmodels pipeline.

**Confidence assessment**: All description-derived claims are CONFIRMED. Chapter structure is CONFIRMED. Inferred technical details are explicitly tagged INFERRED. No fabrication.

---

## Confidence Tags Legend
- **CONFIRMED**: Directly observed from successful tool output (ytInitialData, DOM)
- **TRANSCRIBED**: Read from transcript/captions (NOT available here)
- **INFERRED**: Deduced from context, title, chapter structure, channel patterns
- **UNVERIFIED**: Visual element not confirmed by vision
- **MISSING**: Data could not be obtained
- **TOOL FAILURE**: Tool error prevented extraction (distinct from structural unavailability)