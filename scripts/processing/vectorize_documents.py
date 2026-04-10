#!/usr/bin/env python3
"""Optimal document vectorization using llama.cpp GPU servers.

Pipeline: DB Reader → GPU Embedder → DB Writer (all concurrent)
Uses OpenAI-compatible /v1/embeddings endpoint.

Strategy:
  1. BGE-M3 first (fast, ~23h for 2.9M docs, 1024-dim)
  2. Qwen3 second (slow, ~14d for 2.9M docs, 4096-dim, higher quality)

Usage:
    python scripts/vectorize_documents.py bge_m3     # Run BGE-M3
    python scripts/vectorize_documents.py qwen3      # Run Qwen3
    python scripts/vectorize_documents.py all         # Run both sequentially
    python scripts/vectorize_documents.py status      # Check progress
"""

import json
import os
import sys
import time
import signal
import threading
from queue import Queue, Empty

import psycopg2
import requests
from psycopg2.extras import execute_values

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
LOG_DIR = "/home/cbwinslow/workspace/epstein/logs"

MODELS = {
    "bge_m3": {
        "url": "http://localhost:8081/v1/embeddings",
        "model_id": "bge-m3-FP16.gguf",
        "column": "bge_m3_embedding",
        "dims": 1024,
        "batch_size": 100,
        "max_text_len": 500,
        "fallback_text_len": 200,
        "prefetch": 6,
    },
    "qwen3": {
        "url": "http://localhost:8080/v1/embeddings",
        "model_id": "Qwen3-Embedding-8B-Q6_K.gguf",
        "column": "qwen3_embedding",
        "dims": 4096,
        "batch_size": 50,
        "max_text_len": 200,
        "fallback_text_len": 100,
        "prefetch": 4,
    },
}

shutdown = False


def signal_handler(sig, frame):
    global shutdown
    print("\nGraceful shutdown requested...")
    shutdown = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def get_conn():
    return psycopg2.connect(DB_URL)


def setup_logging(model_name):
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"vectorize_{model_name}.log")
    return open(log_path, "a")


def ensure_column(conn, column, dims):
    cur = conn.cursor()
    cur.execute(f"""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'pages' AND column_name = '{column}'
            ) THEN
                ALTER TABLE pages ADD COLUMN {column} vector({dims});
            END IF;
        END $$;
    """)
    conn.commit()


def count_remaining(conn, column):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*) FROM pages
        WHERE {column} IS NULL AND text_content IS NOT NULL
          AND length(text_content) > 10
    """)
    return cur.fetchone()[0]


def reader_thread(config, read_q, total, log_f):
    """Read batches from DB using keyset pagination."""
    conn = get_conn()
    cur = conn.cursor()
    col = config["column"]
    batch_size = config["batch_size"]
    last_id = 0
    batch_num = 0
    read_count = 0

    while not shutdown:
        cur.execute(f"""
            SELECT id, LEFT(text_content, %s) FROM pages
            WHERE {col} IS NULL AND text_content IS NOT NULL
              AND length(text_content) > 10 AND id > %s
            ORDER BY id LIMIT %s
        """, (config["max_text_len"], last_id, batch_size))

        rows = cur.fetchall()
        if not rows:
            read_q.put(None)
            break

        last_id = rows[-1][0]
        read_q.put((batch_num, rows))
        read_count += len(rows)
        batch_num += 1

        # Backpressure: don't read too far ahead
        while read_q.qsize() >= config["prefetch"] and not shutdown:
            time.sleep(0.05)

    conn.close()
    msg = f"Reader done: {read_count:,} pages queued in {batch_num} batches"
    print(f"  {msg}")
    log_f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    log_f.flush()


def embedder_thread(config, read_q, embed_q, log_f):
    """Embed batches via GPU server."""
    url = config["url"]
    model_id = config["model_id"]
    dims = config["dims"]
    batch_num = 0

    while not shutdown:
        try:
            item = read_q.get(timeout=3)
        except Empty:
            continue

        if item is None:
            embed_q.put(None)
            break

        bnum, rows = item
        page_ids = [r[0] for r in rows]
        texts = [(r[1] or "")[:config["max_text_len"]] for r in rows]

        try:
            resp = requests.post(
                url,
                json={"input": texts, "model": model_id},
                timeout=300,
            )
            if resp.status_code == 400:
                # Token limit - retry with shorter texts
                shorter = [t[:config["fallback_text_len"]] for t in texts]
                resp = requests.post(
                    url,
                    json={"input": shorter, "model": model_id},
                    timeout=300,
                )
            resp.raise_for_status()
            data = resp.json()

            embeddings = []
            for item_data in data["data"]:
                emb = item_data["embedding"]
                if isinstance(emb[0], list):
                    emb = emb[0]
                embeddings.append(emb)

            embed_q.put((bnum, page_ids, embeddings))
            batch_num += 1

        except Exception as e:
            err_msg = f"Embed error batch {bnum}: {e}"
            print(f"  {err_msg}")
            log_f.write(f"{time.strftime('%H:%M:%S')} {err_msg}\n")
            log_f.flush()
            embed_q.put((bnum, page_ids, None))

    msg = f"Embedder done: {batch_num} batches processed"
    print(f"  {msg}")


def writer_thread(config, embed_q, total, log_f):
    """Write embeddings to DB using temp table batch updates."""
    conn = get_conn()
    cur = conn.cursor()
    col = config["column"]
    dims = config["dims"]

    processed = 0
    written = 0
    errors = 0
    t0 = time.time()
    last_report = t0

    while not shutdown:
        try:
            item = embed_q.get(timeout=5)
        except Empty:
            continue

        if item is None:
            break

        bnum, page_ids, embeddings = item

        if embeddings is None:
            errors += len(page_ids)
            processed += len(page_ids)
        else:
            rows = []
            for pid, emb in zip(page_ids, embeddings):
                if emb is not None and len(emb) == dims:
                    vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
                    rows.append((pid, vec))

            if rows:
                try:
                    cur.execute("DROP TABLE IF EXISTS _tmp_emb")
                    cur.execute(
                        f"CREATE TEMP TABLE _tmp_emb (id INTEGER PRIMARY KEY, emb vector({dims}))"
                    )
                    execute_values(
                        cur, "INSERT INTO _tmp_emb (id, emb) VALUES %s", rows
                    )
                    cur.execute(
                        f"UPDATE pages SET {col} = te.emb "
                        f"FROM _tmp_emb te WHERE pages.id = te.id"
                    )
                    cur.execute("DROP TABLE IF EXISTS _tmp_emb")
                    conn.commit()
                    written += len(rows)
                except Exception as e:
                    conn.rollback()
                    err_msg = f"DB write error batch {bnum}: {e}"
                    print(f"  {err_msg}")
                    log_f.write(f"{time.strftime('%H:%M:%S')} {err_msg}\n")
                    errors += len(rows)

            processed += len(page_ids)

        # Report every 10 seconds
        now = time.time()
        if now - last_report >= 10:
            elapsed = now - t0
            rate = processed / elapsed if elapsed > 0 else 0
            remaining = total - processed
            eta_sec = remaining / rate if rate > 0 else 0
            eta_h = eta_sec / 3600
            pct = processed / total * 100 if total > 0 else 0
            msg = (
                f"{processed:,}/{total:,} ({pct:.1f}%) | "
                f"{rate:.1f}/sec | ETA: {eta_h:.1f}h | "
                f"Written: {written:,} | Err: {errors}"
            )
            print(f"  {msg}")
            log_f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
            log_f.flush()
            last_report = now

    elapsed = time.time() - t0
    summary = (
        f"Done: {written:,} written in {elapsed/3600:.1f}h "
        f"({written/elapsed:.1f}/sec) | Errors: {errors}"
    )
    print(f"\n  {summary}")
    log_f.write(f"{time.strftime('%H:%M:%S')} {summary}\n")
    log_f.flush()
    conn.close()


def run_model(model_name):
    global shutdown
    config = MODELS[model_name]
    col = config["column"]

    log_f = setup_logging(model_name)
    log_f.write(f"\n{'='*60}\n")
    log_f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Starting {model_name}\n")
    log_f.write(f"{'='*60}\n")

    print(f"\n{'='*60}")
    print(f"Vectorizing: {model_name}")
    print(f"  Column: {col} ({config['dims']}-dim)")
    print(f"  Server: {config['url']}")
    print(f"  Batch: {config['batch_size']}")
    print(f"  Log: {LOG_DIR}/vectorize_{model_name}.log")
    print(f"{'='*60}")

    conn = get_conn()
    ensure_column(conn, col, config["dims"])

    total = count_remaining(conn, col)
    conn.close()

    if total == 0:
        msg = f"All pages already have {model_name} embeddings!"
        print(f"  {msg}")
        log_f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
        log_f.close()
        return

    msg = f"Pages to embed: {total:,}"
    print(f"  {msg}")
    log_f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")

    read_q = Queue(maxsize=config["prefetch"] + 2)
    embed_q = Queue(maxsize=4)

    reader = threading.Thread(
        target=reader_thread, args=(config, read_q, total, log_f), daemon=True
    )
    embedder = threading.Thread(
        target=embedder_thread, args=(config, read_q, embed_q, log_f), daemon=True
    )
    writer = threading.Thread(
        target=writer_thread, args=(config, embed_q, total, log_f), daemon=True
    )

    reader.start()
    embedder.start()
    writer.start()

    reader.join()
    embedder.join()
    writer.join()

    log_f.close()


def show_status():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL AND length(text_content) > 10")
    total = cur.fetchone()[0]

    print(f"\nEmbedding Status ({total:,} eligible pages)\n")
    print(f"  {'Model':<20} {'Filled':>12} {'Remaining':>12} {'%':>8}")
    print(f"  {'-'*54}")

    for name, config in MODELS.items():
        col = config["column"]
        cur.execute(f"SELECT COUNT(*) FROM pages WHERE {col} IS NOT NULL")
        filled = cur.fetchone()[0]
        remaining = total - filled
        pct = filled / total * 100 if total > 0 else 0
        print(f"  {col:<20} {filled:>12,} {remaining:>12,} {pct:>7.1f}%")

    cur.execute("SELECT COUNT(*) FROM page_embeddings")
    old = cur.fetchone()[0]
    print(f"  {'page_embeddings(384)':<20} {old:>12,} {'-':>12} {'-':>8}")

    conn.close()


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"

    if action == "status":
        show_status()
    elif action == "all":
        # Run BGE-M3 first (fast), then Qwen3 (slow)
        for name in ["bge_m3", "qwen3"]:
            if not shutdown:
                run_model(name)
    elif action in MODELS:
        run_model(action)
    else:
        print(f"Usage: {sys.argv[0]} [qwen3|bge_m3|all|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
