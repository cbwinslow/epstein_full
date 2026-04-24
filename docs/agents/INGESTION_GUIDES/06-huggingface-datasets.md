# Data Source: HuggingFace Datasets

> **Source:** https://huggingface.co/datasets
> **Type:** Community Curated Collections
> **License:** Various (check per dataset)
> **Status:** 🔴 Not Yet Ingested (~20K documents available)

---

## 📋 Available Datasets

| Dataset | Author | Records | Description | URL |
|---------|--------|---------|-------------|-----|
| **FULL_EPSTEIN_INDEX** | theelderemo | ~20,000 pages | House Oversight + DOJ combined | `datasets/theelderemo/FULL_EPSTEIN_INDEX` |
| **epstein-files-20k** | teyler | 20,000 docs | House Oversight documents | `datasets/teyler/epstein-files-20k` |
| **epstein-data** | kabasshouse | CC records | Credit card transactions | `datasets/kabasshouse/epstein-data` |
| **epstein-emails** | notesbymuneeb | 5,082 threads | Parsed email threads | `datasets/notesbymuneeb/epstein-emails` |
| **EPSTEIN_FILES_20K** | tensonaut | 20,000 docs | OCR + embeddings | `datasets/tensonaut/EPSTEIN_FILES_20K` |
| **epstein-fbi-files** | svetfm | FBI docs | FBI Vault releases | `datasets/svetfm/epstein-fbi-files` |
| **epstein-files-nov11-25** | svetfm | OCR'd docs | Post-OCR with embeddings | `datasets/svetfm/epstein-files-nov11-25-house-post-ocr-embeddings` |

---

## 🎯 Priority Datasets

### 1. FULL_EPSTEIN_INDEX (Highest Priority)

**Description:** Combined collection of:
- House Oversight Committee documents (~20,000 pages)
- DOJ disclosures (flight logs, contact books)
- "Masseuse List" and redacted materials

**Value:** Most comprehensive recent release (Nov 2025)

**Ingestion Status:** 🔴 NOT INGESTED

**Estimated Records:** ~20,000 pages

### 2. epstein-files-20k

**Description:** House Oversight Committee additional estate documents

**Source:** https://oversight.house.gov/release/oversight-committee-releases-additional-epstein-estate-documents/

**Value:** Official government release, court documents

**Ingestion Status:** 🔴 NOT INGESTED

**Estimated Records:** 20,000 documents

### 3. epstein-data (v2.0)

**Description:** Credit card transaction data from DOJ

**Contains:**
- Cardholder names (Epstein, Maxwell, Shuliak, etc.)
- Flight data (origin, destination, carrier, passenger)
- Merchant category classification

**Quality:** 31% quarantined for quality issues

**License:** CC-BY-4.0

**Ingestion Status:** 🔴 NOT INGESTED

---

## 🔧 Ingestion Pipeline

### Prerequisites

```bash
pip install datasets huggingface_hub
```

### Generic Ingestion Script Template

```python
from datasets import load_dataset
import asyncpg
import asyncio

async def ingest_huggingface_dataset():
    # Load dataset
    dataset = load_dataset("thelde/remo/FULL_EPSTEIN_INDEX", split="train")

    # Connect to PostgreSQL
    conn = await asyncpg.connect("postgresql://cbwinslow:123qweasd@localhost:5432/epstein")

    # Insert records
    for item in dataset:
        await conn.execute("""
            INSERT INTO documents (source, content, metadata)
            VALUES ($1, $2, $3)
            ON CONFLICT DO NOTHING
        """, "huggingface", item['text'], item['metadata'])

    await conn.close()

asyncio.run(ingest_huggingface_dataset())
```

---

## 📥 Proposed Ingestion Procedures

### Dataset 1: FULL_EPSTEIN_INDEX

```python
# save as: scripts/import_huggingface_full_index.py

from datasets import load_dataset
import asyncpg
import asyncio

async def import_full_index():
    print("Loading FULL_EPSTEIN_INDEX dataset...")
    dataset = load_dataset("thelde/remo/FULL_EPSTEIN_INDEX", split="train")

    conn = await asyncpg.connect(
        "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    )

    # Create table if not exists
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS hf_epstein_index (
            id SERIAL PRIMARY KEY,
            source TEXT,
            document_type TEXT,
            content TEXT,
            metadata JSONB,
            page_number INT,
            ingestion_date TIMESTAMPTZ DEFAULT NOW()
        )
    """)

    count = 0
    for item in dataset:
        await conn.execute("""
            INSERT INTO hf_epstein_index
            (source, document_type, content, metadata, page_number)
            VALUES ($1, $2, $3, $4, $5)
        """,
            item.get('source', 'unknown'),
            item.get('document_type', 'unknown'),
            item.get('text', ''),
            item.get('metadata', {}),
            item.get('page_number', 0)
        )
        count += 1

        if count % 100 == 0:
            print(f"Imported {count} records...")

    print(f"Complete! Imported {count} records")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(import_full_index())
```

### Dataset 2: epstein-data (Credit Cards)

```python
# save as: scripts/import_huggingface_cc_data.py

from datasets import load_dataset
import asyncpg
import asyncio

async def import_cc_data():
    print("Loading epstein-data credit card dataset...")
    dataset = load_dataset("kabasshouse/epstein-data", split="train")

    conn = await asyncpg.connect(
        "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"
    )

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS hf_credit_card_transactions (
            id SERIAL PRIMARY KEY,
            cardholder_name TEXT,
            transaction_date DATE,
            merchant TEXT,
            merchant_category TEXT,
            amount DECIMAL,
            flight_origin TEXT,
            flight_destination TEXT,
            carrier TEXT,
            passengers TEXT[],
            metadata JSONB
        )
    """)

    for item in dataset:
        await conn.execute("""
            INSERT INTO hf_credit_card_transactions
            (cardholder_name, transaction_date, merchant, merchant_category,
             amount, flight_origin, flight_destination, carrier, passengers, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        """,
            item.get('cardholder'),
            item.get('date'),
            item.get('merchant'),
            item.get('merchant_category'),
            item.get('amount'),
            item.get('flight_origin'),
            item.get('flight_destination'),
            item.get('carrier'),
            item.get('passengers', []),
            item
        )

    await conn.close()

if __name__ == "__main__":
    asyncio.run(import_cc_data())
```

---

## 📊 Expected Impact

| Dataset | Records | New Information | Priority |
|---------|---------|-----------------|----------|
| FULL_EPSTEIN_INDEX | ~20,000 | House Oversight 2025 | **HIGH** |
| epstein-files-20k | 20,000 | Estate documents | **HIGH** |
| epstein-data | ? | Credit card transactions | **HIGH** |
| epstein-emails | 5,082 | Parsed threads | Medium |
| epstein-fbi-files | ? | FBI releases | Medium |

---

## 📝 For AI Agents

### Implementation Steps:

1. **Create ingestion scripts** in `scripts/` directory
2. **Test on small sample** first (first 100 records)
3. **Verify schema** matches existing tables
4. **Run full ingestion** with progress logging
5. **Validate counts** match dataset metadata
6. **Document completion** in DATA_INVENTORY

### Quality Checks:

- Check for duplicates (ON CONFLICT DO NOTHING)
- Validate date formats
- Verify JSON metadata structure
- Confirm record counts match expected

### Integration:

- Cross-reference with existing `exposed_persons`
- Link to `exposed_flights` for flight data
- Match to `icij_entities` for financial connections

---

## ⚠️ Considerations

### Data Quality

- 31% of epstein-data (credit cards) quarantined for quality issues
- Some datasets may have OCR errors
- Verify against DOJ originals when possible

### Licensing

- **CC-BY-4.0:** Attribution required
- **ODbL:** Share-alike for derivatives
- Check each dataset's license before commercial use

### Storage

- Estimated 2-5 GB for all datasets
- Plan PostgreSQL storage accordingly
- Consider compression for text fields

---

## 🔗 Related Documentation

- **Data Inventory:** `../../DATA_INVENTORY_FULL.md`
- **DOJ Guide:** `01-doj-epstein-library.md`
- **GitHub Repos:** `07-third-party-repos.md`

---

*Last Updated: April 10, 2026*
*Status: Ready for Implementation*
