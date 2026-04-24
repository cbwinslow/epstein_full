#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM usa_spending_awards")
    count = cur.fetchone()[0]
    print(f"USA Spending: {count} records")

    cur.execute(
        """
        INSERT INTO data_inventory (source_name, source_type, target_table, actual_records, status, imported_at, last_updated)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (source_name) DO UPDATE SET
            actual_records = EXCLUDED.actual_records,
            status = EXCLUDED.status,
            last_updated = NOW()
    """,
        (
            "USA Spending Federal Awards",
            "government",
            "usa_spending_awards",
            count,
            "complete" if count > 0 else "failed",
        ),
    )
    conn.commit()
    print("Inventory updated")
conn.close()
