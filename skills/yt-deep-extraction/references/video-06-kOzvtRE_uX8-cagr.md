# Video 06: Compound Annual Growth Rate (CAGR) for Quant Finance

- **URL**: https://youtube.com/watch?v=kOzvtRE_uX8
- **Video ID**: kOzvtRE_uX8
- **Uploaded**: 2025-07-08 (9 days ago from extraction)
- **Duration**: 9:57
- **Views**: 3.8K
- **Channel**: Roman Paolucci (@QuantGuild)
- **Extraction Date**: 2025-07-17
- **Confidence**: CONFIRMED (metadata from DOM/ytInitialData)

---

## Metadata Summary

**Title**: Compound Annual Growth Rate (CAGR) for Quant Finance

**Description** (from video page, truncated in snapshot):
> 🚀 Master Quantitative Skills with Quant Guild
> https://quantguild.com
> … (description expanded via "...more" button, full text not captured in snapshot)

**Links in Description**:
- https://quantguild.com
- (4 more links indicated)

**Chapter marker visible in player**: None visible in initial snapshot

---

## Transcript-Derived Content

**TRANSCRIPT STATUS**: MISSING (Subtitles/closed captions unavailable - button shows "Subtitles/closed captions unavailable")

**Note**: No transcript could be extracted. Content below is INFERRED from title, description fragments, and channel context.

---

## [00:00 – 09:57] CAGR for Quant Finance

### Key Claims / Knowledge (INFERRED)
- Video explains Compound Annual Growth Rate (CAGR) in the context of quantitative finance
- Likely covers: CAGR formula, geometric mean vs arithmetic mean, log returns, annualization
- Channel context suggests: mathematical derivation, practical calculation, Python implementation
- May address: common pitfalls (arithmetic vs geometric, volatility drag, survivorship bias)

### Likely Topics Covered:
1. **CAGR Definition** - (Ending Value / Beginning Value)^(1/n) - 1
2. **Geometric vs Arithmetic Mean** - Why CAGR uses geometric, impact of volatility
3. **Log Returns & Continuous Compounding** - ln(P_t/P_0)/t relationship
4. **Volatility Drag** - How variance reduces compound growth (approximation: CAGR ≈ μ - σ²/2)
5. **Practical Calculation** - From price series, handling dividends/splits, benchmarking
6. **Python Implementation** - pandas/numpy for CAGR, rolling CAGR, comparison to buy-and-hold

### Data Points & Statistics
- None captured (transcript missing)

### Code / Techniques Shown (INFERRED)
- numpy/pandas for return calculations
- `np.log()`, `np.exp()` for continuous compounding
- `pct_change()`, `cumprod()` for wealth index
- Rolling window CAGR: `(1 + returns).rolling(n).apply(lambda x: x.prod()**(1/n) - 1)`
- Benchmarking: strategy CAGR vs SPY CAGR

### Visual Elements
- **0:00-9:57** - Total duration
- Player shows: 1080p60 available, subtitles unavailable

---

## Visual Elements Registry

| Timestamp | Type | Description | Confidence |
|-----------|------|-------------|------------|
| 0:00-9:57 | Video content | Formulas, charts, Python code | UNVERIFIED (no vision) |

---

## Key Takeaways (INFERRED)
- CAGR is the correct metric for long-term growth (not arithmetic average)
- Volatility drag is real and quantifiable: CAGR ≈ Arithmetic Mean - 0.5*Variance
- Proper annualization requires geometric compounding, not simple multiplication
- Implementation in Python is straightforward but requires careful handling of edge cases

---

## Connections to Other Videos
- **Video #1** (GTVBT1SQKWY): "Math to Increase your Sharpe Ratios" - CAGR is component of Sharpe
- **Video #3** (LX4Ugaxx9n0): "Ultimate Guide to Quant Portfolio Management" - CAGR as performance metric
- **Video #19** (YDjOBWb5iG8): "Quant Portfolio Management and Volatility Drag" - directly related
- **Theme**: Return metrics, risk-adjusted performance

---

## Numbers Ledger [from video page extraction]

| Value | Label | Confidence | Source |
|-------|-------|------------|--------|
| 9:57 | Duration | CONFIRMED | Video player UI |
| 3,800 | Views | CONFIRMED | Video page |
| 198 | Likes | CONFIRMED | Video page |
| 9 days ago | Upload time | CONFIRMED | Video page |

---

## TOOL FAILURES
- **Transcript extraction**: Subtitles unavailable (button shows "Subtitles/closed captions unavailable")
- **Full description**: Truncated in snapshot; "...more" button clicked but full text not captured
- **Transcript panel**: Not accessible (no captions)

---

## Synthesis / Agent Notes [INFERRED]
This is a foundational metrics video - CAGR is one of the most basic yet commonly misunderstood return metrics in quant finance. The channel's mathematical approach means this likely covers:
- The exact formula and why it works
- The approximation CAGR ≈ μ - σ²/2 (from Ito's lemma)
- Common mistakes: using arithmetic mean, ignoring dividends, wrong annualization
- Python code that handles real-world data issues (splits, dividends, missing data)

**Priority for re-extraction**: HIGH - CAGR is a building block metric used throughout the channel's content. If transcript becomes available, the mathematical derivation and code would be valuable to capture.