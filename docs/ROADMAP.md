# Technical Roadmap: Epstein Government Data Project

> **Version**: 1.0  
> **Last Updated**: April 14, 2026  
> **Status**: IN PROGRESS

---

## Phase 1: Data Acquisition (April 13-15, 2026) ⏳

### 1.1 Bulk Downloads (IN PROGRESS)

- [x] FEC 2024 Individual Contributions (447M records) ✅
- [x] White House Visitor Logs (sample) ✅
- [x] SEC EDGAR Form 4 (placeholders) ✅
- [x] USA Spending Awards (sample) ✅
- [x] Congress.gov Members & Bills ✅
- [ ] GovInfo Federal Register (2020-2024) - 300K docs 🔄 RUNNING
- [ ] Congressional Bills (2023-2024) - 20K docs 🔄 RUNNING
- [ ] Court Opinions (2022-2024) - 50K docs 🔄 RUNNING
- [ ] FARA Registrations - 5K docs 🔄 RUNNING
- [ ] Lobbying Disclosure (2020-2024) - 200K docs 🔄 RUNNING
- [ ] FEC Candidates & Committees (2020-2024) - 30K docs 🔄 RUNNING
- [ ] Financial Disclosures (2020-2024) - 2K docs 🔄 RUNNING

### 1.2 Import Pipeline (PENDING)

- [ ] Create standardized import schema
- [ ] Build `master_import_all.py` orchestration
- [ ] Implement conflict resolution (ON CONFLICT DO UPDATE)
- [ ] Add data validation layer
- [ ] Create ingestion monitoring dashboard

---

## Phase 2: Data Processing (April 15-17, 2026) ⏳

### 2.1 Cleaning & Normalization

- [ ] **Entity Name Standardization**
  - Remove titles (Mr., Mrs., Dr., Hon.)
  - Normalize suffixes (Jr., Sr., III)
  - Expand abbreviations (Corp. → Corporation)
  - Create name matching index

- [ ] **Address Normalization**
  - USPS standardization
  - Geocoding (lat/lon)
  - Congressional district mapping

- [ ] **Date Normalization**
  - ISO 8601 format enforcement
  - Fiscal vs calendar year alignment

- [ ] **Financial Amount Normalization**
  - Currency standardization
  - Inflation adjustment (CPI)

### 2.2 Entity Deduplication

- [ ] Build fuzzy matching pipeline
  - SOUNDEX/Metaphone for names
  - Levenshtein distance threshold
  - ML-based entity resolution (optional)

- [ ] Create master entity registry
  ```sql
  CREATE TABLE entity_master (
      entity_id UUID PRIMARY KEY,
      entity_type TEXT, -- 'person', 'organization', 'location'
      canonical_name TEXT,
      aliases TEXT[],
      sources TEXT[], -- ['fec', 'congress', 'lobbying']
      created_at TIMESTAMPTZ,
      updated_at TIMESTAMPTZ
  );
  ```

---

## Phase 3: Knowledge Graph (April 16-18, 2026) ⏳

### 3.1 Graph Schema Design

- [ ] **Node Types**
  - Person (politician, lobbyist, executive, victim)
  - Organization (company, NGO, government agency)
  - Location (address, city, country, coordinate)
  - Document (bill, filing, court case, email)

- [ ] **Edge Types**
  - CONTRIBUTED_TO (amount, date, cycle)
  - LOBBIED_FOR (start_date, end_date, issues, income)
  - VISITED (date, location, meeting_type)
  - EMPLOYED_BY (start_date, end_date, role)
  - REPRESENTS (entity_type, start_date, end_date)
  - MENTIONED_IN (role, confidence, context)
  - RELATED_TO (relationship_type, evidence)

### 3.2 Neo4j Implementation

- [ ] Deploy Neo4j Community instance
- [ ] Create import scripts (Cypher LOAD CSV)
- [ ] Build relationship extraction queries
- [ ] Add temporal edge properties
- [ ] Implement confidence scoring

### 3.3 Graph Analytics

- [ ] Centrality analysis (PageRank on influence)
- [ ] Community detection (clustering)
- [ ] Path finding (degrees of separation)
- [ ] Temporal analysis (evolution over time)

---

## Phase 4: RAG Pipeline (April 17-20, 2026) ⏳

### 4.1 Embedding Generation

- [ ] Select embedding model
  - **Choice**: nomic-embed-text-v2-moe (768-dim, Matryoshka)
  - Alternative: BGE-M3 (multi-lingual, multi-task)

- [ ] Generate embeddings for:
  - All documents (chunked)
  - All entities (canonical descriptions)
  - All relationships (edge descriptions)

- [ ] Store in pgvector
  ```sql
  CREATE TABLE embeddings (
      id UUID PRIMARY KEY,
      entity_type TEXT,
      entity_id TEXT,
      embedding vector(768),
      metadata JSONB
  );
  CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
  ```

### 4.2 Retrieval System

- [ ] Hybrid retriever (vector + graph)
- [ ] Re-ranking layer (Cohere/BGE cross-encoder)
- [ ] Query expansion (synonyms, related terms)
- [ ] Filter by time range, entity type, confidence

### 4.3 LLM Integration

- [ ] Select local LLM
  - **Choice**: Llama 3.1 70B (4-bit quantized)
  - Context: 128K tokens
  - Alternative: Mixtral 8x22B

- [ ] Prompt engineering
  - System prompt with context guidelines
  - Citation requirements (always cite sources)
  - Uncertainty handling ("I don't know")
  - Safety guardrails (no victim identification)

### 4.4 RAG Evaluation

- [ ] Create test query set
  - Factual lookup queries
  - Relationship path queries
  - Temporal analysis queries
- [ ] Measure accuracy, recall, hallucination rate
- [ ] A/B test different retrieval strategies

---

## Phase 5: API & Web Interface (April 18-22, 2026) ⏳

### 5.1 REST API (FastAPI)

Endpoints:
- [ ] `GET /api/v1/entities/search` - Full-text + semantic search
- [ ] `GET /api/v1/entities/{id}` - Entity details
- [ ] `GET /api/v1/entities/{id}/relationships` - Graph traversal
- [ ] `GET /api/v1/documents/search` - Document search
- [ ] `POST /api/v1/query` - Natural language RAG query
- [ ] `GET /api/v1/statistics` - Dataset statistics
- [ ] `GET /api/v1/cross-references` - Entity linking lookup

### 5.2 Web Interface (Next.js)

Pages:
- [ ] **Search Page** - Unified entity/document search
- [ ] **Entity Profile** - Full entity view with network graph
- [ ] **Network Explorer** - Interactive graph visualization (D3.js)
- [ ] **Timeline View** - Temporal activity visualization
- [ ] **Query Builder** - Structured query interface
- [ ] **API Docs** - Swagger/OpenAPI documentation

### 5.3 Data Export

- [ ] CSV export for filtered results
- [ ] Graph export (GEXF, GraphML)
- [ ] API rate limiting & authentication

---

## Phase 6: HuggingFace Publication (April 18, 2026) ⏳

### 6.1 Dataset Card

- [ ] Comprehensive README.md
  - Dataset description
  - Schema documentation
  - Usage examples
  - Citation information
  - Ethics statement

### 6.2 Data Organization

```
cbwinslow/epstein-government-data/
├── data/
│   ├── fec_contributions/
│   ├── lobbying_registrations/
│   ├── lobbying_quarterly/
│   ├── congress_members/
│   ├── congress_bills/
│   ├── fara_registrations/
│   ├── fara_principals/
│   ├── govinfo_packages/
│   ├── whitehouse_visitors/
│   ├── sec_filings/
│   └── usa_spending/
├── cross_references/
│   ├── entity_master_lookup.parquet
│   ├── relationship_graph.parquet
│   └── entity_embeddings.parquet
└── scripts/
    ├── download/
    ├── import/
    └── analysis/
```

### 6.3 Automated Publishing

- [ ] GitHub Actions workflow
  - Weekly data updates
  - Schema validation
  - Quality checks
  - Auto-publish to HuggingFace

---

## Phase 7: Advanced Analytics (April 20-25, 2026) 📅

### 7.1 Pattern Detection

- [ ] **Circular Contribution Detection**
  - A → B → C → A contribution cycles
  - Shell company identification

- [ ] **Influence Path Analysis**
  - Shortest path between entity and legislation
  - Multi-hop influence chains

- [ ] **Temporal Pattern Mining**
  - Bill introduction timing vs lobbying spend
  - Campaign contribution timing vs votes

### 7.2 ML Models

- [ ] **Entity Classification**
  - Classify entities by risk/interest level
  - Victim vs perpetrator vs witness classification

- [ ] **Anomaly Detection**
  - Unusual contribution patterns
  - Outlier lobbying expenditures

---

## Phase 8: Production Hardening (April 22-25, 2026) 📅

### 8.1 Performance Optimization

- [ ] Database query optimization
- [ ] Caching layer (Redis)
- [ ] CDN for static assets
- [ ] Database partitioning by year

### 8.2 Security

- [ ] Input sanitization
- [ ] SQL injection prevention
- [ ] Rate limiting
- [ ] DDoS protection
- [ ] Audit logging

### 8.3 Monitoring

- [ ] Application metrics (Prometheus)
- [ ] Error tracking (Sentry)
- [ ] Usage analytics
- [ ] Data freshness alerts

---

## Key Milestones

| Date | Milestone | Deliverable |
|------|-----------|-------------|
| Apr 15 | Data Acquisition Complete | 500M+ records ingested |
| Apr 16 | Processing Complete | Clean, normalized data |
| Apr 17 | Knowledge Graph Live | Neo4j with 1M+ nodes |
| Apr 18 | HuggingFace v1.0 | Public dataset release |
| Apr 20 | RAG Pipeline Beta | Working QA system |
| Apr 22 | Web Interface Beta | Search + graph viz |
| Apr 25 | Production Launch | Full public access |

---

## Resource Requirements

| Resource | Spec | Cost |
|----------|------|------|
| PostgreSQL | 32GB RAM, 1TB SSD | Self-hosted |
| Neo4j | 16GB RAM, 500GB SSD | Self-hosted |
| Embeddings | GPU (RTX 4090 / A100) | Self-hosted |
| API Server | 16GB RAM, 4 cores | Self-hosted |
| HuggingFace | Dataset hosting | Free |
| Total Monthly | | ~$200 (electricity) |

---

## Success Metrics

- [ ] **Data Coverage**: 500M+ records across 10+ sources
- [ ] **Entity Resolution**: 95%+ accuracy on name matching
- [ ] **RAG Accuracy**: 90%+ factual accuracy on test queries
- [ ] **Performance**: <2s query response time
- [ ] **Adoption**: 100+ researchers/journalists using platform
- [ ] **Impact**: 5+ investigative stories citing data

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| API rate limits | Download delays | Use bulk files, implement backoff |
| Data quality issues | Wrong conclusions | Validation layer, confidence scores |
| Legal challenges | Shutdown risk | Legal review, DMCA compliance |
| Compute limitations | Slow processing | Batch processing, prioritize |
| Hallucination in RAG | Misinformation | Citation requirements, confidence thresholds |

---

## Next Actions (Today)

1. ✅ Complete documentation (PROJECT_OVERVIEW.md, ROADMAP.md)
2. ⏳ Create HuggingFace dataset repository
3. ⏳ Set up monitoring for active downloads
4. ⏳ Begin entity normalization script
5. ⏳ Design knowledge graph schema

---

**Maintained by**: @cbwinslow  
**Contributors welcome**: See CONTRIBUTING.md
