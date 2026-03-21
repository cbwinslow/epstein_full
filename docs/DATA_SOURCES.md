# Data Sources

## Primary Sources

### 1. DOJ Website (justice.gov/epstein)
- **URL**: `https://www.justice.gov/epstein/doj-disclosures`
- **Content**: 12 Data Sets, ~2.8M pages, ~1.4M documents, ~218GB
- **Auth**: JavaScript age-gate cookie required
- **URL Pattern**: `https://www.justice.gov/epstein/files/DataSet%20{N}/EFTA{XXXXXXXX}.pdf`
- **Status**: Individual PDFs available, bulk downloads removed Feb 6, 2026
- **Note**: ~67,784 documents confirmed removed (404)

### 2. RollCall CDN (Recommended for bulk)
- **URL**: `https://media-cdn.rollcall.com/epstein-files/EFTA{NUMBER}.pdf`
- **Coverage**: DS1-12, byte-identical to DOJ originals (SHA-256 verified)
- **Auth**: None required
- **Speed**: ~28 MB/s, no rate limiting detected
- **Download**: `aria2c` with parallel connections

### 3. Archive.org Mirrors
| Dataset | URL | Size |
|---------|-----|------|
| DS9 | `archive.org/download/Epstein-Dataset-9-2026-01-30/full.tar.bz2` | 103.6 GB |
| DS11 | `archive.org/download/Epstein-Data-Sets-So-Far/DataSet%2011.zip` | 25.6 GB |
| DS1-5 | `archive.org/details/combined-all-epstein-files/` | Multiple files |
| FBI Vault | `archive.org/download/jeffrey-epstein-FBI-vault-files/` | 22 PDF parts |

### 4. HuggingFace Dataset (Pre-extracted text)
- **URL**: `https://huggingface.co/datasets/AfricanKillshot/Epstein-Files`
- **Content**: 634 parquet files, 4.11M rows, ~317GB
- **Fields**: `doc_id`, `file_type`, `text_content` (OCR), `image`, `metadata`
- **Auth**: HF token (free account)
- **Note**: Pre-extracted text — skips OCR entirely

### 5. GitHub Releases (Pre-built databases)
- **URL**: `https://github.com/rhowardstone/Epstein-research-data/releases`
- **Content**: 8 SQLite databases, ~8GB total
- **Key files**:
  - `full_text_corpus.db` (7GB) — 1.4M documents, FTS5 search
  - `redaction_analysis_v2.db` (940MB) — 2.59M redactions
  - `knowledge_graph.db` (892KB) — 606 entities, 2,302 relationships

## EFTA Dataset Ranges

| Dataset | EFTA Start | EFTA End | Files |
|---------|-----------|----------|-------|
| 1 | 00000001 | 00003158 | 3,158 |
| 2 | 00003159 | 00003857 | 699 |
| 3 | 00003858 | 00005586 | 1,729 |
| 4 | 00005705 | 00008320 | 2,616 |
| 5 | 00008409 | 00008528 | 120 |
| 6 | 00008529 | 00008998 | 470 |
| 7 | 00009016 | 00009664 | 649 |
| 8 | 00009676 | 00039023 | 29,348 |
| 9 | 00039025 | 01262781 | 103,608 |
| 10 | 01262782 | 02205654 | 94,287 |
| 11 | 02205655 | 02730264 | 52,459 |
| 12 | 02730265 | 02858497 | 12,820 |

## Additional CDN Mirrors

| Mirror | URL Pattern | Coverage |
|--------|-------------|----------|
| Kino/JDrive | `assets.getkino.com/documents/EFTA{N}.pdf` | DS1-7, DS9-11 |
| JMail | `jmail.world/drive/EFTA{N}.pdf` | DS1-7, DS9-11 |

## Download Commands

```bash
# RollCall CDN (fastest, recommended)
aria2c --input-file urls.txt --max-concurrent-downloads 16 --continue=true

# HuggingFace parquet
aria2c --input-file hf_urls.txt --header "Authorization: Bearer $HF_TOKEN"

# Archive.org bulk (DS9)
wget https://archive.org/download/Epstein-Dataset-9-2026-01-30/full.tar.bz2

# Pre-built databases
wget https://github.com/rhowardstone/Epstein-research-data/releases/download/v4.0/knowledge_graph.db
```
