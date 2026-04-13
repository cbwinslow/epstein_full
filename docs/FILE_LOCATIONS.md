# File Locations Reference
**Date:** April 13, 2026  
**Purpose:** Master reference for all data file locations

---

## 📁 Workspace Structure Overview

```
~/workspace/
├── epstein/                    # Code, scripts, documentation (~15 GB)
├── epstein-data/              # Data storage (~500+ GB)
└── epstein-pipeline/           # Pipeline submodule
```

---

## 1. CODE & DOCUMENTATION (`~/workspace/epstein/`)

### Main Directories
| Directory | Purpose | Size |
|-----------|---------|------|
| `docs/` | Documentation (DATA_INVENTORY.md, etc.) | ~50 MB |
| `scripts/` | Python import/analysis scripts | ~5 MB |
| `Epstein-Pipeline/` | Processing pipeline submodule | Submodule |
| `Epstein-research-data/` | Research exports submodule | Submodule |
| `epstein-ripper/` | DOJ downloader submodule | Submodule |
| `EpsteinLibraryMediaScraper/` | Media scraper submodule | Submodule |
| `data/` | Small data files | ~100 MB |
| `backups/` | PostgreSQL backups | ~2 GB |
| `downloads/` | Downloaded datasets | ~5 GB |

### Key Files
| File | Purpose |
|------|---------|
| `DATA_INVENTORY.md` | Main data inventory |
| `DUPLICATE_ANALYSIS_REPORT.md` | Duplicate analysis findings |
| `IMPORT_REPORT_APRIL_12.md` | Import summary |
| `AGENTS.md` | Agent configuration |

---

## 2. DATA STORAGE (`~/workspace/epstein-data/`)

### Core Data Directories

#### DOJ Documents
| Directory | Path | Size | Files | Description |
|-----------|------|------|-------|-------------|
| **Raw Files** | `raw-files/` | 177 GB | 1.3M | DOJ PDFs (data1-data12) |
| **Raw Files** | `raw-f/` | - | - | Additional raw files |

#### HuggingFace Datasets
| Directory | Path | Size | Files | SQL Table | Status |
|-----------|------|------|-------|-----------|--------|
| **epstein-files-20k** | `huggingface/epstein_files_20k/` | 127 MB | 2 | `hf_epstein_files_20k` | ✅ Complete |
| **House Oversight TXT** | `hf-house-oversight/` | 101 MB | 7 | `hf_house_oversight_docs` | ✅ Complete |
| **Email Threads** | `hf-emails-threads/` | 4 MB | 7 | ~~`hf_email_threads`~~ | ❌ Duplicate (dropped) |
| **OCR Complete** | `hf-ocr-complete/data/` | 1.3 GB | 1 | `hf_ocr_complete` | 🔄 Importing |
| **Embeddings** | `hf-embeddings/data/` | 341 MB | 1 | `hf_embeddings` | ⏳ Pending |
| **Epstein Data Text** | `hf-new-datasets/epstein-data-text/` | 2.2 GB | 17 | `hf_epstein_data_text` | ⏳ Pending |
| **Epstein Images** | `hf-new-datasets/epstein-images/` | 4.9 GB | 10 | - | 📂 Filesystem |
| **Cropped Images** | `hf-new-datasets/epstein-images-cropped/` | 4.3 GB | 7 | - | 📂 Filesystem |
| **FBI Files** | `hf-datasets/fbi-files/` | 4.5 GB | 355+ | `fbi_vault_pages` | ✅ Metadata |
| **Full Index** | `hf-datasets/full-index/` | 4 MB | 32 | `full_epstein_index` | ✅ Complete |

#### Legacy HuggingFace Data
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **HF Parquet** | `hf-parquet/` | 318 GB | 634 parquet files |
| **HF Datasets** | `hf-datasets/` | - | Various HF datasets |
| **HF Emails Alt** | `hf-emails-alt/` | - | Alternative email source |

#### External Repositories
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **External Repos** | `external_repos/` | - | Cloned repos (epstein-network-data, etc.) |
| **kabbashouse Data** | `kabasshouse-data/` | - | kabbashouse HF datasets |

#### Government & Legal Data
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **CourtListener** | `courtlistener/` | - | Court records |
| **FBI Vault** | `fbi-vault/` | - | FBI released documents |
| **FEC Data** | `fec/` | 22 GB | Campaign finance data |

#### News & Media
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **GDELT** | `gdelt/` | - | News articles database |
| **Media** | `media/` | - | Media files |

#### ICIJ Offshore Leaks
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **ICIJ Data** | `icij-data/` | ~600 MB | Panama/Paradise/Pandora Papers |

#### Processed Data
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **Processed** | `processed/` | - | OCR output, entities |
| **Knowledge Graph** | `knowledge-graph/` | - | KG exports |

#### Databases & Models
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **SQLite DBs** | `databases/` | 12 GB | 8 pre-built SQLite databases |
| **ML Models** | `models/` | 109 GB | ML models for processing |

#### Downloads & Supplementary
| Directory | Path | Size | Description |
|-----------|------|------|-------------|
| **Downloads** | `downloads/` | - | Download staging |
| **Supplementary** | `supplementary/` | ~22 MB | epsteinexposed.com scrape |
| **Supplementary Datasets** | `supplementary-datasets/` | - | Additional HF datasets |

#### System Data
| Directory | Path | Description |
|-----------|------|-------------|
| **Backups** | `backups/` | PostgreSQL backups |
| **Logs** | `logs/` | Download/processing logs |
| **PIDs** | `pids/` | Process ID files |
| **Letta Data** | `letta-data/` | Letta memory system |

---

## 3. PIPELINE (`~/workspace/epstein-pipeline/`)

| Directory | Purpose |
|-----------|---------|
| `src/` | Source code |
| `scripts/` | Pipeline scripts |
| `config/` | Configuration |
| `data/` | Pipeline data |
| `docs/` | Documentation |
| `tests/` | Tests |

---

## 📊 Summary Statistics

### By Category
| Category | Directories | Total Size |
|----------|-------------|------------|
| **DOJ Documents** | 2 | ~177 GB |
| **HuggingFace Datasets** | 10 | ~17 GB |
| **HF Parquet** | 1 | ~318 GB |
| **External Repos** | 2 | - |
| **Government Data** | 3 | ~22 GB |
| **News/Media** | 2 | - |
| **ICIJ** | 1 | ~600 MB |
| **SQLite DBs** | 1 | ~12 GB |
| **ML Models** | 1 | ~109 GB |
| **Other** | 8 | - |

**Grand Total: ~655+ GB**

---

## 🔍 Quick Access Commands

```bash
# Find files by extension
find ~/workspace/epstein-data -name "*.parquet" | head

# Find large files (>100MB)
find ~/workspace/epstein-data -type f -size +100M -exec ls -lh {} \;

# Check directory size
du -sh ~/workspace/epstein-data/hf-*/

# Count files by type
find ~/workspace/epstein-data -name "*.pdf" | wc -l
```

---

*Generated: April 13, 2026*
