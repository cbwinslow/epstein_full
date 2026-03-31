#!/usr/bin/env python3
"""CPU embedding generator — all-MiniLM-L6-v2, 384-dim.

Pre-computes unembedded IDs, then processes in batches without
expensive SQL subqueries. No GPU needed.

Usage:
    python -u scripts/embed_cpu.py           # Run
    python scripts/embed_cpu.py status       # Check progress
"""

import sys
import time
import signal

import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
MODEL_NAME = "all-MiniLM-L6-v2"
DIMS = 384
BATCH_SIZE = 2048
MAX_TEXT_LEN = 512

shutdown = False
signal.signal(signal.SIGINT, lambda s, f: globals().__setitem__('shutdown', True))
signal.signal(signal.SIGTERM, lambda s, f: globals().__setitem__('shutdown', True))


def log(msg):
    print(msg, flush=True)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL AND length(text_content) > 10")
        total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM page_embeddings")
        emb = cur.fetchone()[0]
        log(f"Embedded: {emb:,}/{total:,} ({emb/total*100:.1f}%) | Remaining: {total-emb:,}")
        conn.close()
        return

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Pre-compute unembedded page IDs (sorted)
    log("Finding unembedded pages...")
    t0 = time.time()
    cur.execute("""
        SELECT p.id FROM pages p
        WHERE p.text_content IS NOT NULL AND length(p.text_content) > 10
          AND NOT EXISTS (SELECT 1 FROM page_embeddings pe WHERE pe.page_id = p.id)
        ORDER BY p.id
    """)
    all_ids = [r[0] for r in cur.fetchall()]
    log(f"  Found {len(all_ids):,} unembedded pages in {time.time()-t0:.0f}s")

    if not all_ids:
        log("All pages already embedded!")
        conn.close()
        return

    log(f"Loading {MODEL_NAME}...")
    model = SentenceTransformer(MODEL_NAME)
    total = len(all_ids)
    log(f"Pages to embed: {total:,}")
    log(f"Batch size: {BATCH_SIZE}\n")

    processed = 0
    errors = 0
    t0 = time.time()

    for batch_start in range(0, total, BATCH_SIZE):
        if shutdown:
            break

        batch_ids = all_ids[batch_start:batch_start + BATCH_SIZE]

        # Fetch text for this batch of IDs
        cur.execute("""
            SELECT id, LEFT(text_content, %s) FROM pages
            WHERE id = ANY(%s)
        """, (MAX_TEXT_LEN, batch_ids))
        rows = cur.fetchall()
        # Maintain order
        row_dict = {r[0]: r[1] for r in rows}
        page_ids = [pid for pid in batch_ids if pid in row_dict]
        texts = [row_dict.get(pid, "")[:MAX_TEXT_LEN] for pid in page_ids]

        if not texts:
            continue

        try:
            embeddings = model.encode(
                texts, show_progress_bar=False, batch_size=256, normalize_embeddings=True
            )

            insert_rows = [
                (pid, "[" + ",".join(f"{v:.6f}" for v in emb) + "]", MODEL_NAME)
                for pid, emb in zip(page_ids, embeddings)
            ]

            execute_values(
                cur,
                "INSERT INTO page_embeddings (page_id, embedding, model_name) VALUES %s "
                "ON CONFLICT (page_id) DO NOTHING",
                insert_rows,
                template=f"(%s, %s::vector({DIMS}), %s)",
            )
            conn.commit()
            processed += len(page_ids)
        except Exception as e:
            conn.rollback()
            errors += len(page_ids)
            if errors <= 3:
                log(f"  Error: {e}")

        elapsed = time.time() - t0
        rate = processed / elapsed if elapsed > 0 else 0
        pct = processed / total * 100
        eta_min = (total - processed) / rate / 60 if rate > 0 else 0
        log(f"  {processed:,}/{total:,} ({pct:.1f}%) | {rate:.0f}/sec | ETA: {eta_min:.0f}min | Err: {errors}")

    elapsed = time.time() - t0
    log(f"\nDone: {processed:,} in {elapsed/60:.0f}min ({processed/elapsed:.0f}/sec) | Errors: {errors}")
    conn.close()


if __name__ == "__main__":
    main()
