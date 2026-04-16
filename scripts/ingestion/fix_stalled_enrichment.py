#!/usr/bin/env python3
"""
Fix stalled enrichment - re-process articles with short/no content.
Addresses the issue where only 4/9283 articles have meaningful content.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Optional, List, Dict
from urllib.parse import urlparse

import asyncpg
import httpx
import structlog
from tenacity import retry, stop_after_attempt, wait_exponential
from trafilatura import fetch_url, extract

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Database connection
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Request configuration
CONCURRENT_REQUESTS = 5
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3


class EnrichmentFixer:
    """Fix stalled enrichment by re-processing articles with short content."""
    
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None
        self.semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)
        self.stats = {
            "processed": 0,
            "succeeded": 0,
            "failed": 0,
            "paywalled": 0,
            "no_change": 0,
            "improved": 0,
        }
    
    async def init(self):
        """Initialize database pool."""
        self.pool = await asyncpg.create_pool(DB_URL, min_size=5, max_size=20)
        logger.info("Database pool initialized")
    
    async def close(self):
        """Close database pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database pool closed")
    
    async def get_stalled_articles(self, batch_size: int = 100) -> List[asyncpg.Record]:
        """Get articles with short or no content."""
        async with self.pool.acquire() as conn:
            # Get articles with NULL content OR content < 100 chars
            rows = await conn.fetch(
                """
                SELECT id, article_url, title, content, word_count, 
                       all_topics, published_date, source_domain
                FROM media_news_articles
                WHERE word_count IS NULL 
                   OR word_count < 100
                   OR content IS NULL
                   OR LENGTH(TRIM(content)) < 100
                ORDER BY published_date DESC NULLS LAST
                LIMIT $1
                """,
                batch_size
            )
            return rows
    
    def detect_paywall(self, html: str, extracted_text: str) -> str:
        """Detect if content is behind paywall."""
        indicators = [
            "subscribe", "subscription", "paywall", "premium",
            "sign up to read", "create account", "register to continue",
            "you have reached your limit", "upgrade to continue"
        ]
        
        html_lower = html.lower()
        for indicator in indicators:
            if indicator in html_lower:
                return "paywalled"
        
        # Check if extracted text is very short vs expected
        if len(extracted_text) < 200 and len(html) > 5000:
            return "likely_paywalled"
        
        return "free"
    
    @retry(stop=stop_after_attempt(RETRY_ATTEMPTS), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def extract_with_trafilatura(self, url: str) -> Optional[Dict]:
        """Extract article content using Trafilatura."""
        try:
            # Fetch with timeout
            downloaded = await asyncio.wait_for(
                asyncio.to_thread(fetch_url, url),
                timeout=REQUEST_TIMEOUT
            )
            
            if not downloaded:
                return None
            
            # Extract with metadata
            result = await asyncio.to_thread(
                extract,
                downloaded,
                output_format='json',
                include_comments=False,
                include_tables=True,
                include_images=True,
                include_links=True,
                url=url,
                with_metadata=True
            )
            
            if not result:
                return None
            
            data = json.loads(result)
            content = data.get('text', '') or data.get('raw_text', '')
            
            # Detect paywall status
            paywall_status = self.detect_paywall(downloaded, content)
            
            return {
                'content': content,
                'title': data.get('title'),
                'author': data.get('author'),
                'publish_date': data.get('date'),
                'description': data.get('description'),
                'word_count': len(content.split()) if content else 0,
                'language': data.get('language', 'en'),
                'fingerprint': data.get('fingerprint'),
                'hostname': data.get('hostname'),
                'image_url': data.get('image'),
                'sitename': data.get('sitename'),
                'paywall_status': paywall_status,
                'extraction_method': 'trafilatura_v2',
            }
            
        except asyncio.TimeoutError:
            logger.warning("Request timeout", url=url)
            return None
        except Exception as e:
            logger.error("Extraction error", url=url, error=str(e))
            return None
    
    async def process_article(self, article: asyncpg.Record) -> bool:
        """Process a single article."""
        async with self.semaphore:
            article_id = article['id']
            url = article['article_url']
            
            logger.info("Processing article", article_id=str(article_id), url=url)
            
            try:
                # Extract content
                extracted = await self.extract_with_trafilatura(url)
                
                if not extracted:
                    await self.mark_failed(article_id, "extraction_failed")
                    self.stats["failed"] += 1
                    return False
                
                # Check if we got better content
                old_word_count = article['word_count'] or 0
                new_word_count = extracted['word_count']
                
                if new_word_count <= old_word_count:
                    logger.info("No improvement", article_id=str(article_id), 
                               old_words=old_word_count, new_words=new_word_count)
                    self.stats["no_change"] += 1
                    return False
                
                # Update database
                await self.update_article(article_id, extracted)
                
                self.stats["succeeded"] += 1
                self.stats["improved"] += 1
                
                logger.info("Article improved", 
                           article_id=str(article_id),
                           old_words=old_word_count,
                           new_words=new_word_count)
                
                return True
                
            except Exception as e:
                logger.error("Processing error", article_id=str(article_id), error=str(e))
                self.stats["failed"] += 1
                return False
    
    async def update_article(self, article_id: int, data: Dict) -> None:
        """Update article with extracted data."""
        async with self.pool.acquire() as conn:
            # Merge with existing all_topics
            existing = await conn.fetchval(
                "SELECT all_topics FROM media_news_articles WHERE id = $1",
                article_id
            )
            
            existing_topics = json.loads(existing) if existing else {}
            
            # Merge topics
            merged_topics = {
                **existing_topics,
                'extraction_method': data.get('extraction_method', 'trafilatura_v2'),
                'extraction_timestamp': datetime.now().isoformat(),
                'fingerprint': data.get('fingerprint'),
                'hostname': data.get('hostname'),
                'image_url': data.get('image_url'),
                'sitename': data.get('sitename'),
                'paywall_status': data.get('paywall_status'),
            }
            
            await conn.execute(
                """
                UPDATE media_news_articles
                SET content = $1,
                    title = COALESCE($2, title),
                    author = COALESCE($3, author),
                    published_date = COALESCE($4, published_date),
                    description = COALESCE($5, description),
                    word_count = $6,
                    language = COALESCE($7, language),
                    all_topics = $8,
                    updated_at = NOW()
                WHERE id = $9
                """,
                data['content'],
                data['title'],
                data['author'],
                data['publish_date'],
                data['description'],
                data['word_count'],
                data['language'],
                json.dumps(merged_topics),
                article_id
            )
    
    async def mark_failed(self, article_id: int, reason: str) -> None:
        """Mark article as failed."""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE media_news_articles
                SET all_topics = COALESCE(all_topics, '{}'::jsonb) || jsonb_build_object('enrichment_error', $1)
                WHERE id = $2
                """,
                reason,
                article_id
            )
    
    async def run(self, batch_size: int = 100, max_batches: Optional[int] = None):
        """Run the enrichment fix."""
        await self.init()
        
        try:
            batch_num = 0
            while True:
                batch_num += 1
                if max_batches and batch_num > max_batches:
                    break
                
                # Get batch of stalled articles
                articles = await self.get_stalled_articles(batch_size)
                
                if not articles:
                    logger.info("No more stalled articles")
                    break
                
                logger.info(f"Processing batch {batch_num}: {len(articles)} articles")
                
                # Process concurrently
                tasks = [self.process_article(article) for article in articles]
                await asyncio.gather(*tasks, return_exceptions=True)
                
                self.stats["processed"] += len(articles)
                
                # Log progress
                logger.info("Batch complete", batch=batch_num, stats=self.stats)
                
                # Small delay between batches
                await asyncio.sleep(2)
            
            # Final stats
            logger.info("Enrichment fix complete", final_stats=self.stats)
            
        finally:
            await self.close()


async def main():
    """Main entry point."""
    fixer = EnrichmentFixer()
    
    # Process in batches of 100
    await fixer.run(batch_size=100, max_batches=None)


if __name__ == "__main__":
    asyncio.run(main())
