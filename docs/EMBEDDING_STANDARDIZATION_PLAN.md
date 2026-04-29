# Embedding Model Standardization Plan

> **Status:** PENDING - Waiting for all data to be loaded into PostgreSQL
> **Created:** March 31, 2026
> **Target:** Standardize on single embedding model across all tables

## Current State (Chaos)

### Operational Update — April 26, 2026

The active Linux-side embedding generator now targets the Windows `cbwwin`
Ollama endpoint at `http://192.168.4.25:11343/api/embed`.

- Script: `scripts/processing/rtx3060_embeddings.py`
- Default model: `nomic-embed-text:latest`
- Default target column: `pages.rtx3060_embedding`
- Dimensions: 768
- Existing compatible vectors: 37,750

This keeps the existing `rtx3060_embedding` values instead of mixing a new
model into the same column. If switching to a larger model such as
`mxbai-embed-large`, use a new column or run with `--reset-column` so old
vectors are regenerated.

The database currently contains **incompatible embedding models** across different tables:

| Table | Model | Count | Dimensions | Source |
|-------|-------|-------|------------|--------|
| `page_embeddings` | `all-MiniLM-L6-v2` | 1,494,755 | 384 | Local generation (K80s) |
| `page_embeddings` | `nomic-embed-text-v2-moe` | 2,000 | 384 | RTX 3060 test |
| `kabasshouse_chunk_embeddings` | `gemini-embedding-001` | 1,505,618 | 768 | Google Gemini API |
| `house_oversight_embeddings` | (HuggingFace) | ~69,290 | 768 | HuggingFace import |
| `fbi_embeddings` | (HuggingFace) | ~12,000 | ? | HuggingFace import |

### Why This Is a Problem

**You CANNOT mix embedding models in semantic search.** Each model creates embeddings in a different "vector space":

- MiniLM embeddings cluster around certain semantic concepts
- Nomic embeddings cluster differently
- Gemini embeddings are completely incompatible

**Example:** A query for "Epstein flight logs" using a MiniLM embedding will not find relevant documents embedded with Gemini - they speak different "languages" mathematically.

## Goal

**Standardize ALL embeddings to a single model:** `nomic-ai/nomic-embed-text-v2-moe` (384-dim Matryoshka)

### Why Nomic 384-dim?

1. **Quality:** State-of-the-art for document/legal text (outperforms MiniLM by 15-20%)
2. **Efficiency:** 384-dim uses 50% less storage than 768-dim
3. **Speed:** Matryoshka allows trading speed for accuracy at query time
4. **Matryoshka:** Can still get 768-dim quality by using first 384 dims of 768

## Prerequisites (WAITING FOR THESE)

Before proceeding, we need:

- [ ] **ALL raw data loaded** into PostgreSQL
  - [ ] Dataset 10-14 PDFs processed
  - [ ] Any remaining FBI/House Oversight data
  - [ ] All transcripts converted to text
  - [ ] Image analysis results extracted

- [ ] **RTX 3060 machine ready**
  - Python 3.11 + PyTorch CUDA 12.1
  - Network access to PostgreSQL (192.168.4.101:5432)
  - Verified ~100-200 pages/sec performance

- [ ] **Backup strategy confirmed**
  - pg_dump of embedding tables before migration
  - Ability to rollback if needed

## Execution Steps

### Phase 1: Preparation

```bash
# 1. Verify all data is loaded
psql -c "SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL;"
psql -c "SELECT COUNT(*) FROM page_embeddings;"

# 2. Create backup
gpg_dump -Fc epstein > epstein_pre_embedding_migration.dump

# 3. Clear all existing page_embeddings
psql -c "TRUNCATE TABLE page_embeddings;"
```

### Phase 2: Regenerate All Page Embeddings

```bash
# On RTX 3060 Windows machine (192.168.4.25)
# Estimated time: 3-4 hours for ~2.9M pages at 200 pages/sec
cd C:\Users\blain\epstein_scripts
py -3.11 generate_embeddings.py
```

**The script:**
- Uses nomic-embed-text-v2-moe with 384-dim truncation
- Processes 1000 pages per batch
- Inserts with `ON CONFLICT` for resume capability
- Targets PostgreSQL at 192.168.4.101

### Phase 3: Handle Supplementary Data

The supplementary tables (`kabasshouse_chunk_embeddings`, `house_oversight_embeddings`, `fbi_embeddings`) have **incompatible dimensions and models**.

#### Option A: Regenerate (Recommended)

Extract text from supplementary tables and re-embed with nomic:

```python
# Process kabasshouse_chunk_embeddings
for chunk in kabasshouse_chunks:
    text = chunk['chunk_text']
    embedding = nomic_embed(text, truncate_dim=384)
    insert_to_new_table(chunk_id, embedding)

# Similar for house_oversight and fbi
```

**Estimated time:** ~2-3 hours for ~1.6M supplementary embeddings

#### Option B: Keep Separate (Fallback)

If regeneration is too costly:
1. Add `model_name` column filter to search queries
2. Search each model separately
3. Merge results at application layer

### Phase 4: Verification

```sql
-- Verify all embeddings use same model
SELECT model_name, COUNT(*)
FROM page_embeddings
GROUP BY model_name;
-- Should show ONLY: nomic-ai/nomic-embed-text-v2-moe

-- Verify embedding dimensions
SELECT pg_column_size(embedding), COUNT(*)
FROM page_embeddings
GROUP BY pg_column_size(embedding);
-- Should show ONLY: 1544 bytes (384-dim float32)

-- Test semantic similarity
SELECT efta_number, page_number,
       embedding <=> query_embedding AS distance
FROM page_embeddings
WHERE efta_number = 'EFTA00000001'
ORDER BY distance
LIMIT 5;
```

### Phase 5: Index Optimization

After all embeddings are consistent:

```sql
-- Recreate HNSW index for optimal performance
DROP INDEX IF EXISTS idx_page_embeddings_vector;
CREATE INDEX idx_page_embeddings_vector
ON page_embeddings
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);
```

## Hardware Allocation

| Task | Hardware | Time | Notes |
|------|----------|------|-------|
| Page embeddings | RTX 3060 | ~4 hours | 2.9M pages @ 200/sec |
| Supplementary | RTX 3060 | ~3 hours | 1.6M chunks @ 150/sec |
| Index rebuild | CPU (server) | ~2 hours | HNSW creation |
| **Total** | | **~9 hours** | One overnight run |

## Rollback Plan

If anything goes wrong:

```bash
# Restore from backup
pg_restore -d epstein epstein_pre_embedding_migration.dump
```

## Post-Migration

After standardization:

1. **Update search queries** to use unified embedding model
2. **Remove model-specific code paths** in applications
3. **Document the standard model** in project README
4. **Add validation** to prevent mixed models in future

## Files/Scripts Required

1. **Current:** `scripts/generate_page_embeddings_v2.py` (Linux K80 version)
2. **Current:** `C:\Users\blain\epstein_scripts\generate_embeddings.py` (Windows RTX 3060)
3. **TODO:** Create supplementary re-embedding script
4. **TODO:** Create verification script

## Contact/Notes

- RTX 3060: `192.168.4.25` (user: `blain`)
- PostgreSQL: `192.168.4.101:5432`
- Model: `nomic-ai/nomic-embed-text-v2-moe`
- Target dim: `384` (Matryoshka)
