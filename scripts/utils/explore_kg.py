#!/usr/bin/env python3
"""Interactive knowledge graph exploration tool."""

import json
import sqlite3
import sys

DB_PATH = "/home/cbwinslow/workspace/epstein-data/databases/knowledge_graph.db"

def connect():
    return sqlite3.connect(DB_PATH)

def search_entities(query, conn):
    cursor = conn.execute(
        "SELECT id, name, entity_type, metadata FROM entities WHERE name LIKE ? ORDER BY name",
        (f"%{query}%",)
    )
    return cursor.fetchall()

def get_relationships(entity_id, conn):
    cursor = conn.execute("""
        SELECT r.relationship_type, r.weight, 
               e1.name as source, e2.name as target,
               r.metadata
        FROM relationships r
        JOIN entities e1 ON r.source_entity_id = e1.id
        JOIN entities e2 ON r.target_entity_id = e2.id
        WHERE r.source_entity_id = ? OR r.target_entity_id = ?
        ORDER BY r.weight DESC
    """, (entity_id, entity_id))
    return cursor.fetchall()

def main():
    conn = connect()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"\nSearching for: {query}")
        print("=" * 50)

        entities = search_entities(query, conn)
        if not entities:
            print("No entities found.")
            return

        for entity in entities:
            print(f"\n{entity[1]} ({entity[2]})")
            print(f"  ID: {entity[0]}")
            if entity[3]:
                meta = json.loads(entity[3])
                for k, v in meta.items():
                    if isinstance(v, str) and len(v) > 100:
                        v = v[:100] + "..."
                    print(f"  {k}: {v}")

            rels = get_relationships(entity[0], conn)
            if rels:
                print(f"  Relationships ({len(rels)}):")
                for rel in rels[:10]:
                    print(f"    {rel[2]} --[{rel[0]}]--> {rel[3]} (weight: {rel[1]})")
    else:
        print("Usage: python explore_kg.py <entity_name>")
        print("\nQuick stats:")
        cursor = conn.execute("SELECT COUNT(*) FROM entities")
        print(f"  Total entities: {cursor.fetchone()[0]}")
        cursor = conn.execute("SELECT COUNT(*) FROM relationships")
        print(f"  Total relationships: {cursor.fetchone()[0]}")
        cursor = conn.execute("""
            SELECT entity_type, COUNT(*) FROM entities 
            GROUP BY entity_type ORDER BY COUNT(*) DESC
        """)
        print("\n  Entity types:")
        for row in cursor.fetchall():
            print(f"    {row[0]}: {row[1]}")

    conn.close()

if __name__ == "__main__":
    main()
