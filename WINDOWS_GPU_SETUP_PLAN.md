# Windows RTX 3060 Setup Plan for Epstein Files Analysis

## Overview

This plan outlines how to configure the Windows machine with RTX 3060 for distributed processing tasks in the Epstein Files Analysis pipeline, leveraging the existing SSH connection between Windows and the Linux server.

## Current Infrastructure Status

✅ **SSH Bidirectional Access**: 
- Windows ↔ Linux server (Galaxy) fully configured
- Passwordless authentication working
- Administrator access configured on Windows

✅ **Linux Server Ready**:
- Epstein pipeline infrastructure complete
- PostgreSQL database with 10.9M rows
- 94% document coverage (1.31M PDFs + 318GB parquet)
- GPU cluster: 2× Tesla K80 + 1× Tesla K40m

## Windows RTX 3060 Specifications

- **GPU**: NVIDIA GeForce RTX 3060 (8GB VRAM)
- **Architecture**: Ampere (Compute Capability 8.6)
- **CUDA Cores**: 3584
- **Tensor Cores**: 112 (3rd gen)
- **RT Cores**: 28 (2nd gen)
- **Memory**: 12GB GDDR6
- **Driver**: Latest NVIDIA Studio/GeForce driver

## Setup Strategy

### Phase 1: Windows Environment Preparation

#### 1.1 Install Python Environment
```bash
# On Windows via SSH
# Download Python 3.12 from python.org
# Install with "Add Python to PATH" checked
python --version  # Should show 3.12.x
```

#### 1.2 Install Package Manager
```bash
# Install uv (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or use pip
pip install uv
```

#### 1.3 Create Project Structure
```bash
# On Windows via SSH
mkdir C:\epstein-windows
cd C:\epstein-windows
mkdir data processed logs scripts
```

### Phase 2: GPU Software Stack

#### 2.1 Install CUDA Toolkit
```bash
# Download CUDA 12.4 from NVIDIA (RTX 3060 compatible)
# Install CUDA Toolkit + cuDNN
nvcc --version  # Should show CUDA 12.4
```

#### 2.2 Install PyTorch with CUDA
```bash
# Install PyTorch with CUDA 12.4 support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
python -c "import torch; print(torch.cuda.is_available())"  # Should print True
```

#### 2.3 Install Required Packages
```bash
# Core dependencies for Windows
pip install pymupdf pyarrow pandas numpy scipy scikit-learn
pip install spacy insightface opencv-python-headless
pip install jiwer nervaluate networkx tqdm
pip install torchmetrics transformers sentence-transformers
```

### Phase 3: Epstein Pipeline Components

#### 3.1 Install spaCy Models
```bash
python -m spacy download en_core_web_trf
python -m spacy download en_core_web_sm
```

#### 3.2 Install InsightFace
```bash
pip install insightface onnxruntime-gpu
# Test face recognition
python -c "import insightface; print('InsightFace installed')"
```

#### 3.3 Install OCR Tools
```bash
# Surya OCR (GPU-accelerated)
pip install surya-ocr
# Test OCR
python -c "from surya.ocr import run_ocr; print('Surya OCR ready')"
```

### Phase 4: Distributed Processing Architecture

#### 4.1 Task Distribution Strategy
```
Linux Server (Galaxy) → Windows RTX 3060
├── OCR Processing (GPU-intensive)
├── Facial Recognition (GPU-intensive)  
├── NER Extraction (CPU/GPU hybrid)
└── Transcription (GPU-intensive)
```

#### 4.2 Data Transfer Protocol
```bash
# Use rsync over SSH for efficient transfers
rsync -avz -e "ssh" /mnt/data/epstein-project/raw-files/data9/ blaine@192.168.4.25:/epstein-windows/data/
```

#### 4.3 Processing Queue System
```python
# Create task queue system
# Linux server assigns tasks to Windows worker
# Windows processes and returns results
```

### Phase 5: Implementation Plan

#### Week 1: Environment Setup
- [ ] Install Python 3.12 on Windows
- [ ] Install CUDA 12.4 + PyTorch
- [ ] Install all required Python packages
- [ ] Test GPU availability and performance

#### Week 2: Pipeline Integration
- [ ] Create Windows-specific processing scripts
- [ ] Implement SSH-based task distribution
- [ ] Set up data synchronization
- [ ] Test end-to-end workflow

#### Week 3: Optimization & Scaling
- [ ] Optimize batch sizes for RTX 3060
- [ ] Implement parallel processing
- [ ] Add monitoring and logging
- [ ] Performance benchmarking

#### Week 4: Production Deployment
- [ ] Integrate with main pipeline
- [ ] Add error handling and recovery
- [ ] Documentation and procedures
- [ ] Final testing and validation

## Technical Specifications

### RTX 3060 Performance Expectations
- **OCR Processing**: ~200-300 pages/minute (vs K80: ~50-100)
- **Facial Recognition**: ~50-100 faces/second
- **NER Extraction**: ~1000-2000 documents/minute
- **Memory Capacity**: 12GB VRAM (vs K80: 12GB shared)

### Network Requirements
- **SSH Connection**: Already established (192.168.4.25)
- **Bandwidth**: Gigabit Ethernet recommended
- **Latency**: <1ms local network
- **Security**: Key-based authentication

### Storage Strategy
- **Windows Storage**: Local SSD for processing
- **Data Sync**: Periodic rsync from Linux server
- **Results**: Push back to Linux server via SSH

## Implementation Scripts

### Windows Setup Script
```powershell
# setup_windows.ps1
# PowerShell script to automate Windows setup
```

### Task Distribution Script
```python
# distribute_tasks.py
# Python script to assign tasks to Windows worker
```

### Monitoring Script
```python
# monitor_windows.py
# Monitor Windows GPU usage and task progress
```

## Risk Mitigation

### GPU Driver Issues
- Use latest NVIDIA Studio drivers for stability
- Fallback to CPU processing if GPU unavailable

### Network Connectivity
- Implement retry logic for SSH connections
- Use compression for data transfer

### Data Consistency
- Implement checksums for file transfers
- Use atomic operations for result updates

## Expected Benefits

### Performance Improvements
- **OCR Speed**: 3-5x faster than Tesla K80
- **Face Recognition**: 2-3x faster processing
- **Overall Throughput**: 40-60% pipeline acceleration

### Resource Utilization
- **GPU Utilization**: 80-95% during processing
- **CPU Offloading**: Reduce Linux server load
- **Parallel Processing**: Handle multiple datasets simultaneously

### Cost Efficiency
- **Existing Hardware**: Leverage RTX 3060 already available
- **No Additional Costs**: Use existing infrastructure
- **Scalability**: Easy to add more Windows workers

## Next Steps

1. **Immediate**: Begin Windows environment setup
2. **Short-term**: Implement basic task distribution
3. **Medium-term**: Optimize for RTX 3060 performance
4. **Long-term**: Scale to multiple Windows workers

## Monitoring & Maintenance

### Performance Monitoring
- GPU utilization via nvidia-smi
- Task completion rates
- Error rates and recovery

### Maintenance Schedule
- Weekly driver updates
- Monthly performance reviews
- Quarterly optimization reviews

This plan provides a comprehensive roadmap for integrating the Windows RTX 3060 into the Epstein Files Analysis pipeline, leveraging the existing SSH infrastructure for distributed processing.