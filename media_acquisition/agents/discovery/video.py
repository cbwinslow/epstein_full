"""
Video Discovery Agent
Discovers Epstein-related video content from YouTube and Internet Archive.
"""

import asyncio
import json
import logging
import re
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests

# Import base classes
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.base import (
    DiscoveryAgent, AgentConfig, TaskResult,
    VideoMetadata, MediaURL
)

logger = logging.getLogger(__name__)


class YouTubeSearcher:
    """Search YouTube for videos (web scraping approach - no API key needed)."""
    
    BASE_URL = "https://www.youtube.com/results"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search(self,
              query: str,
              published_after: Optional[datetime] = None,
              published_before: Optional[datetime] = None,
              max_results: int = 50) -> List[VideoMetadata]:
        """
        Search YouTube videos.
        
        Uses web scraping if no API key, YouTube Data API if key provided.
        
        Args:
            query: Search query
            published_after: Filter videos after this date
            published_before: Filter videos before this date  
            max_results: Maximum results to return
            
        Returns:
            List of VideoMetadata objects
        """
        if self.api_key:
            return self._search_api(query, published_after, published_before, max_results)
        else:
            return self._search_scrape(query, max_results)
    
    def _search_api(self,
                   query: str,
                   published_after: Optional[datetime],
                   published_before: Optional[datetime],
                   max_results: int) -> List[VideoMetadata]:
        """Search using YouTube Data API (requires API key)."""
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', developerKey=self.api_key)
        
        # Build search request
        search_params = {
            'q': query,
            'part': 'id,snippet',
            'type': 'video',
            'maxResults': min(max_results, 50),  # API limit
            'order': 'relevance'
        }
        
        # Add date filters if provided (RFC 3339 format)
        if published_after:
            search_params['publishedAfter'] = published_after.strftime('%Y-%m-%dT%H:%M:%SZ')
        if published_before:
            search_params['publishedBefore'] = published_before.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        videos = []
        
        try:
            # Execute search
            search_response = youtube.search().list(**search_params).execute()
            
            # Get video IDs for detailed info
            video_ids = [item['id']['videoId'] for item in search_response.get('items', [])]
            
            if video_ids:
                # Get video details (duration, view count, etc.)
                videos_response = youtube.videos().list(
                    part='contentDetails,statistics,snippet',
                    id=','.join(video_ids)
                ).execute()
                
                for item in videos_response.get('items', []):
                    snippet = item.get('snippet', {})
                    content = item.get('contentDetails', {})
                    stats = item.get('statistics', {})
                    
                    # Parse duration (PT4M13S format)
                    duration_str = content.get('duration', 'PT0S')
                    duration_seconds = self._parse_duration(duration_str)
                    
                    # Parse date
                    published_at = snippet.get('publishedAt', '')
                    try:
                        upload_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    except:
                        upload_date = None
                    
                    videos.append(VideoMetadata(
                        video_id=item['id'],
                        url=f"https://youtube.com/watch?v={item['id']}",
                        title=snippet.get('title'),
                        description=snippet.get('description'),
                        platform='youtube',
                        upload_date=upload_date,
                        duration_seconds=duration_seconds,
                        view_count=int(stats.get('viewCount', 0)),
                        transcript_available=None,  # Will check separately
                        discovery_method='youtube_api',
                        priority=1
                    ))
                    
        except Exception as e:
            logger.error(f"YouTube API search failed: {e}")
            
        return videos
    
    def _search_scrape(self, query: str, max_results: int) -> List[VideoMetadata]:
        """Search using web scraping (no API key needed)."""
        # This is a simplified version - in production would need more robust parsing
        # Could use youtube-search-python library
        
        try:
            from youtubesearchpython import VideosSearch
            
            search = VideosSearch(query, limit=max_results)
            results = search.result()
            
            videos = []
            for item in results.get('result', []):
                try:
                    # Parse duration (e.g., "4:13" or "1:23:45")
                    duration_str = item.get('duration', '0:00')
                    duration_seconds = self._parse_duration_simple(duration_str)
                    
                    # Parse view count (e.g., "1.2M views" or "45K views")
                    view_str = item.get('viewCount', {}).get('text', '0 views')
                    view_count = self._parse_view_count(view_str)
                    
                    # Parse date
                    published_time = item.get('publishedTime', '')
                    upload_date = self._parse_relative_date(published_time)
                    
                    videos.append(VideoMetadata(
                        video_id=item.get('id'),
                        url=item.get('link'),
                        title=item.get('title'),
                        description=item.get('descriptionSnippet', [{}])[0].get('text', '') if item.get('descriptionSnippet') else '',
                        platform='youtube',
                        upload_date=upload_date,
                        duration_seconds=duration_seconds,
                        view_count=view_count,
                        transcript_available=None,
                        discovery_method='youtube_scrape',
                        priority=1,
                        metadata={
                            'channel': item.get('channel', {}).get('name'),
                            'thumbnail': item.get('thumbnails', [{}])[0].get('url')
                        }
                    ))
                    
                except Exception as e:
                    logger.warning(f"Failed to parse video item: {e}")
                    
            return videos
            
        except ImportError:
            logger.warning("youtubesearchpython not installed, using fallback")
            return []
        except Exception as e:
            logger.error(f"YouTube scraping failed: {e}")
            return []
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration (PT4M13S) to seconds."""
        import re
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        return hours * 3600 + minutes * 60 + seconds
    
    def _parse_duration_simple(self, duration_str: str) -> int:
        """Parse simple duration (4:13 or 1:23:45) to seconds."""
        parts = duration_str.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    
    def _parse_view_count(self, view_str: str) -> int:
        """Parse view count string to number."""
        view_str = view_str.lower().replace(' views', '').replace(',', '')
        multiplier = 1
        if 'k' in view_str:
            multiplier = 1000
            view_str = view_str.replace('k', '')
        elif 'm' in view_str:
            multiplier = 1000000
            view_str = view_str.replace('m', '')
        try:
            return int(float(view_str) * multiplier)
        except:
            return 0
    
    def _parse_relative_date(self, relative_str: str) -> Optional[datetime]:
        """Parse relative date (e.g., '2 years ago') to datetime."""
        # Simplified - would need more sophisticated parsing
        now = datetime.now()
        
        if 'year' in relative_str:
            years = int(relative_str.split()[0])
            return now.replace(year=now.year - years)
        elif 'month' in relative_str:
            months = int(relative_str.split()[0])
            # Approximate
            year = now.year - (months // 12)
            month = now.month - (months % 12)
            if month <= 0:
                year -= 1
                month += 12
            return now.replace(year=year, month=month)
        elif 'day' in relative_str:
            days = int(relative_str.split()[0])
            return now - timedelta(days=days)
        
        return None
    
    def check_transcript_availability(self, video_id: str) -> Dict[str, Any]:
        """
        Check if video has transcripts available.
        
        Returns dict with:
        - available: bool
        - is_auto_generated: bool
        - language: str
        - source: str (api, auto, manual)
        """
        # Use yt-dlp to check for captions
        import subprocess
        
        url = f"https://youtube.com/watch?v={video_id}"
        
        try:
            result = subprocess.run(
                ['yt-dlp', '--list-subs', url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            
            # Parse output
            has_manual = 'Available subtitles' in output and 'en' in output
            has_auto = 'Available automatic captions' in output and 'en' in output
            
            if has_manual:
                return {
                    'available': True,
                    'is_auto_generated': False,
                    'language': 'en',
                    'source': 'manual'
                }
            elif has_auto:
                return {
                    'available': True,
                    'is_auto_generated': True,
                    'language': 'en',
                    'source': 'auto'
                }
            else:
                return {
                    'available': False,
                    'is_auto_generated': False,
                    'language': None,
                    'source': None
                }
                
        except Exception as e:
            logger.warning(f"Failed to check transcript availability: {e}")
            return {
                'available': False,
                'error': str(e)
            }


class InternetArchiveVideoSearcher:
    """Search Internet Archive for videos."""
    
    API_URL = "https://archive.org/advancedsearch.php"
    
    def __init__(self):
        self.session = requests.Session()
        
    def search(self,
              query: str,
              media_type: str = 'movies',
              date_range: Optional[Tuple[str, str]] = None,
              max_results: int = 50) -> List[VideoMetadata]:
        """
        Search Internet Archive for videos.
        
        Args:
            query: Search query
            media_type: 'movies', 'audio', etc.
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            max_results: Maximum results
            
        Returns:
            List of VideoMetadata objects
        """
        # Build query
        ia_query = f"{query} AND mediatype:{media_type}"
        
        if date_range:
            ia_query += f" AND date:[{date_range[0]} TO {date_range[1]}]"
        
        params = {
            'q': ia_query,
            'fl[]': ['identifier', 'title', 'description', 'date', 'runtime', 'subject'],
            'sort[]': 'date desc',
            'rows': min(max_results, 100),
            'page': 1,
            'output': 'json'
        }
        
        videos = []
        
        try:
            response = self.session.get(self.API_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for doc in data.get('response', {}).get('docs', []):
                # Parse date
                date_str = doc.get('date', '')
                try:
                    upload_date = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    upload_date = None
                
                # Parse runtime (usually in format "HH:MM:SS" or "MM:SS")
                runtime = doc.get('runtime', '')
                duration_seconds = self._parse_runtime(runtime)
                
                identifier = doc.get('identifier', '')
                
                videos.append(VideoMetadata(
                    video_id=identifier,
                    url=f"https://archive.org/details/{identifier}",
                    title=doc.get('title'),
                    description=doc.get('description'),
                    platform='internet_archive',
                    upload_date=upload_date,
                    duration_seconds=duration_seconds,
                    view_count=None,  # Not available from search
                    transcript_available=None,
                    discovery_method='internet_archive_api',
                    priority=2,  # Lower priority than YouTube
                    metadata={
                        'subjects': doc.get('subject', []),
                        'identifier': identifier
                    }
                ))
                
        except Exception as e:
            logger.error(f"Internet Archive search failed: {e}")
            
        return videos
    
    def _parse_runtime(self, runtime: str) -> Optional[int]:
        """Parse runtime string to seconds."""
        if not runtime:
            return None
        
        parts = runtime.split(':')
        if len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        elif len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        
        return None
    
    def check_transcript_availability(self, identifier: str) -> Dict[str, Any]:
        """Check if IA item has transcript files."""
        metadata_url = f"https://archive.org/metadata/{identifier}"
        
        try:
            response = self.session.get(metadata_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Check for subtitle/transcript files
            files = data.get('files', [])
            transcript_files = [
                f for f in files
                if f.get('name', '').endswith(('.srt', '.vtt', '.txt'))
                and 'subtitle' in f.get('name', '').lower()
            ]
            
            if transcript_files:
                return {
                    'available': True,
                    'files': [f['name'] for f in transcript_files],
                    'source': 'internet_archive'
                }
            else:
                return {
                    'available': False,
                    'source': None
                }
                
        except Exception as e:
            logger.warning(f"Failed to check IA transcript: {e}")
            return {
                'available': False,
                'error': str(e)
            }


class VideoDiscoveryAgent(DiscoveryAgent):
    """
    Agent for discovering Epstein-related video content.
    
    Sources:
    1. YouTube (via scraping or API)
    2. Internet Archive
    
    Transcript sources checked:
    - YouTube auto-captions (via yt-dlp)
    - YouTube manual captions (via API)
    - Internet Archive subtitle files
    """
    
    AGENT_ID = 'video-discovery-v2'
    VERSION = '2.0.0'
    
    DEFAULT_KEYWORDS = [
        'Epstein',
        'Jeffrey Epstein',
        'Ghislaine Maxwell',
        'Epstein case',
        'Epstein documentary',
        'Epstein documentary 2024',
        'Epstein documentary 2025',
        'Epstein Island',
        'Little Saint James',
        'Epstein victims',
        'Epstein trial',
        'Epstein files',
        'Epstein release',
        'Virginia Giuffre'
    ]
    
    def __init__(self, config: Optional[AgentConfig] = None):
        # Initialize searchers BEFORE calling super().__init__()
        # because _initialize_resources() needs them
        self.youtube = YouTubeSearcher(api_key=config.youtube_api_key if config and hasattr(config, 'youtube_api_key') else None)
        self.internet_archive = InternetArchiveVideoSearcher()
        
        # Now call parent init (which calls _initialize_resources)
        super().__init__(config)
        
    def _validate_config(self):
        """Validate agent configuration."""
        pass  # YouTube API key is optional
    
    def _initialize_resources(self):
        """Initialize resources."""
        logger.info(f"VideoDiscoveryAgent initialized (YouTube API: {'enabled' if self.youtube.api_key else 'disabled'})")
    
    async def search(self,
                    keywords: List[str] = None,
                    date_range: Tuple[str, str] = None,
                    max_results: int = 1000,
                    platforms: List[str] = None,
                    **kwargs) -> List[VideoMetadata]:
        """
        Search for videos across platforms.
        
        Args:
            keywords: Search terms
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            max_results: Maximum videos to discover
            platforms: ['youtube', 'internet_archive'] or None for both
            
        Returns:
            List of VideoMetadata objects
        """
        keywords = keywords or self.DEFAULT_KEYWORDS
        date_range = date_range or ('1990-01-01', '2025-12-31')
        platforms = platforms or ['youtube', 'internet_archive']
        
        all_videos = []
        
        # Parse date range
        start_date = datetime.strptime(date_range[0], '%Y-%m-%d') if date_range[0] else None
        end_date = datetime.strptime(date_range[1], '%Y-%m-%d') if date_range[1] else None
        
        # Search each platform
        if 'youtube' in platforms:
            logger.info("Searching YouTube...")
            try:
                youtube_results = await self._search_youtube(
                    keywords, start_date, end_date, max_results
                )
                all_videos.extend(youtube_results)
                logger.info(f"YouTube: Found {len(youtube_results)} videos")
            except Exception as e:
                logger.error(f"YouTube search failed: {e}")
        
        if 'internet_archive' in platforms:
            logger.info("Searching Internet Archive...")
            try:
                ia_results = await self._search_internet_archive(
                    keywords, date_range, max_results
                )
                all_videos.extend(ia_results)
                logger.info(f"Internet Archive: Found {len(ia_results)} videos")
            except Exception as e:
                logger.error(f"Internet Archive search failed: {e}")
        
        # Check transcript availability for each video
        logger.info("Checking transcript availability...")
        for video in all_videos:
            if video.platform == 'youtube':
                transcript_info = self.youtube.check_transcript_availability(video.video_id)
                video.transcript_available = transcript_info.get('available', False)
                video.transcript_source = transcript_info.get('source')
            elif video.platform == 'internet_archive':
                transcript_info = self.internet_archive.check_transcript_availability(video.video_id)
                video.transcript_available = transcript_info.get('available', False)
                video.transcript_source = transcript_info.get('source')
        
        # Deduplicate
        deduplicated = self._deduplicate_videos(all_videos)
        
        # Update metrics
        self.metrics['total_discovered'] = len(all_videos)
        self.metrics['unique_videos'] = len(deduplicated)
        self.metrics['with_transcripts'] = sum(1 for v in deduplicated if v.transcript_available)
        self.metrics['platforms_breakdown'] = {
            'youtube': len([v for v in all_videos if v.platform == 'youtube']),
            'internet_archive': len([v for v in all_videos if v.platform == 'internet_archive'])
        }
        
        return deduplicated
    
    async def _search_youtube(self,
                             keywords: List[str],
                             start_date: Optional[datetime],
                             end_date: Optional[datetime],
                             max_results: int) -> List[VideoMetadata]:
        """Search YouTube for videos."""
        loop = asyncio.get_event_loop()
        
        all_results = []
        
        # Search each keyword
        for keyword in keywords:
            try:
                results = await loop.run_in_executor(
                    None,
                    lambda: self.youtube.search(
                        query=keyword,
                        published_after=start_date,
                        published_before=end_date,
                        max_results=min(50, max_results // len(keywords))
                    )
                )
                all_results.extend(results)
                
                # Rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"YouTube search failed for '{keyword}': {e}")
        
        return all_results
    
    async def _search_internet_archive(self,
                                      keywords: List[str],
                                      date_range: Tuple[str, str],
                                      max_results: int) -> List[VideoMetadata]:
        """Search Internet Archive for videos."""
        loop = asyncio.get_event_loop()
        
        # Use primary keywords only
        query = ' OR '.join(keywords[:5])  # IA works better with fewer terms
        
        results = await loop.run_in_executor(
            None,
            lambda: self.internet_archive.search(
                query=query,
                media_type='movies',
                date_range=date_range,
                max_results=min(100, max_results)
            )
        )
        
        return results
    
    def _deduplicate_videos(self, videos: List[VideoMetadata]) -> List[VideoMetadata]:
        """Remove duplicate videos by URL."""
        seen = set()
        unique = []
        
        for video in videos:
            # Use video_id + platform as unique key
            key = f"{video.platform}:{video.video_id}"
            
            if key not in seen:
                seen.add(key)
                unique.append(video)
        
        return unique
    
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute discovery task."""
        keywords = task.get("keywords", self.DEFAULT_KEYWORDS)
        date_range = task.get("date_range", ('1990-01-01', '2025-12-31'))
        max_results = task.get("max_results", 1000)
        platforms = task.get("platforms", ['youtube', 'internet_archive'])
        
        try:
            results = await self.search(
                keywords=keywords,
                date_range=date_range,
                max_results=max_results,
                platforms=platforms
            )
            
            return TaskResult(
                status="success",
                output=results,
                metrics=self.metrics
            )
            
        except Exception as e:
            return TaskResult(
                status="failure",
                error=str(e),
                retry_allowed=self._should_retry(e)
            )


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Video Discovery Agent')
    parser.add_argument('--keywords', nargs='+', default=['Epstein'])
    parser.add_argument('--start-date', default='2024-01-01')
    parser.add_argument('--end-date', default='2024-01-31')
    parser.add_argument('--max-results', type=int, default=50)
    parser.add_argument('--platforms', nargs='+', default=['youtube', 'internet_archive'])
    parser.add_argument('--youtube-api-key', help='YouTube Data API key (optional)')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create config with API key if provided
    config = AgentConfig(agent_id='video-discovery-test')
    if args.youtube_api_key:
        config.youtube_api_key = args.youtube_api_key
    
    # Create agent
    agent = VideoDiscoveryAgent(config)
    
    # Run discovery
    async def main():
        results = await agent.search(
            keywords=args.keywords,
            date_range=(args.start_date, args.end_date),
            max_results=args.max_results,
            platforms=args.platforms
        )
        
        print(f"\nDiscovered {len(results)} videos:")
        for i, video in enumerate(results[:10], 1):
            print(f"{i}. {video.title or 'N/A'}")
            print(f"   Platform: {video.platform}")
            print(f"   Duration: {video.duration_seconds}s")
            print(f"   Transcript: {'Yes' if video.transcript_available else 'No'}")
            print(f"   URL: {video.url}")
            print()
    
    asyncio.run(main())
