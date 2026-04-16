#!/usr/bin/env python3
"""
Generate embeddings using RTX3060 endpoint
"""

import json
import sys
import time
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import requests
from psycopg2.extras import execute_values

# Configuration
# Windows machine with RTX3060 running Ollama
# Options: local IP (192.168.4.25) or Tailscale hostname (cbwwin)
WINDOWS_HOST = "192.168.4.25"  # Local network IP
# WINDOWS_HOST = "cbwwin"  # Tailscale hostname (requires tailscale on Linux box)
OLLAMA_PORT = "11434"
RTX3060_ENDPOINT = f"http://{WINDOWS_HOST}:{OLLAMA_PORT}/api/embed"
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

# Model configuration
# Options for RTX 3060 12GB:
# - mxbai-embed-large: 1024 dims, 64.68 MTEB, ~4GB VRAM [RECOMMENDED]
# - snowflake-arctic-embed-v2: 768 dims, ~3GB VRAM, legal-optimized
# - nomic-embed-text: 768 dims, 62.39 MTEB, ~2GB VRAM, longest context
OLLAMA_MODEL = "nomic-embed-text:latest"  # Confirmed working with Ollama API

MODEL_CONFIG = {
    "column": "rtx3060_embedding",
    "dims": 1024 if "large" in OLLAMA_MODEL else 768,
    "batch_size": 50,   # Conservative for RTX 3060
    "concurrent": 1,    # Single thread to avoid OOM
    "max_text_len": 8192,  # nomic-embed-text supports long contexts
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
    cur.execute(f"""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'pages' AND column_name = '{MODEL_CONFIG['column']}'
            ) THEN
                ALTER TABLE pages ADD COLUMN {MODEL_CONFIG['column']} vector({MODEL_CONFIG['dims']});
            END IF;
        END $$;
    """)
    conn.commit()
    print(f"Embedding column {MODEL_CONFIG['column']} verified.")

def count_unembedded(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*) FROM pages
        WHERE {MODEL_CONFIG['column']} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
    """)
    return cur.fetchone()[0]

def get_pages_batch(conn, batch_size, offset):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT id, text_content FROM pages
        WHERE {MODEL_CONFIG['column']} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
        ORDER BY id LIMIT %s OFFSET %s
    """, (batch_size, offset))
    return cur.fetchall()

def embed_batch(texts, server_url, timeout=300, max_text_len=1500):
    """Embed a batch of texts using Ollama API. Returns list of embeddings or None on failure."""
    # Truncate texts
    truncated = [(t or "")[:max_text_len] for t in texts]

    try:
        # Ollama API format for embeddings
        payload = {
            "model": OLLAMA_MODEL,
            "input": truncated
        }
        resp = requests.post(server_url, json=payload, timeout=timeout)
        resp.raise_for_status()
        data = resp.json()
        # Ollama returns embeddings in "embeddings" array
        embeddings = data.get("embeddings", [])
        return embeddings
    except Exception as e:
        print(f"Error embedding batch: {e}")
        return None

def save_embeddings(conn, page_ids, embeddings):
    cur = conn.cursor()
    rows = []
    for pid, emb in zip(page_ids, embeddings):
        if emb is not None and len(emb) == MODEL_CONFIG["dims"]:
            vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
            rows.append((pid, vec))
    if rows:
        cur.executemany(f"""UPDATE pages SET {MODEL_CONFIG['column']} = %s::vector WHERE id = %s""",
                        [(vec, pid) for pid, vec in rows])
        conn.commit()
    return len(rows)

def process_embeddings():
    global shutdown
    print(f"\n{'='*60}")
    print(f"Embedding generation: RTX3060")
    print(f"  Column: {MODEL_CONFIG['column']} ({MODEL_CONFIG['dims']}-dim)")
    print(f"  Server: {RTX3060_ENDPOINT}")
    print(f"  Batch: {MODEL_CONFIG['batch_size']} x {MODEL_CONFIG['concurrent']} concurrent")
    print(f"{'='*60}")

    conn = get_conn()
    ensure_columns(conn)

    total = count_unembedded(conn)
    if total == 0:
        print(f"  All pages already have {MODEL_CONFIG['column']} embeddings!")
        conn.close()
        return

    print(f"  Pages to embed: {total:,}")
    processed = 0
    errors = 0
    t0 = time.time()
    offset = 0

    while not shutdown:
        try:
            pages = get_pages_batch(conn, MODEL_CONFIG["batch_size"] * MODEL_CONFIG["concurrent"], offset)
        except psycopg2.OperationalError as e:
            print(f"  Database connection lost: {e}")
            print("  Attempting to reconnect in 5 seconds...")
            time.sleep(5)
            try:
                conn = get_conn()
                print("  Reconnected to database, resuming...")
                continue
            except Exception as reconnect_err:
                print(f"  Reconnection failed: {reconnect_err}")
                print("  Exiting - systemd will restart in 30s...")
                break

        if not pages:
            break

        # Split into sub-batches
        sub_batches = [pages[i:i + MODEL_CONFIG["batch_size"]]
                       for i in range(0, len(pages), MODEL_CONFIG["batch_size"])]

        with ThreadPoolExecutor(max_workers=MODEL_CONFIG["concurrent"]) as ex:
            futs = {}
            for batch in sub_batches:
                ids = [p[0] for p in batch]
                texts = [(p[1] or "")[:MODEL_CONFIG["max_text_len"]] for p in batch]
                futs[ex.submit(embed_batch, texts, RTX3060_ENDPOINT)] = ids

            for fut in as_completed(futs):
                ids = futs[fut]
                embs = fut.result()
                if embs and len(embs) == len(ids):
                    try:
                        processed += save_embeddings(conn, ids, embs)
                    except psycopg2.OperationalError as e:
                        print(f"  Database write failed: {e}")
                        print("  Will retry on next restart...")
                        errors += len(ids)
                else:
                    errors += len(ids)

        elapsed = time.time() - t0
        rate = processed / elapsed if elapsed > 0 else 0
        eta_h = (total - processed) / rate / 3600 if rate > 0 else 0
        print(f"  {processed:,}/{total:,} ({processed/total*100:.1f}%) "
              f"| {rate:.1f}/sec | ETA: {eta_h:.1f}h | Err: {errors}")
        offset += len(pages)

    elapsed = time.time() - t0
    print(f"\n  RTX3060: {processed:,} done in {elapsed/3600:.1f}h ({processed/elapsed:.1f}/sec)")
    conn.close()

    # COMPLETION NOTIFICATION
    if processed >= total - 100:  # Within 100 of total = essentially complete
        completion_msg = f"""
{'='*60}
EMBEDDINGS GENERATION COMPLETE!
{'='*60}
Time: {time.strftime('%Y-%m-%d %H:%M:%S')}
Total embedded: {processed:,} pages
Duration: {elapsed/3600:.1f} hours
Rate: {processed/elapsed:.1f}/sec

ACTION REQUIRED:
1. Stop the systemd service: sudo systemctl stop epstein-embeddings
2. Disable auto-start: sudo systemctl disable epstein-embeddings
3. Verify final count: psql -c "SELECT COUNT(rtx3060_embedding) FROM pages;"
4. Create index: psql -c "CREATE INDEX idx_rtx3060_embedding ON pages USING ivfflat (rtx3060_embedding vector_cosine_ops);"

Log location: /tmp/rtx3060_embeddings.log
{'='*60}
"""
        print(completion_msg)
        # Write completion marker file
        with open('/tmp/rtx3060_embeddings_COMPLETE', 'w') as f:
            f.write(completion_msg)
        # Also write to a persistent location
        with open('/home/cbwinslow/workspace/epstein/EMBEDDINGS_COMPLETE.txt', 'w') as f:
            f.write(completion_msg)

def main():
    process_embeddings()

if __name__ == "__main__":
    main()