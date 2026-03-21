# Architecture — System Design

## Overview

The Epstein Full project is a multi-stage pipeline that downloads, processes, and analyzes
the DOJ Epstein Files Transparency Act document releases.

## Infrastructure

| Component | Details |
|-----------|---------|
| Server | Ubuntu, RAID5 md0 (5x drives, 4.4TB), LVM |
| Storage | `/mnt/data/epstein-project/` on vg-data/lv-nextcloud (2.5TB) |
| GPUs | 2x Tesla K80 (12GB) + 1x Tesla K40m (11GB), CUDA 11.4 |
| Python | 3.12 |
| Node | v24 |

## Data Flow

```
                     ┌─────────────────────────────────────┐
                     │           DATA SOURCES              │
                     ├─────────────────────────────────────┤
                     │  DOJ Website (age-gated)            │
                     │  RollCall CDN (no auth)             │
                     │  Archive.org (bulk archives)        │
                     │  HuggingFace (pre-extracted text)   │
                     │  GitHub Releases (pre-built DBs)    │
                     └──────────────┬──────────────────────┘
                                    │
                     ┌──────────────▼──────────────────────┐
                     │        DOWNLOAD LAYER               │
                     ├─────────────────────────────────────┤
                     │  Playwright (DOJ age gate bypass)   │
                     │  aria2c (parallel CDN downloads)    │
                     │  hf_hub (HuggingFace datasets)      │
                     └──────────────┬──────────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
     ┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
     │  Raw PDFs   │     │ HF Parquet  │     │ Pre-built DBs   │
     │  ~218GB     │     │ ~317GB      │     │ ~8GB            │
     │  ~1.4M docs │     │ 4.11M rows  │     │ 1.4M docs       │
     └──────┬──────┘     └──────┬──────┘     └────────┬────────┘
            │                   │                      │
            ▼                   │                      │
     ┌──────────────┐           │                      │
     │ OCR LAYER    │           │                      │
     │ PyMuPDF→Surya│           │                      │
     │ →Docling     │           │                      │
     └──────┬───────┘           │                      │
            │                   │                      │
            └───────────────────┼──────────────────────┘
                                │
                     ┌──────────▼──────────────────────┐
                     │       NLP LAYER                 │
                     ├─────────────────────────────────┤
                     │  spaCy NER (entity extraction)  │
                     │  GLiNER (zero-shot entities)    │
                     │  BART (classification)          │
                     │  nomic-embed (embeddings)       │
                     └──────────┬──────────────────────┘
                                │
                     ┌──────────▼──────────────────────┐
                     │    KNOWLEDGE GRAPH LAYER        │
                     ├─────────────────────────────────┤
                     │  Entity resolution              │
                     │  Relationship extraction        │
                     │  Co-occurrence analysis         │
                     │  Graph building (GEXF/JSON)     │
                     └──────────┬──────────────────────┘
                                │
                     ┌──────────▼──────────────────────┐
                     │       STORAGE LAYER             │
                     ├─────────────────────────────────┤
                     │  SQLite + FTS5 (full-text)      │
                     │  JSON (entities, relationships) │
                     │  GEXF (graph visualization)     │
                     │  pgvector (future: Neon)        │
                     └─────────────────────────────────┘
```

## GPU Allocation

| GPU | Model | VRAM | Assigned Tasks |
|-----|-------|------|----------------|
| 0 | Tesla K80 | 12GB | OCR (Surya), Image Analysis |
| 1 | Tesla K80 | 12GB | Transcription (faster-whisper), NER (spaCy trf) |
| 2 | Tesla K40m | 11GB | Embeddings, Classification |

## Storage Layout

```
/mnt/data/epstein-project/
├── raw-files/              # Downloaded PDFs (data1/ - data12/)
├── databases/              # Pre-built SQLite databases (8GB)
├── hf-parquet/             # HuggingFace parquet files (317GB)
├── processed/              # OCR output, entities, embeddings
├── knowledge-graph/        # Custom KG exports
└── logs/                   # Download and processing logs
```

## Concurrency Model

| Phase | Workers | Concurrency | Bottleneck |
|-------|---------|-------------|------------|
| CDN Download | aria2c | 10 connections/server | Network |
| HF Download | aria2c | 8 connections | HF CDN rate |
| Playwright Download | 4-5 browsers | Sequential per browser | Age gate |
| OCR | 2 GPU workers | GPU-bound | VRAM |
| NER | 4 CPU workers | CPU-bound | spaCy model |
| KG Build | 1 worker | Single-threaded | SQLite writes |

## Upstream Integration

Our code does NOT modify upstream repos. We integrate via:

1. **CLI calls**: `epstein-pipeline ocr ...`, `python3 auto_ep_rip.py ...`
2. **Filesystem interface**: Upstream saves to directories, we read from them
3. **Python imports**: `import spacy`, `import fitz` (public APIs only)

See `RULES.md` for codebase separation rules.
