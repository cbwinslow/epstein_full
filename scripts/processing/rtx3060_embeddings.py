#!/usr/bin/env python3
"""Generate page embeddings through the remote Windows Ollama GPU endpoint."""

import argparse
import os
import re
import signal
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import psycopg2
import requests
from psycopg2.extras import execute_values

DB_URL = os.getenv("EPSTEIN_DB_URL", "postgresql://cbwinslow:123qweasd@localhost:5432/epstein")
DEFAULT_ENDPOINT = os.getenv("OLLAMA_EMBED_ENDPOINT", "http://192.168.4.25:11343/api/embed")
DEFAULT_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text:latest")
DEFAULT_COLUMN = os.getenv("OLLAMA_EMBED_COLUMN", "rtx3060_embedding")
DEFAULT_DIMS = int(os.getenv("OLLAMA_EMBED_DIMS", "768"))
DEFAULT_BATCH_SIZE = int(os.getenv("OLLAMA_EMBED_BATCH", "50"))
DEFAULT_CONCURRENT = int(os.getenv("OLLAMA_EMBED_CONCURRENT", "1"))
DEFAULT_MAX_TEXT_LEN = int(os.getenv("OLLAMA_EMBED_MAX_TEXT", "1500"))

IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
shutdown = False


def signal_handler(_sig, _frame):
    global shutdown
    print("\nGraceful shutdown requested...")
    shutdown = True


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def parse_args():
    parser = argparse.ArgumentParser(description="Generate page embeddings with remote Ollama")
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT, help="Ollama /api/embed endpoint")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Ollama embedding model")
    parser.add_argument(
        "--column", default=DEFAULT_COLUMN, help="pages table vector column to write"
    )
    parser.add_argument(
        "--dims", type=int, default=DEFAULT_DIMS, help="expected embedding dimensions"
    )
    parser.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE)
    parser.add_argument("--concurrent", type=int, default=DEFAULT_CONCURRENT)
    parser.add_argument("--max-text-len", type=int, default=DEFAULT_MAX_TEXT_LEN)
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--status", action="store_true", help="show DB embedding status and exit")
    parser.add_argument("--check-endpoint", action="store_true", help="probe Ollama and exit")
    parser.add_argument(
        "--reset-column",
        action="store_true",
        help="set the target column to NULL before generation; required when changing models",
    )
    return parser.parse_args()


def require_identifier(value: str) -> str:
    if not IDENTIFIER_RE.match(value):
        raise ValueError(f"Unsafe SQL identifier: {value!r}")
    return value


def get_conn():
    return psycopg2.connect(DB_URL)


def ollama_embed(texts: list[str], endpoint: str, model: str, timeout: int) -> list[list[float]]:
    payload = {"model": model, "input": texts}
    response = requests.post(endpoint, json=payload, timeout=timeout)
    response.raise_for_status()
    data = response.json()

    if "embeddings" in data:
        return data["embeddings"]
    if "embedding" in data:
        return [data["embedding"]]
    raise RuntimeError(f"Ollama response did not contain embeddings: keys={sorted(data.keys())}")


def probe_endpoint(args) -> int:
    try:
        embeddings = ollama_embed(
            ["Epstein financial disclosure embedding smoke test."], args.endpoint, args.model, 30
        )
    except Exception as exc:
        print(f"Endpoint check failed: {exc}")
        return 1

    if not embeddings:
        print("Endpoint check failed: empty embeddings response")
        return 1

    dims = len(embeddings[0])
    print(f"Endpoint OK: {args.endpoint}")
    print(f"Model: {args.model}")
    print(f"Dimensions: {dims}")
    if dims != args.dims:
        print(f"Configured dims mismatch: --dims {args.dims}, endpoint returned {dims}")
        return 2
    return 0


def ensure_column(conn, column: str, dims: int, reset: bool = False):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns
                WHERE table_name = 'pages' AND column_name = %s
            )
            """,
            (column,),
        )
        exists = cur.fetchone()[0]
        if not exists:
            cur.execute(f"ALTER TABLE pages ADD COLUMN {column} vector({dims})")
            print(f"Created pages.{column} as vector({dims}).")
        elif reset:
            cur.execute(f"UPDATE pages SET {column} = NULL WHERE {column} IS NOT NULL")
            print(f"Reset {cur.rowcount:,} existing values in pages.{column}.")
    conn.commit()


def count_pages(conn, column: str) -> tuple[int, int]:
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT
                COUNT(*) FILTER (WHERE text_content IS NOT NULL AND length(text_content) > 10),
                COUNT(*) FILTER (WHERE {column} IS NOT NULL)
            FROM pages
            """
        )
        total, embedded = cur.fetchone()
    return total, embedded


def sample_vector_dims(conn, column: str) -> int | None:
    with conn.cursor() as cur:
        cur.execute(f"SELECT vector_dims({column}) FROM pages WHERE {column} IS NOT NULL LIMIT 1")
        row = cur.fetchone()
    return row[0] if row else None


def show_status(args):
    column = require_identifier(args.column)
    conn = get_conn()
    try:
        ensure_column(conn, column, args.dims, reset=False)
        total, embedded = count_pages(conn, column)
        dims = sample_vector_dims(conn, column)
        remaining = total - embedded
        pct = embedded / total * 100 if total else 0
        print(f"Column: pages.{column}")
        print(f"Model: {args.model}")
        print(f"Configured endpoint: {args.endpoint}")
        print(f"Embedded: {embedded:,}/{total:,} ({pct:.2f}%)")
        print(f"Remaining: {remaining:,}")
        print(f"Stored dimensions: {dims if dims is not None else 'none yet'}")
    finally:
        conn.close()


def get_pages_batch(
    conn, column: str, batch_size: int, last_id: int, max_text_len: int
) -> list[tuple[int, str]]:
    with conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT id, LEFT(text_content, %s)
            FROM pages
            WHERE {column} IS NULL
              AND text_content IS NOT NULL
              AND length(text_content) > 10
              AND id > %s
            ORDER BY id
            LIMIT %s
            """,
            (max_text_len, last_id, batch_size),
        )
        return cur.fetchall()


def vector_literal(embedding: list[float]) -> str:
    return "[" + ",".join(f"{value:.8f}" for value in embedding) + "]"


def save_embeddings(
    conn, column: str, dims: int, page_ids: list[int], embeddings: list[list[float]]
) -> int:
    rows = []
    for page_id, embedding in zip(page_ids, embeddings):
        if embedding is not None and len(embedding) == dims:
            rows.append((page_id, vector_literal(embedding)))
    if not rows:
        return 0

    with conn.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS _tmp_remote_ollama_embeddings")
        cur.execute(
            f"CREATE TEMP TABLE _tmp_remote_ollama_embeddings (id INTEGER PRIMARY KEY, embedding vector({dims}))"
        )
        execute_values(
            cur,
            "INSERT INTO _tmp_remote_ollama_embeddings (id, embedding) VALUES %s",
            rows,
            template="(%s, %s::vector)",
        )
        cur.execute(
            f"""
            UPDATE pages
            SET {column} = tmp.embedding
            FROM _tmp_remote_ollama_embeddings tmp
            WHERE pages.id = tmp.id
            """
        )
        updated = cur.rowcount
        cur.execute("DROP TABLE _tmp_remote_ollama_embeddings")
    conn.commit()
    return updated


def embed_batch(args, texts: list[str]) -> list[list[float]] | None:
    retry_lengths = []
    for length in (args.max_text_len, 1500, 512):
        if length > 0 and length not in retry_lengths:
            retry_lengths.append(length)

    last_error = None
    for length in retry_lengths:
        truncated = [(text or "")[:length] for text in texts]
        try:
            return ollama_embed(truncated, args.endpoint, args.model, args.timeout)
        except requests.HTTPError as exc:
            last_error = exc
            if exc.response is None or exc.response.status_code != 400:
                break
        except Exception as exc:
            last_error = exc
            break

    if len(texts) > 1:
        results = []
        for text in texts:
            single = embed_batch(args, [text])
            results.append(single[0] if single else None)
        if any(result is not None for result in results):
            return results

    print(f"Embedding batch failed: {last_error}")
    return None


def process_embeddings(args):
    global shutdown
    column = require_identifier(args.column)

    print("=" * 72)
    print("Remote Ollama page embedding generation")
    print(f"Endpoint: {args.endpoint}")
    print(f"Model: {args.model}")
    print(f"Column: pages.{column} vector({args.dims})")
    print(f"Batch: {args.batch_size} x {args.concurrent}")
    print("=" * 72)

    endpoint_status = probe_endpoint(args)
    if endpoint_status != 0:
        sys.exit(endpoint_status)

    conn = get_conn()
    ensure_column(conn, column, args.dims, reset=args.reset_column)

    stored_dims = sample_vector_dims(conn, column)
    if stored_dims is not None and stored_dims != args.dims:
        conn.close()
        raise RuntimeError(
            f"Existing pages.{column} stores {stored_dims}-dim vectors, but --dims is {args.dims}. "
            "Use a new column or reset/recreate the column for the new model."
        )

    total, embedded_before = count_pages(conn, column)
    remaining = total - embedded_before
    if remaining <= 0:
        print(f"All pages already have {column} embeddings.")
        conn.close()
        return

    print(f"Pages with text: {total:,}")
    print(f"Already embedded: {embedded_before:,}")
    print(f"Remaining: {remaining:,}")

    processed = 0
    errors = 0
    last_id = 0
    started = time.time()

    while not shutdown:
        pages = get_pages_batch(
            conn, column, args.batch_size * args.concurrent, last_id, args.max_text_len
        )
        if not pages:
            break
        last_id = pages[-1][0]

        sub_batches = [
            pages[index : index + args.batch_size]
            for index in range(0, len(pages), args.batch_size)
        ]
        with ThreadPoolExecutor(max_workers=args.concurrent) as executor:
            futures = {
                executor.submit(embed_batch, args, [row[1] for row in batch]): [
                    row[0] for row in batch
                ]
                for batch in sub_batches
            }
            for future in as_completed(futures):
                page_ids = futures[future]
                embeddings = future.result()
                if not embeddings or len(embeddings) != len(page_ids):
                    errors += len(page_ids)
                    continue
                try:
                    processed += save_embeddings(conn, column, args.dims, page_ids, embeddings)
                except Exception as exc:
                    conn.rollback()
                    errors += len(page_ids)
                    print(f"Database write failed: {exc}")

        elapsed = max(time.time() - started, 0.001)
        rate = processed / elapsed
        eta_hours = (remaining - processed) / rate / 3600 if rate > 0 else 0
        print(
            f"{processed:,}/{remaining:,} this run | "
            f"{embedded_before + processed:,}/{total:,} total | "
            f"{rate:.1f}/sec | ETA {eta_hours:.1f}h | errors {errors:,}"
        )

    elapsed = max(time.time() - started, 0.001)
    print(
        f"Run complete: {processed:,} embeddings in {elapsed / 3600:.2f}h ({processed / elapsed:.1f}/sec)"
    )
    conn.close()


def main():
    args = parse_args()
    if args.status:
        show_status(args)
        return
    if args.check_endpoint:
        sys.exit(probe_endpoint(args))
    process_embeddings(args)


if __name__ == "__main__":
    main()
