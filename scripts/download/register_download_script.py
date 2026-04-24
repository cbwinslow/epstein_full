#!/usr/bin/env python3
"""
Register or update a download script in the database.
This utility tracks the script version and content for reproducibility.
"""

import hashlib
import sys
from pathlib import Path

import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd",
}


def get_script_hash(script_path):
    """Calculate SHA-256 hash of script content"""
    with open(script_path, "r") as f:
        content = f.read()
    return hashlib.sha256(content.encode()).hexdigest()


def register_script(script_path, description=None, version=None):
    """
    Register or update a download script in the database.

    Args:
        script_path: Path to the Python script
        description: Optional description of the script
        version: Optional version string

    Returns:
        script_id: The ID of the registered/updated script
    """
    script_path = Path(script_path)
    script_name = script_path.name

    # Read script content
    with open(script_path, "r") as f:
        script_content = f.read()

    # Calculate hash
    script_hash = get_script_hash(script_path)

    # Connect to database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        # Check if script already exists
        cur.execute(
            "SELECT id, script_hash FROM download_scripts WHERE script_name = %s", (script_name,)
        )
        result = cur.fetchone()

        if result:
            existing_id, existing_hash = result
            # Check if content changed
            if existing_hash != script_hash:
                # Update script
                cur.execute(
                    """
                    UPDATE download_scripts
                    SET script_content = %s, script_hash = %s,
                        script_path = %s, description = %s, version = %s, updated_at = NOW()
                    WHERE id = %s
                """,
                    (
                        script_content,
                        script_hash,
                        str(script_path),
                        description,
                        version,
                        existing_id,
                    ),
                )
                print(f"✅ Updated script: {script_name} (content changed)")
            else:
                print(f"✅ Script already registered (no changes): {script_name}")
            return existing_id
        else:
            # Insert new script
            cur.execute(
                """
                INSERT INTO download_scripts
                (script_name, script_path, script_content, script_hash, description, version)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
            """,
                (script_name, str(script_path), script_content, script_hash, description, version),
            )
            script_id = cur.fetchone()[0]
            print(f"✅ Registered new script: {script_name}")
            return script_id

        conn.commit()

    finally:
        cur.close()
        conn.close()


def link_script_to_download(script_id, source_name):
    """
    Link a script to a download in data_pipeline_tracking.

    Args:
        script_id: The ID of the script
        source_name: The source_name in data_pipeline_tracking
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    try:
        cur.execute(
            """
            UPDATE data_pipeline_tracking
            SET download_script_id = %s
            WHERE source_name = %s AND download_script_id IS NULL
        """,
            (script_id, source_name),
        )

        updated = cur.rowcount
        conn.commit()

        if updated > 0:
            print(f"✅ Linked script to {updated} download(s) for {source_name}")
        else:
            print(f"ℹ️  No downloads found for {source_name} or already linked")

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python register_download_script.py <script_path> [description] [version]")
        print(
            "Example: python register_download_script.py download_congress_historical.py 'Downloads Congress.gov historical data' '1.0.0'"
        )
        sys.exit(1)

    script_path = sys.argv[1]
    description = sys.argv[2] if len(sys.argv) > 2 else None
    version = sys.argv[3] if len(sys.argv) > 3 else None

    script_id = register_script(script_path, description, version)
    print(f"Script ID: {script_id}")
