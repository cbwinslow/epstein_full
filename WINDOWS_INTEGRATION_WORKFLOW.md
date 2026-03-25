# Windows RTX 3060 Integration Workflow

## Overview

This document provides the complete workflow for integrating the Windows RTX 3060 machine into the Epstein Files Analysis pipeline using the existing SSH infrastructure.

## Prerequisites

✅ **SSH Bidirectional Access**: 
- Windows ↔ Linux server (Galaxy) fully configured
- Passwordless authentication working
- Administrator access configured on Windows

✅ **Linux Server Ready**:
- Epstein pipeline infrastructure complete
- PostgreSQL database with 10.9M rows
- 94% document coverage (1.31M PDFs + 318GB parquet)

## Quick Start Guide

### Step 1: Initial Setup (One-time)

```bash
# On Linux server
cd /home/cbwinslow/workspace/epstein

# Run Windows setup script
uv run python scripts/setup_windows_gpu.py
```

This will:
- Install Python 3.12 on Windows
- Install CUDA Toolkit 12.4
- Install PyTorch with CUDA support
- Install all required Python packages
- Create project structure
- Test GPU availability

### Step 2: Test SSH Connection

```bash
# Test connection to Windows
ssh blaine@192.168.4.25

# Verify Python and GPU
python --version  # Should show 3.12.x
python -c "import torch; print(torch.cuda.is_available())"  # Should print True
```

### Step 3: Test Data Transfer

```bash
# Transfer a test file to Windows
rsync -avz /mnt/data/epstein-project/raw-files/data9/EFTA00000001.pdf blaine@192.168.4.25:C:\epstein-windows\data\test\EFTA00000001.pdf

# Verify file arrived
ssh blaine@192.168.4.25 "dir C:\epstein-windows\data\test"
```

### Step 4: Run First Task

```bash
# Process OCR on a small batch
uv run python scripts/distribute_tasks.py --task ocr --dataset data9 --batch-size 10

# Monitor performance
uv run python scripts/distribute_tasks.py --monitor
```

## Detailed Workflow

### 1. Environment Setup

#### 1.1 Windows Environment
```powershell
# PowerShell commands to run on Windows (if not using automated script)

# Install Python 3.12
Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile 'python-installer.exe'
.\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

# Install uv
iwr https://astral.sh/uv/install.ps1 -useb | iex

# Create project structure
mkdir C:\epstein-windows
mkdir C:\epstein-windows\data
mkdir C:\epstein-windows\processed
mkdir C:\epstein-windows\logs
mkdir C:\epstein-windows\scripts
```

#### 1.2 GPU Software Stack
```powershell
# Install CUDA Toolkit 12.4
Invoke-WebRequest -Uri 'https://developer.download.nvidia.com/compute/cuda/12.4.0/local_installers/cuda_12.4.0_551.61_windows.exe' -OutFile 'cuda-installer.exe'
.\cuda-installer.exe -s

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# Install dependencies
pip install pymupdf pyarrow pandas numpy scipy scikit-learn
pip install spacy insightface opencv-python-headless
pip install jiwer nervaluate networkx tqdm
pip install torchmetrics transformers sentence-transformers
pip install surya-ocr onnxruntime-gpu

# Install spaCy models
python -m spacy download en_core_web_trf
python -m spacy download en_core_web_sm
```

### 2. Task Distribution

#### 2.1 Automatic Task Assignment
The `distribute_tasks.py` script automatically:
- Discovers files in the specified dataset
- Estimates processing time for each machine
- Selects optimal machine based on performance + transfer overhead
- Transfers data to Windows if needed
- Executes tasks and tracks results

#### 2.2 Manual Task Assignment
```bash
# Force task to run on Windows
uv run python scripts/distribute_tasks.py --task ocr --dataset data9 --batch-size 50

# Force task to run on Linux (existing pipeline)
# Just use existing epstein-pipeline commands directly
epstein-pipeline ocr /mnt/data/epstein-project/raw-files/data9/ -o /tmp/ocr_output
```

### 3. Performance Monitoring

#### 3.1 Real-time Monitoring
```bash
# Monitor Windows GPU usage
ssh blaine@192.168.4.25 "python C:\epstein-windows\scripts\gpu_monitor.py"

# Monitor task progress
tail -f logs/task_distribution.log
```

#### 3.2 Performance Reports
```bash
# Generate performance report
uv run python scripts/distribute_tasks.py --monitor

# View report
cat logs/task_distribution_report.json | jq
```

### 4. Data Management

#### 4.1 Data Transfer Strategy
- **Initial Transfer**: Use rsync for bulk data transfer
- **Incremental Transfer**: Transfer only new files as needed
- **Results Transfer**: Push processed results back to Linux server

#### 4.2 Storage Organization
```
Windows (C:\epstein-windows\):
├── data/                    # Raw files from Linux
│   ├── data9/              # Dataset directories
│   └── batch/              # Temporary processing batches
├── processed/              # OCR results, NER output, face detection
├── logs/                   # Processing logs
└── scripts/                # Windows-specific scripts

Linux (/mnt/data/epstein-project/):
├── raw-files/              # Original PDFs
├── processed/              # Combined results from all machines
└── logs/                   # Centralized logs
```

### 5. Error Handling & Recovery

#### 5.1 Common Issues
- **SSH Connection Timeout**: Check network connectivity, increase timeout
- **GPU Memory Issues**: Reduce batch size, close other GPU applications
- **Data Transfer Failures**: Verify file permissions, check disk space
- **Package Import Errors**: Reinstall packages, check Python version

#### 5.2 Recovery Procedures
```bash
# Restart Windows worker
ssh blaine@192.168.4.25 "taskkill /f /im python.exe && python C:\epstein-windows\scripts\windows_worker.py"

# Clear failed tasks
uv run python scripts/distribute_tasks.py --clear-failed

# Re-transfer corrupted files
rsync -avz --checksum /mnt/data/epstein-project/raw-files/data9/ blaine@192.168.4.25:C:\epstein-windows\data\data9/
```

## Performance Expectations

### RTX 3060 vs Tesla K80 Performance

| Task Type | Tesla K80 | RTX 3060 | Improvement |
|-----------|-----------|----------|-------------|
| OCR Processing | 50-100 pages/min | 200-300 pages/min | 3-5x faster |
| Face Detection | 20-40 faces/sec | 50-100 faces/sec | 2-3x faster |
| NER Extraction | 500-1000 docs/min | 1500-2000 docs/min | 2-3x faster |
| Memory Capacity | 12GB shared | 12GB dedicated | Better batch sizes |

### Network Overhead
- **Data Transfer**: ~2-5 minutes for 100 files (100MB)
- **Result Transfer**: ~1 minute for processed results
- **SSH Latency**: <1ms local network

### Optimal Task Assignment
The system automatically assigns tasks based on:
1. **Task Type**: GPU-intensive tasks prefer Windows
2. **File Count**: Large batches offset transfer overhead
3. **Current Load**: Avoids overloading either machine
4. **Historical Performance**: Learns from past execution times

## Integration with Existing Pipeline

### 1. PostgreSQL Integration
Processed results from Windows are automatically merged into the central PostgreSQL database:
```sql
-- Results appear in the same tables as Linux processing
SELECT * FROM ocr_results WHERE source_machine = 'windows';
SELECT * FROM entities WHERE source_machine = 'windows';
```

### 2. Knowledge Graph Updates
Entities and relationships extracted on Windows are merged with the existing knowledge graph:
```python
# Automatic merging handled by the pipeline
# No manual intervention required
```

### 3. Search Index Updates
Processed text is automatically added to the FTS5 search index:
```sql
-- Search works across all processed documents regardless of processing machine
SELECT * FROM pages WHERE search_vector MATCH 'Epstein';
```

## Maintenance & Updates

### 1. Regular Maintenance
```bash
# Weekly: Update Windows drivers
ssh blaine@192.168.4.25 "powershell -Command \"Start-Process ms-settings:windowsupdate -Verb runas\""

# Monthly: Clean up temporary files
ssh blaine@192.168.4.25 "del /q C:\epstein-windows\data\batch\*"

# Quarterly: Performance review
uv run python scripts/distribute_tasks.py --monitor
```

### 2. Software Updates
```bash
# Update Python packages on Windows
ssh blaine@192.168.4.25 "pip install --upgrade torch torchvision torchaudio"
ssh blaine@192.168.4.25 "pip install --upgrade spacy insightface"

# Update Linux packages
uv run python scripts/setup_dev.py
```

### 3. Backup Strategy
```bash
# Backup Windows processing results
rsync -avz blaine@192.168.4.25:C:\epstein-windows\processed\ /mnt/data/epstein-project/backups\windows_processed\

# Backup task database
cp logs/task_distribution.db logs/backups/task_distribution_$(date +%Y%m%d).db
```

## Troubleshooting

### 1. SSH Issues
```bash
# Test SSH connection
ssh -v blaine@192.168.4.25

# Check SSH keys
ssh-add -l

# Regenerate keys if needed
ssh-keygen -t ed25519 -C "epstein-windows"
```

### 2. GPU Issues
```bash
# Check GPU availability on Windows
ssh blaine@192.168.4.25 "nvidia-smi"

# Test PyTorch CUDA
ssh blaine@192.168.4.25 "python -c \"import torch; print(torch.cuda.is_available())\""

# Check driver version
ssh blaine@192.168.4.25 "nvidia-smi --query-gpu=driver_version --format=csv,noheader,nounits"
```

### 3. Performance Issues
```bash
# Monitor GPU utilization
ssh blaine@192.168.4.25 "python C:\epstein-windows\scripts\gpu_monitor.py"

# Check for background processes
ssh blaine@192.168.4.25 "tasklist | findstr python"

# Optimize batch sizes
# Edit distribute_tasks.py DEFAULT_BATCH_SIZE
```

## Next Steps

1. **Phase 1**: Complete Windows setup and test basic functionality
2. **Phase 2**: Integrate with existing pipeline and run production workloads
3. **Phase 3**: Optimize performance and add monitoring dashboards
4. **Phase 4**: Scale to multiple Windows workers if needed

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `logs/task_distribution.log`
3. Monitor performance with `--monitor` flag
4. Test individual components with smaller batches

This integration provides a significant performance boost for the Epstein Files Analysis pipeline while maintaining compatibility with the existing infrastructure.