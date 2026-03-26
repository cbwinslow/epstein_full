#!/usr/bin/env python3
"""Build knowledge graph connections from co-occurrence analysis.

Analyzes email, flight, and document data to build relationship connections
between entities. Uses co-occurrence patterns to identify relationships.

Usage:
    python scripts/build_connections.py [--source emails|flights|documents|all]
    python scripts/build_connections.py --verify  # Check current state
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor


# PostgreSQL connection
PG_DSN = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"


def get_email_cooccurrences(conn, min_cooccurrence=3):
    """Build connections from email co-occurrence."""
    print("\n=== Building Email Co-occurrence Connections ===")
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Get all participants per email
        cur.execute("""
            SELECT 
                je.id as email_id,
                je.sender,
                je.to_recipients,
                je.cc_recipients,
                je.all_participants
            FROM jmail_emails je
            WHERE je.sender IS NOT NULL 
              AND je.sender != ''
              AND je.to_recipients IS NOT NULL
              AND je.to_recipients != '[]'
            LIMIT 100000
        """)
        emails = cur.fetchall()
    
    print(f"Processing {len(emails):,} emails...")
    
    # Build co-occurrence matrix
    cooccurrence = defaultdict(lambda: defaultdict(int))
    
    for email in emails:
        participants = set()
        
        # Add sender
        if email['sender']:
            participants.add(email['sender'].lower().strip())
        
        # Add TO recipients
        if email['to_recipients']:
            try:
                to_list = json.loads(email['to_recipients'])
                for r in to_list:
                    if r:
                        participants.add(str(r).lower().strip())
            except:
                pass
        
        # Add CC recipients
        if email['cc_recipients']:
            try:
                cc_list = json.loads(email['cc_recipients'])
                for r in cc_list:
                    if r:
                        participants.add(str(r).lower().strip())
            except:
                pass
        
        # Count co-occurrences
        participants = list(participants)
        for i in range(len(participants)):
            for j in range(i + 1, len(participants)):
                p1, p2 = participants[i], participants[j]
                if p1 != p2:
                    cooccurrence[p1][p2] += 1
                    cooccurrence[p2][p1] += 1
    
    # Filter by minimum co-occurrence
    connections = []
    for p1, others in cooccurrence.items():
        for p2, count in others.items():
            if count >= min_cooccurrence and p1 < p2:  # Avoid duplicates
                connections.append({
                    'source': p1,
                    'target': p2,
                    'weight': count,
                    'type': 'communicated_with',
                    'source_type': 'email'
                })
    
    print(f"Found {len(connections):,} email connections (min {min_cooccurrence} co-occurrences)")
    return connections


def get_flight_cooccurrences(conn):
    """Build connections from flight co-occurrence."""
    print("\n=== Building Flight Co-occurrence Connections ===")
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT 
                ef.source_id as flight_id,
                ef.passenger_ids,
                ef.flight_date,
                ef.origin,
                ef.destination
            FROM exposed_flights ef
            WHERE ef.passenger_ids IS NOT NULL
        """)
        flights = cur.fetchall()
    
    print(f"Processing {len(flights):,} flights...")
    
    # Build co-occurrence matrix
    cooccurrence = defaultdict(lambda: defaultdict(int))
    flight_dates = defaultdict(list)
    
    for flight in flights:
        if not flight['passenger_ids']:
            continue
        
        try:
            passengers = json.loads(flight['passenger_ids'])
            if not isinstance(passengers, list):
                continue
        except:
            continue
        
        # Count co-occurrences
        for i in range(len(passengers)):
            for j in range(i + 1, len(passengers)):
                p1, p2 = str(passengers[i]), str(passengers[j])
                if p1 != p2:
                    cooccurrence[p1][p2] += 1
                    cooccurrence[p2][p1] += 1
                    
                    if flight['flight_date']:
                        flight_dates[(min(p1, p2), max(p1, p2))].append(flight['flight_date'])
    
    # Build connections
    connections = []
    for p1, others in cooccurrence.items():
        for p2, count in others.items():
            if count >= 1 and p1 < p2:  # Any shared flight
                dates = flight_dates.get((p1, p2), [])
                connections.append({
                    'source': p1,
                    'target': p2,
                    'weight': count,
                    'type': 'traveled_with',
                    'source_type': 'flight',
                    'dates': dates[:5]  # Sample dates
                })
    
    print(f"Found {len(connections):,} flight connections")
    return connections


def get_document_cooccurrences(conn, min_cooccurrence=2):
    """Build connections from document entity co-occurrence."""
    print("\n=== Building Document Co-occurrence Connections ===")
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Get entities per document (limited to PERSON type)
        cur.execute("""
            SELECT 
                de.document_id,
                de.entity_text,
                de.entity_type
            FROM document_entities de
            WHERE de.entity_type = 'PERSON'
              AND de.entity_text IS NOT NULL
              AND LENGTH(de.entity_text) > 3
            ORDER BY de.document_id
            LIMIT 500000
        """)
        entities = cur.fetchall()
    
    print(f"Processing {len(entities):,} document entities...")
    
    # Group by document
    doc_entities = defaultdict(set)
    for e in entities:
        doc_entities[e['document_id']].add(e['entity_text'].lower().strip())
    
    # Build co-occurrence matrix
    cooccurrence = defaultdict(lambda: defaultdict(int))
    
    for doc_id, entity_set in doc_entities.items():
        entity_list = list(entity_set)
        for i in range(len(entity_list)):
            for j in range(i + 1, len(entity_list)):
                e1, e2 = entity_list[i], entity_list[j]
                if e1 != e2:
                    cooccurrence[e1][e2] += 1
                    cooccurrence[e2][e1] += 1
    
    # Filter by minimum co-occurrence
    connections = []
    for e1, others in cooccurrence.items():
        for e2, count in others.items():
            if count >= min_cooccurrence and e1 < e2:
                connections.append({
                    'source': e1,
                    'target': e2,
                    'weight': count,
                    'type': 'co_mentioned',
                    'source_type': 'document'
                })
    
    print(f"Found {len(connections):,} document connections (min {min_cooccurrence} co-occurrences)")
    return connections


def save_connections(conn, connections, source_type):
    """Save connections to database."""
    print(f"\nSaving {len(connections):,} {source_type} connections...")
    
    # Create table if needed
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS cooccurrence_connections (
                id SERIAL PRIMARY KEY,
                source_entity TEXT NOT NULL,
                target_entity TEXT NOT NULL,
                connection_type VARCHAR(50) NOT NULL,
                source_type VARCHAR(50) NOT NULL,
                weight INTEGER DEFAULT 1,
                metadata JSONB DEFAULT '{}',
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(source_entity, target_entity, connection_type, source_type)
            )
        """)
        conn.commit()
    
    # Insert connections
    inserted = 0
    with conn.cursor() as cur:
        for c in connections:
            try:
                metadata = {}
                if 'dates' in c:
                    metadata['sample_dates'] = c['dates']
                
                cur.execute("""
                    INSERT INTO cooccurrence_connections 
                        (source_entity, target_entity, connection_type, source_type, weight, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (source_entity, target_entity, connection_type, source_type) 
                    DO UPDATE SET weight = EXCLUDED.weight, metadata = EXCLUDED.metadata
                """, (
                    c['source'], c['target'], c['type'], c['source_type'],
                    c['weight'], json.dumps(metadata)
                ))
                inserted += 1
            except Exception as e:
                pass
    
    conn.commit()
    print(f"Saved {inserted:,} connections")
    return inserted


def verify_connections(conn):
    """Verify connection statistics."""
    print("\n=== Connection Statistics ===")
    
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        # Total connections
        cur.execute("SELECT COUNT(*) as cnt FROM cooccurrence_connections")
        total = cur.fetchone()['cnt']
        print(f"Total connections: {total:,}")
        
        # By source type
        cur.execute("""
            SELECT source_type, COUNT(*) as cnt
            FROM cooccurrence_connections
            GROUP BY source_type
            ORDER BY cnt DESC
        """)
        print("\nBy source type:")
        for row in cur.fetchall():
            print(f"  {row['source_type']}: {row['cnt']:,}")
        
        # By connection type
        cur.execute("""
            SELECT connection_type, COUNT(*) as cnt
            FROM cooccurrence_connections
            GROUP BY connection_type
            ORDER BY cnt DESC
        """)
        print("\nBy connection type:")
        for row in cur.fetchall():
            print(f"  {row['connection_type']}: {row['cnt']:,}")
        
        # Top connected entities
        cur.execute("""
            SELECT 
                source_entity,
                COUNT(DISTINCT target_entity) as connections,
                SUM(weight) as total_weight
            FROM cooccurrence_connections
            GROUP BY source_entity
            ORDER BY connections DESC
            LIMIT 10
        """)
        print("\nTop 10 connected entities:")
        for row in cur.fetchall():
            print(f"  {row['source_entity'][:40]}: {row['connections']} connections, weight={row['total_weight']}")


def main():
    parser = argparse.ArgumentParser(description="Build knowledge graph connections")
    parser.add_argument("--source", choices=['emails', 'flights', 'documents', 'all'], 
                       default='all', help="Data source to analyze")
    parser.add_argument("--min-cooccurrence", type=int, default=3, 
                       help="Minimum co-occurrence count for connections")
    parser.add_argument("--verify", action="store_true", help="Just verify current state")
    parser.add_argument("--limit", type=int, help="Limit number of records to process")
    args = parser.parse_args()
    
    conn = psycopg2.connect(PG_DSN)
    try:
        if args.verify:
            verify_connections(conn)
            return
        
        all_connections = []
        
        if args.source in ['emails', 'all']:
            email_conn = get_email_cooccurrences(conn, min_cooccurrence=args.min_cooccurrence)
            all_connections.extend(email_conn)
            save_connections(conn, email_conn, 'email')
        
        if args.source in ['flights', 'all']:
            flight_conn = get_flight_cooccurrences(conn)
            all_connections.extend(flight_conn)
            save_connections(conn, flight_conn, 'flight')
        
        if args.source in ['documents', 'all']:
            doc_conn = get_document_cooccurrences(conn, min_cooccurrence=args.min_cooccurrence)
            all_connections.extend(doc_conn)
            save_connections(conn, doc_conn, 'document')
        
        print(f"\n=== Summary ===")
        print(f"Total connections built: {len(all_connections):,}")
        
        # Verify
        verify_connections(conn)
        
    finally:
        conn.close()


if __name__ == "__main__":
    main()
