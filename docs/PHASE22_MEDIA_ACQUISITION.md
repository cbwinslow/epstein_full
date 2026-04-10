# Epstein Media Acquisition Infrastructure

> **Phase 22: Comprehensive Media Collection System**  
> **Created:** April 4, 2026  
> **Architecture:** Multi-Agent Pipeline  
> **Status:** Planning Phase

---

## Executive Summary

**Goal:** Build enterprise-grade infrastructure to automatically discover, acquire, analyze, and store ALL Epstein-related media:
- News articles (print/web)
- Court documents & legal filings
- Government releases & reports
- Video content (with transcription)
- Audio files & podcasts
- Social media archives
- Academic papers & research
- FOIA releases

**Architecture:** Agent-based pipeline with specialized workers
**Cost:** 100% FREE using open APIs and public archives
**Timeline:** 21 days implementation

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     EPSTEIN MEDIA ACQUISITION SYSTEM                        │
│                                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Discovery   │  │  Acquisition │  │  Processing  │  │   Storage    │     │
│  │   Agents     │→ │   Agents     │→ │   Agents     │→ │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
│         ↓                ↓                ↓                ↓               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ GDELT        │  │ NewsCollector│  │ TextAnalyzer │  │ PostgreSQL   │     │
│  │ Scraper      │  │ Wayback      │  │ VideoTrans   │  │ Object Store │     │
│  │ YouTube      │  │ Document     │  │ EntityExtract│  │ Index Store  │     │
│  │ RSS Crawler  │  │ Downloader   │  │ Summarizer   │  │ Cache Layer  │     │
│  │ CourtMonitor │  │ VideoFetcher │  │ Classifier   │  │ Queue        │     │
│  └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Core Classes & Components

### 1. Discovery Agents (`agents/discovery/`)

#### NewsDiscoveryAgent
```python
class NewsDiscoveryAgent:
    """
    Discovers Epstein-related news articles from multiple sources.
    """
    
    def __init__(self):
        self.gdelt_client = GdeltClient()
        self.wayback_searcher = WaybackSearcher()
        self.rss_crawler = RSSCrawler()
        
    def search_news(self, 
                   keywords: List[str],
                   date_range: Tuple[datetime, datetime],
                   sources: List[str] = None) -> List[NewsArticleURL]:
        """
        Search for news articles across all discovery sources.
        
        Args:
            keywords: Search terms (Epstein, Maxwell, etc.)
            date_range: Start and end dates
            sources: Specific news domains to search
            
        Returns:
            List of discovered article URLs with metadata
        """
        results = []
        
        # GDELT discovery (bulk historical)
        results.extend(
            self.gdelt_client.query_events(
                keywords=keywords,
                date_range=date_range
            )
        )
        
        # Wayback Machine discovery
        results.extend(
            self.wayback_searcher.find_snapshots(
                domains=sources or DEFAULT_NEWS_SOURCES,
                keywords=keywords,
                date_range=date_range
            )
        )
        
        # RSS feed discovery
        results.extend(
            self.rss_crawler.discover(
                feeds=self._load_historical_rss_feeds(),
                keywords=keywords
            )
        )
        
        return self._deduplicate_results(results)
```

#### VideoDiscoveryAgent
```python
class VideoDiscoveryAgent:
    """
    Discovers Epstein-related video content.
    """
    
    SOURCES = ['youtube', 'vimeo', 'internet_archive', 'court_tv']
    
    def __init__(self):
        self.youtube_searcher = YouTubeSearcher(api_key=None)  # Can use without API for basic search
        self.ia_searcher = InternetArchiveVideoSearcher()
        
    def search_videos(self,
                     keywords: List[str],
                     date_range: Tuple[datetime, datetime],
                     max_results: int = 1000) -> List[VideoMetadata]:
        """
        Discover videos across platforms.
        
        Returns video metadata including:
        - Video URL
        - Platform (YouTube, Vimeo, etc.)
        - Title, description, duration
        - Upload date
        - Transcript availability
        """
        videos = []
        
        # YouTube search (can use web scraping or API)
        videos.extend(
            self.youtube_searcher.search(
                query=' '.join(keywords),
                published_after=date_range[0],
                published_before=date_range[1],
                max_results=max_results
            )
        )
        
        # Internet Archive video search
        videos.extend(
            self.ia_searcher.search(
                query='epstein',
                media_type='movies',
                date_range=date_range
            )
        )
        
        return videos
    
    def check_transcript_availability(self, video: VideoMetadata) -> TranscriptSource:
        """
        Check if video has available transcript.
        
        Sources checked:
        1. YouTube auto-captions (free API)
        2. YouTube community captions
        3. Manual transcripts in description
        4. External transcript sites
        """
        if video.platform == 'youtube':
            return self._check_youtube_transcripts(video.video_id)
        elif video.platform == 'internet_archive':
            return self._check_ia_transcripts(video.identifier)
        return None
```

#### DocumentDiscoveryAgent
```python
class DocumentDiscoveryAgent:
    """
    Discovers official documents, court filings, releases.
    """
    
    SOURCES = {
        'court_listener': 'https://www.courtlistener.com/api/rest/v3/',
        'pacer': 'https://pacer.uscourts.gov/',  # Requires account
        'recap': 'https://www.courtlistener.com/recap/',
        'foia': 'https://www.foia.gov/',
        'govinfo': 'https://www.govinfo.gov/api/',
        'federal_register': 'https://www.federalregister.gov/api/v1/'
    }
    
    def __init__(self):
        self.court_listener = CourtListenerAPI()
        self.govinfo_client = GovInfoAPI()
        
    def search_court_documents(self,
                              case_name: str = 'Epstein',
                              docket_number: str = None,
                              court: str = None) -> List[DocumentMetadata]:
        """
        Search for court documents and filings.
        
        Uses RECAP archive (free, crowdsourced PACER docs)
        and CourtListener API (free tier available).
        """
        documents = []
        
        # Search CourtListener/RECAP
        recap_docs = self.court_listener.search(
            q=case_name,
            type='document',
            court=court
        )
        documents.extend(recap_docs)
        
        # Search GovInfo for official releases
        govinfo_docs = self.govinfo_client.search(
            query=case_name,
            collections=['USCOURTS', 'CREC', 'FR']
        )
        documents.extend(govinfo_docs)
        
        return documents
    
    def monitor_new_releases(self, 
                            sources: List[str] = None,
                            interval_hours: int = 24) -> Iterator[List[DocumentMetadata]]:
        """
        Continuously monitor for new document releases.
        
        Yields newly discovered documents as they appear.
        """
        while True:
            new_docs = []
            for source in (sources or self.SOURCES.keys()):
                latest = self._get_latest_documents(source)
                new = self._filter_new_only(latest)
                new_docs.extend(new)
            
            if new_docs:
                yield new_docs
                
            time.sleep(interval_hours * 3600)
```

---

### 2. Acquisition Agents (`agents/acquisition/`)

#### NewsCollector
```python
class NewsCollector:
    """
    Collects and stores news articles from discovered URLs.
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.extractor = ArticleExtractor()
        self.wayback_client = WaybackClient()
        
    def collect_article(self, article_url: NewsArticleURL) -> CollectedArticle:
        """
        Download and process a single news article.
        
        Workflow:
        1. Try direct download
        2. If 404/paywall → try Wayback Machine
        3. Extract text, metadata, entities
        4. Cross-reference with our database
        5. Store in PostgreSQL
        """
        try:
            # Attempt direct download
            html = self._download(article_url.url)
            
        except (requests.HTTPError, ConnectionError):
            # Fallback to Wayback Machine
            html = self.wayback_client.get_snapshot(
                url=article_url.url,
                timestamp=article_url.publish_date or 'closest'
            )
            
        if not html:
            logger.warning(f"Could not retrieve: {article_url.url}")
            return None
        
        # Extract article content
        article = self.extractor.extract(html, article_url.url)
        
        # Cross-reference with our entities
        article.entities_mentioned = self._find_entity_mentions(article.text)
        article.related_person_ids = self._link_to_persons(article.entities_mentioned)
        
        # Store
        article_id = self.storage.store_article(article)
        
        return CollectedArticle(
            id=article_id,
            article=article,
            source_url=article_url.url,
            collection_method='wayback' if 'web.archive.org' in str(html) else 'direct'
        )
    
    def collect_batch(self, 
                     article_urls: List[NewsArticleURL],
                     max_workers: int = 10) -> CollectionResult:
        """
        Collect multiple articles in parallel.
        
        Args:
            article_urls: List of discovered article URLs
            max_workers: Number of parallel download workers
            
        Returns:
            CollectionResult with success/failure stats
        """
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.collect_article, url): url 
                for url in article_urls
            }
            
            results = CollectionResult()
            for future in as_completed(futures):
                url = futures[future]
                try:
                    article = future.result()
                    if article:
                        results.successful += 1
                    else:
                        results.failed += 1
                except Exception as e:
                    logger.error(f"Failed to collect {url}: {e}")
                    results.failed += 1
                    
        return results
```

#### VideoTranscriber
```python
class VideoTranscriber:
    """
    Downloads videos and extracts transcripts.
    Supports multiple free transcript sources.
    """
    
    TRANSCRIPT_SOURCES = {
        'youtube_api': 'YouTube Data API v3 (captions endpoint)',
        'youtube_auto': 'YouTube auto-generated captions (yt-dlp)',
        'whisper_local': 'OpenAI Whisper local (free, GPU)',
        'whisper_api': 'OpenAI Whisper API (paid backup)',
        'assembly_ai': 'AssemblyAI (free tier available)',
        'internet_archive': 'IA transcript files'
    }
    
    def __init__(self, 
                 youtube_api_key: str = None,
                 use_local_whisper: bool = True):
        self.youtube_api_key = youtube_api_key
        self.use_local_whisper = use_local_whisper
        self.whisper_model = None
        
        if use_local_whisper:
            self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Load Whisper model on GPU if available."""
        import whisper
        self.whisper_model = whisper.load_model("base")  # Can use "small", "medium", "large"
        logger.info("Whisper model loaded (local transcription ready)")
    
    def get_transcript(self, video: VideoMetadata) -> VideoTranscript:
        """
        Get transcript for a video using best available source.
        
        Priority order (free options first):
        1. YouTube API captions (free with API key)
        2. YouTube auto-captions via yt-dlp (free)
        3. Local Whisper transcription (free, GPU)
        4. Internet Archive transcript files (free)
        """
        
        # Try YouTube API first
        if video.platform == 'youtube' and self.youtube_api_key:
            try:
                return self._get_youtube_api_transcript(video.video_id)
            except NoTranscriptAvailable:
                pass
        
        # Try yt-dlp for auto-captions
        if video.platform == 'youtube':
            try:
                return self._get_ytdlp_transcript(video.video_id)
            except Exception:
                pass
        
        # Download audio and transcribe locally
        if self.use_local_whisper and self.whisper_model:
            try:
                audio_path = self._download_audio(video.url)
                return self._transcribe_with_whisper(audio_path, video)
            except Exception as e:
                logger.warning(f"Whisper transcription failed: {e}")
        
        # Check Internet Archive
        if video.platform == 'internet_archive':
            return self._get_ia_transcript(video.identifier)
        
        raise TranscriptNotAvailable(f"No transcript available for {video.url}")
    
    def _get_youtube_api_transcript(self, video_id: str) -> VideoTranscript:
        """
        Use YouTube Data API to get captions.
        
        Free tier: 10,000 quota units/day
        caption download: 200 units per video
        = 50 videos/day on free tier
        """
        from googleapiclient.discovery import build
        
        youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
        
        # Get caption tracks
        captions = youtube.captions().list(
            part='snippet',
            videoId=video_id
        ).execute()
        
        for caption in captions.get('items', []):
            if caption['snippet']['trackKind'] in ['standard', 'ASR']:
                # Download caption content
                caption_data = youtube.captions().download(
                    id=caption['id']
                ).execute()
                
                return VideoTranscript(
                    video_id=video_id,
                    text=self._parse_caption_format(caption_data),
                    language=caption['snippet']['language'],
                    is_auto_generated=caption['snippet']['trackKind'] == 'ASR',
                    source='youtube_api'
                )
        
        raise NoTranscriptAvailable("No captions found via API")
    
    def _get_ytdlp_transcript(self, video_id: str) -> VideoTranscript:
        """
        Use yt-dlp to extract auto-generated captions.
        
        Completely free, no API key needed.
        """
        import subprocess
        
        url = f"https://youtube.com/watch?v={video_id}"
        
        # List available subtitles
        result = subprocess.run(
            ['yt-dlp', '--list-subs', url],
            capture_output=True,
            text=True
        )
        
        # Download auto-generated English transcript
        cmd = [
            'yt-dlp',
            '--skip-download',
            '--write-auto-subs',
            '--sub-langs', 'en',
            '--convert-subs', 'srt',
            '-o', f'/tmp/{video_id}.%(ext)s',
            url
        ]
        
        subprocess.run(cmd, capture_output=True)
        
        # Parse the SRT file
        srt_path = f'/tmp/{video_id}.en.srt'
        if os.path.exists(srt_path):
            with open(srt_path, 'r') as f:
                text = self._clean_srt(f.read())
            os.remove(srt_path)
            
            return VideoTranscript(
                video_id=video_id,
                text=text,
                language='en',
                is_auto_generated=True,
                source='yt-dlp_auto'
            )
        
        raise TranscriptNotAvailable("No auto-captions available")
    
    def _transcribe_with_whisper(self, 
                                 audio_path: str, 
                                 video: VideoMetadata) -> VideoTranscript:
        """
        Transcribe audio using local Whisper model.
        
        Requires:
        - GPU recommended (Tesla K80 available)
        - 10GB+ VRAM for 'large-v3' model
        - 2-5GB VRAM for 'base' model
        """
        result = self.whisper_model.transcribe(audio_path)
        
        # Clean up audio file
        os.remove(audio_path)
        
        return VideoTranscript(
            video_id=video.video_id if hasattr(video, 'video_id') else video.url,
            text=result['text'],
            language=result.get('language', 'en'),
            is_auto_generated=True,
            source='whisper_local',
            segments=result.get('segments', [])  # Timestamped segments
        )
```

#### DocumentDownloader
```python
class DocumentDownloader:
    """
    Downloads and processes official documents.
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.pdf_processor = PDFProcessor()
        
    def download_document(self, doc: DocumentMetadata) -> DownloadedDocument:
        """
        Download a document from various sources.
        
        Handles:
        - Direct PDF downloads
        - CourtListener/RECAP API
        - GovInfo API
        - Wayback Machine for historical docs
        """
        
        # Determine download strategy
        if doc.source == 'court_listener':
            content = self._download_from_recap(doc.recap_id)
        elif doc.source == 'govinfo':
            content = self._download_from_govinfo(doc.package_id)
        elif doc.source == 'direct_url':
            content = self._download_direct(doc.url)
        else:
            # Fallback to Wayback
            content = self._download_from_wayback(doc.url)
        
        if not content:
            raise DownloadFailed(f"Could not download: {doc.url}")
        
        # Process based on type
        if doc.mime_type == 'application/pdf':
            processed = self.pdf_processor.process(content)
        elif doc.mime_type == 'text/html':
            processed = self._extract_text_from_html(content)
        else:
            processed = content
        
        # Store
        doc_id = self.storage.store_document(
            content=processed,
            metadata=doc,
            original_content=content if doc.mime_type == 'application/pdf' else None
        )
        
        return DownloadedDocument(
            id=doc_id,
            metadata=doc,
            text_content=processed.get('text'),
            extracted_entities=processed.get('entities')
        )
```

---

### 3. Processing Agents (`agents/processing/`)

#### EntityExtractor
```python
class EntityExtractor:
    """
    Extracts named entities from text content.
    Uses our existing NER pipeline.
    """
    
    def __init__(self):
        # Use existing models from our pipeline
        self.spacy_model = spacy.load('en_core_web_trf')
        self.gliner = GLiNER.from_pretrained('urchade/gliner_base')
        
    def extract_from_text(self, text: str) -> ExtractedEntities:
        """
        Extract all entity types from text.
        
        Returns:
            persons, organizations, locations, dates, 
            case_numbers, financial_amounts, etc.
        """
        # spaCy NER
        doc = self.spacy_model(text)
        
        entities = ExtractedEntities(
            persons=[ent.text for ent in doc.ents if ent.label_ == 'PERSON'],
            organizations=[ent.text for ent in doc.ents if ent.label_ == 'ORG'],
            locations=[ent.text for ent in doc.ents if ent.label_ == 'GPE'],
            dates=[ent.text for ent in doc.ents if ent.label_ == 'DATE']
        )
        
        # GLiNER for specialized entities
        gliner_entities = self.gliner.predict_entities(
            text,
            labels=['case_number', 'court', 'charge', 'statute', 'Bates_number']
        )
        
        entities.legal_references = [
            e['text'] for e in gliner_entities 
            if e['label'] in ['case_number', 'court']
        ]
        
        return entities
    
    def cross_reference_with_database(self, 
                                     entities: ExtractedEntities) -> CrossReferenceResult:
        """
        Match extracted entities to our existing database.
        
        Links articles to:
        - exposed_persons
        - exposed_organizations  
        - exposed_locations
        - flights
        - documents
        """
        matches = CrossReferenceResult()
        
        # Match persons
        for person_name in entities.persons:
            db_match = self._find_person_in_db(person_name)
            if db_match:
                matches.person_ids.append(db_match.id)
                matches.confidence_scores.append(db_match.match_confidence)
        
        return matches
```

#### TextAnalyzer
```python
class TextAnalyzer:
    """
    Analyzes text content for themes, sentiment, topics.
    """
    
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            'sentiment-analysis',
            model='distilbert-base-uncased-finetuned-sst-2-english'
        )
        self.classifier = pipeline(
            'zero-shot-classification',
            model='facebook/bart-large-mnli'
        )
        
    def analyze(self, text: str) -> TextAnalysis:
        """
        Full text analysis including:
        - Sentiment (positive/negative/neutral)
        - Subjectivity
        - Topic classification
        - Key phrases
        - Readability metrics
        """
        
        # Sentiment
        sentiment = self.sentiment_analyzer(text[:512])[0]  # Model limit
        
        # Topic classification
        topics = self.classifier(
            text[:1024],
            candidate_labels=[
                'court proceedings',
                'investigation',
                'victim testimony',
                'political implications',
                'social commentary',
                'financial crimes',
                'relationships/network',
                'prison/death',
                'aftermath/releases'
            ]
        )
        
        return TextAnalysis(
            sentiment_score=sentiment['score'] if sentiment['label'] == 'POSITIVE' else -sentiment['score'],
            primary_topic=topics['labels'][0],
            topic_confidence=topics['scores'][0],
            all_topics=dict(zip(topics['labels'], topics['scores'])),
            word_count=len(text.split()),
            readability_score=self._flesch_reading_ease(text)
        )
```

---

### 4. Storage Manager (`storage/`)

#### StorageManager
```python
class StorageManager:
    """
    Centralized storage interface for all media types.
    Uses PostgreSQL for metadata, filesystem for content.
    """
    
    def __init__(self, 
                 pg_connection_string: str,
                 base_path: str = '/home/cbwinslow/workspace/epstein-data/media/'):
        self.pg_conn = psycopg2.connect(pg_connection_string)
        self.base_path = base_path
        
    def store_article(self, article: CollectedArticle) -> int:
        """Store news article with metadata."""
        with self.pg_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO media_news_articles (
                    source_domain, source_name, article_url, wayback_url,
                    title, authors, publish_date, content, summary,
                    keywords, sentiment_score, entities_mentioned,
                    related_person_ids, extraction_method, collection_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id
            """, (
                article.source_domain, article.source_name,
                article.source_url, article.wayback_url,
                article.title, article.authors, article.publish_date,
                article.content, article.summary, article.keywords,
                article.sentiment_score, json.dumps(article.entities_mentioned),
                article.related_person_ids, article.collection_method
            ))
            return cur.fetchone()[0]
    
    def store_video(self, video: VideoWithTranscript) -> int:
        """Store video metadata and transcript."""
        # Store transcript
        transcript_path = self._save_transcript(video.transcript)
        
        with self.pg_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO media_videos (
                    video_id, platform, title, description,
                    url, upload_date, duration_seconds,
                    transcript_text, transcript_path,
                    transcript_source, entities_mentioned,
                    related_person_ids, collection_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id
            """, (
                video.video_id, video.platform, video.title,
                video.description, video.url, video.upload_date,
                video.duration, video.transcript.text,
                transcript_path, video.transcript.source,
                json.dumps(video.entities_mentioned),
                video.related_person_ids
            ))
            return cur.fetchone()[0]
    
    def store_document(self, 
                      content: Dict[str, Any],
                      metadata: DocumentMetadata,
                      original_content: bytes = None) -> int:
        """Store official document with extracted text."""
        # Save PDF if provided
        file_path = None
        if original_content:
            file_path = self._save_file(
                original_content, 
                f"documents/{metadata.source}/",
                f"{metadata.id}.pdf"
            )
        
        with self.pg_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO media_documents (
                    source, document_type, title, docket_number,
                    court, filing_date, url, file_path,
                    text_content, extracted_entities,
                    page_count, file_size_bytes, collection_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING id
            """, (
                metadata.source, metadata.document_type,
                metadata.title, metadata.docket_number,
                metadata.court, metadata.filing_date,
                metadata.url, file_path,
                content.get('text'),
                json.dumps(content.get('entities')),
                content.get('page_count'),
                len(original_content) if original_content else None
            ))
            return cur.fetchone()[0]
```

---

## Database Schema

```sql
-- Media content metadata tables

-- News Articles
CREATE TABLE media_news_articles (
    id SERIAL PRIMARY KEY,
    
    -- Source info
    source_domain VARCHAR(100) NOT NULL,
    source_name VARCHAR(100),
    source_category VARCHAR(50),  -- mainstream, investigative, tabloid, blog
    
    -- URLs
    article_url TEXT NOT NULL,
    wayback_url TEXT,
    canonical_url TEXT,
    
    -- Content metadata
    title TEXT NOT NULL,
    authors TEXT[],
    publish_date DATE,
    publish_timestamp TIMESTAMP,
    content TEXT,
    summary TEXT,
    keywords TEXT[],
    word_count INTEGER,
    
    -- Analysis
    sentiment_score FLOAT,
    subjectivity_score FLOAT,
    primary_topic VARCHAR(50),
    topic_confidence FLOAT,
    all_topics JSONB,
    
    -- Cross-references
    entities_mentioned JSONB,
    related_person_ids INTEGER[],
    related_flight_ids INTEGER[],
    related_document_ids INTEGER[],
    
    -- Collection metadata
    discovery_source VARCHAR(50),  -- gdelt, wayback, rss, manual
    collection_method VARCHAR(50),  -- direct, wayback, api
    extraction_method VARCHAR(50),  -- newspaper3k, news-please
    extraction_confidence FLOAT,
    gdelt_event_id BIGINT,
    
    -- Timestamps
    discovered_at TIMESTAMP,
    collected_at TIMESTAMP DEFAULT NOW(),
    analyzed_at TIMESTAMP,
    
    -- Constraints
    CONSTRAINT unique_article_url UNIQUE (article_url, publish_date)
);

CREATE INDEX idx_news_articles_date ON media_news_articles(publish_date);
CREATE INDEX idx_news_articles_source ON media_news_articles(source_domain);
CREATE INDEX idx_news_articles_topic ON media_news_articles(primary_topic);
CREATE INDEX idx_news_entities ON media_news_articles USING GIN(entities_mentioned);
CREATE INDEX idx_news_persons ON media_news_articles USING GIN(related_person_ids);

-- Videos
CREATE TABLE media_videos (
    id SERIAL PRIMARY KEY,
    
    -- Video metadata
    video_id VARCHAR(50) NOT NULL,
    platform VARCHAR(50) NOT NULL,  -- youtube, vimeo, internet_archive
    title TEXT,
    description TEXT,
    url TEXT NOT NULL,
    upload_date DATE,
    duration_seconds INTEGER,
    view_count BIGINT,
    
    -- Transcript
    transcript_text TEXT,
    transcript_path TEXT,  -- File path if stored separately
    transcript_source VARCHAR(50),  -- youtube_api, yt-dlp, whisper_local, whisper_api
    transcript_language VARCHAR(10),
    is_auto_transcript BOOLEAN DEFAULT TRUE,
    transcript_segments JSONB,  -- Timestamped segments
    
    -- Analysis
    entities_mentioned JSONB,
    related_person_ids INTEGER[],
    sentiment_score FLOAT,
    key_topics TEXT[],
    
    -- Collection metadata
    discovered_at TIMESTAMP,
    collected_at TIMESTAMP DEFAULT NOW(),
    transcript_collected_at TIMESTAMP,
    
    UNIQUE(video_id, platform)
);

CREATE INDEX idx_videos_date ON media_videos(upload_date);
CREATE INDEX idx_videos_platform ON media_videos(platform);
CREATE INDEX idx_video_persons ON media_videos USING GIN(related_person_ids);

-- Official Documents
CREATE TABLE media_documents (
    id SERIAL PRIMARY KEY,
    
    -- Document metadata
    source VARCHAR(50) NOT NULL,  -- court_listener, govinfo, pacer, foia
    document_type VARCHAR(50),  -- filing, opinion, order, release, report
    title TEXT,
    docket_number VARCHAR(100),
    case_name TEXT,
    court VARCHAR(100),
    filing_date DATE,
    
    -- URLs and files
    url TEXT,
    file_path TEXT,
    
    -- Content
    text_content TEXT,
    extracted_entities JSONB,
    summary TEXT,
    key_findings TEXT[],
    
    -- File info
    page_count INTEGER,
    file_size_bytes BIGINT,
    mime_type VARCHAR(50),
    checksum VARCHAR(64),
    
    -- Cross-references
    related_person_ids INTEGER[],
    related_case_ids INTEGER[],
    
    -- Collection metadata
    discovered_at TIMESTAMP,
    collected_at TIMESTAMP DEFAULT NOW(),
    analyzed_at TIMESTAMP,
    
    UNIQUE(source, docket_number, filing_date)
);

CREATE INDEX idx_documents_date ON media_documents(filing_date);
CREATE INDEX idx_documents_source ON media_documents(source);
CREATE INDEX idx_documents_court ON media_documents(court);
CREATE INDEX idx_doc_persons ON media_documents USING GIN(related_person_ids);

-- Collection Queue (for background processing)
CREATE TABLE media_collection_queue (
    id SERIAL PRIMARY KEY,
    media_type VARCHAR(50) NOT NULL,  -- article, video, document
    source_url TEXT NOT NULL,
    source_platform VARCHAR(50),
    priority INTEGER DEFAULT 5,  -- 1 (high) to 10 (low)
    status VARCHAR(50) DEFAULT 'pending',  -- pending, processing, completed, failed
    
    -- Discovery metadata
    discovered_by VARCHAR(50),  -- agent name
    discovery_date TIMESTAMP,
    keywords_matched TEXT[],
    
    -- Processing
    worker_id VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    -- Result
    result_id INTEGER,  -- ID in respective table
    
    UNIQUE(source_url, media_type)
);

CREATE INDEX idx_queue_status ON media_collection_queue(status, priority);
CREATE INDEX idx_queue_type ON media_collection_queue(media_type, status);

-- Collection Statistics (daily tracking)
CREATE TABLE media_collection_stats (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    media_type VARCHAR(50) NOT NULL,
    
    -- Discovery stats
    discovered_count INTEGER DEFAULT 0,
    
    -- Collection stats
    attempted_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    failed_count INTEGER DEFAULT 0,
    
    -- Storage stats
    storage_bytes BIGINT DEFAULT 0,
    
    UNIQUE(date, media_type)
);
```

---

## YouTube Transcript Strategy

### Free Options (Priority Order)

| Method | Cost | Rate Limit | Quality | Implementation |
|--------|------|------------|---------|----------------|
| **yt-dlp** | FREE | None | Auto-captions | Download via CLI |
| **YouTube API** | FREE | 10K quota/day | Official captions | API calls |
| **Whisper Local** | FREE (GPU) | Unlimited | AI transcription | Local model |
| **Captions via URL** | FREE | None | Manual upload | Parse from URL |

### Implementation Plan

```python
# 1. Extract video URLs from web resources
# 2. For each video, try transcript sources in order:

class YouTubeTranscriptStrategy:
    def get_transcript(self, video_id: str) -> str:
        # 1. Try yt-dlp (free, no API key)
        try:
            return self._get_ytdlp_transcript(video_id)
        except:
            pass
        
        # 2. Try YouTube API (if key available)
        if self.youtube_api_key:
            try:
                return self._get_api_transcript(video_id)
            except:
                pass
        
        # 3. Download audio + Whisper local
        try:
            audio_path = self._download_audio(video_id)
            return self._whisper_transcribe(audio_path)
        except:
            pass
        
        raise TranscriptNotAvailable(video_id)
```

### YouTube Data API (Free Tier)

- **10,000 quota units per day**
- `captions().list()` = 50 units
- `captions().download()` = 200 units
- **~40-50 videos/day** on free tier

**Strategy:** Use for high-priority videos, fallback to yt-dlp/Whisper for bulk

---

## Master Orchestration Script

```python
#!/usr/bin/env python3
"""
Epstein Media Acquisition Master Controller
Runs all discovery and collection agents
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

from agents.discovery import (
    NewsDiscoveryAgent,
    VideoDiscoveryAgent, 
    DocumentDiscoveryAgent
)
from agents.acquisition import (
    NewsCollector,
    VideoTranscriber,
    DocumentDownloader
)
from agents.processing import (
    EntityExtractor,
    TextAnalyzer
)
from storage import StorageManager

logger = logging.getLogger(__name__)

class EpsteinMediaAcquisitionSystem:
    """
    Master controller for all media acquisition.
    
    Usage:
        system = EpsteinMediaAcquisitionSystem()
        
        # Run full historical collection
        system.run_historical_collection(
            start_date='1990-01-01',
            end_date='2025-12-31'
        )
        
        # Run continuous monitoring
        system.run_continuous_monitoring()
    """
    
    def __init__(self, config: dict = None):
        self.config = config or self._load_default_config()
        
        # Initialize storage
        self.storage = StorageManager(
            pg_connection_string=self.config['postgres_url'],
            base_path=self.config['media_storage_path']
        )
        
        # Initialize discovery agents
        self.discovery_agents = {
            'news': NewsDiscoveryAgent(),
            'video': VideoDiscoveryAgent(),
            'document': DocumentDiscoveryAgent()
        }
        
        # Initialize acquisition agents
        self.acquisition_agents = {
            'news': NewsCollector(self.storage),
            'video': VideoTranscriber(
                youtube_api_key=self.config.get('youtube_api_key'),
                use_local_whisper=self.config.get('use_whisper', True)
            ),
            'document': DocumentDownloader(self.storage)
        }
        
        # Initialize processing agents
        self.entity_extractor = EntityExtractor()
        self.text_analyzer = TextAnalyzer()
        
    def run_historical_collection(self,
                                  start_date: str,
                                  end_date: str,
                                  media_types: List[str] = None):
        """
        Run full historical collection for date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            media_types: ['news', 'video', 'document'] or None for all
        """
        media_types = media_types or ['news', 'video', 'document']
        
        for media_type in media_types:
            logger.info(f"Starting historical collection: {media_type}")
            
            # Discovery phase
            discovered = self._discover_media(
                media_type=media_type,
                start_date=start_date,
                end_date=end_date
            )
            
            # Queue for collection
            self._queue_for_collection(media_type, discovered)
            
            # Collection phase (batch processing)
            self._process_collection_queue(media_type)
    
    def run_continuous_monitoring(self, interval_hours: int = 24):
        """
        Continuously monitor for new media.
        Runs indefinitely until interrupted.
        """
        logger.info(f"Starting continuous monitoring (interval: {interval_hours}h)")
        
        while True:
            try:
                # Check for new content
                for media_type, agent in self.discovery_agents.items():
                    new_items = agent.find_recent(
                        since=datetime.now() - timedelta(hours=interval_hours)
                    )
                    
                    if new_items:
                        logger.info(f"Discovered {len(new_items)} new {media_type} items")
                        self._queue_for_collection(media_type, new_items)
                        self._process_collection_queue(media_type)
                
                # Wait for next check
                time.sleep(interval_hours * 3600)
                
            except KeyboardInterrupt:
                logger.info("Monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Monitoring error: {e}")
                time.sleep(300)  # Wait 5 min on error
    
    def _discover_media(self,
                       media_type: str,
                       start_date: str,
                       end_date: str) -> List[MediaURL]:
        """Run discovery agent for media type."""
        agent = self.discovery_agents[media_type]
        
        if media_type == 'news':
            return agent.search_news(
                keywords=['Epstein', 'Maxwell', 'Virginia Giuffre', 'Jeffrey Epstein'],
                date_range=(start_date, end_date)
            )
        elif media_type == 'video':
            return agent.search_videos(
                keywords=['Epstein'],
                date_range=(start_date, end_date)
            )
        elif media_type == 'document':
            return agent.search_court_documents(
                case_name='Epstein'
            )
    
    def _queue_for_collection(self, 
                             media_type: str,
                             items: List[MediaURL]):
        """Add discovered items to collection queue."""
        for item in items:
            self.storage.queue_item(
                media_type=media_type,
                source_url=item.url,
                priority=item.priority,
                keywords_matched=item.keywords
            )
    
    def _process_collection_queue(self, media_type: str):
        """Process queued items for collection."""
        agent = self.acquisition_agents[media_type]
        
        while True:
            # Get batch of pending items
            batch = self.storage.get_queued_items(
                media_type=media_type,
                status='pending',
                limit=100
            )
            
            if not batch:
                break
            
            # Process batch
            for item in batch:
                try:
                    if media_type == 'news':
                        result = agent.collect_article(item)
                    elif media_type == 'video':
                        result = agent.get_transcript(item)
                    elif media_type == 'document':
                        result = agent.download_document(item)
                    
                    # Mark as completed
                    self.storage.update_queue_status(
                        item.id, 
                        'completed',
                        result_id=result.id
                    )
                    
                except Exception as e:
                    logger.error(f"Collection failed for {item.url}: {e}")
                    self.storage.update_queue_status(
                        item.id,
                        'failed',
                        error_message=str(e)
                    )

if __name__ == '__main__':
    system = EpsteinMediaAcquisitionSystem()
    
    # Run historical collection for all media types
    system.run_historical_collection(
        start_date='1990-01-01',
        end_date='2025-12-31',
        media_types=['news', 'video', 'document']
    )
```

---

## Implementation Timeline

### Week 1: Core Infrastructure
- **Day 1-2:** Create base classes (StorageManager, Config)
- **Day 3-4:** Implement NewsDiscoveryAgent + NewsCollector
- **Day 5-7:** Implement VideoDiscoveryAgent + VideoTranscriber

### Week 2: Document & Processing
- **Day 8-9:** Implement DocumentDiscoveryAgent + DocumentDownloader
- **Day 10-11:** Implement EntityExtractor + TextAnalyzer
- **Day 12-14:** Database schema + migration scripts

### Week 3: Integration & Testing
- **Day 15-17:** Master orchestration script
- **Day 18-19:** Integration testing
- **Day 20-21:** Performance optimization + documentation

---

## Configuration

```yaml
# config/media_acquisition.yaml

# Storage
postgres_url: "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
media_storage_path: "/home/cbwinslow/workspace/epstein-data/media/"

# API Keys (optional but recommended)
youtube_api_key: null  # Set for higher quota
assemblyai_key: null   # Backup transcription

# Processing
use_whisper: true
whisper_model: "base"  # base, small, medium, large
max_workers: 10

# Discovery
default_date_range:
  start: "1990-01-01"
  end: "2025-12-31"

news_sources:
  - cnn.com
  - nytimes.com
  - washingtonpost.com
  - bbc.com
  - theguardian.com
  - miamiherald.com
  - vanityfair.com
  - newyorker.com

video_platforms:
  - youtube
  - internet_archive
  - vimeo

# Monitoring
continuous_monitoring: false
monitor_interval_hours: 24

# Logging
log_level: "INFO"
log_file: "/var/log/epstein/media_acquisition.log"
```

---

*Document created as part of Epstein Files Analysis Project*  
*Phase 22: Media Acquisition Infrastructure*
