#!/usr/bin/env python3
"""Generate text embeddings for semantic search (384-dim).

Generates 384-dim embeddings using sentence-transformers (all-MiniLM-L6-v2)
for all document pages in PostgreSQL. Stores in a new page_embeddings table.

Usage:
    python scripts/generate_embeddings_384.py [--batch-size 32]
    python scripts/generate_embeddings_384.py --verify  # Just check current status
"""

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Embedding model (384-dim, fast, CPU-friendly)
MODEL_NAME = "all-MiniLM-L6-v2"

# Batch size for embedding generation
BATCH_SIZE = 32


def create_embeddings_table(conn):
    """Create the page_embeddings table if it doesn't exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS page_embeddings (
                page_id INTEGER PRIMARY KEY REFERENCES pages(id),
                embedding vector(384) NOT NULL,
                model_name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()
    print("Created page_embeddings table")


def get_embedding_stats(conn):
    """Get current embedding statistics."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                (SELECT COUNT(*) FROM pages) as total_pages,
                COUNT(*) as pages_with_embeddings
            FROM page_embeddings
        """)
        stats = cur.fetchone()
        stats['pages_without_embeddings'] = stats['total_pages'] - stats['pages_with_embeddings']
        stats['embedding_coverage_percent'] = round(stats['pages_with_embeddings'] * 100.0 / stats['total_pages'], 2) if stats['total_pages'] > 0 else 0
        return stats


def get_pages_without_embeddings(conn, limit, offset=0):
    """Get pages that don't have embeddings yet."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT p.id, p.text_content
            FROM pages p
            LEFT JOIN page_embeddings pe ON p.id = pe.page_id
            WHERE pe.page_id IS NULL
            ORDER BY p.id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        return cur.fetchall()


def insert_embeddings(conn, updates):
    """Insert embeddings in batch."""
    with conn.cursor() as cur:
        for page_id, embedding in updates:
            cur.execute("""
                INSERT INTO page_embeddings (page_id, embedding, model_name)
                VALUES (%s, %s::vector, %s)
                ON CONFLICT (page_id) DO NOTHING
            """, (page_id, embedding, MODEL_NAME))
    conn.commit()


def generate_embeddings(batch_size, limit=None):
    """Generate embeddings for all pages without them."""
    from sentence_transformers import SentenceTransformer
    
    print(f"Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    embedding_dim = model.get_sentence_embedding_dimension()
    print(f"Embedding dimension: {embedding_dim}")
    
    conn = psycopg2.connect(PG_DSN)
    try:
        # Create table if needed
        create_embeddings_table(conn)
        
        # Check current status
        stats = get_embedding_stats(conn)
        print(f"\nCurrent status:")
        print(f"  Total pages: {stats['total_pages']:,}")
        print(f"  With embeddings: {stats['pages_with_embeddings']:,}")
        print(f"  Without embeddings: {stats['pages_without_embeddings']:,}")
        print(f"  Coverage: {stats['embedding_coverage_percent']}%")
        
        if stats['pages_without_embeddings'] == 0:
            print("\nAll pages already have embeddings!")
            return
        
        # Process in batches
        total_to_process = min(limit, stats['pages_without_embeddings']) if limit else stats['pages_without_embeddings']
        print(f"\nProcessing {total_to_process:,} pages (batch_size={batch_size})...")
        
        processed = 0
        errors = 0
        start_time = time.time()
        
        while processed < total_to_process:
            # Get batch of pages
            batch_limit = min(batch_size, total_to_process - processed)
            pages = get_pages_without_embeddings(conn, batch_limit, processed)
            
            if not pages:
                break
            
            # Extract text content
            texts = []
            page_ids = []
            for page in pages:
                content = page.get('text_content', '')
                if content and len(content.strip()) > 10:
                    texts.append(content[:1000])  # Truncate long texts
                    page_ids.append(page['id'])
            
            if not texts:
                processed += len(pages)
                continue
            
            # Generate embeddings
            try:
                embeddings = model.encode(texts, show_progress_bar=False, batch_size=batch_size)
                
                # Prepare for database
                updates = []
                for page_id, embedding in zip(page_ids, embeddings):
                    # Convert numpy array to string for pgvector
                    embedding_str = '[' + ','.join(map(str, embedding.tolist())) + ']'
                    updates.append((page_id, embedding_str))
                
                insert_embeddings(conn, updates)
                processed += len(pages)
                
            except Exception as e:
                errors += 1
                conn.rollback()  # Roll back failed transaction
                if errors <= 3:
                    print(f"\n  Error at batch {processed}: {e}")
                processed += len(pages)
            
            # Progress update
            elapsed = time.time() - start_time
            rate = processed / elapsed if elapsed > 0 else 0
            eta = (total_to_process - processed) / rate if rate > 0 else 0
            
            print(f"\r  Progress: {processed:,}/{total_to_process:,} "
                  f"({processed/total_to_process*100:.1f}%) "
                  f"rate: {rate:.1f} pages/sec "
                  f"ETA: {eta/60:.1f} min",
                  end="", flush=True)
        
        print(f"\n\nDone! Processed: {processed:,}, Errors: {errors}")
        
        # Final status
        final_stats = get_embedding_stats(conn)
        print(f"\nFinal status:")
        print(f"  With embeddings: {final_stats['pages_with_embeddings']:,}")
        print(f"  Coverage: {final_stats['embedding_coverage_percent']}%")
        
    finally:
        conn.close()


def verify_embeddings():
    """Verify embedding status."""
    conn = psycopg2.connect(PG_DSN)
    try:
        stats = get_embedding_stats(conn)
        print("=== Embedding Status ===")
        print(f"Total pages: {stats['total_pages']:,}")
        print(f"With embeddings: {stats['pages_with_embeddings']:,}")
        print(f"Without embeddings: {stats['pages_without_embeddings']:,}")
        print(f"Coverage: {stats['embedding_coverage_percent']}%")
        
        # Check vector dimensions
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT 
                    vector_dims(embedding) as dimensions,
                    COUNT(*) as count
                FROM page_embeddings 
                GROUP BY vector_dims(embedding)
            """)
            dims = cur.fetchall()
            if dims:
                print("\nVector dimensions:")
                for d in dims:
                    print(f"  {d['dimensions']}-dim: {d['count']:,} pages")
            else:
                print("\nNo embeddings found.")
        
        # Sample embedding
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT pe.page_id, LEFT(p.text_content, 100) as content_preview
                FROM page_embeddings pe
                JOIN pages p ON pe.page_id = p.id
                LIMIT 1
            """)
            sample = cur.fetchone()
            if sample:
                print(f"\nSample page with embedding:")
                print(f"  Page ID: {sample['page_id']}")
                print(f"  Content: {sample['content_preview']}...")
        
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Generate 384-dim text embeddings")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--limit", type=int, help="Limit number of pages to process")
    parser.add_argument("--verify", action="store_true", help="Just verify status")
    args = parser.parse_args()
    
    if args.verify:
        verify_embeddings()
        return
    
    generate_embeddings(args.batch_size, args.limit)


if __name__ == "__main__":
    main()
