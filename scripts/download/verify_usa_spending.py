#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM usa_spending_awards")
    count = cur.fetchone()[0]
    print(f"USA Spending: {count} records")
conn.close()
