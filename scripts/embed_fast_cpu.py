#!/usr/bin/env python3
"""Fast CPU embedding with fastembed + bge-small-en-v1.5.

~500 texts/sec on CPU → ~47 min for 1.4M remaining pages.
No GPU needed. Uses ONNX Runtime optimized for CPU.

Creates a new column bge_small_embedding (vector(384)) on the pages table.

Usage:
    python -u scripts/embed_fast_cpu.py           # Run
    python scripts/embed_fast_cpu.py status       # Check progress
"""

import sys
import io
import time
import signal

import psycopg2
from fastembed import TextEmbedding

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
COLUMN = "bge_small_embedding"
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
        cur.execute(f"SELECT COUNT(*) FROM pages WHERE {COLUMN} IS NOT NULL")
        filled = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL AND length(text_content) > 10")
        total = cur.fetchone()[0]
        log(f"{COLUMN}: {filled:,}/{total:,} ({filled/total*100:.1f}%) | Remaining: {total-filled:,}")
        conn.close()
        return

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Ensure column exists
    cur.execute(f"ALTER TABLE pages ADD COLUMN IF NOT EXISTS {COLUMN} vector({DIMS})")
    conn.commit()

    cur.execute(f"""
        SELECT COUNT(*) FROM pages
        WHERE {COLUMN} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
    """)
    total = cur.fetchone()[0]
    if total == 0:
        log(f"All pages already have {COLUMN}!")
        conn.close()
        return

    log(f"Loading {MODEL_NAME}...")
    model = TextEmbedding(MODEL_NAME)
    log(f"Pages to embed: {total:,}")
    log(f"Batch size: {BATCH_SIZE}")
    log(f"ETA: ~{total/500/60:.0f} min at ~500/sec\n")

    processed = 0
    errors = 0
    t0 = time.time()
    last_id = 0

    while not shutdown:
        cur.execute(f"""
            SELECT id, LEFT(text_content, %s) FROM pages
            WHERE {COLUMN} IS NULL AND text_content IS NOT NULL
              AND length(text_content) > 10 AND id > %s
            ORDER BY id LIMIT %s
        """, (MAX_TEXT_LEN, last_id, BATCH_SIZE))
        rows = cur.fetchall()
        if not rows:
            break

        last_id = rows[-1][0]
        page_ids = [r[0] for r in rows]
        texts = [(r[1] or "")[:MAX_TEXT_LEN] for r in rows]

        try:
            # Encode with fastembed (ONNX)
            embeddings = list(model.embed(texts, batch_size=512))

            # Build COPY data for fast bulk insert
            buf = io.StringIO()
            for pid, emb in zip(page_ids, embeddings):
                vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
                buf.write(f"{pid}\t{vec}\n")
            buf.seek(0)

            # Use COPY to temp table for fastest writes
            cur.execute("DROP TABLE IF EXISTS _tmp_emb")
            cur.execute(f"CREATE TEMP TABLE _tmp_emb (id INTEGER PRIMARY KEY, emb vector({DIMS}))")
            cur.copy_from(buf, "_tmp_emb", columns=("id", "emb"))
            cur.execute(f"""
                UPDATE pages SET {COLUMN} = te.emb
                FROM _tmp_emb te WHERE pages.id = te.id
            """)
            cur.execute("DROP TABLE IF EXISTS _tmp_emb")
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
