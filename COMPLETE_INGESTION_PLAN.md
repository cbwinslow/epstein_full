# COMPLETE INGESTION PLAN - ALL DATA SOURCES

## Current State Analysis

### What We Have:
1. **House Financial Disclosures**: 50,429 records (2008-2026) - MISSING 1995-2007
2. **Senate Financial Disclosures**: 2,602 records (2012-2026) - Need full historical
3. **Congress Trading**: 18,521 transactions (2012-2026) - From OCR
4. **House PTR OCR**: 21,098 pages (2013-2026)
5. **FEC Contributions**: 490,000 records (2024 only) - MISSING 2000-2023, 2025-2026
6. **LDA Filings**: 30,600 records (2015 only) - MISSING other years

### What CapitolGains Offers:
- House: 1995-present (all report types)
- Senate: 2012-present (all report types)
- Report Types: PTR, Annual, Amendment, Blind Trust, Extension, New Filer, Termination, Other

### What We Need to Ingest:
1. ✅ House 1995-2007 (missing years)
2. ✅ House all report types for ALL years (comprehensive)
3. ✅ Senate all years 2012-2026 (comprehensive)
4. ✅ FEC 2000-2026 (all cycles)
5. ✅ LDA all available years
6. ✅ Full entity resolution across all data
7. ✅ Complete cross-source linking

## Execution Plan

### Phase 1: House Disclosures (1995-2007) - ~2 hours
- Use CapitolGains HouseDisclosureScraper
- Process years 1995-2007
- All report types
- Estimated: ~13 years × avg 500 records = 6,500 records

### Phase 2: House Comprehensive (All Years, All Types) - ~4 hours
- Re-process all years 1995-2026
- All 8 report types
- Ensure completeness
- Estimated: ~31 years × avg 1,000 records = 31,000 records

### Phase 3: Senate Comprehensive (All Years) - ~6 hours
- Use CapitolGains SenateDisclosureScraper
- All years 2012-2026
- All report types
- Estimated: ~15 years × avg 500 records = 7,500 records

### Phase 4: FEC Complete (2000-2026) - ~8 hours
- Download all FEC contribution files
- Process all cycles 2000-2026
- Estimated: ~5M+ records

### Phase 5: LDA Complete - ~2 hours
- Import all available LDA filings
- All years

### Phase 6: Entity Resolution - ~2 hours
- Re-run on complete dataset
- Cross-source linking

### Phase 7: Network Analysis - ~2 hours
- Build complete influence network
- Generate reports

### Total Estimated Time: ~26 hours

## Implementation Strategy

### Parallel Processing:
- House: 8 workers
- Senate: 4 workers (rate-limited)
- FEC: Batch processing

### Checkpoint System:
- Save progress after each year
- Resume capability
- Error recovery

### Data Validation:
- Verify record counts
- Check for duplicates
- Validate relationships

## Database Schema - Final

### House Financial Disclosures
- filing_id (PK)
- year
- last_name, first_name, suffix
- filing_type
- state_dst
- pdf_url
- updated_at

### Senate Financial Disclosures
- report_id (PK)
- first_name, last_name
- office_name
- filing_type
- report_year
- date_received
- pdf_url
- updated_at

### Congress Trading
- id (PK)
- politician_name, politician_party
- politician_state, politician_district
- transaction_date
- ticker, asset_name, asset_type
- transaction_type
- amount_low, amount_high, amount_text
- description
- data_source
- filing_date
- disclosure_url
- source_filing_id
- source_page_number
- source_row_hash
- source_raw_text
- created_at

### FEC Individual Contributions
- id (PK)
- cmte_id
- amndt_ind
- rpt_tp
- transaction_pgi
- image_num
- transaction_tp
- entity_tp
- name
- city
- state
- zip_code
- employer
- occupation
- transaction_dt
- transaction_amt
- other_id
- tran_id
- file_num
- memo_cd
- memo_text
- sub_id
- cycle
- created_at

### LDA Filings
- filing_uuid (PK)
- filing_type
- filing_year
- filing_period
- registrant_name
- registrant_id
- client_name
- client_id
- lobbyist_names
- lobbying_activities
- income
- expenses
- signed_date
- url
- updated_at

### Entity Resolution
- entity_id (PK)
- canonical_name
- entity_type
- states
- sources
- first_seen
- last_seen
- total_mentions

### Entity Raw Names
- mapping_id (PK)
- entity_id (FK)
- raw_name
- normalized_name
- source_table
- source_id
- confidence

## Expected Final Results

### Record Counts:
- House Financial Disclosures: ~60,000 (was 50,429)
- Senate Financial Disclosures: ~10,000 (was 2,602)
- Congress Trading: ~25,000 (was 18,521)
- FEC Contributions: ~5,000,000 (was 490,000)
- LDA Filings: ~50,000 (was 30,600)
- Entity Resolutions: ~500,000 (was 297,960)

### Total: ~5.2 million records

## Quality Assurance

### Validation Checks:
1. No duplicate records
2. All years covered
3. All report types included
4. Cross-source linking functional
5. Entity resolution accurate
6. Network analysis complete

### Data Integrity:
- Foreign key constraints
- Index optimization
- Query performance
- Backup procedures

## Success Criteria

✅ All CapitolGains data ingested (1995-present)
✅ All FEC data ingested (2000-present)
✅ All LDA data ingested (all years)
✅ No orphaned tables
✅ No duplicate work
✅ Complete documentation
✅ Full cross-source integration
✅ Analysis-ready database
