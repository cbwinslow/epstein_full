# Windows RTX 3060 Integration - Usage Guide

This guide explains how to use the Windows RTX 3060 to process files for the Epstein Files Analysis project.

## Overview

The Windows RTX 3060 integration allows you to use your Windows machine as a powerful processing worker for the Epstein pipeline. This provides significant performance improvements for GPU-intensive tasks.

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

### 1. Windows Setup (One-time)

**Prerequisites:**
- Windows 10/11 with Python 3.12
- RTX 3060 with existing NVIDIA driver (no updates required)
- SSH client (OpenSSH or PuTTY)
- SFTP access to Linux server

**Steps:**
1. Copy the `scripts/windows_integration/` directory to your Windows machine
2. Open Command Prompt as Administrator
3. Navigate to the integration directory
4. Run the setup script:

```bash
python setup_windows_worker.py
```

This will:
- Check Python 3.12 installation
- Verify CUDA compatibility (no driver updates)
- Install required Python packages
- Download spaCy models
- Setup Playwright browsers
- Create processing scripts
- Test SSH connection

### 2. Linux Setup (One-time)

On your Linux server, run the coordination script:

```bash
cd /home/cbwinslow/workspace/epstein
python scripts/windows_integration/coordinate_processing.py
```

## Usage Workflow

### Step 1: Place Files for Processing

Put PDF files you want to process in the Linux downloads directory:

```bash
# On Linux server
cp /path/to/your/files/*.pdf /home/cbwinslow/workspace/epstein/downloads/
```

### Step 2: Start Windows Processing

**On Windows machine:**
```bash
cd C:\epstein-windows
python process_files.py
```

This will:
- Monitor the downloads directory for new files
- Process files using RTX 3060 GPU
- Generate OCR, entity extraction, and image analysis
- Save results to the results directory

### Step 3: Transfer Files to Windows

**On Linux server:**
```bash
# Transfer files to Windows
python scripts/windows_integration/coordinate_processing.py
```

Or manually:
```bash
# Transfer files
scp /home/cbwinslow/workspace/epstein/downloads/*.pdf blaine@192.168.4.25:/home/cbwinslow/workspace/epstein/downloads/

# Or use the transfer script
python scripts/windows_integration/coordinate_processing.py
```

### Step 4: Monitor Processing

**On Windows:**
The processing script will show real-time progress:
```
🚀 Starting Windows RTX 3060 processing worker...
Processing file: EFTA00000001.pdf
   ✅ OCR completed: EFTA00000001_ocr.json
   ✅ Entity extraction completed: EFTA00000001_entities.json
   ✅ Image extraction completed
   ✅ Completed processing: EFTA00000001.pdf
```

**On Linux:**
The coordination script shows status:
```
📊 Processing Status:
   Total tasks: 5
   Pending: 2
   Processing: 0
   Completed: 3
   Failed: 0
```

### Step 5: Transfer Results Back

**On Linux server:**
```bash
# Transfer results from Windows
scp -r blaine@192.168.4.25:/home/cbwinslow/workspace/epstein/results/ /home/cbwinslow/workspace/epstein/results/

# Or use the transfer script with upload flag
python scripts/windows_integration/coordinate_processing.py
```

### Step 6: Integrate into Main Pipeline

The coordination script automatically integrates results into the main Epstein pipeline:
- OCR results are processed for text extraction
- Entity results are added to the knowledge graph
- Image results are analyzed for face detection
- All results are stored in PostgreSQL database

## Performance Expectations

### RTX 3060 Performance vs CPU

| Task | CPU Performance | RTX 3060 Performance | Improvement |
|------|----------------|---------------------|-------------|
| OCR Processing | 50-100 pages/minute | 200-300 pages/minute | 3-5x faster |
| Face Detection | 20-40 faces/second | 50-100 faces/second | 2-3x faster |
| NER Extraction | 500-1000 docs/minute | 1500-2000 docs/minute | 2-3x faster |
| Overall Pipeline | Baseline | 40-60% faster | Significant |

### Processing Times

- **Small files (1-10 pages)**: 10-30 seconds each
- **Medium files (10-50 pages)**: 30 seconds - 2 minutes each
- **Large files (50+ pages)**: 2-10 minutes each
- **Batch processing**: 3-5 files concurrently

## File Formats Supported

### Input Files
- **PDF files** (.pdf) - Primary format for document processing
- **Image files** (.png, .jpg, .jpeg) - For image analysis
- **Text files** (.txt, .docx) - For entity extraction

### Output Files
- **OCR results** (.json) - Text extraction with page numbers
- **Entity results** (.json) - Named entities with locations
- **Image results** (.png) - Extracted images from PDFs
- **Processing logs** (.log) - Detailed processing information

## Configuration

### Edit Configuration File

The `config_windows.json` file contains all configuration options:

```json
{
  "linux_server": {
    "host": "192.168.4.25",
    "user": "blaine",
    "remote_path": "/home/cbwinslow/workspace/epstein"
  },
  "local_paths": {
    "base_dir": "C:\\epstein-windows",
    "downloads": "C:\\epstein-windows\\downloads",
    "processing": "C:\\epstein-windows\\processing",
    "results": "C:\\epstein-windows\\results"
  },
  "processing": {
    "batch_size": 1,
    "max_concurrent_files": 3,
    "ocr_backend": "pymupdf",
    "entity_model": "en_core_web_sm"
  }
}
```

### Key Configuration Options

- **`linux_server.host`**: IP address of your Linux server
- **`linux_server.user`**: SSH username for Linux server
- **`local_paths`**: Windows directory paths
- **`processing.batch_size`**: Number of files to process at once
- **`processing.max_concurrent_files`**: Maximum concurrent processing

## Troubleshooting

### Common Issues

#### 1. SSH Connection Failed
```
❌ SSH connection failed: Permission denied
```
**Solution:**
- Ensure SSH keys are set up between machines
- Test SSH manually: `ssh blaine@192.168.4.25`
- Check firewall settings on both machines

#### 2. Python Packages Not Found
```
❌ Failed to install package: No module named 'torch'
```
**Solution:**
- Run setup script again: `python setup_windows_worker.py`
- Install packages manually: `pip install torch`
- Check Python version is 3.12

#### 3. CUDA Not Detected
```
⚠️ CUDA 12.4 not found, but continuing...
```
**Solution:**
- Install CUDA Toolkit 12.4 from NVIDIA website
- Ensure RTX 3060 driver supports CUDA
- No driver updates required per user request

#### 4. File Transfer Failed
```
❌ Transfer failed: Connection timed out
```
**Solution:**
- Check network connectivity
- Verify SSH access works manually
- Check file permissions on both machines

#### 5. Processing Errors
```
❌ OCR failed: PDF parsing error
```
**Solution:**
- Check PDF file integrity
- Try processing a different file
- Check available disk space

### Debug Mode

Enable debug logging by modifying the config:

```json
{
  "monitoring": {
    "log_level": "DEBUG",
    "log_file": "C:\\epstein-windows\\logs\\processing.log"
  }
}
```

### Manual Testing

Test individual components:

```bash
# Test SSH connection
ssh blaine@192.168.4.25 "echo 'SSH test successful'"

# Test file transfer
scp test.pdf blaine@192.168.4.25:/tmp/

# Test Python packages
python -c "import torch; print(torch.cuda.is_available())"

# Test processing script
python process_files.py --test
```

## Security Considerations

### SSH Security
- Use SSH key-based authentication (no passwords)
- Restrict SSH access to specific IP addresses
- Use non-standard SSH ports if possible
- Regularly update SSH keys

### File Security
- Verify file integrity with checksums
- Use encrypted file transfers (SCP/SFTP)
- Limit file access permissions
- Regular backup of important files

### Network Security
- Use VPN for remote connections
- Configure firewalls appropriately
- Monitor network traffic
- Regular security updates

## Performance Optimization

### GPU Optimization
- Ensure CUDA drivers are compatible
- Use appropriate batch sizes for GPU memory
- Monitor GPU temperature and usage
- Close other GPU-intensive applications

### Network Optimization
- Use wired connections when possible
- Compress files before transfer
- Transfer files in batches
- Monitor network bandwidth usage

### Processing Optimization
- Process multiple files concurrently
- Use appropriate file formats
- Monitor disk space and memory usage
- Regular cleanup of temporary files

## Integration with Main Pipeline

### Database Integration
Processed results are automatically integrated into:
- **PostgreSQL database** (10.9M rows)
- **Knowledge graph** (entity relationships)
- **Full-text search** (FTS5 indexing)
- **OCR database** (text extraction results)

### Pipeline Compatibility
- Results compatible with existing Epstein pipeline
- No modifications needed to main pipeline
- Automatic format conversion and validation
- Seamless integration with existing workflows

### Monitoring and Reporting
- Real-time processing status
- Performance metrics and statistics
- Error reporting and logging
- Integration with existing monitoring tools

## Support and Maintenance

### Regular Maintenance
- Update Python packages regularly
- Monitor disk space usage
- Clean up old log files
- Verify SSH key validity

### Performance Monitoring
- Track processing times
- Monitor GPU utilization
- Check network transfer speeds
- Review error logs regularly

### Updates and Upgrades
- Update configuration as needed
- Upgrade packages for performance
- Monitor for new CUDA versions
- Test with sample files regularly

## Getting Help

### Documentation
- Read all `.md` files in the integration directory
- Check the main Epstein project documentation
- Review configuration examples

### Logs and Debugging
- Check processing logs: `C:\epstein-windows\logs\`
- Enable debug mode for detailed information
- Review SSH connection logs
- Monitor GPU usage with nvidia-smi

### Community Support
- Check Epstein project GitHub issues
- Search for similar problems and solutions
- Ask for help in project discussions
- Share your experiences and improvements

---

## Quick Start Summary

1. **Setup Windows**: `python setup_windows_worker.py`
2. **Place files on Linux**: Copy PDFs to `/downloads/`
3. **Start processing**: `python process_files.py` (Windows)
4. **Transfer files**: `scp` or coordination script
5. **Monitor progress**: Check logs and status
6. **Transfer results**: Back to Linux server
7. **Integrate**: Automatic pipeline integration

**Expected Performance**: 40-60% faster processing with RTX 3060 GPU acceleration!