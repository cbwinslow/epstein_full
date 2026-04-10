#!/usr/bin/env python3
"""
Quick import for jmail supplementary data (iMessages, photos)
Runs in parallel with main parquet processing
"""

import logging
import os

import pandas as pd
import psycopg2

DATA_ROOT = os.environ.get("EPSTEIN_DATA_ROOT", "/home/cbwinslow/workspace/epstein-data")

PG_CONFIG = {
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": int(os.environ.get("PG_PORT", "5432")),
    "user": os.environ.get("PG_USER", "cbwinslow"),
    "password": os.environ.get("PG_PASSWORD", "123qweasd"),
    "dbname": os.environ.get("PG_DB", "epstein"),
}


def import_imessages():
    """Import iMessage conversations."""
    file_path = f"{DATA_ROOT}/supplementary/imessage_conversations.parquet"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 0

    try:
        df = pd.read_parquet(file_path)
        print(f"iMessage data: {len(df)} conversations")

        conn = psycopg2.connect(**PG_CONFIG)
        with conn.cursor() as cur:
            # Create table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jmail_imessages (
                    id SERIAL PRIMARY KEY,
                    conversation_id TEXT,
                    participants TEXT,
                    message_count INTEGER,
                    first_date TEXT,
                    last_date TEXT,
                    source_file TEXT,
                    imported_at TIMESTAMP DEFAULT NOW()
                )
            """)
            conn.commit()

            # Insert data
            for _, row in df.iterrows():
                cur.execute("""
                    INSERT INTO jmail_imessages (conversation_id, participants, message_count, first_date, last_date, source_file)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    str(row.get('conversation_id', '')),
                    str(row.get('participants', '')),
                    int(row.get('message_count', 0)),
                    str(row.get('first_date', '')),
                    str(row.get('last_date', '')),
                    file_path
                ))
            conn.commit()

        conn.close()
        print(f"✓ Imported {len(df)} iMessage conversations")
        return len(df)

    except Exception as e:
        print(f"Error importing iMessages: {e}")
        return 0


def import_photos():
    """Import photos metadata."""
    file_path = f"{DATA_ROOT}/supplementary/photos.parquet"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return 0

    try:
        df = pd.read_parquet(file_path)
        print(f"Photos data: {len(df)} photos")

        conn = psycopg2.connect(**PG_CONFIG)
        with conn.cursor() as cur:
            # Create table if not exists
            cur.execute("""
                CREATE TABLE IF NOT EXISTS jmail_photos (
                    id SERIAL PRIMARY KEY,
                    photo_id TEXT,
                    file_name TEXT,
                    file_path TEXT,
                    date_taken TEXT,
                    people_detected TEXT,
                    source_file TEXT,
                    imported_at TIMESTAMP DEFAULT NOW()
                )
            """)
            conn.commit()

            # Insert data in batches
            batch_size = 1000
            imported = 0
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                for _, row in batch.iterrows():
                    cur.execute("""
                        INSERT INTO jmail_photos (photo_id, file_name, file_path, date_taken, people_detected, source_file)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                        str(row.get('id', '')),
                        str(row.get('file_name', '')),
                        str(row.get('file_path', '')),
                        str(row.get('date', '')),
                        str(row.get('people', '')),
                        file_path
                    ))
                conn.commit()
                imported += len(batch)
                print(f"  Progress: {imported}/{len(df)} photos")

        conn.close()
        print(f"✓ Imported {imported} photos")
        return imported

    except Exception as e:
        print(f"Error importing photos: {e}")
        return 0


if __name__ == "__main__":
    print("=" * 60)
    print("JMAIL SUPPLEMENTARY DATA IMPORT")
    print("=" * 60)

    print("\n[1/2] Importing iMessage conversations...")
    imsg_count = import_imessages()

    print("\n[2/2] Importing photos metadata...")
    photo_count = import_photos()

    print("\n" + "=" * 60)
    print(f"SUMMARY: {imsg_count} iMessages, {photo_count} photos")
    print("=" * 60)
