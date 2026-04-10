# News Ingestion System Analysis & Improvement Plan

## Current Status Assessment

### What We Successfully Achieved
✅ **149 articles** collected from 108 sources
✅ Database schema with comprehensive fields
✅ Primary key (id SERIAL PRIMARY KEY)
✅ Duplicate prevention (UNIQUE constraint on article_url)
✅ Basic metadata collection (title, authors, content, summary, keywords)
✅ Cross-reference fields (entities_mentioned, related_person_ids, etc.)

### Current Search Parameters
- **Keywords**: `['Jeffrey Epstein', 'Epstein', 'Ghislaine Maxwell', 'Virginia Giuffre']`
- **Date Range**: 2019-01-01 to 2025-12-31
- **Max Results**: 5,000 (configurable)
- **Discovery Methods**: RSS feeds only (GDELT and Wayback skipped due to rate limits)
- **Sources**: Limited to 7 RSS feeds (CNN, NYT, WaPo, BBC, Guardian, Reuters, AP)

### What's Missing (Industry Standard Gaps)

## 1. SEARCH EXHAUSTIVENESS - CRITICAL GAPS

### Current Issues:
- **Only 149 articles** for 6+ year span (2019-2025) is extremely low
- **RSS-only discovery** - misses 90%+ of news content
- **Limited sources** - only 7 major outlets
- **No international coverage** beyond English-speaking countries
- **No niche sources** (investigative journalism, legal blogs, academic papers)
- **No social media monitoring** (Twitter/X, Reddit, forums)
- **No press release monitoring**
- **No court document tracking**

### Industry Standard Approaches:

#### A. Multi-Source Discovery (Required)
```
✓ GDELT Project (global news monitoring - 100M+ articles)
✓ NewsAPI.org (aggregated news from 150K+ sources)
✓ Common Crawl (web archive - billions of pages)
✓ Wayback Machine (historical snapshots)
✓ RSS feeds (real-time updates)
✓ Google News API (search-based discovery)
✓ Bing News API (alternative search)
✓ Webhose.io (news monitoring service)
✓ LexisNexis (premium legal/news database)
✓ Factiva (Dow Jones news archive)
```

#### B. Expanded Keywords (Required)
Current: 4 keywords
Industry Standard: 50-100 keywords including:
- Names: Jeffrey Epstein, Ghislaine Maxwell, Virginia Giuffre, Sarah Ransome, 
  Maria Farmer, Annie Farmer, Jane Does 1-15+
- Locations: Little Saint James, Great St James, Palm Beach, Manhattan, 
  US Virgin Islands, Zorro Ranch, New Mexico
- Organizations: Mossack Fonseca, Epstein VI, Southern Trust, 
  Gratitude America, J Epstein & Co
- Legal terms: sex trafficking, sex offender, plea deal, non-prosecution agreement,
  Acosta, SDNY, civil lawsuit, criminal case
- Associated figures: Trump, Clinton, Prince Andrew, Alan Dershowitz, 
  Bill Gates, Leslie Wexner, Leon Black
- Case references: 1:08-cr-00808, 1:15-cv-07433, etc.

#### C. Temporal Coverage (Required)
- **Full historical span**: 1990-2026 (Epstein's entire public life)
- **Key periods**: 
  - 1990s: Early career
  - 2000s: First investigations
  - 2007: Plea deal
  - 2008-2019: Post-plea period
  - 2019: Arrest and death
  - 2019-2026: Aftermath, lawsuits, documentaries

#### D. Source Expansion (Required)
Current: 7 sources
Industry Standard: 500+ sources including:
- **Mainstream**: NYT, WaPo, WSJ, CNN, BBC, Reuters, AP, AFP
- **Investigative**: Miami Herald, Miami New Times, ProPublica, ICIJ, 
  BuzzFeed News, The Guardian US
- **Legal**: Law360, Bloomberg Law, Above the Law, SCOTUSblog
- **Business**: Forbes, Bloomberg, WSJ, Financial Times
- **Tabloids**: NY Post, Daily Mail, Sun, Mirror (for breaking news)
- **International**: El País (Spain), Le Monde (France), Der Spiegel (Germany),
  The Guardian UK, Sydney Morning Herald (Australia)
- **Local**: Palm Beach Post, Virgin Islands Daily News, Santa Fe New Mexican
- **Academic**: Law review articles, academic papers
- **Blogs**: Legal blogs, political blogs, independent journalists

## 2. DATA INGESTION QUALITY - CRITICAL GAPS

### Current Issues:
- **No author networking information** (author bios, affiliations, past articles)
- **No entity extraction** (NER not running)
- **No sentiment analysis** (field exists but not populated)
- **No topic classification** (field exists but not populated)
- **No relationship extraction** (who's connected to whom)
- **No fact-checking** (veracity scoring)
- **No language detection** (foreign language articles not processed)
- **No image extraction** (article images, charts, graphs)
- **No link extraction** (internal/external links for network analysis)
- **No citation tracking** (which articles cite which)

### Industry Standard Data Fields:

#### Required Additional Fields:
```sql
-- Author Information
author_bios JSONB,  -- {author_id: {bio, email, twitter, affiliation}}
author_affiliations TEXT[],  -- Organizations authors work for
author_contact_info JSONB,  -- Email, social media
author_history JSONB,  -- Previous articles by same author

-- Network Analysis
linked_articles INTEGER[],  -- Articles this article cites/links to
citing_articles INTEGER[],  -- Articles that cite this article
shared_entities INTEGER[],  -- Articles mentioning same entities
cluster_id INTEGER,  -- Story cluster for duplicate detection
canonical_article_id INTEGER,  -- If this is a duplicate/rewrite

-- Content Analysis
language_code VARCHAR(10),  -- ISO 639-1
translated_content TEXT,  -- Machine translation if needed
reading_time_seconds INTEGER,
flesch_kincaid_grade FLOAT,
complexity_score FLOAT,

-- Fact-checking
fact_check_status VARCHAR(50),  -- verified, disputed, unverified
fact_check_sources JSONB,
correction_notes TEXT,

-- Social Signals
social_media_shares JSONB,  -- {twitter: 1000, facebook: 500, reddit: 200}
viral_score FLOAT,
engagement_metrics JSONB,

-- Technical
http_status INTEGER,
response_time_ms INTEGER,
content_type VARCHAR(100),
charset VARCHAR(50),
last_modified TIMESTAMP,
etag VARCHAR(100),
```

## 3. EMBEDDINGS & SEMANTIC SEARCH - CRITICAL GAPS

### Current Status:
- ✅ Embedding infrastructure exists (nomic-embed-text-v2-moe)
- ❌ No embeddings generated for news articles
- ❌ No pgvector extension installed
- ❌ No semantic search capability

### Industry Standard Approach:

#### A. Embedding Strategy
```python
# Multi-level embeddings for different use cases:
1. Title Embeddings (768-dim) - Quick search, clustering
2. Summary Embeddings (768-dim) - Content overview
3. Content Chunks (768-dim, 512 tokens) - Detailed search
4. Entity Embeddings (768-dim) - Entity similarity
5. Author Embeddings (768-dim) - Author similarity
```

#### B. Required Infrastructure
```sql
-- Install pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding columns
ALTER TABLE media_news_articles 
ADD COLUMN title_embedding vector(768),
ADD COLUMN summary_embedding vector(768),
ADD COLUMN content_embedding vector(768);

-- Create indexes for vector search
CREATE INDEX idx_news_title_embedding 
ON media_news_articles USING ivfflat(title_embedding vector_cosine_ops);
CREATE INDEX idx_news_summary_embedding 
ON media_news_articles USING ivfflat(summary_embedding vector_cosine_ops);
CREATE INDEX idx_news_content_embedding 
ON media_news_articles USING ivfflat(content_embedding vector_cosine_ops);
```

#### C. Embedding Pipeline
```python
# Process:
1. Extract article content
2. Clean and normalize text
3. Generate title embedding
4. Generate summary embedding
5. Chunk content into 512-token segments
6. Generate embeddings for each chunk
7. Store in database with metadata
8. Update search indexes
```

## 4. DUPLICATE DETECTION - CRITICAL GAPS

### Current Status:
- ✅ URL-based deduplication (UNIQUE constraint)
- ❌ No content-based deduplication
- ❌ No near-duplicate detection (rewritten articles)
- ❌ No story clustering (same story from multiple sources)

### Industry Standard Approaches:

#### A. Multi-Level Deduplication
```python
1. URL Normalization (current)
   - Remove tracking parameters
   - Normalize http/https
   - Remove trailing slashes

2. Content Hashing (SHA-256)
   - Full article hash
   - Title hash
   - First paragraph hash

3. MinHash/LSH (near-duplicates)
   - Detect rewrites
   - Detect syndicated content
   - Detect translations

4. Semantic Clustering
   - Embedding-based clustering
   - Group same story from different sources
   - Identify canonical version

5. Temporal Deduplication
   - Detect updated articles
   - Track article versions
```

#### B. Required Schema Additions
```sql
ALTER TABLE media_news_articles 
ADD COLUMN content_hash VARCHAR(64),
ADD COLUMN title_hash VARCHAR(64),
ADD COLUMN cluster_id INTEGER,
ADD COLUMN canonical_article_id INTEGER,
ADD COLUMN is_duplicate BOOLEAN DEFAULT FALSE,
ADD COLUMN duplicate_reason VARCHAR(50),
ADD COLUMN similarity_score FLOAT;
```

## 5. ENTITY EXTRACTION & NETWORKING - CRITICAL GAPS

### Current Status:
- ✅ Schema has entities_mentioned JSONB field
- ✅ Schema has related_person_ids INTEGER[] field
- ❌ No NER running
- ❌ No entity linking to existing database
- ❌ No relationship extraction
- ❌ No network graph building

### Industry Standard Approach:

#### A. Entity Extraction Pipeline
```python
1. Named Entity Recognition (NER)
   - spaCy en_core_web_trf (transformer-based)
   - GLiNER zero-shot for custom entities
   - Custom regex patterns for case numbers, flight IDs

2. Entity Linking
   - Match to exposed_persons table
   - Match to organizations database
   - Match to locations database
   - Fuzzy matching for name variants

3. Relationship Extraction
   - Co-occurrence analysis
   - Dependency parsing (who did what to whom)
   - Temporal relationship extraction

4. Network Graph Building
   - Neo4j or PostgreSQL graph
   - Centrality metrics
   - Community detection
```

#### B. Required Processing
```python
# For each article:
1. Extract all entities (persons, orgs, locations, dates)
2. Link to existing database IDs
3. Extract relationships between entities
4. Store in entities_mentioned JSONB
5. Store related_person_ids INTEGER[]
6. Update media_entity_mentions table
7. Update knowledge graph
```

## 6. AUTHOR NETWORKING - CRITICAL GAPS

### Current Status:
- ✅ Authors stored as TEXT[]
- ❌ No author profiles
- ❌ No author affiliation tracking
- ❌ No author network analysis
- ❌ No author credibility scoring

### Industry Standard Approach:

#### A. Author Profile System
```sql
CREATE TABLE media_authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    twitter_handle VARCHAR(100),
    linkedin_url TEXT,
    affiliation VARCHAR(255),
    bio TEXT,
    beat VARCHAR(100),  -- e.g., "legal affairs", "politics"
    location VARCHAR(100),
    total_articles INTEGER DEFAULT 0,
    epstein_articles INTEGER DEFAULT 0,
    credibility_score FLOAT,  -- 0.0 to 1.0
    political_leaning VARCHAR(50),  -- left, center, right
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(name, email)
);

CREATE TABLE media_article_authors (
    article_id INTEGER REFERENCES media_news_articles(id),
    author_id INTEGER REFERENCES media_authors(id),
    author_role VARCHAR(50),  -- primary, co-author, contributor
    contribution_type VARCHAR(50),  -- reporting, analysis, opinion
    UNIQUE(article_id, author_id)
);
```

#### B. Author Network Analysis
```python
# Track:
1. Co-authorship networks
2. Source hopping (authors moving between outlets)
3. Citation networks (who cites whom)
4. Beat specialization
5. Credibility scoring based on accuracy
```

## 7. REAL-TIME MONITORING - CRITICAL GAPS

### Current Status:
- ❌ No real-time monitoring
- ❌ No alert system for breaking news
- ❌ No scheduled updates
- ❌ No change detection

### Industry Standard Approach:

#### A. Continuous Monitoring
```python
# Schedule:
1. RSS feeds: Every 15 minutes
2. NewsAPI: Every hour
3. GDELT: Every 6 hours
4. Social media: Real-time (Twitter API, Reddit API)
5. Court dockets: Daily (CourtListener API)

# Alert triggers:
1. New articles about key persons
2. Breaking news (viral articles)
3. New court filings
4. New documentary releases
5. New book releases
```

## RECOMMENDED IMPROVEMENT PLAN

### Phase 1: Immediate (Week 1)
1. ✅ Fix current ingestion bugs (DONE)
2. Expand keywords to 50+ terms
3. Add 100+ RSS feeds
4. Enable GDELT discovery (with rate limiting)
5. Add content-based deduplication
6. Install pgvector extension
7. Generate embeddings for existing 149 articles

### Phase 2: Short-term (Weeks 2-4)
1. Add NewsAPI.org integration
2. Implement NER pipeline (spaCy + GLiNER)
3. Add entity linking to exposed_persons
4. Build author profile system
5. Add sentiment analysis
6. Add topic classification
7. Implement near-duplicate detection

### Phase 3: Medium-term (Months 2-3)
1. Add Common Crawl integration
2. Add social media monitoring
3. Build real-time monitoring system
4. Add fact-checking integration
5. Build network graph visualization
5. Add multilingual support
6. Implement story clustering

### Phase 4: Long-term (Months 4-6)
1. Add LexisNexis/Factiva integration
2. Build ML-based duplicate detection
3. Add automated summarization
4. Build trend analysis dashboard
5. Add predictive analytics
6. Build API for external access

## ESTIMATED ARTICLE COUNTS

### Current: 149 articles (RSS only, 7 sources)
### Phase 1: 5,000-10,000 articles (expanded RSS + GDELT)
### Phase 2: 50,000-100,000 articles (NewsAPI + NER)
### Phase 3: 500,000+ articles (Common Crawl + social media)
### Phase 4: 1M+ articles (premium sources + full archive)

## TECHNICAL RECOMMENDATIONS

### 1. Database Schema
- Add pgvector extension for embeddings
- Add content_hash for deduplication
- Add author profile tables
- Add embedding columns
- Add fact-checking fields

### 2. Processing Pipeline
- Use Celery for async processing
- Use Redis for queue management
- Use GPU for embeddings (Tesla K80/K40m)
- Use GPU for NER (spaCy trf)
- Implement retry logic with exponential backoff

### 3. Storage
- Store raw HTML for reprocessing
- Store extracted images
- Store article versions
- Use compression for large text fields

### 4. API & Integration
- REST API for querying
- GraphQL for complex queries
- Webhook notifications for breaking news
- Scheduled jobs for monitoring
