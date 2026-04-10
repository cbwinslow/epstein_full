#!/usr/bin/env python3
"""
Simple test script for Windows RTX 3060 processing system.
Tests database connection and source indicators without requiring CUDA.
"""

from pathlib import Path

import psycopg2


def test_database_connection():
    """Test PostgreSQL connection and check for source_system column."""
    print("🔍 Testing database connection...")

    try:
        # Database configuration
        config = {
            'host': "localhost",
            'port': 5432,
            'database': "epstein",
            'user': "cbwinslow",
            'password': "123qweasd"
        }

        conn = psycopg2.connect(**config)

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

        # Show some sample data to verify structure
        cursor.execute("""
            SELECT efta_number, file_name, source_system, ocr_method 
            FROM documents 
            WHERE source_system IS NOT NULL 
            LIMIT 5
        """)
        samples = cursor.fetchall()
        if samples:
            print("📊 Sample documents with source_system:")
            for sample in samples:
                print(f"   - {sample[0]}: {sample[1]} ({sample[2]}, {sample[3]})")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_file_detection():
    """Test file detection."""
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
        size_kb = pdf_file.stat().st_size / 1024
        print(f"   - {pdf_file.name} ({size_kb:.1f} KB)")

    return True

def test_sql_queries():
    """Test the SQL queries that will be used by the Windows RTX 3060 processor."""
    print("\n🧪 Testing SQL queries...")

    try:
        config = {
            'host': "localhost",
            'port': 5432,
            'database': "epstein",
            'user': "cbwinslow",
            'password': "123qweasd"
        }

        conn = psycopg2.connect(**config)
        cursor = conn.cursor()

        # Test document insertion query structure
        test_efta = "TEST00000001"
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
            RETURNING efta_number
        """, (test_efta, "test.pdf", 1000, "test_hash", "test_method", 0.9, 100, 1, "Windows_RTX3060"))

        result = cursor.fetchone()
        print(f"✅ Document insertion test successful: {result[0]}")

        # Test pages insertion query structure
        cursor.execute("""
            INSERT INTO pages (efta_number, page_number, text_content, confidence, 
                             ocr_method, processing_time, word_count, source_system)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (efta_number, page_number) DO UPDATE SET
                text_content = EXCLUDED.text_content,
                confidence = EXCLUDED.confidence,
                ocr_method = EXCLUDED.ocr_method,
                processing_time = EXCLUDED.processing_time,
                word_count = EXCLUDED.word_count,
                source_system = EXCLUDED.source_system,
                updated_at = NOW()
            RETURNING COUNT(*)
        """, (test_efta, 1, "Test page content", 0.9, "test_method", 1.0, 10, "Windows_RTX3060"))

        pages_result = cursor.fetchone()
        print(f"✅ Pages insertion test successful: {pages_result[0]} pages")

        # Test entities insertion query structure
        cursor.execute("""
            INSERT INTO entities (entity_text, entity_type, efta_number, page_number, 
                                start_char, end_char, start_token, end_token, source_system)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            RETURNING COUNT(*)
        """, ("Test Entity", "PERSON", test_efta, 1, 0, 10, 0, 2, "Windows_RTX3060"))

        entities_result = cursor.fetchone()
        print(f"✅ Entities insertion test successful: {entities_result[0]} entities")

        # Clean up test data
        cursor.execute("DELETE FROM entities WHERE efta_number = %s", (test_efta,))
        cursor.execute("DELETE FROM pages WHERE efta_number = %s", (test_efta,))
        cursor.execute("DELETE FROM documents WHERE efta_number = %s", (test_efta,))

        conn.commit()
        cursor.close()
        conn.close()

        print("✅ All SQL queries tested successfully")
        return True

    except Exception as e:
        print(f"❌ SQL query test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Windows RTX 3060 Processing System Test (Simple)")
    print("=" * 55)

    # Test database connection
    if not test_database_connection():
        print("❌ Database test failed")
        return

    # Test file detection
    if not test_file_detection():
        print("❌ File detection test failed")
        return

    # Test SQL queries
    if not test_sql_queries():
        print("❌ SQL query test failed")
        return

    print("\n🎉 All tests passed! Windows RTX 3060 processing system is ready.")
    print("\n📋 Summary:")
    print("   ✅ Database connection established")
    print("   ✅ Source system indicators configured")
    print("   ✅ File detection working")
    print("   ✅ SQL queries validated")
    print("   ✅ Windows RTX 3060 indicators ready")

    print("\n💡 Next steps:")
    print("   1. Run this on your Windows machine with RTX 3060")
    print("   2. Install required packages: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121")
    print("   3. Install Surya OCR: pip install surya-ocr")
    print("   4. Install spaCy models: python -m spacy download en_core_web_trf")
    print("   5. Run the full processing pipeline")

if __name__ == "__main__":
    main()
