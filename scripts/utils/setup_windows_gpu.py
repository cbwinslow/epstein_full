#!/usr/bin/env python3
"""
Windows RTX 3060 GPU Setup Script

Sets up the Epstein Files processing pipeline on Windows with RTX 3060 GPU
and PostgreSQL database integration.
"""

import os
import subprocess
import sys
import json
import time
from pathlib import Path

def run_command(cmd, description, cwd=None):
    """Run a command and return success status."""
    print(f"\\n{description}")
    print("-" * 50)
    print(f"Command: {cmd}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=600, cwd=cwd)
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

def check_windows_gpu():
    """Check if we're on Windows with RTX 3060."""
    print("\\nChecking Windows GPU environment...")
    
    # Check if we're on Windows
    if sys.platform != 'win32':
        print("✗ Not running on Windows")
        return False
    
    # Check GPU via nvidia-smi
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,memory.free', '--format=csv,noheader,nounits'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            gpu_info = result.stdout.strip()
            print(f"GPU Info: {gpu_info}")
            
            if 'RTX 3060' in gpu_info:
                print("✓ RTX 3060 detected")
                return True
            else:
                print("✗ RTX 3060 not detected")
                return False
        else:
            print("✗ nvidia-smi failed")
            return False
    except Exception as e:
        print(f"✗ GPU check failed: {e}")
        return False

def install_windows_dependencies():
    """Install Windows-specific dependencies."""
    print("\\nInstalling Windows dependencies...")
    
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
        run_command(f'pip install {package}', f"Installing {package}")

def setup_postgresql():
    """Set up PostgreSQL database connection."""
    print("\\nSetting up PostgreSQL database...")
    
    # Create database schema
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
    
    # Database connection parameters
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'epstein',
        'user': 'cbwinslow',
        'password': '123qweasd'
    }
    
    try:
        import psycopg2
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(schema_sql)
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ PostgreSQL schema created")
        return True
    except Exception as e:
        print(f"✗ PostgreSQL setup failed: {e}")
        return False

def create_windows_processing_script():
    """Create the main Windows processing script."""
    script_content = '''#!/usr/bin/env python3
"""
Epstein Files Processing Pipeline - Windows RTX 3060 Edition

Main processing script optimized for Windows with RTX 3060 GPU and PostgreSQL database.
"""

import os
import sys
import time
import json
import logging
import concurrent.futures
from pathlib import Path
from datetime import datetime
import fitz
import spacy
import psycopg2
import numpy as np
from PIL import Image
import cv2
import torch
from insightface.app import FaceAnalysis
from faster_whisper import WhisperModel
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EpsteinPipelineWindows:
    def __init__(self):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        logger.info(f"Using device: {self.device}")
        
        # Database connection
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'epstein',
            'user': 'cbwinslow',
            'password': '123qweasd'
        }
        
        # Load models
        self.load_models()
        
        # Statistics
        self.stats = {
            'processed_files': 0,
            'total_chars': 0,
            'total_entities': 0,
            'total_faces': 0,
            'processing_times': []
        }
    
    def load_models(self):
        """Load all ML models."""
        logger.info("Loading models...")
        
        # spaCy NER model
        try:
            self.nlp = spacy.load('en_core_web_trf')
            logger.info("✓ spaCy transformer model loaded")
        except Exception as e:
            logger.error(f"✗ spaCy model failed: {e}")
            self.nlp = None
        
        # InsightFace for facial recognition
        try:
            self.face_app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
            self.face_app.prepare(ctx_id=0, det_size=(640, 640))
            logger.info("✓ InsightFace model loaded")
        except Exception as e:
            logger.error(f"✗ InsightFace model failed: {e}")
            self.face_app = None
        
        # Whisper for transcription
        try:
            self.whisper_model = WhisperModel("large-v3", device=self.device, compute_type="float16")
            logger.info("✓ Whisper model loaded")
        except Exception as e:
            logger.error(f"✗ Whisper model failed: {e}")
            self.whisper_model = None
        
        # Sentence transformers for embeddings
        try:
            self.embedding_model = SentenceTransformer('nomic-embed-text-v2-moe', device=self.device)
            logger.info("✓ Embedding model loaded")
        except Exception as e:
            logger.error(f"✗ Embedding model failed: {e}")
            self.embedding_model = None
    
    def process_pdf(self, pdf_path):
        """Process a single PDF file."""
        start_time = time.time()
        
        try:
            # Extract text with PyMuPDF
            doc = fitz.open(pdf_path)
            text = ''
            page_count = min(20, len(doc))
            
            for page_num in range(page_count):
                page = doc.load_page(page_num)
                text += page.get_text()
            
            doc.close()
            
            if not text.strip():
                return None
            
            # Extract entities with spaCy
            entities = []
            if self.nlp:
                doc_nlp = self.nlp(text)
                for ent in doc_nlp.ents:
                    if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'MONEY', 'CARDINAL']:
                        entities.append({
                            'text': ent.text,
                            'label': ent.label_,
                            'start': ent.start_char,
                            'end': ent.end_char
                        })
            
            # Extract images and detect faces
            faces = []
            if self.face_app:
                for page_num in range(page_count):
                    page = doc.load_page(page_num)
                    image_list = page.get_images(full=True)
                    
                    for img_index, img in enumerate(image_list):
                        try:
                            xref = img[0]
                            base_image = doc.extract_image(xref)
                            image_bytes = base_image["image"]
                            
                            # Convert to PIL Image
                            pil_image = Image.open(io.BytesIO(image_bytes))
                            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                            
                            # Detect faces
                            faces_result = self.face_app.get(cv_image)
                            
                            for face in faces_result:
                                faces.append({
                                    'page': page_num,
                                    'bounding_box': face.bbox.tolist(),
                                    'embedding': face.embedding.tolist(),
                                    'confidence': float(face.det_score)
                                })
                        except Exception as e:
                            logger.warning(f"Face detection failed for image {img_index} in {pdf_path}: {e}")
            
            # Generate embeddings
            embeddings = []
            if self.embedding_model and text:
                # Generate embeddings for chunks of text
                chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
                embeddings = self.embedding_model.encode(chunks).tolist()
            
            # Store in database
            self.store_document(pdf_path, text, entities, faces, embeddings)
            
            processing_time = time.time() - start_time
            
            # Update statistics
            self.stats['processed_files'] += 1
            self.stats['total_chars'] += len(text)
            self.stats['total_entities'] += len(entities)
            self.stats['total_faces'] += len(faces)
            self.stats['processing_times'].append(processing_time)
            
            logger.info(f"Processed {os.path.basename(pdf_path)}: {len(text)} chars, {len(entities)} entities, {len(faces)} faces ({processing_time:.2f}s)")
            
            return {
                'filename': os.path.basename(pdf_path),
                'char_count': len(text),
                'entities': len(entities),
                'faces': len(faces),
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path}: {e}")
            return None
    
    def store_document(self, pdf_path, text, entities, faces, embeddings):
        """Store document and extracted data in PostgreSQL."""
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Insert document
            efta_number = os.path.basename(pdf_path).replace('.pdf', '')
            cursor.execute('''
                INSERT INTO documents (efta_number, file_name, file_type, page_count, ocr_text, ocr_confidence, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (efta_number) DO UPDATE SET
                    ocr_text = EXCLUDED.ocr_text,
                    ocr_confidence = EXCLUDED.ocr_confidence
            ''', (efta_number, os.path.basename(pdf_path), 'pdf', len(text.split('\\n')), text, 1.0, json.dumps({'source': 'windows_pipeline'})))
            
            # Insert entities
            for entity in entities:
                cursor.execute('''
                    INSERT INTO entities (name, entity_type, confidence, metadata, source_documents, source_pages)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (name, entity_type) DO UPDATE SET
                        mention_count = entities.mention_count + 1,
                        last_seen = CURRENT_TIMESTAMP
                ''', (entity['text'], entity['label'], 0.9, json.dumps({'source': pdf_path}), [efta_number], [1]))
            
            # Insert faces
            for face in faces:
                cursor.execute('''
                    INSERT INTO face_detections (source_document, source_page, bounding_box, embedding, confidence, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s)
                ''', (efta_number, face['page'], json.dumps(face['bounding_box']), 
                      face['embedding'], face['confidence'], json.dumps({'source': pdf_path})))
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database storage failed: {e}")
    
    def process_dataset(self, dataset_num, max_files=None):
        """Process all files in a dataset."""
        pdf_dir = f'/home/cbwinslow/workspace/epstein-data/raw-files/data{dataset_num}/'
        
        if not os.path.exists(pdf_dir):
            logger.error(f"Dataset {dataset_num} directory not found: {pdf_dir}")
            return []
        
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
        
        if max_files:
            pdf_files = pdf_files[:max_files]
        
        logger.info(f"Processing Dataset {dataset_num}: {len(pdf_files)} files")
        
        results = []
        file_paths = [os.path.join(pdf_dir, f) for f in pdf_files]
        
        # Process files with progress bar
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(self.process_pdf, path): path for path in file_paths}
            
            for future in concurrent.futures.as_completed(future_to_file):
                result = future.result()
                if result:
                    results.append(result)
        
        logger.info(f"✓ Dataset {dataset_num} complete: {len(results)} files processed")
        return results
    
    def generate_report(self):
        """Generate processing report."""
        logger.info("\\n" + "="*60)
        logger.info("EPSTEIN FILES PROCESSING REPORT - WINDOWS RTX 3060")
        logger.info("="*60)
        
        logger.info(f"\\nFiles processed: {self.stats['processed_files']:,}")
        logger.info(f"Total characters: {self.stats['total_chars']:,}")
        logger.info(f"Total entities: {self.stats['total_entities']:,}")
        logger.info(f"Total faces detected: {self.stats['total_faces']:,}")
        logger.info(f"Average processing time: {sum(self.stats['processing_times'])/len(self.stats['processing_times']):.3f}s")
        
        # Save report
        report_file = '/home/cbwinslow/workspace/epstein/processed_windows/report.json'
        os.makedirs(os.path.dirname(report_file), exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.stats, f, indent=2, default=str)
        
        logger.info(f"\\nReport saved to: {report_file}")
    
    def run_full_pipeline(self, datasets=None, max_files_per_dataset=None):
        """Run the full processing pipeline."""
        logger.info("Epstein Files - Windows RTX 3060 Processing Pipeline")
        logger.info("="*50)
        
        if datasets is None:
            datasets = [9, 10]  # Start with smaller datasets for testing
        
        all_results = []
        
        for dataset in datasets:
            start_time = time.time()
            results = self.process_dataset(dataset, max_files_per_dataset)
            end_time = time.time()
            
            if results:
                all_results.extend(results)
                logger.info(f"Dataset {dataset} time: {end_time - start_time:.2f}s")
        
        self.generate_report()
        logger.info(f"\\n✓ Pipeline complete! Processed {len(all_results)} files total.")

def main():
    """Main function."""
    pipeline = EpsteinPipelineWindows()
    
    # Example: Process datasets 9 and 10 with 100 files each for testing
    pipeline.run_full_pipeline(datasets=[9, 10], max_files_per_dataset=100)
    
    # For full processing (uncomment when ready):
    # pipeline.run_full_pipeline(datasets=[1,2,3,4,5,6,7,8,9,10,11,12])

if __name__ == "__main__":
    main()
'''
    
    with open('/home/cbwinslow/workspace/epstein/scripts/windows_processing.py', 'w') as f:
        f.write(script_content)
    
    logger.info("✓ Windows processing script created")

def create_ssh_config():
    """Create SSH configuration for Windows access."""
    ssh_config = '''
# Windows RTX 3060 Configuration
Host windows-rtx
    HostName 192.168.4.101
    User blain
    Port 22
    IdentityFile ~/.ssh/id_rsa
    ForwardAgent yes
    ServerAliveInterval 60
    ServerAliveCountMax 3
'''
    
    ssh_dir = Path.home() / '.ssh'
    ssh_dir.mkdir(exist_ok=True)
    
    config_file = ssh_dir / 'config'
    if config_file.exists():
        with open(config_file, 'a') as f:
            f.write(ssh_config)
    else:
        with open(config_file, 'w') as f:
            f.write(ssh_config)
    
    print("✓ SSH configuration updated for Windows RTX 3060")

def main():
    """Main setup function."""
    print("Epstein Files - Windows RTX 3060 Setup")
    print("="*50)
    
    # Check if we're on Windows with RTX 3060
    if not check_windows_gpu():
        print("\\n⚠️  Not running on Windows with RTX 3060")
        print("This script should be run on the Windows machine at 192.168.4.101")
        return False
    
    # Install dependencies
    install_windows_dependencies()
    
    # Set up PostgreSQL
    setup_postgresql()
    
    # Create processing script
    create_windows_processing_script()
    
    # Create SSH config
    create_ssh_config()
    
    print("\\n" + "="*60)
    print("WINDOWS RTX 3060 SETUP COMPLETE")
    print("="*60)
    print("\\nNext steps:")
    print("1. SSH to Windows machine: ssh blain@192.168.4.101")
    print("2. Run the processing script: python scripts/windows_processing.py")
    print("3. Monitor progress with: python scripts/dashboard.py")
    print("\\nConfiguration:")
    print("- GPU: RTX 3060 (12GB VRAM)")
    print("- Database: PostgreSQL (epstein database)")
    print("- Processing: Multi-threaded with GPU acceleration")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)