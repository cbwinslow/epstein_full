#!/usr/bin/env python3
"""
Import Neo4j Knowledge Graph from epstein-network-data
Source: dleerdefi/epstein-network-data/data/final/epstein_notes/

Imports:
- Nodes: persons, organizations, locations, equipment, claims, citations, events, legal_cases
- Relationships: 65+ typed relationship CSVs

Tables created:
- neo4j_nodes (unified node storage with type discrimination)
- neo4j_relationships (typed edges with metadata)
"""

import os
import sys
import csv
import json
import asyncio
import asyncpg
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Base path to epstein-network-data repo
BASE_DIR = Path("/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/final/epstein_notes")

# PostgreSQL connection
DB_URL = os.environ.get("EPSTEIN_DB_URL", "postgresql://cbwinslow:123qweasd@localhost:5432/epstein")


async def create_tables(conn: asyncpg.Connection):
    """Create Neo4j graph tables."""
    print("Creating Neo4j graph tables...")
    
    # Drop existing tables if they exist (for clean import)
    await conn.execute("DROP TABLE IF EXISTS neo4j_relationships CASCADE")
    await conn.execute("DROP TABLE IF EXISTS neo4j_nodes CASCADE")
    
    # Create unified nodes table
    await conn.execute("""
        CREATE TABLE neo4j_nodes (
            id SERIAL PRIMARY KEY,
            entity_id VARCHAR(50) NOT NULL UNIQUE,  -- e.g., person_001, org_093
            node_type VARCHAR(30) NOT NULL,           -- Person, Organization, Location, etc.
            name TEXT,
            aliases TEXT[],                           -- Array of alternate names
            birth_year INTEGER,
            death_year INTEGER,
            nationality VARCHAR(100),
            occupations TEXT[],
            summary TEXT,
            sources TEXT[],
            -- Location-specific fields
            country_code VARCHAR(10),
            location_type VARCHAR(50),
            -- Organization-specific fields
            organization_type VARCHAR(50),
            -- Equipment-specific fields
            equipment_type VARCHAR(50),
            model VARCHAR(100),
            tail_number VARCHAR(50),
            -- Legal case fields
            case_number VARCHAR(100),
            court VARCHAR(100),
            case_status VARCHAR(50),
            -- Event fields
            event_date DATE,
            event_type VARCHAR(50),
            venue TEXT,
            -- Claim fields
            claim_type VARCHAR(50),
            claim_status VARCHAR(50),
            -- Citation fields
            citation_text TEXT,
            citation_source VARCHAR(200),
            -- Raw data
            raw_properties JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Create indexes
    await conn.execute("CREATE INDEX idx_neo4j_nodes_type ON neo4j_nodes(node_type)")
    await conn.execute("CREATE INDEX idx_neo4j_nodes_name ON neo4j_nodes(name)")
    await conn.execute("CREATE INDEX idx_neo4j_nodes_entity_id ON neo4j_nodes(entity_id)")
    
    # Create relationships table
    await conn.execute("""
        CREATE TABLE neo4j_relationships (
            id SERIAL PRIMARY KEY,
            start_entity_id VARCHAR(50) NOT NULL,
            end_entity_id VARCHAR(50) NOT NULL,
            rel_type VARCHAR(50) NOT NULL,           -- ASSOCIATED_WITH, CEO_OF, etc.
            circled BOOLEAN,
            citations TEXT[],
            confidence FLOAT,
            context TEXT,
            verification_status VARCHAR(20),
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)
    
    # Create indexes
    await conn.execute("CREATE INDEX idx_neo4j_rel_start ON neo4j_relationships(start_entity_id)")
    await conn.execute("CREATE INDEX idx_neo4j_rel_end ON neo4j_relationships(end_entity_id)")
    await conn.execute("CREATE INDEX idx_neo4j_rel_type ON neo4j_relationships(rel_type)")
    await conn.execute("CREATE INDEX idx_neo4j_rel_confidence ON neo4j_relationships(confidence)")
    
    print("✓ Tables created")


async def import_persons(conn: asyncpg.Connection) -> int:
    """Import persons from persons.csv."""
    csv_path = BASE_DIR / "nodes/persons.csv"
    if not csv_path.exists():
        print(f"⚠ Persons file not found: {csv_path}")
        return 0
    
    print(f"Importing persons from {csv_path}...")
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse arrays (semicolon-separated)
            aliases = row.get('aliases:string[]', '').split(';') if row.get('aliases:string[]') else []
            occupations = row.get('occupations:string[]', '').split(';') if row.get('occupations:string[]') else []
            sources = row.get('sources:string[]', '').split(';') if row.get('sources:string[]') else []
            
            await conn.execute("""
                INSERT INTO neo4j_nodes (
                    entity_id, node_type, name, aliases, birth_year, death_year,
                    nationality, occupations, summary, sources
                ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ON CONFLICT (entity_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    aliases = EXCLUDED.aliases,
                    birth_year = EXCLUDED.birth_year,
                    death_year = EXCLUDED.death_year,
                    nationality = EXCLUDED.nationality,
                    occupations = EXCLUDED.occupations,
                    summary = EXCLUDED.summary,
                    sources = EXCLUDED.sources
            """, 
                row.get('entity_id:ID'),
                'Person',
                row.get('name'),
                aliases,
                int(row['birth_year:int']) if row.get('birth_year:int') else None,
                int(row['death_year:int']) if row.get('death_year:int') else None,
                row.get('nationality'),
                occupations,
                row.get('summary'),
                sources
            )
            count += 1
    
    print(f"✓ Imported {count} persons")
    return count


async def import_organizations(conn: asyncpg.Connection) -> int:
    """Import organizations."""
    csv_path = BASE_DIR / "nodes/organizations.csv"
    if not csv_path.exists():
        return 0
    
    print(f"Importing organizations...")
    count = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            await conn.execute("""
                INSERT INTO neo4j_nodes (entity_id, node_type, name, organization_type, summary)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (entity_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    organization_type = EXCLUDED.organization_type,
                    summary = EXCLUDED.summary
            """,
                row.get('entity_id:ID'),
                'Organization',
                row.get('name'),
                row.get('organization_type'),
                row.get('summary')
            )
            count += 1
    
    print(f"✓ Imported {count} organizations")
    return count


async def import_locations(conn: asyncpg.Connection) -> int:
    """Import locations."""
    csv_path = BASE_DIR / "nodes/locations.csv"
    if not csv_path.exists():
        return 0
    
    print(f"Importing locations...")
    count = 0
    
    # Check if file exists in different location
    alt_paths = [
        BASE_DIR / "nodes/location_nodes.csv",
        BASE_DIR.parent / "extracted/epstein_notes/csv/location_nodes.csv"
    ]
    
    for path in alt_paths:
        if path.exists():
            csv_path = path
            break
    
    if not csv_path.exists():
        print(f"⚠ Locations file not found")
        return 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            await conn.execute("""
                INSERT INTO neo4j_nodes (
                    entity_id, node_type, name, country_code, location_type, summary
                ) VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (entity_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    country_code = EXCLUDED.country_code,
                    location_type = EXCLUDED.location_type
            """,
                row.get('entity_id:ID') or row.get('id'),
                'Location',
                row.get('name'),
                row.get('country_code'),
                row.get('location_type'),
                row.get('summary')
            )
            count += 1
    
    print(f"✓ Imported {count} locations")
    return count


async def import_other_nodes(conn: asyncpg.Connection) -> int:
    """Import other node types (equipment, claims, citations, events, legal_cases)."""
    count = 0
    
    # Equipment
    csv_path = BASE_DIR / "nodes/equipment.csv"
    if csv_path.exists():
        print("Importing equipment...")
        skipped = 0
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entity_id = row.get('entity_id:ID')
                if not entity_id:
                    skipped += 1
                    continue
                await conn.execute("""
                    INSERT INTO neo4j_nodes (
                        entity_id, node_type, name, equipment_type, model, tail_number, summary
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                    ON CONFLICT (entity_id) DO NOTHING
                """,
                    entity_id,
                    'Equipment',
                    row.get('name'),
                    row.get('equipment_type'),
                    row.get('model'),
                    row.get('tail_number'),
                    row.get('summary')
                )
                count += 1
        if skipped > 0:
            print(f"  Skipped {skipped} rows with null entity_id")
    
    # Claims
    csv_path = BASE_DIR / "nodes/claims.csv"
    if csv_path.exists():
        print("Importing claims...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entity_id = row.get('entity_id:ID')
                if not entity_id:
                    continue
                await conn.execute("""
                    INSERT INTO neo4j_nodes (
                        entity_id, node_type, name, claim_type, claim_status, summary
                    ) VALUES ($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (entity_id) DO NOTHING
                """,
                    entity_id,
                    'Claim',
                    row.get('name'),
                    row.get('claim_type'),
                    row.get('claim_status'),
                    row.get('summary')
                )
                count += 1
    
    # Citations
    csv_path = BASE_DIR / "nodes/citations.csv"
    if csv_path.exists():
        print("Importing citations...")
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entity_id = row.get('entity_id:ID')
                if not entity_id:
                    continue
                await conn.execute("""
                    INSERT INTO neo4j_nodes (
                        entity_id, node_type, name, citation_text, citation_source
                    ) VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (entity_id) DO NOTHING
                """,
                    entity_id,
                    'Citation',
                    row.get('name'),
                    row.get('citation_text'),
                    row.get('citation_source')
                )
                count += 1
    
    # Events and Legal Cases (check extracted folder)
    for node_type, filename in [('Event', 'event_nodes.csv'), ('LegalCase', 'legal_case_nodes.csv')]:
        csv_path = BASE_DIR.parent / "extracted/epstein_notes/csv" / filename
        if csv_path.exists():
            print(f"Importing {node_type.lower()}s...")
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    raw_props = json.dumps({k: v for k, v in row.items() if v})
                    await conn.execute("""
                        INSERT INTO neo4j_nodes (
                            entity_id, node_type, name, raw_properties
                        ) VALUES ($1, $2, $3, $4)
                        ON CONFLICT (entity_id) DO NOTHING
                    """,
                        row.get('entity_id:ID') or row.get('id'),
                        node_type,
                        row.get('name'),
                        raw_props
                    )
                    count += 1
    
    print(f"✓ Imported {count} other nodes")
    return count


async def import_relationships(conn: asyncpg.Connection) -> int:
    """Import all relationship CSV files."""
    rel_dir = BASE_DIR / "relationships"
    if not rel_dir.exists():
        print(f"⚠ Relationships directory not found: {rel_dir}")
        return 0
    
    print(f"Importing relationships from {rel_dir}...")
    total_count = 0
    
    # Get all relationship CSV files
    rel_files = sorted(rel_dir.glob("*.csv"))
    print(f"Found {len(rel_files)} relationship files")
    
    for csv_file in rel_files:
        rel_type = csv_file.stem  # Filename without extension
        count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse citations array
                citations = []
                if row.get('citations:string[]'):
                    citations = row['citations:string[]'].split(';')
                
                # Parse circled boolean
                circled = None
                if row.get('circled:boolean'):
                    circled = row['circled:boolean'].lower() == 'true'
                
                # Parse confidence
                confidence = None
                if row.get('confidence:float'):
                    try:
                        confidence = float(row['confidence:float'])
                    except ValueError:
                        pass
                
                await conn.execute("""
                    INSERT INTO neo4j_relationships (
                        start_entity_id, end_entity_id, rel_type,
                        circled, citations, confidence, context, verification_status
                    ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                    row.get(':START_ID'),
                    row.get(':END_ID'),
                    rel_type,
                    circled,
                    citations,
                    confidence,
                    row.get('context'),
                    row.get('verification_status')
                )
                count += 1
        
        total_count += count
        print(f"  {rel_type}: {count} relationships")
    
    print(f"✓ Imported {total_count} total relationships from {len(rel_files)} files")
    return total_count


async def verify_import(conn: asyncpg.Connection):
    """Verify the import by querying counts."""
    print("\n--- Import Verification ---")
    
    # Node counts by type
    node_counts = await conn.fetch("""
        SELECT node_type, COUNT(*) as cnt 
        FROM neo4j_nodes 
        GROUP BY node_type 
        ORDER BY cnt DESC
    """)
    
    print("\nNode counts by type:")
    for row in node_counts:
        print(f"  {row['node_type']}: {row['cnt']}")
    
    # Relationship counts by type
    rel_counts = await conn.fetch("""
        SELECT rel_type, COUNT(*) as cnt 
        FROM neo4j_relationships 
        GROUP BY rel_type 
        ORDER BY cnt DESC
    """)
    
    print(f"\nRelationship counts (top 10 of {len(rel_counts)} types):")
    for row in rel_counts[:10]:
        print(f"  {row['rel_type']}: {row['cnt']}")
    
    # Total counts
    total_nodes = await conn.fetchval("SELECT COUNT(*) FROM neo4j_nodes")
    total_rels = await conn.fetchval("SELECT COUNT(*) FROM neo4j_relationships")
    
    print(f"\n--- Totals ---")
    print(f"Total nodes: {total_nodes}")
    print(f"Total relationships: {total_rels}")
    
    # Sample high-confidence relationships
    sample = await conn.fetch("""
        SELECT r.*, ns.name as start_name, ne.name as end_name
        FROM neo4j_relationships r
        LEFT JOIN neo4j_nodes ns ON r.start_entity_id = ns.entity_id
        LEFT JOIN neo4j_nodes ne ON r.end_entity_id = ne.entity_id
        WHERE r.confidence > 0.8 AND r.verification_status = 'Factual'
        LIMIT 5
    """)
    
    print(f"\n--- Sample High-Confidence Factual Relationships ---")
    for row in sample:
        print(f"  {row['start_name']} --[{row['rel_type']}]--> {row['end_name']} (conf: {row['confidence']})")


async def main():
    print("=" * 60)
    print("Neo4j Knowledge Graph Import")
    print("=" * 60)
    print(f"Source: {BASE_DIR}")
    print(f"Database: {DB_URL.replace('://', '://***:***@')}")
    print()
    
    try:
        conn = await asyncpg.connect(DB_URL)
        
        # Create tables
        await create_tables(conn)
        
        # Import nodes
        total_nodes = 0
        total_nodes += await import_persons(conn)
        total_nodes += await import_organizations(conn)
        total_nodes += await import_locations(conn)
        total_nodes += await import_other_nodes(conn)
        
        # Import relationships
        total_rels = await import_relationships(conn)
        
        # Verify
        await verify_import(conn)
        
        await conn.close()
        
        print("\n" + "=" * 60)
        print("Import Complete!")
        print(f"Total nodes: {total_nodes}")
        print(f"Total relationships: {total_rels}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
