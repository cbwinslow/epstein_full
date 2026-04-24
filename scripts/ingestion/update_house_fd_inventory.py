#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    cur.execute('SELECT COUNT(*) FROM house_financial_disclosures')
    house_count = cur.fetchone()[0]
    print(f'House FD count: {house_count}')
    
    # Update inventory
    cur.execute("""
        INSERT INTO data_inventory (source_name, source_type, target_table, actual_records, status, imported_at, last_updated)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (source_name) DO UPDATE SET
            actual_records = EXCLUDED.actual_records,
            status = EXCLUDED.status,
            last_updated = NOW()
    """, ("House Financial Disclosures", "government", "house_financial_disclosures", house_count, "complete"))
    
    conn.commit()
    print('Inventory updated')
conn.close()
