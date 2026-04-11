#!/usr/bin/env python3
"""
Import Flight Logs from dleerdefi/epstein-network-data

Sources:
- /home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/flight_logs/name_references/epstein_names_master_list.json
- /home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/flight_logs/twitter_user @LividsRevenge/epstein_flight_logs_thread.json
"""

import asyncio
import asyncpg
import json
import re
from pathlib import Path
from datetime import datetime

NAMES_FILE = Path("/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/flight_logs/name_references/epstein_names_master_list.json")
FLIGHTS_FILE = Path("/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/flight_logs/twitter_user @LividsRevenge/epstein_flight_logs_thread.json")
BATCH_SIZE = 100
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

async def create_tables(conn):
    """Create tables for Flight Logs data."""
    print("Creating tables...")
    
    await conn.execute("DROP TABLE IF EXISTS flight_log_passengers CASCADE")
    await conn.execute("DROP TABLE IF EXISTS flight_log_entries CASCADE")
    await conn.execute("DROP TABLE IF EXISTS flight_log_names CASCADE")
    
    # Names reference table (from master list)
    await conn.execute("""
        CREATE TABLE flight_log_names (
            id SERIAL PRIMARY KEY,
            full_name TEXT,
            category TEXT,
            variations TEXT[],
            notable BOOLEAN,
            description TEXT,
            source TEXT
        )
    """)
    
    # Flight entries table (parsed from tweets)
    await conn.execute("""
        CREATE TABLE flight_log_entries (
            id SERIAL PRIMARY KEY,
            flight_date DATE,
            origin TEXT,
            destination TEXT,
            route TEXT,
            passengers TEXT[],
            notes TEXT,
            source_tweet_id TEXT,
            source_username TEXT,
            created_at TIMESTAMPTZ
        )
    """)
    
    print("✅ Tables created")

async def import_names(conn):
    """Import names from master list."""
    print(f"Importing names from {NAMES_FILE}...")
    
    with open(NAMES_FILE, 'r') as f:
        data = json.load(f)
    
    metadata = data.get('metadata', {})
    names = data.get('names', [])
    
    print(f"Metadata: {metadata.get('total_names')} names, categories: {metadata.get('categories')}")
    
    batch = []
    for name in names:
        batch.append((
            name.get('full_name'),
            name.get('category'),
            name.get('variations', []),
            name.get('notable', False),
            name.get('description'),
            'name_references/epstein_names_master_list.json'
        ))
        
        if len(batch) >= BATCH_SIZE:
            await conn.copy_records_to_table(
                'flight_log_names',
                records=batch,
                columns=['full_name', 'category', 'variations', 'notable', 'description', 'source']
            )
            batch = []
    
    if batch:
        await conn.copy_records_to_table(
            'flight_log_names',
            records=batch,
            columns=['full_name', 'category', 'variations', 'notable', 'description', 'source']
        )
    
    print(f"✅ Imported {len(names)} names")
    return len(names)

def parse_flight_text(text):
    """Parse flight information from tweet text."""
    flights = []
    
    # Pattern: MM/DD/YYYY - Origin to Destination - Passenger1, Passenger2
    # Example: "4/25/1991 - Palm Springs, FL to Columbus, OH - Nestle, Mr. Martino"
    pattern = r'(\d{1,2}/\d{1,2}/\d{4})\s*-\s*([^-]+?)\s+to\s+([^-]+)\s*-\s*(.+?)(?=\n|\d{1,2}/\d{1,2}/\d{4}|$)'
    
    for match in re.finditer(pattern, text, re.DOTALL):
        date_str = match.group(1)
        origin = match.group(2).strip()
        destination = match.group(3).strip()
        passengers_str = match.group(4).strip()
        
        # Parse passengers (comma-separated)
        passengers = [p.strip() for p in passengers_str.split(',') if p.strip()]
        
        # Parse date
        try:
            flight_date = datetime.strptime(date_str, '%m/%d/%Y').date()
        except:
            flight_date = None
        
        flights.append({
            'date': flight_date,
            'origin': origin,
            'destination': destination,
            'route': f"{origin} to {destination}",
            'passengers': passengers
        })
    
    return flights

async def import_flights(conn):
    """Import flight entries from Twitter thread."""
    print(f"Importing flights from {FLIGHTS_FILE}...")
    
    with open(FLIGHTS_FILE, 'r') as f:
        data = json.load(f)
    
    username = data.get('username', 'Unknown')
    tweets = data.get('all_tweets', [])
    
    print(f"Processing {len(tweets)} tweets from @{username}...")
    
    all_flights = []
    for tweet in tweets:
        tweet_id = tweet.get('id')
        text = tweet.get('text', '')
        created_at = tweet.get('createdAt')
        
        # Parse flights from tweet text
        flights = parse_flight_text(text)
        
        for flight in flights:
            all_flights.append({
                'date': flight['date'],
                'origin': flight['origin'],
                'destination': flight['destination'],
                'route': flight['route'],
                'passengers': flight['passengers'],
                'notes': text[:500] if len(text) > 500 else text,  # First part of tweet
                'tweet_id': str(tweet_id) if tweet_id else None,
                'username': username,
                'created_at': created_at
            })
    
    # Insert flights
    batch = []
    for flight in all_flights:
        batch.append((
            flight['date'],
            flight['origin'],
            flight['destination'],
            flight['route'],
            flight['passengers'],
            flight['notes'],
            flight['tweet_id'],
            flight['username'],
            flight['created_at']
        ))
        
        if len(batch) >= BATCH_SIZE:
            await conn.copy_records_to_table(
                'flight_log_entries',
                records=batch,
                columns=['flight_date', 'origin', 'destination', 'route', 'passengers', 
                        'notes', 'source_tweet_id', 'source_username', 'created_at']
            )
            batch = []
    
    if batch:
        await conn.copy_records_to_table(
            'flight_log_entries',
            records=batch,
            columns=['flight_date', 'origin', 'destination', 'route', 'passengers',
                    'notes', 'source_tweet_id', 'source_username', 'created_at']
        )
    
    print(f"✅ Imported {len(all_flights)} flight entries")
    return len(all_flights)

async def verify(conn):
    """Verify import."""
    print("\nVerification:")
    
    names = await conn.fetchval("SELECT COUNT(*) FROM flight_log_names")
    flights = await conn.fetchval("SELECT COUNT(*) FROM flight_log_entries")
    
    print(f"Names: {names}")
    print(f"Flight entries: {flights}")
    
    # Sample names by category
    categories = await conn.fetch("""
        SELECT category, COUNT(*) as count 
        FROM flight_log_names 
        GROUP BY category 
        ORDER BY count DESC
    """)
    
    print("\nNames by category:")
    for cat in categories:
        print(f"   - {cat['category']}: {cat['count']}")
    
    # Sample flights
    samples = await conn.fetch("""
        SELECT flight_date, route, passengers
        FROM flight_log_entries
        WHERE flight_date IS NOT NULL
        ORDER BY flight_date
        LIMIT 5
    """)
    
    print("\nSample flights:")
    for s in samples:
        pax = ', '.join(s['passengers'][:3]) if s['passengers'] else 'Unknown'
        print(f"   - {s['flight_date']}: {s['route']} - {pax}")

async def main():
    print("="*70)
    print("FLIGHT LOGS IMPORT")
    print("="*70)
    print(f"Started: {datetime.now()}")
    print("="*70)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        await create_tables(conn)
        names_count = await import_names(conn)
        flights_count = await import_flights(conn)
        await verify(conn)
        print("\n" + "="*70)
        print(f"✅ COMPLETE - {names_count} names, {flights_count} flights imported")
        print("="*70)
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
