# Database Migration System

## Overview

This migration system manages the database schema for the Epstein media acquisition project. It provides version-controlled schema changes with rollback support and migration tracking.

## Migration Files

### Location
All migration files are stored in:
```
scripts/migrations/
```

### Naming Convention
```
XXX_description.sql
```
Where:
- `XXX` = Sequential version number (001, 002, 003...)
- `description` = Brief description of the migration

### Current Migrations

| Version | File | Description |
|---------|------|-------------|
| 1.0.0 | `001_create_media_tables.sql` | Create all media acquisition tables with rich metadata |

## Usage

### Apply All Migrations
```bash
cd /home/cbwinslow/workspace/epstein
python scripts/apply_migrations.py
```

### Apply Specific Migration
```bash
python scripts/apply_migrations.py --version 001
```

### Check Migration Status
```bash
python scripts/apply_migrations.py --status
```

### Dry Run (Preview changes)
```bash
python scripts/apply_migrations.py --dry-run
```

## Database Schema

### Core Tables

#### media_collection_queue
Central queue for all media items pending processing.

**Key Fields:**
- `id`, `uuid` - Primary identifiers
- `media_type` - Type of media (news, video, document, audio)
- `source_url`, `canonical_url` - URLs
- `priority` - Processing priority (1-10)
- `status` - Current status (pending, processing, completed, failed, retry)
- `keywords_matched` - Keywords that triggered discovery
- `url_hash`, `content_hash` - SHA256 hashes for deduplication
- `metadata` - JSONB for flexible metadata

#### media_news_articles
Rich metadata storage for news articles.

**Content Fields:**
- `title`, `subtitle`, `content`, `content_cleaned`, `content_summary`
- `word_count`, `char_count`, `reading_time_minutes`, `readability_score`

**Attribution:**
- `authors`, `author_emails`, `author_twitter_handles`, `byline`
- `source_domain`, `source_name`, `source_type`, `publication_name`
- `publication_date`, `publication_modified_date`

**Network & Technical:**
- `ip_address`, `server_location`, `hosting_provider`, `cdn_provider`
- `http_status_code`, `content_type`, `charset`, `headers`

**Analysis:**
- `sentiment_score`, `sentiment_label`
- `language`, `topics`, `categories`, `tags`, `keywords`
- `credibility_score`, `fact_check_status`, `bias_indicator`

**Archival:**
- `archive_org_url`, `archive_date`
- `screenshot_path`, `pdf_path`
- `raw_html`, `raw_html_hash`

**Links & Social:**
- `outgoing_links`, `incoming_links`
- `social_share_count`, `comment_count`

**Full-Text Search:**
- `search_vector` - TSVECTOR for full-text search
- Automatically updated via trigger

#### media_videos
Rich metadata for video content.

**Platform & Identification:**
- `video_id`, `platform`, `url`, `embed_url`
- `channel_id`, `channel_name`, `uploader`

**Content:**
- `title`, `description`, `duration_seconds`, `duration_formatted`
- `transcript`, `transcript_available`, `transcript_source`

**Engagement:**
- `view_count`, `like_count`, `dislike_count`, `comment_count`, `share_count`

#### media_documents
Rich metadata for documents (PDFs, court filings, etc.).

**Document Info:**
- `doc_type`, `mime_type`, `file_format`
- `document_category` - legal_filing, court_order, indictment, etc.
- `legal_case_number`, `court_name`, `jurisdiction`

**OCR & Analysis:**
- `ocr_performed`, `ocr_engine`, `ocr_confidence`
- `redaction_count`, `redaction_analysis`

#### media_entities
Named entities (people, organizations, locations).

**Entity Fields:**
- `entity_name`, `normalized_name`, `entity_type`
- `aliases`, `name_variants`
- `description`, `wikipedia_url`, `wikidata_id`

#### media_entity_mentions
Links between entities and content.

### Views

#### vw_recent_articles
Recent articles with full metadata (last 30 days).

#### vw_content_by_domain
Statistics grouped by source domain.

#### vw_entity_mentions
Entity mention statistics across all content.

### Functions & Triggers

#### update_article_search_vector()
Automatically updates the full-text search vector when articles are inserted/updated.

#### update_entity_search_vector()
Automatically updates entity search vectors.

#### update_updated_at()
Automatically updates the `updated_at` timestamp on modifications.

## Schema Migrations Table

The `schema_migrations` table tracks applied migrations:

```sql
SELECT * FROM schema_migrations;
```

**Fields:**
- `version` - Migration version number
- `name` - Description
- `applied_at` - When it was applied
- `applied_by` - Who applied it
- `checksum` - File hash for integrity
- `execution_time_ms` - How long it took

## Indexes

### For Performance
- All primary keys automatically indexed
- Foreign key relationships indexed
- Frequently queried fields indexed
- Full-text search using GIN indexes
- Trigram indexes for fuzzy search

### For Full-Text Search
- `idx_articles_search` - Main article search
- `idx_articles_title_trgm` - Fuzzy title matching
- `idx_articles_content_trgm` - Fuzzy content matching
- `idx_entities_search` - Entity search

### For JSONB Queries
- `idx_queue_metadata` - Queue metadata queries
- `idx_articles_metadata` - Article metadata queries
- `idx_videos_metadata` - Video metadata queries

## Best Practices

### Adding New Migrations

1. Create new migration file with next version number
2. Include both `CREATE TABLE IF NOT EXISTS` and `DROP IF EXISTS` for views
3. Add indexes for new columns that will be queried
4. Update this README
5. Record migration in `schema_migrations` table

### Migration Safety

- All migrations use `IF NOT EXISTS` to be idempotent
- Views use `CREATE OR REPLACE` for easy updates
- Indexes include `IF NOT EXISTS` check
- Foreign keys use `ON DELETE` actions

### Rollback Strategy

While forward migrations are supported, rollbacks require manual intervention:

```sql
-- Example: Rollback migration 002
DROP TABLE IF EXISTS new_table_created_in_002;
DELETE FROM schema_migrations WHERE version = '002';
```

## Connection Details

**Default Connection:**
```
postgresql://cbwinslow:123qweasd@localhost:5432/epstein
```

**Environment Variables:**
```bash
export DATABASE_URL="postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
```

## Troubleshooting

### Migration Already Applied
If you see "migration already applied" errors, check `schema_migrations`:
```sql
SELECT * FROM schema_migrations WHERE version = '001';
```

### Index Creation Fails
If index creation fails (e.g., duplicate), use:
```sql
DROP INDEX IF EXISTS idx_name;
CREATE INDEX idx_name ON table(column);
```

### Extension Not Available
Enable required extensions:
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
```

## Maintenance

### Rebuilding Search Vectors
If needed, manually rebuild search vectors:
```sql
UPDATE media_news_articles SET search_vector = NULL;
-- Trigger will automatically rebuild
```

### Vacuum and Analyze
```sql
VACUUM ANALYZE media_news_articles;
VACUUM ANALYZE media_videos;
VACUUM ANALYZE media_documents;
```

## Contact

For questions about the database schema, contact the development team.
