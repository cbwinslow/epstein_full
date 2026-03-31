#!/usr/bin/env python3
"""GPU-optimized embedding generator - keeps server constantly fed.

Pipelined architecture:
  Thread 1: Read batches from DB (prefetch ahead)
  Thread 2: Send to GPU server, get embeddings  
  Thread 3: Write embeddings to DB
  
All three run concurrently so the GPU server never waits.
"""

import json
import sys
import time
import signal
import threading
from queue import Queue, Empty

import psycopg2
import requests
from psycopg2.extras import execute_values

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
SERVER_URL = "http://localhost:8081/embedding"
COLUMN = "bge_m3_embedding"
DIMS = 1024
BATCH_SIZE = 200
MAX_TEXT_LEN = 1500
PREFETCH_BATCHES = 4  # Keep 4 batches ahead

shutdown = False

def signal_handler(sig, frame):
    global shutdown
    print("\nShutting down...")
    shutdown = True

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def get_conn():
    return psycopg2.connect(DB_URL)

def reader_thread(read_q, total_count):
    """Read pages from DB and put in queue."""
    conn = get_conn()
    cur = conn.cursor()
    offset = 0
    batch_num = 0
    
    while not shutdown:
        cur.execute(f"""
            SELECT id, LEFT(text_content, %s) FROM pages
            WHERE {COLUMN} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
            ORDER BY id LIMIT %s OFFSET %s
        """, (MAX_TEXT_LEN, BATCH_SIZE, offset))
        
        rows = cur.fetchall()
        if not rows:
            read_q.put(None)  # Signal end
            break
        
        read_q.put((batch_num, rows))
        offset += len(rows)
        batch_num += 1
        
        # Don't read too far ahead
        while read_q.qsize() >= PREFETCH_BATCHES and not shutdown:
            time.sleep(0.1)
    
    conn.close()

def embedder_thread(read_q, embed_q):
    """Take batches from read queue, embed via GPU, put in embed queue."""
    while not shutdown:
        try:
            item = read_q.get(timeout=2)
        except Empty:
            continue
        
        if item is None:
            embed_q.put(None)
            break
        
        batch_num, rows = item
        page_ids = [r[0] for r in rows]
        texts = [(r[1] or "")[:MAX_TEXT_LEN] for r in rows]
        
        try:
            resp = requests.post(SERVER_URL, json={"content": texts}, timeout=300)
            if resp.status_code == 400:
                # Token limit - try shorter
                shorter = [t[:500] for t in texts]
                resp = requests.post(SERVER_URL, json={"content": shorter}, timeout=300)
            resp.raise_for_status()
            data = resp.json()
            
            embeddings = []
            for item in data:
                emb = item["embedding"]
                if isinstance(emb[0], list):
                    emb = emb[0]
                embeddings.append(emb)
            
            embed_q.put((batch_num, page_ids, embeddings))
        except Exception as e:
            print(f"  Embed error batch {batch_num}: {e}")
            embed_q.put((batch_num, page_ids, None))

def writer_thread(embed_q, total_count):
    """Take embedded batches and write to DB."""
    conn = get_conn()
    cur = conn.cursor()
    
    processed = 0
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
        
        batch_num, page_ids, embeddings = item
        
        if embeddings is None:
            errors += len(page_ids)
            processed += len(page_ids)
        else:
            # Batch update
            rows = []
            for pid, emb in zip(page_ids, embeddings):
                if emb is not None and len(emb) == DIMS:
                    vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
                    rows.append((pid, vec))
            
            if rows:
                cur.executemany(
                    f"UPDATE pages SET {COLUMN} = %s::vector WHERE id = %s",
                    [(vec, pid) for pid, vec in rows]
                )
                conn.commit()
            
            processed += len(page_ids)
        
        # Report every 5 seconds
        now = time.time()
        if now - last_report >= 5:
            elapsed = now - t0
            rate = processed / elapsed if elapsed > 0 else 0
            eta_h = (total_count - processed) / rate / 3600 if rate > 0 else 0
            pct = processed / total_count * 100 if total_count > 0 else 0
            print(f"  {processed:,}/{total_count:,} ({pct:.1f}%) | {rate:.0f}/sec | ETA: {eta_h:.1f}h | Err: {errors}")
            last_report = now
    
    elapsed = time.time() - t0
    print(f"\n  Done: {processed:,} in {elapsed/3600:.1f}h ({processed/elapsed:.0f}/sec)")
    conn.close()

def main():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(f"""
        SELECT COUNT(*) FROM pages
        WHERE {COLUMN} IS NULL AND text_content IS NOT NULL AND length(text_content) > 10
    """)
    total = cur.fetchone()[0]
    conn.close()
    
    if total == 0:
        print("All pages already embedded!")
        return
    
    print(f"Pages to embed: {total:,}")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Starting pipelined embedding...")
    
    read_q = Queue(maxsize=PREFETCH_BATCHES + 2)
    embed_q = Queue(maxsize=2)
    
    reader = threading.Thread(target=reader_thread, args=(read_q, total))
    embedder = threading.Thread(target=embedder_thread, args=(read_q, embed_q))
    writer = threading.Thread(target=writer_thread, args=(embed_q, total))
    
    reader.start()
    embedder.start()
    writer.start()
    
    reader.join()
    embedder.join()
    writer.join()

if __name__ == "__main__":
    main()
