#!/usr/bin/env python3
"""Import all unimported local data files to PostgreSQL.

Imports:
- persons_registry.json → person_registry table
- extracted_entities_filtered.json → extracted_entities table
- phone_numbers_enriched.csv → phone_numbers table
- imessage_conversations.parquet → imessage_conversations table
- imessage_messages.parquet → imessage_messages table
- photos.parquet → photo_metadata table
- photo_faces.parquet → photo_faces table
- people.parquet → photo_people table
- DOJ audit CSVs → doj_audit_* tables
"""

import json
import csv
import sys
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
RESEARCH_DATA = Path("/home/cbwinslow/workspace/epstein/Epstein-research-data")
SUPPLEMENTARY = Path("/mnt/data/epstein-project/supplementary")
DOJ_AUDIT = RESEARCH_DATA / "doj_audit"
ALTERATION = RESEARCH_DATA / "alteration_analysis"


def get_conn():
    return psycopg2.connect(DB_URL)


def create_tables(conn):
    """Create all import tables."""
    cur = conn.cursor()

    # person_registry - unified person registry
    cur.execute("""
        CREATE TABLE IF NOT EXISTS person_registry (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            slug TEXT,
            category TEXT,
            aliases TEXT[],
            search_terms TEXT[],
            sources TEXT[],
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_person_registry_name ON person_registry(name);
        CREATE INDEX IF NOT EXISTS idx_person_registry_slug ON person_registry(slug);
        CREATE INDEX IF NOT EXISTS idx_person_registry_category ON person_registry(category);
    """)

    # extracted_entities - filtered NER entities
    cur.execute("""
        CREATE TABLE IF NOT EXISTS extracted_entities (
            id SERIAL PRIMARY KEY,
            entity_value TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            document_count INTEGER,
            efta_numbers TEXT[],
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_extracted_entities_value ON extracted_entities(entity_value);
        CREATE INDEX IF NOT EXISTS idx_extracted_entities_type ON extracted_entities(entity_type);
        CREATE INDEX IF NOT EXISTS idx_extracted_entities_count ON extracted_entities(document_count DESC);
    """)

    # phone_numbers - enriched phone data
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phone_numbers (
            id SERIAL PRIMARY KEY,
            number TEXT NOT NULL,
            formatted TEXT,
            call_count INTEGER,
            valid BOOLEAN,
            location TEXT,
            carrier TEXT,
            phone_type TEXT,
            timezone TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_phone_numbers_number ON phone_numbers(number);
        CREATE INDEX IF NOT EXISTS idx_phone_numbers_call_count ON phone_numbers(call_count DESC);
    """)

    # imessage_conversations
    cur.execute("""
        CREATE TABLE IF NOT EXISTS imessage_conversations (
            id SERIAL PRIMARY KEY,
            conversation_id TEXT,
            participants TEXT[],
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            message_count INTEGER,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # imessage_messages
    cur.execute("""
        CREATE TABLE IF NOT EXISTS imessage_messages (
            id SERIAL PRIMARY KEY,
            message_id TEXT,
            conversation_id TEXT,
            sender TEXT,
            recipient TEXT,
            text TEXT,
            timestamp TIMESTAMP,
            is_from_me BOOLEAN,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_imessage_conv ON imessage_messages(conversation_id);
        CREATE INDEX IF NOT EXISTS idx_imessage_sender ON imessage_messages(sender);
        CREATE INDEX IF NOT EXISTS idx_imessage_ts ON imessage_messages(timestamp);
    """)

    # photo_metadata
    cur.execute("""
        CREATE TABLE IF NOT EXISTS photo_metadata (
            id SERIAL PRIMARY KEY,
            photo_id TEXT,
            filename TEXT,
            date TIMESTAMP,
            location TEXT,
            description TEXT,
            source TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # photo_faces
    cur.execute("""
        CREATE TABLE IF NOT EXISTS photo_faces (
            id SERIAL PRIMARY KEY,
            face_id TEXT,
            photo_id TEXT,
            person_name TEXT,
            confidence REAL,
            bbox JSONB,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # photo_people
    cur.execute("""
        CREATE TABLE IF NOT EXISTS photo_people (
            id SERIAL PRIMARY KEY,
            person_id TEXT,
            name TEXT,
            photo_count INTEGER,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    # DOJ audit tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doj_audit_confirmed_removed (
            id SERIAL PRIMARY KEY,
            efta_number TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS doj_audit_flagged (
            id SERIAL PRIMARY KEY,
            efta_number TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS doj_audit_flagged_details (
            id SERIAL PRIMARY KEY,
            efta_number TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS doj_audit_size_mismatches (
            id SERIAL PRIMARY KEY,
            efta_number TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS doj_audit_alterations (
            id SERIAL PRIMARY KEY,
            efta_number TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS doj_audit_removed_entities (
            id SERIAL PRIMARY KEY,
            entity_value TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS doj_audit_sample_verification (
            id SERIAL PRIMARY KEY,
            efta_number TEXT,
            raw_data JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    print("All tables created/verified.")


def import_person_registry(conn):
    """Import persons_registry.json → person_registry table."""
    filepath = RESEARCH_DATA / "persons_registry.json"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    with open(filepath) as f:
        data = json.load(f)

    cur = conn.cursor()
    cur.execute("TRUNCATE person_registry RESTART IDENTITY")

    rows = []
    for p in data:
        rows.append((
            p.get("name", ""),
            p.get("slug", ""),
            p.get("category", ""),
            p.get("aliases", []),
            p.get("search_terms", []),
            p.get("sources", []),
        ))

    execute_values(cur,
        "INSERT INTO person_registry (name, slug, category, aliases, search_terms, sources) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  person_registry: {len(rows)} rows imported")
    return len(rows)


def import_extracted_entities(conn):
    """Import extracted_entities_filtered.json → extracted_entities table."""
    filepath = RESEARCH_DATA / "extracted_entities_filtered.json"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    with open(filepath) as f:
        data = json.load(f)

    cur = conn.cursor()
    cur.execute("TRUNCATE extracted_entities RESTART IDENTITY")

    rows = []
    for entity_type in ["names", "organizations", "emails", "phones", "amounts"]:
        for e in data.get(entity_type, []):
            rows.append((
                e.get("entity_value", ""),
                e.get("entity_type", entity_type.rstrip("s")),
                e.get("document_count", 0),
                e.get("efta_numbers", []),
            ))

    execute_values(cur,
        "INSERT INTO extracted_entities (entity_value, entity_type, document_count, efta_numbers) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  extracted_entities: {len(rows)} rows imported")
    return len(rows)


def import_phone_numbers(conn):
    """Import phone_numbers_enriched.csv → phone_numbers table."""
    filepath = RESEARCH_DATA / "phone_numbers_enriched.csv"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    cur = conn.cursor()
    cur.execute("TRUNCATE phone_numbers RESTART IDENTITY")

    rows = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append((
                row.get("number", ""),
                row.get("formatted", ""),
                int(row["call_count"]) if row.get("call_count") else 0,
                row.get("valid", "").lower() == "true",
                row.get("location", ""),
                row.get("carrier", ""),
                row.get("type", ""),
                row.get("timezone", ""),
            ))

    execute_values(cur,
        "INSERT INTO phone_numbers (number, formatted, call_count, valid, location, carrier, phone_type, timezone) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  phone_numbers: {len(rows)} rows imported")
    return len(rows)


def import_parquet_table(conn, filepath, table_name, column_map=None):
    """Generic parquet importer using pandas."""
    import pandas as pd

    if not Path(filepath).exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    df = pd.read_parquet(filepath)
    if column_map:
        df = df.rename(columns=column_map)

    cur = conn.cursor()
    cur.execute(f"TRUNCATE {table_name} RESTART IDENTITY")

    # Convert all columns to strings for JSONB storage of complex types
    cols = list(df.columns)
    col_str = ", ".join(cols)
    placeholders = ", ".join(["%s"] * len(cols))

    rows = []
    for _, row in df.iterrows():
        vals = []
        for c in cols:
            v = row[c]
            if pd.isna(v):
                vals.append(None)
            elif isinstance(v, (list, dict)):
                vals.append(json.dumps(v, default=str))
            else:
                vals.append(str(v) if not isinstance(v, (int, float, bool)) else v)
        rows.append(tuple(vals))

    execute_values(cur,
        f"INSERT INTO {table_name} ({col_str}, raw_data) VALUES %s",
        [(r + (None,)) for r in rows]
    )
    conn.commit()
    print(f"  {table_name}: {len(rows)} rows imported")
    return len(rows)


def import_imessage_conversations(conn):
    """Import imessage_conversations.parquet."""
    import pandas as pd

    filepath = SUPPLEMENTARY / "imessage_conversations.parquet"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    df = pd.read_parquet(filepath)
    cur = conn.cursor()
    cur.execute("TRUNCATE imessage_conversations RESTART IDENTITY")

    rows = []
    for _, row in df.iterrows():
        raw = json.dumps({k: str(v) if not pd.isna(v) else None for k, v in row.items()}, default=str)
        rows.append((
            str(row.iloc[0]) if len(row) > 0 and not pd.isna(row.iloc[0]) else None,
            None,  # participants
            None,  # start_date
            None,  # end_date
            None,  # message_count
            raw,
        ))

    execute_values(cur,
        "INSERT INTO imessage_conversations (conversation_id, participants, start_date, end_date, message_count, raw_data) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  imessage_conversations: {len(rows)} rows imported")
    return len(rows)


def import_imessage_messages(conn):
    """Import imessage_messages.parquet."""
    import pandas as pd

    filepath = SUPPLEMENTARY / "imessage_messages.parquet"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    df = pd.read_parquet(filepath)
    cur = conn.cursor()
    cur.execute("TRUNCATE imessage_messages RESTART IDENTITY")

    rows = []
    for _, row in df.iterrows():
        raw = json.dumps({k: str(v) if not pd.isna(v) else None for k, v in row.items()}, default=str)
        rows.append((
            str(row.iloc[0]) if len(row) > 0 and not pd.isna(row.iloc[0]) else None,
            None,  # conversation_id
            None,  # sender
            None,  # recipient
            None,  # text
            None,  # timestamp
            None,  # is_from_me
            raw,
        ))

    execute_values(cur,
        "INSERT INTO imessage_messages (message_id, conversation_id, sender, recipient, text, timestamp, is_from_me, raw_data) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  imessage_messages: {len(rows)} rows imported")
    return len(rows)


def import_photo_metadata(conn):
    """Import photos.parquet."""
    import pandas as pd

    filepath = SUPPLEMENTARY / "photos.parquet"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    df = pd.read_parquet(filepath)
    cur = conn.cursor()
    cur.execute("TRUNCATE photo_metadata RESTART IDENTITY")

    rows = []
    for _, row in df.iterrows():
        raw = json.dumps({k: str(v) if not pd.isna(v) else None for k, v in row.items()}, default=str)
        rows.append((
            str(row.iloc[0]) if len(row) > 0 and not pd.isna(row.iloc[0]) else None,
            None, None, None, None, None, raw,
        ))

    execute_values(cur,
        "INSERT INTO photo_metadata (photo_id, filename, date, location, description, source, raw_data) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  photo_metadata: {len(rows)} rows imported")
    return len(rows)


def import_photo_faces(conn):
    """Import photo_faces.parquet."""
    import pandas as pd

    filepath = SUPPLEMENTARY / "photo_faces.parquet"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    df = pd.read_parquet(filepath)
    cur = conn.cursor()
    cur.execute("TRUNCATE photo_faces RESTART IDENTITY")

    rows = []
    for _, row in df.iterrows():
        raw = json.dumps({k: str(v) if not pd.isna(v) else None for k, v in row.items()}, default=str)
        rows.append((None, None, None, None, None, raw))

    execute_values(cur,
        "INSERT INTO photo_faces (face_id, photo_id, person_name, confidence, bbox, raw_data) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  photo_faces: {len(rows)} rows imported")
    return len(rows)


def import_photo_people(conn):
    """Import people.parquet."""
    import pandas as pd

    filepath = SUPPLEMENTARY / "people.parquet"
    if not filepath.exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    df = pd.read_parquet(filepath)
    cur = conn.cursor()
    cur.execute("TRUNCATE photo_people RESTART IDENTITY")

    rows = []
    for _, row in df.iterrows():
        raw = json.dumps({k: str(v) if not pd.isna(v) else None for k, v in row.items()}, default=str)
        rows.append((None, None, None, raw))

    execute_values(cur,
        "INSERT INTO photo_people (person_id, name, photo_count, raw_data) VALUES %s",
        rows
    )
    conn.commit()
    print(f"  photo_people: {len(rows)} rows imported")
    return len(rows)


def import_csv_audit(conn, filepath, table_name):
    """Import a CSV audit file into a JSONB-based table."""
    if not Path(filepath).exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    cur = conn.cursor()
    cur.execute(f"TRUNCATE {table_name} RESTART IDENTITY")

    rows = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = json.dumps(dict(row))
            efta = None
            for k in row:
                if "efta" in k.lower() or "document" in k.lower():
                    efta = row[k]
                    break
            rows.append((efta, raw))

    if rows:
        execute_values(cur,
            f"INSERT INTO {table_name} (efta_number, raw_data) VALUES %s",
            rows
        )
    conn.commit()
    print(f"  {table_name}: {len(rows)} rows imported")
    return len(rows)


def import_csv_audit_entity(conn, filepath, table_name):
    """Import a CSV where first column is entity name (not EFTA)."""
    if not Path(filepath).exists():
        print(f"  SKIP: {filepath} not found")
        return 0

    cur = conn.cursor()
    cur.execute(f"TRUNCATE {table_name} RESTART IDENTITY")

    rows = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            raw = json.dumps(dict(row))
            entity = list(row.values())[0] if row else None
            rows.append((entity, raw))

    if rows:
        execute_values(cur,
            f"INSERT INTO {table_name} (entity_value, raw_data) VALUES %s",
            rows
        )
    conn.commit()
    print(f"  {table_name}: {len(rows)} rows imported")
    return len(rows)


def main():
    print("=" * 60)
    print("Importing local data files to PostgreSQL")
    print("=" * 60)

    conn = get_conn()

    print("\n[1/8] Creating tables...")
    create_tables(conn)

    total = 0

    print("\n[2/8] Importing person registry...")
    total += import_person_registry(conn)

    print("\n[3/8] Importing extracted entities...")
    total += import_extracted_entities(conn)

    print("\n[4/8] Importing phone numbers...")
    total += import_phone_numbers(conn)

    print("\n[5/8] Importing iMessage data...")
    total += import_imessage_conversations(conn)
    total += import_imessage_messages(conn)

    print("\n[6/8] Importing photo data...")
    total += import_photo_metadata(conn)
    total += import_photo_faces(conn)
    total += import_photo_people(conn)

    print("\n[7/8] Importing DOJ audit data...")
    total += import_csv_audit(conn, DOJ_AUDIT / "CONFIRMED_REMOVED.csv", "doj_audit_confirmed_removed")
    total += import_csv_audit(conn, DOJ_AUDIT / "FLAGGED_documents.csv", "doj_audit_flagged")
    total += import_csv_audit(conn, DOJ_AUDIT / "FLAGGED_documents_details.csv", "doj_audit_flagged_details")
    total += import_csv_audit(conn, DOJ_AUDIT / "SIZE_MISMATCHES.csv", "doj_audit_size_mismatches")
    total += import_csv_audit(conn, ALTERATION / "classified_alterations.csv", "doj_audit_alterations")
    total += import_csv_audit_entity(conn, ALTERATION / "removed_entities_export.csv", "doj_audit_removed_entities")
    total += import_csv_audit(conn, DOJ_AUDIT / "sample_verification_results.csv", "doj_audit_sample_verification")

    print("\n[8/8] Summary")
    print(f"  Total rows imported: {total:,}")
    print("  Done!")

    conn.close()


if __name__ == "__main__":
    main()
