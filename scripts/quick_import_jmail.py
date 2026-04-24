#!/usr/bin/env python3
"""Quick import for jMail photos and iMessage conversations."""

import os
from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

DATA_ROOT = Path(os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data"))
PG_CONFIG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", "5432")),
    "user": os.environ.get("PG_USER", "cbwinslow"),
    "password": os.environ.get("PG_PASSWORD", "123qweasd"),
    "dbname": os.environ.get("PG_DB", "epstein"),
}


def import_photos():
    file_path = DATA_ROOT / "supplementary/photos.parquet"
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return 0

    try:
        df = pd.read_parquet(file_path)
        print(f"Photos data: {len(df)} rows")

        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()

        # Create table if not exists (matching actual parquet schema)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS jmail_photos (
                id TEXT PRIMARY KEY,
                source TEXT,
                release_batch TEXT,
                original_filename TEXT,
                content_type TEXT,
                size BIGINT,
                width INT,
                height INT,
                image_description TEXT,
                source_url TEXT,
                imported_at TIMESTAMP DEFAULT NOW()
            )
        """)
        conn.commit()

        # Insert data - release_batch is TEXT in parquet
        rows = []
        for _, row in df.iterrows():
            rows.append(
                (
                    str(row.get("id", "")),
                    str(row.get("source", "")),
                    str(row.get("release_batch", "")),
                    str(row.get("original_filename", "")),
                    str(row.get("content_type", "")),
                    int(row.get("size", 0)),
                    int(row.get("width", 0)),
                    int(row.get("height", 0)),
                    str(row.get("image_description", "")),
                    str(row.get("source_url", "")),
                )
            )

        sql = """
            INSERT INTO jmail_photos (
                id, source, release_batch, original_filename, content_type,
                size, width, height, image_description, source_url
            ) VALUES %s
            ON CONFLICT (id) DO NOTHING
        """
        execute_values(cur, sql, rows, page_size=1000)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM jmail_photos")
        count = cur.fetchone()[0]
        print(f"✅ Imported {count} photos into jmail_photos table")

        cur.close()
        conn.close()
        return count

    except Exception as e:
        print(f"Error importing photos: {e}")
        return 0


def import_imessages():
    file_path = DATA_ROOT / "supplementary/message_conversations.parquet"
    if not file_path.exists():
        print(f"File not found: {file_path}")
        return 0

    try:
        df = pd.read_parquet(file_path)
        print(f"iMessage data: {len(df)} conversations")

        conn = psycopg2.connect(**PG_CONFIG)
        cur = conn.cursor()

        # Insert data
        rows = []
        for _, row in df.iterrows():
            rows.append(
                (
                    str(row.get("id", "")),
                    str(row.get("conversation_id", "")),
                    str(row.get("participants", "")),
                    int(row.get("message_count", 0)),
                    str(row.get("first_date", "")),
                    str(row.get("last_date", "")),
                    str(file_path),
                )
            )

        sql = """
            INSERT INTO jmail_imessages (
                id, conversation_id, participants, message_count, first_date, last_date, source_file
            ) VALUES %s
            ON CONFLICT (id) DO NOTHING
        """
        execute_values(cur, sql, rows, page_size=1000)
        conn.commit()

        cur.execute("SELECT COUNT(*) FROM jmail_imessages")
        count = cur.fetchone()[0]
        print(f"✅ Imported {count} iMessage conversations into jmail_imessages table")

        cur.close()
        conn.close()
        return count

    except Exception as e:
        print(f"Error importing iMessages: {e}")
        return 0


if __name__ == "__main__":
    print("=" * 60)
    print("Quick Import: jMail Photos + iMessages")
    print("=" * 60)

    photos_count = import_photos()
    imessages_count = import_imessages()

    print("=" * 60)
    print("✅ Quick Win Complete!")
    print(f"   Photos: {photos_count} rows")
    print(f"   iMessages: {imessages_count} rows")
    print("=" * 60)
