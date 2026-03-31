#!/usr/bin/env python3
"""Import kabasshouse entities, chunks, and embeddings into PostgreSQL.

Downloads parquet files from HuggingFace and imports with dedup.
Uses source-provided unique IDs to prevent duplicates.

Usage:
    python -u scripts/import_kabasshouse.py entities    # Import entities (10.6M)
    python -u scripts/import_kabasshouse.py chunks      # Import chunks (2.2M)
    python -u scripts/import_kabasshouse.py embeddings  # Import embeddings (2.1M)
    python -u scripts/import_kabasshouse.py status      # Check import status
"""

import sys
import json
import time
import signal

import pyarrow.parquet as pq
import psycopg2
from huggingface_hub import HfApi, hf_hub_download

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
REPO = "kabasshouse/epstein-data"

shutdown = False
signal.signal(signal.SIGINT, lambda s, f: globals().__setitem__('shutdown', True))
signal.signal(signal.SIGTERM, lambda s, f: globals().__setitem__('shutdown', True))


def log(msg):
    print(msg, flush=True)


def get_parquet_files(subdir):
    api = HfApi()
    files = list(api.list_repo_tree(REPO, repo_type='dataset', path_in_repo=f'data/{subdir}'))
    return sorted([f for f in files if f.path.endswith('.parquet')], key=lambda x: x.path)


def import_entities():
    """Import 10.6M entities, unique by document_id + entity_type + value."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kabasshouse_entities (
            id INTEGER,
            document_id INTEGER,
            file_key TEXT,
            entity_type TEXT,
            entity_value TEXT,
            normalized_value TEXT,
            context TEXT,
            source_page INTEGER,
            extraction_model TEXT,
            PRIMARY KEY (document_id, entity_type, entity_value)
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ke_file_key ON kabasshouse_entities(file_key)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_ke_type ON kabasshouse_entities(entity_type)")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM kabasshouse_entities")
    existing = cur.fetchone()[0]
    if existing > 0:
        log(f"Already have {existing:,} entities, skipping.")
        conn.close()
        return

    parquet_files = get_parquet_files('entities')
    log(f"Importing entities from {len(parquet_files)} files...")

    total_inserted = 0
    t0 = time.time()

    for pf in parquet_files:
        if shutdown:
            break
        path = hf_hub_download(REPO, pf.path, repo_type='dataset')
        t = pq.read_table(path)
        cols = t.column_names

        inserted = 0
        for i in range(len(t)):
            row = []
            for col in cols:
                val = t.column(col)[i].as_py()
                if isinstance(val, (dict, list)):
                    val = json.dumps(val)
                row.append(val)

            try:
                cur.execute("""
                    INSERT INTO kabasshouse_entities 
                    (id, document_id, file_key, entity_type, entity_value, normalized_value, context, source_page, extraction_model)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (document_id, entity_type, entity_value) DO NOTHING
                """, row)
                if cur.rowcount > 0:
                    inserted += 1
            except Exception as e:
                conn.rollback()
                continue

        conn.commit()
        total_inserted += inserted
        elapsed = time.time() - t0
        log(f"  {pf.path.split('/')[-1]}: +{inserted:,} | total: {total_inserted:,} | {total_inserted/elapsed:.0f}/sec")

    conn.close()
    log(f"Entities done: {total_inserted:,} inserted")


def import_chunks():
    """Import 2.2M chunks, unique by document_id + chunk_index."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kabasshouse_chunks (
            id INTEGER,
            document_id INTEGER NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT,
            token_count INTEGER,
            char_start INTEGER,
            char_end INTEGER,
            PRIMARY KEY (document_id, chunk_index)
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_kc_doc ON kabasshouse_chunks(document_id)")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM kabasshouse_chunks")
    existing = cur.fetchone()[0]
    if existing > 0:
        log(f"Already have {existing:,} chunks, skipping.")
        conn.close()
        return

    parquet_files = get_parquet_files('chunks')
    log(f"Importing chunks from {len(parquet_files)} files...")

    total_inserted = 0
    t0 = time.time()

    for pf in parquet_files:
        if shutdown:
            break
        path = hf_hub_download(REPO, pf.path, repo_type='dataset')
        t = pq.read_table(path)
        cols = t.column_names

        inserted = 0
        for i in range(len(t)):
            row = [t.column(col)[i].as_py() for col in cols]
            try:
                cur.execute("""
                    INSERT INTO kabasshouse_chunks (id, document_id, chunk_index, content, token_count, char_start, char_end)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (document_id, chunk_index) DO NOTHING
                """, row)
                if cur.rowcount > 0:
                    inserted += 1
            except:
                conn.rollback()
                continue

        conn.commit()
        total_inserted += inserted
        elapsed = time.time() - t0
        log(f"  {pf.path.split('/')[-1]}: +{inserted:,} | total: {total_inserted:,} | {total_inserted/elapsed:.0f}/sec")

    conn.close()
    log(f"Chunks done: {total_inserted:,} inserted")


def import_embeddings():
    """Import 2.1M chunk embeddings, unique by chunk_id."""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS kabasshouse_chunk_embeddings (
            chunk_id INTEGER PRIMARY KEY,
            document_id INTEGER,
            embedding BYTEA,
            embedding_dim INTEGER DEFAULT 768,
            model TEXT DEFAULT 'gemini-embedding-001',
            source_text_hash TEXT
        )
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_kce_doc ON kabasshouse_chunk_embeddings(document_id)")
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM kabasshouse_chunk_embeddings")
    existing = cur.fetchone()[0]
    if existing > 0:
        log(f"Already have {existing:,} embeddings, skipping.")
        conn.close()
        return

    parquet_files = get_parquet_files('embeddings_chunk')
    log(f"Importing embeddings from {len(parquet_files)} files...")

    total_inserted = 0
    t0 = time.time()

    for pf in parquet_files:
        if shutdown:
            break
        path = hf_hub_download(REPO, pf.path, repo_type='dataset')
        t = pq.read_table(path)
        cols = t.column_names

        inserted = 0
        for i in range(len(t)):
            row = []
            for col in cols:
                val = t.column(col)[i].as_py()
                if isinstance(val, (list, bytes)):
                    val = bytes(val) if isinstance(val, list) else val
                row.append(val)

            try:
                cur.execute("""
                    INSERT INTO kabasshouse_chunk_embeddings (chunk_id, document_id, embedding, embedding_dim, model, source_text_hash)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (chunk_id) DO NOTHING
                """, row)
                if cur.rowcount > 0:
                    inserted += 1
            except:
                conn.rollback()
                continue

        conn.commit()
        total_inserted += inserted
        elapsed = time.time() - t0
        log(f"  {pf.path.split('/')[-1]}: +{inserted:,} | total: {total_inserted:,} | {total_inserted/elapsed:.0f}/sec")

    conn.close()
    log(f"Embeddings done: {total_inserted:,} inserted")


def show_status():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    for t in ['kabasshouse_entities', 'kabasshouse_chunks', 'kabasshouse_chunk_embeddings',
              'kabasshouse_financial_transactions', 'kabasshouse_derived_events',
              'kabasshouse_curated_docs', 'house_oversight_emails']:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            log(f"  {t}: {cur.fetchone()[0]:,}")
        except:
            log(f"  {t}: not created")
    conn.close()


def main():
    action = sys.argv[1] if len(sys.argv) > 1 else "status"
    if action == "status":
        show_status()
    elif action == "entities":
        import_entities()
    elif action == "chunks":
        import_chunks()
    elif action == "embeddings":
        import_embeddings()
    elif action == "all":
        import_entities()
        import_chunks()
        import_embeddings()
    else:
        log("Usage: import_kabasshouse.py [entities|chunks|embeddings|all|status]")


if __name__ == "__main__":
    main()
