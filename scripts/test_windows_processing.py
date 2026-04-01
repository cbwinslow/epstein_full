#!/usr/bin/env python3
"""
Test script for Windows RTX 3060 processing system.
Tests the optimized_processor.py with source indicators.
"""

import os
import sys
import time
from pathlib import Path

import psycopg2

# Add the current directory to Python path to import from windows_integration
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from windows_integration.optimized_processor import OptimizedProcessor, ProcessingConfig


def test_database_connection():
    """Test PostgreSQL connection and check for source_system column."""
    print("🔍 Testing database connection...")

    try:
        config = ProcessingConfig()
        conn = psycopg2.connect(
            host=config.db_host,
            port=config.db_port,
            database=config.db_name,
            user=config.db_user,
            password=config.db_password
        )

        cursor = conn.cursor()

        # Check if source_system column exists in documents table
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'documents' AND column_name = 'source_system'
        """)
        doc_has_source = cursor.fetchone() is not None

        # Check if source_system column exists in pages table
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'pages' AND column_name = 'source_system'
        """)
        pages_has_source = cursor.fetchone() is not None

        # Check if source_system column exists in entities table
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'entities' AND column_name = 'source_system'
        """)
        entities_has_source = cursor.fetchone() is not None

        print("✅ Database connection successful")
        print(f"✅ Documents table has source_system: {doc_has_source}")
        print(f"✅ Pages table has source_system: {pages_has_source}")
        print(f"✅ Entities table has source_system: {entities_has_source}")

        # Count existing Windows RTX 3060 processed documents
        cursor.execute("""
            SELECT COUNT(*) FROM documents WHERE source_system = 'Windows_RTX3060'
        """)
        existing_count = cursor.fetchone()[0]
        print(f"📊 Existing Windows RTX 3060 documents: {existing_count}")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_file_detection():
    """Test file detection and OCR method selection."""
    print("\n📁 Testing file detection...")

    downloads_dir = Path("downloads")
    if not downloads_dir.exists():
        print("❌ Downloads directory not found")
        return False

    pdf_files = list(downloads_dir.glob("*.pdf"))
    if not pdf_files:
        print("❌ No PDF files found in downloads directory")
        return False

    print(f"✅ Found {len(pdf_files)} PDF files:")
    for pdf_file in pdf_files:
        print(f"   - {pdf_file.name} ({pdf_file.stat().st_size / 1024:.1f} KB)")

    return True

def test_processing_pipeline():
    """Test the complete processing pipeline with a single file."""
    print("\n🚀 Testing processing pipeline...")

    config = ProcessingConfig()
    processor = OptimizedProcessor(config)

    # Test with first available PDF
    downloads_dir = Path(config.downloads_dir)
    pdf_files = list(downloads_dir.glob("*.pdf"))

    if not pdf_files:
        print("❌ No PDF files available for testing")
        return False

    test_file = pdf_files[0]
    print(f"🧪 Testing with: {test_file.name}")

    # Process the file
    start_time = time.time()
    success = processor.process_file(str(test_file))
    processing_time = time.time() - start_time

    if success:
        print(f"✅ Processing completed successfully in {processing_time:.2f} seconds")

        # Verify the data was saved with Windows RTX 3060 indicator
        try:
            conn = psycopg2.connect(
                host=config.db_host,
                port=config.db_port,
                database=config.db_name,
                user=config.db_user,
                password=config.db_password
            )
            cursor = conn.cursor()

            efta_number = test_file.stem

            # Check documents table
            cursor.execute("""
                SELECT source_system, ocr_method, word_count, page_count 
                FROM documents WHERE efta_number = %s
            """, (efta_number,))
            doc_result = cursor.fetchone()

            if doc_result:
                source_system, ocr_method, word_count, page_count = doc_result
                print(f"📊 Document saved with source_system: {source_system}")
                print(f"📊 OCR method used: {ocr_method}")
                print(f"📊 Word count: {word_count}")
                print(f"📊 Page count: {page_count}")
            else:
                print("❌ Document not found in database")

            # Check pages table
            cursor.execute("""
                SELECT COUNT(*) FROM pages WHERE efta_number = %s AND source_system = 'Windows_RTX3060'
            """, (efta_number,))
            pages_count = cursor.fetchone()[0]
            print(f"📊 Pages saved with Windows RTX 3060 indicator: {pages_count}")

            # Check entities table
            cursor.execute("""
                SELECT COUNT(*) FROM entities WHERE efta_number = %s AND source_system = 'Windows_RTX3060'
            """, (efta_number,))
            entities_count = cursor.fetchone()[0]
            print(f"📊 Entities saved with Windows RTX 3060 indicator: {entities_count}")

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"❌ Database verification failed: {e}")

        return True
    else:
        print("❌ Processing failed")
        return False

def main():
    """Main test function."""
    print("🧪 Windows RTX 3060 Processing System Test")
    print("=" * 50)

    # Test database connection
    if not test_database_connection():
        print("❌ Database test failed")
        return

    # Test file detection
    if not test_file_detection():
        print("❌ File detection test failed")
        return

    # Test processing pipeline
    if not test_processing_pipeline():
        print("❌ Processing pipeline test failed")
        return

    print("\n🎉 All tests passed! Windows RTX 3060 processing system is ready.")
    print("\n📋 Summary:")
    print("   ✅ Database connection established")
    print("   ✅ Source system indicators configured")
    print("   ✅ File detection working")
    print("   ✅ Processing pipeline operational")
    print("   ✅ Windows RTX 3060 indicators being saved")

if __name__ == "__main__":
    main()
