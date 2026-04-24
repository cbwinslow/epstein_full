#!/usr/bin/env python3
import config

conn = config.get_db_connection()
with conn.cursor() as cur:
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_name LIKE '%inventory%'
    """)
    tables = cur.fetchall()
    if tables:
        for row in tables:
            print(f'Table: {row[0]}')
            # Get schema
            cur.execute(f"""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = '{row[0]}'
                ORDER BY ordinal_position
            """)
            for col_row in cur.fetchall():
                print(f'  {col_row[0]}: {col_row[1]}')
    else:
        print('No inventory tables found')
conn.close()
