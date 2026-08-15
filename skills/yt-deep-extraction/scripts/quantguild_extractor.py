#!/usr/bin/env python3
"""
Quant Guild YouTube Channel Video Extractor
Automatically opens the channel, scrolls to bottom, and extracts all video IDs and metadata.
Requires: pip install playwright && playwright install chromium
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Page, Browser, BrowserContext

CHANNEL_URL = "https://www.youtube.com/@QuantGuild/videos"
OUTPUT_DIR = Path("quantguild_extraction")
OUTPUT_DIR.mkdir(exist_ok=True)

class QuantGuildExtractor:
    def __init__(self, headless: bool = False, scroll_pause: float = 2.0):
        self.headless = headless
        self.scroll_pause = scroll_pause
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.videos: List[Dict[str, Any]] = []
        self.seen_video_ids = set()
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.headless,
            args=['--disable-blink-features=AutomationControlled']
        )
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await self.context.new_page()
        # Block unnecessary resources for speed
        await self.page.route("**/*.{png,jpg,jpeg,gif,webp,woff,woff2}", lambda route: route.abort())
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.browser:
            await self.browser.close()
        await self.playwright.stop()
        
    async def navigate_to_channel(self):
        """Navigate to the Quant Guild videos page."""
        print(f"Navigating to {CHANNEL_URL}...")
        await self.page.goto(CHANNEL_URL, wait_until='networkidle', timeout=60000)
        # Wait for initial content
        await self.page.wait_for_selector('ytd-rich-item-renderer, ytd-grid-video-renderer', timeout=30000)
        print("Initial page loaded.")
        
    async def scroll_to_bottom(self, max_scrolls: int = 500) -> int:
        """Scroll to bottom of page to load all videos."""
        print("Scrolling to load all videos...")
        last_count = 0
        no_change_count = 0
        
        for scroll_num in range(max_scrolls):
            # Extract current videos
            current_videos = await self.extract_videos_from_dom()
            current_count = len(current_videos)
            
            if current_count == last_count:
                no_change_count += 1
                if no_change_count >= 5:
                    print(f"No new videos after {no_change_count} scrolls. Stopping.")
                    break
            else:
                no_change_count = 0
                last_count = current_count
                print(f"  Scroll {scroll_num + 1}: {current_count} videos loaded")
            
            # Scroll down
            await self.page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
            await asyncio.sleep(self.scroll_pause)
            
        final_videos = await self.extract_videos_from_dom()
        print(f"Final count: {len(final_videos)} videos")
        return len(final_videos)
        
    async def extract_videos_from_dom(self) -> List[Dict[str, Any]]:
        """Extract video metadata from current DOM."""
        videos = await self.page.evaluate("""
            () => {
                const items = document.querySelectorAll('ytd-rich-item-renderer, ytd-grid-video-renderer');
                const results = [];
                items.forEach(item => {
                    try {
                        const titleEl = item.querySelector('#video-title, #video-title-link, h3 a, a#video-title');
                        const title = titleEl ? titleEl.textContent.trim() : '';
                        const link = titleEl ? titleEl.href : '';
                        
                        // Extract video ID from various URL formats
                        let videoId = '';
                        if (link) {
                            const match = link.match(/[?&]v=([^&]+)/) || link.match(/\\/watch\\?v=([^&]+)/) || link.match(/\\/shorts\\/([^?&]+)/);
                            if (match) videoId = match[1];
                        }
                        
                        // Duration
                        const durationEl = item.querySelector('.ytd-thumbnail-overlay-time-status-renderer, .badge-shape-wiz__text');
                        const duration = durationEl ? durationEl.textContent.trim() : '';
                        
                        // Views and date from metadata line
                        const metaLine = item.querySelector('#metadata-line, .ytd-video-meta-block');
                        let views = '', date = '';
                        if (metaLine) {
                            const spans = metaLine.querySelectorAll('span');
                            if (spans.length > 0) views = spans[0].textContent.trim();
                            if (spans.length > 1) date = spans[1].textContent.trim();
                        }
                        
                        // Channel name (for verification)
                        const channelEl = item.querySelector('#channel-name, .ytd-channel-name a');
                        const channel = channelEl ? channelEl.textContent.trim() : '';
                        
                        if (title && videoId) {
                            results.push({title, videoId, link, duration, views, date, channel});
                        }
                    } catch (e) {}
                });
                return results;
            }
        """)
        
        # Deduplicate
        for v in videos:
            if v['videoId'] not in self.seen_video_ids:
                self.seen_video_ids.add(v['videoId'])
                self.videos.append(v)
                
        return self.videos
        
    async def extract_from_ytinitialdata(self) -> List[Dict[str, Any]]:
        """Extract from ytInitialData JSON (more complete data)."""
        data = await self.page.evaluate("() => window.ytInitialData")
        if not data:
            return []
            
        try:
            tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
            videos_tab = None
            for tab in tabs:
                if tab.get('tabRenderer', {}).get('title') == 'Videos':
                    videos_tab = tab
                    break
                    
            if not videos_tab:
                return []
                
            rich_grid = videos_tab.get('tabRenderer', {}).get('content', {}).get('richGridRenderer', {})
            contents = rich_grid.get('contents', [])
            
            for item in contents:
                if not item.get('richItemRenderer'):
                    continue
                content = item['richItemRenderer'].get('content', {})
                lockup = content.get('lockupViewModel', {})
                if not lockup:
                    continue
                    
                video_id = lockup.get('contentId', '')
                title = lockup.get('metadata', {}).get('lockupMetadataViewModel', {}).get('title', {}).get('content', '')
                
                # Duration
                duration = ''
                overlays = lockup.get('contentImage', {}).get('thumbnailViewModel', {}).get('overlays', [])
                for overlay in overlays:
                    badge = overlay.get('thumbnailBottomOverlayViewModel', {}).get('badges', [{}])[0]
                    if badge.get('thumbnailBadgeViewModel', {}).get('text'):
                        duration = badge['thumbnailBadgeViewModel']['text']
                        break
                
                # Views and upload time
                rows = lockup.get('metadata', {}).get('lockupMetadataViewModel', {}).get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
                views = ''
                uploaded = ''
                for row in rows:
                    for part in row.get('metadataParts', []):
                        txt = part.get('text', {}).get('content', '')
                        if 'view' in txt.lower() or 'k' in txt.lower() or 'm' in txt.lower():
                            views = txt
                        elif any(x in txt for x in ['il y a', 'ago', 'jour', 'sem', 'mois', 'week', 'month', 'year']):
                            uploaded = txt
                
                if video_id and title and video_id not in self.seen_video_ids:
                    self.seen_video_ids.add(video_id)
                    self.videos.append({
                        'videoId': video_id,
                        'title': title,
                        'duration': duration,
                        'views': views,
                        'uploaded': uploaded,
                        'link': f'https://www.youtube.com/watch?v={video_id}'
                    })
                    
        except Exception as e:
            print(f"Error parsing ytInitialData: {e}")
            
        return self.videos
        
    async def save_results(self):
        """Save extracted data to JSON and CSV."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Sort by upload date (newest first) - best effort
        self.videos.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # JSON output
        json_path = OUTPUT_DIR / f"quantguild_videos_{timestamp}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'channel': '@QuantGuild',
                'channel_name': 'Roman Paolucci',
                'extraction_date': datetime.now().isoformat(),
                'total_videos': len(self.videos),
                'videos': self.videos
            }, f, ensure_ascii=False, indent=2)
            
        # CSV output
        csv_path = OUTPUT_DIR / f"quantguild_videos_{timestamp}.csv"
        import csv
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['videoId', 'title', 'duration', 'views', 'date', 'link'])
            writer.writeheader()
            for v in self.videos:
                writer.writerow({
                    'videoId': v.get('videoId', ''),
                    'title': v.get('title', ''),
                    'duration': v.get('duration', ''),
                    'views': v.get('views', '') or v.get('uploaded', ''),
                    'date': v.get('date', '') or v.get('uploaded', ''),
                    'link': v.get('link', f"https://www.youtube.com/watch?v={v.get('videoId', '')}")
                })
                
        print(f"Saved {len(self.videos)} videos to:")
        print(f"  JSON: {json_path}")
        print(f"  CSV:  {csv_path}")
        
        return json_path, csv_path


async def main():
    """Main extraction routine."""
    import argparse
    parser = argparse.ArgumentParser(description='Extract Quant Guild YouTube videos')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--scroll-pause', type=float, default=2.0, help='Pause between scrolls (seconds)')
    parser.add_argument('--max-scrolls', type=int, default=500, help='Maximum scroll attempts')
    args = parser.parse_args()
    
    print("=" * 60)
    print("Quant Guild YouTube Channel Extractor")
    print("=" * 60)
    
    async with QuantGuildExtractor(headless=args.headless, scroll_pause=args.scroll_pause) as extractor:
        await extractor.navigate_to_channel()
        
        # First extract from ytInitialData (immediate data)
        await extractor.extract_from_ytinitialdata()
        print(f"Initial ytInitialData extraction: {len(extractor.videos)} videos")
        
        # Scroll to load more
        await extractor.scroll_to_bottom(max_scrolls=args.max_scrolls)
        
        # Final extraction from DOM (catches any lazy-loaded)
        await extractor.extract_videos_from_dom()
        
        # Save results
        await extractor.save_results()
        
        print(f"\n✅ Extraction complete: {len(extractor.videos)} unique videos")
        return extractor.videos


if __name__ == '__main__':
    asyncio.run(main())