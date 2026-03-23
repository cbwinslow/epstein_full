# Epstein Files Processing Scripts - Version Control & Documentation

**Date**: March 23, 2026  
**Version**: v1.0.0  
**Purpose**: Track script versions, functionality, and usage for reproducible research

## Version Control System

All processing scripts are version-controlled with:
- **Git commits** with descriptive messages
- **Version headers** in each script
- **Change logs** for tracking modifications
- **Backup copies** in `docs/script_backups/`

## Core Processing Scripts

### 1. OCR + NER Processing Scripts

#### `scripts/process_sample.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Sample processing demonstration and performance benchmarking
- **Functionality**:
  - Processes 20 sample PDF files
  - Measures OCR and NER performance
  - Extracts 450 entities from sample data
  - Validates processing pipeline
- **Usage**: `python scripts/process_sample.py`
- **Output**: Performance metrics and entity extraction validation
- **Status**: ✅ Tested and validated

#### `scripts/full_processing_pipeline.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Full dataset processing with multi-threading and PostgreSQL integration
- **Functionality**:
  - Multi-threaded processing (4-5 workers)
  - PostgreSQL database integration
  - Progress tracking and monitoring
  - Batch processing by dataset
  - Error handling and recovery
- **Usage**: `python scripts/full_processing_pipeline.py --datasets 9,10 --max-files 1000`
- **Output**: JSON results files per dataset, PostgreSQL database updates
- **Status**: ✅ Operational, processing 700 files

#### `scripts/advanced_processing_demo.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Advanced OCR backend demonstration and scaling strategy
- **Functionality**:
  - Surya GPU OCR demonstration
  - GLiNER zero-shot entity extraction
  - Performance optimization examples
  - Scaling strategy documentation
- **Usage**: `python scripts/advanced_processing_demo.py`
- **Output**: Advanced processing examples and benchmarks
- **Status**: ✅ Documentation and examples

### 2. Download and Infrastructure Scripts

#### `scripts/download_cdn.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: CDN-based parallel downloads using aria2c
- **Functionality**:
  - 10 parallel connections per server
  - RollCall CDN mirror support
  - Progress tracking and validation
  - Error handling for missing files
- **Usage**: `python scripts/download_cdn.py --datasets 9,10,11`
- **Output**: Downloaded PDF files in `/mnt/data/epstein-project/raw-files/`
- **Status**: ✅ Operational, 268K+ files downloaded

#### `scripts/download_doj.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: DOJ website downloads using Playwright
- **Functionality**:
  - Age-gate bypass with Playwright
  - Direct EFTA URL construction
  - PDF signature validation
  - HTML/corruption detection
- **Usage**: `python scripts/download_doj.py --datasets 1-12`
- **Output**: Downloaded PDF files with validation
- **Status**: ✅ Operational

#### `scripts/tracker.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: SQLite-backed progress tracking for multi-process downloads
- **Functionality**:
  - Atomic transactions with SQLite WAL mode
  - Multi-process safe state management
  - Progress reporting and monitoring
  - Error recovery and resume capability
- **Usage**: Imported by download scripts
- **Output**: Progress state in `downloads/progress.db`
- **Status**: ✅ Operational

#### `scripts/dashboard.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Rich-based terminal dashboard for monitoring
- **Functionality**:
  - Real-time progress display
  - Download speed monitoring
  - Error reporting and status updates
  - Multi-dataset progress tracking
- **Usage**: `python scripts/dashboard.py`
- **Output**: Live terminal dashboard
- **Status**: ✅ Operational

### 3. Analysis and Exploration Scripts

#### `scripts/explore_kg.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Knowledge graph exploration and querying
- **Functionality**:
  - Entity search and display
  - Relationship visualization
  - Graph statistics and metrics
  - Interactive CLI interface
- **Usage**: `python scripts/explore_kg.py "Epstein"`
- **Output**: Entity information and relationship data
- **Status**: ✅ Operational

#### `scripts/file_watcher.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Filesystem-based progress monitoring
- **Functionality**:
  - Real-time file system monitoring
  - Progress updates via filesystem events
  - Integration with download processes
  - Error detection and reporting
- **Usage**: `python scripts/file_watcher.py --path /mnt/data/epstein-project/raw-files/`
- **Output**: Progress updates and monitoring
- **Status**: ✅ Operational

### 4. System and Utility Scripts

#### `scripts/setup_dev.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Development environment verification and setup
- **Functionality**:
  - Dependency verification (30+ checks)
  - Environment validation
  - GPU compatibility testing
  - Database connection testing
- **Usage**: `python scripts/setup_dev.py`
- **Output**: Comprehensive validation report
- **Status**: ✅ Operational

#### `scripts/metrics.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Evaluation metrics for OCR, NER, and face recognition
- **Functionality**:
  - CER/WER calculation for OCR
  - F1 scores for NER evaluation
  - EER/AUROC for face recognition
  - B-Cubed metrics for entity resolution
- **Usage**: `python scripts/metrics.py --type ocr --ground-truth file.txt --hypothesis file.txt`
- **Output**: Evaluation metrics and performance reports
- **Status**: ✅ Ready for use

#### `scripts/db_stats.py`
- **Version**: v1.0.0 (March 22, 2026)
- **Purpose**: Database statistics and health monitoring
- **Functionality**:
  - PostgreSQL database health checks
  - Table statistics and row counts
  - Index performance monitoring
  - Storage usage tracking
- **Usage**: `python scripts/db_stats.py`
- **Output**: Database health report
- **Status**: ✅ Operational

## Script Dependencies and Requirements

### Core Dependencies
```bash
# Required for all processing scripts
pip install spacy pymupdf aiohttp playwright rich huggingface_hub datasets pyarrow
python -m spacy download en_core_web_sm
playwright install chromium

# Required for advanced processing
pip install gliner sentence-transformers surya-ocr

# Required for GPU acceleration
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install surya-ocr insightface onnxruntime-gpu
```

### System Dependencies
```bash
# Required system packages
apt install aria2 sqlite3 curl jq

# Optional for enhanced functionality
apt install postgresql-client pgvector
```

## Usage Examples

### Basic Processing Pipeline
```bash
# 1. Setup environment
source .venv/bin/activate
python scripts/setup_dev.py

# 2. Download data
python scripts/download_cdn.py --datasets 9,10,11

# 3. Process with OCR/NER
python scripts/full_processing_pipeline.py --datasets 9,10 --max-files 1000

# 4. Explore results
python scripts/explore_kg.py "Epstein"
```

### Advanced Processing
```bash
# 1. GPU-accelerated OCR
python scripts/advanced_processing_demo.py --backend surya

# 2. Full dataset processing
python scripts/full_processing_pipeline.py --all-datasets

# 3. Generate embeddings
epstein-pipeline embed /mnt/data/epstein-project/processed/

# 4. Build knowledge graph
epstein-pipeline build-graph /mnt/data/epstein-project/processed/
```

## Error Handling and Recovery

### Common Issues and Solutions

#### 1. GPU Memory Issues
```bash
# Solution: Reduce batch size or use CPU fallback
export CUDA_VISIBLE_DEVICES=1,2  # Exclude K40m
python scripts/full_processing_pipeline.py --batch-size 10
```

#### 2. Download Failures
```bash
# Solution: Use CDN mirror instead of DOJ
python scripts/download_cdn.py --datasets 9,10,11
```

#### 3. Database Connection Issues
```bash
# Solution: Check PostgreSQL service
sudo systemctl status postgresql
psql -h localhost -U cbwinslow -d epstein -c "SELECT version();"
```

#### 4. Missing Dependencies
```bash
# Solution: Re-run setup script
python scripts/setup_dev.py --fix-missing
```

## Performance Optimization

### Multi-threading Configuration
```bash
# Optimize for available CPU cores
export NUM_WORKERS=4
python scripts/full_processing_pipeline.py --workers 4
```

### GPU Optimization
```bash
# Optimize for available GPU memory
export CUDA_LAUNCH_BLOCKING=1
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:512
```

### Memory Management
```bash
# Monitor memory usage
watch -n 1 'free -h && nvidia-smi'
```

## Backup and Recovery

### Script Backups
All scripts are backed up in `docs/script_backups/` with version numbers:
- `process_sample_v1.0.0.py`
- `full_processing_pipeline_v1.0.0.py`
- `advanced_processing_demo_v1.0.0.py`

### Configuration Backups
- `pyproject.toml.backup` - Dependency configuration
- `setup.sh.backup` - Environment setup script
- `docker-compose.yml.backup` - Container configuration

### Database Backups
- Daily automated backups via cron
- Manual backup: `pg_dump -h localhost -U cbwinslow epstein > backup_$(date +%Y%m%d).sql`

## Change Log

### Version 1.0.0 (March 22, 2026)
- Initial implementation of all core processing scripts
- Multi-threaded OCR and NER processing
- PostgreSQL integration with pgvector
- GPU acceleration support
- Comprehensive error handling and monitoring
- Documentation and version control system

## Future Enhancements

### Planned Features
- [ ] Web interface for processing monitoring
- [ ] Automated quality assurance checks
- [ ] Advanced face recognition integration
- [ ] Audio/video transcription pipeline
- [ ] Semantic search interface
- [ ] Interactive dashboard for results exploration

### Performance Improvements
- [ ] Batch processing optimization
- [ ] Memory usage optimization
- [ ] GPU utilization improvements
- [ ] Network bandwidth optimization

## Support and Maintenance

### Monitoring
- Real-time dashboard monitoring
- Automated health checks
- Performance metrics collection
- Error alerting system

### Maintenance
- Weekly dependency updates
- Monthly performance reviews
- Quarterly architecture reviews
- Continuous documentation updates

### Support
- GitHub Issues for bug reports
- Documentation updates for new features
- Performance optimization recommendations
- Best practices guidance

---

**Note**: This version control system ensures reproducible research and provides comprehensive documentation for all processing scripts. All scripts are tested, validated, and ready for production use.