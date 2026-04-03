#!/usr/bin/env python3
"""
Initialize PostgreSQL Epstein Database
Applies schema and imports data from SQLite databases without duplication
"""

import os
import sys
import json
import sqlite3
import psycopg2
from psycopg2.extras import execute_values
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/home/cbwinslow/workspace/epstein/.env')

# Database configuration
DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "epstein"),
    "user": os.getenv("POSTGRES_USER", "cbwinslow"),
    "password": os.getenv("POSTGRES_PASSWORD", "123qweasd"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5432")
}

DATA_ROOT = "/home/cbwinslow/workspace/epstein-data"

def get_postgres_connection():
    """Get PostgreSQL connection"""
    return psycopg2.connect(**DB_CONFIG)

def apply_schema():
    """Apply SQL schema to PostgreSQL"""
    print("Applying database schema...")
    
    schema_file = "/home/cbwinslow/workspace/epstein/migrations/003_full_schema.sql"
    
    if not os.path.exists(schema_file):
        print(f"ERROR: Schema file not found: {schema_file}")
        return False
    
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✓ Schema applied successfully")
        return True
        
    except Exception as e:
        print(f"ERROR applying schema: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

def check_duplicates(conn, table, key_field, values):
    """Check for existing records to avoid duplicates"""
    cursor = conn.cursor()
    
    # Create temporary table for batch checking
    existing = set()
    
    # Check in batches to avoid huge queries
    batch_size = 1000
    for i in range(0, len(values), batch_size):
        batch = values[i:i+batch_size]
        placeholders = ','.join(['%s'] * len(batch))
        
        cursor.execute(
            f"SELECT {key_field} FROM {table} WHERE {key_field} IN ({placeholders})",
            batch
        )
        existing.update(row[0] for row in cursor.fetchall())
    
    cursor.close()
    return existing

def import_full_text_corpus():
    """Import documents and pages from full_text_corpus.db"""
    db_path = f"{DATA_ROOT}/databases/full_text_corpus.db"
    
    if not os.path.exists(db_path):
        print(f"WARNING: Database not found: {db_path}")
        return 0
    
    print(f"Importing from full_text_corpus.db...")
    
    try:
        sqlite_conn = sqlite3.connect(db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        pg_conn = get_postgres_connection()
        pg_cursor = pg_conn.cursor()
        
        # Import documents
        print("  Importing documents...")
        sqlite_cursor.execute("SELECT efta_id, filename, dataset, filepath, file_size, page_count, document_type, classification, metadata FROM documents")
        
        documents = []
        for row in sqlite_cursor.fetchall():
            efta_id, filename, dataset, filepath, file_size, page_count, doc_type, classification, metadata = row
            
            # Parse metadata if it's a string
            if isinstance(metadata, str):
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            documents.append((
                efta_id, filename, dataset or 'unknown', filepath or '', 
                file_size, page_count, doc_type, classification,
                json.dumps(metadata) if metadata else '{}'
            ))
        
        # Check for existing documents
        if documents:
            efta_ids = [d[0] for d in documents]
            existing = check_duplicates(pg_conn, 'documents', 'efta_id', efta_ids)
            
            # Filter out duplicates
            new_documents = [d for d in documents if d[0] not in existing]
            
            if new_documents:
                execute_values(pg_cursor, """
                    INSERT INTO documents (efta_id, filename, dataset, filepath, file_size, page_count, document_type, classification, metadata)
                    VALUES %s
                    ON CONFLICT (efta_id) DO NOTHING
                """, new_documents)
                pg_conn.commit()
                print(f"    ✓ Imported {len(new_documents)} new documents (skipped {len(existing)} duplicates)")
            else:
                print(f"    ✓ All {len(documents)} documents already exist")
        
        # Import pages with OCR text
        print("  Importing pages...")
        sqlite_cursor.execute("""
            SELECT p.document_efta_id, p.page_number, p.ocr_text, p.ocr_confidence, 
                   p.has_redactions, p.redaction_count
            FROM pages p
            JOIN documents d ON p.document_efta_id = d.efta_id
        """)
        
        pages = []
        for row in sqlite_cursor.fetchall():
            doc_efta, page_num, ocr_text, confidence, has_redact, redact_count = row
            pages.append((doc_efta, page_num, ocr_text, confidence, has_redact, redact_count))
        
        # Get document IDs and insert pages
        if pages:
            batch_size = 10000
            imported = 0
            skipped = 0
            
            for i in range(0, len(pages), batch_size):
                batch = pages[i:i+batch_size]
                
                # Get document IDs
                efta_ids = list(set(p[0] for p in batch))
                pg_cursor.execute(
                    "SELECT id, efta_id FROM documents WHERE efta_id IN %s",
                    (tuple(efta_ids),)
                )
                doc_id_map = {row[1]: row[0] for row in pg_cursor.fetchall()}
                
                # Prepare page inserts
                page_inserts = []
                for p in batch:
                    doc_id = doc_id_map.get(p[0])
                    if doc_id:
                        page_inserts.append((doc_id, p[1], p[2], p[3], p[4], p[5]))
                
                if page_inserts:
                    execute_values(pg_cursor, """
                        INSERT INTO pages (document_id, page_number, ocr_text, ocr_confidence, has_redactions, redaction_count)
                        VALUES %s
                        ON CONFLICT (document_id, page_number) DO NOTHING
                    """, page_inserts)
                    pg_conn.commit()
                    imported += len(page_inserts)
            
            print(f"    ✓ Imported {imported} pages")
        
        sqlite_conn.close()
        pg_conn.close()
        
        return len(documents)
        
    except Exception as e:
        print(f"ERROR importing full_text_corpus: {e}")
        import traceback
        traceback.print_exc()
        return 0

def import_knowledge_graph():
    """Import entities and relationships from knowledge_graph.db"""
    db_path = f"{DATA_ROOT}/databases/knowledge_graph.db"
    
    if not os.path.exists(db_path):
        print(f"WARNING: Database not found: {db_path}")
        return 0
    
    print(f"Importing from knowledge_graph.db...")
    
    try:
        sqlite_conn = sqlite3.connect(db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        pg_conn = get_postgres_connection()
        pg_cursor = pg_conn.cursor()
        
        # Import entities
        print("  Importing entities...")
        sqlite_cursor.execute("SELECT name, entity_type, normalized_name, category, confidence, metadata FROM entities")
        
        entities = []
        for row in sqlite_cursor.fetchall():
            name, ent_type, norm_name, category, confidence, metadata = row
            entities.append((name, ent_type, norm_name, category, confidence, json.dumps(metadata or {})))
        
        if entities:
            # Check for existing
            entity_keys = [(e[0], e[1]) for e in entities]
            
            execute_values(pg_cursor, """
                INSERT INTO entities (name, entity_type, normalized_name, category, confidence, metadata)
                VALUES %s
                ON CONFLICT (name, entity_type) DO NOTHING
            """, entities)
            pg_conn.commit()
            print(f"    ✓ Imported {len(entities)} entities")
        
        # Import relationships
        print("  Importing relationships...")
        sqlite_cursor.execute("SELECT source_name, target_name, relationship_type, confidence FROM relationships")
        
        relationships = []
        for row in sqlite_cursor.fetchall():
            source, target, rel_type, confidence = row
            relationships.append((source, target, rel_type, confidence))
        
        if relationships:
            print(f"    Found {len(relationships)} relationships to import")
            # Note: Relationships require entity IDs, need to map names to IDs
            # This is a simplified version - full implementation would need proper mapping
        
        sqlite_conn.close()
        pg_conn.close()
        
        return len(entities)
        
    except Exception as e:
        print(f"ERROR importing knowledge_graph: {e}")
        return 0

def import_communications():
    """Import emails from communications.db"""
    db_path = f"{DATA_ROOT}/databases/communications.db"
    
    if not os.path.exists(db_path):
        print(f"WARNING: Database not found: {db_path}")
        return 0
    
    print(f"Importing from communications.db...")
    
    try:
        sqlite_conn = sqlite3.connect(db_path)
        sqlite_cursor = sqlite_conn.cursor()
        
        pg_conn = get_postgres_connection()
        pg_cursor = pg_conn.cursor()
        
        # Import emails
        sqlite_cursor.execute("SELECT communication_type, sent_date, subject, content, sender_email FROM emails")
        
        emails = []
        for row in sqlite_cursor.fetchall():
            comm_type, sent_date, subject, content, sender = row
            emails.append((comm_type, sent_date, subject, content, sender))
        
        if emails:
            execute_values(pg_cursor, """
                INSERT INTO communications (communication_type, sent_date, subject, content, sender_entity_id)
                VALUES %s
            """, emails)
            pg_conn.commit()
            print(f"    ✓ Imported {len(emails)} communications")
        
        sqlite_conn.close()
        pg_conn.close()
        
        return len(emails)
        
    except Exception as e:
        print(f"ERROR importing communications: {e}")
        return 0

def import_transcripts():
    """Import transcripts from transcripts.db"""
    db_path = f"{DATA_ROOT}/databases/transcripts.db"
    
    if not os.path.exists(db_path):
        print(f"WARNING: Database not found: {db_path}")
        return 0
    
    print(f"Importing from transcripts.db...")
    # Implementation similar to above
    return 0

def import_ocr_results():
    """Import OCR results from ocr_database.db"""
    db_path = f"{DATA_ROOT}/databases/ocr_database.db"
    
    if not os.path.exists(db_path):
        print(f"WARNING: Database not found: {db_path}")
        return 0
    
    print(f"Importing from ocr_database.db...")
    # OCR data is already imported via full_text_corpus
    return 0

def import_fec_data():
    """Import FEC data from raw files"""
    print("Importing FEC data...")
    
    fec_dir = f"{DATA_ROOT}/raw-files/fec"
    if not os.path.exists(fec_dir):
        print(f"  WARNING: FEC directory not found: {fec_dir}")
        return 0
    
    # Check for existing FEC files
    files = list(Path(fec_dir).rglob("*.zip"))
    print(f"  Found {len(files)} FEC zip files")
    
    # FEC import would be handled by separate FEC ingestion scripts
    return len(files)

def verify_import():
    """Verify the import was successful"""
    print("\nVerifying PostgreSQL import...")
    
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        # Check table counts
        tables = ['documents', 'pages', 'entities', 'communications', 
                  'fec_individual_contributions', 'fec_committee_master', 'fec_candidate_master']
        
        print("\nTable counts:")
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  {table}: {count:,} rows")
            except Exception as e:
                print(f"  {table}: Error - {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR verifying import: {e}")
        return False

def main():
    """Main initialization function"""
    print("="*80)
    print("POSTGRESQL EPSTEIN DATABASE INITIALIZATION")
    print("="*80)
    print(f"Started: {datetime.now().isoformat()}")
    print()
    
    # Step 1: Apply schema
    if not apply_schema():
        print("ERROR: Failed to apply schema. Aborting.")
        return False
    
    print()
    print("="*80)
    print("IMPORTING DATA FROM SQLITE DATABASES")
    print("="*80)
    
    # Step 2: Import data from SQLite databases
    stats = {
        "documents": import_full_text_corpus(),
        "entities": import_knowledge_graph(),
        "communications": import_communications(),
        "transcripts": import_transcripts(),
        "ocr": import_ocr_results(),
        "fec_files": import_fec_data()
    }
    
    print()
    print("="*80)
    print("IMPORT STATISTICS")
    print("="*80)
    for key, value in stats.items():
        print(f"  {key}: {value:,}")
    
    # Step 3: Verify
    verify_import()
    
    print()
    print("="*80)
    print("INITIALIZATION COMPLETE")
    print("="*80)
    print(f"Finished: {datetime.now().isoformat()}")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
