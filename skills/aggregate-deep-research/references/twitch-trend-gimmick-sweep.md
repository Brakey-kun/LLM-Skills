# Twitch / Trend / Gimmick / Content-Creator Sweep

## When to Use

When expanding into the content-creator domain (streamer tools, viral apps, trend-adaptive websites, fun/gimmicky ideas). This domain has different characteristics than utility/mining subjects — prioritize shareable output, viewer participation, low build time, and high entertainment value.

## What Makes a Good Twitch/Trend/Gimmick Idea

- **Can be used in Twitch streams**: overlays, chat games, viewer interactions, polls, prediction markets, soundboards, channel-point redeems
- **Trend-adaptive**: tied to TikTok/Instagram trends, meme formats, seasonal events, viral challenges
- **Gimmicky but engaging**: reaction checkers, personality tests, tier lists, bracket generators, roasts, AI dares, "which X are you" quizzes
- **Generates shareable output**: screenshots, clips, URLs that people post to social media — the tool markets itself
- **Low dev time (T1-T2)**: hours to a few days — content trends peak in 48 hours

## Search Patterns

### HN Algolia (most reliable)
```
"show HN fun"
"browser game"
"meme generator"
"twitch tool"
"stream overlay"
"viral app"
"party game"
"reaction tool"
"chat game"
"interactive stream"
```

### YouTube
```
"twitch extension idea"
"stream overlay tutorial"
"fun browser app"
"viral web game"
```

### DuckDuckGo Lite / General
```
"streamer tool"
"fun web app viral"
"gimmick website"
"trending app tiktok"
"discord bot game"
"viral website idea"
"streamer engagement tool"
```

## Validation Sources

| Source | Reliability | What to Look For |
|--------|-------------|------------------|
| Twitch API docs | ✅ High | Extension capabilities, PubSub events, channel points |
| StreamElements/Streamlabs blogs | ✅ High | Streamer usage patterns, popular features |
| r/Twitch | ⚠️ Mixed (Cloudflare) | Streamer requests, pain points (may need search snippet fallback) |
| Streamer Discord servers | ✅ (if accessible) | Direct feedback, feature requests |
| Twitch extension marketplace | ✅ High | Gaps in existing offerings, under-served categories |
| TikTok trends | ⚠️ (snippet) | Viral formats, "which X are you" trends |
| Jackbox Games | ✅ High | Party game market validation ($150M+ revenue) |

## Category Classification

Use category `"twitch"` with custom badge styling:
```css
.badge-cat.twitch{background:rgba(168,85,247,0.15);color:#a855f7}
```

Most ideas are T1 (Hours, 2hr-2d) or T2 (Weekend, 1-7d). Sprint/Platform ideas are rare in this domain — if build time exceeds a week the trend window will pass.

## Entry Template for Twitch Ideas

Each idea follows the same SOURCE/MY ANALYSIS format as other domains, but with Twitch-specific framing:

### Section: Intent & Origin [SOURCE]
Focus on: existing streamer pain points, missing tool gaps, proven engagement patterns (mention specific subreddits/forums/streamer behaviors).

### Section: Design Objective [SOURCE]
Focus on: OBS browser source compatibility, chat integration (IRC/PubSub), no-signup-required workflows, overlay-friendly sizing, real-time interactivity.

### Section: My Analysis [MY ANALYSIS]
Three dimensions:
1. **UX**: How does chat participate? Is the output shareable? Does it work in 30-second ad breaks?
2. **Monetization**: Free core → Pro tier ($3-6/mo) for custom themes, pack creation, export features. Twitch extensions can use Bits/Channel Points.
3. **Differentiation**: Why would a streamer choose this over existing tools? Speed, focus, visual polish, no bloat.

## Example Seed Ideas (from the 133-idea project)

The following 18 ideas were seeded as a Twitch/trend/gimmick category in a 133-idea corpus. They demonstrate the pattern:

| # | Name | Tier | Key Hook |
|---|------|------|----------|
| 116 | Stream Soundboard — Chat-Triggered Effects | Weekend | Viewers type !sound → plays audio |
| 117 | Chat Pet / Dino — Viewers Control On-Screen Character | Weekend | Chat votes move pixel-art character |
| 118 | Stream Prediction Market — Channel Points Stock Exchange | Weekend | Real-time share trading with channel points |
| 119 | Trend Tier List Maker — Drag-Drop Ranking | Hours | 50M+ TierMaker visits prove demand |
| 120 | AI Roast Battle — Two Personas, Chat Votes | Weekend | r/RoastBattle has 1M+ subs |
| 121 | Live Bingo Card Generator — Stream Moment Bingo | Hours | Streamer bingo events get 10K+ viewers |
| 122 | Mood Board Collage Maker — Shareable Vibe Boards | Hours | #moodboard has 2M+ Instagram posts |
| 123 | Stream Trivia — Chat vs Streamer Quiz Show | Weekend | Jackbox $150M+ revenue proves market |
| 124 | Viral Meme Template Generator — Trend-Ready Maker | Hours | Imgflip serves 500M+ memes/year |
| 125 | Twitch 'Would You Rather?' Stream Deck | Hours | r/WouldYouRather has 500K+ subs |
| 126 | 'Guess the Screenshot' — Chat Guessing Game | Hours | GeoGuessr has 5M+ monthly players |
| 127 | Reaction Rating Slider — Rate Anything Real-Time | Hours | RateMyProfessors 5M+ visits/month |
| 128 | Stream Sound Alert — Donation/Follow Sound Manager | Weekend | Streamlabs processes $100M+ yearly |
| 129 | Bracket Generator — Tournament Voting for Any Topic | Hours | March Madness gets 60M+ bracket entries |
| 130 | AI Personality Quiz — 'Which X Are You?' Generator | Weekend | BuzzFeed quizzes drive 360M+ completions |
| 131 | 'This or That' Hot Takes — Chat Opinion Arena | Hours | Instagram story polls: 500M+ daily users |
| 132 | Meme Review Generator — Commentator-Style Judge | Weekend | PewDiePie Meme Review: 500M+ views |
| 133 | Stream Challenge Wheel — Chat-Spun Dare Generator | Hours | Challenge wheels hit Twitch front page |

## Pitfalls

1. **Trend-window too short**: Don't recommend week-long builds for 48-hour trends. Filter by tier.
2. **OBS compatibility**: Not all web tech works in OBS browser sources. Avoid WebGL-heavy or audio-capture-dependent features unless verified.
3. **Chat spam**: Twitch chat-based tools must rate-limit commands (e.g. 30s cooldown per user) to avoid stream-chat disruption.
4. **API keys in overlays**: Never embed API keys in OBS browser sources — viewers can inspect the source. Use server-side proxy or Twitch EBS.
5. **Gambling gray area**: Prediction markets and chance-based mechanics can violate Twitch ToS. Always label as "for entertainment, no real value."
