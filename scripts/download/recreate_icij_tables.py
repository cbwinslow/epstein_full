#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect("postgresql://cbwinslow:123qweasd@localhost:5432/epstein")
cur = conn.cursor()

# Drop existing ICIJ tables
tables = [
    "icij_entities",
    "icij_officers",
    "icij_addresses",
    "icij_intermediaries",
    "icij_others",
    "icij_relationships",
]

for table in tables:
    try:
        cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE")
        print(f"Dropped {table}")
    except Exception as e:
        print(f"Error dropping {table}: {e}")

conn.commit()
conn.close()
print("All ICIJ tables dropped")
