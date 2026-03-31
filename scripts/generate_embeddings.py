#!/usr/bin/env python3
"""Generate embeddings for all pages using llama.cpp GPU servers.

Supports:
- Qwen3-Embedding-8B (4096-dim) on port 8080
- BGE-M3 (1024-dim) on port 8081

Usage:
    python scripts/generate_embeddings.py bge_m3     # Start BGE-M3 (fast, ~1.8 days)
    python scripts/generate_embeddings.py qwen3      # Start Qwen3 (slow, ~7-16 days)
    python scripts/generate_embeddings.py all         # Run both sequentially
    python scripts/generate_embeddings.py status      # Check embedding status
"""

import json
import sys
import time
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import requests
from psycopg2.extras import execute_values

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

SERVERS = {
    "qwen3": {
        "url": "http://localhost:8080/embedding",
        "column": "qwen3_embedding",
        "dims": 4096,
        "batch_size": 100,
        "concurrent": 2,
        "max_text_len": 1500,
    },
    "bge_m3": {
        "url": "http://localhost:8081/embedding",
        "column": "bge_m3_embedding",
        "dims": 1024,
        "batch_size": 200,
        "concurrent": 1,
        "max_text_len": 1500,
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


def ensure_columns(conn):
    cur = conn.cursor()
    cur.execute("""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'pages' AND column_name = 'qwen3_embedding'
            ) THEN
                ALTER TABLE pages ADD COLUMN qwen3_embedding vector(4096);
            END IF;
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'pages' AND column_name = 'bge_m3_embedding'
            ) THEN
                ALTER TABLE pages ADD COLUMN bge_m3_embedding vector(1024);
            END IF;
        END $$;
    """)
    conn.commit()
    print("Embedding columns verified.")


def count_unembedded(conn, column):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*) FROM pages
        WHERE {column} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
    """)
    return cur.fetchone()[0]


def get_pages_batch(conn, column, batch_size, offset):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT id, text_content FROM pages
        WHERE {column} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
        ORDER BY id LIMIT %s OFFSET %s
    """, (batch_size, offset))
    return cur.fetchall()


def embed_batch(texts, server_url, timeout=300, max_text_len=1500):
    """Embed a batch of texts. Returns list of embeddings or None on failure."""
    # Truncate texts
    truncated = [(t or "")[:max_text_len] for t in texts]

    try:
        resp = requests.post(server_url, json={"content": truncated}, timeout=timeout)
        if resp.status_code == 400:
            # Token limit exceeded - try shorter texts
            shorter = [(t or "")[:500] for t in texts]
            resp = requests.post(server_url, json={"content": shorter}, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        embeddings = []
        for item in data:
            emb = item["embedding"]
            if isinstance(emb[0], list):
                emb = emb[0]
            embeddings.append(emb)
        return embeddings
    except Exception as e:
        # Try one by one as fallback
        results = []
        for t in truncated:
            try:
                r = requests.post(server_url, json={"content": [t[:500]]}, timeout=60)
                r.raise_for_status()
                d = r.json()
                emb = d[0]["embedding"]
                if isinstance(emb[0], list):
                    emb = emb[0]
                results.append(emb)
            except Exception:
                results.append(None)
        if any(r is not None for r in results):
            return results
        return None


def save_embeddings(conn, page_ids, embeddings, column, dims):
    cur = conn.cursor()
    rows = []
    for pid, emb in zip(page_ids, embeddings):
        if emb is not None and len(emb) == dims:
            vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
            rows.append((pid, vec))
    if rows:
        cur.executemany(f"UPDATE pages SET {column} = %s::vector WHERE id = %s",
                        [(vec, pid) for pid, vec in rows])
        conn.commit()
    return len(rows)


def process_model(model_name):
    global shutdown
    config = SERVERS[model_name]
    col = config["column"]

    print(f"\n{'='*60}")
    print(f"Embedding generation: {model_name}")
    print(f"  Column: {col} ({config['dims']}-dim)")
    print(f"  Server: {config['url']}")
    print(f"  Batch: {config['batch_size']} x {config['concurrent']} concurrent")
    print(f"{'='*60}")

    conn = get_conn()
    ensure_columns(conn)

    total = count_unembedded(conn, col)
    if total == 0:
        print(f"  All pages already have {model_name} embeddings!")
        conn.close()
        return

    print(f"  Pages to embed: {total:,}")
    processed = 0
    errors = 0
    t0 = time.time()
    offset = 0

    while not shutdown:
        pages = get_pages_batch(conn, col, config["batch_size"] * config["concurrent"], offset)
        if not pages:
            break

        # Split into sub-batches
        sub_batches = [pages[i:i + config["batch_size"]]
                       for i in range(0, len(pages), config["batch_size"])]

        with ThreadPoolExecutor(max_workers=config["concurrent"]) as ex:
            futs = {}
            for batch in sub_batches:
                ids = [p[0] for p in batch]
                texts = [(p[1] or "")[:config["max_text_len"]] for p in batch]
                futs[ex.submit(embed_batch, texts, config["url"])] = ids

            for fut in as_completed(futs):
                ids = futs[fut]
                embs = fut.result()
                if embs and len(embs) == len(ids):
                    processed += save_embeddings(conn, ids, embs, col, config["dims"])
                else:
                    errors += len(ids)

        elapsed = time.time() - t0
        rate = processed / elapsed if elapsed > 0 else 0
        eta_h = (total - processed) / rate / 3600 if rate > 0 else 0
        print(f"  {processed:,}/{total:,} ({processed/total*100:.1f}%) "
              f"| {rate:.1f}/sec | ETA: {eta_h:.1f}h | Err: {errors}")
        offset += len(pages)

    elapsed = time.time() - t0
    print(f"\n  {model_name}: {processed:,} done in {elapsed/3600:.1f}h ({processed/elapsed:.1f}/sec)")
    conn.close()


def show_status():
    conn = get_conn()
    cur = conn.cursor()
    for col in ["qwen3_embedding", "bge_m3_embedding"]:
        cur.execute(f"SELECT COUNT(*) FROM pages WHERE {col} IS NOT NULL")
        have = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM pages WHERE text_content IS NOT NULL AND length(text_content) > 10")
        total = cur.fetchone()[0]
        pct = have / total * 100 if total > 0 else 0
        print(f"  {col}: {have:,}/{total:,} ({pct:.1f}%)")
    conn.close()


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"

    if action == "status":
        show_status()
    elif action == "all":
        for name in SERVERS:
            if not shutdown:
                process_model(name)
    elif action in SERVERS:
        process_model(action)
    else:
        print(f"Usage: {sys.argv[0]} [qwen3|bge_m3|all|status]")
        sys.exit(1)


if __name__ == "__main__":
    main()
