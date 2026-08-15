#!/usr/bin/env python3
"""
yt_analyzer.py — Bulletproof YouTube Analysis Toolkit
======================================================

Single-file, zero-config tool for ALL YouTube analysis tasks:
  • Transcript fetching (dual backend: youtube-transcript-api + yt-dlp fallback)
  • Single video deep metadata extraction
  • Full channel reconnaissance (all videos, stats, playlists)
  • Batch extraction (N videos with progress tracking)
  • Channel analytics (engagement rates, posting frequency, content themes)
  • Playlist extraction
  • Cross-video topic & keyword analysis
  • Export to JSON, CSV, and Markdown

Dependencies auto-installed on first run. Works on Windows/Linux/Mac.
Handles youtube-transcript-api AND yt-dlp as dual backends.

Usage:
    python yt_analyzer.py transcript <url> [--lang en,tr] [--timestamps] [--out file.json]
    python yt_analyzer.py video <url> [--out file.json]
    python yt_analyzer.py channel <channel_url> [--limit N] [--out dir/]
    python yt_analyzer.py batch <channel_url> [--limit N] [--transcripts] [--out dir/]
    python yt_analyzer.py playlist <playlist_url> [--out dir/]
    python yt_analyzer.py analytics <channel_url> [--out report.md]
    python yt_analyzer.py install    # just install dependencies

Author: Hermes Agent (auto-generated)
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
import textwrap
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# --- Version ---
__version__ = "2.0.0"

# --- Dependency Management ---

REQUIRED_PACKAGES = {
    "youtube_transcript_api": "youtube-transcript-api",
}

OPTIONAL_PACKAGES = {
    "yt_dlp": "yt-dlp",
}


def ensure_dependencies():
    """Auto-install missing dependencies."""
    missing = []
    for module, pip_name in REQUIRED_PACKAGES.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(pip_name)

    for module, pip_name in OPTIONAL_PACKAGES.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print(f"Installing missing packages: {', '.join(missing)}")
        for mgr in ["uv", sys.executable]:
            try:
                if mgr == sys.executable:
                    cmd = [sys.executable, "-m", "pip", "install", "--quiet"] + missing
                else:
                    cmd = ["uv", "pip", "install"] + missing
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                if result.returncode == 0:
                    print(f"Installed: {', '.join(missing)}")
                    return True
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        print(f"Failed to install: {', '.join(missing)}")
        print(f"   Run manually: pip install {' '.join(missing)}")
        return False
    return True


# --- URL / ID Parsing ---

VIDEO_ID_PATTERN = re.compile(
    r'(?:youtube\.com/watch\?.*?[&?]v=|youtu\.be/|youtube\.com/shorts/|'
    r'youtube\.com/embed/|youtube\.com/live/)([a-zA-Z0-9_-]{11})'
)
BARE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_-]{11}$')
CHANNEL_HANDLE_PATTERN = re.compile(r'youtube\.com/@([a-zA-Z0-9_.-]+)')
CHANNEL_ID_PATTERN = re.compile(r'youtube\.com/channel/(UC[a-zA-Z0-9_-]{22})')
PLAYLIST_PATTERN = re.compile(r'youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)')


def extract_video_id(url_or_id: str) -> Optional[str]:
    url_or_id = url_or_id.strip()
    match = VIDEO_ID_PATTERN.search(url_or_id)
    if match:
        return match.group(1)
    if BARE_ID_PATTERN.match(url_or_id):
        return url_or_id
    return None


def extract_playlist_id(url: str) -> Optional[str]:
    match = PLAYLIST_PATTERN.search(url)
    return match.group(1) if match else None


def extract_channel_handle(url: str) -> Optional[str]:
    match = CHANNEL_HANDLE_PATTERN.search(url)
    return match.group(1) if match else None


def is_channel_url(url: str) -> bool:
    return bool(CHANNEL_HANDLE_PATTERN.search(url) or CHANNEL_ID_PATTERN.search(url) or
                re.search(r'youtube\.com/@[^/]+/?$', url))


def is_playlist_url(url: str) -> bool:
    return bool(PLAYLIST_PATTERN.search(url))


def format_timestamp(seconds: float) -> str:
    total = int(seconds)
    h, remainder = divmod(total, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def parse_view_count(text: str) -> int:
    text = text.lower().replace(",", "").replace("views", "").strip()
    multipliers = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}
    for suffix, mult in multipliers.items():
        if text.endswith(suffix):
            try:
                return int(float(text[:-1]) * mult)
            except ValueError:
                return 0
    try:
        return int(re.sub(r"[^\d]", "", text) or 0)
    except ValueError:
        return 0


# --- yt-dlp Backend ---

class YtDlpBackend:
    """Wrapper around yt-dlp for metadata and subtitle downloads."""

    def __init__(self):
        self.available = False
        try:
            import yt_dlp
            self.yt_dlp = yt_dlp
            self.available = True
        except ImportError:
            pass

    def _run_yt_dlp(self, args: List[str], timeout: int = 120) -> Optional[str]:
        if not self.available:
            return None
        try:
            cmd = ["yt-dlp"] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
            return None
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return None

    def dump_json(self, url: str) -> Optional[Dict]:
        raw = self._run_yt_dlp(["--dump-json", "--no-playlist", url])
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return None
        return None

    def flat_playlist(self, url: str, limit: int = 0) -> List[Dict]:
        args = ["--flat-playlist", "--dump-json"]
        if limit > 0:
            args += ["--playlist-end", str(limit)]
        args.append(url)
        raw = self._run_yt_dlp(args, timeout=300)
        if not raw:
            return []
        videos = []
        for line in raw.strip().split("\n"):
            if line.strip():
                try:
                    videos.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return videos

    def download_subtitles(self, video_id: str, output_dir: Path,
                           languages: List[str] = None) -> Optional[Path]:
        lang_str = ",".join(languages or ["en"])
        output_template = str(output_dir / f"{video_id}.%(ext)s")
        args = [
            "--write-auto-sub", "--write-sub",
            "--skip-download",
            "--sub-format", "json3",
            "--sub-lang", lang_str,
            "--output", output_template,
            f"https://youtube.com/watch?v={video_id}"
        ]
        self._run_yt_dlp(args, timeout=60)
        for ext in ["json3", "vtt", "srt"]:
            p = output_dir / f"{video_id}.{ext}"
            if p.exists():
                return p
        return None

    def channel_info(self, channel_url: str) -> Optional[Dict]:
        first = self._run_yt_dlp(["--dump-json", "--playlist-items", "1", channel_url])
        if first:
            try:
                data = json.loads(first)
                return {
                    "channel": data.get("channel", ""),
                    "channel_id": data.get("channel_id", ""),
                    "uploader": data.get("uploader", ""),
                    "uploader_id": data.get("uploader_id", ""),
                    "description": data.get("description", ""),
                    "subscriber_count": data.get("channel_follower_count", 0),
                }
            except json.JSONDecodeError:
                pass
        return None


# --- youtube-transcript-api Backend ---

class TranscriptBackend:
    """Wrapper around youtube-transcript-api."""

    def __init__(self):
        self.available = False
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            self.api = YouTubeTranscriptApi()
            self.available = True
        except ImportError:
            pass

    def fetch(self, video_id: str, languages: List[str] = None) -> Optional[List[Dict]]:
        if not self.available:
            return None
        try:
            if languages:
                result = self.api.fetch(video_id, languages=languages)
            else:
                result = self.api.fetch(video_id)
            return [
                {"text": seg.text, "start": seg.start, "duration": seg.duration}
                for seg in result
            ]
        except Exception:
            return None

    def list_languages(self, video_id: str) -> List[str]:
        if not self.available:
            return []
        try:
            tl = self.api.list(video_id)
            return [t.language_code for t in tl]
        except Exception:
            return []


# --- Core Analysis Functions ---

def fetch_transcript(url: str, languages: List[str] = None,
                     timestamps: bool = False) -> Dict[str, Any]:
    """Fetch transcript with dual-backend fallback."""
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": f"Could not extract video ID from: {url}"}

    result = {
        "video_id": video_id,
        "url": f"https://youtube.com/watch?v={video_id}",
        "backend": None,
        "segments": [],
        "full_text": "",
        "timestamped_text": "",
        "duration": "0:00",
        "language": None,
        "available_languages": [],
    }

    segments = []

    # Backend 1: youtube-transcript-api (preferred)
    tb = TranscriptBackend()
    if tb.available:
        result["available_languages"] = tb.list_languages(video_id)
        segments = tb.fetch(video_id, languages) or []
        if segments:
            result["backend"] = "youtube-transcript-api"
            result["segments"] = segments
            result["language"] = languages[0] if languages else "auto"

    # Backend 2: yt-dlp subtitles fallback
    if not segments:
        yb = YtDlpBackend()
        if yb.available:
            sub_file = yb.download_subtitles(video_id, Path("."))
            if sub_file and sub_file.suffix == ".json3":
                try:
                    data = json.loads(sub_file.read_text(encoding="utf-8"))
                    events = data.get("events", [])
                    segs = []
                    for ev in events:
                        if "segs" in ev:
                            text = "".join(s.get("utf8", "") for s in ev["segs"]).strip()
                            if text and text != "\n":
                                segs.append({
                                    "text": text,
                                    "start": ev.get("tStartMs", 0) / 1000,
                                    "duration": ev.get("dDurationMs", 0) / 1000,
                                })
                    if segs:
                        result["backend"] = "yt-dlp"
                        result["segments"] = segs
                        segments = segs
                        result["language"] = "auto"
                except (json.JSONDecodeError, KeyError):
                    pass
            if sub_file and sub_file.exists():
                try:
                    sub_file.unlink()
                except OSError:
                    pass

    if not result["segments"]:
        return {"error": "No transcript available for this video", **result}

    result["full_text"] = " ".join(s["text"] for s in result["segments"])
    if timestamps:
        result["timestamped_text"] = "\n".join(
            f"{format_timestamp(s['start'])} {s['text']}" for s in result["segments"]
        )
    if result["segments"]:
        last = result["segments"][-1]
        result["duration"] = format_timestamp(last["start"] + last["duration"])

    return result


def fetch_video_metadata(url: str) -> Dict[str, Any]:
    """Fetch comprehensive metadata for a single video."""
    video_id = extract_video_id(url)
    if not video_id:
        return {"error": f"Could not extract video ID from: {url}"}

    yb = YtDlpBackend()
    if not yb.available:
        return {"error": "yt-dlp not available for metadata extraction"}

    meta = yb.dump_json(f"https://youtube.com/watch?v={video_id}")
    if not meta:
        return {"error": "Failed to fetch video metadata"}

    description = meta.get("description", "")
    chapters = extract_chapters_from_description(description)

    return {
        "video_id": video_id,
        "title": meta.get("title", ""),
        "url": f"https://youtube.com/watch?v={video_id}",
        "channel": meta.get("channel", ""),
        "channel_id": meta.get("channel_id", ""),
        "uploader": meta.get("uploader", ""),
        "upload_date": meta.get("upload_date", ""),
        "duration": meta.get("duration", 0),
        "duration_string": meta.get("duration_string", ""),
        "view_count": meta.get("view_count", 0),
        "like_count": meta.get("like_count", 0),
        "comment_count": meta.get("comment_count", 0),
        "description": description,
        "tags": meta.get("tags", []),
        "categories": meta.get("categories", []),
        "thumbnail": meta.get("thumbnail", ""),
        "chapters": chapters,
        "has_subtitles": bool(meta.get("subtitles")),
        "has_auto_captions": bool(meta.get("automatic_captions")),
        "available_subtitles": list(meta.get("subtitles", {}).keys()),
        "available_auto_captions": list(meta.get("automatic_captions", {}).keys())[:10],
        "engagement": {
            "like_view_ratio": round(meta.get("like_count", 0) / max(meta.get("view_count", 1), 1), 4),
            "comment_view_ratio": round(meta.get("comment_count", 0) / max(meta.get("view_count", 1), 1), 4),
        },
    }


def extract_chapters_from_description(description: str) -> List[Dict[str, str]]:
    chapters = []
    pattern = re.compile(r'^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$', re.MULTILINE)
    for match in pattern.finditer(description):
        chapters.append({
            "timestamp": match.group(1),
            "title": match.group(2).strip(),
        })
    return chapters


def fetch_channel(channel_url: str, limit: int = 0) -> Dict[str, Any]:
    """Full channel reconnaissance."""
    handle = extract_channel_handle(channel_url)
    if handle:
        channel_url = f"https://www.youtube.com/@{handle}"
    elif not channel_url.startswith("http"):
        channel_url = f"https://www.youtube.com/{channel_url}"

    yb = YtDlpBackend()
    if not yb.available:
        return {"error": "yt-dlp not available for channel extraction"}

    info = yb.channel_info(channel_url)
    videos = yb.flat_playlist(channel_url, limit)

    enriched = []
    total_views = 0
    total_duration = 0
    for v in videos:
        vid = {
            "video_id": v.get("id", ""),
            "title": v.get("title", ""),
            "url": v.get("url") or v.get("webpage_url") or f"https://youtube.com/watch?v={v.get('id', '')}",
            "duration": v.get("duration", 0),
            "view_count": v.get("view_count") or v.get("approx_duration_ms", 0),
            "upload_date": v.get("upload_date", ""),
            "description": v.get("description", ""),
        }
        total_views += vid["view_count"] or 0
        total_duration += vid["duration"] or 0
        enriched.append(vid)

    return {
        "channel": (info.get("channel") or info.get("uploader", "")) if info else "",
        "channel_id": info.get("channel_id", "") if info else "",
        "description": info.get("description", "") if info else "",
        "subscriber_count": info.get("subscriber_count", 0) if info else 0,
        "total_videos": len(enriched),
        "total_views": total_views,
        "total_duration_seconds": total_duration,
        "total_duration_string": format_timestamp(total_duration),
        "average_views": round(total_views / max(len(enriched), 1)),
        "videos": enriched,
    }


def batch_extract(channel_url: str, limit: int = 20,
                  with_transcripts: bool = False,
                  languages: List[str] = None) -> Dict[str, Any]:
    """Batch extract video metadata (and optionally transcripts)."""
    channel_data = fetch_channel(channel_url, limit)
    if "error" in channel_data:
        return channel_data

    videos = channel_data["videos"][:limit]
    results = []
    errors = []

    for i, v in enumerate(videos):
        vid_id = v["video_id"]
        print(f"  [{i+1}/{len(videos)}] {v['title'][:60]}...", end=" ", flush=True)

        entry = {**v}

        full_meta = fetch_video_metadata(f"https://youtube.com/watch?v={vid_id}")
        if "error" not in full_meta:
            entry.update({
                "like_count": full_meta.get("like_count", 0),
                "comment_count": full_meta.get("comment_count", 0),
                "tags": full_meta.get("tags", []),
                "categories": full_meta.get("categories", []),
                "chapters": full_meta.get("chapters", []),
                "engagement": full_meta.get("engagement", {}),
            })

        if with_transcripts:
            transcript = fetch_transcript(f"https://youtube.com/watch?v={vid_id}", languages)
            if "error" not in transcript:
                entry["transcript"] = transcript
                print("OK", end=" ", flush=True)
            else:
                errors.append({"video_id": vid_id, "error": transcript.get("error", "transcript failed")})
                print("WARN no transcript", end=" ", flush=True)
        else:
            print("OK", end=" ", flush=True)

        results.append(entry)
        if i < len(videos) - 1:
            time.sleep(0.5)

    return {
        "channel": channel_data["channel"],
        "channel_id": channel_data["channel_id"],
        "subscriber_count": channel_data["subscriber_count"],
        "total_extracted": len(results),
        "total_errors": len(errors),
        "videos": results,
        "errors": errors,
    }


def fetch_playlist(playlist_url: str, limit: int = 0) -> Dict[str, Any]:
    """Extract all videos from a playlist."""
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        return {"error": f"Could not extract playlist ID from: {playlist_url}"}

    yb = YtDlpBackend()
    if not yb.available:
        return {"error": "yt-dlp not available for playlist extraction"}

    url = f"https://www.youtube.com/playlist?list={playlist_id}"
    videos = yb.flat_playlist(url, limit)

    return {
        "playlist_id": playlist_id,
        "url": url,
        "total_videos": len(videos),
        "videos": [
            {
                "video_id": v.get("id", ""),
                "title": v.get("title", ""),
                "url": f"https://youtube.com/watch?v={v.get('id', '')}",
                "duration": v.get("duration", 0),
                "view_count": v.get("view_count", 0),
                "upload_date": v.get("upload_date", ""),
            }
            for v in videos
        ],
    }


def channel_analytics(channel_url: str) -> Dict[str, Any]:
    """Comprehensive channel analytics."""
    channel_data = fetch_channel(channel_url)
    if "error" in channel_data:
        return channel_data

    videos = channel_data["videos"]
    if not videos:
        return {"error": "No videos found on channel"}

    # View Distribution
    view_counts = [v["view_count"] for v in videos if v["view_count"]]
    view_counts.sort(reverse=True)
    avg_views = sum(view_counts) / max(len(view_counts), 1)
    median_views = view_counts[len(view_counts) // 2] if view_counts else 0
    max_views = max(view_counts) if view_counts else 0
    min_views = min(view_counts) if view_counts else 0
    p25 = view_counts[len(view_counts) * 3 // 4] if view_counts else 0
    p75 = view_counts[len(view_counts) // 4] if view_counts else 0

    # Duration Distribution
    durations = [v["duration"] for v in videos if v["duration"]]
    avg_duration = sum(durations) / max(len(durations), 1)
    duration_buckets = {"short (<5min)": 0, "medium (5-20min)": 0,
                        "long (20-60min)": 0, "very_long (>60min)": 0}
    for d in durations:
        if d < 300:
            duration_buckets["short (<5min)"] += 1
        elif d < 1200:
            duration_buckets["medium (5-20min)"] += 1
        elif d < 3600:
            duration_buckets["long (20-60min)"] += 1
        else:
            duration_buckets["very_long (>60min)"] += 1

    # Posting Frequency
    dated_videos = [(v["upload_date"], v["title"]) for v in videos if v["upload_date"]]
    dated_videos.sort(key=lambda x: x[0], reverse=True)
    posting_gaps = []
    for i in range(len(dated_videos) - 1):
        try:
            d1 = datetime.strptime(dated_videos[i][0], "%Y%m%d")
            d2 = datetime.strptime(dated_videos[i + 1][0], "%Y%m%d")
            posting_gaps.append((d1 - d2).days)
        except ValueError:
            continue

    avg_gap = sum(posting_gaps) / max(len(posting_gaps), 1) if posting_gaps else 0
    if avg_gap <= 3:
        freq = "daily"
    elif avg_gap <= 7:
        freq = "weekly"
    elif avg_gap <= 14:
        freq = "bi-weekly"
    elif avg_gap <= 30:
        freq = "monthly"
    else:
        freq = "irregular"

    # Title Word Frequency
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to",
                  "for", "of", "and", "or", "but", "not", "with", "this", "that", "how",
                  "what", "why", "when", "where", "who", "which", "i", "you", "we", "they",
                  "it", "my", "your", "our", "their", "can", "will", "do", "does", "did",
                  "have", "has", "had", "be", "been", "from", "by", "as", "no", "so",
                  "if", "than", "just", "about", "more", "all", "me", "let"}
    all_words = []
    for v in videos:
        title_words = re.findall(r'[a-zA-Z]{3,}', v["title"].lower())
        all_words.extend([w for w in title_words if w not in stop_words])
    word_freq = Counter(all_words).most_common(30)

    # Top Videos
    top_by_views = sorted(videos, key=lambda x: x.get("view_count", 0), reverse=True)[:10]

    # Engagement
    engagement_data = []
    for v in videos:
        if v.get("engagement", {}).get("like_view_ratio"):
            engagement_data.append({
                "title": v["title"],
                "like_view_ratio": v["engagement"]["like_view_ratio"],
            })
    avg_engagement = (
        sum(e["like_view_ratio"] for e in engagement_data) / max(len(engagement_data), 1)
        if engagement_data else 0
    )

    return {
        "channel": channel_data["channel"],
        "channel_id": channel_data["channel_id"],
        "subscriber_count": channel_data["subscriber_count"],
        "total_videos_analyzed": len(videos),
        "views": {
            "total": channel_data["total_views"],
            "average": round(avg_views),
            "median": median_views,
            "max": max_views,
            "min": min_views,
            "p25": p25,
            "p75": p75,
        },
        "duration": {
            "average_seconds": round(avg_duration),
            "average_string": format_timestamp(avg_duration),
            "total_string": channel_data["total_duration_string"],
            "distribution": duration_buckets,
        },
        "posting_frequency": {
            "average_days_between": round(avg_gap, 1),
            "category": freq,
            "total_gaps_analyzed": len(posting_gaps),
        },
        "title_themes": [{"word": w, "count": c} for w, c in word_freq],
        "top_videos": [
            {"title": v["title"], "views": v["view_count"], "url": v["url"]}
            for v in top_by_views
        ],
        "engagement": {
            "average_like_view_ratio": round(avg_engagement, 4),
            "videos_with_data": len(engagement_data),
        },
    }


# --- Export Functions ---

def save_json(data: Any, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    print(f"  Saved: {p}")


def save_csv(rows: List[Dict], path: str):
    if not rows:
        print("  No data to save as CSV")
        return
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    flat_rows = []
    for row in rows:
        flat = {}
        for k, v in row.items():
            if isinstance(v, (dict, list)):
                flat[k] = json.dumps(v, ensure_ascii=False)
            else:
                flat[k] = v
        flat_rows.append(flat)
    with open(p, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=flat_rows[0].keys())
        writer.writeheader()
        writer.writerows(flat_rows)
    print(f"  Saved: {p}")


def save_markdown(data: Dict, path: str):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# YouTube Analytics Report\n"]
    lines.append(f"**Channel**: {data.get('channel', 'Unknown')}")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Videos Analyzed**: {data.get('total_videos_analyzed', 0)}\n")

    subs = data.get("subscriber_count", 0)
    if subs:
        lines.append(f"**Subscribers**: {subs:,}\n")

    views = data.get("views", {})
    if views:
        lines.append("## View Statistics\n")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        for k, label in [("total","Total"),("average","Average"),("median","Median"),
                          ("max","Max"),("min","Min"),("p25","25th %ile"),("p75","75th %ile")]:
            lines.append(f"| {label} Views | {views.get(k, 0):,} |")
        lines.append("")

    dur = data.get("duration", {})
    if dur:
        lines.append("## Duration Analysis\n")
        lines.append(f"- **Average**: {dur.get('average_string', 'N/A')}")
        lines.append(f"- **Total**: {dur.get('total_string', 'N/A')}\n")
        dist = dur.get("distribution", {})
        if dist:
            lines.append("| Bucket | Count |")
            lines.append("|--------|-------|")
            for bucket, count in dist.items():
                lines.append(f"| {bucket} | {count} |")
            lines.append("")

    freq = data.get("posting_frequency", {})
    if freq:
        lines.append("## Posting Frequency\n")
        lines.append(f"- **Average Gap**: {freq.get('average_days_between', 0)} days")
        lines.append(f"- **Category**: {freq.get('category', 'N/A')}\n")

    themes = data.get("title_themes", [])
    if themes:
        lines.append("## Top Title Themes\n")
        lines.append("| Word | Count |")
        lines.append("|------|-------|")
        for t in themes[:15]:
            lines.append(f"| {t['word']} | {t['count']} |")
        lines.append("")

    top_vids = data.get("top_videos", [])
    if top_vids:
        lines.append("## Top 10 Videos\n")
        lines.append("| # | Title | Views |")
        lines.append("|---|-------|-------|")
        for i, v in enumerate(top_vids, 1):
            title = v["title"][:50] + ("..." if len(v["title"]) > 50 else "")
            lines.append(f"| {i} | [{title}]({v['url']}) | {v.get('views', 0):,} |")
        lines.append("")

    eng = data.get("engagement", {})
    if eng and eng.get("average_like_view_ratio"):
        lines.append("## Engagement\n")
        lines.append(f"- **Avg Like/View**: {eng['average_like_view_ratio']:.2%}")
        lines.append(f"- **Videos with data**: {eng.get('videos_with_data', 0)}\n")

    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  Saved: {p}")


# --- CLI Commands ---

def cmd_install(args):
    print("Checking and installing dependencies...")
    if ensure_dependencies():
        print("All dependencies installed!")
    else:
        print("Some dependencies failed to install.")
        sys.exit(1)


def cmd_transcript(args):
    print(f"Fetching transcript: {args.url}")
    languages = [l.strip() for l in args.lang.split(",")] if args.lang else None
    result = fetch_transcript(args.url, languages, timestamps=args.timestamps)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"  Backend: {result['backend']}")
    print(f"  Segments: {len(result['segments'])}")
    print(f"  Duration: {result['duration']}")

    if args.out:
        save_json(result, args.out)
    else:
        if args.timestamps and result.get("timestamped_text"):
            print(f"\n{'='*60}")
            print(result["timestamped_text"])
        else:
            print(f"\n{'='*60}")
            text = result["full_text"]
            print(text[:2000])
            if len(text) > 2000:
                print(f"\n... ({len(text) - 2000} more characters)")


def cmd_video(args):
    print(f"Fetching video metadata: {args.url}")
    result = fetch_video_metadata(args.url)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"  Title: {result['title']}")
    print(f"  Channel: {result['channel']}")
    print(f"  Views: {result['view_count']:,}")
    lc = result.get('like_count')
    print(f"  Likes: {lc:,}" if lc else "  Likes: N/A")
    print(f"  Duration: {result.get('duration_string', 'N/A')}")
    print(f"  Uploaded: {result['upload_date']}")
    print(f"  Tags: {len(result.get('tags', []))} tags")
    print(f"  Chapters: {len(result.get('chapters', []))}")

    if result.get("chapters"):
        print("\n  Chapters:")
        for ch in result["chapters"]:
            print(f"    {ch['timestamp']} -- {ch['title']}")

    if args.out:
        save_json(result, args.out)


def cmd_channel(args):
    print(f"Fetching channel: {args.url}")
    result = fetch_channel(args.url, limit=args.limit or 0)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"  Channel: {result['channel']}")
    sc = result.get('subscriber_count', 0)
    print(f"  Subscribers: {sc:,}" if sc else "  Subscribers: N/A")
    print(f"  Videos: {result['total_videos']}")
    print(f"  Total Views: {result['total_views']:,}")
    print(f"  Total Duration: {result['total_duration_string']}")
    print(f"  Avg Views/Video: {result['average_views']:,}")

    out_dir = args.out or f"yt-channel-{result['channel'].replace(' ', '_').lower()}"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    save_json(result, f"{out_dir}/channel_data.json")
    if result["videos"]:
        save_csv(result["videos"], f"{out_dir}/videos.csv")
    print(f"\n  Output: {out_dir}")


def cmd_batch(args):
    print(f"Batch extraction: {args.url} (limit: {args.limit})")
    result = batch_extract(
        args.url,
        limit=args.limit,
        with_transcripts=args.transcripts,
        languages=[l.strip() for l in args.lang.split(",")] if args.lang else None,
    )

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"\n  Extracted: {result['total_extracted']} videos")
    if result.get("total_errors"):
        print(f"  Errors: {result['total_errors']}")

    out_dir = args.out or f"yt-batch-{result.get('channel', 'unknown').replace(' ', '_').lower()}"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    save_json(result, f"{out_dir}/batch_data.json")

    if args.transcripts:
        for v in result["videos"]:
            if v.get("transcript") and "error" not in v["transcript"]:
                save_json(v["transcript"], f"{out_dir}/{v['video_id']}_transcript.json")

    if result["videos"]:
        save_csv(result["videos"], f"{out_dir}/videos.csv")
    print(f"\n  Output: {out_dir}")


def cmd_playlist(args):
    print(f"Fetching playlist: {args.url}")
    result = fetch_playlist(args.url, limit=args.limit or 0)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"  Playlist ID: {result['playlist_id']}")
    print(f"  Videos: {result['total_videos']}")

    out_dir = args.out or f"yt-playlist-{result['playlist_id']}"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    save_json(result, f"{out_dir}/playlist_data.json")
    if result["videos"]:
        save_csv(result["videos"], f"{out_dir}/videos.csv")
    print(f"\n  Output: {out_dir}")


def cmd_analytics(args):
    print(f"Generating analytics: {args.url}")
    result = channel_analytics(args.url)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"  Analyzed {result.get('total_videos_analyzed', 0)} videos")
    views = result.get("views", {})
    if views:
        print(f"  Avg Views: {views.get('average', 0):,}")
        print(f"  Median Views: {views.get('median', 0):,}")
    freq = result.get("posting_frequency", {})
    if freq:
        print(f"  Posting: {freq.get('category', 'N/A')} (~{freq.get('average_days_between', 0)} days)")

    out_path = args.out or f"yt-analytics-{result.get('channel', 'unknown').replace(' ', '_').lower()}.md"
    save_markdown(result, out_path)
    save_json(result, out_path.replace(".md", ".json"))


# --- Main CLI ---

def main():
    parser = argparse.ArgumentParser(
        prog="yt_analyzer",
        description="yt_analyzer v2.0 — Bulletproof YouTube Analysis Toolkit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              python yt_analyzer.py transcript "https://youtube.com/watch?v=abc123" --timestamps
              python yt_analyzer.py video "https://youtu.be/abc123def45"
              python yt_analyzer.py channel "@MrBeast" --limit 50 --out ./beast_data/
              python yt_analyzer.py batch "@TechLinked" --limit 20 --transcripts --lang en
              python yt_analyzer.py playlist "https://youtube.com/playlist?list=PLxxxxxx"
              python yt_analyzer.py analytics "@Veritasium" --out analytics.md
              python yt_analyzer.py install
        """),
    )
    parser.add_argument("--version", action="version", version=f"yt_analyzer {__version__}")

    sub = parser.add_subparsers(dest="command", help="Command to run")

    sub.add_parser("install", help="Install required dependencies")

    p_trans = sub.add_parser("transcript", help="Fetch video transcript")
    p_trans.add_argument("url", help="YouTube URL or video ID")
    p_trans.add_argument("--lang", "-l", default=None, help="Comma-separated languages (e.g. en,tr)")
    p_trans.add_argument("--timestamps", "-t", action="store_true", help="Include timestamps")
    p_trans.add_argument("--out", "-o", default=None, help="Output JSON file path")

    p_vid = sub.add_parser("video", help="Fetch detailed video metadata")
    p_vid.add_argument("url", help="YouTube URL or video ID")
    p_vid.add_argument("--out", "-o", default=None, help="Output JSON file path")

    p_ch = sub.add_parser("channel", help="Full channel reconnaissance")
    p_ch.add_argument("url", help="Channel URL (e.g. @handle)")
    p_ch.add_argument("--limit", "-n", type=int, default=0, help="Limit videos (0=all)")
    p_ch.add_argument("--out", "-o", default=None, help="Output directory")

    p_batch = sub.add_parser("batch", help="Batch extract from channel")
    p_batch.add_argument("url", help="Channel URL")
    p_batch.add_argument("--limit", "-n", type=int, default=20, help="Videos (default: 20)")
    p_batch.add_argument("--transcripts", action="store_true", help="Also fetch transcripts")
    p_batch.add_argument("--lang", "-l", default=None, help="Transcript languages")
    p_batch.add_argument("--out", "-o", default=None, help="Output directory")

    p_pl = sub.add_parser("playlist", help="Extract playlist")
    p_pl.add_argument("url", help="Playlist URL")
    p_pl.add_argument("--limit", "-n", type=int, default=0, help="Limit videos")
    p_pl.add_argument("--out", "-o", default=None, help="Output directory")

    p_an = sub.add_parser("analytics", help="Channel analytics report")
    p_an.add_argument("url", help="Channel URL")
    p_an.add_argument("--out", "-o", default=None, help="Output Markdown file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command != "install":
        if not ensure_dependencies():
            print("Missing deps. Run: python yt_analyzer.py install")
            sys.exit(1)

    commands = {
        "install": cmd_install,
        "transcript": cmd_transcript,
        "video": cmd_video,
        "channel": cmd_channel,
        "batch": cmd_batch,
        "playlist": cmd_playlist,
        "analytics": cmd_analytics,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
