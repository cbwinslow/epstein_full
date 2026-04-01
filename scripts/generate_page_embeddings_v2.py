#!/usr/bin/env python3
"""
Resume-capable embedding generation for PostgreSQL pages - Optimized version.

Generates embeddings for pages that don't have them yet, with progress
tracking stored in PostgreSQL for crash/resume safety.
"""

from __future__ import annotations

import logging
import signal
import time
from datetime import datetime
from typing import Any

import psycopg2
import os
# Force use of K80s only (GPUs 1 and 2), skip K40 (GPU 0) due to compute capability 3.5
os.environ["CUDA_VISIBLE_DEVICES"] = "1,2"

import torch
from psycopg2.extras import execute_values
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

# Settings - Optimized for older GPUs (K40/K80)
MODEL_NAME = "nomic-ai/nomic-embed-text-v2-moe"
BATCH_SIZE = 64  # Larger batch for GPU
MAX_PAGES_PER_BATCH = 500  # Larger batches for GPU efficiency
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
GPU_COUNT = torch.cuda.device_count() if torch.cuda.is_available() else 0
EMBEDDING_DIM = 384  # Matryoshka 384-dim to match existing table

console = Console()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
        execute_values(
            cur,
            """
            INSERT INTO page_embeddings (page_id, embedding, model_name, created_at)
            VALUES %s
            ON CONFLICT (page_id) DO UPDATE SET
                embedding = EXCLUDED.embedding,
                model_name = EXCLUDED.model_name,
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

        # For pages, we store the full page text (truncated to first 2000 chars for efficiency)
        truncated_text = text_content[:2000]

        try:
            # Generate embedding for single text (384-dim Matryoshka)
            embedding = model.encode(
                truncated_text,
                show_progress_bar=False,
                convert_to_numpy=True,
                truncate_dim=EMBEDDING_DIM
            )
            embedding_list = embedding.tolist()

            records.append((
                page_id,
                embedding_list,
                MODEL_NAME,
                datetime.now().isoformat()
            ))
        except Exception as e:
            logger.warning(f"Failed to embed page {page_id}: {e}")
            continue

    # Insert all records
    if records and not shutdown_requested:
        return insert_embeddings_batch(records)
    return 0


def run_embedding_generation():
    """Main embedding generation loop with resume capability."""
    console.print("[bold cyan]Embedding Generation Pipeline (GPU Optimized)[/bold cyan]")
    console.print(f"Model: {MODEL_NAME}")
    console.print(f"Device: {DEVICE}")
    console.print(f"GPUs detected: {GPU_COUNT}")
    if GPU_COUNT > 0:
        for i in range(GPU_COUNT):
            console.print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    console.print(f"Batch size: {BATCH_SIZE}")
    console.print()

    # Get current stats
    stats = get_embedding_stats()
    console.print("[bold]Current Status:[/bold]")
    console.print(f"  Total pages: {stats['total_pages']:,}")
    console.print(f"  Embedded: {stats['embedded_pages']:,} ({stats['percent_complete']:.1f}%)")
    console.print(f"  Remaining: {stats['remaining_pages']:,}")
    console.print()

    if stats['remaining_pages'] == 0:
        console.print("[green]All pages already have embeddings![/green]")
        return

    # Load model
    console.print(f"[bold]Loading model {MODEL_NAME}...[/bold]")
    start_load = time.time()
    model = SentenceTransformer(MODEL_NAME, device=DEVICE, trust_remote_code=True)
    load_time = time.time() - start_load
    console.print(f"[green]Model loaded in {load_time:.1f}s. Embedding dim: {model.get_sentence_embedding_dimension()}[/green]")
    console.print()

    # Progress tracking
    total_embedded = stats['embedded_pages']
    total_remaining = stats['remaining_pages']
    pages_processed = 0
    start_time = time.time()

    console.print(f"[bold]Starting embedding generation...[/bold]")
    console.print(f"Processing {MAX_PAGES_PER_BATCH} pages per DB query")
    console.print()

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
            batch_start = time.time()
            pages = get_unembedded_pages(MAX_PAGES_PER_BATCH)
            fetch_time = time.time() - batch_start

            if not pages:
                console.print("[green]No more pages to process![/green]")
                break

            console.print(f"[dim]Fetched {len(pages)} pages in {fetch_time:.2f}s[/dim]")

            # Process batch
            process_start = time.time()
            embedded_count = process_pages_batch(pages, model)
            process_time = time.time() - process_start

            pages_processed += len(pages)

            # Update progress
            progress.update(task, advance=len(pages))

            # Log progress
            rate = len(pages) / process_time if process_time > 0 else 0
            console.print(
                f"[dim]Processed {len(pages)} pages in {process_time:.1f}s "
                f"({rate:.1f} pages/sec) - "
                f"{pages_processed:,} this run[/dim]"
            )

            # Periodic status update every 500 pages
            if pages_processed % 500 == 0:
                current_stats = get_embedding_stats()
                console.print(
                    f"[cyan]Status: {current_stats['embedded_pages']:,} embedded "
                    f"({current_stats['percent_complete']:.1f}%)[/cyan]"
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
    if elapsed > 0 and pages_processed > 0:
        console.print(f"  Average rate: {pages_processed/elapsed:.1f} pages/sec")


if __name__ == "__main__":
    run_embedding_generation()
