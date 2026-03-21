#!/usr/bin/env python3
"""
Epstein Project — Unified Database Search

Search across all data: FTS, entities, emails, transcripts, redactions.

Usage:
  python db_search.py "Epstein flight logs"           # FTS search
  python db_search.py --entity "Maxwell"               # Entity lookup
  python db_search.py --email "clinton"                # Email search
  python db_search.py --transcript "Epstein"           # Transcript search
  python db_search.py --redaction "EFTA00100000"        # Redaction lookup
  python db_search.py --all "Prince Andrew"             # Search everywhere
"""

import sys
import argparse
import psycopg2

# =============================================================================
# Configuration
# =============================================================================

PG_HOST = "localhost"
PG_PORT = 5432
PG_USER = "cbwinslow"
PG_PASS = "123qweasd"
PG_DB = "epstein"


def get_conn():
    return psycopg2.connect(
        host=PG_HOST, port=PG_PORT,
        user=PG_USER, password=PG_PASS,
        dbname=PG_DB
    )


def search_fts(conn, query, limit=10):
    """Full-text search across pages."""
    cur = conn.cursor()
    cur.execute("""
        SELECT efta_number, page_number,
               ts_rank_cd(search_vector, q) AS rank,
               left(ts_headline('english', coalesce(text_content, ''), q), 200) AS snippet
        FROM pages, plainto_tsquery('english', %s) q
        WHERE search_vector @@ q
        ORDER BY rank DESC
        LIMIT %s
    """, (query, limit))

    print(f"\n=== FTS Search: '{query}' ===")
    for efta, page, rank, snippet in cur.fetchall():
        print(f"  {efta} p{page} (rank: {rank:.4f})")
        print(f"    {snippet[:150]}...")
        print()


def search_entities(conn, name, limit=10):
    """Search entities by name (fuzzy)."""
    cur = conn.cursor()

    # Exact match first
    cur.execute("""
        SELECT id, name, entity_type, mention_count, metadata::text
        FROM entities WHERE name ILIKE %s
        ORDER BY mention_count DESC LIMIT %s
    """, (f"%{name}%", limit))

    results = cur.fetchall()
    if not results:
        # Fuzzy match
        cur.execute("""
            SELECT id, name, entity_type, mention_count,
                   similarity(name, %s) AS sim
            FROM entities
            WHERE similarity(name, %s) > 0.3
            ORDER BY sim DESC LIMIT %s
        """, (name, name, limit))
        results = cur.fetchall()

    print(f"\n=== Entity Search: '{name}' ===")
    for row in results:
        eid, name, etype, mentions = row[0], row[1], row[2], row[3]
        print(f"  {name} ({etype}) — {mentions} mentions")

        # Get relationships
        cur.execute("""
            SELECT e2.name, r.relationship_type, r.weight
            FROM relationships r
            JOIN entities e2 ON r.target_entity_id = e2.id
            WHERE r.source_entity_id = %s
            ORDER BY r.weight DESC LIMIT 5
        """, (eid,))
        for rel_name, rel_type, weight in cur.fetchall():
            print(f"    → {rel_type}: {rel_name} (weight: {weight})")
        print()


def search_emails(conn, query, limit=10):
    """Search emails by subject/from/content."""
    cur = conn.cursor()
    cur.execute("""
        SELECT efta_number, from_name, subject, date_sent,
               ts_rank_cd(to_tsvector('english', coalesce(subject, '')),
                          plainto_tsquery('english', %s)) AS rank
        FROM emails
        WHERE to_tsvector('english', coalesce(subject, '') || ' ' || coalesce(from_name, ''))
              @@ plainto_tsquery('english', %s)
           OR from_name ILIKE %s
           OR subject ILIKE %s
        ORDER BY rank DESC
        LIMIT %s
    """, (query, query, f"%{query}%", f"%{query}%", limit))

    print(f"\n=== Email Search: '{query}' ===")
    for efta, from_name, subject, date, rank in cur.fetchall():
        print(f"  {efta} | {from_name} | {date}")
        print(f"    {subject[:100]}")
        print()


def search_transcripts(conn, query, limit=10):
    """Search transcripts."""
    cur = conn.cursor()
    cur.execute("""
        SELECT efta_number, duration_secs, word_count,
               ts_rank_cd(to_tsvector('english', coalesce(transcript, '')),
                          plainto_tsquery('english', %s)) AS rank,
               left(transcript, 150) AS preview
        FROM transcripts
        WHERE to_tsvector('english', coalesce(transcript, ''))
              @@ plainto_tsquery('english', %s)
        ORDER BY rank DESC
        LIMIT %s
    """, (query, query, limit))

    print(f"\n=== Transcript Search: '{query}' ===")
    for efta, duration, words, rank, preview in cur.fetchall():
        print(f"  {efta} | {duration:.0f}s | {words} words")
        print(f"    {preview}...")
        print()


def search_redactions(conn, efta, limit=20):
    """Look up redactions for a specific EFTA."""
    cur = conn.cursor()
    cur.execute("""
        SELECT page_number, redaction_type, confidence, left(ocr_text, 100)
        FROM redactions
        WHERE efta_number = %s
        ORDER BY page_number
        LIMIT %s
    """, (efta, limit))

    print(f"\n=== Redactions for {efta} ===")
    for page, rtype, conf, text in cur.fetchall():
        print(f"  p{page}: {rtype} (conf: {conf:.2f}) {text[:80] if text else ''}")


def search_all(conn, query, limit=5):
    """Search across all data sources."""
    search_fts(conn, query, limit)
    search_entities(conn, query, limit)
    search_emails(conn, query, limit)
    search_transcripts(conn, query, limit)


def main():
    parser = argparse.ArgumentParser(description="Unified database search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--entity", type=str, help="Search entities")
    parser.add_argument("--email", type=str, help="Search emails")
    parser.add_argument("--transcript", type=str, help="Search transcripts")
    parser.add_argument("--redaction", type=str, help="Look up redactions for EFTA")
    parser.add_argument("--all", type=str, help="Search everywhere")
    parser.add_argument("--limit", type=int, default=10, help="Max results per source")
    args = parser.parse_args()

    conn = get_conn()

    if args.entity:
        search_entities(conn, args.entity, args.limit)
    elif args.email:
        search_emails(conn, args.email, args.limit)
    elif args.transcript:
        search_transcripts(conn, args.transcript, args.limit)
    elif args.redaction:
        search_redactions(conn, args.redaction, args.limit)
    elif args.all:
        search_all(conn, args.all, args.limit)
    elif args.query:
        search_fts(conn, args.query, args.limit)
    else:
        print("Usage: python db_search.py 'search query'")
        print("       python db_search.py --entity 'Maxwell'")
        print("       python db_search.py --all 'Prince Andrew'")

    conn.close()


if __name__ == "__main__":
    main()
