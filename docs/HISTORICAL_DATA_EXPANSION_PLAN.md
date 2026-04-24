# Historical Data Expansion Plan (2000-Present)

**Objective:** Expand data coverage to year 2000 for Congress.gov, GovInfo.gov, and FEC contributions

**Last Updated:** April 22, 2026

**Tracking Issues:** `#51` (Congress historical backfill), `#52` (GovInfo historical backfill)

---

## Executive Summary

This plan outlines the strategy to expand historical data coverage from the current limited datasets to comprehensive year 2000-present coverage for:
- **Congress.gov:** Members, bills, votes (all branches)
- **GovInfo.gov:** Federal Register, bills, court opinions, committee reports
- **FEC:** Individual contributions (already covered 1980-2026)

**Estimated Data Volume:**
- Congress.gov: ~50,000 bills + ~2,000 members + ~50,000 votes per congress (25 years × 2 congresses)
- GovInfo.gov: ~500,000 documents (Federal Register + bills + opinions)
- FEC: ~500M individual contributions (already available 1980-2026)

---

## Current State Analysis

### Congress.gov
**Current verified state:**
- 107th Congress imported
  - Members: 553
  - Bills: 10,791
- 108th Congress imported
  - Members: 544
  - Bills: 10,669
- 109th Congress imported
  - Members: 546
  - Bills: 13,072
- 118th Congress imported
  - Members: 2,691
  - Bills: 19,315
- Votes: Not yet downloaded

**Gap:** 110th-117th backfill, and optional vote backfill

### GovInfo.gov
**Current verified state:**
- Existing current-era package import remains present
- Historical 2000 slice imported into `govinfo_packages`
  - `BILLS`: 7,075
  - `CRPT`: 849
  - `FR`: 253
  - `USCOURTS`: 366
- Historical 2001 slice imported into `govinfo_packages`
  - `FR`: 249
  - `USCOURTS`: 358
- Specialized summary tables now populated
  - `federal_register_entries`: 2,245
  - `court_opinions`: 30,724

**Gap:** 2002-2024 historical package backfill

### FEC
**Current:** 447,189,732 individual contributions in PostgreSQL
- Cycles present: 2000-2026
- Bulk historical requirement already satisfied for this project phase

**Gap:** None for 2000+ historical coverage

---

## Phase 1: API Research & Feasibility Assessment

### 1.1 Congress.gov API Research
**Tasks:**
- [x] Test Congress.gov API for historical congress access (107th-117th)
- [x] Verify availability of member lists and bills for historical congresses
- [ ] Check rate limits and pagination parameters
- [ ] Test ProPublica Congress API as alternative (may have better historical coverage)

**Validated endpoints:**
- `/member/congress/{congress}` - Members by congress
- `/bill/{congress}` - Bills by congress
- `/vote/congress/{congress}/{chamber}` - Votes by congress

**Success Criteria:**
- Can retrieve data for at least 107th Congress (2001-2002)
- API supports pagination for large result sets
- Rate limits allow reasonable download speed

### 1.2 GovInfo.gov API Research
**Tasks:**
- [x] Test GovInfo.gov API for historical date range (2000-2023)
- [ ] Verify bulk download availability for Federal Register
- [ ] Check collection coverage for bills, court opinions, committee reports
- [x] Test pagination and rate limits

**Collections to Test:**
- `FR` - Federal Register
- `BILLS` - Bills
- `USCOURTS` - Court opinions
- `CRPT` - Committee reports

**Success Criteria:**
- Can retrieve data from 2000-01-01 onwards
- Bulk download works for date ranges
- Reasonable rate limits for large downloads
- Large collections avoid the GovInfo `offset=10000` failure by splitting into smaller date windows

### 1.3 FEC Data Verification
**Tasks:**
- [x] Verify historical FEC coverage is already present in PostgreSQL
- [x] Verify data quality for historical cycles via cycle counts
- [ ] Estimate total size for 2000-2022 (13 cycles × 2.5GB = ~32GB)

**Success Criteria:**
- Historical coverage exists for the required 2000+ range
- Data format is queryable and partitionable by `cycle`
- Estimated total size is manageable

---

## Phase 2: Database Schema Optimization

### 2.1 Schema Audit
**Tasks:**
- [ ] Review current table schemas for data type optimization
- [ ] Identify oversized columns (TEXT where VARCHAR would suffice)
- [ ] Check for missing indexes on historical date columns
- [ ] Verify foreign key relationships

**Optimization Targets:**
- Convert TEXT to VARCHAR where length is known
- Add indexes on year/date columns for historical queries
- Partition large tables by year if needed
- Optimize numeric types (BIGINT vs INT vs SMALLINT)

### 2.2 Partitioning Strategy
**Considerations:**
- Partition `congress_bills` by congress number
- Partition `fec_individual_contributions` by 2-year cycle
- Partition `govinfo_packages` by year
- Partition `congress_votes` by congress

**Benefits:**
- Faster queries on specific time ranges
- Easier data management (drop old partitions)
- Parallel ingestion by partition

### 2.3 Index Optimization
**New Indexes to Add:**
```sql
-- Congress
CREATE INDEX idx_congress_bills_congress ON congress_bills(congress);
CREATE INDEX idx_congress_bills_year ON congress_bills(year);
CREATE INDEX idx_congress_votes_congress ON congress_votes(congress);

-- FEC
CREATE INDEX idx_fec_indiv_cycle ON fec_individual_contributions(cycle);
CREATE INDEX idx_fec_indiv_year ON fec_individual_contributions(transaction_date);

-- GovInfo
CREATE INDEX idx_govinfo_year ON govinfo_packages(year);
```

---

## Phase 3: Parallel Processing Architecture

### 3.1 Worker Pool Design
**Architecture:**
- Master process: Orchestrates downloads, assigns work to workers
- Worker processes: 5-10 concurrent workers per dataset type
- GPU workers: 3 GPU workers for OCR/embedding if needed
- Queue system: Redis or PostgreSQL queue for task distribution

**Worker Types:**
1. **Download Workers** (CPU-bound)
   - 5-10 workers for API downloads
   - Rate limiting per API endpoint
   - Retry logic with exponential backoff

2. **Ingestion Workers** (CPU-bound)
   - 5-10 workers for data parsing
   - Batch processing (1000-5000 records per batch)
   - Parallel database inserts

3. **GPU Workers** (if applicable)
   - 3 workers for OCR processing
   - 3 workers for embedding generation
   - Tesla K80 GPUs (2 available)

### 3.2 Task Scheduling Strategy
**Approach:**
- Break downloads into year-by-year chunks
- Schedule by priority and dependencies
- Example: Congress 107th → 108th → 109th → etc.

**Scheduling Rules:**
- Download all data for year X before ingestion
- Ingestion can run in parallel with next year's download
- FEC cycles can download independently (no dependencies)
- GovInfo collections can download in parallel

### 3.3 Rate Limiting & API Management
**Strategy:**
- Implement per-API rate limiters
- Use exponential backoff for retries
- Cache API responses where possible
- Respect API terms of service

**Rate Limits to Configure:**
- Congress.gov: 10 requests/second (documented limit)
- GovInfo.gov: 10 requests/second
- FEC API: 10 requests/second (if using API)
- FEC bulk downloads: No rate limit (file downloads)

---

## Phase 4: Implementation Plan

### 4.1 Congress.gov Historical Download (Priority: HIGH)

**Scope:** 107th-117th Congress (2001-2022)

**Data Types:**
- Members: ~2,000 per congress × 22 congresses = ~44,000 records
- Bills: ~4,000 per congress × 22 congresses = ~88,000 records
- Votes: ~2,000 per congress × 22 congresses = ~44,000 records

**Estimated Time:** 2-3 weeks (with 5 workers)

**Steps:**
1. Create `download_congress_historical.py` script
2. Implement year-by-year download loop
3. Add parallel processing with 5 workers
4. Create ingestion script for historical data
5. Test with 107th Congress first
6. Scale to all congresses

**Script Structure:**
```python
download_congress_historical.py
├── download_members(congress, chamber)
├── download_bills(congress)
├── download_votes(congress, chamber)
├── parallel_download(start_congress, end_congress, workers=5)
└── ingest_congress_historical.py
    ├── ingest_members()
    ├── ingest_bills()
    └── ingest_votes()
```

### 4.2 GovInfo.gov Historical Download (Priority: HIGH)

**Scope:** 2000-2023 Federal Register + Bills + Court Opinions

**Data Types:**
- Federal Register: ~20,000 documents/year × 23 years = ~460,000 records
- Bills: ~1,000 bills/year × 23 years = ~23,000 records
- Court Opinions: ~5,000 opinions/year × 23 years = ~115,000 records

**Estimated Time:** 3-4 weeks (with 5 workers)

**Steps:**
1. Modify `download_govinfo_bulk.py` to support 2000-2023
2. Add collection-specific download functions
3. Implement parallel processing by year
4. Create ingestion script for historical data
5. Test with 2000 first
6. Scale to all years

### 4.3 FEC Historical Download (Priority: MEDIUM)

**Scope:** 2000-2022 individual contributions (cycles 00, 02, 04, 06, 08, 10, 12, 14, 16, 18, 20, 22)

**Data Types:**
- Individual contributions: ~2.5GB per cycle × 13 cycles = ~32GB
- Estimated records: ~5-10M per cycle × 13 cycles = ~65-130M records

**Estimated Time:** 1-2 weeks (bulk downloads are fast, ingestion is slow)

**Steps:**
1. Modify existing FEC bulk download to target 2000-2022
2. Download all 13 cycle files
3. Create ingestion script with parallel processing
4. Optimize ingestion for large datasets (batch size, indexes)
5. Test with cycle 00 first
6. Scale to all cycles

---

## Phase 5: GPU Utilization Strategy

### 5.1 GPU Use Cases
**Applicable Tasks:**
- OCR processing for scanned PDFs (if any historical documents are scanned)
- Embedding generation for semantic search
- Text classification (document type detection)

**GPU Allocation:**
- Tesla K80 (0): OCR processing
- Tesla K80 (1): Embedding generation
- Tesla K40m (2): Classification/overflow

**Estimated Speedup:**
- OCR: 10-20x faster than CPU
- Embeddings: 5-10x faster than CPU
- Classification: 3-5x faster than CPU

### 5.2 GPU Implementation
**Tools:**
- Surya (OCR) - GPU-accelerated
- nomic-embed-text (embeddings) - GPU support
- BERT models (classification) - GPU support

**Integration:**
- Add GPU worker processes to worker pool
- Implement GPU task queue
- Batch GPU operations for efficiency

---

## Phase 6: Monitoring & Quality Assurance

### 6.1 Progress Tracking
**Metrics to Track:**
- Records downloaded per dataset per year
- Records ingested per dataset per year
- Download speed (records/second)
- Ingestion speed (records/second)
- Error rates and retry counts
- GPU utilization (if applicable)

**Dashboard:**
- Create `pipeline_status.py` with historical progress view
- Update `data_pipeline_tracking` table with historical entries
- Generate daily progress reports

### 6.2 Data Quality Checks
**Validation Steps:**
- [ ] Verify record counts match expected ranges
- [ ] Check for duplicate records (hash-based)
- [ ] Validate date ranges are correct
- [ ] Check for missing critical fields
- [ ] Sample data quality checks (format, consistency)

**Quality Thresholds:**
- Duplicate rate < 0.1%
- Missing critical fields < 1%
- Date range validation 100%
- Format consistency 100%

---

## Phase 7: Timeline & Resource Allocation

### 7.1 Estimated Timeline

| Phase | Duration | Dependencies | Workers |
|-------|----------|--------------|---------|
| Phase 1: API Research | 1 week | None | 1-2 |
| Phase 2: Schema Optimization | 1 week | Phase 1 | 1-2 |
| Phase 3: Architecture Design | 1 week | Phase 1 | 2-3 |
| Phase 4a: Congress Historical | 2-3 weeks | Phase 1-3 | 5-10 |
| Phase 4b: GovInfo Historical | 3-4 weeks | Phase 1-3 | 5-10 |
| Phase 4c: FEC Historical | 1-2 weeks | Phase 1-3 | 5-10 |
| Phase 5: GPU Integration | 1 week | Phase 4 | 2-3 |
| Phase 6: QA & Monitoring | Ongoing | Phase 4 | 2-3 |

**Total Estimated Time:** 10-13 weeks

### 7.2 Resource Requirements

**Compute Resources:**
- CPU: 16 cores (current server)
- GPU: 3 GPUs (Tesla K80 × 2, Tesla K40m × 1)
- RAM: 128GB (current server)
- Storage: ~500GB additional for historical data

**Network:**
- Bandwidth: ~100Mbps for bulk downloads
- API rate limits: Respect documented limits

**Database:**
- Current PostgreSQL: 2.1TB free (sufficient)
- May need additional storage for indexes

---

## Phase 8: Risk Mitigation

### 8.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limits exceeded | High | Medium | Implement rate limiters, use exponential backoff |
| Historical data not available | Medium | High | Research alternative APIs (ProPublica, bulk downloads) |
| Database performance degradation | Medium | Medium | Optimize indexes, use partitioning, batch inserts |
| Storage space insufficient | Low | High | Monitor disk usage, compress archives, add storage |
| GPU memory overflow | Medium | Low | Batch GPU operations, monitor GPU memory |
| Data quality issues | Medium | Medium | Implement validation checks, sample data review |

### 8.2 Contingency Plans

**If API historical data is unavailable:**
- Use bulk download sites (Congress.gov bulk data, GovInfo bulk)
- Scrape web pages as last resort
- Accept partial coverage (e.g., 2010-present)

**If database performance degrades:**
- Add more indexes
- Implement partitioning
- Use read replicas for queries
- Archive old data to separate tables

**If storage runs out:**
- Compress downloaded archives
- Delete intermediate files
- Add additional storage (RAID array has space)

---

## Next Steps

**Immediate Actions (This Week):**
1. Complete API research (Phase 1)
2. Test Congress.gov API for 107th Congress
3. Test GovInfo.gov API for 2000 date range
4. Verify FEC historical data availability

**Short-term Actions (Next 2-3 Weeks):**
1. Optimize database schemas (Phase 2)
2. Design parallel processing architecture (Phase 3)
3. Begin Congress.gov historical download (Phase 4a)

**Long-term Actions (Next 8-10 Weeks):**
1. Complete GovInfo.gov historical download (Phase 4b)
2. Complete FEC historical download (Phase 4c)
3. Integrate GPU processing (Phase 5)
4. Implement monitoring and QA (Phase 6)

---

## Success Criteria

**Project Success Defined As:**
- Congress.gov: Data available 107th-118th Congress (2001-2024)
- GovInfo.gov: Data available 2000-2024
- FEC: Data available 2000-2024 (already covered 1980-2026)
- Database performance: Queries complete in <5 seconds for year ranges
- Data quality: <1% error rate, <0.1% duplicate rate
- Storage: <500GB additional space used

**Failure Conditions:**
- Cannot access historical data for any source
- Database performance degrades significantly
- Storage space runs out
- Data quality issues >5% error rate

---

## Appendix: Reference Links

**API Documentation:**
- Congress.gov API: https://api.congress.gov/
- ProPublica Congress API: https://projects.propublica.org/api-docs/congress-api/
- GovInfo.gov API: https://www.govinfo.gov/api
- FEC API: https://api.open.fec.gov/v1/

**Bulk Download Sites:**
- Congress.gov Bulk: https://www.govinfo.gov/bulkdata
- FEC Bulk: https://www.fec.gov/files/bulk-downloads
- GovInfo Bulk: https://www.govinfo.gov/content/pkg

**Existing Scripts:**
- `/home/cbwinslow/workspace/epstein/scripts/ingestion/download_congress.py`
- `/home/cbwinslow/workspace/epstein/scripts/ingestion/download_govinfo_bulk.py`
- `/home/cbwinslow/workspace/epstein/scripts/ingestion/download/download_fec_bulk.py`
