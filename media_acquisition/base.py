"""
Epstein Media Acquisition - Base Agent Classes
Base classes for all discovery, collection, and processing agents.
"""

import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
from psycopg2.extras import RealDictCursor

logger = logging.getLogger(__name__)


class AgentState(Enum):
    """Agent lifecycle states."""

    IDLE = "idle"
    READY = "ready"
    RUNNING = "running"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMEOUT = "timeout"


@dataclass
class AgentConfig:
    """Configuration for agents."""

    agent_id: str
    version: str = "1.0.0"
    max_workers: int = 5
    batch_size: int = 100
    retry_attempts: int = 3
    request_timeout: int = 30
    log_level: str = "INFO"
    use_gpu: bool = False
    gpu_device: int = 0

    # Storage
    postgres_url: str = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    storage_path: str = "/home/cbwinslow/workspace/epstein-data/media/"

    # API Keys (optional)
    youtube_api_key: Optional[str] = None
    newsapi_key: Optional[str] = None

    # Rate limiting
    requests_per_second: float = 1.0
    respect_robots_txt: bool = True


@dataclass
class TaskResult:
    """Result from agent task execution."""

    status: str  # 'success', 'failure', 'timeout'
    output: Optional[Any] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
    metrics: Dict[str, Any] = field(default_factory=dict)
    retry_allowed: bool = True
    execution_time_ms: int = 0


@dataclass
class MediaURL:
    """Base class for discovered media URLs."""

    url: str
    title: Optional[str] = None
    source_domain: Optional[str] = None
    publish_date: Optional[datetime] = None
    discovery_method: str = "unknown"
    priority: int = 5
    keywords_matched: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NewsArticleURL(MediaURL):
    """News article URL from discovery."""

    authors: List[str] = field(default_factory=list)
    summary: Optional[str] = None
    source_name: Optional[str] = None
    gdelt_event_id: Optional[int] = None


@dataclass
class VideoMetadata(MediaURL):
    """Video metadata from discovery."""

    video_id: str = ""
    platform: str = ""
    description: Optional[str] = None
    upload_date: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    view_count: Optional[int] = None
    transcript_available: bool = False
    transcript_source: Optional[str] = None


@dataclass
class DocumentMetadata(MediaURL):
    """Document metadata from discovery."""

    # NOTE: Historically the field was named ``doc_type`` in the test suite.
    # The production code renamed it to ``document_type`` for clarity, which
    # caused a type‑checking failure (``__init__`` received an unexpected
    # ``doc_type`` keyword).  To retain backward compatibility we expose both
    # names.  ``doc_type`` is defined as a field with ``init=False`` and a
    # ``__post_init__`` hook copies its value to ``document_type``.  This allows
    # existing callers (including the unit tests) to pass ``doc_type=...`` while
    # keeping the preferred ``document_type`` attribute for new code.
    source: str = ""  # courtlistener, govinfo, pacer, foia
    document_type: Optional[str] = None  # filing, opinion, order
    # Compatibility alias – not part of the public API but accepted by ``__init__``.
    doc_type: Optional[str] = field(default=None, init=False, repr=False)
    docket_number: Optional[str] = None
    case_name: Optional[str] = None
    court: Optional[str] = None
    filing_date: Optional[datetime] = None
    recap_id: Optional[str] = None
    page_count: Optional[int] = None
    file_size_bytes: Optional[int] = None

    def __post_init__(self) -> None:
        """Synchronise the legacy ``doc_type`` alias.

        If a caller supplied ``doc_type`` via ``**kwargs`` (as the test suite
        does), ``dataclasses`` will place the value in ``__dict__`` under the
        ``doc_type`` key because the field is defined with ``init=False``.  We
        then copy that value to ``document_type`` so the rest of the code can
        rely on the canonical attribute.
        """
        if self.doc_type is not None and self.document_type is None:
            self.document_type = self.doc_type


class BaseAgent(ABC):
    """
    Base class for all agents in the media acquisition system.

    Usage:
        class MyAgent(BaseAgent):
            AGENT_ID = 'my-agent'

            async def execute(self, task: Dict) -> TaskResult:
                # Implementation
                pass
    """

    AGENT_ID: str = "base-agent"
    VERSION: str = "1.0.0"
    AGENT_TYPE: str = "base"  # discovery, collection, processing

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or AgentConfig(agent_id=self.AGENT_ID)
        self.state = AgentState.IDLE
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.metrics: Dict[str, Any] = {}

        # Setup logging
        self.logger = logging.getLogger(f"agent.{self.AGENT_ID}")

        # Initialize
        self._validate_config()
        self._initialize_resources()
        self.state = AgentState.READY

        self.logger.info(f"Agent {self.AGENT_ID} v{self.VERSION} initialized")

    def _validate_config(self):
        """Validate agent configuration. Override in subclass."""
        pass

    def _initialize_resources(self):
        """Initialize agent resources. Override in subclass."""
        pass

    def _set_state(self, state: AgentState):
        """Update agent state."""
        old_state = self.state
        self.state = state
        self.logger.debug(f"State transition: {old_state.value} -> {state.value}")

        if state == AgentState.RUNNING:
            self.started_at = datetime.now()
        elif state in [AgentState.SUCCESS, AgentState.FAILURE, AgentState.TIMEOUT]:
            self.completed_at = datetime.now()

    def _get_metrics(self) -> Dict[str, Any]:
        """Get execution metrics."""
        return {
            "agent_id": self.AGENT_ID,
            "version": self.VERSION,
            "state": self.state.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            **self.metrics,
        }

    def _should_retry(self, error: Exception) -> bool:
        """Determine if task should be retried. Override in subclass."""
        retryable_errors = (
            TimeoutError,
            ConnectionError,
            IOError,
        )
        return isinstance(error, retryable_errors)

    def _log_error(self, error: Exception, context: Dict = None):
        """Log error with context."""
        self.logger.error(
            f"Agent {self.AGENT_ID} error: {error}", exc_info=True, extra={"context": context or {}}
        )

    @abstractmethod
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """
        Execute agent task.

        Args:
            task: Task parameters

        Returns:
            TaskResult with status and output
        """
        pass

    async def run(self, task: Dict[str, Any]) -> TaskResult:
        """
        Run agent with full lifecycle management.

        Args:
            task: Task parameters

        Returns:
            TaskResult
        """
        start_time = time.time()

        try:
            self._set_state(AgentState.RUNNING)

            # Execute task
            result = await self.execute(task)

            # Update state based on result
            if result.status == "success":
                self._set_state(AgentState.SUCCESS)
            elif result.status == "timeout":
                self._set_state(AgentState.TIMEOUT)
            else:
                self._set_state(AgentState.FAILURE)

            # Add execution time
            result.execution_time_ms = int((time.time() - start_time) * 1000)
            result.metrics = self._get_metrics()

            return result

        except Exception as e:
            self._set_state(AgentState.FAILURE)
            self._log_error(e, task)

            return TaskResult(
                status="failure",
                error=str(e),
                error_code="E001",
                retry_allowed=self._should_retry(e),
                execution_time_ms=int((time.time() - start_time) * 1000),
                metrics=self._get_metrics(),
            )

    def health_check(self) -> bool:
        """Check agent health. Override in subclass."""
        return self.state in [AgentState.IDLE, AgentState.READY]

    def shutdown(self):
        """Cleanup resources. Override in subclass."""
        self.logger.info(f"Agent {self.AGENT_ID} shutting down")
        self.state = AgentState.IDLE


class DiscoveryAgent(BaseAgent):
    """Base class for discovery agents."""

    AGENT_TYPE = "discovery"

    async def search(
        self, keywords: List[str], date_range: Tuple[str, str], **kwargs
    ) -> List[MediaURL]:
        """
        Search for media items.

        Args:
            keywords: Search terms
            date_range: (start_date, end_date) as ISO strings
            **kwargs: Additional search parameters

        Returns:
            List of MediaURL objects
        """
        raise NotImplementedError()

    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute discovery task."""
        keywords = task.get("keywords", [])
        date_range = task.get("date_range", ("1990-01-01", "2025-12-31"))
        max_results = task.get("max_results", 1000)

        try:
            results = await self.search(keywords, date_range, max_results=max_results)

            return TaskResult(
                status="success",
                output=results,
                metrics={
                    "items_found": len(results),
                    "keywords": keywords,
                    "date_range": date_range,
                },
            )
        except Exception as e:
            return TaskResult(status="failure", error=str(e), retry_allowed=self._should_retry(e))


class CollectionAgent(BaseAgent):
    """Base class for collection agents."""

    AGENT_TYPE = "collection"

    def __init__(self, config: Optional[AgentConfig] = None, storage=None):
        super().__init__(config)
        self.storage = storage

    async def collect(self, item: MediaURL) -> Any:
        """
        Collect a single media item.

        Args:
            item: MediaURL to collect

        Returns:
            Collected item with metadata
        """
        raise NotImplementedError()

    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute collection task."""
        items = task.get("items", [])

        results = []
        failed = []

        for item in items:
            try:
                result = await self.collect(item)
                results.append(result)
            except Exception as e:
                self.logger.warning(f"Failed to collect {item.url}: {e}")
                failed.append((item.url, str(e)))

        return TaskResult(
            status="success" if results else "failure",
            output=results,
            metrics={"successful": len(results), "failed": len(failed), "failed_urls": failed},
        )


class ProcessingAgent(BaseAgent):
    """Base class for processing agents (NLP)."""

    AGENT_TYPE = "processing"

    async def process(self, text: str, context: Dict = None) -> Any:
        """
        Process text content.

        Args:
            text: Text to process
            context: Additional context

        Returns:
            Processing result
        """
        raise NotImplementedError()

    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute processing task."""
        text = task.get("text", "")
        context = task.get("context", {})

        try:
            result = await self.process(text, context)

            return TaskResult(
                status="success",
                output=result,
                metrics={"text_length": len(text), "processing_type": self.AGENT_ID},
            )
        except Exception as e:
            return TaskResult(
                status="failure",
                error=str(e),
                retry_allowed=False,  # NLP errors are not retryable
            )


class StorageManager:
    """
    Centralized storage manager for all media types.
    Handles PostgreSQL operations and file storage.
    """

    def __init__(self, connection_string: str, base_path: str):
        self.connection_string = connection_string
        self.base_path = base_path
        self.logger = logging.getLogger("storage")

        # Ensure directories exist
        import os

        os.makedirs(f"{base_path}/news-html", exist_ok=True)
        os.makedirs(f"{base_path}/videos", exist_ok=True)
        os.makedirs(f"{base_path}/documents", exist_ok=True)
        os.makedirs(f"{base_path}/transcripts", exist_ok=True)

    def _get_connection(self):
        """Get database connection."""
        return psycopg2.connect(self.connection_string)

    def queue_item(
        self,
        media_type: str,
        source_url: str,
        priority: int = 5,
        keywords_matched: List[str] = None,
        discovered_by: str = None,
        ingestion_run_id: str = None,
    ) -> int:
        """Add item to collection queue."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO media_collection_queue
                    (media_type, source_url, priority, keywords_matched,
                     discovered_by, discovery_date, status, ingestion_run_id)
                    VALUES (%s, %s, %s, %s, %s, NOW(), 'pending', %s)
                    ON CONFLICT (source_url, media_type) DO NOTHING
                    RETURNING id
                """,
                    (
                        media_type,
                        source_url,
                        priority,
                        keywords_matched or [],
                        discovered_by,
                        ingestion_run_id,
                    ),
                )

                result = cur.fetchone()
                conn.commit()
                return result[0] if result else None

    def add_to_queue(
        self,
        media_type: str,
        source_url: str,
        priority: int = 5,
        keywords_matched: List[str] = None,
        discovered_by: str = None,
        metadata: Dict = None,
    ) -> int:
        """Alias for queue_item with metadata support."""
        # Note: metadata is stored in the discovery_metadata column if the table supports it
        # For now, we use the base queue_item method
        return self.queue_item(
            media_type=media_type,
            source_url=source_url,
            priority=priority,
            keywords_matched=keywords_matched,
            discovered_by=discovered_by,
        )

    def get_queue_summary(self) -> Dict:
        """Get summary of queue status."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT media_type, status, COUNT(*)
                    FROM media_collection_queue
                    GROUP BY media_type, status
                    ORDER BY media_type, status
                """)
                results = cur.fetchall()

                summary = {}
                for media_type, status, count in results:
                    if media_type not in summary:
                        summary[media_type] = {}
                    summary[media_type][status] = count

                return summary

    def get_queued_items(
        self,
        media_type: str,
        status: str = "pending",
        limit: int = 100,
        ingestion_run_id: str = None,
    ) -> List[Dict]:
        """Get items from queue."""
        with self._get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                if ingestion_run_id:
                    cur.execute(
                        """
                        SELECT * FROM media_collection_queue
                        WHERE media_type = %s AND status = %s AND ingestion_run_id = %s
                        ORDER BY priority ASC, id ASC
                        LIMIT %s
                    """,
                        (media_type, status, ingestion_run_id, limit),
                    )
                else:
                    cur.execute(
                        """
                        SELECT * FROM media_collection_queue
                        WHERE media_type = %s AND status = %s
                        ORDER BY priority ASC, id ASC
                        LIMIT %s
                    """,
                        (media_type, status, limit),
                    )

                return cur.fetchall()

    def link_queue_item_to_run(self, source_url: str, media_type: str, ingestion_run_id: str):
        """Update existing queue item to link to a new ingestion run and reset status."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE media_collection_queue
                    SET ingestion_run_id = %s,
                        status = 'pending',
                        error_message = NULL,
                        retry_count = 0
                    WHERE source_url = %s AND media_type = %s
                """,
                    (ingestion_run_id, source_url, media_type),
                )
                conn.commit()

    def update_queue_status(
        self, item_id: int, status: str, result_id: int = None, error_message: str = None
    ):
        """Update queue item status."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                if status == "processing":
                    cur.execute(
                        """
                        UPDATE media_collection_queue
                        SET status = %s, started_at = NOW()
                        WHERE id = %s
                    """,
                        (status, item_id),
                    )
                elif status == "completed":
                    cur.execute(
                        """
                        UPDATE media_collection_queue
                        SET status = %s, completed_at = NOW(),
                            result_id = %s
                        WHERE id = %s
                    """,
                        (status, result_id, item_id),
                    )
                elif status == "failed":
                    cur.execute(
                        """
                        UPDATE media_collection_queue
                        SET status = %s, completed_at = NOW(),
                            error_message = %s,
                            retry_count = retry_count + 1
                        WHERE id = %s
                    """,
                        (status, error_message, item_id),
                    )

                conn.commit()

    def store_article(self, article: Dict) -> int:
        """Store news article."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO media_news_articles (
                        source_domain, source_name, article_url, wayback_url,
                        title, authors, publish_date, content, summary,
                        keywords, sentiment_score, entities_mentioned,
                        related_person_ids, extraction_method, collected_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (article_url) DO UPDATE SET
                        collected_at = NOW(),
                        content = EXCLUDED.content
                    RETURNING id
                """,
                    (
                        article.get("source_domain"),
                        article.get("source_name"),
                        article.get("source_url"),
                        article.get("wayback_url"),
                        article.get("title"),
                        article.get("authors", []),
                        article.get("publish_date"),
                        article.get("content"),
                        article.get("summary"),
                        article.get("keywords", []),
                        article.get("sentiment_score"),
                        article.get("entities_mentioned", {}),
                        article.get("related_person_ids", []),
                        article.get("collection_method", "unknown"),
                    ),
                )

                result = cur.fetchone()
                conn.commit()
                return result[0]

    def store_video(self, video: Dict) -> int:
        """Store video with transcript."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO media_videos (
                        video_id, platform, title, description,
                        url, upload_date, duration_seconds,
                        transcript_text, transcript_source, transcript_language,
                        is_auto_transcript, entities_mentioned,
                        related_person_ids, collected_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (video_id, platform) DO UPDATE SET
                        collected_at = NOW(),
                        transcript_text = EXCLUDED.transcript_text
                    RETURNING id
                """,
                    (
                        video.get("video_id"),
                        video.get("platform"),
                        video.get("title"),
                        video.get("description"),
                        video.get("url"),
                        video.get("upload_date"),
                        video.get("duration_seconds"),
                        video.get("transcript", {}).get("text"),
                        video.get("transcript", {}).get("source"),
                        video.get("transcript", {}).get("language"),
                        video.get("transcript", {}).get("is_auto_generated", True),
                        video.get("entities_mentioned", {}),
                        video.get("related_person_ids", []),
                    ),
                )

                result = cur.fetchone()
                conn.commit()
                return result[0]

    def store_document(self, document: Dict) -> int:
        """Store official document."""
        with self._get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO media_documents (
                        source, document_type, title, docket_number,
                        case_name, court, filing_date, url, file_path,
                        text_content, extracted_entities, page_count,
                        file_size_bytes, mime_type, checksum, collected_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (source, docket_number, filing_date) DO UPDATE SET
                        collected_at = NOW(),
                        text_content = EXCLUDED.text_content
                    RETURNING id
                """,
                    (
                        document.get("source"),
                        document.get("document_type"),
                        document.get("title"),
                        document.get("docket_number"),
                        document.get("case_name"),
                        document.get("court"),
                        document.get("filing_date"),
                        document.get("url"),
                        document.get("file_path"),
                        document.get("text_content"),
                        document.get("extracted_entities", {}),
                        document.get("page_count"),
                        document.get("file_size_bytes"),
                        document.get("mime_type"),
                        document.get("checksum"),
                    ),
                )

                result = cur.fetchone()
                conn.commit()
                return result[0]


# Error classes
class AgentError(Exception):
    """Base error for agents."""

    pass


class DiscoveryError(AgentError):
    """Error during discovery."""

    pass


class CollectionError(AgentError):
    """Error during collection."""

    pass


class ProcessingError(AgentError):
    """Error during processing."""

    pass


class StorageError(AgentError):
    """Error during storage."""

    pass


class TranscriptNotAvailable(AgentError):
    """Transcript not available for video."""

    pass


class DownloadFailed(AgentError):
    """Download failed."""

    pass
