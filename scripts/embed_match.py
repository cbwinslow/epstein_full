#!/usr/bin/env python3
"""GPU embedding for all-MiniLM-L6-v2 — matches existing page_embeddings.

Fills remaining page_embeddings (all-MiniLM-L6-v2, 384-dim).
~2,500/sec on K80 GPU → ~10-30 min for 1.4M pages.

Usage:
    python -u scripts/embed_match.py                    # Run on cuda:1
    python scripts/embed_match.py status                # Check progress
    python scripts/embed_match.py --device cuda:2       # Use different GPU
    python scripts/embed_match.py --split 0/2           # Split 0 of 2 (even IDs)
    python scripts/embed_match.py --split 1/2           # Split 1 of 2 (odd IDs)
"""

import sys
import io
import time
import signal
import argparse

import torch
import psycopg2
from sentence_transformers import SentenceTransformer

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
MODEL_NAME = "all-MiniLM-L6-v2"
DIMS = 384
DB_BATCH = 4096
ENCODE_BATCH = 256
MAX_TEXT_LEN = 512

shutdown = False
signal.signal(signal.SIGINT, lambda s, f: globals().__setitem__('shutdown', True))
signal.signal(signal.SIGTERM, lambda s, f: globals().__setitem__('shutdown', True))


def log(msg):
    print(msg, flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="?", default="run", choices=["run", "status"])
    parser.add_argument("--device", default="cuda:1")
    parser.add_argument("--split", default=None, help="split N/M for parallel (e.g., 0/2)")
    args = parser.parse_args()

    if args.action == "status":
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM page_embeddings")
        emb = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL AND length(text_content) > 10")
        total = cur.fetchone()[0]
        log(f"page_embeddings: {emb:,}/{total:,} ({emb/total*100:.1f}%) | Remaining: {total-emb:,}")
        conn.close()
        return

    device = args.device
    split_mod = None
    split_rem = None
    if args.split:
        parts = args.split.split("/")
        split_rem, split_mod = int(parts[0]), int(parts[1])
        log(f"Split: {split_rem}/{split_mod} (processing id % {split_mod} = {split_rem})")

    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    # Count remaining
    where = "NOT EXISTS (SELECT 1 FROM page_embeddings pe WHERE pe.page_id = p.id)"
    if split_mod is not None:
        where += f" AND p.id % {split_mod} = {split_rem}"
    cur.execute(f"""
        SELECT COUNT(*) FROM pages p
        WHERE p.text_content IS NOT NULL AND length(p.text_content) > 10 AND {where}
    """)
    total = cur.fetchone()[0]
    if total == 0:
        log("All pages already embedded!")
        conn.close()
        return

    log(f"Loading {MODEL_NAME} on {device}...")
    model = SentenceTransformer(MODEL_NAME, device=device)
    log(f"Model on {model.device}")
    log(f"Pages to embed: {total:,}")
    log(f"ETA: ~{total/2500/60:.0f} min at ~2500/sec\n")

    processed = 0
    errors = 0
    t0 = time.time()
    last_id = 0

    while not shutdown:
        q = f"""
            SELECT p.id, LEFT(p.text_content, {MAX_TEXT_LEN}) FROM pages p
            WHERE p.text_content IS NOT NULL AND length(p.text_content) > 10
              AND p.id > {last_id} AND {where}
            ORDER BY p.id LIMIT {DB_BATCH}
        """
        cur.execute(q)
        rows = cur.fetchall()
        if not rows:
            break

        last_id = rows[-1][0]
        page_ids = [r[0] for r in rows]
        texts = [(r[1] or "")[:MAX_TEXT_LEN] for r in rows]

        try:
            embeddings = model.encode(
                texts, batch_size=ENCODE_BATCH, show_progress_bar=False, device=device,
                normalize_embeddings=True
            )

            buf = io.StringIO()
            for pid, emb in zip(page_ids, embeddings):
                vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
                buf.write(f"{pid}\t{vec}\t{MODEL_NAME}\n")
            buf.seek(0)

            cur.execute("DROP TABLE IF EXISTS _tmp_emb")
            cur.execute(f"CREATE TEMP TABLE _tmp_emb (id INTEGER PRIMARY KEY, emb vector({DIMS}), model VARCHAR)")
            cur.copy_from(buf, "_tmp_emb", columns=("id", "emb", "model"))
            cur.execute("""
                INSERT INTO page_embeddings (page_id, embedding, model_name)
                SELECT t.id, t.emb, t.model FROM _tmp_emb t
                ON CONFLICT (page_id) DO NOTHING
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
