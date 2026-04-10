# News Data Acquisition Implementation Plan

> **Phase 21 Implementation Document**  
> **Created:** April 4, 2026  
> **Status:** Planning Phase

---

## Executive Summary

**Goal:** Acquire historical news coverage of Epstein case (1990-2025) using free APIs and open-source tools.

**Approach:** Leverage existing GitHub projects to avoid reinventing the wheel

**Expected Outcome:** 50,000-250,000 news articles in PostgreSQL with entity cross-references

---

## Tools & Sources Selected

### Tier 1: Primary Data Sources (FREE)

| Source | Tool | Records | Use Case |
|--------|------|---------|----------|
| **GDELT Project** | gdeltPyR | 100M+ events | Bulk discovery of Epstein mentions |
| **Wayback Machine** | wayback-machine-downloader | 916B+ pages | Recover deleted news articles |
| **Internet Archive** | waybackpy | 800B+ pages | Programmatic access to snapshots |

### Tier 2: Supporting Tools (FREE)

| Tool | Purpose | GitHub URL |
|------|---------|------------|
| **newspaper3k** | Article text extraction | https://github.com/codelucas/newspaper |
| **gdelt-doc-api** | GDELT API client | https://github.com/alex9smith/gdelt-doc-api |
| **news-please** | Recursive news crawler | https://github.com/fhamborg/news-please |
| **feedparser** | RSS feed parsing | https://github.com/kurtmckee/feedparser |

---

## Implementation Phases

### Phase 21A: GDELT Discovery (Days 1-3)

**Objective:** Find all news events mentioning Epstein 1990-2025

**Steps:**
1. Clone gdeltPyR repository
2. Query GDELT Event Database for:
   - Actor mentions: "Epstein", "Maxwell", "Virginia Giuffre"
   - Date range: 1990-01-01 to 2025-12-31
   - Event codes: Media mentions, legal proceedings, etc.
3. Extract URLs from GDELT GKG (Global Knowledge Graph)
4. Store raw data in staging table

**Output:** `news_gdelt_raw` table with URLs and metadata

---

### Phase 21B: Wayback Recovery (Days 4-7)

**Objective:** Download full article HTML from archived sources

**Target News Domains:**
- CNN (cnn.com) - 24/7 coverage
- New York Times (nytimes.com) - Investigative pieces
- Washington Post (washingtonpost.com) - Breaking news
- BBC (bbc.com) - International coverage
- The Guardian (theguardian.com) - UK perspective
- Miami Herald - "Perversion of Justice" series
- Vanity Fair - Early profiles

**Steps:**
1. Install wayback-machine-downloader
2. Generate search patterns for each domain
3. Download Epstein-related snapshots
4. Organize by domain and date
5. Store in: `/home/cbwinslow/workspace/epstein-data/news-html/`

**Output:** Raw HTML files organized by source and date

---

### Phase 21C: Text Extraction (Days 8-10)

**Objective:** Parse HTML into clean article text

**Tools:**
- **newspaper3k** - Primary extractor
- **news-please** - Fallback for complex layouts

**Extraction Fields:**
- title (article headline)
- authors (array of bylines)
- publish_date (publication date)
- text (full article content)
- summary (auto-generated summary)
- keywords (extracted topics)
- top_image (featured image URL)

**Steps:**
1. Process all HTML files
2. Extract structured data
3. Validate extractions (non-empty title, text length > 500 chars)
4. Cross-reference with our person database
5. Load to `news_articles` table

**Output:** Clean article records in PostgreSQL

---

### Phase 21D: Analysis Integration (Days 11-14)

**Objective:** Build analysis views and cross-references

**SQL Views to Create:**
1. `v_news_person_mentions` - Articles mentioning each person
2. `v_news_timeline` - Coverage volume by date
3. `v_news_source_breakdown` - Articles by news outlet
4. `v_news_sentiment_over_time` - Sentiment tracking
5. `v_news_flight_correlation` - Articles near flight dates

**Cross-Reference Strategy:**
- Match article text against `exposed_persons` names
- Link to `exposed_flights` by date proximity
- Connect to `exposed_locations` by mentions
- Associate with `exposed_organizations` by coverage

---

## Database Schema

### Table: news_articles

```sql
CREATE TABLE news_articles (
    id SERIAL PRIMARY KEY,
    
    -- Source information
    source_domain VARCHAR(100) NOT NULL,  -- cnn.com
    source_name VARCHAR(100),              -- CNN
    source_category VARCHAR(50),           -- mainstream, investigative, tabloid
    
    -- Article metadata
    article_url TEXT NOT NULL,
    wayback_url TEXT,                      -- Archive.org snapshot
    title TEXT NOT NULL,
    authors TEXT[],
    publish_date DATE,
    publish_timestamp TIMESTAMP,
    
    -- Content
    content TEXT,                          -- Full article text
    summary TEXT,                          -- Auto summary
    keywords TEXT[],
    word_count INTEGER,
    
    -- Analysis
    sentiment_score FLOAT,                 -- -1.0 to 1.0
    subjectivity_score FLOAT,              -- 0.0 to 1.0
    
    -- Cross-references
    entities_mentioned JSONB,              -- {persons: [], locations: []}
    related_person_ids INTEGER[],          -- FK to exposed_persons
    
    -- Source tracking
    gdelt_event_id BIGINT,                 -- Link to GDELT
    extraction_method VARCHAR(50),           -- newspaper3k, news-please
    extraction_confidence FLOAT,
    
    -- Timestamps
    extracted_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_news_articles_date ON news_articles(publish_date);
CREATE INDEX idx_news_articles_source ON news_articles(source_domain);
CREATE INDEX idx_news_articles_wayback ON news_articles(wayback_url);
CREATE INDEX idx_news_entities ON news_articles USING GIN(entities_mentioned);
```

### Table: news_gdelt_raw (Staging)

```sql
CREATE TABLE news_gdelt_raw (
    id SERIAL PRIMARY KEY,
    
    -- GDELT Event fields
    event_id BIGINT,
    event_date DATE,
    event_month INTEGER,
    event_year INTEGER,
    
    -- Actors
    actor1_code VARCHAR(50),
    actor1_name VARCHAR(255),
    actor1_country VARCHAR(3),
    actor1_type VARCHAR(50),
    
    actor2_code VARCHAR(50),
    actor2_name VARCHAR(255),
    actor2_country VARCHAR(3),
    actor2_type VARCHAR(50),
    
    -- Event details
    event_code VARCHAR(10),
    event_base_code VARCHAR(10),
    event_root_code VARCHAR(10),
    quad_class INTEGER,
    goldstein_scale FLOAT,
    
    -- Mentions
    num_mentions INTEGER,
    num_sources INTEGER,
    num_articles INTEGER,
    avg_tone FLOAT,
    
    -- Source URLs
    source_url TEXT,
    document_source VARCHAR(100),
    
    -- Timestamps
    imported_at TIMESTAMP DEFAULT NOW()
);
```

---

## Expected Data Volume

### Conservative Estimate
- **Articles:** 50,000-75,000
- **Storage (HTML):** 5-10 GB
- **Storage (PostgreSQL):** 1-2 GB
- **Time to collect:** 7-10 days

### Optimistic Estimate
- **Articles:** 200,000-300,000
- **Storage (HTML):** 20-30 GB
- **Storage (PostgreSQL):** 5-8 GB
- **Time to collect:** 14-21 days

---

## Reuse Strategy

### Projects to Clone/Modify

| Priority | Project | Modification |
|----------|---------|--------------|
| **P0** | gdeltPyR | Add Epstein keyword filters |
| **P0** | wayback-machine-downloader | Add news domain list |
| **P1** | newspaper3k | Integrate with our DB schema |
| **P1** | news-please | Add PostgreSQL export option |
| **P2** | gdelt-doc-api | Build article URL discovery |

### Custom Scripts to Create

1. **scripts/news_gdelt_query.py** - Query GDELT for Epstein data
2. **scripts/news_wayback_download.py** - Bulk Wayback downloads
3. **scripts/news_extract_text.py** - Text extraction pipeline
4. **scripts/news_load_postgres.py** - Database loader
5. **scripts/news_entity_link.py** - Cross-reference with our entities

---

## Research Paper Applications

### Analysis Possibilities

1. **Timeline Analysis**
   - Coverage volume over time
   - Major story peaks (2008 plea, 2019 arrest, 2024 releases)

2. **Source Analysis**
   - Coverage by outlet type
   - Investigative vs breaking news ratio
   - Geographic coverage patterns

3. **Sentiment Tracking**
   - Tone shift from "socialite" to "sex offender"
   - Post-conviction vs pre-conviction coverage
   - Political bias analysis

4. **Entity Co-occurrence**
   - Which persons appear together in articles
   - Network effects in media coverage
   - Breakout vs buried stories

5. **Coverage Gaps**
   - Missing periods or topics
   - Under-covered aspects
   - Delayed reporting analysis

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Total articles collected | 50,000+ |
| Unique news sources | 50+ |
| Date range coverage | 1990-2025 |
| Person mentions cross-referenced | 100% of exposed_persons |
| Extraction success rate | >90% |
| Full text available | >85% |

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Wayback 404s | Use multiple snapshots, fallback to GDELT URLs |
| Paywalls | Only use Wayback archived versions (pre-paywall) |
| Extraction failures | Multiple extractors (newspaper3k → news-please) |
| Rate limits | Respect limits, add delays, cache results |
| Storage limits | Monitor RAID space, compress HTML after extraction |

---

## Next Immediate Actions

1. ⏳ **Clone gdeltPyR** and test basic query
2. ⏳ **Install wayback-machine-downloader** (requires Ruby)
3. ⏳ **Test newspaper3k** on single CNN article
4. ⏳ **Create database tables** for news data
5. ⏳ **Wait for ICIJ import completion** (95%+ done)

---

## Integration with Phase 20

This Phase 21 builds on Phase 20's enterprise architecture:
- Uses same naming conventions
- Follows PostgreSQL best practices
- Creates validation views
- Documents all acquisition methods
- Maintains data provenance

---

*Document created as part of Epstein Files Analysis Project*  
*Phase 21: News Data Acquisition*
