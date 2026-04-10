#!/usr/bin/env python3
"""
Resume-capable embedding generation for PostgreSQL pages.

Generates embeddings for pages that don't have them yet, with progress
tracking stored in PostgreSQL for crash/resume safety.
"""

from __future__ import annotations

import json
import logging
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import psycopg2
import torch
from rich.console import Console
from rich.progress import BarColumn, MofNCompleteColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from sentence_transformers import SentenceTransformer

# PostgreSQL connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd"
}

# Settings
MODEL_NAME = "nomic-ai/nomic-embed-text-v2-moe"
BATCH_SIZE = 128  # GPU optimized
CHUNK_SIZE = 512  # Characters per chunk
MAX_PAGES_PER_BATCH = 1000  # Pages to fetch at once
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

console = Console()
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_requested
    console.print("\n[yellow]Shutdown requested. Finishing current batch...[/yellow]")
    shutdown_requested = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def get_connection():
    """Get PostgreSQL connection."""
    return psycopg2.connect(**DB_CONFIG)


def get_embedding_stats() -> dict:
    """Get current embedding statistics."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT COUNT(*) FROM pages")
    total_pages = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM page_embeddings")
    embedded_pages = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return {
        "total_pages": total_pages,
        "embedded_pages": embedded_pages,
        "remaining_pages": total_pages - embedded_pages,
        "percent_complete": (embedded_pages / total_pages * 100) if total_pages > 0 else 0
    }


def get_unembedded_pages(limit: int = MAX_PAGES_PER_BATCH) -> list[tuple]:
    """Fetch pages that don't have embeddings yet."""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT p.id, p.efta_number, p.page_number, p.text_content
        FROM pages p
        LEFT JOIN page_embeddings pe ON p.id = pe.page_id
        WHERE pe.page_id IS NULL
          AND p.text_content IS NOT NULL
          AND LENGTH(p.text_content) > 10
        ORDER BY p.id
        LIMIT %s
    """, (limit,))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    
    return results


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = 100) -> list[str]:
    """Split text into overlapping chunks."""
    if not text or len(text) <= chunk_size:
        return [text] if text else []
    
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # Try to break at sentence or word boundary
        if end < len(text):
            # Look for sentence break
            for i in range(end, max(start + chunk_size // 2, end - 200), -1):
                if i < len(text) and text[i] in '.!?':
                    end = i + 1
                    break
            else:
                # Look for word break
                for i in range(end, max(start + chunk_size // 2, end - 100), -1):
                    if i < len(text) and text[i].isspace():
                        end = i
                        break
        
        chunks.append(text[start:end].strip())
        start = end - overlap
        if start >= len(text):
            break
    
    return [c for c in chunks if c]


def generate_embeddings_batch(texts: list[str], model: SentenceTransformer) -> list[list[float]]:
    """Generate embeddings for a batch of texts."""
    if not texts:
        return []
    
    # Generate embeddings
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        show_progress_bar=False,
        convert_to_numpy=True
    )
    
    return embeddings.tolist()


def insert_embeddings_batch(records: list[tuple]) -> int:
    """Insert embeddings into PostgreSQL."""
    if not records:
        return 0
    
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        # Use execute_values for batch insert with ON CONFLICT
        from psycopg2.extras import execute_values
        
        execute_values(
            cur,
            """
            INSERT INTO page_embeddings (page_id, embedding, chunk_index, total_chunks, chunk_text, created_at)
            VALUES %s
            ON CONFLICT (page_id) DO UPDATE SET
                embedding = EXCLUDED.embedding,
                chunk_index = EXCLUDED.chunk_index,
                total_chunks = EXCLUDED.total_chunks,
                chunk_text = EXCLUDED.chunk_text,
                created_at = EXCLUDED.created_at
            """,
            records
        )
        conn.commit()
        return len(records)
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to insert embeddings: {e}")
        return 0
    finally:
        cur.close()
        conn.close()


def process_pages_batch(pages: list[tuple], model: SentenceTransformer) -> int:
    """Process a batch of pages and generate embeddings."""
    records = []
    
    for page_id, efta_number, page_number, text_content in pages:
        if shutdown_requested:
            break
        
        if not text_content or len(text_content) < 10:
            continue
        
        # Chunk the text
        chunks = chunk_text(text_content)
        if not chunks:
            continue
        
        # For pages, we store the full page text as a single chunk
        # or average multiple chunks if needed
        if len(chunks) == 1:
            # Single chunk - embed directly
            embedding = generate_embeddings_batch([chunks[0]], model)[0]
            records.append((
                page_id,
                embedding,
                0,  # chunk_index
                1,  # total_chunks
                chunks[0][:1000],  # truncated chunk_text
                int(time.time())
            ))
        else:
            # Multiple chunks - embed each and store first (or average)
            # For simplicity, store first chunk's embedding
            embedding = generate_embeddings_batch([chunks[0]], model)[0]
            records.append((
                page_id,
                embedding,
                0,
                len(chunks),
                chunks[0][:1000],
                int(time.time())
            ))
    
    # Insert all records
    if records and not shutdown_requested:
        return insert_embeddings_batch(records)
    return 0


def run_embedding_generation():
    """Main embedding generation loop with resume capability."""
    console.print("[bold cyan]Embedding Generation Pipeline[/bold cyan]")
    console.print(f"Model: {MODEL_NAME}")
    console.print(f"Device: {DEVICE}")
    console.print()
    
    # Get current stats
    stats = get_embedding_stats()
    console.print(f"[bold]Current Status:[/bold]")
    console.print(f"  Total pages: {stats['total_pages']:,}")
    console.print(f"  Embedded: {stats['embedded_pages']:,} ({stats['percent_complete']:.1f}%)")
    console.print(f"  Remaining: {stats['remaining_pages']:,}")
    console.print()
    
    if stats['remaining_pages'] == 0:
        console.print("[green]All pages already have embeddings![/green]")
        return
    
    # Load model
    console.print(f"[bold]Loading model {MODEL_NAME}...[/bold]")
    model = SentenceTransformer(MODEL_NAME, device=DEVICE, trust_remote_code=True)
    console.print(f"[green]Model loaded. Embedding dim: {model.get_sentence_embedding_dimension()}[/green]")
    console.print()
    
    # Progress tracking
    total_embedded = stats['embedded_pages']
    total_remaining = stats['remaining_pages']
    pages_processed = 0
    start_time = time.time()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=None),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        task = progress.add_task("Generating embeddings", total=total_remaining)
        
        while not shutdown_requested:
            # Fetch batch of unembedded pages
            pages = get_unembedded_pages(MAX_PAGES_PER_BATCH)
            
            if not pages:
                console.print("[green]No more pages to process![/green]")
                break
            
            # Process batch
            embedded_count = process_pages_batch(pages, model)
            pages_processed += len(pages)
            
            # Update progress
            progress.update(task, advance=len(pages))
            
            # Log progress every 1000 pages
            if pages_processed % 1000 == 0:
                elapsed = time.time() - start_time
                rate = pages_processed / elapsed if elapsed > 0 else 0
                console.print(
                    f"[dim]Processed {pages_processed:,} pages "
                    f"({rate:.1f} pages/sec) - "
                    f"{total_embedded + pages_processed:,} total embedded[/dim]"
                )
    
    # Final stats
    final_stats = get_embedding_stats()
    elapsed = time.time() - start_time
    
    console.print()
    console.print("[bold green]Embedding generation complete![/bold green]")
    console.print(f"  Pages processed this run: {pages_processed:,}")
    console.print(f"  Total embedded: {final_stats['embedded_pages']:,}")
    console.print(f"  Remaining: {final_stats['remaining_pages']:,}")
    console.print(f"  Percent complete: {final_stats['percent_complete']:.1f}%")
    console.print(f"  Time elapsed: {elapsed/60:.1f} minutes")
    console.print(f"  Average rate: {pages_processed/elapsed:.1f} pages/sec" if elapsed > 0 else "  N/A")


if __name__ == "__main__":
    run_embedding_generation()
