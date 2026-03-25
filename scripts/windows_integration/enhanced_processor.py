#!/usr/bin/env python3
"""
Enhanced Windows RTX 3060 Processing Worker with Surya OCR

This script uses state-of-the-art OCR (Surya) and NLP (spaCy) for processing
Epstein Files with maximum accuracy.

Features:
- Surya OCR: GPU-accelerated, transformer-based OCR
- PyMuPDF: Fast text extraction for text-layer PDFs
- spaCy: Advanced entity extraction
- Confidence scoring and quality metrics
- Batch processing optimization
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List

import fitz  # PyMuPDF
import numpy as np
import spacy
import torch
from PIL import Image
from surya.model.detection.model import load_model as load_detection_model
from surya.model.detection.processor import load_processor as load_detection_processor
from surya.model.recognition.model import load_model as load_recognition_model
from surya.model.recognition.processor import load_processor as load_recognition_processor
from surya.ocr import run_ocr

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedProcessor:
    def __init__(self):
        self.config = self.load_config()
        self.device = self.get_device()
        self.ocr_models = None
        self.nlp = None
        self.setup_models()

    def load_config(self) -> Dict:
        """Load configuration."""
        config_path = Path(__file__).parent / "config_windows.json"
        with open(config_path, 'r') as f:
            return json.load(f)

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
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("✅ spaCy model loaded")
        except Exception as e:
            logger.error(f"❌ Failed to load spaCy model: {e}")
            self.nlp = None

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
                "processing_time": 0.0
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
            pix = page.get_pixmap(dpi=200)  # 200 DPI for good quality
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

    def process_file(self, pdf_path: str, output_dir: str) -> bool:
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

            # Save results
            self.save_results(pdf_path, text_content, entities, quality_metrics, output_dir)

            logger.info("✅ Processing completed successfully")
            return True

        except Exception as e:
            logger.error(f"❌ Processing failed: {e}")
            return False

    def save_results(self, pdf_path: str, text_content: List[Dict], entities: List[Dict],
                    quality_metrics: Dict, output_dir: str):
        """Save processing results to JSON files."""
        base_name = Path(pdf_path).stem

        # Create output directory
        proc_subdir = Path(output_dir) / base_name
        proc_subdir.mkdir(exist_ok=True)

        # Save OCR results
        ocr_file = proc_subdir / f"{base_name}_ocr.json"
        with open(ocr_file, 'w', encoding='utf-8') as f:
            json.dump({
                "file": Path(pdf_path).name,
                "processing_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "quality_metrics": quality_metrics,
                "pages": text_content
            }, f, indent=2, ensure_ascii=False)

        # Save entity results
        entity_file = proc_subdir / f"{base_name}_entities.json"
        with open(entity_file, 'w', encoding='utf-8') as f:
            json.dump({
                "file": Path(pdf_path).name,
                "processing_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_entities": len(entities),
                "entities": entities
            }, f, indent=2, ensure_ascii=False)

        # Save summary
        summary_file = proc_subdir / f"{base_name}_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                "file": Path(pdf_path).name,
                "processing_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "quality_metrics": quality_metrics,
                "entity_summary": self.get_entity_summary(entities)
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"📁 Results saved to: {proc_subdir}")

    def get_entity_summary(self, entities: List[Dict]) -> Dict:
        """Get summary of extracted entities."""
        if not entities:
            return {"total": 0, "by_type": {}}

        entity_types = {}
        for entity in entities:
            label = entity['label']
            entity_types[label] = entity_types.get(label, 0) + 1

        return {
            "total": len(entities),
            "by_type": entity_types,
            "top_types": sorted(entity_types.items(), key=lambda x: x[1], reverse=True)[:10]
        }

    def run_processing_loop(self):
        """Main processing loop."""
        logger.info("🚀 Starting Enhanced Windows RTX 3060 processing worker...")

        downloads_dir = self.config['local_paths']['downloads']
        processing_dir = self.config['local_paths']['processing']
        results_dir = self.config['local_paths']['results']

        while True:
            try:
                # Look for new files to process
                pdf_files = list(Path(downloads_dir).glob("*.pdf"))

                if not pdf_files:
                    logger.info("⏳ No files to process, waiting...")
                    time.sleep(30)
                    continue

                logger.info(f"📁 Found {len(pdf_files)} files to process")

                for pdf_file in pdf_files:
                    logger.info(f"🎯 Processing: {pdf_file.name}")

                    # Create processing subdirectory
                    proc_subdir = Path(processing_dir) / pdf_file.stem
                    proc_subdir.mkdir(exist_ok=True)

                    # Process file
                    success = self.process_file(str(pdf_file), str(proc_subdir))

                    if success:
                        # Move to results
                        result_subdir = Path(results_dir) / pdf_file.stem
                        proc_subdir.rename(result_subdir)

                        # Remove original
                        pdf_file.unlink()

                        logger.info(f"✅ Completed processing: {pdf_file.name}")
                    else:
                        logger.error(f"❌ Failed to process: {pdf_file.name}")

            except KeyboardInterrupt:
                logger.info("🛑 Processing stopped by user")
                break
            except Exception as e:
                logger.error(f"❌ Processing error: {e}")
                time.sleep(60)

def main():
    """Main function."""
    processor = EnhancedProcessor()
    processor.run_processing_loop()

if __name__ == "__main__":
    main()
