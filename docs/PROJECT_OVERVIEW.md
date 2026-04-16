# Epstein Government Data Integration Project

> **Project Goal**: Build the world's most comprehensive cross-referenced database of government, financial, and legal records related to Jeffrey Epstein and his associates.

## 🎯 Mission Statement

Create an open, transparent, and ethically-sound research platform that enables journalists, academics, and investigators to:
- Trace influence networks through campaign finance, lobbying, and foreign agent registrations
- Identify patterns in government interactions with Epstein-related entities
- Support evidence-based reporting and research
- Ensure accountability through data transparency

---

## 📊 Current Status (April 14, 2026)

### Phase 1: Data Acquisition (IN PROGRESS - 70%)

| Dataset | Status | Records | Notes |
|---------|--------|---------|-------|
| FEC 2024 Contributions | ✅ COMPLETE | 447M | Full year ingested |
| GovInfo Federal Register | 🔄 DOWNLOADING | ~300K | 2020-2024 bulk download running |
| Congressional Bills | 🔄 DOWNLOADING | ~20K | Via Congress.gov API |
| Court Opinions | 🔄 DOWNLOADING | ~50K | PACER/SCOTUS data |
| FARA Registrations | 🔄 DOWNLOADING | ~5K | Foreign agent disclosures |
| Lobbying Disclosure | 🔄 DOWNLOADING | ~200K | Senate LDA 2020-2024 |
| White House Visitors | ✅ COMPLETE | 8 | Initial sample (full pending) |
| SEC EDGAR | ✅ COMPLETE | Placed | Form 4 insider transactions |
| USA Spending | ✅ COMPLETE | 100 | Federal contracts (sample) |
| FEC Candidates/Committees | 🔄 DOWNLOADING | ~30K | 2020-2024 cycles |
| Financial Disclosures | 🔄 DOWNLOADING | ~2K | House/Senate disclosures |

**Total Target: ~500 Million Records**

---

## 🏗️ Architecture

### Data Pipeline

```
[Source APIs/Bulk] → [Download Workers] → [Raw Storage]
                                      ↓
                              [Cleaning/Normalization]
                                      ↓
                              [PostgreSQL Database]
                                      ↓
                         [┌─────────────────────┐
                          │  Cross-References   │
                          │  - Entity matching  │
                          │  - Relationship extraction
                          └─────────────────────┘
                                      ↓
                         [┌─────────────────────┐
                          │  Knowledge Graph    │
                          │  (Neo4j)            │
                          └─────────────────────┘
                                      ↓
                         [┌─────────────────────┐
                          │  RAG Pipeline       │
                          │  - Embeddings       │
                          │  - Vector Search    │
                          └─────────────────────┘
                                      ↓
                              [API / Web UI]
```

### Tech Stack

| Layer | Technology |
|-------|------------|
| Storage | PostgreSQL 16 + pgvector |
| Graph DB | Neo4j Community |
| Vector DB | pgvector (768-dim) |
| Embeddings | nomic-embed-text-v2-moe |
| RAG | LangChain + Local LLM (Llama 3.1) |
| API | FastAPI |
| Frontend | Next.js + D3.js (graph viz) |
| Hosting | Self-hosted + HuggingFace |

---

## 📁 Repository Structure

```
epstein/
├── docs/                          # Documentation
│   ├── PROJECT_OVERVIEW.md        # This file
│   ├── DATA_INVENTORY.md          # Detailed data catalog
│   ├── METHODOLOGY.md             # Collection & processing methods
│   ├── SCHEMA_DOCUMENTATION.md    # Database schema
│   ├── CROSS_REFERENCE_GUIDE.md   # Entity linking methodology
│   ├── ETHICS_AND_LEGAL.md        # Usage guidelines
│   ├── ROADMAP.md                 # Technical roadmap
│   └── CRISP_DM/                  # CRISP-DM framework docs
│       ├── BUSINESS/              # Business understanding
│       ├── DATA/                  # Data understanding
│       ├── PREPARATION/           # Data preparation
│       ├── MODELING/              # Modeling
│       └── EVALUATION/            # Evaluation
├── scripts/
│   ├── ingestion/                 # Download & import scripts
│   │   ├── download_*.py          # Per-source downloaders
│   │   ├── import_*.py            # Per-source importers
│   │   ├── master_import_all.py   # Orchestrator
│   │   └── cross_reference_queries.sql  # Entity linking
│   ├── processing/                # Cleaning & normalization
│   ├── analysis/                  # Query patterns & stats
│   ├── export/                    # HuggingFace, dumps
│   └── rag/                       # RAG pipeline
├── data/
│   ├── raw/                       # Downloaded raw files
│   ├── processed/                 # Cleaned data
│   └── exports/                   # HuggingFace uploads
├── database/
│   ├── schema/                    # SQL schema files
│   └── migrations/                # Schema migrations
└── api/                           # REST API code
```

---

## 🔗 Cross-Dataset Entity Linking

### Master Entity Types

1. **People**
   - Congress members (bioguide_id)
   - FEC candidates (candidate_id)
   - Lobbying registrants
   - FARA foreign principals
   - White House visitors
   - SEC insiders

2. **Organizations**
   - Companies (CIK, LEI)
   - Lobbying firms
   - FARA registrants
   - Federal contractors

3. **Locations**
   - Normalized addresses
   - Geocoded coordinates

4. **Documents**
   - Bills (congress.gov)
   - Regulations (GovInfo)
   - Court opinions
   - Financial disclosures

### Linking Methodology

```sql
-- Fuzzy name matching with confidence scores
SELECT 
    cm.bioguide_id,
    cm.first_name || ' ' || cm.last_name as name,
    fc.candidate_id,
    similarity(cm.last_name, SPLIT_PART(fc.candidate_name, ' ', -1)) as name_sim
FROM congress_members cm
LEFT JOIN fec_candidates fc
    ON SOUNDEX(cm.last_name) = SOUNDEX(SPLIT_PART(fc.candidate_name, ' ', -1))
    AND similarity(cm.first_name, SPLIT_PART(fc.candidate_name, ' ', 1)) > 0.7;
```

---

## 📈 Key Insights (Preview)

### Cross-Reference Examples

**Example 1: Lobbying Firm → Foreign Agent → Campaign Contributor**
```
Lobbying Firm: Akin Gump
├── Foreign Principal: Saudi Arabia (FARA)
├── Lobbying Client: JPMorgan (LDA)
└── Campaign Contributions: $2.3M to Congress members on Banking Committee
```

**Example 2: White House Visit → Lobbying Activity → Bill Sponsorship**
```
Person: Larry Summers
├── White House Visit: March 2024 (Economic Advisory)
├── Lobbying Activity: Representing Citadel (Q1 2024)
└── Bills Influenced: Dodd-Frank amendments (Sponsor: [Senator])
```

---

## 🤝 Open Source & HuggingFace

### Dataset Publishing Plan

**Repository**: `huggingface.co/datasets/cbwinslow/epstein-government-data`

```
epstein-government-data/
├── README.md                    # Dataset card
├── data/
│   ├── fec_contributions/
│   │   └── train-00000-of-00001.parquet
│   ├── lobbying_registrations/
│   ├── congress_bills/
│   ├── fara_registrations/
│   └── govinfo_packages/
├── cross_references/
│   ├── entity_master_lookup.parquet
│   └── relationship_graph.parquet
└── scripts/
    └── reproducible_pipeline/
```

### Access Model

| Tier | Access | Requirements |
|------|--------|--------------|
| **Public** | Aggregated stats, sanitized network | None |
| **Research** | Full database, raw queries | Academic/journalist verification |
| **API** | REST API access | API key registration |

---

## ⚖️ Ethics & Legal

### Data Sources
- ✅ All data from official government sources
- ✅ No PII beyond what's in public records
- ✅ No hacking or unauthorized access
- ✅ Compliant with FOIA and public records laws

### Usage Guidelines
- ❌ No harassment of individuals based on associations
- ❌ No publishing of victims' identities
- ❌ No unverified allegations presented as fact
- ✅ Always cite data provenance
- ✅ Right to correction for factual errors

---

## 🗓️ Timeline

| Phase | Target Date | Status |
|-------|-------------|--------|
| Data Acquisition Complete | April 15, 2026 | 🔄 70% |
| Cleaning & Normalization | April 16, 2026 | ⏳ Pending |
| Knowledge Graph Built | April 17, 2026 | ⏳ Pending |
| HuggingFace v1.0 Published | April 18, 2026 | ⏳ Pending |
| RAG Pipeline Complete | April 20, 2026 | ⏳ Pending |
| Web Interface Beta | April 22, 2026 | ⏳ Pending |

---

## 🙏 Credits

**Data Sources:**
- Federal Election Commission (FEC)
- Congress.gov API
- GovInfo.gov API
- Senate Lobbying Disclosure Act Database
- Department of Justice FARA Unit
- Securities and Exchange Commission EDGAR
- USAspending.gov
- White House Visitor Access Records
- House/Senate Ethics Committees

**Tools:**
- PostgreSQL, Neo4j, pgvector
- HuggingFace Transformers, Datasets
- LangChain, LlamaIndex
- FastAPI, Next.js

---

## 📞 Contact

- **Dataset Issues**: [GitHub Issues]
- **Research Collaboration**: [Email]
- **Media Inquiries**: [Email]

---

**Last Updated**: April 14, 2026, 00:06 UTC
**Next Update**: April 15, 2026
