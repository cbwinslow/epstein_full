#!/usr/bin/env python3
"""
Optimized Windows RTX 3060 Processing Pipeline

Based on GitHub issues analysis and current bottlenecks:
- Phase 9.1: OCR pipeline on downloaded PDFs (HIGH PRIORITY)
- Phase 9.3: NER extraction on all document text (HIGH PRIORITY) 
- Current bottleneck: Only 268K PDFs downloaded, need to process all
- PostgreSQL has 2.9M pages but needs more OCR text content
- Need to integrate with existing Linux PostgreSQL database

This script optimizes for:
1. Maximum OCR accuracy with Surya + PyMuPDF smart detection
2. Fast NER extraction with spaCy transformer models
3. Direct PostgreSQL integration for entity storage
4. Batch processing for efficiency
5. Quality metrics and validation
"""

import concurrent.futures
import hashlib
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import fitz  # PyMuPDF
import numpy as np
import psycopg2
import spacy
import torch
from PIL import Image
from psycopg2.extras import execute_values
from surya.model.detection.model import load_model as load_detection_model
from surya.model.detection.processor import load_processor as load_detection_processor
from surya.model.recognition.model import load_model as load_recognition_model
from surya.model.recognition.processor import load_processor as load_recognition_processor
from surya.ocr import run_ocr

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ProcessingConfig:
    """Configuration for processing pipeline."""
    # Database settings
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "epstein"
    db_user: str = "cbwinslow"
    db_password: str = "123qweasd"

    # Processing settings
    batch_size: int = 100
    max_workers: int = 4
    dpi: int = 200
    confidence_threshold: float = 0.8

    # Paths
    downloads_dir: str = "downloads"
    results_dir: str = "results"
    temp_dir: str = "temp"

class OptimizedProcessor:
    def __init__(self, config: ProcessingConfig):
        self.config = config
        self.device = self.get_device()
        self.ocr_models = None
        self.nlp = None
        self.db_conn = None
        self.setup_models()
        self.setup_database()

    def get_device(self) -> str:
        """Get optimal device for processing."""
        if torch.cuda.is_available():
            device = "cuda"
            logger.info(f"✅ CUDA available: {torch.cuda.get_device_name(0)}")
        else:
            device = "cpu"
            logger.warning("⚠️ CUDA not available, using CPU")
        return device

    def setup_models(self):
        """Initialize OCR and NLP models."""
        logger.info("🚀 Initializing models...")

        # Initialize Surya OCR models
        try:
            self.ocr_models = {
                'detection_model': load_detection_model(),
                'detection_processor': load_detection_processor(),
                'recognition_model': load_recognition_model(),
                'recognition_processor': load_recognition_processor()
            }
            logger.info("✅ Surya OCR models loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load Surya models: {e}")
            self.ocr_models = None

        # Initialize spaCy
        try:
            self.nlp = spacy.load("en_core_web_trf")  # Use transformer model for better accuracy
            logger.info("✅ spaCy transformer model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load spaCy model: {e}")
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("✅ Fallback: spaCy small model loaded")
            except Exception as e2:
                logger.error(f"❌ Failed to load any spaCy model: {e2}")
                self.nlp = None

    def setup_database(self):
        """Setup PostgreSQL connection."""
        try:
            self.db_conn = psycopg2.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                database=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password
            )
            logger.info("✅ PostgreSQL connection established")
        except Exception as e:
            logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
            self.db_conn = None

    def is_text_layer_pdf(self, pdf_path: str) -> bool:
        """Check if PDF has a text layer (not scanned)."""
        try:
            doc = fitz.open(pdf_path)
            text = ""
            for page_num in range(min(3, len(doc))):  # Check first 3 pages
                page = doc.load_page(page_num)
                text += page.get_text()
                if len(text) > 100:  # If we find substantial text, it's likely text-layer
                    return True
            return False
        except Exception as e:
            logger.error(f"Error checking text layer: {e}")
            return False

    def extract_text_with_pymupdf(self, pdf_path: str) -> List[Dict]:
        """Extract text using PyMuPDF (fast for text-layer PDFs)."""
        logger.info(f"📄 Extracting text with PyMuPDF: {Path(pdf_path).name}")

        doc = fitz.open(pdf_path)
        text_content = []

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text()

            text_content.append({
                "page": page_num + 1,
                "text": text,
                "confidence": 1.0,  # PyMuPDF doesn't provide confidence
                "method": "pymupdf",
                "processing_time": 0.0,
                "word_count": len(text.split())
            })

        logger.info(f"✅ PyMuPDF extraction completed: {len(text_content)} pages")
        return text_content

    def extract_text_with_surya(self, pdf_path: str) -> List[Dict]:
        """Extract text using Surya OCR (best for scanned PDFs)."""
        if not self.ocr_models:
            logger.error("❌ Surya models not available")
            return []

        logger.info(f"🔍 Extracting text with Surya OCR: {Path(pdf_path).name}")

        doc = fitz.open(pdf_path)
        text_content = []

        for page_num in range(len(doc)):
            start_time = time.time()

            # Convert page to image
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=self.config.dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            # Run OCR
            predictions = run_ocr(
                [img],
                [doc.language if hasattr(doc, 'language') else 'en'],
                self.ocr_models['detection_model'],
                self.ocr_models['detection_processor'],
                self.ocr_models['recognition_model'],
                self.ocr_models['recognition_processor'],
                self.device
            )

            page_text = ""
            total_confidence = 0.0
            confidence_count = 0

            # Extract text and confidence from predictions
            for line in predictions[0].text_lines:
                page_text += line.text + " "
                total_confidence += line.confidence
                confidence_count += 1

            avg_confidence = total_confidence / confidence_count if confidence_count > 0 else 0.0
            processing_time = time.time() - start_time

            text_content.append({
                "page": page_num + 1,
                "text": page_text.strip(),
                "confidence": avg_confidence,
                "method": "surya_ocr",
                "processing_time": processing_time,
                "word_count": len(page_text.split())
            })

        logger.info(f"✅ Surya OCR completed: {len(text_content)} pages")
        return text_content

    def extract_entities(self, text_content: List[Dict]) -> List[Dict]:
        """Extract entities using spaCy."""
        if not self.nlp:
            logger.error("❌ spaCy model not available")
            return []

        logger.info("🏷️ Extracting entities with spaCy...")

        all_entities = []
        total_entities = 0

        for page_data in text_content:
            if not page_data['text'].strip():
                continue

            doc = self.nlp(page_data['text'])

            page_entities = []
            for ent in doc.ents:
                entity_data = {
                    "text": ent.text,
                    "label": ent.label_,
                    "page": page_data['page'],
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "start_token": ent.start,
                    "end_token": ent.end
                }
                page_entities.append(entity_data)
                all_entities.append(entity_data)

            total_entities += len(page_entities)

        logger.info(f"✅ Entity extraction completed: {total_entities} entities found")
        return all_entities

    def analyze_document_quality(self, text_content: List[Dict]) -> Dict:
        """Analyze document quality metrics."""
        total_pages = len(text_content)
        total_words = sum(page['word_count'] for page in text_content)
        avg_confidence = np.mean([page['confidence'] for page in text_content])
        processing_times = [page['processing_time'] for page in text_content]
        avg_processing_time = np.mean(processing_times) if processing_times else 0

        quality_metrics = {
            "total_pages": total_pages,
            "total_words": total_words,
            "avg_confidence": round(avg_confidence, 4),
            "avg_processing_time": round(avg_processing_time, 2),
            "pages_with_text": sum(1 for page in text_content if page['text'].strip()),
            "avg_words_per_page": round(total_words / total_pages, 2) if total_pages > 0 else 0,
            "ocr_method": text_content[0]['method'] if text_content else "unknown"
        }

        return quality_metrics

    def save_to_postgresql(self, pdf_path: str, text_content: List[Dict], entities: List[Dict],
                          quality_metrics: Dict):
        """Save processing results directly to PostgreSQL database."""
        if not self.db_conn:
            logger.error("❌ No database connection available")
            return False

        try:
            efta_number = Path(pdf_path).stem
            cursor = self.db_conn.cursor()

            # Calculate document hash for deduplication
            with open(pdf_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            # Insert document metadata with Windows RTX 3060 indicator
            cursor.execute("""
                INSERT INTO documents (efta_number, file_name, file_size_bytes, sha256_hash, 
                                     ocr_method, ocr_confidence, word_count, page_count, 
                                     source_system, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (efta_number) DO UPDATE SET
                    file_name = EXCLUDED.file_name,
                    file_size_bytes = EXCLUDED.file_size_bytes,
                    sha256_hash = EXCLUDED.sha256_hash,
                    ocr_method = EXCLUDED.ocr_method,
                    ocr_confidence = EXCLUDED.ocr_confidence,
                    word_count = EXCLUDED.word_count,
                    page_count = EXCLUDED.page_count,
                    source_system = EXCLUDED.source_system,
                    updated_at = NOW()
            """, (
                efta_number, Path(pdf_path).name, Path(pdf_path).stat().st_size, file_hash,
                quality_metrics['ocr_method'], quality_metrics['avg_confidence'],
                quality_metrics['total_words'], quality_metrics['total_pages'],
                "Windows_RTX3060"  # Clear indicator of Windows RTX 3060 processing
            ))

            # Insert pages with Windows RTX 3060 indicator
            page_data = []
            for page_data_item in text_content:
                page_data.append((
                    efta_number, page_data_item['page'], page_data_item['text'],
                    page_data_item['confidence'], page_data_item['method'],
                    page_data_item['processing_time'], page_data_item['word_count'],
                    "Windows_RTX3060"  # Clear indicator of Windows RTX 3060 processing
                ))

            execute_values(cursor, """
                INSERT INTO pages (efta_number, page_number, text_content, confidence, 
                                 ocr_method, processing_time, word_count, source_system)
                VALUES %s
                ON CONFLICT (efta_number, page_number) DO UPDATE SET
                    text_content = EXCLUDED.text_content,
                    confidence = EXCLUDED.confidence,
                    ocr_method = EXCLUDED.ocr_method,
                    processing_time = EXCLUDED.processing_time,
                    word_count = EXCLUDED.word_count,
                    source_system = EXCLUDED.source_system,
                    updated_at = NOW()
            """, page_data)

            # Insert entities with Windows RTX 3060 indicator
            entity_data = []
            for entity in entities:
                entity_data.append((
                    entity['text'], entity['label'], efta_number, entity['page'],
                    entity['start'], entity['end'], entity['start_token'], entity['end_token'],
                    "Windows_RTX3060"  # Clear indicator of Windows RTX 3060 processing
                ))

            if entity_data:
                execute_values(cursor, """
                    INSERT INTO entities (entity_text, entity_type, efta_number, page_number, 
                                        start_char, end_char, start_token, end_token, source_system)
                    VALUES %s
                    ON CONFLICT DO NOTHING
                """, entity_data)

            # Update FTS search vector for the document
            full_text = " ".join(page['text'] for page in text_content if page['text'].strip())
            if full_text:
                cursor.execute("""
                    UPDATE documents SET search_vector = to_tsvector('english', %s)
                    WHERE efta_number = %s
                """, (full_text, efta_number))

            self.db_conn.commit()
            cursor.close()

            logger.info(f"✅ Results saved to PostgreSQL for {efta_number}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to save to PostgreSQL: {e}")
            if self.db_conn:
                self.db_conn.rollback()
            return False

    def process_file(self, pdf_path: str) -> bool:
        """Process a single PDF file with optimal OCR method."""
        logger.info(f"🚀 Processing file: {Path(pdf_path).name}")

        try:
            # Determine best OCR method
            if self.is_text_layer_pdf(pdf_path):
                logger.info("📄 Detected text-layer PDF, using PyMuPDF")
                text_content = self.extract_text_with_pymupdf(pdf_path)
            else:
                logger.info("🔍 Detected scanned PDF, using Surya OCR")
                text_content = self.extract_text_with_surya(pdf_path)

            if not text_content:
                logger.error("❌ No text content extracted")
                return False

            # Extract entities
            entities = self.extract_entities(text_content)

            # Analyze quality
            quality_metrics = self.analyze_document_quality(text_content)

            # Save to PostgreSQL
            success = self.save_to_postgresql(pdf_path, text_content, entities, quality_metrics)

            if success:
                logger.info(f"✅ Processing completed successfully for {Path(pdf_path).name}")
                return True
            else:
                logger.error(f"❌ Failed to save results for {Path(pdf_path).name}")
                return False

        except Exception as e:
            logger.error(f"❌ Processing failed for {Path(pdf_path).name}: {e}")
            return False

    def process_batch(self, pdf_files: List[str]) -> Dict[str, Any]:
        """Process a batch of PDF files."""
        logger.info(f"📦 Processing batch of {len(pdf_files)} files")

        results = {
            "total_files": len(pdf_files),
            "successful": 0,
            "failed": 0,
            "total_pages": 0,
            "total_entities": 0,
            "avg_confidence": 0.0,
            "processing_time": 0.0
        }

        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            # Submit all tasks
            future_to_file = {executor.submit(self.process_file, pdf_file): pdf_file for pdf_file in pdf_files}

            # Process results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                pdf_file = future_to_file[future]
                try:
                    success = future.result()
                    if success:
                        results["successful"] += 1
                    else:
                        results["failed"] += 1
                except Exception as e:
                    logger.error(f"❌ Exception processing {pdf_file}: {e}")
                    results["failed"] += 1

        results["processing_time"] = time.time() - start_time
        logger.info(f"✅ Batch processing completed in {results['processing_time']:.2f} seconds")
        return results

    def run_processing_loop(self):
        """Main processing loop."""
        logger.info("🚀 Starting Optimized Windows RTX 3060 processing pipeline...")

        downloads_dir = Path(self.config.downloads_dir)
        if not downloads_dir.exists():
            logger.error("❌ Downloads directory not found")
            return

        while True:
            try:
                # Look for new files to process
                pdf_files = list(downloads_dir.glob("*.pdf"))

                if not pdf_files:
                    logger.info("⏳ No files to process, waiting...")
                    time.sleep(30)
                    continue

                logger.info(f"📁 Found {len(pdf_files)} files to process")

                # Process in batches
                batch_size = self.config.batch_size
                for i in range(0, len(pdf_files), batch_size):
                    batch = pdf_files[i:i + batch_size]
                    results = self.process_batch(batch)

                    # Log batch results
                    logger.info(f"📊 Batch Results: {results['successful']}/{results['total_files']} successful")
                    logger.info(f"📊 Total entities extracted: {results['total_entities']}")
                    logger.info(f"📊 Average confidence: {results['avg_confidence']:.4f}")

                # Wait before checking for new files
                logger.info("⏳ Waiting for new files...")
                time.sleep(60)

            except KeyboardInterrupt:
                logger.info("🛑 Processing stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Processing error: {e}")
                time.sleep(60)

def main():
    """Main function."""
    config = ProcessingConfig()
    processor = OptimizedProcessor(config)
    processor.run_processing_loop()

if __name__ == "__main__":
    main()
