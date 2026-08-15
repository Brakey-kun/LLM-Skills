# Channel Reconnaissance Example: Quant Guild (@QuantGuild)

This is a concrete example of Phase 0 channel reconnaissance performed July 2026.

## Step 1: Navigate to Channel Videos Page

```
browser_navigate("https://www.youtube.com/@QuantGuild/videos")
```

Extract visible video cards. YouTube renders 30 initial videos.

## Step 2: Extract Video List

```javascript
// From browser_console:
document.body.innerText  // captions all visible video titles, view counts, dates
```

**What to look for**: Title patterns, view count range, upload frequency, content categories.

## Step 3: Navigate to Playlists Page

```
browser_navigate("https://www.youtube.com/@QuantGuild/playlists")
```

Playlists reveal the channel's own content categorization system. Extract:
- Playlist name → number of videos
- Playlist name → theme description (emoji often signals category)

## Step 4: Classify Content from Playlists

### Playlist Catalog (July 2025 — Updated from Live Extraction)

| # | Playlist | Videos | Category | Priority for Quant Goal |
|---|----------|--------|----------|------------------------|
| 1 | Getting Started in Quantitative Finance 🗺️ | 82 | Foundation | HIGH (primer) |
| 2 | Practical Quantitative Trading Videos 📈 | 61 | Applied | HIGH |
| 3 | Quantitative Finance 💸 | 151 | Theory + Applied | HIGH (core) |
| 4 | Quant Builds from Scratch 💻 | 13 | Coding | HIGH (implementation) |
| 5 | Financial Mathematics 🏛️ | 12 lessons | Theory | HIGH (math) |
| 6 | Popular Quant Guild Videos 🚀 | 19 | Highest-viewed | MEDIUM |
| 7 | Options Trading 📜 | 6 | Derivatives | MEDIUM |
| 8 | Fireside Chats 🏕️ | 13 | Discussion | LOW |
| 9 | Math for Life 🌱 | 7 | General | LOW |
| 10 | Quant Strats 🧮 | 3 | Strategy | MEDIUM |
| 11 | Quant Finance in 3 Minutes ⏳ | 4 | Quick intros | MEDIUM |
| 12 | Quant Interview Questions 🏛️ | 1 | Interview prep | LOW |
| 13 | Quant Research Seminars 👨🏻‍🏫 | 1 | Research-level | LOW |
| 14 | Quant Guild Livestreams [🔴REC] | 2 | Recorded streams | LOW |
| 15 | Journey to 🚀 Quant V | 3 | Personal journey | LOW |

**Total playlist videos**: ~378 (subset of 653 total — some videos in multiple playlists, some unlisted)

## Step 5: Extract Channel Metadata

From the channel page header:
- **Subscribers**: 88.6K
- **Total videos**: 653
- **Total views**: 5,479,845
- **Joined**: May 24, 2020
- **Description**: Full text from the channel description

## Output: _channel-overview.md

Save the structured output including: channel metadata, content map (playlist table), identified themes, and extraction strategy decision.

## Tips for Channel Recon

1. **Scrolling**: YouTube loads videos lazily. `browser_scroll(down)` multiple times to load more.
2. **Playlists page is critical**: It often reveals the creator's own categorization — use this over your own ad-hoc categories.
3. **View count as signal**: <5K = niche/deep content; 10K-50K = popular/influential; >100K = viral or broad-appeal content. This helps prioritize.
4. **Upload frequency**: Check the dates on the first page of videos. Daily = news/updates; Weekly = planned content; Irregular = passion project.
5. **Channel description links**: Often point to the creator's website, GitHub, Discord, courses — these are valuable companion resources for extraction.
6. **Playlist navigation quirk**: Clicking "View full playlist" or "View full course" buttons on the playlists page may redirect back to the playlists overview rather than opening the playlist. Use browser_console to extract playlist URLs from link hrefs, or navigate directly if you know the playlist ID pattern.
7. **Content themes**: Map emoji prefixes to categories (🗺️=foundation, 📈=applied, 💸=core theory, 💻=coding, 🏛️=math, 📜=derivatives, 🏕️=discussion, 🌱=general, 🧮=strategy, ⏳=quick, 🚀=popular).
