# Processing Workflow

## Pipeline Stages

### Stage 1: Download
- **Tools**: `download_cdn.py`, `download_doj.py`, `auto_ep_rip.py`
- **Input**: DOJ URLs, CDN mirrors, HuggingFace
- **Output**: Raw PDFs in `raw-files/data{N}/`, HF parquet in `hf-parquet/`
- **Concurrency**: 5-8 aria2c instances, 4-5 Playwright browsers
- **Validation**: PDF signature check (`%PDF-` header)

### Stage 2: OCR (optional if using HF parquet)
- **Tool**: `epstein-pipeline ocr <dir> -o <out> --backend surya`
- **Backends**: PyMuPDF (instant) → Surya (GPU) → Docling (fallback)
- **Input**: Raw PDFs
- **Output**: JSON with per-page text + confidence scores
- **GPU**: Tesla K80

### Stage 3: Entity Extraction
- **Tool**: `epstein-pipeline extract-entities <dir>`
- **Backends**: spaCy en_core_web_trf + GLiNER + regex patterns
- **Input**: OCR text
- **Output**: Entity JSON with document cross-references
- **Entities**: people, organizations, locations, dates, case numbers, financial amounts

### Stage 4: Embeddings
- **Tool**: `epstein-pipeline embed <dir> -o <out>`
- **Model**: nomic-embed-text-v2-moe (768-dim, Matryoshka 256-dim)
- **Input**: OCR text
- **Output**: Vector embeddings for semantic search
- **GPU**: Tesla K40m (overflow)

### Stage 5: Classification
- **Tool**: `epstein-pipeline classify <dir>`
- **Model**: BART-large-mnli (zero-shot)
- **Input**: OCR text
- **Output**: Document categories (court filings, depositions, flight logs, etc.)

### Stage 6: Knowledge Graph
- **Tool**: `epstein-pipeline build-graph <dir> -o <out>`
- **Input**: Extracted entities
- **Output**: entities.json + relationships.json + GEXF
- **Logic**: Co-occurrence analysis, relationship extraction, entity resolution

### Stage 7: Export
- **Tool**: `epstein-pipeline export sqlite <dir> -o <db>`
- **Input**: All processed data
- **Output**: SQLite database with FTS5 full-text search

## Command Sequence

```bash
# 1. Download (runs in background)
python scripts/download_cdn.py --datasets 1-12

# 2. OCR (if not using HF parquet)
epstein-pipeline ocr /home/cbwinslow/workspace/epstein-data/raw-files/data9/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/ocr/data9/ \
  --backend surya --workers 4

# 3. Entities
epstein-pipeline extract-entities /home/cbwinslow/workspace/epstein-data/processed/ocr/data9/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/entities/

# 4. Embeddings
epstein-pipeline embed /home/cbwinslow/workspace/epstein-data/processed/ocr/data9/ \
  -o /home/cbwinslow/workspace/epstein-data/processed/embeddings/

# 5. Knowledge Graph
epstein-pipeline build-graph /home/cbwinslow/workspace/epstein-data/processed/ \
  -o /home/cbwinslow/workspace/epstein-data/knowledge-graph/

# 6. Export
epstein-pipeline export sqlite /home/cbwinslow/workspace/epstein-data/processed/ \
  -o /home/cbwinslow/workspace/epstein-data/databases/processed_corpus.db
```

## Monitoring

```bash
# Live dashboard
python scripts/dashboard.py

# Progress tracker
python scripts/tracker.py watch

# File watcher
python scripts/file_watcher.py
```

## Error Handling

| Error | Action |
|-------|--------|
| HTML age-gate response | Quarantine + re-auth with Playwright |
| 404 (file removed) | Log + skip |
| GPU OOM | Fallback to CPU |
| Network timeout | Exponential backoff retry |
| Disk full (90%) | Pause downloads, alert |

## Deduplication

Three-pass deduplication after download:
1. **SHA-256 hash**: Exact duplicate detection
2. **MinHash/LSH**: Near-duplicate detection
3. **Semantic similarity**: OCR variant detection
