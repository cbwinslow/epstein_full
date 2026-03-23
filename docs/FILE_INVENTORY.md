# Epstein Files Project - Complete File Inventory

**Date**: March 23, 2026  
**Version**: v1.0.0  
**Purpose**: Comprehensive inventory of all project files with descriptions and usage

## Directory Structure

```
epstein_full/
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md           # System design and technical architecture
│   ├── DATA_SOURCES.md           # Data sources and acquisition methods
│   ├── FILE_INVENTORY.md         # This file - complete file inventory
│   ├── IMPLEMENTATION_STATUS.md  # Implementation status and progress
│   ├── METHODOLOGY.md            # Research methodology and data model
│   ├── PROJECT_SUMMARY.md        # Executive summary and technical specs
│   ├── SCRIPT_VERSIONS.md        # Script version control and documentation
│   ├── WORKFLOW.md               # Processing pipeline documentation
│   └── script_backups/           # Version-controlled script backups
├── scripts/                      # Processing and analysis scripts
├── Epstein-Pipeline/             # [submodule] Main processing pipeline
├── Epstein-research-data/        # [submodule] Pre-built databases + tools
├── epstein-ripper/               # [submodule] DOJ downloader
├── EpsteinLibraryMediaScraper/   # [submodule] Media URL scraper
├── processed/                    # Processing results and outputs
├── downloads/                    # Downloaded files and progress tracking
├── raw-files/                    # Raw PDF files from downloads
├── databases/                    # Pre-built SQLite databases
└── migrations/                   # Database migration scripts
```

## Documentation Files

### Core Documentation

| File | Size | Description | Last Modified |
|------|------|-------------|---------------|
| `ARCHITECTURE.md` | 15KB | System design, technical architecture, GPU allocation | March 23, 2026 |
| `DATA_SOURCES.md` | 8KB | Data sources, URLs, acquisition methods | March 23, 2026 |
| `FILE_INVENTORY.md` | 12KB | Complete file inventory (this file) | March 23, 2026 |
| `IMPLEMENTATION_STATUS.md` | 25KB | Implementation status and current progress | March 23, 2026 |
| `METHODOLOGY.md` | 45KB | Research methodology, data model, evaluation metrics | March 23, 2026 |
| `PROJECT_SUMMARY.md` | 28KB | Executive summary and technical specifications | March 23, 2026 |
| `SCRIPT_VERSIONS.md` | 32KB | Script version control and comprehensive documentation | March 23, 2026 |
| `WORKFLOW.md` | 18KB | Processing pipeline documentation | March 23, 2026 |

### Script Backups

| File | Size | Description | Version |
|------|------|-------------|---------|
| `script_backups/process_sample_v1.0.0.py` | 5KB | Sample processing demonstration | v1.0.0 |
| `script_backups/full_processing_pipeline_v1.0.0.py` | 9KB | Full dataset processing pipeline | v1.0.0 |
| `script_backups/advanced_processing_demo_v1.0.0.py` | 9KB | Advanced OCR backend demonstration | v1.0.0 |
| `script_backups/download_cdn_v1.0.0.py` | 12KB | CDN-based parallel downloads | v1.0.0 |
| `script_backups/download_doj_v1.0.0.py` | 15KB | DOJ website downloads | v1.0.0 |
| `script_backups/tracker_v1.0.0.py` | 8KB | Progress tracking and monitoring | v1.0.0 |
| `script_backups/dashboard_v1.0.0.py` | 10KB | Terminal dashboard for monitoring | v1.0.0 |
| `script_backups/explore_kg_v1.0.0.py` | 6KB | Knowledge graph exploration | v1.0.0 |
| `script_backups/file_watcher_v1.0.0.py` | 7KB | Filesystem progress monitoring | v1.0.0 |
| `script_backups/setup_dev_v1.0.0.py` | 11KB | Development environment setup | v1.0.0 |
| `script_backups/metrics_v1.0.0.py` | 14KB | Evaluation metrics and performance testing | v1.0.0 |
| `script_backups/db_stats_v1.0.0.py` | 6KB | Database statistics and health monitoring | v1.0.0 |

## Processing Scripts

### OCR + NER Processing Scripts

| Script | Size | Purpose | Status | Dependencies |
|--------|------|---------|---------|--------------|
| `scripts/process_sample.py` | 5KB | Sample processing demonstration | ✅ Operational | spaCy, PyMuPDF |
| `scripts/full_processing_pipeline.py` | 9KB | Full dataset processing | ✅ Operational | spaCy, PostgreSQL |
| `scripts/advanced_processing_demo.py` | 9KB | Advanced OCR backend demo | ✅ Documentation | Surya, GLiNER |

### Download and Infrastructure Scripts

| Script | Size | Purpose | Status | Dependencies |
|--------|------|---------|---------|--------------|
| `scripts/download_cdn.py` | 12KB | CDN-based parallel downloads | ✅ Operational | aria2c, requests |
| `scripts/download_doj.py` | 15KB | DOJ website downloads | ✅ Operational | Playwright |
| `scripts/tracker.py` | 8KB | Progress tracking | ✅ Operational | SQLite |
| `scripts/dashboard.py` | 10KB | Terminal dashboard | ✅ Operational | Rich library |
| `scripts/launch_downloads.sh` | 2KB | Multi-process launcher | ✅ Operational | Bash |
| `scripts/run_downloads.py` | 4KB | Download runner | ✅ Operational | Python |

### Analysis and Exploration Scripts

| Script | Size | Purpose | Status | Dependencies |
|--------|------|---------|---------|--------------|
| `scripts/explore_kg.py` | 6KB | Knowledge graph exploration | ✅ Operational | NetworkX |
| `scripts/file_watcher.py` | 7KB | Filesystem monitoring | ✅ Operational | watchdog |
| `scripts/test_windows_processing.py` | 7KB | Windows processing test | ✅ Tested | Windows compatibility |

### System and Utility Scripts

| Script | Size | Purpose | Status | Dependencies |
|--------|------|---------|---------|--------------|
| `scripts/setup_dev.py` | 11KB | Development environment setup | ✅ Operational | 30+ checks |
| `scripts/metrics.py` | 14KB | Evaluation metrics | ✅ Ready | sklearn, scipy |
| `scripts/db_stats.py` | 6KB | Database health monitoring | ✅ Operational | PostgreSQL |
| `scripts/db_backup.py` | 4KB | Database backup automation | ✅ Operational | pg_dump |
| `scripts/db_search.py` | 5KB | Database search interface | ✅ Operational | FTS5 |
| `scripts/db_vacuum.py` | 3KB | Database maintenance | ✅ Operational | VACUUM |
| `scripts/system_monitor.py` | 8KB | System resource monitoring | ✅ Operational | psutil |
| `scripts/gpu_monitor.py` | 4KB | GPU utilization monitoring | ✅ Operational | nvidia-ml-py |
| `scripts/cpu_monitor.py` | 3KB | CPU utilization monitoring | ✅ Operational | psutil |

### Advanced Processing Scripts

| Script | Size | Purpose | Status | Dependencies |
|--------|------|---------|---------|--------------|
| `scripts/distribute_tasks.py` | 6KB | Task distribution | ✅ Ready | multiprocessing |
| `scripts/migrate_sqlite_to_pg.py` | 12KB | Database migration | ✅ Operational | SQLAlchemy |
| `scripts/load_supplementary.py` | 8KB | Supplementary data loading | ✅ Ready | Various APIs |
| `scripts/fetch_epstein_exposed.py` | 5KB | External data fetching | ✅ Ready | requests |
| `scripts/save_memory.py` | 3KB | Memory management | ✅ Ready | pickle |
| `scripts/letta_memory.py` | 9KB | AI memory integration | ✅ Ready | Letta framework |

## Configuration Files

| File | Size | Purpose | Status |
|------|------|---------|---------|
| `pyproject.toml` | 4KB | Python dependencies and configuration | ✅ Complete |
| `setup.sh` | 3KB | Environment setup script | ✅ Complete |
| `docker-compose.yml` | 2KB | Container configuration | ✅ Ready |
| `.env.example` | 1KB | Environment variables template | ✅ Complete |
| `.gitignore` | 1KB | Git ignore patterns | ✅ Complete |
| `.python-version` | 10B | Python version specification | ✅ Complete |

## Project Management Files

| File | Size | Purpose | Status |
|------|------|---------|---------|
| `README.md` | 8KB | Project overview and quick start | ✅ Updated |
| `PROJECT.md` | 6KB | Project structure and goals | ✅ Complete |
| `AGENTS.md` | 15KB | Agent architecture and workflow | ✅ Complete |
| `CONTEXT.md` | 12KB | Living memory and current state | ✅ Updated |
| `RULES.md` | 8KB | Coding standards and conventions | ✅ Complete |
| `TASKS.md` | 25KB | Task tracking and progress | ✅ Complete |
| `VALIDATION_REPORT.md` | 10KB | Validation results and testing | ✅ Complete |
| `LICENSE` | 1KB | MIT license | ✅ Complete |

## Data and Output Files

### Processed Results

| File | Size | Description | Status |
|------|------|-------------|---------|
| `processed/postgresql_processing_report.json` | 17KB | Processing statistics | ✅ Complete |
| `processed/dataset_1_results.json` | 1.1MB | Dataset 1 entities | ✅ Complete |
| `processed/dataset_2_results.json` | 241KB | Dataset 2 entities | ✅ Complete |
| `processed/dataset_3_results.json` | 248KB | Dataset 3 entities | ✅ Complete |
| `processed/dataset_4_results.json` | 3.6MB | Dataset 4 entities | ✅ Complete |
| `processed/dataset_5_results.json` | 174KB | Dataset 5 entities | ✅ Complete |
| `processed/dataset_6_results.json` | 480KB | Dataset 6 entities | ✅ Complete |
| `processed/dataset_7_results.json` | 751KB | Dataset 7 entities | ✅ Complete |
| `processed/dataset_9_results.json` | 962KB | Dataset 9 entities | ✅ Complete |
| `processed/dataset_10_results.json` | 630KB | Dataset 10 entities | ✅ Complete |
| `processed/dataset_11_results.json` | 513KB | Dataset 11 entities | ✅ Complete |

### Database Files

| File | Size | Description | Status |
|------|------|-------------|---------|
| `databases/knowledge_graph.db` | 892KB | Entity relationships | ✅ Complete |
| `databases/redaction_analysis_v2.db` | 940MB | Redaction analysis | ✅ Complete |
| `databases/image_analysis.db` | 389MB | Image descriptions | ✅ Complete |
| `databases/ocr_database.db` | 68MB | OCR results | ✅ Complete |
| `databases/communications.db` | 30MB | Email analysis | ✅ Complete |
| `databases/transcripts.db` | 4.8MB | Media transcripts | ✅ Complete |
| `databases/prosecutorial_query_graph.db` | 2.5MB | Subpoena analysis | ✅ Complete |
| `databases/full_text_corpus.db` | 7.0GB | Full text search | ✅ Complete |

### Download Progress

| File | Size | Description | Status |
|------|------|-------------|---------|
| `downloads/progress.db` | 2MB | Download progress tracking | ✅ Active |
| `downloads/state_*.json` | Variable | Dataset download states | ✅ Active |
| `downloads/logs/` | Variable | Download logs | ✅ Active |

## Upstream Repository Integration

### Git Submodules

| Repository | Stars | Purpose | Status |
|------------|-------|---------|---------|
| `Epstein-Pipeline/` | 95 | Main processing pipeline | ✅ Integrated |
| `Epstein-research-data/` | 157 | Pre-built databases + tools | ✅ Integrated |
| `epstein-ripper/` | 3 | DOJ downloader | ✅ Integrated |
| `EpsteinLibraryMediaScraper/` | 23 | Media URL scraper | ✅ Integrated |

### Integration Points

| Component | Integration Method | Status |
|-----------|-------------------|---------|
| OCR Backend | `epstein-pipeline ocr` CLI | ✅ Working |
| NER Extraction | `epstein-pipeline extract-entities` | ✅ Working |
| Database Export | `epstein-pipeline export` | ✅ Working |
| Knowledge Graph | Custom integration | ✅ Working |
| Download Tools | Direct script calls | ✅ Working |

## File Integrity and Version Control

### Git Status
- **Total Files**: 150+ tracked files
- **Commits**: 50+ commits with descriptive messages
- **Branches**: main branch with feature branches
- **Tags**: v1.0.0 release tag

### Backup Strategy
- **Script Backups**: Version-controlled in `docs/script_backups/`
- **Configuration Backups**: `.backup` files for critical configs
- **Database Backups**: Daily automated backups via cron
- **Git Backups**: Remote repository on GitHub

### File Validation
- **Checksums**: SHA-256 checksums for critical files
- **Integrity Checks**: Automated validation scripts
- **Version Verification**: Script version headers
- **Dependency Verification**: 30+ dependency checks

## Usage Guidelines

### Script Execution Order

1. **Setup Phase**
   ```bash
   python scripts/setup_dev.py
   python scripts/db_stats.py
   ```

2. **Download Phase**
   ```bash
   python scripts/download_cdn.py --datasets 9,10,11
   python scripts/dashboard.py
   ```

3. **Processing Phase**
   ```bash
   python scripts/full_processing_pipeline.py --datasets 9,10 --max-files 1000
   python scripts/advanced_processing_demo.py
   ```

4. **Analysis Phase**
   ```bash
   python scripts/explore_kg.py "Epstein"
   python scripts/metrics.py --type ocr
   ```

### Error Recovery

1. **Script Failures**: Check logs in `scripts/logs/`
2. **Database Issues**: Use `scripts/db_stats.py` for diagnostics
3. **Download Failures**: Use `scripts/download_cdn.py` as fallback
4. **Processing Errors**: Check `processed/` directory for partial results

### Performance Optimization

1. **Multi-threading**: Use `--workers 4` for optimal CPU usage
2. **GPU Acceleration**: Set `CUDA_VISIBLE_DEVICES=1,2` for K80s
3. **Memory Management**: Monitor with `scripts/system_monitor.py`
4. **Batch Processing**: Use `--batch-size 100` for large datasets

## Maintenance Schedule

### Daily Tasks
- [ ] Check download progress via `scripts/dashboard.py`
- [ ] Monitor system resources via `scripts/system_monitor.py`
- [ ] Review processing logs in `processed/` directory

### Weekly Tasks
- [ ] Update dependencies via `scripts/setup_dev.py --update`
- [ ] Run database maintenance via `scripts/db_vacuum.py`
- [ ] Backup critical files to `docs/script_backups/`

### Monthly Tasks
- [ ] Performance review and optimization
- [ ] Documentation updates
- [ ] Version control cleanup
- [ ] Backup verification

## Security Considerations

### File Permissions
- **Scripts**: 755 (executable)
- **Configuration**: 644 (readable)
- **Data**: 644 (readable)
- **Backups**: 644 (readable)

### Access Control
- **Sensitive Data**: Encrypted database connections
- **API Keys**: Stored in `.env` files (not committed)
- **System Access**: Limited to authorized users
- **Audit Logging**: All operations logged

### Data Privacy
- **GDPR Compliance**: Personal data handling protocols
- **Document Handling**: Secure processing procedures
- **Access Logging**: All data access tracked
- **Retention Policies**: Automated cleanup procedures

---

**Note**: This inventory provides comprehensive documentation of all project files, their purposes, and usage guidelines. All files are version-controlled and backed up for reproducible research.