

---

## Phase 22: Media Acquisition Agents (NEW)

### NewsDiscoveryAgent
```yaml
agent_id: news-discovery-v2
name: News Discovery Agent v2
version: 2.0.0
type: discovery
category: news

purpose: |
  Discovers Epstein-related news articles from GDELT, Wayback Machine,
  RSS feeds, and news APIs. Multi-source discovery with deduplication.

capabilities:
  - gdelt_query: Query GDELT Event Database (100M+ events)
  - wayback_search: Search Wayback Machine (916B+ pages)
  - rss_crawl: Historical RSS feed crawling
  - newsapi_query: Query NewsAPI.org (free tier)
  - keyword_matching: Multi-keyword boolean search
  - deduplication: URL and content hash dedup
  - rate_limiting: Respectful 1 req/sec to APIs

inputs:
  - keywords: List[str] - ["Epstein", "Maxwell", "Virginia Giuffre"]
  - date_range: Tuple[str, str] - ("1990-01-01", "2025-12-31")
  - sources: List[str] - Specific domains or None for all
  - max_results: int - Maximum articles to discover

outputs:
  - NewsArticleURL:
    - url: str
    - title: str
    - publish_date: datetime
    - source_domain: str
    - discovery_method: str (gdelt/wayback/rss/api)
    - priority: int (1-10)
    - keywords_matched: List[str]

dependencies:
  - gdelt >= 0.1.14
  - requests >= 2.31.0
  - beautifulsoup4 >= 4.12.0
  - feedparser >= 6.0.0
  - waybackpy >= 3.0.0

configuration:
  gdelt_timeout: 30
  wayback_delay: 1.0
  rss_feeds_file: config/rss_feeds.json
  max_results_per_source: 10000
  newsapi_key: null  # Optional
  
runtime:
  max_workers: 5
  batch_size: 100
  retry_attempts: 3
```

### VideoDiscoveryAgent
```yaml
agent_id: video-discovery-v2
name: Video Discovery Agent v2
version: 2.0.0
type: discovery
category: video

purpose: |
  Discovers Epstein-related video content across YouTube,
  Internet Archive, Vimeo, and other platforms.

capabilities:
  - youtube_search: YouTube search (API or scraping)
  - ia_movies_search: Internet Archive movies
  - transcript_check: Verify caption availability
  - metadata_extraction: Title, description, duration, views
  - duration_filter: Filter by video length
  - date_filter: Filter by upload date

inputs:
  - keywords: List[str]
  - date_range: Tuple[str, str]
  - max_results: int (default 1000)
  - platforms: List[str] - ["youtube", "internet_archive", "vimeo"]
  - min_duration: int - Minimum seconds (default 60)
  - max_duration: int - Maximum seconds (default 7200)

outputs:
  - VideoMetadata:
    - video_id: str
    - platform: str
    - title: str
    - description: str
    - url: str
    - upload_date: datetime
    - duration_seconds: int
    - view_count: int
    - transcript_available: bool
    - transcript_source: str

dependencies:
  - youtube-search-python >= 1.6.0
  - google-api-python-client >= 2.100.0 (optional)
  - requests >= 2.31.0

configuration:
  youtube_api_key: null  # Optional for higher quota
  use_web_scraping: true  # Fallback without API
  max_results_per_platform: 500
  
runtime:
  max_workers: 3
  youtube_quota_limit: 10000  # per day
  
free_tier_limits:
  youtube_api: 10000 quota/day (~40-50 videos with captions)
  youtube_scraping: Unlimited (slower)
  internet_archive: Unlimited
```

### VideoTranscriberAgent
```yaml
agent_id: video-transcriber
name: Video Transcriber Agent
version: 1.0.0
type: collection
category: video

purpose: |
  Downloads videos and extracts transcripts using FREE methods:
  yt-dlp (auto-captions), YouTube API (official captions),
  or local Whisper (AI transcription on GPU).

capabilities:
  - yt_dlp_transcript: Extract auto-captions (FREE)
  - youtube_api_transcript: Official captions (FREE with API key)
  - whisper_local_transcribe: AI transcription on Tesla K80 (FREE)
  - whisper_api_transcribe: Backup paid option
  - audio_extraction: Extract audio for transcription
  - format_conversion: SRT/VTT/JSON to plain text
  - timestamp_preservation: Keep segment timestamps
  - language_detection: Auto-detect language

inputs:
  - video: VideoMetadata
  - preferred_method: str (yt_dlp/youtube_api/whisper_local)
  - download_video: bool (default false)
  - language: str (default "auto")

outputs:
  - VideoTranscript:
    - video_id: str
    - transcript_text: str (full text)
    - transcript_segments: List[Dict] (with timestamps)
    - transcript_source: str
    - language: str
    - is_auto_generated: bool
    - confidence_score: float
    - download_duration_seconds: int

free_methods_priority:
  1: yt_dlp_auto       # FREE, no API key needed
  2: youtube_api      # FREE, 10K quota/day
  3: whisper_local    # FREE, uses our GPU
  4: whisper_api      # PAID backup

dependencies:
  - yt-dlp >= 2023.10.0
  - openai-whisper >= 20231117 (optional, for local)
  - google-api-python-client >= 2.100.0 (optional)
  - pydub >= 0.25.0
  - ffmpeg (system binary)

configuration:
  whisper_model: "base"  # Options: tiny, base, small, medium, large-v3
  use_gpu: true
  gpu_device: 0  # Tesla K80
  download_audio: false  # Stream to Whisper
  keep_audio_files: false
  max_audio_duration: 7200  # 2 hours
  youtube_api_key: null
  
runtime:
  max_workers: 2
  whisper_batch_size: 1
  
gpu_requirements:
  tiny: ~1GB VRAM
  base: ~1GB VRAM
  small: ~2GB VRAM
  medium: ~5GB VRAM
  large-v3: ~10GB VRAM (K80 has 12GB - OK!)
```

### DocumentDiscoveryAgent
```yaml
agent_id: document-discovery-v2
name: Document Discovery Agent v2
version: 2.0.0
type: discovery
category: document

purpose: |
  Discovers official documents, court filings, government releases
  from CourtListener/RECAP, GovInfo, PACER, and FOIA archives.

capabilities:
  - courtlistener_search: Search RECAP archive (FREE)
  - govinfo_search: Search GovInfo API (FREE)
  - pacer_monitor: Monitor PACER (requires account)
  - foia_search: Search FOIA releases
  - docket_tracking: Track case dockets for updates
  - new_release_monitor: Continuous monitoring
  - metadata_extraction: Case info, parties, dates

inputs:
  - case_name: str - "Epstein" or "Maxwell" or case number
  - docket_number: str - Optional (e.g., "19-cr-08333")
  - court: str - Optional (e.g., "sdny")
  - document_type: str - Optional (filing, opinion, order)
  - date_range: Tuple[str, str]

outputs:
  - DocumentMetadata:
    - id: str
    - source: str (courtlistener/govinfo/pacer/foia)
    - document_type: str
    - title: str
    - docket_number: str
    - case_name: str
    - court: str
    - filing_date: datetime
    - url: str
    - recap_id: str
    - page_count: int
    - file_size_bytes: int

dependencies:
  - courtlistener-python >= 0.3.0
  - requests >= 2.31.0
  - python-dateutil >= 2.8.0

configuration:
  court_listener_api_key: null  # Not required for basic search
  pacer_username: null
  pacer_password: null
  check_interval_hours: 24
  
runtime:
  max_workers: 2
  respect_robots_txt: true
  
free_access:
  court_listener: Full access (crowdsourced PACER)
  govinfo: Full access (public documents)
  pacer: $0.10/page (not free, use CourtListener instead)
```

### NewsCollectorAgent
```yaml
agent_id: news-collector
name: News Collector Agent
version: 1.0.0
type: collection
category: news

purpose: |
  Downloads and processes news articles. Handles paywalls
  via Wayback Machine fallback. Extracts clean text,
  metadata, and cross-references with our database.

capabilities:
  - direct_download: HTTP with browser headers
  - wayback_fallback: Wayback Machine retrieval
  - article_extraction: newspaper3k / news-please
  - metadata_extraction: Authors, date, keywords
  - paywall_detection: Detect and bypass paywalls
  - content_validation: Verify quality/extraction
  - entity_linking: Cross-reference with exposed_persons
  - duplicate_detection: URL and content dedup

inputs:
  - article_url: NewsArticleURL
  - extraction_method: str (newspaper3k/news-please)
  - force_wayback: bool (default false)

outputs:
  - CollectedArticle:
    - id: int (database ID)
    - title: str
    - content: str (clean text)
    - summary: str (auto-generated)
    - authors: List[str]
    - publish_date: datetime
    - source_url: str
    - wayback_url: str (if used)
    - source_domain: str
    - entities_mentioned: Dict
    - related_person_ids: List[int]
    - collection_method: str
    - extraction_confidence: float

dependencies:
  - newspaper3k >= 0.2.8
  - news-please >= 1.5.0
  - beautifulsoup4 >= 4.12.0
  - requests >= 2.31.0
  - waybackpy >= 3.0.0

configuration:
  user_agent: "EpsteinMediaBot/1.0 (Research Project)"
  request_timeout: 30
  wayback_timeout: 60
  min_content_length: 500
  max_retries: 3
  respect_robots_txt: true
  
runtime:
  max_workers: 10
  batch_size: 50
  parallel_domains: 5
  delay_between_requests: 0.5
```

### DocumentDownloaderAgent
```yaml
agent_id: document-downloader
name: Document Downloader Agent
version: 1.0.0
type: collection
category: document

purpose: |
  Downloads official documents (PDFs) from court systems,
  government archives, and other sources. Extracts text,
  entities, and stores with metadata.

capabilities:
  - pdf_download: HTTP PDF download
  - recap_api_download: CourtListener/RECAP API
  - govinfo_download: GovInfo API
  - wayback_fallback: Historical versions
  - pdf_text_extraction: PyMuPDF / pdfplumber
  - ocr_fallback: OCR for scanned PDFs (Surya on GPU)
  - metadata_extraction: PDF properties
  - checksum_verification: SHA-256 integrity check
  - encryption_detection: Handle encrypted PDFs

inputs:
  - document: DocumentMetadata
  - store_original: bool (default true)
  - extract_entities: bool (default true)

outputs:
  - DownloadedDocument:
    - id: int (database ID)
    - metadata: DocumentMetadata
    - text_content: str (extracted text)
    - extracted_entities: Dict
    - summary: str
    - file_path: str (original PDF location)
    - page_count: int
    - checksum: str (SHA-256)
    - file_size_bytes: int
    - processing_time_seconds: float

dependencies:
  - PyMuPDF >= 1.23.0
  - pdfplumber >= 0.10.0
  - requests >= 2.31.0
  - courtlistener-python >= 0.3.0
  - surya-ocr >= 0.4.0 (for OCR fallback)

configuration:
  store_original_files: true
  pdf_max_pages: 1000
  ocr_enabled: true
  ocr_backend: "surya"  # surya, docling, tesseract
  ocr_gpu_device: 0  # Tesla K80
  download_timeout: 120
  max_file_size_mb: 100
  
runtime:
  max_workers: 5
  batch_size: 10
```

### EntityExtractorAgent
```yaml
agent_id: entity-extractor-v2
name: Entity Extractor Agent v2
version: 2.0.0
type: processing
category: nlp

purpose: |
  Extracts named entities from text using spaCy NER and
  GLiNER zero-shot. Cross-references with our existing
  exposed_persons database for relationship mapping.

capabilities:
  - spacy_ner: Named entity recognition (PERSON, ORG, GPE, DATE)
  - gliner_extraction: Zero-shot NER (case_number, court, charge)
  - regex_patterns: Custom patterns (dates, amounts, phone numbers)
  - entity_resolution: Deduplicate and normalize
  - database_matching: Match to exposed_persons
  - relationship_extraction: Entity co-occurrence
  - confidence_scoring: Per-entity confidence scores

inputs:
  - text: str
  - context: Dict (article metadata for context)
  - entity_types: List[str] (optional filter)

outputs:
  - ExtractedEntities:
    - persons: List[Dict] (name, confidence, count)
    - organizations: List[Dict]
    - locations: List[Dict]
    - dates: List[Dict]
    - legal_references: List[Dict] (case_number, court, statute)
    - financial_amounts: List[Dict]
    - database_matches: List[Dict] (matched entities from our DB)
    - confidence_scores: Dict[str, float]

dependencies:
  - spacy >= 3.7.0
  - en-core-web-trf (spaCy model)
  - gliner >= 0.2.0
  - rapidfuzz >= 3.4.0
  - psycopg2-binary >= 2.9.0

configuration:
  spacy_model: "en_core_web_trf"
  gliner_model: "urchade/gliner_base"
  confidence_threshold: 0.7
  max_entities_per_type: 100
  fuzzy_match_threshold: 85  # For DB matching
  
runtime:
  use_gpu: true
  batch_size: 32
  parallel_workers: 4
```

### TextAnalyzerAgent
```yaml
agent_id: text-analyzer
name: Text Analyzer Agent
version: 1.0.0
type: processing
category: nlp

purpose: |
  Analyzes text for sentiment, topics, themes, readability,
  and key phrases. Classifies content type for research
  paper categorization.

capabilities:
  - sentiment_analysis: Positive/negative/neutral score
  - topic_classification: Zero-shot classification (BART)
  - theme_extraction: Key themes and concepts
  - readability_scoring: Flesch-Kincaid, Flesch Reading Ease
  - keyword_extraction: TF-IDF key phrases
  - summarization: Extractive and abstractive summaries
  - bias_detection: Political/media bias indicators
  - emotion_detection: Anger, fear, joy, etc.

inputs:
  - text: str
  - analysis_types: List[str] (sentiment, topics, readability, etc.)
  - candidate_topics: List[str] (for zero-shot classification)

outputs:
  - TextAnalysis:
    - sentiment_score: float (-1.0 to 1.0)
    - subjectivity_score: float (0.0 to 1.0)
    - primary_topic: str
    - topic_confidence: float
    - all_topics: Dict[str, float]
    - key_phrases: List[str]
    - summary: str
    - readability_score: float
    - word_count: int
    - emotion_scores: Dict[str, float]

dependencies:
  - transformers >= 4.35.0
  - torch >= 2.1.0
  - textblob >= 0.17.0
  - nltk >= 3.8.0
  - scikit-learn >= 1.3.0

configuration:
  sentiment_model: "distilbert-base-uncased-finetuned-sst-2-english"
  topic_classifier: "facebook/bart-large-mnli"
  summarizer: "facebook/bart-large-cnn"
  max_input_length: 1024
  candidate_topics:
    - "court proceedings"
    - "investigation"
    - "victim testimony"
    - "political implications"
    - "social commentary"
    - "financial crimes"
    - "relationships and network"
    - "prison and death"
    - "document releases"
    
runtime:
  use_gpu: true
  batch_size: 16
  max_workers: 2
```

---

## Agent Communication Bus

### Message Types

```python
@dataclass
class DiscoveryResult:
    """Message from discovery agents to orchestrator."""
    agent_id: str
    query_id: str
    timestamp: datetime
    items_found: int
    items: List[MediaURL]
    query_params: Dict
    execution_time_ms: int
    
@dataclass
class CollectionTask:
    """Message from orchestrator to collection agents."""
    task_id: str
    media_type: str  # news, video, document
    source_url: str
    priority: int
    retry_count: int
    max_retries: int
    context: Dict  # Discovery metadata
    
@dataclass
class CollectionResult:
    """Message from collection agents to orchestrator."""
    task_id: str
    success: bool
    media_id: Optional[int]  # Database ID
    error_message: Optional[str]
    storage_path: Optional[str]
    processing_time_ms: int
    
@dataclass
class ProcessingTask:
    """Message for NLP processing agents."""
    task_id: str
    media_type: str
    media_id: int
    text_content: str
    extract_entities: bool
    analyze_text: bool
    
@dataclass
class ProcessingResult:
    """Result from processing agents."""
    task_id: str
    entities: Optional[ExtractedEntities]
    analysis: Optional[TextAnalysis]
    success: bool
    error_message: Optional[str]
```

### Event Topics

```yaml
# Pub/Sub topics for agent communication
topics:
  discovery.news.found:
    description: "New articles discovered"
    publishers: [news-discovery-v2]
    subscribers: [orchestrator, logger]
    
  discovery.video.found:
    description: "New videos discovered"
    publishers: [video-discovery-v2]
    subscribers: [orchestrator, logger]
    
  discovery.document.found:
    description: "New documents discovered"
    publishers: [document-discovery-v2]
    subscribers: [orchestrator, logger]
    
  collection.completed:
    description: "Media item successfully collected"
    publishers: [news-collector, video-transcriber, document-downloader]
    subscribers: [orchestrator, storage-manager, logger]
    
  collection.failed:
    description: "Media collection failed"
    publishers: [all-collection-agents]
    subscribers: [orchestrator, error-handler, logger]
    
  processing.completed:
    description: "NLP processing completed"
    publishers: [entity-extractor-v2, text-analyzer]
    subscribers: [orchestrator, storage-manager]
    
  system.health:
    description: "Agent health status"
    publishers: [all-agents]
    subscribers: [monitor, logger]
```

---

## Phase 22 Implementation Status

| Agent | Status | Priority | Completion |
|-------|--------|----------|------------|
| NewsDiscoveryAgent | ✅ Spec'd | P0 | 100% |
| VideoDiscoveryAgent | ✅ Spec'd | P0 | 100% |
| VideoTranscriberAgent | ✅ Spec'd | P0 | 100% |
| DocumentDiscoveryAgent | ✅ Spec'd | P0 | 100% |
| NewsCollectorAgent | ✅ Spec'd | P0 | 100% |
| DocumentDownloaderAgent | ✅ Spec'd | P0 | 100% |
| EntityExtractorAgent | ✅ Spec'd | P1 | 100% |
| TextAnalyzerAgent | ✅ Spec'd | P1 | 100% |

---

*Phase 22 Agent Specifications Added*
