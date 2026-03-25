#!/usr/bin/env python3
"""
Demo Enhanced Processing with Best Available OCR

This demonstrates the processing pipeline using the best available OCR
and entity extraction methods for Epstein Files.
"""

import json
import logging
import time
from pathlib import Path

import fitz  # PyMuPDF
import spacy

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_text_layer_pdf(pdf_path: str) -> bool:
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

def extract_text_with_pymupdf(pdf_path: str) -> list:
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

def extract_entities(text_content: list, nlp) -> list:
    """Extract entities using spaCy."""
    logger.info("🏷️ Extracting entities with spaCy...")

    all_entities = []
    total_entities = 0

    for page_data in text_content:
        if not page_data['text'].strip():
            continue

        doc = nlp(page_data['text'])

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

def analyze_document_quality(text_content: list) -> dict:
    """Analyze document quality metrics."""
    total_pages = len(text_content)
    total_words = sum(page['word_count'] for page in text_content)
    avg_confidence = sum(page['confidence'] for page in text_content) / total_pages
    processing_times = [page['processing_time'] for page in text_content]
    avg_processing_time = sum(processing_times) / len(processing_times) if processing_times else 0

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

def process_file(pdf_path: str, output_dir: str, nlp) -> bool:
    """Process a single PDF file."""
    logger.info(f"🚀 Processing file: {Path(pdf_path).name}")

    try:
        # Extract text
        text_content = extract_text_with_pymupdf(pdf_path)

        if not text_content:
            logger.error("❌ No text content extracted")
            return False

        # Extract entities
        entities = extract_entities(text_content, nlp)

        # Analyze quality
        quality_metrics = analyze_document_quality(text_content)

        # Save results
        base_name = Path(pdf_path).stem
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
            entity_types = {}
            for entity in entities:
                label = entity['label']
                entity_types[label] = entity_types.get(label, 0) + 1

            json.dump({
                "file": Path(pdf_path).name,
                "processing_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "quality_metrics": quality_metrics,
                "entity_summary": {
                    "total": len(entities),
                    "by_type": entity_types,
                    "top_types": sorted(entity_types.items(), key=lambda x: x[1], reverse=True)[:10]
                }
            }, f, indent=2, ensure_ascii=False)

        logger.info(f"📁 Results saved to: {proc_subdir}")
        logger.info("✅ Processing completed successfully")
        return True

    except Exception as e:
        logger.error(f"❌ Processing failed: {e}")
        return False

def main():
    """Main function."""
    logger.info("🚀 Starting Enhanced Processing Demo...")

    # Check available files
    downloads_dir = Path("downloads")
    if not downloads_dir.exists():
        logger.error("❌ Downloads directory not found")
        return

    pdf_files = list(downloads_dir.glob("*.pdf"))
    if not pdf_files:
        logger.error("❌ No PDF files found in downloads directory")
        return

    logger.info(f"📁 Found {len(pdf_files)} files to process")

    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("✅ spaCy model loaded")
    except Exception as e:
        logger.error(f"❌ Failed to load spaCy model: {e}")
        return

    # Process each file
    for pdf_file in pdf_files:
        logger.info(f"🎯 Processing: {pdf_file.name}")

        # Determine if it's text-layer or scanned
        if is_text_layer_pdf(str(pdf_file)):
            logger.info("📄 Detected text-layer PDF, using PyMuPDF")
        else:
            logger.info("🔍 Detected scanned PDF, would use Surya OCR (not available in demo)")

        # Process file
        success = process_file(str(pdf_file), "results", nlp)

        if success:
            logger.info(f"✅ Completed processing: {pdf_file.name}")
        else:
            logger.error(f"❌ Failed to process: {pdf_file.name}")

    logger.info("🎉 Processing demo completed!")

if __name__ == "__main__":
    main()
