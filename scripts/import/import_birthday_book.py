#!/usr/bin/env python3
"""
Import Birthday Book from epstein-network-data
Source: dleerdefi/epstein-network-data/data/extracted/v1 - first pass/birthday_book/

Imports:
- 128 pages with full analysis JSON
- Entities (people mentioned)
- Visual analysis (photos, signatures, redactions)
- Insights and forensic notes
- Timeline markers

Tables created:
- birthday_book_pages
- birthday_book_entities (people mentioned in pages)
- birthday_book_photos (photos found on pages)
- birthday_book_signatures (signatures found)
"""

import os
import sys
import json
import asyncio
import asyncpg
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Base path to extracted birthday book data
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/extracted/v1 - first pass/birthday_book")

# PostgreSQL connection
DB_URL = os.environ.get("EPSTEIN_DB_URL", "postgresql://cbwinslow:123qweasd@localhost:5432/epstein")


async def create_tables(conn: asyncpg.Connection):
    """Create Birthday Book tables."""
    print("Creating Birthday Book tables...")
    
    # Drop existing tables
    await conn.execute("DROP TABLE IF EXISTS birthday_book_entities CASCADE")
    await conn.execute("DROP TABLE IF EXISTS birthday_book_photos CASCADE")
    await conn.execute("DROP TABLE IF EXISTS birthday_book_signatures CASCADE")
    await conn.execute("DROP TABLE IF EXISTS birthday_book_redactions CASCADE")
    await conn.execute("DROP TABLE IF EXISTS birthday_book_pages CASCADE")
    
    # Main pages table
    await conn.execute("""
        CREATE TABLE birthday_book_pages (
            id SERIAL PRIMARY KEY,
            page_number INTEGER NOT NULL UNIQUE,
            file_path TEXT,
            file_size_mb FLOAT,
            page_type VARCHAR(50),
            full_text TEXT,
            transcription TEXT,
            annotations TEXT[],
            sender TEXT,
            recipient TEXT,
            page_date DATE,
            subject TEXT,
            significance VARCHAR(20),
            theme TEXT,
            document_type VARCHAR(50),
            insights TEXT[],
            document_id VARCHAR(100),
            processed_at TIMESTAMP,
            extraction_version VARCHAR(10),
            quality_score INTEGER,
            requires_review BOOLEAN,
            contains_sensitive_info BOOLEAN,
            extraction_complete BOOLEAN,
            review_notes TEXT[],
            forensic_notes TEXT[],
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Entities (people mentioned)
    await conn.execute("""
        CREATE TABLE birthday_book_entities (
            id SERIAL PRIMARY KEY,
            page_number INTEGER NOT NULL REFERENCES birthday_book_pages(page_number) ON DELETE CASCADE,
            name TEXT NOT NULL,
            title TEXT,
            relationship TEXT,
            context TEXT,
            confidence VARCHAR(20),
            page_appearances INTEGER[],
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Photos found on pages
    await conn.execute("""
        CREATE TABLE birthday_book_photos (
            id SERIAL PRIMARY KEY,
            page_number INTEGER NOT NULL REFERENCES birthday_book_pages(page_number) ON DELETE CASCADE,
            photo_description TEXT,
            photo_type VARCHAR(50),
            people_in_photo TEXT[],
            location_in_photo TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Signatures found
    await conn.execute("""
        CREATE TABLE birthday_book_signatures (
            id SERIAL PRIMARY KEY,
            page_number INTEGER NOT NULL REFERENCES birthday_book_pages(page_number) ON DELETE CASCADE,
            signer_name TEXT,
            signature_type VARCHAR(50),
            confidence VARCHAR(20),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Redactions
    await conn.execute("""
        CREATE TABLE birthday_book_redactions (
            id SERIAL PRIMARY KEY,
            page_number INTEGER NOT NULL REFERENCES birthday_book_pages(page_number) ON DELETE CASCADE,
            redaction_description TEXT,
            redaction_type VARCHAR(50),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Create indexes
    await conn.execute("CREATE INDEX idx_bb_entities_name ON birthday_book_entities(name)")
    await conn.execute("CREATE INDEX idx_bb_entities_page ON birthday_book_entities(page_number)")
    await conn.execute("CREATE INDEX idx_bb_photos_page ON birthday_book_photos(page_number)")
    await conn.execute("CREATE INDEX idx_bb_signatures_name ON birthday_book_signatures(signer_name)")
    
    print("✓ Tables created")


async def import_pages(conn: asyncpg.Connection) -> Dict[str, int]:
    """Import all birthday book pages."""
    print(f"Importing pages from {BASE_DIR}...")
    
    counts = {"pages": 0, "entities": 0, "photos": 0, "signatures": 0, "redactions": 0}
    
    # Get all analysis JSON files
    json_files = sorted(BASE_DIR.glob("page_*_analysis.json"))
    print(f"Found {len(json_files)} analysis files")
    
    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            page_number = data.get('page_number')
            if not page_number:
                continue
            
            # Parse date if available
            page_date = None
            if data.get('metadata', {}).get('date'):
                date_str = data['metadata']['date']
                # Try to extract date from string like "January 20, 2003"
                try:
                    page_date = datetime.strptime(date_str.split('(')[0].strip(), "%B %d, %Y").date()
                except:
                    pass
            
            # Parse processed_at
            processed_at = None
            if data.get('processed_at'):
                try:
                    processed_at = datetime.fromisoformat(data['processed_at'].replace(' ', 'T'))
                except:
                    pass
            
            # Insert page
            await conn.execute("""
                INSERT INTO birthday_book_pages (
                    page_number, file_path, file_size_mb, page_type,
                    full_text, transcription, annotations,
                    sender, recipient, page_date, subject,
                    significance, theme, document_type,
                    insights, document_id, processed_at, extraction_version,
                    quality_score, requires_review, contains_sensitive_info,
                    extraction_complete, review_notes, forensic_notes
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21, $22, $23, $24)
                ON CONFLICT (page_number) DO UPDATE SET
                    file_path = EXCLUDED.file_path,
                    full_text = EXCLUDED.full_text,
                    transcription = EXCLUDED.transcription,
                    quality_score = EXCLUDED.quality_score
                RETURNING page_number
            """,
                page_number,
                data.get('file_path'),
                data.get('file_size_mb'),
                data.get('type'),
                data.get('content', {}).get('text'),
                data.get('content', {}).get('text_sections', {}).get('full_transcription'),
                data.get('content', {}).get('text_sections', {}).get('annotations'),
                data.get('metadata', {}).get('sender'),
                data.get('metadata', {}).get('recipient'),
                page_date,
                data.get('metadata', {}).get('subject'),
                data.get('metadata', {}).get('significance'),
                data.get('metadata', {}).get('theme'),
                data.get('metadata', {}).get('document_type'),
                data.get('insights'),
                data.get('document_id'),
                processed_at,
                data.get('extraction_version'),
                data.get('flags', {}).get('quality_score'),
                data.get('flags', {}).get('requires_second_review'),
                data.get('flags', {}).get('contains_sensitive_info'),
                data.get('flags', {}).get('extraction_complete'),
                data.get('flags', {}).get('review_notes'),
                data.get('forensic_notes')
            )
            counts["pages"] += 1
            
            # Insert entities (people)
            for person in data.get('entities', {}).get('people', []):
                await conn.execute("""
                    INSERT INTO birthday_book_entities (
                        page_number, name, title, relationship, context,
                        confidence, page_appearances
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                    page_number,
                    person.get('name'),
                    person.get('title'),
                    person.get('relationship'),
                    person.get('context'),
                    person.get('confidence'),
                    person.get('page_appearances')
                )
                counts["entities"] += 1
            
            # Insert photos
            for photo in data.get('visual_analysis', {}).get('photos', []):
                if isinstance(photo, dict):
                    await conn.execute("""
                        INSERT INTO birthday_book_photos (
                            page_number, photo_description, photo_type,
                            people_in_photo, location_in_photo
                        ) VALUES ($1, $2, $3, $4, $5)
                    """,
                        page_number,
                        photo.get('description'),
                        photo.get('type'),
                        photo.get('people'),
                        photo.get('location')
                    )
                else:
                    # Handle string descriptions
                    await conn.execute("""
                        INSERT INTO birthday_book_photos (page_number, photo_description)
                        VALUES ($1, $2)
                    """, page_number, str(photo))
                counts["photos"] += 1
            
            # Insert signatures
            for sig in data.get('visual_analysis', {}).get('signatures', []):
                if isinstance(sig, dict):
                    await conn.execute("""
                        INSERT INTO birthday_book_signatures (
                            page_number, signer_name, signature_type, confidence
                        ) VALUES ($1, $2, $3, $4)
                    """,
                        page_number,
                        sig.get('name'),
                        sig.get('type'),
                        sig.get('confidence')
                    )
                else:
                    await conn.execute("""
                        INSERT INTO birthday_book_signatures (page_number, signer_name)
                        VALUES ($1, $2)
                    """, page_number, str(sig))
                counts["signatures"] += 1
            
            # Insert redactions
            for redaction in data.get('visual_analysis', {}).get('redactions', []):
                await conn.execute("""
                    INSERT INTO birthday_book_redactions (page_number, redaction_description)
                    VALUES ($1, $2)
                """, page_number, str(redaction))
                counts["redactions"] += 1
            
            if counts["pages"] % 10 == 0:
                print(f"  Progress: {counts['pages']} pages...")
                
        except Exception as e:
            print(f"  Error processing {json_file}: {e}")
            continue
    
    print(f"✓ Imported {counts['pages']} pages")
    print(f"  - Entities: {counts['entities']}")
    print(f"  - Photos: {counts['photos']}")
    print(f"  - Signatures: {counts['signatures']}")
    print(f"  - Redactions: {counts['redactions']}")
    return counts


async def verify_import(conn: asyncpg.Connection):
    """Verify the import."""
    print("\n--- Import Verification ---")
    
    # Page count
    page_count = await conn.fetchval("SELECT COUNT(*) FROM birthday_book_pages")
    print(f"Total pages: {page_count}")
    
    # Entity count
    entity_count = await conn.fetchval("SELECT COUNT(*) FROM birthday_book_entities")
    print(f"Total entities (people): {entity_count}")
    
    # Top people mentioned
    top_people = await conn.fetch("""
        SELECT name, COUNT(*) as mentions
        FROM birthday_book_entities
        GROUP BY name
        ORDER BY mentions DESC
        LIMIT 10
    """)
    print("\nTop 10 people mentioned:")
    for row in top_people:
        print(f"  {row['name']}: {row['mentions']} mentions")
    
    # Page types
    page_types = await conn.fetch("""
        SELECT page_type, COUNT(*) as cnt
        FROM birthday_book_pages
        WHERE page_type IS NOT NULL
        GROUP BY page_type
    """)
    print("\nPage types:")
    for row in page_types:
        print(f"  {row['page_type']}: {row['cnt']}")
    
    # Photos and signatures
    photo_count = await conn.fetchval("SELECT COUNT(*) FROM birthday_book_photos")
    sig_count = await conn.fetchval("SELECT COUNT(*) FROM birthday_book_signatures")
    redaction_count = await conn.fetchval("SELECT COUNT(*) FROM birthday_book_redactions")
    print(f"\nVisual elements:")
    print(f"  Photos: {photo_count}")
    print(f"  Signatures: {sig_count}")
    print(f"  Redactions: {redaction_count}")
    
    # Sample insights
    sample_insights = await conn.fetch("""
        SELECT page_number, insights
        FROM birthday_book_pages
        WHERE insights IS NOT NULL AND array_length(insights, 1) > 0
        LIMIT 3
    """)
    print(f"\n--- Sample Insights ---")
    for row in sample_insights:
        print(f"\nPage {row['page_number']}:")
        for insight in row['insights'][:3]:
            print(f"  • {insight[:100]}...")


async def main():
    print("=" * 60)
    print("Birthday Book Import")
    print("=" * 60)
    print(f"Source: {BASE_DIR}")
    print(f"Database: {DB_URL.replace('://', '://***:***@')}")
    print()
    
    try:
        conn = await asyncpg.connect(DB_URL)
        
        # Create tables
        await create_tables(conn)
        
        # Import data
        counts = await import_pages(conn)
        
        # Verify
        await verify_import(conn)
        
        await conn.close()
        
        print("\n" + "=" * 60)
        print("Import Complete!")
        print(f"Pages: {counts['pages']}")
        print(f"Entities: {counts['entities']}")
        print(f"Photos: {counts['photos']}")
        print(f"Signatures: {counts['signatures']}")
        print(f"Redactions: {counts['redactions']}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
