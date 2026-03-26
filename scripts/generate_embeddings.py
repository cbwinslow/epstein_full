#!/usr/bin/env python3
"""Generate text embeddings for semantic search.

Generates 768-dim embeddings using sentence-transformers for all document pages
in PostgreSQL. Stores embeddings in the pages.embedding column (pgvector).

Usage:
    python scripts/generate_embeddings.py [--batch-size 32] [--model nomic-ai/nomic-embed-text-v2-moe]
    python scripts/generate_embeddings.py --verify  # Just check current status
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

# Default embedding model (384-dim, fast, CPU-friendly)
DEFAULT_MODEL = "all-MiniLM-L6-v2"  # 384-dim, fast
# For 768-dim: use "nomic-ai/nomic-embed-text-v2-moe" or "all-mpnet-base-v2"

# Expected embedding dimension (must match pages.embedding column)
EXPECTED_DIM = 384  # Update if using a different model

# Batch size for embedding generation
BATCH_SIZE = 32


def get_embedding_stats(conn):
    """Get current embedding statistics."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                COUNT(*) as total_pages,
                COUNT(embedding) as pages_with_embeddings,
                COUNT(*) - COUNT(embedding) as pages_without_embeddings,
                ROUND(COUNT(embedding) * 100.0 / COUNT(*), 2) as embedding_coverage_percent
            FROM pages
        """)
        return cur.fetchone()


def get_pages_without_embeddings(conn, limit, offset=0):
    """Get pages that don't have embeddings yet."""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, text_content
            FROM pages
            WHERE embedding IS NULL
            ORDER BY id
            LIMIT %s OFFSET %s
        """, (limit, offset))
        return cur.fetchall()


def update_embeddings(conn, updates):
    """Update embeddings in batch."""
    with conn.cursor() as cur:
        for page_id, embedding in updates:
            cur.execute("""
                UPDATE pages 
                SET embedding = %s::vector
                WHERE id = %s
            """, (embedding, page_id))
    conn.commit()


def generate_embeddings(model_name, batch_size, limit=None):
    """Generate embeddings for all pages without them."""
    from sentence_transformers import SentenceTransformer
    
    print(f"Loading model: {model_name}")
    model = SentenceTransformer(model_name)
    embedding_dim = model.get_sentence_embedding_dimension()
    print(f"Embedding dimension: {embedding_dim}")
    
    # Check if dimension matches column
    if embedding_dim != EXPECTED_DIM:
        print(f"WARNING: Model produces {embedding_dim}-dim vectors but column expects {EXPECTED_DIM}-dim")
        print(f"You may need to ALTER TABLE pages ALTER COLUMN embedding TYPE vector({embedding_dim})")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborting. Update the column type first.")
            return
    
    conn = psycopg2.connect(PG_DSN)
    try:
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
                
                # Update database
                updates = []
                for page_id, embedding in zip(page_ids, embeddings):
                    # Convert numpy array to string for pgvector
                    embedding_str = '[' + ','.join(map(str, embedding.tolist())) + ']'
                    updates.append((page_id, embedding_str))
                
                update_embeddings(conn, updates)
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
                FROM pages 
                WHERE embedding IS NOT NULL 
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
                SELECT id, LEFT(text_content, 100) as content_preview
                FROM pages 
                WHERE embedding IS NOT NULL 
                LIMIT 1
            """)
            sample = cur.fetchone()
            if sample:
                print(f"\nSample page with embedding:")
                print(f"  ID: {sample['id']}")
                print(f"  Content: {sample['content_preview']}...")
        
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Generate text embeddings for semantic search")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE, help="Batch size")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name")
    parser.add_argument("--limit", type=int, help="Limit number of pages to process")
    parser.add_argument("--verify", action="store_true", help="Just verify status")
    args = parser.parse_args()
    
    if args.verify:
        verify_embeddings()
        return
    
    generate_embeddings(args.model, args.batch_size, args.limit)


if __name__ == "__main__":
    main()
