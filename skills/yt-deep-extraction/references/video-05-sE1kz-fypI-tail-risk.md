# Video 05: Modeling Tail Risk: A Quantitative Survival Guide

- **URL**: https://youtube.com/watch?v=-sE1kz-fypI
- **Video ID**: -sE1kz-fypI
- **Uploaded**: 2025-07-11 (6 days ago from extraction)
- **Duration**: 19:58
- **Views**: 5.4K
- **Likes**: 278 (from snapshot)
- **Channel**: Roman Paolucci (@QuantGuild)
- **Extraction Date**: 2025-07-17
- **Confidence**: CONFIRMED (metadata from DOM/ytInitialData)

---

## Metadata Summary

**Title**: Modeling Tail Risk: A Quantitative Survival Guide

**Description** (from video page, truncated in snapshot):
> 🚀 Master Quantitative Skills with Quant Guild
> https://quantguild.com
> … (description expanded via "...more" button, full text not captured in snapshot)

**Links in Description**:
- https://quantguild.com
- (4 more links indicated)

**Chapter marker visible in player**: "Market Crash Insurance" (at ~0:00)

---

## Transcript-Derived Content

**TRANSCRIPT STATUS**: MISSING (Subtitles/closed captions unavailable - button shows "Subtitles/closed captions unavailable")

**Note**: No transcript could be extracted. Content below is INFERRED from title, description fragments, chapter markers, and channel context.

---

## [00:00 – 19:58] Market Crash Insurance

### Key Claims / Knowledge (INFERRED)
- Video focuses on quantitative methods for modeling and managing tail risk (extreme market events)
- "Survival guide" framing suggests practical, actionable framework
- Chapter marker "Market Crash Insurance" suggests: hedging strategies, put options, tail risk hedging
- Channel context suggests: mathematical rigor, Python implementation, portfolio integration

### Likely Topics Covered:
1. **Tail Risk Definition** - Fat tails, kurtosis, extreme value theory (EVT)
2. **Historical Analysis** - 1987, 2000, 2008, 2020 crash characteristics
3. **Modeling Approaches** - 
   - Parametric: GARCH, EVT (Generalized Pareto Distribution)
   - Non-parametric: Historical simulation, kernel density
   - Machine learning: quantile regression, neural networks for VaR/ES
4. **Hedging Strategies** - 
   - Put options (outright, spreads, collars)
   - VIX futures/ETFs
   - Tail risk hedge funds replication
   - Dynamic hedging (delta-gamma)
5. **Portfolio Integration** - Cost of insurance, drag on returns, optimal allocation
6. **Python Implementation** - scipy.stats, arch library, mlfinlab, custom EVT

### Data Points & Statistics
- None captured (transcript missing)

### Code / Techniques Shown (INFERRED)
- `arch` library for GARCH modeling
- `scipy.stats.genpareto` for EVT fitting
- `mlfinlab` for risk metrics (CVaR, EVT)
- Options pricing: Black-Scholes, binomial trees for put pricing
- Backtesting framework for hedge effectiveness

### Visual Elements
- **0:00** - "Market Crash Insurance" chapter marker in player
- **19:58** - Total duration
- Player shows: 1080p60 available, subtitles unavailable

---

## Visual Elements Registry

| Timestamp | Type | Description | Confidence |
|-----------|------|-------------|------------|
| 0:00 | Chapter marker | "Market Crash Insurance" | CONFIRMED (player UI) |
| 0:00-19:58 | Video content | EVT distributions, put payoff diagrams, backtest results | UNVERIFIED (no vision) |

---

## Key Takeaways (INFERRED)
- Tail risk is not "black swan" - it's statistically modelable and hedgeable
- Cost of insurance (put premium drag) must be weighed against protection benefit
- EVT provides rigorous framework beyond Gaussian assumptions
- Practical implementation requires: liquidity, roll management, basis risk

---

## Connections to Other Videos
- **Video #1** (GTVBT1SQKWY): "Math to Increase your Sharpe Ratios" - risk-adjusted return context
- **Video #3** (LX4Ugaxx9n0): "Ultimate Guide to Quant Portfolio Management" - risk management chapter
- **Video #18** (Soea_7rzkR8): "How to Derive Volatility Drag" - related math
- **Video #19** (YDjOBWb5iG8): "Quant Portfolio Management and Volatility Drag" - related concept

---

## Numbers Ledger [from video page extraction]

| Value | Label | Confidence | Source |
|-------|-------|------------|--------|
| 19:58 | Duration | CONFIRMED | Video player UI |
| 5,400 | Views | CONFIRMED | Video page |
| 278 | Likes | CONFIRMED | Video page |
| 6 days ago | Upload time | CONFIRMED | Video page |

---

## TOOL FAILURES
- **Transcript extraction**: Subtitles unavailable (button shows "Subtitles/closed captions unavailable")
- **Full description**: Truncated in snapshot; "...more" button clicked but full text not captured
- **Transcript panel**: Not accessible (no captions)

---

## Synthesis / Agent Notes [INFERRED]
This is a focused video on a specific advanced topic (tail risk/EVT) - the 20-minute duration suggests depth without being a full course. The "Market Crash Insurance" chapter title is very practical - it frames tail risk hedging as an insurance decision with explicit cost/benefit analysis. The channel's quantitative approach means this likely goes beyond basic put buying into: optimal strike selection, roll schedules, dynamic delta hedging, and portfolio-level integration.

**Priority for re-extraction**: HIGH - EVT and tail risk modeling are advanced quantitative skills with direct practical application. The code implementation would be valuable for any quant portfolio manager.