# Windows RTX 3060 Setup Guide

## Overview

This guide sets up the Epstein Files processing pipeline on a Windows machine with RTX 3060 GPU and PostgreSQL database integration. The pipeline performs OCR, Named Entity Recognition (NER), facial recognition, and stores results in a PostgreSQL database.

## Prerequisites

### Hardware Requirements
- **GPU**: NVIDIA RTX 3060 (12GB VRAM)
- **RAM**: 32GB minimum, 64GB recommended
- **Storage**: 1TB SSD (for processing and database)
- **Network**: Stable internet connection for downloads

### Software Requirements
- **OS**: Windows 10/11 (64-bit)
- **Python**: 3.10+ (64-bit)
- **PostgreSQL**: 12+ with pgvector extension
- **CUDA**: 11.8 compatible drivers

### Network Access
- SSH access to Windows machine: `blain@192.168.4.101`
- Access to data storage: `/home/cbwinslow/workspace/epstein-data/`

## Quick Start

### 1. Deploy to Windows

From the Linux machine, run the deployment script:

```bash
cd /home/cbwinslow/workspace/epstein
python scripts/deploy_to_windows.py
```

This will:
- Transfer setup scripts to Windows
- Install all required Python packages
- Set up PostgreSQL database schema
- Create launch scripts

### 2. SSH to Windows Machine

```bash
ssh blain@192.168.4.101
```

### 3. Run Setup on Windows

```cmd
cd C:\epstein_pipeline\scripts
python setup_windows_gpu.py
```

### 4. Start Processing

```cmd
# Option 1: Run the batch file (easiest)
epstein_pipeline.bat

# Option 2: Run directly
python windows_processing.py
```

## Detailed Setup Instructions

### Manual Setup (Alternative to Automated Deployment)

#### Step 1: Install Python Packages

```cmd
pip install torch==2.3.1+cu118 torchvision==0.18.1+cu118 torchaudio==2.3.1+cu118
pip install spacy==3.7.5 fitz==1.24.4 insightface==0.7.3 onnxruntime-gpu==1.21.0
pip install faster-whisper==0.10.1 sentence-transformers==3.0.1 psycopg2-binary==2.9.9
pip install sqlalchemy==2.0.35 pandas==2.2.2 numpy==1.26.4 opencv-python-headless==4.10.0.84
pip install pillow==11.1.0 pyarrow==17.0.0 huggingface-hub==0.26.2 requests==2.32.3
pip install tqdm==4.66.5 rapidfuzz==3.10.2 scikit-learn==1.5.2 networkx==3.4.2
pip install matplotlib==3.9.3 seaborn==0.13.2
```

#### Step 2: Download spaCy Model

```cmd
python -m spacy download en_core_web_trf
```

#### Step 3: Set Up PostgreSQL Database

```sql
-- Connect to PostgreSQL and run:
CREATE DATABASE epstein;

-- Connect to epstein database and create schema:
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(20) UNIQUE NOT NULL,
    dataset_id INTEGER,
    file_name VARCHAR(255),
    file_type VARCHAR(50),
    page_count INTEGER DEFAULT 1,
    ocr_text TEXT,
    ocr_confidence FLOAT DEFAULT 0.0,
    document_type VARCHAR(50),
    classification_confidence FLOAT DEFAULT 0.0,
    redaction_count INTEGER DEFAULT 0,
    source_url TEXT,
    sha256_hash VARCHAR(64),
    file_size_bytes BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    aliases TEXT[],
    mention_count INTEGER DEFAULT 0,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    confidence FLOAT DEFAULT 0.0,
    metadata JSONB,
    source_documents TEXT[],
    source_pages INTEGER[]
);

CREATE TABLE relationships (
    id SERIAL PRIMARY KEY,
    source_entity_id INTEGER REFERENCES entities(id),
    target_entity_id INTEGER REFERENCES entities(id),
    relationship_type VARCHAR(50) NOT NULL,
    weight FLOAT DEFAULT 1.0,
    confidence FLOAT DEFAULT 0.0,
    context TEXT,
    source_document VARCHAR(20),
    metadata JSONB
);

CREATE TABLE face_detections (
    id SERIAL PRIMARY KEY,
    source_document VARCHAR(20),
    source_page INTEGER,
    bounding_box JSONB,
    embedding VECTOR(512),
    identity_label VARCHAR(255),
    confidence FLOAT DEFAULT 0.0,
    similarity_score FLOAT DEFAULT 0.0,
    metadata JSONB
);

CREATE TABLE transcriptions (
    id SERIAL PRIMARY KEY,
    source_file VARCHAR(255),
    duration_seconds FLOAT,
    text TEXT,
    segments JSONB,
    language VARCHAR(10) DEFAULT 'en',
    confidence FLOAT DEFAULT 0.0,
    metadata JSONB
);

-- Create indexes
CREATE INDEX idx_documents_efta ON documents(efta_number);
CREATE INDEX idx_entities_name ON entities(name);
CREATE INDEX idx_relationships_source ON relationships(source_entity_id);
CREATE INDEX idx_relationships_target ON relationships(target_entity_id);
CREATE INDEX idx_face_document ON face_detections(source_document);
```

#### Step 4: Configure Database Connection

Edit the database configuration in `windows_processing.py`:

```python
self.db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'epstein',
    'user': 'cbwinslow',
    'password': '123qweasd'
}
```

#### Step 5: Run Processing

```cmd
cd C:\epstein_pipeline\scripts
python windows_processing.py
```

## Processing Pipeline Details

### What Gets Processed

1. **OCR (Optical Character Recognition)**
   - Extracts text from PDF documents using PyMuPDF
   - Handles both text-layer and scanned documents
   - Confidence scoring for each page

2. **Named Entity Recognition (NER)**
   - Identifies people, organizations, locations, dates
   - Uses spaCy transformer model (GPU-accelerated)
   - Extracts financial amounts and case numbers

3. **Facial Recognition**
   - Detects faces in extracted images
   - Generates 512-dimensional embeddings using InsightFace
   - Clusters faces by identity

4. **Transcription (Audio/Video)**
   - Processes audio and video files
   - Uses faster-whisper for speech-to-text
   - Includes speaker diarization

5. **Embeddings and Classification**
   - Generates text embeddings for semantic search
   - Classifies document types
   - Stores vectors in PostgreSQL

### Output Data

All processed data is stored in PostgreSQL with the following structure:

- **documents**: Raw text, metadata, OCR confidence
- **entities**: Extracted entities with types and confidence
- **relationships**: Entity relationships with weights
- **face_detections**: Face embeddings and metadata
- **transcriptions**: Audio/video transcriptions

### Performance Expectations

- **RTX 3060**: ~10-15 files/minute processing speed
- **Memory usage**: ~4-8GB GPU memory during processing
- **Storage**: ~50GB for processed data (estimates)
- **Database size**: ~100GB for full dataset

## Monitoring and Troubleshooting

### Monitoring Progress

1. **Real-time logs**: Check console output during processing
2. **Database queries**: Monitor row counts in tables
3. **GPU usage**: Use Task Manager or nvidia-smi

### Common Issues

#### GPU Memory Errors
```cmd
# Reduce batch sizes in the processing script
# Or process smaller datasets first
```

#### Database Connection Issues
```cmd
# Check PostgreSQL service is running
# Verify credentials in db_config
# Check firewall settings
```

#### Missing Dependencies
```cmd
# Re-run setup script
python setup_windows_gpu.py
```

#### Slow Processing
```cmd
# Check GPU utilization
# Verify CUDA drivers are up to date
# Reduce concurrent workers
```

### Log Files

- **Processing logs**: `C:\epstein_pipeline\logs\`
- **Error logs**: Console output and Windows Event Viewer
- **Database logs**: PostgreSQL log directory

## Integration with Existing Infrastructure

### Data Sources

The pipeline can process data from:

1. **Local storage**: `/home/cbwinslow/workspace/epstein-data/raw-files/data{N}/`
2. **HuggingFace parquet**: Pre-extracted text data
3. **Existing databases**: Can merge with existing knowledge graphs

### Database Integration

The PostgreSQL database integrates with:

- **Existing knowledge graph**: Can merge entities and relationships
- **Full-text search**: FTS5 indexing for document search
- **Vector search**: pgvector for semantic similarity

### API Access

The processed data can be accessed via:

- **SQL queries**: Direct database access
- **Python API**: SQLAlchemy ORM
- **REST API**: Can be built on top of the database

## Security Considerations

### Data Security
- **Encryption**: Use SSL for database connections
- **Access control**: Limit database user permissions
- **Backup**: Regular database backups

### System Security
- **Firewall**: Configure appropriate rules
- **Updates**: Keep Windows and drivers updated
- **Antivirus**: Ensure compatibility with processing software

## Advanced Configuration

### Custom Entity Types

Modify the NER section to extract custom entity types:

```python
# Add custom entity types to extraction
if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'MONEY', 'CARDINAL', 'CUSTOM_TYPE']:
```

### Custom Processing

Extend the pipeline for additional processing:

```python
# Add custom processing functions
def custom_processing(self, text):
    # Your custom logic here
    pass
```

### Performance Tuning

Optimize for your specific hardware:

```python
# Adjust batch sizes and worker counts
MAX_WORKERS = 4  # Adjust based on CPU cores
BATCH_SIZE = 32  # Adjust based on GPU memory
```

## Support and Maintenance

### Regular Maintenance

1. **Database maintenance**: Regular VACUUM and ANALYZE
2. **Disk cleanup**: Monitor storage usage
3. **Software updates**: Keep packages updated

### Getting Help

- **Documentation**: This guide and project README
- **Logs**: Check processing logs for errors
- **Community**: Project GitHub issues and discussions

## Next Steps

After successful setup:

1. **Process test dataset**: Start with smaller datasets
2. **Validate results**: Check entity extraction quality
3. **Scale up**: Process larger datasets
4. **Analysis**: Use processed data for research
5. **Visualization**: Create dashboards and reports

## Contact

For issues or questions:
- Check the project documentation
- Review processing logs
- Contact the development team