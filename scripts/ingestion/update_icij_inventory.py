#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    # Get counts
    cur.execute('SELECT COUNT(*) FROM icij_entities')
    entities = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM icij_officers')
    officers = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM icij_addresses')
    addresses = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM icij_intermediaries')
    intermediaries = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM icij_others')
    others = cur.fetchone()[0]
    
    cur.execute('SELECT COUNT(*) FROM icij_relationships')
    relationships = cur.fetchone()[0]
    
    total = entities + officers + addresses + intermediaries + others + relationships
    
    print(f'ICIJ Import Summary:')
    print(f'  Entities: {entities:,}')
    print(f'  Officers: {officers:,}')
    print(f'  Addresses: {addresses:,}')
    print(f'  Intermediaries: {intermediaries:,}')
    print(f'  Others: {others:,}')
    print(f'  Relationships: {relationships:,}')
    print(f'  Total: {total:,}')
    
    # Update inventory
    cur.execute("""
        INSERT INTO data_inventory (source_name, source_type, target_table, actual_records, status, imported_at, last_updated)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        ON CONFLICT (source_name) DO UPDATE SET
            actual_records = EXCLUDED.actual_records,
            status = EXCLUDED.status,
            last_updated = NOW()
    """, ('ICIJ Offshore Leaks', 'financial', 'icij_entities', total, 'complete'))
    conn.commit()
    print(f'Inventory updated')
conn.close()
