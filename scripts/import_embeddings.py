#!/usr/bin/env python3
"""Import kabasshouse chunk embeddings (2.1M, 768-dim Gemini vectors)."""
import time
import signal
from huggingface_hub import hf_hub_download
import pyarrow.parquet as pq
import psycopg2

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
REPO = "kabasshouse/epstein-data"

shutdown = False
signal.signal(signal.SIGINT, lambda s, f: globals().__setitem__('shutdown', True))
signal.signal(signal.SIGTERM, lambda s, f: globals().__setitem__('shutdown', True))


def log(msg):
    print(msg, flush=True)


def main():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM kabasshouse_chunk_embeddings")
    existing = cur.fetchone()[0]
    if existing > 0:
        log(f"Already have {existing:,} embeddings, skipping.")
        conn.close()
        return

    with open("/tmp/embedding_files.txt") as f:
        file_paths = [line.strip() for line in f if line.strip()]

    log(f"Importing embeddings from {len(file_paths)} files...")

    total_inserted = 0
    t0 = time.time()

    for file_path in file_paths:
        if shutdown:
            break

        path = hf_hub_download(REPO, file_path, repo_type="dataset")
        t = pq.read_table(path)

        ids = t.column("id").to_pylist()
        chunk_ids = t.column("chunk_id").to_pylist()
        doc_ids = t.column("document_id").to_pylist()
        embeddings_raw = t.column("embedding").to_pylist()
        dims = t.column("embedding_dim").to_pylist()
        models = t.column("model").to_pylist()
        hashes = t.column("source_text_hash").to_pylist()
        created = t.column("created_at").to_pylist()

        inserted = 0
        for i in range(len(t)):
            emb = embeddings_raw[i]
            if emb is not None:
                vec = "[" + ",".join(f"{v:.6f}" for v in emb) + "]"
            else:
                continue

            try:
                cur.execute(
                    """INSERT INTO kabasshouse_chunk_embeddings
                       (id, chunk_id, document_id, embedding, embedding_dim, model, source_text_hash, created_at)
                       VALUES (%s, %s, %s, %s::vector(768), %s, %s, %s, %s)
                       ON CONFLICT (chunk_id) DO NOTHING""",
                    (ids[i], chunk_ids[i], doc_ids[i], vec, dims[i], models[i], hashes[i], created[i]),
                )
                if cur.rowcount > 0:
                    inserted += 1
            except Exception as e:
                conn.rollback()
                if inserted < 2:
                    log(f"  Error: {e}")
                continue

        conn.commit()
        total_inserted += inserted
        elapsed = time.time() - t0
        fname = file_path.split("/")[-1]
        log(f"  {fname}: +{inserted:,} | total: {total_inserted:,} | {total_inserted / elapsed:.0f}/sec")

    conn.close()
    elapsed = time.time() - t0
    log(f"Done: {total_inserted:,} embeddings in {elapsed / 60:.0f}min")


if __name__ == "__main__":
    main()
