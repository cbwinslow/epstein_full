# Data Source: Third-Party GitHub Repositories

> **Source:** Various GitHub repositories  
> **Type:** Community curated data and knowledge graphs  
> **License:** Various Open Source  
> **Status:** 🔴 Not Yet Ingested (10K+ nodes available)  

---

## 📋 Available Repositories

| Repository | Author | Records | Type | URL | Status |
|------------|--------|---------|------|-----|--------|
| **epstein-network-data** | dleerdefi | 10,356 nodes, 16,625 edges | Knowledge Graph | `github.com/dleerdefi/epstein-network-data` | 🔴 Available |
| **epsteinbase** | white-roz3 | ~26 docs | DOJ Ingestion | `github.com/white-roz3/epsteinbase` | 🔴 Reference |
| **Epstein-files-dashboard** | maninka123 | 1,297 persons | Dashboard/Data | `github.com/maninka123/Epstein-files-dashboard` | 🔴 Reference |

---

## 🎯 Priority: epstein-network-data

### Repository Overview

**URL:** https://github.com/dleerdefi/epstein-network-data

**Description:** Making Epstein network documents searchable through data science. Extracts and structures data from:
- 📗 Birthday Book (128 pages)
- 📕 Black Book (95 pages, 1,252 contacts)
- ✈️ Flight Logs (118 pages, 1991-2019)

### Data Breakdown

| Document | Pages | Size | Status |
|----------|-------|------|--------|
| Birthday Book | 128 | ~244 MB | ⏸️ Needs extraction |
| Black Book | 95 | ~79 MB | ✅ Complete (external CSV) |
| Flight Logs | 118 | ~797 MB | 🔄 Partial (pages 32-38 need extraction) |

### Neo4j Knowledge Graph

**Nodes (10,356 total):**
- 2,541 Persons
- 2,051 Flights
- 283 Airports
- 97 Organizations
- 5 Equipment (aircraft)
- 53 Claims
- 73 Citations
- Contact Nodes: 3,676 PhoneNumbers, 385 EmailAddresses, 1,192 Addresses

**Relationships (16,625+ total, 65+ types):**
- FLEW_ON: Person → Flight (4,951)
- DEPARTED_FROM / ARRIVED_AT: Flight → Airport (4,012)
- TRAVELED_WITH: Person → Person (1,570)
- HAS_PHONE / HAS_EMAIL / HAS_ADDRESS (5,572)
- Legal: ABUSED, SUED_BY, REPRESENTED_BY
- Professional: WORKED_FOR, CEO_OF, FOUNDED

**Embeddings:**
- 436 vectors (1024 dimensions)
- Voyage-3-Large model
- Person, organization, claim embeddings

---

## 🔧 Ingestion Procedures

### Step 1: Clone Repository

```bash
cd /home/cbwinslow/workspace/epstein-data/external_repos

git clone https://github.com/dleerdefi/epstein-network-data.git
cd epstein-network-data
```

### Step 2: Explore Data Structure

```
data/
├── source/                    # 1.1GB - Original documents (LFS tracked)
│   ├── birthday_book/        # 128 PNG pages
│   ├── black_book/           # 95 PNG pages
│   └── flight_logs/          # 118 PNG pages
├── external_sources/          # 11MB - Third-party validated data
│   ├── black_book/
│   │   └── processed/complete.json    # 1,252 contacts
│   └── flight_logs/
│       └── EPSTEIN FLIGHT LOGS UNREDACTED.pdf
├── extracted/                 # 8.1MB - AI extraction outputs
└── final/                     # 7.3MB - Processed datasets
    └── epstein_notes/        # Production Neo4j dataset v2.0
        ├── nodes/            # 5 CSV files
        ├── relationships/    # 65 CSV files
        ├── embeddings/       # 3 CSV files
        └── NEO4J_COMPLETE_IMPORT.cypher
```

### Step 3: Import Black Book

```python
# save as: scripts/import_black_book.py

import json
import asyncpg
import asyncio

async def import_black_book():
    # Load external CSV/JSON
    with open('/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/black_book/processed/complete.json') as f:
        contacts = json.load(f)
    
    conn = await asyncpg.connect(
        "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    )
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS black_book_contacts (
            id SERIAL PRIMARY KEY,
            name TEXT,
            addresses TEXT[],
            phone_numbers TEXT[],
            emails TEXT[],
            professional_affiliations TEXT[],
            metadata JSONB,
            source TEXT DEFAULT 'dleerdefi/github'
        )
    """)
    
    for contact in contacts:
        await conn.execute("""
            INSERT INTO black_book_contacts 
            (name, addresses, phone_numbers, emails, professional_affiliations, metadata)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT DO NOTHING
        """,
            contact.get('name'),
            contact.get('addresses', []),
            contact.get('phone_numbers', []),
            contact.get('emails', []),
            contact.get('professional_affiliations', []),
            contact
        )
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(import_black_book())
```

### Step 4: Import Flight Logs

```python
# save as: scripts/import_flight_logs_github.py

import json
import asyncpg
import asyncio
from datetime import datetime

async def import_flight_logs():
    # Load extracted flight data
    with open('/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/final/flight_logs/flights.json') as f:
        flights = json.load(f)
    
    conn = await asyncpg.connect(
        "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    )
    
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS flight_logs_github (
            id SERIAL PRIMARY KEY,
            flight_date DATE,
            aircraft TEXT,
            departure_airport TEXT,
            arrival_airport TEXT,
            passengers TEXT[],
            notes TEXT,
            source TEXT DEFAULT 'dleerdefi/github'
        )
    """)
    
    for flight in flights:
        await conn.execute("""
            INSERT INTO flight_logs_github 
            (flight_date, aircraft, departure_airport, arrival_airport, passengers, notes)
            VALUES ($1, $2, $3, $4, $5, $6)
        """,
            flight.get('date'),
            flight.get('aircraft'),
            flight.get('departure'),
            flight.get('arrival'),
            flight.get('passengers', []),
            flight.get('notes')
        )
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(import_flight_logs())
```

### Step 5: Import Neo4j Knowledge Graph

```python
# save as: scripts/import_neo4j_graph.py

import csv
import asyncpg
import asyncio
from pathlib import Path

async def import_neo4j_graph():
    base_path = Path('/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/final/epstein_notes')
    
    conn = await asyncpg.connect(
        "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    )
    
    # Create tables
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS kg_persons (
            id TEXT PRIMARY KEY,
            name TEXT,
            normalized_name TEXT,
            entity_type TEXT,
            aliases TEXT[],
            embeddings VECTOR(1024)
        );
        
        CREATE TABLE IF NOT EXISTS kg_flights (
            id TEXT PRIMARY KEY,
            flight_date DATE,
            aircraft TEXT,
            departure_airport TEXT,
            arrival_airport TEXT
        );
        
        CREATE TABLE IF NOT EXISTS kg_relationships (
            id SERIAL PRIMARY KEY,
            from_id TEXT,
            to_id TEXT,
            rel_type TEXT,
            properties JSONB
        );
    """)
    
    # Import nodes
    nodes_path = base_path / 'nodes'
    
    # Import persons
    with open(nodes_path / 'persons.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            await conn.execute("""
                INSERT INTO kg_persons (id, name, normalized_name, entity_type)
                VALUES ($1, $2, $3, 'person')
                ON CONFLICT DO NOTHING
            """, row['id'], row['name'], row.get('normalized_name'))
    
    # Import relationships
    rels_path = base_path / 'relationships'
    
    for rel_file in rels_path.glob('*.csv'):
        rel_type = rel_file.stem
        with open(rel_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                await conn.execute("""
                    INSERT INTO kg_relationships (from_id, to_id, rel_type, properties)
                    VALUES ($1, $2, $3, $4)
                """, row['from'], row['to'], rel_type, row)
    
    await conn.close()

if __name__ == "__main__":
    asyncio.run(import_neo4j_graph())
```

---

## 📊 Expected Data Impact

| Source | Records | Value | Priority |
|--------|---------|-------|----------|
| Black Book | 1,252 contacts | Phone/address network | **HIGH** |
| Flight Logs | 2,051 flights | 1991-2019 travel | **HIGH** |
| Neo4j Graph | 10,356 nodes | Pre-built knowledge graph | **HIGH** |
| Birthday Book | 128 pages | Event photos/signatures | Medium |

---

## 📝 For AI Agents

### Before Starting:

1. **Clone the repository** to `epstein-data/external_repos/`
2. **Review the data structure** in `data/final/`
3. **Check CSV schemas** before writing import scripts
4. **Plan database schema** to avoid conflicts with existing tables

### During Import:

1. **Test on small sample** first
2. **Handle duplicates** with ON CONFLICT
3. **Log progress** for large imports
4. **Validate counts** match repository documentation

### After Import:

1. **Cross-reference** with existing data
2. **Build relationships** between sources
3. **Document completion** in DATA_INVENTORY
4. **Update AGENTS.md** with new capabilities

---

## 🔗 Related Documentation

- **Main Data Inventory:** `../../DATA_INVENTORY_FULL.md`
- **HuggingFace Guide:** `06-huggingface-datasets.md`
- **DOJ Guide:** `01-doj-epstein-library.md`

---

*Last Updated: April 10, 2026*  
*Status: Ready for Implementation*
