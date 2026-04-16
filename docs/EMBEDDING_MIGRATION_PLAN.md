# Embedding Migration Plan - Least Effort Approach

> **Status:** Draft - April 16, 2026  
> **Goal:** Minimize GPU usage while maximizing embedding coverage  
> **Principle:** Keep all existing data, use optimal model for new work

---

## Current State Analysis

| Metric | Count | % |
|--------|-------|---|
| **Total pages with text** | 2,892,730 | 100% |
| **Unique content (deduped)** | ~2,500,000* | ~86% |
| **Duplicate pages** | ~392,730 | ~14% |
| **Has MiniLM embedding** | 1,561,755 | 54% |
| **Has Nomic embedding** | 36,700 | 1.3% |
| **Has both embeddings** | 36,700 | 1.3% |
| **No embedding** | 1,330,975 | 46% |

*Estimated - pending content hash calculation

---

## The Problem: Mixed Models

| Model | Dimensions | Records | Incompatible With |
|-------|------------|---------|-----------------|
| **all-MiniLM-L6-v2** | 384 | 1,561,755 | Nomic, Gemini |
| **nomic-embed-text-v2** | 384 | 36,700 | MiniLM (different vector space) |
| **gemini-embedding** | 768 | 1,505,618 | Everything (different dims) |

**Critical Issue:** You cannot mix embedding models in semantic search. Each model creates embeddings in a different "vector space."

---

## Recommended Approach: Dual-Column Strategy

**Decision:** Keep BOTH MiniLM and Nomic embeddings in separate columns. Don't recalculate existing embeddings.

### Why This Approach?

1. **✅ Saves GPU life** - Don't recalculate 1.56M MiniLM embeddings
2. **✅ Keeps all data** - Both embedding sets preserved
3. **✅ Enables comparison** - Can benchmark MiniLM vs Nomic
4. **✅ Future flexibility** - Can add more models later
5. **✅ Deduplication savings** - Only embed unique content (~2.5M not 2.9M)

### Database Schema

```sql
-- Current state
pages.rtx3060_embedding (vector)  -- Nomic embeddings (36K)
page_embeddings table             -- MiniLM embeddings (1.56M)

-- Proposed addition
pages.embedding_minilm (vector)   -- Migrate from page_embeddings
pages.embedding_nomic (vector)    -- Current rtx3060_embedding (rename)
```

---

## Phase 1: Deduplication (Zero GPU)

**Goal:** Identify duplicate pages to avoid embedding same content twice

### Steps:

1. **Add content_hash column**
   ```bash
   psql -U cbwinslow -d epstein -f scripts/processing/add_content_hash_dedup.sql
   ```

2. **Results expected:**
   - ~2.5M unique content pages (down from 2.9M)
   - ~392K duplicates identified
   - **Savings: 392K fewer embeddings to calculate**

---

## Phase 2: Keep MiniLM, Add Nomic (Minimal GPU)

**Goal:** Add Nomic embeddings only for pages missing embeddings (deduplicated)

### Calculation:

| Step | Pages | GPU Hours* |
|------|-------|------------|
| Current MiniLM | 1,561,755 | 0 (already done) |
| Unique pages needing Nomic | ~900,000 | ~15 hours |
| **Total if recalculate all** | 2,500,000 | ~42 hours |
| **Savings** | - | **27 hours (64% less GPU)** |

*Assuming 100 pages/sec on RTX 3060

### Implementation:

1. **Update rtx3060_embeddings.py** to only process deduplicated pages
2. **Skip pages that already have MiniLM** (or both)
3. **Target: ~900K pages instead of 2.9M**

---

## Phase 3: Migration Script

### Option A: Keep Separate Tables (Minimal Effort)

```sql
-- Just add column reference
ALTER TABLE pages ADD COLUMN IF NOT EXISTS has_minilm_embedding BOOLEAN DEFAULT FALSE;
UPDATE pages SET has_minilm_embedding = TRUE 
WHERE id IN (SELECT page_id FROM page_embeddings);

-- Create index for fast lookup
CREATE INDEX idx_pages_has_minilm ON pages(has_minilm_embedding) 
WHERE has_minilm_embedding = TRUE;
```

### Option B: Migrate to Single Table (Recommended for Query Simplicity)

```sql
-- Add column for MiniLM embeddings
ALTER TABLE pages ADD COLUMN IF NOT EXISTS embedding_minilm vector(384);

-- Migrate from page_embeddings (batch to avoid lock)
UPDATE pages p
SET embedding_minilm = pe.embedding
FROM page_embeddings pe
WHERE p.id = pe.page_id
  AND p.embedding_minilm IS NULL;

-- Rename rtx3060_embedding for clarity
ALTER TABLE pages RENAME COLUMN rtx3060_embedding TO embedding_nomic;
```

---

## Phase 4: Query Strategy

### Unified Search View

```sql
CREATE OR REPLACE VIEW v_pages_with_embeddings AS
SELECT 
    p.id,
    p.efta_number,
    p.page_number,
    p.text_content,
    COALESCE(p.embedding_minilm, p.embedding_nomic) as embedding,  -- Prefer MiniLM
    CASE 
        WHEN p.embedding_minilm IS NOT NULL THEN 'minilm'
        WHEN p.embedding_nomic IS NOT NULL THEN 'nomic'
        ELSE NULL
    END as embedding_model
FROM pages p
WHERE p.embedding_minilm IS NOT NULL 
   OR p.embedding_nomic IS NOT NULL;
```

### Semantic Search Function

```sql
CREATE OR REPLACE FUNCTION search_pages_semantic(
    query_embedding vector(384),
    match_threshold FLOAT DEFAULT 0.7,
    max_results INT DEFAULT 10
)
RETURNS TABLE (
    page_id INT,
    efta_number TEXT,
    text_content TEXT,
    similarity FLOAT,
    embedding_model TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.id,
        p.efta_number,
        LEFT(p.text_content, 500),
        1 - (p.embedding_minilm <=> query_embedding) as similarity,
        'minilm'::TEXT
    FROM pages p
    WHERE p.embedding_minilm IS NOT NULL
        AND 1 - (p.embedding_minilm <=> query_embedding) > match_threshold
    
    UNION ALL
    
    SELECT 
        p.id,
        p.efta_number,
        LEFT(p.text_content, 500),
        1 - (p.embedding_nomic <=> query_embedding) as similarity,
        'nomic'::TEXT
    FROM pages p
    WHERE p.embedding_nomic IS NOT NULL
        AND 1 - (p.embedding_nomic <=> query_embedding) > match_threshold
        AND p.embedding_minilm IS NULL  -- Avoid duplicates
    
    ORDER BY similarity DESC
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;
```

---

## Phase 5: Validation & Monitoring

### Coverage Tracking

```sql
-- Create tracking table
CREATE TABLE IF NOT EXISTS embedding_migration_log (
    migration_date TIMESTAMPTZ DEFAULT NOW(),
    phase TEXT,
    pages_processed INTEGER,
    embeddings_generated INTEGER,
    gpu_hours DECIMAL(10,2),
    notes TEXT
);

-- Log entries
INSERT INTO embedding_migration_log (phase, pages_processed, embeddings_generated, gpu_hours, notes)
VALUES 
    ('Initial state', 2892730, 1561755, 0, 'MiniLM embeddings from K80s'),
    ('Deduplication', 2892730, 0, 0, 'Identified ~392K duplicate pages'),
    ('Nomic embeddings', 900000, 900000, 15, 'Generated for unique pages missing embeddings');
```

---

## Summary: GPU Time Savings

| Approach | Pages to Embed | GPU Hours | Cost |
|----------|---------------|-----------|------|
| **Recalculate ALL with Nomic** | 2,892,730 | ~48 hours | High GPU wear |
| **Keep MiniLM + Add Nomic for gaps** | 900,000 | ~15 hours | **Optimal** |
| **Current path (mixed models)** | 1,330,975 | ~22 hours | Won't work (incompatible) |

**Recommended: Keep MiniLM + Add Nomic for ~900K deduplicated pages**

---

## Next Steps

1. **Run deduplication SQL** (5 minutes, zero GPU)
2. **Verify duplicate count** - should be ~392K
3. **Update rtx3060_embeddings.py** to use deduplicated page list
4. **Generate Nomic embeddings for ~900K pages** (~15 GPU hours)
5. **Create unified search view** (SQL only)
6. **Document final state** in DATA_INVENTORY_FULL.md

---

*Last Updated: April 16, 2026*  
*Status: Draft - Pending User Approval*
