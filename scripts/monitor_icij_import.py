#!/usr/bin/env python3
"""Monitor ICIJ Import Progress"""
import asyncpg
import asyncio
import time
from datetime import datetime

DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

async def monitor():
    conn = await asyncpg.connect(DB_URL)
    
    print("="*70)
    print("ICIJ IMPORT MONITOR")
    print("="*70)
    
    while True:
        # Get status
        rows = await conn.fetch("""
            SELECT filename, status, worker_id, rows_imported, 
                   started_at, completed_at, error_message
            FROM icij_import_progress
            ORDER BY 
                CASE status 
                    WHEN 'running' THEN 0 
                    WHEN 'pending' THEN 1 
                    WHEN 'complete' THEN 2 
                    ELSE 3 
                END,
                started_at
        """)
        
        # Clear screen (optional)
        print("\033[2J\033[H" if hasattr(__builtins__, 'print') else "")
        
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] ICIJ Import Status:")
        print("-"*70)
        
        running = 0
        complete = 0
        pending = 0
        total_rows = 0
        
        for row in rows:
            status_icon = {
                'running': '🔄',
                'pending': '⏳',
                'complete': '✅',
                'failed': '❌'
            }.get(row['status'], '❓')
            
            rows_str = f"{row['rows_imported']:,}" if row['rows_imported'] else ""
            worker = f"({row['worker_id']})" if row['worker_id'] else ""
            
            print(f"{status_icon} {row['filename']:<25} {row['status']:<10} {rows_str:>12} {worker}")
            
            if row['status'] == 'running':
                running += 1
            elif row['status'] == 'complete':
                complete += 1
            elif row['status'] == 'pending':
                pending += 1
            
            total_rows += row['rows_imported'] or 0
        
        print("-"*70)
        print(f"Running: {running} | Complete: {complete} | Pending: {pending}")
        print(f"Total rows imported: {total_rows:,}")
        
        # Check if all complete
        if pending == 0 and running == 0 and complete > 0:
            print("\n✅ ALL IMPORTS COMPLETE!")
            break
        
        await asyncio.sleep(5)
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(monitor())
