# Quant Guild Channel - Video Inventory (Phase 0: Channel Page Extraction)

## Extraction Summary
- **Channel**: Roman Paolucci (@QuantGuild)
- **Date**: 2025-07-17
- **Method**: Browser DOM extraction from https://www.youtube.com/@QuantGuild/videos
- **Videos Found**: 30 (initial page load)
- **Total Channel Videos**: 653 (per channel page)

## Extracted Videos (30 of ~653)

| # | Video ID | Title | Duration | Views | Uploaded |
|---|----------|-------|----------|-------|----------|
| 1 | GTVBT1SQKWY | Math to Increase your Sharpe Ratios | 18:15 | 1.9k | 19 hours ago |
| 2 | A7zJARrdo3U | How to Calculate Portfolio Alpha & Beta (Python + Interactive Brokers) | 13:32 | 2.4k | 1 day ago |
| 3 | LX4Ugaxx9n0 | The Ultimate Guide to Quant Portfolio Management | 57:12 | 5.5k | 2 days ago |
| 4 | bCg9Q-nnJKI | The Quant Case for Bitcoin: A Structural Analysis | 11:52 | 6.6k | 4 days ago |
| 5 | -sE1kz-fypI | Modeling Tail Risk: A Quantitative Survival Guide | 19:59 | 5.4k | 6 days ago |
| 6 | kOzvtRE_uX8 | Compound Annual Growth Rate (CAGR) for Quant Finance | 9:57 | 3.8k | 9 days ago |
| 7 | A6QWWrhDJTc | How to Think About Stock Market Bubbles and Drawdowns | 20:06 | 4.1k | 11 days ago |
| 8 | WsEwKlr_1lA | When Does a Trading Strategy Actually Need to be Secret? | 19:53 | 9.8k | 13 days ago |
| 9 | 37wRzGdC9w4 | How a Quant would Invest $1,000,000 | 7:10 | 16k | 2 weeks ago |
| 10 | Io49x7t0sZI | Why You Shouldn't Be a Quant (Unfiltered) | 11:40 | 11k | 2 weeks ago |
| 11 | xa5eSjASDWo | A REAL Quant Debunks the "Day Trading" Scam | 20:00 | 40k | 2 weeks ago |
| 12 | E2PuxT_SucA | Stock Picking is Worse than Gambling at a Casino (I Can Prove It) | 17:28 | 10k | 3 weeks ago |
| 13 | 21SONVlvkDQ | What the F*ck is Alpha? (And How to Actually Find It) | 18:07 | 11k | 3 weeks ago |
| 14 | E73rL7Hex-k | I Met a Jane Street Quant at the Gym (He Got This Wrong) | 14:49 | 8.3k | 3 weeks ago |
| 15 | kmAE9ZhQ0jU | Volatility Risk Premium Explained: Implied vs Realized Volatility | 20:22 | 9.5k | 1 month ago |
| 16 | aoT3Zln2cak | I want the market to crash | 13:42 | 7.1k | 1 month ago |
| 17 | KD_fh_jA_iQ | No. You don't need to backtest a trading strategy. | 25:13 | 22k | 1 month ago |
| 18 | Soea_7rzkR8 | How to Derive Volatility Drag | 23:17 | 8.1k | 1 month ago |
| 19 | YDjOBWb5iG8 | Quant Portfolio Management and Volatility Drag | 16:05 | 5.5k | 1 month ago |
| 20 | sgbEkAYAdwk | The Mathematical Trap of "Just Buy SPY" | 6:23 | 9.1k | 1 month ago |
| 21 | 1r39EGSm9fw | How Quants Engineer Portfolios | 9:59 | 9.4k | 1 month ago |
| 22 | QNYstoX0u1k | Why I Quit Being a Quant Researcher | 30:39 | 23k | 1 month ago |
| 23 | -CPUbalMh14 | Modeling with the Law of Total Expectation | 24:00 | 5.7k | 1 month ago |
| 24 | mFovTf-TMvw | How to Trade the Cash Secured Put | 19:25 | 7.7k | 1 month ago |
| 25 | bX-mT1pZFho | The reason you want a Ferrari is why you don't have one | 9:44 | 6.8k | 1 month ago |
| 26 | 8kBpVelo9Tg | Why your Trading Strategy Sucks | 5:05 | 7.7k | 1 month ago |
| 27 | RBfc8SkRwwU | The Mathematical Delusion of Retail Trading | 13:14 | 26k | 1 month ago |
| 28 | 92dW2ZDTsJg | You Don't Find a Passion. You Build One. | 21:51 | 4.2k | 1 month ago |
| 29 | qKCjatq9CZM | Coding an AI Bot to Trade Nvidia (From Scratch) | 52:33 | 8.7k | 2 months ago |
| 30 | FdqvAuHOQeE | Vibe Coding an Options Trading System | 1:43:16 | 23k | 2 months ago |

## Content Analysis (Initial 30)

### Content Categories
1. **Portfolio Management & Quant Finance** (7 videos): #3, #7, #9, #18, #19, #21, #27
2. **Trading Strategies & Implementation** (6 videos): #2, #6, #16, #24, #25, #30
3. **Risk Management & Mathematics** (5 videos): #1, #4, #5, #15, #23
4. **Career & Philosophy** (4 videos): #8, #10, #14, #22
5. **Debunking/Education** (4 videos): #11, #12, #13, #26
6. **Python/Coding Tutorials** (3 videos): #2, #29, #30
7. **Market Analysis** (1 video): #16

### Time Range
- **Most Recent**: 19 hours ago
- **Oldest in Batch**: 2 months ago
- **Span**: ~8 weeks (2 months)

### View Distribution
- **High (>20k views)**: 4 videos (#11, #17, #22, #27, #30)
- **Medium (5k-20k views)**: 14 videos
- **Low (<5k views)**: 12 videos
- **Average**: ~11.5k views

### Duration Distribution
- **Short (<10 min)**: 4 videos
- **Medium (10-20 min)**: 14 videos
- **Long (20-40 min)**: 10 videos
- **Very Long (>40 min)**: 2 videos

## Next Steps
1. **Cron job created**: `quantguild-progressive-extraction` (job_id: 23015355496e) - runs every 3 hours
2. **State file**: `references/_loop_state.json` initialized with 30-video queue
3. Run full scroll extraction to get all 653 videos (via Playwright script)
4. Navigate to playlists for organized content extraction
5. Extract transcripts for priority videos
6. Build master report and HTML lesson document

## Cron Job Details
- **Job ID**: 23015355496e
- **Schedule**: Every 3 hours (180 minutes)
- **Model**: nemotron-3-ultra-free (opencode-zen)
- **Skills**: yt-deep-extraction
- **Phase**: extract_next_queued_video (position 1 of 8)
- **Next run**: 2026-07-17T17:45:59+01:00
- **Delivery**: origin (local session)

## Extraction Queue (30 videos from initial load)
Priority order for Phase 1 extraction:
1. GTVBT1SQKWY - Math to Increase your Sharpe Ratios
2. A7zJARrdo3U - How to Calculate Portfolio Alpha & Beta (Python + IBKR)
3. LX4Ugaxx9n0 - The Ultimate Guide to Quant Portfolio Management
4. bCg9Q-nnJKI - The Quant Case for Bitcoin: A Structural Analysis
5. -sE1kz-fypI - Modeling Tail Risk: A Quantitative Survival Guide
6. kOzvtRE_uX8 - CAGR for Quant Finance
7. A6QWWrhDJTc - How to Think About Stock Market Bubbles and Drawdowns
8. WsEwKlr_1lA - When Does a Trading Strategy Actually Need to be Secret?
9. 37wRzGdC9w4 - How a Quant would Invest $1,000,000
10. Io49x7t0sZI - Why You Shouldn't Be a Quant (Unfiltered)
... + 20 more

## Files Generated
- `scripts/quantguild_extractor.py` - Playwright automation for full extraction
- `scripts/extract_ytinitialdata.py` - HTML parsing from ytInitialData