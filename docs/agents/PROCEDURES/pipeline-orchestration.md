# Pipeline Orchestration Procedures

> **Last Updated:** April 24, 2026  
> **Purpose:** Procedures for orchestrating the full ingestion pipeline - from discovery to enrichment  

---

## 🎯 Pipeline Orchestration Overview

### Full Pipeline Flow

```
[Discovery] → [Download] → [Import] → [Process] → [Enrich]
     │              │            │            │            │
     └── Phase 1     └── Phase 2   └── Phase 3   └── Phase 4   └── Phase 5
```

### Orchestration Scripts

| Phase | Script | Purpose |
|--------|--------|---------|
| 1: Discovery | `scripts/ingestion/phase1_discovery.py` | Identify sources, plan |
| 2: Download | `scripts/download/run_all_downloads.sh` | Download all sources |
| 3: Import | `scripts/import/run_all_imports.sh` | Import to PostgreSQL |
| 4: Process | `epstein-pipeline/ocr`, `extract-entities` | OCR, NER |
| 5: Enrich | `scripts/enrichment/`, `processing/` | Embeddings, Graph |

---

## 🚀 Full Pipeline Run (from Scratch)

### Automated Full Pipeline

```bash
# File: scripts/run_full_pipeline.sh
#!/bin/bash
set -e  # Exit on error

echo "Starting full Epstein data pipeline..."

# Phase 1: Discovery
echo "Phase 1: Discovery..."
python scripts/ingestion/check_inventory.py
python scripts/ingestion/check_gov_data_status.py

# Phase 2: Download
echo "Phase 2: Download..."
bash scripts/download/run_all_downloads.sh

# Phase 3: Import
echo "Phase 3: Import..."
bash scripts/import/run_all_imports.sh

# Phase 4: Process (OCR, NER)
echo "Phase 4: Processing..."
cd epstein-pipeline
./ocr --all -o /home/cbwinslow/workspace/epstein-data/processed/ocr_output/
./extract-entities --all -o /home/cbwinslow/workspace/epstein-data/processed/entities/
cd ..

# Phase 5: Enrichment
echo "Phase 5: Enrichment..."
python scripts/enrichment/rtx3060_embeddings.py --all
python scripts/processing/master_unify.py

echo "Pipeline complete!"
```

---

## 📋 Phase-by-Phase Procedures

### Phase 1: Discovery & Planning

```bash
# Check what's available
python scripts/ingestion/check_inventory.py
# Output: 421-line inventory with all sources

# Verify government data status
python scripts/ingestion/check_gov_data_status.py
# Checks: Congress, GovInfo, FEC, White House

# Plan ingestion
# 1. Read docs/DATA_INVENTORY_FULL.md
# 2. Check specific guide in docs/agents/INGESTION_GUIDES/
# 3. Follow step-by-step procedure
```

**Deliverables:**
- Updated `docs/DATA_INVENTORY_FULL.md`
- Identified gaps and priorities
- Plan for next ingestion cycle

---

### Phase 2: Download

```bash
# DOJ Epstein Library (✅ Complete, skip if done)
cd epstein-ripper && python auto_ep_rip.py --dataset ALL

# Congress Historical (105th-119th)
for congress in {105..119}; do
    python scripts/download/download_congress_historical.py --congress $congress
done

# GovInfo Bulk
python scripts/download/download_govinfo_bulk.py --type FR --year 2024

# Retry with rate limiting (for problematic sources)
python scripts/download/download_senate_vote_details.py --retry --delay 2.0
```

**Key Download Scripts:**
- `epstein-ripper/auto_ep_rip.py` - DOJ (Playwright)
- `scripts/download/download_congress_historical.py` - Congress
- `scripts/download/download_govinfo_bulk.py` - GovInfo
- `scripts/download/download_whitehouse.py` - White House visitors
- `scripts/download/download_fara.py` - FARA
- `scripts/download/download_sec_edgar_recent.py` - SEC EDGAR

---

### Phase 3: Import to PostgreSQL

```bash
# Import all sources to PostgreSQL
python scripts/import/import_jmail_full.py
python scripts/import/import_icij.py
python scripts/import/import_fara.py
python scripts/import/import_congress.py
python scripts/import/import_whitehouse_visitors.py
python scripts/import/import_hf_epstein_files_20k.py
```

**Import Order (respecting foreign keys):**
1. `congress_members` (no dependencies)
2. `congress_bills` (references members)
3. `congress_house_votes` (references bills)
4. Other tables...

**Verification:**
```sql
-- Check all table counts
\dt+  # List all tables with row counts
```

---

### Phase 4: Processing (OCR, NER)

```bash
# OCR PDFs (GPU recommended for Surya)
cd epstein-pipeline
./ocr /home/cbwinslow/workspace/epstein-data/raw-files/data1/ \
     -o /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
     --backend surya

# Extract entities (spaCy + GLiNER)
./extract-entities \
     /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
     -o /home/cbwinslow/workspace/epstein-data/processed/entities/

# Batch NER
python scripts/enrichment/batch_ner_extraction.py \
     --input /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
     --output /home/cbwinslow/workspace/epstein-data/processed/entities/
```

---

### Phase 5: Enrichment (Embeddings, Graph)

```bash
# Generate embeddings (RTX 3060)
python scripts/enrichment/rtx3060_embeddings.py \
     --input /home/cbwinslow/workspace/epstein-data/processed/ocr_output/ \
     --output /home/cbwinslow/workspace/epstein-data/processed/embeddings/

# Build knowledge graph
python scripts/processing/master_unify.py \
     --sources epstein,dleeerdefi,icij \
     --output /home/cbwinslow/workspace/epstein-data/knowledge-graph/

# Cross-reference datasets
python scripts/enrichment/load_supplementary.py \
     --primary epstein --secondary jmail,icij,fec
```

---

## 🔄 Error Handling & Recovery

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Rate limit / Block | Retry with delay, alternate headers |
| Connection timeout | Network issue | Retry with exponential backoff |
| Duplicate key | Existing data | Use `ON CONFLICT DO NOTHING` |
| Out of memory | Large dataset | Process in batches |

### Recovery Procedures

```bash
# 1. Check what completed
psql -d epstein -c "
SELECT table_name, row_count FROM inventory_table;
"

# 2. Resume from last successful point
python scripts/download/download_congress_historical.py --congress 119 --resume

# 3. Verify partial imports
python scripts/processing/verify_counts.sql --partial
```

---

## 📊 Monitoring & Logging

### Progress Tracking

**Table:** `collection_queue` (in PostgreSQL)  

```sql
-- Check collection progress
SELECT source, status, COUNT(*) as total,
       SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as done
FROM collection_queue
GROUP BY source;
```

### Logging

```bash
# All scripts log to:
/home/cbwinslow/workspace/epstein/logs/

# View recent logs
tail -f /home/cbwinslow/workspace/epstein/logs/*.log
```

---

## 📝 Notes for AI Agents

- **Follow** the phase order (1→2→3→4→5)
- **Use** `scripts/config.py` for all paths
- **Log** all progress and errors
- **Update** documentation after each phase
- **Close** GitHub issues when phases complete
- **Make** the pipeline repeatable - use the wrapper scripts!

---

## 🚨 Where Codex Left Off (Open Issues)

### High Priority (🚨 Urgent)

1. **Issue #58**: Senate vote details (403 errors)
   - Script: `download_senate_vote_details.py`
   - Action: Fix retry logic, alternate sources

2. **Issue #55**: SEC EDGAR bulk ingestion
   - Script: `download_sec_edgar_recent.py`
   - Action: Run bulk import for Form 4, 13F

3. **Issue #39**: 749K missing documents
   - Action: Identify gaps, re-download

### Medium Priority

4. **Issue #52**: GovInfo expansion
   - Script: `download_govinfo_bulk.py`
   - Action: Expand beyond current baseline

5. **Issue #30**: Knowledge graph connections
   - Script: `processing/master_unify.py`
   - Action: Build from document co-occurrence

6. **Issue #29**: Text embeddings expansion
   - Scripts: `enrichment/embed_*.py`
   - Action: Expand coverage beyond RTX 3060

---

*Last Updated: April 24, 2026*  
*Status: Ready for Continuation*
