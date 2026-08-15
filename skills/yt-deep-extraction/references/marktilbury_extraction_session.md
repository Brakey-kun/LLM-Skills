# Mark Tilbury Channel Extraction — Session Reference

**Channel**: Mark Tilbury (@marktilbury)  
**URL**: https://www.youtube.com/@marktilbury  
**Date**: 2025  
**Total Videos**: 353  
**Subscribers**: 8.65M  

---

## Extraction Summary

| Phase | Status | Notes |
|-------|--------|-------|
| Phase −1 (Environment) | ✅ Complete | Tier A — full capability (shell + browser + vision) |
| Phase 0 (Recon) | ✅ Complete | 11 themes identified, 12+ language playlists |
| Phase 1 (Per-Video) | ✅ Complete | 353/353 videos extracted |
| Phase 2 (Master Report) | ✅ Complete | Lossless thematic aggregation |
| Phase 3 (HTML Lesson) | ✅ Complete | Interactive lesson.html with 7 components |
| Phase 4 (Verification) | ✅ Complete | Fidelity audit passed |

---

## Key Technical Learnings

### 1. yt-dlp Channel URL Matters
- **Wrong**: `yt-dlp --flat-playlist "https://www.youtube.com/@marktilbury/videos"` → Returns ~102 videos (first pagination batch only)
- **Correct**: `yt-dlp --flat-playlist "https://www.youtube.com/@marktilbury"` → Returns ALL 353 videos including Shorts

The `/videos` endpoint paginates; the channel root URL returns the complete flat playlist.

### 2. Windows/MSYS Terminal Fork Crash (0xC0000142)
The `terminal` tool and `write_file` tool fail on Windows with git-bash due to broken `fork()` syscall.

**Working workaround**: All extraction logic runs via `execute_code` with Python's `subprocess.run()` — this bypasses the shell entirely.

### 3. Shorts Without Captions
2 of 353 videos (Shorts) had no auto-captions:
- `tO7KFTdPNu0` — "How To Spot A Fake $100! 💵 #shorts"
- `03Q2Nck4MBY` — "ALL INVESTORS BEWARE OF THIS 😳 #shorts"

These are tagged `MISSING` in the transcript field — correct behavior per Fidelity Protocol.

### 4. Content Distribution (353 videos)
| Theme | Count |
|-------|-------|
| Investing Education | ~85 |
| Money Psychology & Habits | ~55 |
| Side Hustles & Income | ~45 |
| Spending & Saving (Cost vs Price) | ~35 |
| Wealth Frameworks | ~25 |
| Case Studies/Interviews | ~20 |
| AI & Tech Impact | ~15 |
| Consumer Education (Brand Scams) | ~20 |
| Career & Jobs | ~15 |
| Tax & Legal | ~12 |
| Shorts (Viral Clips) | ~30 |

### 5. Raw Data Volume
- 353 meta.json files (~7 MB each = ~2.5 GB)
- 351 transcript files (~200-500 KB each = ~100 MB)
- 353 description files (~1-4 KB each = ~1 MB)
- Total: ~2.6 GB in `raw/`

---

## Extraction Commands (for replay)

```bash
# 1. Get complete channel list (use channel ROOT, not /videos)
yt-dlp --flat-playlist --dump-json "https://www.youtube.com/@marktilbury" > raw/_channel.videos.full.jsonl

# 2. Batch extract (run via Python execute_code, not terminal)
python scripts/batch_extract_videos.py \
  --output-dir "C:/Users/amine/yt-extraction-marktilbury" \
  --channel-url "https://www.youtube.com/@marktilbury" \
  --batch-size 20 \
  --start-index 0

# Repeat with --start-index 20, 40, 60... until all 353 done
```

---

## Output Files Created

| File | Description |
|------|-------------|
| `_environment.md` | Tier A capability probe results |
| `_channel-overview.md` | Channel metadata + 11 themes + 12 language playlists |
| `_extraction-plan.md` | 353-video queue with priorities |
| `_numbers.md` | Full statistics ledger (views, likes, duration, dates) |
| `master-report.md` | Lossless thematic aggregation (11 sections) |
| `lesson.html` | Interactive lesson (7 components: catalog tabs, formulas, concept network, timeline, search) |
| `video-001` through `video-353.md` | Per-video reports with metadata, chapters, transcript excerpts |
| `raw/` | Ground truth: 353 × {meta.json, en.json3, description.txt} |

---

## Fidelity Tags Applied

| Tag | Videos | Notes |
|-----|--------|-------|
| CONFIRMED | 353 | All yt-dlp metadata (views, duration, dates, chapters) |
| TRANSCRIBED | 351 | Auto-captions (en.json3) — timing drift possible |
| INFERRED | N/A | Cross-video syntheses in master report only (clearly labeled) |
| UNVERIFIED | All visuals | No vision tool used; screenshots not captured |
| MISSING | 2 | Shorts without auto-captions |

---

## Known Limitations Documented

1. **Only 351/353 transcripts** — 2 Shorts lack auto-captions (correctly tagged MISSING)
2. **No visual verification** — All charts/screenshots tagged UNVERIFIED
3. **Auto-caption errors possible** — Technical terms, numbers, proper nouns may be mis-transcribed
4. **No comment analysis** — Community sentiment not captured
5. **Age-restricted/private videos** — Not accessible via public API

---

## Next Steps for Future Enrichment

1. **Visual capture** — Browser automation at chapter markers for top 50 videos
2. **Caption verification** — Manual review of key videos (investing frameworks, stock picks)
3. **Cross-channel** — Extract "Mark Tilbury Economics" channel
4. **RAG system** — Build searchable knowledge base over 351 transcripts
5. **Scheduled updates** — Cron job for new uploads (channel posts ~2-3 videos/week)