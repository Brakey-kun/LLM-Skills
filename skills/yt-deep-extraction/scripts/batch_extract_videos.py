#!/usr/bin/env python3
"""
Batch video extraction script for yt-deep-extraction skill.
Run via execute_code to bypass Windows/MSYS terminal fork issues.

Usage (inside execute_code):
    import subprocess
    result = subprocess.run(["python", "scripts/batch_extract_videos.py", 
                            "--output-dir", "C:/path/to/output",
                            "--channel-url", "https://www.youtube.com/@handle",
                            "--start-index", "0",
                            "--batch-size", "20"],
                           capture_output=True, text=True, timeout=300)
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def run_yt_dlp(cmd, timeout=120):
    """Run yt-dlp command and return parsed JSON or None on failure."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.stdout:
            return json.loads(result.stdout)
        return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
        print(f"  ✗ Error: {e}", file=sys.stderr)
        return None


def extract_video(video_id, output_dir):
    """Extract metadata, description, and transcript for a single video."""
    raw_dir = Path(output_dir) / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    meta_file = raw_dir / f"{video_id}.meta.json"
    desc_file = raw_dir / f"{video_id}.description.txt"
    transcript_file = raw_dir / f"{video_id}.en.json3"
    
    # Skip if already fully extracted
    if meta_file.exists() and desc_file.exists() and transcript_file.exists():
        print(f"  ✓ {video_id} already complete")
        return True
    
    # 1. Full metadata + description + auto-subs
    if not meta_file.exists() or not desc_file.exists():
        meta = run_yt_dlp([
            "yt-dlp", "--dump-json", "--write-auto-sub", "--skip-download",
            "--sub-format", "json3", "--write-sub",
            "--output", f"{raw_dir}/%(id)s.%(ext)s",
            f"https://youtube.com/watch?v={video_id}"
        ])
        
        if meta:
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            with open(desc_file, 'w', encoding='utf-8') as f:
                f.write(meta.get('description', ''))
            print(f"  ✓ Metadata + description saved")
        else:
            print(f"  ✗ Metadata failed")
            return False
    
    # 2. Transcript (if missing)
    if not transcript_file.exists():
        run_yt_dlp([
            "yt-dlp", "--write-auto-sub", "--skip-download",
            "--sub-format", "json3", "--sub-lang", "en",
            "--output", f"{raw_dir}/%(id)s.%(ext)s",
            f"https://youtube.com/watch?v={video_id}"
        ], timeout=60)
        if transcript_file.exists():
            print(f"  ✓ Transcript saved")
        else:
            print(f"  ⚠ Transcript not available (likely Shorts without captions)")
    
    return True


def main():
    parser = argparse.ArgumentParser(description="Batch extract YouTube videos for yt-deep-extraction")
    parser.add_argument("--output-dir", required=True, help="Output directory (e.g. C:/Users/amine/yt-extraction-marktilbury)")
    parser.add_argument("--channel-url", required=True, help="Channel URL (e.g. https://www.youtube.com/@marktilbury)")
    parser.add_argument("--start-index", type=int, default=0, help="Start from this video index")
    parser.add_argument("--batch-size", type=int, default=20, help="Number of videos to process")
    parser.add_argument("--reverse", action="store_true", help="Process oldest first (default: newest first)")
    args = parser.parse_args()
    
    output_dir = Path(args.output_dir)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    # Get full channel video list
    channel_list_file = raw_dir / "_channel.videos.full.jsonl"
    
    if not channel_list_file.exists():
        print("Fetching complete channel video list...")
        # Use channel ROOT URL (not /videos) to get ALL videos including Shorts
        result = subprocess.run([
            "yt-dlp", "--flat-playlist", "--dump-json", args.channel_url
        ], capture_output=True, text=True, timeout=180)
        
        if result.stdout:
            with open(channel_list_file, 'w', encoding='utf-8') as f:
                f.write(result.stdout)
            print(f"Saved {len(result.stdout.strip().split(chr(10)))} videos to {channel_list_file}")
        else:
            print("Failed to fetch channel list", file=sys.stderr)
            return 1
    
    # Load all videos
    all_videos = []
    with open(channel_list_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    all_videos.append(data)
                except json.JSONDecodeError:
                    pass
    
    if args.reverse:
        all_videos = list(reversed(all_videos))
    
    batch = all_videos[args.start_index : args.start_index + args.batch_size]
    print(f"Processing {len(batch)} videos (index {args.start_index}-{args.start_index + len(batch) - 1})")
    
    success = 0
    for i, v in enumerate(batch):
        video_id = v.get('id')
        title = v.get('title', 'Unknown')[:60]
        print(f"\n[{i+1}/{len(batch)}] {title}... (ID: {video_id})")
        if extract_video(video_id, args.output_dir):
            success += 1
    
    print(f"\n✓ Batch complete: {success}/{len(batch)} videos extracted")
    print(f"Total videos in channel: {len(all_videos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())