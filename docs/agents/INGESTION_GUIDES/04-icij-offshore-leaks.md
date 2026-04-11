# Data Source: ICIJ Offshore Leaks

> **Source:** https://offshoreleaks-data.icij.org/  
> **Type:** Financial Data / Offshore Entities  
> **License:** Open Database License (ODbL)  
> **Status:** ✅ Complete (3.3M relationships imported)  
> **Size:** ~600 MB extracted  

---

## 📋 Data Overview

The International Consortium of Investigative Journalists (ICIJ) Offshore Leaks database contains information on offshore entities and their connections to individuals worldwide.

### Leaks Included

| Leak | Year | Records |
|------|------|---------|
| Panama Papers | 2016 | ~11.5M documents |
| Paradise Papers | 2017 | ~13.4M documents |
| Pandora Papers | 2021 | ~11.9M documents |
| Bahamas Leaks | 2016 | ~38,000 entities |
| Offshore Leaks | 2013 | ~130,000 entities |

### Our Extracted Data

| File | Rows | Size | Description |
|------|------|------|-------------|
| nodes-entities.csv | 814,617 | 190 MB | Companies/offshore entities |
| nodes-officers.csv | ~1,800,000 | 87 MB | People/officers |
| nodes-addresses.csv | ~700,000 | 69 MB | Addresses |
| nodes-intermediaries.csv | ~38,000 | 3.8 MB | Intermediaries |
| nodes-others.csv | ~4,000 | 389 KB | Other entities |
| relationships.csv | 3,339,272 | 247 MB | Entity relationships |

---

## 🔧 Ingestion Pipeline

### Download Location

```
https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip
```

### Downloaded File

- **Date:** April 3, 2026
- **Size:** 69.7 MB compressed
- **Extracted:** ~600 MB
- **Location:** `/home/cbwinslow/workspace/epstein-data/downloads/icij_extracted/`

---

## 📥 Ingestion Procedure

### Step 1: Import Script

```bash
cd /home/cbwinslow/workspace/epstein/scripts

python3 import_icij.py
```

**Features:**
- Batch processing: 5,000 rows/batch
- Proper column mapping (ibcRUC, sourceID match CSV headers)
- Conflict handling: ON CONFLICT DO NOTHING
- Index creation for performance

### Step 2: Monitoring

```bash
tail -f /tmp/icij_import_v2.log
```

---

## 🗄️ Database Schema

### PostgreSQL Tables

| Table | Records | Description |
|-------|---------|-------------|
| `icij_entities` | 814,344 | Offshore companies/entities |
| `icij_officers` | ~1,800,000 | People/officers |
| `icij_addresses` | ~700,000 | Addresses |
| `icij_intermediaries` | ~38,000 | Intermediaries/brokers |
| `icij_others` | ~4,000 | Other entity types |
| `icij_relationships` | 3,339,272 | Entity relationships |

### Schema Details

#### icij_entities

```csv
node_id, name, original_name, former_name, jurisdiction, 
jurisdiction_description, company_type, address, internal_id, 
incorporation_date, inactivation_date, struck_off_date, 
dorm_date, status, service_provider, ibcRUC, country_codes, 
countries, sourceID, valid_until, note
```

#### icij_relationships

```csv
node_id_start, node_id_end, rel_type, link, status, 
start_date, end_date, sourceID
```

---

## 📊 Quality Metrics

| Metric | Value | Date |
|--------|-------|------|
| Entities | 814,344 | April 4, 2026 |
| Officers | ~1,800,000 | April 4, 2026 |
| Relationships | 3,339,267 | April 4, 2026 |
| Import Time | ~4 hours | - |
| Errors | 0 | - |

---

## 🔍 Epstein Network Connections

### Search Strategy

```sql
-- Find entities related to Epstein
SELECT * FROM icij_entities 
WHERE name ILIKE '%epstein%'
OR name ILIKE '%maxwell%'
OR name ILIKE '%wexner%';

-- Find officers related to Epstein network
SELECT * FROM icij_officers 
WHERE name ILIKE '%epstein%'
OR name ILIKE '%maxwell%';

-- Find relationships
SELECT r.*, e1.name as entity1, e2.name as entity2
FROM icij_relationships r
JOIN icij_entities e1 ON r.node_id_start = e1.node_id
JOIN icij_entities e2 ON r.node_id_end = e2.node_id
WHERE e1.name ILIKE '%epstein%'
OR e2.name ILIKE '%epstein%';
```

---

## 📝 For AI Agents

### When Working with This Data:

1. **Use node_id joins** - All tables connect via node_id
2. **Filter by sourceID** - Panama, Paradise, Pandora, etc.
3. **Check incorporation_date** - Temporal analysis
4. **Look for jurisdictions** - Tax havens (BVI, Cayman, etc.)
5. **Follow relationships** - officer_of, registered_address, etc.

### Relationship Types

| Type | Meaning |
|------|---------|
| officer_of | Person is officer of entity |
| registered_address | Entity address |
| intermediary_of | Intermediary connection |
| similar | Similar entities |

### Sample Analysis Query:

```sql
-- Find offshore entities with multiple officers
SELECT e.name, e.jurisdiction, COUNT(*) as officer_count
FROM icij_entities e
JOIN icij_relationships r ON e.node_id = r.node_id_end
WHERE r.rel_type = 'officer_of'
GROUP BY e.name, e.jurisdiction
HAVING COUNT(*) > 5
ORDER BY officer_count DESC
LIMIT 100;
```

---

## 📚 License

**Open Database License (ODbL)**

- ✅ Free to use
- ✅ Free to share
- ✅ Free to modify
- ✅ Commercial use allowed
- ⚠️ Must share-alike
- ⚠️ Must attribute ICIJ

---

## 🔗 Related Sources

- **FEC Data:** Political donations (cross-reference officers)
- **DOJ Library:** Financial documents (cross-reference entities)
- **Black Book:** Contact addresses (cross-reference addresses)

---

*Last Updated: April 10, 2026*
