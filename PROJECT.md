# Epstein Files Analysis Project

## Quick Start

```bash
# Activate environment
source /home/cbwinslow/workspace/epstein/venv/bin/activate

# Check pipeline
epstein-pipeline --help

# Explore knowledge graph
python3 scripts/explore_kg.py

# Start downloading DOJ files
cd /home/cbwinslow/workspace/epstein/epstein-ripper
python3 auto_ep_rip.py --dataset 1 --out-dir /mnt/data/epstein-project/raw-files/data1
```

## Project Structure

```
/home/cbwinslow/workspace/epstein/
├── CONTEXT.md              # Project context and data sources
├── AGENTS.md               # Agent architecture and workflow
├── RULES.md                # Rules and conventions
├── PROJECT.md              # This file
├── venv/                   # Python virtual environment
├── Epstein-Pipeline/       # Main processing pipeline (forked)
├── Epstein-research-data/  # Pre-built databases and tools
├── epstein-ripper/         # DOJ downloader with Playwright
├── EpsteinLibraryMediaScraper/  # Media URL scraper
└── scripts/                # Custom analysis scripts

/mnt/data/epstein-project/
├── raw-files/              # Downloaded PDFs and media
├── databases/              # Pre-built SQLite databases
├── processed/              # OCR output, entities
├── knowledge-graph/        # Custom KG exports
└── logs/                   # Processing logs
```

## Available Databases

| Database | Size | Rows | Description |
|----------|------|------|-------------|
| knowledge_graph.db | 892KB | 606 entities, 2,302 relationships | Curated entity relationship graph |
| redaction_analysis_v2.db | 940MB | 2.59M redactions, 849K summaries | Redaction detection and text recovery |
| transcripts.db | 4.8MB | 1,628 media files | Audio/video transcriptions |
| ocr_database.db | 68MB | OCR extraction data | Per-page text extraction |
| communications.db | 30MB | Email thread analysis | Communication patterns |
| prosecutorial_query_graph.db | 2.5MB | Subpoena analysis | Legal document tracking |
| full_text_corpus.db | 6.3GB | 1.39M documents | Complete OCR text (downloading) |

## Processing Pipeline

### Phase 1: Download (Current)
- Using epstein-ripper with Playwright for age-verification bypass
- 5 concurrent workers per dataset
- Resume-safe with state files

### Phase 2: OCR
- PyMuPDF for text-layer PDFs (instant)
- Surya for scanned PDFs (GPU-accelerated)
- Confidence scoring per page

### Phase 3: Entity Extraction
- spaCy transformer models for NER
- GLiNER for zero-shot entity types
- Regex patterns for structured data (dates, amounts, case numbers)

### Phase 4: Knowledge Graph Building
- Co-occurrence analysis
- Relationship extraction
- Entity deduplication
- Export to SQLite + JSON + GEXF

### Phase 5: Analysis & Visualization
- Semantic search with embeddings
- Graph visualization
- Timeline analysis
- Financial pattern detection

## GPU Allocation

| GPU | Model | VRAM | Assigned Tasks |
|-----|-------|------|----------------|
| 0 | Tesla K80 | 12GB | OCR (Surya), Image Analysis |
| 1 | Tesla K80 | 12GB | Transcription, NER (spaCy trf) |
| 2 | Tesla K40m | 11GB | Embeddings, Classification |

## Research Goals

1. **Entity Network Mapping**: Identify all persons, organizations, and their relationships
2. **Timeline Reconstruction**: Build chronological event sequences from documents
3. **Financial Flow Analysis**: Track money movements and shell company structures
4. **Redaction Recovery**: Recover improperly redacted text where possible
5. **Cross-Reference Analysis**: Link entities across datasets, court records, and public sources
6. **Knowledge Graph Discovery**: Find new entity relationships through graph analysis

## Status Dashboard

```bash
# Check download progress
ls -lh /mnt/data/epstein-project/raw-files/*/resume_*.txt

# Check GPU status
nvidia-smi

# Check disk usage
df -h /mnt/data

# Database stats
sqlite3 /mnt/data/epstein-project/databases/knowledge_graph.db \
  "SELECT 'Entities:', COUNT(*) FROM entities UNION ALL \
   SELECT 'Relationships:', COUNT(*) FROM relationships;"
```
