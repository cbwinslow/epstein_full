# Windows RTX 3060 Integration for Epstein Files Analysis

This directory contains scripts and documentation for using the Windows RTX 3060 to process files for the Epstein Files Analysis project.

## Overview

The Windows RTX 3060 can be used as a powerful processing worker for the Epstein pipeline, providing significant performance improvements for GPU-intensive tasks like OCR, face detection, and NER processing.

## Architecture

```
Linux Server (Main Coordinator)
├── PostgreSQL Database (10.9M rows)
├── File Management & Distribution
└── Task Coordination

Windows RTX 3060 (Processing Worker)
├── GPU-Accelerated Processing
├── OCR (3-5x faster than CPU)
├── Face Detection (2-3x faster)
└── NER Processing (2-3x faster)
```

## Setup Process

### 1. Windows Environment Setup

**Prerequisites:**
- Windows 10/11 with Python 3.12
- RTX 3060 with CUDA 12.4+ (no driver updates required)
- SSH client (OpenSSH or PuTTY)
- SFTP access to Linux server

**Installation Steps:**
1. Install Python 3.12 from python.org
2. Install CUDA Toolkit 12.4 (compatible with existing driver)
3. Install required Python packages
4. Configure SSH key-based authentication

### 2. Processing Workflow

1. **File Transfer**: Linux server sends PDFs/media to Windows via SFTP
2. **GPU Processing**: Windows processes files using RTX 3060
3. **Result Upload**: Processed results uploaded back to Linux server
4. **Database Integration**: Results integrated into PostgreSQL database

### 3. Performance Benefits

- **OCR Processing**: 3-5x faster (200-300 vs 50-100 pages/minute)
- **Face Detection**: 2-3x faster (50-100 vs 20-40 faces/second)
- **NER Extraction**: 2-3x faster (1500-2000 vs 500-1000 docs/minute)
- **Overall Pipeline**: 40-60% throughput improvement

## Scripts

- `setup_windows_worker.py` - Automated Windows setup
- `process_files.py` - Main processing script for Windows
- `transfer_manager.py` - File transfer coordination
- `monitor_worker.py` - Real-time monitoring
- `config_windows.json` - Windows-specific configuration

## Usage

1. Run `setup_windows_worker.py` on Windows to configure environment
2. Start `process_files.py` on Windows to begin processing
3. Monitor progress with `monitor_worker.py`
4. Results automatically integrated into main pipeline

## Security & Safety

- No NVIDIA driver updates required
- SSH key-based authentication
- File integrity verification with checksums
- Error handling and retry logic
- Progress tracking and monitoring

## Troubleshooting

See `TROUBLESHOOTING.md` for common issues and solutions.