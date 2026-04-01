#!/usr/bin/env python3
"""Minimal embedding generator - maximize GPU throughput."""
import sys, time, signal, psycopg2, requests
from psycopg2.extras import execute_values

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
SERVER = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8081/embedding"
COLUMN = sys.argv[2] if len(sys.argv) > 2 else "bge_m3_embedding"
DIMS = int(sys.argv[3]) if len(sys.argv) > 3 else 1024
BATCH = 200
MAX_TEXT = 200

shutdown = False
signal.signal(signal.SIGINT, lambda s,f: globals().__setitem__('shutdown', True))
signal.signal(signal.SIGTERM, lambda s,f: globals().__setitem__('shutdown', True))

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Ensure column exists
cur.execute(f"ALTER TABLE pages ADD COLUMN IF NOT EXISTS {COLUMN} vector({DIMS})")
conn.commit()

# Count unembedded
cur.execute(f"SELECT COUNT(*) FROM pages WHERE {COLUMN} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10")
total = cur.fetchone()[0]
print(f"Pages: {total:,} | Column: {COLUMN} | Dims: {DIMS}")
if total == 0:
    sys.exit(0)

processed = 0
errors = 0
t0 = time.time()
last_id = 0

while not shutdown:
    # Read batch (keyset pagination - much faster than OFFSET)
    cur.execute(f"""
        SELECT id, LEFT(text_content, %s) FROM pages
        WHERE {COLUMN} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
          AND id > %s
        ORDER BY id LIMIT %s
    """, (MAX_TEXT, last_id, BATCH))
    rows = cur.fetchall()
    if not rows:
        break

    page_ids = [r[0] for r in rows]
    texts = [(r[1] or "")[:MAX_TEXT] for r in rows]

    # Embed
    try:
        resp = requests.post(SERVER, json={"content": texts}, timeout=300)
        if resp.status_code == 400:
            resp = requests.post(SERVER, json={"content": [t[:100] for t in texts]}, timeout=300)
        resp.raise_for_status()
        data = resp.json()

        # Write batch via temp table
        update_rows = []
        for pid, item in zip(page_ids, data):
            emb = item["embedding"]
            if isinstance(emb[0], list):
                emb = emb[0]
            if len(emb) == DIMS:
                vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
                update_rows.append((pid, vec))

        if update_rows:
            cur.execute("DROP TABLE IF EXISTS _tmp_emb")
            cur.execute(f"CREATE TEMP TABLE _tmp_emb (id INTEGER PRIMARY KEY, emb vector({DIMS}))")
            execute_values(cur, "INSERT INTO _tmp_emb (id, emb) VALUES %s", update_rows)
            cur.execute(f"UPDATE pages SET {COLUMN} = te.emb FROM _tmp_emb te WHERE pages.id = te.id")
            cur.execute("DROP TABLE _tmp_emb")
            conn.commit()

        processed += len(page_ids)
    except Exception as e:
        errors += len(page_ids)
        conn.rollback()
        if errors <= 5:
            print(f"  Error: {e}")

    last_id = page_ids[-1] if page_ids else last_id

    # Progress
    elapsed = time.time() - t0
    rate = processed / elapsed if elapsed > 0 else 0
    eta = (total - processed) / rate / 3600 if rate > 0 else 0
    if processed % 1000 < BATCH:
        print(f"  {processed:,}/{total:,} ({processed/total*100:.1f}%) | {rate:.0f}/sec | ETA: {eta:.1f}h | Err: {errors}")

elapsed = time.time() - t0
print(f"\nDone: {processed:,} in {elapsed/3600:.1f}h ({processed/elapsed:.0f}/sec)")
conn.close()
