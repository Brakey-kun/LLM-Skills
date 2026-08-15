#!/usr/bin/env python3
"""
Simple YouTube Channel Video Extractor using ytInitialData
Works with saved HTML or live browser - extracts all video metadata from ytInitialData JSON
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

def extract_videos_from_ytinitialdata(html_content: str) -> List[Dict[str, Any]]:
    """Extract video metadata from ytInitialData in HTML."""
    # Find ytInitialData JSON
    pattern = r'var ytInitialData = ({.*?});'
    match = re.search(pattern, html_content, re.DOTALL)
    
    if not match:
        # Try alternative pattern
        pattern = r'window\["ytInitialData"\] = ({.*?});'
        match = re.search(pattern, html_content, re.DOTALL)
        
    if not match:
        # Try finding in script tags
        script_pattern = r'<script[^>]*>.*?ytInitialData\s*=\s*({.*?});.*?</script>'
        match = re.search(script_pattern, html_content, re.DOTALL)
        
    if not match:
        raise ValueError("ytInitialData not found in HTML")
        
    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse ytInitialData JSON: {e}")
        
    return parse_videos_from_data(data)

def parse_videos_from_data(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Parse video entries from ytInitialData structure."""
    videos = []
    
    try:
        tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        
        videos_tab = None
        for tab in tabs:
            if tab.get('tabRenderer', {}).get('title') == 'Videos':
                videos_tab = tab
                break
                
        if not videos_tab:
            return videos
            
        # Handle both direct content and continuation-based loading
        contents = videos_tab.get('tabRenderer', {}).get('content', {})
        
        def extract_from_rich_grid(rich_grid: Dict[str, Any]):
            items = rich_grid.get('contents', [])
            for item in items:
                if not item.get('richItemRenderer'):
                    continue
                content = item['richItemRenderer'].get('content', {})
                lockup = content.get('lockupViewModel', {})
                if not lockup:
                    continue
                    
                video_id = lockup.get('contentId', '')
                title_obj = lockup.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {})
                title = title_obj.get('content', '') if isinstance(title_obj, dict) else str(title_obj)
                
                # Duration
                duration = ''
                overlays = lockup.get('contentImage', {}).get('thumbnailViewModel', {}).get('overlays', [])
                for overlay in overlays:
                    badge = overlay.get('thumbnailBottomOverlayViewModel', {}).get('badges', [{}])[0]
                    badge_text = badge.get('thumbnailBadgeViewModel', {}).get('text', '')
                    if badge_text and ':' in badge_text:
                        duration = badge_text
                        break
                
                # Metadata rows (views, upload time)
                rows = lockup.get('metadata', {}).get('lockupMetadataViewModel', {}).get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
                views = ''
                uploaded = ''
                for row in rows:
                    for part in row.get('metadataParts', []):
                        txt = part.get('text', {}).get('content', '')
                        if any(kw in txt.lower() for kw in ['view', 'k', 'm', 'k vues', 'm vues']):
                            views = txt
                        elif any(kw in txt for kw in ['il y a', 'ago', 'jour', 'sem', 'mois', 'an', 'week', 'month', 'year', 'hour', 'minute']):
                            uploaded = txt
                
                if video_id and title:
                    videos.append({
                        'videoId': video_id,
                        'title': title,
                        'duration': duration,
                        'views': views,
                        'uploaded': uploaded,
                        'link': f'https://www.youtube.com/watch?v={video_id}'
                    })
                    
        # Extract from main rich grid
        if 'richGridRenderer' in contents:
            extract_from_rich_grid(contents['richGridRenderer'])
            
    except Exception as e:
        print(f"Error parsing data: {e}", file=sys.stderr)
        
    return videos

def save_videos(videos: List[Dict[str, Any]], output_dir: Path, prefix: str = "quantguild"):
    """Save videos to JSON and CSV."""
    import csv
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir.mkdir(exist_ok=True)
    
    # JSON
    json_path = output_dir / f"{prefix}_videos_{timestamp}.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({
            'channel': '@QuantGuild',
            'extraction_date': datetime.now().isoformat(),
            'total_videos': len(videos),
            'videos': videos
        }, f, ensure_ascii=False, indent=2)
    
    # CSV
    csv_path = output_dir / f"{prefix}_videos_{timestamp}.csv"
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['videoId', 'title', 'duration', 'views', 'uploaded', 'link'])
        writer.writeheader()
        for v in videos:
            writer.writerow(v)
            
    print(f"Saved {len(videos)} videos to {json_path} and {csv_path}")
    return json_path, csv_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_ytinitialdata.py <html_file_or_directory>")
        print("  If directory provided, processes all .html files")
        sys.exit(1)
        
    input_path = Path(sys.argv[1])
    output_dir = Path("quantguild_extraction")
    
    all_videos = []
    seen_ids = set()
    
    if input_path.is_file() and input_path.suffix == '.html':
        files = [input_path]
    elif input_path.is_dir():
        files = list(input_path.glob("*.html"))
    else:
        print(f"Error: {input_path} not found or not HTML file/directory")
        sys.exit(1)
        
    for html_file in files:
        print(f"Processing {html_file}...")
        try:
            html = html_file.read_text(encoding='utf-8')
            videos = extract_videos_from_ytinitialdata(html)
            for v in videos:
                if v['videoId'] not in seen_ids:
                    seen_ids.add(v['videoId'])
                    all_videos.append(v)
            print(f"  Extracted {len(videos)} videos ({len(all_videos)} unique total)")
        except Exception as e:
            print(f"  Error: {e}")
            
    if all_videos:
        save_videos(all_videos, output_dir)
    else:
        print("No videos extracted!")

if __name__ == '__main__':
    main()