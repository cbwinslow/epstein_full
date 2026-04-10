#!/usr/bin/env python3
"""Direct database fix and collection start"""

import psycopg2
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

from media_acquisition.config import DATABASE_URL

print("Checking database...")

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# Check if media_news_articles exists
cur.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE table_schema = 'public' 
        AND table_name = 'media_news_articles'
    )
""")
exists = cur.fetchone()[0]

if exists:
    print("Table exists, checking columns...")
    cur.execute("""
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_schema = 'public' AND table_name = 'media_news_articles'
        ORDER BY ordinal_position
    """)
    cols = [c[0] for c in cur.fetchall()]
    print(f"Columns: {cols[:10]}... ({len(cols)} total)")
    
    if 'url' not in cols:
        print("ERROR: 'url' column missing! Adding it...")
        cur.execute("ALTER TABLE media_news_articles ADD COLUMN url TEXT UNIQUE;")
        conn.commit()
        print("Added url column")
else:
    print("Table doesn't exist! Creating it...")
    cur.execute("""
        CREATE TABLE media_news_articles (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL UNIQUE,
            title TEXT,
            content TEXT,
            authors TEXT[],
            publication_date TIMESTAMP,
            source_domain TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    conn.commit()
    print("Created table")

conn.close()
print("Database ready!")
