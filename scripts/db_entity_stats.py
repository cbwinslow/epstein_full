#!/usr/bin/env python3
"""
Epstein Project — Knowledge Graph Statistics

Shows entity types, relationship types, top connected entities,
and community structure analysis.

Usage:
  python db_entity_stats.py              # Full stats
  python db_entity_stats.py --top 20     # Top 20 entities
  python db_entity_stats.py --entity "Epstein"  # Specific entity details
"""

import sys
import argparse
import json
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


def show_overview(conn):
    """Show KG overview."""
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM entities")
    entities = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM relationships")
    relationships = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM edge_sources")
    edge_sources = cur.fetchone()[0]

    print(f"\n{'=' * 60}")
    print(f"  Knowledge Graph Overview")
    print(f"{'=' * 60}")
    print(f"  Entities:     {entities:,}")
    print(f"  Relationships:{relationships:,}")
    print(f"  Edge Sources: {edge_sources:,}")


def show_entity_types(conn):
    """Show entity type distribution."""
    cur = conn.cursor()
    cur.execute("""
        SELECT entity_type, COUNT(*) AS count
        FROM entities
        GROUP BY entity_type
        ORDER BY count DESC
    """)

    print(f"\n  Entity Types:")
    for etype, count in cur.fetchall():
        print(f"    {etype}: {count}")


def show_relationship_types(conn):
    """Show relationship type distribution."""
    cur = conn.cursor()
    cur.execute("""
        SELECT relationship_type, COUNT(*) AS count, SUM(weight::numeric) AS total_weight
        FROM relationships
        GROUP BY relationship_type
        ORDER BY count DESC
    """)

    print(f"\n  Relationship Types:")
    for rtype, count, weight in cur.fetchall():
        print(f"    {rtype}: {count} edges, total weight: {weight:.0f}")


def show_top_entities(conn, limit=10):
    """Show top connected entities."""
    cur = conn.cursor()
    cur.execute("""
        SELECT e.name, e.entity_type,
               COUNT(DISTINCT r.id) AS connections,
               SUM(r.weight::numeric) AS total_weight
        FROM entities e
        LEFT JOIN relationships r ON e.id = r.source_entity_id OR e.id = r.target_entity_id
        GROUP BY e.id, e.name, e.entity_type
        ORDER BY connections DESC
        LIMIT %s
    """, (limit,))

    print(f"\n  Top {limit} Entities by Connections:")
    for name, etype, conns, weight in cur.fetchall():
        print(f"    {name} ({etype}): {conns} connections, weight: {weight:.0f}")


def show_entity_details(conn, name):
    """Show detailed info for a specific entity."""
    cur = conn.cursor()

    # Find entity
    cur.execute("""
        SELECT id, name, entity_type, aliases::text, metadata::text, mention_count
        FROM entities
        WHERE name ILIKE %s
        ORDER BY mention_count DESC
        LIMIT 1
    """, (f"%{name}%",))

    row = cur.fetchone()
    if not row:
        print(f"Entity '{name}' not found.")
        return

    eid, name, etype, aliases, metadata, mentions = row
    print(f"\n  Entity: {name}")
    print(f"  Type: {etype}")
    print(f"  Mentions: {mentions}")
    print(f"  Aliases: {aliases}")
    print(f"  Metadata: {metadata[:200] if metadata else 'N/A'}")

    # Relationships
    cur.execute("""
        SELECT e2.name, r.relationship_type, r.weight, r.date_first, r.date_last
        FROM relationships r
        JOIN entities e2 ON r.target_entity_id = e2.id
        WHERE r.source_entity_id = %s
        ORDER BY r.weight DESC
    """, (eid,))

    rels = cur.fetchall()
    if rels:
        print(f"\n  Relationships ({len(rels)}):")
        for rel_name, rtype, weight, d1, d2 in rels:
            dates = f" ({d1} → {d2})" if d1 else ""
            print(f"    → {rtype}: {rel_name} (weight: {weight}){dates}")

    # Reverse relationships
    cur.execute("""
        SELECT e1.name, r.relationship_type, r.weight
        FROM relationships r
        JOIN entities e1 ON r.source_entity_id = e1.id
        WHERE r.target_entity_id = %s
        ORDER BY r.weight DESC
    """, (eid,))

    rev_rels = cur.fetchall()
    if rev_rels:
        print(f"\n  Connected from ({len(rev_rels)}):")
        for rel_name, rtype, weight in rev_rels:
            print(f"    ← {rtype}: {rel_name} (weight: {weight})")


def main():
    parser = argparse.ArgumentParser(description="Knowledge graph statistics")
    parser.add_argument("--top", type=int, default=10, help="Top N entities")
    parser.add_argument("--entity", type=str, help="Specific entity details")
    args = parser.parse_args()

    conn = get_conn()

    if args.entity:
        show_entity_details(conn, args.entity)
    else:
        show_overview(conn)
        show_entity_types(conn)
        show_relationship_types(conn)
        show_top_entities(conn, args.top)

    conn.close()
    print()


if __name__ == "__main__":
    main()
