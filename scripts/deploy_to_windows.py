#!/usr/bin/env python3
"""
Deploy Epstein Files Pipeline to Windows RTX 3060

This script transfers the processing pipeline to the Windows machine at 192.168.4.101
and sets up the complete environment with PostgreSQL database integration.
"""

import json
import os
import subprocess
import sys


def run_ssh_command(host, user, command, description):
    """Run a command on the Windows machine via SSH."""
    print(f"\\n{description}")
    print("-" * 50)
    print(f"Command: {command}")

    ssh_cmd = f'ssh {user}@{host} "{command}"'

    try:
        result = subprocess.run(ssh_cmd, shell=True, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            print("✓ Success")
            if result.stdout:
                print(f"Output: {result.stdout[:500]}...")
            return True
        else:
            print(f"✗ Failed with code {result.returncode}")
            if result.stderr:
                print(f"Error: {result.stderr[:500]}...")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Timeout")
        return False
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def transfer_files(host, user):
    """Transfer necessary files to Windows machine."""
    print("\\nTransferring files to Windows machine...")

    # Create remote directory structure
    run_ssh_command(host, user, 'mkdir -p C:\\\\epstein_pipeline\\\\scripts', "Creating remote directories")

    # Transfer setup script
    local_setup = '/home/cbwinslow/workspace/epstein/scripts/setup_windows_gpu.py'
    remote_setup = 'C:\\\\epstein_pipeline\\\\scripts\\\\setup_windows_gpu.py'

    scp_cmd = f'scp {local_setup} {user}@{host}:{remote_setup}'
    print(f"Transferring setup script: {scp_cmd}")
    os.system(scp_cmd)

    # Transfer processing script
    local_processing = '/home/cbwinslow/workspace/epstein/scripts/windows_processing.py'
    remote_processing = 'C:\\\\epstein_pipeline\\\\scripts\\\\windows_processing.py'

    scp_cmd = f'scp {local_processing} {user}@{host}:{remote_processing}'
    print(f"Transferring processing script: {scp_cmd}")
    os.system(scp_cmd)

    print("✓ Files transferred successfully")

def setup_windows_environment(host, user):
    """Set up the Windows environment."""
    print("\\nSetting up Windows environment...")

    # Install Python packages
    packages = [
        'torch==2.3.1+cu118',
        'torchvision==0.18.1+cu118',
        'torchaudio==2.3.1+cu118',
        'spacy==3.7.5',
        'fitz==1.24.4',
        'insightface==0.7.3',
        'onnxruntime-gpu==1.21.0',
        'faster-whisper==0.10.1',
        'sentence-transformers==3.0.1',
        'psycopg2-binary==2.9.9',
        'sqlalchemy==2.0.35',
        'pandas==2.2.2',
        'numpy==1.26.4',
        'opencv-python-headless==4.10.0.84',
        'pillow==11.1.0',
        'pyarrow==17.0.0',
        'huggingface-hub==0.26.2',
        'requests==2.32.3',
        'tqdm==4.66.5',
        'rapidfuzz==3.10.2',
        'scikit-learn==1.5.2',
        'networkx==3.4.2',
        'matplotlib==3.9.3',
        'seaborn==0.13.2'
    ]

    for package in packages:
        run_ssh_command(host, user, f'pip install {package}', f"Installing {package}")

    # Download spaCy model
    run_ssh_command(host, user, 'python -m spacy download en_core_web_trf', "Downloading spaCy model")

    # Create PostgreSQL database schema
    schema_sql = '''
    CREATE TABLE IF NOT EXISTS documents (
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

    CREATE TABLE IF NOT EXISTS entities (
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

    CREATE TABLE IF NOT EXISTS relationships (
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

    CREATE TABLE IF NOT EXISTS face_detections (
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

    CREATE TABLE IF NOT EXISTS transcriptions (
        id SERIAL PRIMARY KEY,
        source_file VARCHAR(255),
        duration_seconds FLOAT,
        text TEXT,
        segments JSONB,
        language VARCHAR(10) DEFAULT 'en',
        confidence FLOAT DEFAULT 0.0,
        metadata JSONB
    );

    CREATE INDEX IF NOT EXISTS idx_documents_efta ON documents(efta_number);
    CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
    CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);
    CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);
    CREATE INDEX IF NOT EXISTS idx_face_document ON face_detections(source_document);
    '''

    # Create database setup script
    db_setup_script = f'''
import psycopg2
import json

db_config = {{
    'host': 'localhost',
    'port': 5432,
    'database': 'epstein',
    'user': 'cbwinslow',
    'password': '123qweasd'
}}

schema_sql = {json.dumps(schema_sql)}

try:
    conn = psycopg2.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(schema_sql)
    conn.commit()
    cursor.close()
    conn.close()
    print("✓ PostgreSQL schema created successfully")
except Exception as e:
    print(f"✗ PostgreSQL setup failed: {{e}}")
'''

    # Transfer and run database setup
    with open('/tmp/setup_db.py', 'w') as f:
        f.write(db_setup_script)

    scp_cmd = f'scp /tmp/setup_db.py {user}@{host}:C:\\\\epstein_pipeline\\\\scripts\\\\setup_db.py'
    os.system(scp_cmd)

    run_ssh_command(host, user, 'python C:\\\\epstein_pipeline\\\\scripts\\\\setup_db.py', "Setting up PostgreSQL database")

def create_windows_launcher():
    """Create a Windows batch file for easy execution."""
    batch_content = '''@echo off
echo Epstein Files Processing Pipeline - Windows RTX 3060 Edition
echo ============================================================
echo.
echo GPU: RTX 3060 (12GB VRAM)
echo Database: PostgreSQL (epstein)
echo Processing: Multi-threaded with GPU acceleration
echo.
echo Starting processing pipeline...
echo.

cd /d C:\\epstein_pipeline\\scripts

REM Set environment variables
set PYTHONPATH=C:\\epstein_pipeline\\scripts;%PYTHONPATH%
set CUDA_VISIBLE_DEVICES=0

REM Run the processing pipeline
python windows_processing.py

echo.
echo Processing complete. Check the logs for details.
echo Report saved to: C:\\epstein_pipeline\\processed_windows\report.json
echo.
pause
'''

    with open('/tmp/epstein_pipeline.bat', 'w') as f:
        f.write(batch_content)

    print("✓ Windows launcher created")

def main():
    """Main deployment function."""
    host = '192.168.4.101'
    user = 'blain'

    print("Epstein Files - Windows RTX 3060 Deployment")
    print("="*50)
    print(f"Target: {user}@{host}")
    print()

    # Check SSH connectivity
    if not run_ssh_command(host, user, 'echo "SSH connection test successful"', "Testing SSH connection"):
        print("\\n✗ SSH connection failed")
        print("Please ensure:")
        print("1. SSH is enabled on the Windows machine")
        print("2. You can SSH to blain@192.168.4.101")
        print("3. You have proper SSH keys set up")
        return False

    # Transfer files
    transfer_files(host, user)

    # Set up environment
    setup_windows_environment(host, user)

    # Create launcher
    create_windows_launcher()

    print("\\n" + "="*60)
    print("WINDOWS DEPLOYMENT COMPLETE")
    print("="*60)
    print("\\nNext steps on Windows machine:")
    print("1. Open Command Prompt as Administrator")
    print("2. Navigate to C:\\\\epstein_pipeline\\\\scripts")
    print("3. Run: python setup_windows_gpu.py")
    print("4. Or run the batch file: epstein_pipeline.bat")
    print()
    print("Configuration:")
    print("- GPU: RTX 3060 (12GB VRAM)")
    print("- Database: PostgreSQL (epstein database)")
    print("- Processing: Multi-threaded with GPU acceleration")
    print("- Output: PostgreSQL database + JSON reports")
    print()
    print("Monitoring:")
    print("- SSH back to monitor progress: ssh blain@192.168.4.101")
    print("- Check logs in C:\\\\epstein_pipeline\\\\logs")
    print("- View reports in C:\\\\epstein_pipeline\\\\processed_windows")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
