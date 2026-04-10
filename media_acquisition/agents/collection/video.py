"""
Video Transcriber Agent
Downloads and transcribes video content using yt-dlp and Whisper.
"""

import asyncio
import json
import logging
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

import requests

# Import base classes
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.base import (
    CollectionAgent, AgentConfig, TaskResult,
    VideoMetadata, StorageManager
)

logger = logging.getLogger(__name__)


class YouTubeTranscriber:
    """Transcribe YouTube videos using yt-dlp (captions) or Whisper (audio)."""
    
    def __init__(self,
                 whisper_model: str = 'base',
                 use_gpu: bool = True,
                 storage_path: str = '/home/cbwinslow/workspace/epstein-data/media/videos/'):
        self.whisper_model = whisper_model
        self.use_gpu = use_gpu
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.audio_path = self.storage_path / 'audio'
        self.transcript_path = self.storage_path / 'transcripts'
        self.caption_path = self.storage_path / 'captions'
        
        for path in [self.audio_path, self.transcript_path, self.caption_path]:
            path.mkdir(exist_ok=True)
    
    def extract_video_id(self, url: str) -> str:
        """Extract YouTube video ID from URL."""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video metadata using yt-dlp."""
        try:
            result = subprocess.run(
                ['yt-dlp', '--dump-json', '--no-download', url],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                return json.loads(result.stdout)
            else:
                logger.error(f"yt-dlp failed: {result.stderr}")
                return {}
                
        except Exception as e:
            logger.error(f"Failed to get video info: {e}")
            return {}
    
    def check_captions(self, url: str) -> Dict[str, Any]:
        """Check available captions using yt-dlp."""
        try:
            result = subprocess.run(
                ['yt-dlp', '--list-subs', url],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = result.stdout
            
            # Parse output
            captions = {
                'manual': [],
                'auto': []
            }
            
            lines = output.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                
                if 'Available subtitles' in line:
                    current_section = 'manual'
                elif 'Available automatic captions' in line:
                    current_section = 'auto'
                elif current_section and line and not line.startswith('Language'):
                    # Parse language code and name
                    parts = line.split()
                    if len(parts) >= 2:
                        lang_code = parts[0]
                        lang_name = ' '.join(parts[1:])
                        captions[current_section].append({
                            'code': lang_code,
                            'name': lang_name
                        })
            
            return captions
            
        except Exception as e:
            logger.error(f"Failed to check captions: {e}")
            return {'manual': [], 'auto': []}
    
    def download_captions(self,
                         url: str,
                         video_id: str,
                         language: str = 'en',
                         prefer_manual: bool = True) -> Optional[Path]:
        """
        Download captions using yt-dlp.
        
        Args:
            url: Video URL
            video_id: YouTube video ID
            language: Language code (e.g., 'en')
            prefer_manual: Prefer manual captions over auto-generated
            
        Returns:
            Path to caption file or None
        """
        caption_file = self.caption_path / f"{video_id}_{language}.vtt"
        
        # Build yt-dlp command
        cmd = [
            'yt-dlp',
            '--skip-download',
            '--write-subs' if prefer_manual else '--write-auto-subs',
            '--write-auto-subs' if not prefer_manual else '',
            '--sub-langs', language,
            '--sub-format', 'vtt/best',
            '-o', str(self.caption_path / f"{video_id}.%(ext)s"),
            url
        ]
        
        # Remove empty strings
        cmd = [c for c in cmd if c]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                # Find the downloaded file
                expected_file = self.caption_path / f"{video_id}.{language}.vtt"
                if expected_file.exists():
                    return expected_file
                    
                # Check for alternative names
                for file in self.caption_path.glob(f"{video_id}*.{language}.*"):
                    return file
                    
            logger.warning(f"Caption download failed or no captions available: {result.stderr}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to download captions: {e}")
            return None
    
    def download_audio(self,
                      url: str,
                      video_id: str,
                      format: str = 'mp3',
                      quality: str = 'best') -> Optional[Path]:
        """
        Download audio using yt-dlp.
        
        Args:
            url: Video URL
            video_id: YouTube video ID
            format: Output format (mp3, wav, m4a)
            quality: Audio quality (best, worst, or specific bitrate)
            
        Returns:
            Path to audio file or None
        """
        audio_file = self.audio_path / f"{video_id}.{format}"
        
        # Build yt-dlp command
        cmd = [
            'yt-dlp',
            '--extract-audio',
            '--audio-format', format,
            '--audio-quality', quality,
            '--output', str(self.audio_path / f"{video_id}.%(ext)s"),
            url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes for long videos
            )
            
            if result.returncode == 0:
                # yt-dlp saves with the original extension, then converts
                expected_file = self.audio_path / f"{video_id}.{format}"
                if expected_file.exists():
                    return expected_file
                    
                # Check for the file with any extension
                for ext in [format, 'm4a', 'webm', 'mp4']:
                    file = self.audio_path / f"{video_id}.{ext}"
                    if file.exists():
                        return file
                        
            logger.error(f"Audio download failed: {result.stderr}")
            return None
            
        except Exception as e:
            logger.error(f"Failed to download audio: {e}")
            return None
    
    def transcribe_with_whisper(self,
                                 audio_path: Path,
                                 video_id: str,
                                 model: str = None,
                                 language: str = 'en') -> Dict[str, Any]:
        """
        Transcribe audio using faster-whisper (local GPU).
        
        Args:
            audio_path: Path to audio file
            video_id: Video ID for output naming
            model: Whisper model size (tiny, base, small, medium, large-v3)
            language: Language code
            
        Returns:
            Dict with transcript text, segments, and metadata
        """
        model = model or self.whisper_model
        
        # Use faster-whisper for GPU acceleration
        try:
            from faster_whisper import WhisperModel
            
            # Load model
            device = "cuda" if self.use_gpu else "cpu"
            compute_type = "float16" if self.use_gpu else "int8"
            
            logger.info(f"Loading Whisper model '{model}' on {device}...")
            whisper_model = WhisperModel(model, device=device, compute_type=compute_type)
            
            # Transcribe
            logger.info(f"Transcribing {audio_path}...")
            segments, info = whisper_model.transcribe(
                str(audio_path),
                language=language,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Process segments
            transcript_segments = []
            full_text_parts = []
            
            for segment in segments:
                transcript_segments.append({
                    'start': segment.start,
                    'end': segment.end,
                    'text': segment.text.strip()
                })
                full_text_parts.append(segment.text.strip())
            
            full_text = ' '.join(full_text_parts)
            
            # Save transcript
            output_file = self.transcript_path / f"{video_id}_whisper.json"
            transcript_data = {
                'video_id': video_id,
                'model': model,
                'language': language,
                'detected_language': info.language,
                'language_probability': info.language_probability,
                'full_text': full_text,
                'segments': transcript_segments,
                'transcribed_at': datetime.now().isoformat()
            }
            
            with open(output_file, 'w') as f:
                json.dump(transcript_data, f, indent=2)
            
            return transcript_data
            
        except ImportError:
            logger.error("faster-whisper not installed. Run: pip install faster-whisper")
            return {'error': 'faster-whisper not installed'}
        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            return {'error': str(e)}
    
    def parse_caption_file(self, caption_path: Path) -> Dict[str, Any]:
        """Parse VTT caption file to transcript format."""
        try:
            with open(caption_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple VTT parsing (could use webvtt-py for better parsing)
            segments = []
            full_text_parts = []
            
            # Remove WEBVTT header
            content = re.sub(r'WEBVTT.*?\n\n', '\n', content, flags=re.DOTALL)
            
            # Parse cues
            cue_pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3}).*?\n(.*?)(?=\n\n|\Z)'
            
            for match in re.finditer(cue_pattern, content, re.DOTALL):
                start = match.group(1)
                end = match.group(2)
                text = match.group(3).replace('\n', ' ').strip()
                
                # Parse timestamps
                def parse_ts(ts):
                    h, m, s = ts.split(':')
                    return int(h) * 3600 + int(m) * 60 + float(s)
                
                segments.append({
                    'start': parse_ts(start),
                    'end': parse_ts(end),
                    'text': text
                })
                full_text_parts.append(text)
            
            return {
                'full_text': ' '.join(full_text_parts),
                'segments': segments,
                'source': 'caption_file'
            }
            
        except Exception as e:
            logger.error(f"Failed to parse caption file: {e}")
            return {'error': str(e)}
    
    def transcribe(self,
                  url: str,
                  strategy: str = 'auto',
                  language: str = 'en') -> Dict[str, Any]:
        """
        Main transcription method with fallback strategies.
        
        Strategies (in order):
        1. 'captions': Use YouTube captions only
        2. 'whisper': Use Whisper transcription only
        3. 'auto': Try captions first, fall back to Whisper
        
        Args:
            url: Video URL
            strategy: Transcription strategy
            language: Language code
            
        Returns:
            Dict with transcript data
        """
        video_id = self.extract_video_id(url)
        result = {
            'video_id': video_id,
            'url': url,
            'strategy': strategy,
            'success': False
        }
        
        # Strategy 1: Try captions
        if strategy in ['captions', 'auto']:
            logger.info(f"Trying caption download for {video_id}...")
            
            caption_info = self.check_captions(url)
            has_manual = any(c['code'] == language for c in caption_info.get('manual', []))
            has_auto = any(c['code'] == language for c in caption_info.get('auto', []))
            
            if has_manual or has_auto:
                caption_path = self.download_captions(
                    url, video_id, language, prefer_manual=has_manual
                )
                
                if caption_path:
                    transcript = self.parse_caption_file(caption_path)
                    
                    if 'error' not in transcript:
                        result.update({
                            'success': True,
                            'source': 'youtube_captions',
                            'caption_type': 'manual' if has_manual else 'auto',
                            'transcript': transcript['full_text'],
                            'segments': transcript['segments'],
                            'caption_file': str(caption_path)
                        })
                        return result
        
        # Strategy 2: Whisper transcription
        if strategy in ['whisper', 'auto']:
            logger.info(f"Falling back to Whisper for {video_id}...")
            
            # Download audio
            audio_path = self.download_audio(url, video_id)
            
            if audio_path:
                # Transcribe
                transcript = self.transcribe_with_whisper(
                    audio_path, video_id, language=language
                )
                
                if 'error' not in transcript:
                    result.update({
                        'success': True,
                        'source': 'whisper_local',
                        'model': transcript.get('model'),
                        'transcript': transcript['full_text'],
                        'segments': transcript.get('segments', []),
                        'audio_file': str(audio_path),
                        'transcript_file': str(self.transcript_path / f"{video_id}_whisper.json")
                    })
                    return result
                else:
                    result['error'] = transcript['error']
            else:
                result['error'] = 'Failed to download audio'
        
        return result


class VideoTranscriber(CollectionAgent):
    """
    Agent for transcribing video content.
    
    Sources prioritized:
    1. YouTube captions (free, via yt-dlp)
    2. Local Whisper (free, GPU-accelerated)
    3. YouTube Data API (free tier: 10k units/day)
    
    Transcript strategy:
    - Prefer manual captions (higher quality)
    - Accept auto-captions (acceptable quality)
    - Fall back to Whisper (best quality, costs GPU time)
    """
    
    AGENT_ID = 'video-transcriber-v2'
    VERSION = '2.0.0'
    
    def __init__(self, config: Optional[AgentConfig] = None, storage: Optional[StorageManager] = None):
        super().__init__(config, storage)
        
        self.transcriber = YouTubeTranscriber(
            whisper_model=getattr(config, 'whisper_model', 'base'),
            use_gpu=getattr(config, 'use_gpu', True),
            storage_path='/home/cbwinslow/workspace/epstein-data/media/videos/'
        )
    
    def _validate_config(self):
        """Validate agent configuration."""
        pass  # No strict requirements
    
    async def collect(self, video: VideoMetadata, strategy: str = 'auto') -> Dict[str, Any]:
        """
        Transcribe a video.
        
        Args:
            video: VideoMetadata with URL
            strategy: 'captions', 'whisper', or 'auto'
            
        Returns:
            Dict with transcript data and storage info
        """
        url = video.url
        
        logger.info(f"Transcribing video: {video.title or url}")
        
        # Run transcription
        start_time = asyncio.get_event_loop().time()
        
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.transcriber.transcribe(url, strategy=strategy)
        )
        
        duration = asyncio.get_event_loop().time() - start_time
        
        # Update metrics
        if result.get('success'):
            self.metrics['items_collected'] += 1
            self.metrics['transcription_time'] += duration
        else:
            self.metrics['errors'] += 1
        
        # Store in database
        if result.get('success') and self.storage:
            try:
                video_id = self.storage.store_video(
                    video_id=result['video_id'],
                    url=url,
                    title=video.title,
                    description=video.description,
                    platform=video.platform,
                    upload_date=video.upload_date,
                    duration_seconds=video.duration_seconds,
                    view_count=video.view_count,
                    transcript_text=result['transcript'],
                    transcript_source=result['source'],
                    transcript_segments=result.get('segments', [])
                )
                
                result['stored_id'] = video_id
                
            except Exception as e:
                logger.error(f"Failed to store video: {e}")
        
        return result
    
    async def process_queue(self,
                           batch_size: int = 10,
                           strategy: str = 'auto') -> List[Dict[str, Any]]:
        """
        Process a batch of videos from the queue.
        
        Args:
            batch_size: Number of videos to process
            strategy: Transcription strategy
            
        Returns:
            List of transcription results
        """
        if not self.storage:
            raise ValueError("Storage manager required for queue processing")
        
        # Get pending videos
        items = self.storage.get_queued_items(
            media_type='video',
            status='pending',
            limit=batch_size
        )
        
        results = []
        
        for item in items:
            try:
                # Mark as processing
                self.storage.update_queue_status(item['id'], 'processing')
                
                # Create VideoMetadata
                metadata = item.get('metadata', {})
                video = VideoMetadata(
                    video_id=metadata.get('video_id', 'unknown'),
                    url=item['source_url'],
                    title=metadata.get('title'),
                    description=metadata.get('description'),
                    platform=metadata.get('platform', 'youtube'),
                    priority=item['priority']
                )
                
                # Transcribe
                result = await self.collect(video, strategy=strategy)
                
                # Update queue
                if result.get('success'):
                    self.storage.update_queue_status(
                        item['id'],
                        'completed',
                        result_id=result.get('stored_id')
                    )
                else:
                    self.storage.update_queue_status(
                        item['id'],
                        'failed',
                        error_message=result.get('error', 'Unknown error')
                    )
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Failed to process video {item['id']}: {e}")
                self.storage.update_queue_status(
                    item['id'],
                    'failed',
                    error_message=str(e)
                )
                self.metrics['errors'] += 1
        
        return results
    
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute transcription task."""
        videos = task.get("videos", [])
        strategy = task.get("strategy", 'auto')
        
        if not videos:
            return TaskResult(
                status="failure",
                error="No videos provided"
            )
        
        results = []
        
        for video_data in videos:
            try:
                video = VideoMetadata(**video_data)
                result = await self.collect(video, strategy=strategy)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to transcribe video: {e}")
                results.append({
                    'success': False,
                    'error': str(e)
                })
        
        success_count = sum(1 for r in results if r.get('success'))
        
        return TaskResult(
            status="success" if success_count > 0 else "failure",
            output=results,
            metrics=self.metrics
        )


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Video Transcriber Agent')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--strategy', choices=['captions', 'whisper', 'auto'],
                       default='auto',
                       help='Transcription strategy')
    parser.add_argument('--model', default='base',
                       help='Whisper model (tiny/base/small/medium/large-v3)')
    parser.add_argument('--no-gpu', action='store_true',
                       help='Disable GPU (use CPU)')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create transcriber
    transcriber = YouTubeTranscriber(
        whisper_model=args.model,
        use_gpu=not args.no_gpu
    )
    
    # Transcribe
    print(f"Transcribing: {args.url}")
    print(f"Strategy: {args.strategy}")
    print("-" * 60)
    
    result = transcriber.transcribe(args.url, strategy=args.strategy)
    
    if result.get('success'):
        print(f"\n✅ SUCCESS!")
        print(f"Source: {result['source']}")
        print(f"Transcript length: {len(result['transcript'])} characters")
        print(f"Segments: {len(result.get('segments', []))}")
        print(f"\nFirst 500 characters:")
        print(result['transcript'][:500])
    else:
        print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
