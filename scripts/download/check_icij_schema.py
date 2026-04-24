#!/usr/bin/env python3
import psycopg2

conn = psycopg2.connect("postgresql://cbwinslow:123qweasd@localhost:5432/epstein")
cur = conn.cursor()

# Check if icij_officers table exists and its schema
cur.execute("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = 'icij_officers'
    ORDER BY ordinal_position
""")

print("icij_officers schema:")
for row in cur.fetchall():
    print(f"  {row[0]}: {row[1]}")

conn.close()
