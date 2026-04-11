#!/usr/bin/env python3
"""
Enhanced Article Ingestion Pipeline
Extracts rich metadata from news articles and stores in database.
"""

import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

import aiohttp
import psycopg2
from bs4 import BeautifulSoup

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ArticleMetadataExtractor:
    """Extract comprehensive metadata from article HTML."""
    
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        )
        return self
    
    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()
    
    async def extract_from_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Extract rich metadata from article URL."""
        try:
            logger.info(f"Extracting metadata from: {url}")
            
            async with self.session.get(url, ssl=False) as response:
                if response.status != 200:
                    logger.warning(f"HTTP {response.status} for {url}")
                    return None
                
                html = await response.text()
                headers = dict(response.headers)
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract content first for analysis
                content = self._extract_content(soup)
                title = self._extract_title(soup) or ''
                source_type = self._classify_source(url)
                authors = self._extract_authors(soup)
                pub_date = self._extract_publication_date(soup)
                
                # Perform enhanced analysis
                sentiment_analysis = self._analyze_sentiment(content)
                readability = self._calculate_readability(content)
                entities = self._extract_entities(content, title)
                credibility = self._assess_credibility(source_type, bool(authors), bool(pub_date))
                
                # Extract all metadata
                metadata = {
                    # Core content
                    'url': url,
                    'canonical_url': self._get_canonical_url(soup, url),
                    'title': self._extract_title(soup),
                    'subtitle': self._extract_subtitle(soup),
                    'content': self._extract_content(soup),
                    'content_summary': self._generate_summary(soup),
                    
                    # Authors
                    'authors': self._extract_authors(soup),
                    'author_emails': self._extract_author_emails(soup, html),
                    'author_twitter_handles': self._extract_twitter_handles(html),
                    'byline': self._extract_byline(soup),
                    
                    # Publication info
                    'source_domain': urlparse(url).netloc,
                    'source_name': self._extract_source_name(soup, url),
                    'source_type': self._classify_source(url),
                    'publication_name': self._extract_publication_name(soup),
                    'publication_date': self._extract_publication_date(soup),
                    'publication_modified_date': self._extract_modified_date(soup),
                    
                    # Network metadata
                    'ip_address': None,  # Would need separate lookup
                    'server_location': None,
                    'hosting_provider': headers.get('Server'),
                    'cdn_provider': self._detect_cdn(headers),
                    
                    # Content metrics
                    'word_count': self._count_words(soup),
                    'char_count': len(self._extract_content(soup) or ''),
                    'reading_time_minutes': self._estimate_reading_time(soup),
                    'readability_score': None,  # Would need calculation
                    
                    # Classification
                    'language': self._detect_language(soup) or 'en',
                    'topics': self._extract_topics(soup),
                    'categories': self._extract_categories(soup),
                    'tags': self._extract_tags(soup),
                    'keywords': self._extract_keywords(soup),
                    
                    # Technical
                    'extraction_method': 'rich_metadata_extractor_v1',
                    'http_status_code': response.status,
                    'content_type': headers.get('Content-Type'),
                    'charset': self._extract_charset(headers.get('Content-Type', '')),
                    
                    # Raw data
                    'raw_html': html[:100000],  # First 100KB
                    'raw_html_hash': hashlib.sha256(html.encode()).hexdigest(),
                    'headers': json.dumps(dict(headers)),
                    
                    # Links
                    'outgoing_links': self._extract_links(soup, url),
                    'outgoing_link_count': len(self._extract_links(soup, url)),
                    
                    # Social
                    'social_share_count': self._extract_social_counts(soup),
                    
                    # Enhanced analysis
                    'sentiment_score': sentiment_analysis['score'],
                    'sentiment_label': sentiment_analysis['label'],
                    'readability_score': readability,
                    'entities_mentioned': entities,
                    'ip_address': self._extract_ip_address(url),
                    'archive_org_url': self._check_archive_org(url),
                    'image_urls': self._extract_images(soup, url),
                    
                    # Credibility assessment
                    'credibility_score': credibility['credibility_score'],
                    'fact_check_status': credibility['fact_check_status'],
                    'bias_indicator': credibility['bias_indicator'],
                }
                
                logger.info(f"✓ Extracted metadata for: {metadata['title'][:60]}...")
                return metadata
                
        except Exception as e:
            logger.error(f"Failed to extract from {url}: {e}")
            return None
    
    def _get_canonical_url(self, soup: BeautifulSoup, fallback: str) -> Optional[str]:
        """Extract canonical URL."""
        canonical = soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            return canonical['href']
        og_url = soup.find('meta', property='og:url')
        if og_url and og_url.get('content'):
            return og_url['content']
        return fallback
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract article title."""
        # Try various sources
        og_title = soup.find('meta', property='og:title')
        if og_title and og_title.get('content'):
            return og_title['content'].strip()
        
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title and twitter_title.get('content'):
            return twitter_title['content'].strip()
        
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        
        return None
    
    def _extract_subtitle(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract subtitle/deck."""
        # Common subtitle patterns
        selectors = [
            'h2.subtitle', 'h2.deck', '.subtitle', '.deck',
            'p.lead', '.lead', '.summary', '.excerpt'
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        return None
    
    def _extract_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract main article content."""
        # Try article tag first
        article = soup.find('article')
        if article:
            # Remove script and style elements
            for script in article.find_all(['script', 'style', 'nav', 'header', 'footer']):
                script.decompose()
            return article.get_text(separator='\n', strip=True)
        
        # Try common content selectors
        selectors = [
            '[role="main"]', 'main', '.content', '.article-content',
            '.post-content', '.entry-content', '#content'
        ]
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text(separator='\n', strip=True)
        
        # Fallback to all paragraphs
        paragraphs = soup.find_all('p')
        return '\n\n'.join(p.get_text().strip() for p in paragraphs if len(p.get_text()) > 50)
    
    def _generate_summary(self, soup: BeautifulSoup, max_length: int = 500) -> Optional[str]:
        """Generate content summary."""
        content = self._extract_content(soup)
        if not content:
            return None
        
        # Use meta description if available
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            return meta_desc['content'][:max_length]
        
        # Extract first meaningful paragraph
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if len(para) > 100:
                return para[:max_length]
        
        return content[:max_length] if content else None
    
    def _extract_authors(self, soup: BeautifulSoup) -> List[str]:
        """Extract article authors."""
        authors = []
        
        # Try various author metadata patterns
        selectors = [
            'meta[name="author"]', 'meta[property="article:author"]',
            '.author', '.byline-author', '[rel="author"]',
            '.writer', '.journalist'
        ]
        
        for selector in selectors:
            elems = soup.select(selector)
            for elem in elems:
                if elem.name == 'meta':
                    author = elem.get('content')
                else:
                    author = elem.get_text().strip()
                
                if author and author not in authors:
                    # Clean up author name
                    author = re.sub(r'^(By|by)\s+', '', author)
                    authors.append(author)
        
        return authors if authors else None
    
    def _extract_author_emails(self, soup: BeautifulSoup, html: str) -> List[str]:
        """Extract author emails."""
        emails = []
        # Regex pattern for emails
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        matches = re.findall(pattern, html)
        for email in matches[:5]:  # Limit to first 5
            if email not in emails:
                emails.append(email)
        return emails if emails else None
    
    def _extract_twitter_handles(self, html: str) -> List[str]:
        """Extract Twitter handles."""
        handles = []
        pattern = r'@([a-zA-Z0-9_]{1,15})'
        matches = re.findall(pattern, html)
        for handle in matches[:5]:
            if handle not in handles:
                handles.append(handle)
        return handles if handles else None
    
    def _extract_byline(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract byline text."""
        byline_selectors = ['.byline', '.attribution', '.author-line']
        for selector in byline_selectors:
            elem = soup.select_one(selector)
            if elem:
                return elem.get_text().strip()
        return None
    
    def _extract_source_name(self, soup: BeautifulSoup, url: str) -> Optional[str]:
        """Extract publication source name."""
        # Try OpenGraph site name
        og_site = soup.find('meta', property='og:site_name')
        if og_site and og_site.get('content'):
            return og_site['content']
        
        # Try publisher
        publisher = soup.find('meta', attrs={'name': 'publisher'})
        if publisher and publisher.get('content'):
            return publisher['content']
        
        # Extract from domain
        domain = urlparse(url).netloc
        return domain.replace('www.', '').split('.')[0].title()
    
    def _classify_source(self, url: str) -> str:
        """Classify source type."""
        domain = urlparse(url).netloc.lower()
        
        # Government domains
        if domain.endswith('.gov') or domain.endswith('.gov.uk'):
            return 'government'
        
        # Academic
        if domain.endswith('.edu') or 'university' in domain:
            return 'academic'
        
        # News organizations
        news_domains = ['nytimes.com', 'washingtonpost.com', 'cnn.com', 'bbc.com',
                       'reuters.com', 'ap.org', 'bloomberg.com', 'wsj.com']
        if any(nd in domain for nd in news_domains):
            return 'mainstream'
        
        return 'independent'
    
    def _extract_publication_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract publication name."""
        # Try various metadata sources
        sources = [
            soup.find('meta', property='og:site_name'),
            soup.find('meta', attrs={'name': 'application-name'}),
            soup.find('meta', attrs={'name': 'publisher'})
        ]
        for source in sources:
            if source and source.get('content'):
                return source['content']
        return None
    
    def _extract_publication_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract publication date."""
        date_sources = [
            soup.find('meta', property='article:published_time'),
            soup.find('meta', property='datePublished'),
            soup.find('meta', attrs={'name': 'date'}),
            soup.find('time', attrs={'datetime': True}),
            soup.find('time', class_=re.compile(r'date|published'))
        ]
        
        for source in date_sources:
            if source:
                date_str = source.get('content') or source.get('datetime') or source.get_text()
                if date_str:
                    try:
                        # Try parsing various date formats
                        return self._parse_date(date_str)
                    except:
                        continue
        return None
    
    def _extract_modified_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extract modified date."""
        modified = soup.find('meta', property='article:modified_time')
        if modified and modified.get('content'):
            try:
                return self._parse_date(modified['content'])
            except:
                pass
        return None
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats."""
        formats = [
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d',
            '%B %d, %Y',
            '%b %d, %Y',
            '%d %B %Y',
            '%d %b %Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except:
                continue
        return None
    
    def _detect_cdn(self, headers: Dict) -> Optional[str]:
        """Detect CDN provider from headers."""
        server = headers.get('Server', '')
        via = headers.get('Via', '')
        
        cdns = {
            'cloudflare': 'Cloudflare',
            'fastly': 'Fastly',
            'akamai': 'Akamai',
            'cloudfront': 'AWS CloudFront',
            'maxcdn': 'MaxCDN'
        }
        
        header_str = f"{server} {via}".lower()
        for key, name in cdns.items():
            if key in header_str:
                return name
        return None
    
    def _count_words(self, soup: BeautifulSoup) -> int:
        """Count words in article."""
        content = self._extract_content(soup)
        if not content:
            return 0
        return len(content.split())
    
    def _estimate_reading_time(self, soup: BeautifulSoup) -> int:
        """Estimate reading time in minutes."""
        word_count = self._count_words(soup)
        # Average reading speed: 200 words per minute
        return max(1, word_count // 200)
    
    def _detect_language(self, soup: BeautifulSoup) -> Optional[str]:
        """Detect article language."""
        # Try HTML lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            return html_tag['lang'].split('-')[0]
        
        # Try meta tag
        meta_lang = soup.find('meta', attrs={'http-equiv': 'Content-Language'})
        if meta_lang and meta_lang.get('content'):
            return meta_lang['content'].split('-')[0]
        
        return 'en'
    
    def _extract_topics(self, soup: BeautifulSoup) -> List[str]:
        """Extract article topics."""
        topics = []
        
        # Try OpenGraph tags
        og_section = soup.find('meta', property='article:section')
        if og_section and og_section.get('content'):
            topics.append(og_section['content'])
        
        # Try meta keywords
        keywords_meta = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_meta and keywords_meta.get('content'):
            keywords = [k.strip() for k in keywords_meta['content'].split(',')]
            topics.extend(keywords[:10])
        
        return list(set(topics)) if topics else None
    
    def _extract_categories(self, soup: BeautifulSoup) -> List[str]:
        """Extract article categories."""
        return self._extract_topics(soup)  # Often same as topics
    
    def _extract_tags(self, soup: BeautifulSoup) -> List[str]:
        """Extract article tags."""
        tags = []
        
        # Try tag links
        tag_selectors = ['.tags a', '.tag', 'a[rel="tag"]']
        for selector in tag_selectors:
            elems = soup.select(selector)
            for elem in elems:
                tag = elem.get_text().strip()
                if tag and tag not in tags:
                    tags.append(tag)
        
        return tags if tags else None
    
    def _extract_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Extract keywords from meta tags."""
        keywords = []
        
        # Try meta keywords
        meta = soup.find('meta', attrs={'name': 'keywords'})
        if meta and meta.get('content'):
            keywords = [k.strip().lower() for k in meta['content'].split(',')]
        
        # Add from tags
        tags = self._extract_tags(soup) or []
        for tag in tags:
            if tag.lower() not in [k.lower() for k in keywords]:
                keywords.append(tag.lower())
        
        return keywords if keywords else None
    
    def _extract_charset(self, content_type: str) -> Optional[str]:
        """Extract charset from Content-Type header."""
        match = re.search(r'charset=([\w-]+)', content_type, re.IGNORECASE)
        return match.group(1) if match else None
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract outgoing links."""
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                domain = urlparse(base_url).scheme + '://' + urlparse(base_url).netloc
                links.append(domain + href)
        
        return list(set(links))[:100]  # Limit to 100 unique links
    
    def _extract_social_counts(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract social share counts."""
        counts = {}
        
        # Try to find share counts (usually in meta tags or specific elements)
        # Note: Most social counts require API access, this is a placeholder
        
        return counts if counts else None
    
    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Basic sentiment analysis based on keyword matching."""
        if not content:
            return {'score': 0, 'label': 'neutral'}
        
        positive_words = ['good', 'great', 'excellent', 'positive', 'success', 'victory', 'win', 'celebrate']
        negative_words = ['bad', 'terrible', 'awful', 'negative', 'fail', 'disaster', 'crisis', 'tragedy']
        
        content_lower = content.lower()
        pos_count = sum(1 for word in positive_words if word in content_lower)
        neg_count = sum(1 for word in negative_words if word in content_lower)
        
        total = pos_count + neg_count
        if total == 0:
            return {'score': 0, 'label': 'neutral'}
        
        score = (pos_count - neg_count) / total
        
        if score > 0.2:
            label = 'positive'
        elif score < -0.2:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {'score': round(score, 3), 'label': label}
    
    def _calculate_readability(self, content: str) -> Optional[float]:
        """Calculate Flesch-Kincaid readability score."""
        if not content:
            return None
        
        sentences = content.count('.') + content.count('!') + content.count('?')
        words = len(content.split())
        syllables = sum(self._count_syllables(word) for word in content.split())
        
        if sentences == 0 or words == 0:
            return None
        
        # Flesch Reading Ease score
        score = 206.835 - (1.015 * (words / sentences)) - (84.6 * (syllables / words))
        return round(score, 2)
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word."""
        word = word.lower()
        vowels = 'aeiouy'
        count = 0
        prev_was_vowel = False
        
        for char in word:
            if char in vowels:
                if not prev_was_vowel:
                    count += 1
                prev_was_vowel = True
            else:
                prev_was_vowel = False
        
        if word.endswith('e'):
            count -= 1
        
        return max(1, count)
    
    def _extract_ip_address(self, url: str) -> Optional[str]:
        """Extract IP address from URL (placeholder for DNS lookup)."""
        # Would need socket.gethostbyname() in actual implementation
        return None
    
    def _check_archive_org(self, url: str) -> Optional[str]:
        """Check if URL is archived on archive.org."""
        # Return a placeholder URL format
        timestamp = datetime.now().strftime('%Y%m%d')
        return f"https://web.archive.org/web/{timestamp}/{url}"
    
    def _assess_credibility(self, source_type: str, has_author: bool, has_date: bool) -> Dict[str, Any]:
        """Assess article credibility based on source characteristics."""
        score = 0.5  # Base score
        
        # Source type weighting
        if source_type == 'mainstream':
            score += 0.2
        elif source_type == 'government':
            score += 0.25
        elif source_type == 'academic':
            score += 0.3
        
        # Attribution quality
        if has_author:
            score += 0.15
        if has_date:
            score += 0.1
        
        score = min(1.0, score)
        
        return {
            'credibility_score': round(score, 2),
            'fact_check_status': 'unverified',
            'bias_indicator': 'unknown'
        }
    
    def _extract_entities(self, content: str, title: str) -> List[str]:
        """Extract named entities from content (basic implementation)."""
        if not content:
            return []
        
        # Combine title and first 1000 chars of content
        text = f"{title} {content[:1000]}"
        
        # Simple entity extraction based on capitalized words
        import re
        entities = set()
        
        # Find capitalized phrases (potential names)
        matches = re.findall(r'\b[A-Z][a-z]+ (?:[A-Z][a-z]+ )*[A-Z][a-z]+\b', text)
        for match in matches:
            if len(match) > 3:  # Filter out short matches
                entities.add(match)
        
        return list(entities)[:20]  # Return top 20
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract image URLs from article."""
        images = []
        
        for img in soup.find_all('img'):
            src = img.get('src')
            if src:
                if src.startswith('http'):
                    images.append(src)
                elif src.startswith('/'):
                    domain = urlparse(base_url).scheme + '://' + urlparse(base_url).netloc
                    images.append(domain + src)
                elif not src.startswith('data:'):
                    images.append(src)
        
        return list(set(images))[:10]  # Limit to 10 unique images


class ArticleIngestionPipeline:
    """Pipeline for ingesting articles with rich metadata."""
    
    def __init__(self, db_connection_string: str):
        self.db_connection_string = db_connection_string
    
    async def ingest_article(self, url: str, keywords_matched: List[str] = None, priority: int = 5, discovered_by: str = 'manual') -> Optional[int]:
        """Ingest a single article with full metadata."""
        
        async with ArticleMetadataExtractor() as extractor:
            # Extract metadata
            metadata = await extractor.extract_from_url(url)
            
            if not metadata:
                logger.error(f"Failed to extract metadata from {url}")
                return None
            
            # Add ingestion metadata
            metadata['keywords_matched'] = keywords_matched or []
            metadata['quality_score'] = self._calculate_quality_score(metadata)
            metadata['processing_status'] = 'collected'
            metadata['priority'] = priority
            metadata['discovered_by'] = discovered_by
            
            # Store in database
            article_id = await self._store_article(metadata)
            
            return article_id
    
    def _calculate_quality_score(self, metadata: Dict) -> float:
        """Calculate quality score for article."""
        score = 0.5  # Base score
        
        # Content length (0.2 max)
        word_count = metadata.get('word_count', 0)
        if word_count > 500:
            score += 0.2
        elif word_count > 200:
            score += 0.1
        
        # Has author (0.1 max)
        if metadata.get('authors'):
            score += 0.1
        
        # Has publication date (0.1 max)
        if metadata.get('publication_date'):
            score += 0.1
        
        # Has tags/categories (0.1 max)
        if metadata.get('tags') or metadata.get('categories'):
            score += 0.1
        
        return min(1.0, score)
    
    async def _store_article(self, metadata: Dict) -> Optional[int]:
        """Store article in database."""
        conn = psycopg2.connect(self.db_connection_string)
        
        try:
            with conn.cursor() as cur:
                # Build SQL query dynamically based on available fields
                fields = []
                values = []
                
                field_mapping = {
                    'url': 'url',
                    'canonical_url': 'canonical_url',
                    'title': 'title',
                    'subtitle': 'subtitle',
                    'content': 'content',
                    'content_summary': 'content_summary',
                    'authors': 'authors',
                    'author_emails': 'author_emails',
                    'author_twitter_handles': 'author_twitter_handles',
                    'byline': 'byline',
                    'source_domain': 'source_domain',
                    'source_name': 'source_name',
                    'source_type': 'source_type',
                    'publication_name': 'publication_name',
                    'publication_date': 'publication_date',
                    'publication_modified_date': 'publication_modified_date',
                    'word_count': 'word_count',
                    'reading_time_minutes': 'reading_time_minutes',
                    'language': 'language',
                    'topics': 'topics',
                    'categories': 'categories',
                    'tags': 'tags',
                    'keywords': 'keywords',
                    'keywords_matched': 'keywords_matched',
                    'extraction_method': 'extraction_method',
                    'http_status_code': 'http_status_code',
                    'raw_html_hash': 'raw_html_hash',
                    'outgoing_link_count': 'outgoing_link_count',
                    'social_share_count': 'social_share_count',
                    'quality_score': 'quality_score',
                    'processing_status': 'processing_status',
                    'metadata': 'metadata',
                    'priority': 'priority',
                    'discovered_by': 'discovered_by'
                }
                
                for json_key, db_field in field_mapping.items():
                    if json_key in metadata and metadata[json_key] is not None:
                        fields.append(db_field)
                        value = metadata[json_key]
                        
                        # Convert lists to PostgreSQL arrays
                        if isinstance(value, list):
                            value = value if value else None
                        
                        # Convert dicts to JSON
                        elif isinstance(value, dict):
                            value = json.dumps(value)
                        
                        # Convert datetime
                        elif isinstance(value, datetime):
                            value = value.isoformat()
                        
                        values.append(value)
                
                if not fields:
                    logger.error("No fields to insert")
                    return None
                
                # Build and execute query
                placeholders = ', '.join(['%s'] * len(fields))
                columns = ', '.join(fields)
                
                query = f"""
                    INSERT INTO media_news_articles ({columns})
                    VALUES ({placeholders})
                    ON CONFLICT (url) DO UPDATE SET
                        {', '.join([f"{f} = EXCLUDED.{f}" for f in fields if f != 'url'])},
                        updated_at = NOW()
                    RETURNING id
                """
                
                cur.execute(query, values)
                article_id = cur.fetchone()[0]
                conn.commit()
                
                logger.info(f"✓ Stored article ID {article_id}: {metadata.get('title', 'Unknown')[:60]}...")
                return article_id
                
        except Exception as e:
            logger.error(f"Failed to store article: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    async def ingest_articles_batch(self, urls: List[Dict[str, Any]]) -> Dict[str, int]:
        """Ingest multiple articles."""
        results = {
            'success': 0,
            'failed': 0,
            'total': len(urls)
        }
        
        for item in urls:
            url = item.get('url')
            keywords = item.get('keywords', [])
            
            article_id = await self.ingest_article(url, keywords)
            
            if article_id:
                results['success'] += 1
            else:
                results['failed'] += 1
        
        logger.info(f"Batch ingestion complete: {results['success']}/{results['total']} successful")
        return results


# Example usage
if __name__ == "__main__":
    import asyncio
    
    async def main():
        pipeline = ArticleIngestionPipeline(
            db_connection_string='postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
        )
        
        # Test with a single URL
        test_url = "https://en.wikipedia.org/wiki/Jeffrey_Epstein"
        
        article_id = await pipeline.ingest_article(
            url=test_url,
            keywords_matched=['Epstein', 'Wikipedia']
        )
        
        if article_id:
            print(f"✓ Successfully ingested article ID: {article_id}")
        else:
            print("✗ Failed to ingest article")
    
    asyncio.run(main())
