#!/usr/bin/env python3
"""
Sample Processing Script - OCR + NER Pipeline

Processes a sample of PDF files using PyMuPDF for OCR and spaCy for entity extraction.
Demonstrates the full processing pipeline on Epstein files.
"""

import spacy
import fitz
import os
import json
import time
from pathlib import Path
from collections import defaultdict

def process_pdf(pdf_path, nlp):
    """Process a single PDF file - extract text and entities."""
    try:
        doc = fitz.open(pdf_path)
        text = ''
        page_count = min(10, len(doc))  # Process up to 10 pages
        
        for page_num in range(page_count):
            page = doc.load_page(page_num)
            text += page.get_text()
        
        doc.close()
        
        if not text.strip():
            return None, 0, 0, []
        
        # Run NER
        doc_nlp = nlp(text)
        
        # Extract entities
        entities = []
        entity_counts = defaultdict(int)
        
        for ent in doc_nlp.ents:
            if ent.label_ in ['PERSON', 'ORG', 'GPE', 'DATE', 'MONEY', 'CARDINAL']:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char
                })
                entity_counts[ent.label_] += 1
        
        return text, len(text), page_count, entities
        
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None, 0, 0, []

def main():
    """Main processing function."""
    print("Epstein Files - Sample Processing Pipeline")
    print("=" * 50)
    
    # Load spaCy model
    try:
        nlp = spacy.load('en_core_web_sm')
        print("✓ spaCy model loaded successfully")
    except Exception as e:
        print(f"✗ spaCy model error: {e}")
        return
    
    # Configuration
    pdf_dir = '/mnt/data/epstein-project/raw-files/data9/'
    sample_size = 20  # Process 20 files for demonstration
    output_dir = '/home/cbwinslow/workspace/epstein/processed_sample/'
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Get sample files
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
    sample_files = pdf_files[:sample_size]
    
    print(f"Processing {len(sample_files)} PDF files...")
    print(f"Output directory: {output_dir}")
    print()
    
    # Processing statistics
    total_chars = 0
    total_entities = 0
    entity_type_counts = defaultdict(int)
    processing_times = []
    
    results = []
    
    # Process each file
    for i, pdf_file in enumerate(sample_files, 1):
        pdf_path = os.path.join(pdf_dir, pdf_file)
        
        start_time = time.time()
        text, char_count, page_count, entities = process_pdf(pdf_path, nlp)
        end_time = time.time()
        
        processing_time = end_time - start_time
        processing_times.append(processing_time)
        
        if text is None:
            print(f"{i:2d}/{len(sample_files):2d} {pdf_file}: SKIPPED (error)")
            continue
        
        # Update statistics
        total_chars += char_count
        total_entities += len(entities)
        
        for entity in entities:
            entity_type_counts[entity['label']] += 1
        
        # Save results
        result = {
            'filename': pdf_file,
            'char_count': char_count,
            'page_count': page_count,
            'processing_time': processing_time,
            'entities': entities,
            'sample_text': text[:500] if text else ""
        }
        
        results.append(result)
        
        # Print progress
        print(f"{i:2d}/{len(sample_files):2d} {pdf_file}: {char_count:6d} chars, {len(entities):3d} entities ({processing_time:.2f}s)")
    
    print()
    print("Processing Summary:")
    print("-" * 30)
    print(f"Files processed: {len(results)}/{len(sample_files)}")
    print(f"Total characters: {total_chars:,}")
    print(f"Total entities: {total_entities}")
    print(f"Average processing time: {sum(processing_times)/len(processing_times):.2f}s")
    print()
    
    print("Entity Type Distribution:")
    print("-" * 25)
    for entity_type, count in sorted(entity_type_counts.items()):
        print(f"  {entity_type:10s}: {count:4d}")
    
    # Save detailed results
    output_file = os.path.join(output_dir, 'processing_results.json')
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\\nDetailed results saved to: {output_file}")
    
    # Show sample entities
    print("\\nSample Entities Found:")
    print("-" * 20)
    sample_entities = []
    for result in results:
        for entity in result['entities'][:3]:  # Show first 3 entities per file
            sample_entities.append(f"{entity['text']} ({entity['label']})")
        if len(sample_entities) >= 15:
            break
    
    for entity in sample_entities[:15]:
        print(f"  {entity}")
    
    print(f"\\n✓ Processing complete! Processed {len(results)} files successfully.")

if __name__ == "__main__":
    main()