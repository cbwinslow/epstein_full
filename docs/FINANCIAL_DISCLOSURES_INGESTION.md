# Financial Disclosures Ingestion - Documentation

## Overview

This document tracks the financial disclosure data ingestion process for all US Congress members (House and Senate). The pipeline uses the **CapitolGains** library as the primary data source.

## Data Sources

### Primary Source: CapitolGains Library
- **GitHub**: https://github.com/thewillmundy/capitolgains
- **Version**: 0.1.0
- **Location**: `/home/cbwinslow/workspace/epstein/scripts/political_disclosures/CapitolGains/`

### CapitolGains Capabilities
- **House Disclosures**: 1995-present (electronic records)
- **Senate Disclosures**: 2012-present
- **Report Types**:
  - Periodic Transaction Reports (PTRs) - trades
  - Annual Financial Disclosures (FDs)
  - Amendments
  - Blind Trust Reports
  - Filing Extensions
  - New Filer Reports
  - Termination Reports

## Current Database Status

### House Financial Disclosures ✅ COMPLETE
- **Total Records**: 50,429
- **Year Range**: 2008-2026
- **Unique Filings**: 50,429
- **Report Types**:
  - O (Other): 15,789 (31.31%)
  - C: 9,616 (19.07%)
  - P (PTRs): 8,150 (16.16%)
  - X: 6,753 (13.39%)
  - A: 4,817 (9.55%)
  - D: 2,304 (4.57%)
  - T: 1,327 (2.63%)
  - W: 1,071 (2.12%)
  - H: 392 (0.78%)
  - E: 88 (0.17%)
  - G: 66 (0.13%)
  - B: 25 (0.05%)
  - N: 17 (0.03%)
  - F: 10 (0.02%)
  - R: 4 (0.01%)

### House PTR OCR Processing ✅ COMPLETE
- **Total PTRs OCR'd**: 8,150
- **OCR Pages**: 18,521
- **Transactions Extracted**: 18,521
- **Year Range**: 2013-2026
- **Total Transaction Value (low)**: $870M+
- **Total Transaction Value (high)**: $2.7B+

### Senate Financial Disclosures ⚠️ LIMITED
- **Total Records**: 3 (test records: Warren, Sanders, Graham)
- **Year Range**: 2023 (test data only)
- **Status**: ⚠️ **BLOCKED** - Senate efts.senate.gov API not accessible from this environment
  - CapitolGains library functional but requires efts.senate.gov for bulk data
  - DNS resolution fails for efts.senate.gov in current environment
  - Alternative: Use CapitolGains with manual Senator list (slow, rate-limited)
  - See "Senate Ingestion Options" section below

## Database Schema

### house_financial_disclosures
```sql
CREATE TABLE house_financial_disclosures (
    filing_id TEXT PRIMARY KEY,
    year INT,
    last_name TEXT,
    first_name TEXT,
    suffix TEXT,
    filing_type TEXT,
    state_dst TEXT,
    pdf_url TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### senate_financial_disclosures
```sql
CREATE TABLE senate_financial_disclosures (
    report_id TEXT PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    office_name TEXT,
    filing_type TEXT,
    report_year INT,
    date_received DATE,
    pdf_url TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

### house_ptr_ocr_pages
```sql
CREATE TABLE house_ptr_ocr_pages (
    filing_id TEXT NOT NULL,
    year INT,
    page_number INT NOT NULL,
    image_width INT,
    image_height INT,
    rotation INT,
    ocr_text TEXT,
    words JSONB,
    avg_confidence NUMERIC,
    ocr_engine TEXT DEFAULT 'tesseract',
    ocr_config TEXT,
    source_pdf TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (filing_id, page_number)
);
```

### congress_trading
```sql
CREATE TABLE congress_trading (
    id SERIAL PRIMARY KEY,
    politician_name TEXT,
    politician_state TEXT,
    politician_district TEXT,
    transaction_date DATE,
    ticker TEXT,
    asset_name TEXT,
    asset_type TEXT,
    transaction_type TEXT,
    amount_low NUMERIC,
    amount_high NUMERIC,
    amount_text TEXT,
    description TEXT,
    data_source TEXT,
    filing_date DATE,
    disclosure_url TEXT,
    source_filing_id TEXT,
    source_page_number INT,
    source_row_hash TEXT,
    source_raw_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Ingestion Pipeline

### Scripts

1. **financial_disclosures_ingestion.py**
   - Location: `/home/cbwinslow/workspace/epstein/scripts/ingestion/`
   - Purpose: Unified pipeline using CapitolGains
   - Features:
     - Parallel processing (configurable workers)
     - Checkpoint/resume capability
     - Progress tracking
     - Error handling
     - Database integration

2. **import_financial_disclosures.py**
   - Location: `/home/cbwinslow/workspace/epstein/scripts/ingestion/`
   - Purpose: Legacy House/Senate bulk import
   - Status: Used for initial House data load

### Usage

```bash
# Validate existing data
python3 scripts/ingestion/financial_disclosures_ingestion.py --validate-only

# Process House only
python3 scripts/ingestion/financial_disclosures_ingestion.py --chambers house --workers 8

# Process Senate only
python3 scripts/ingestion/financial_disclosures_ingestion.py --chambers senate --workers 4

# Process both with year range
python3 scripts/ingestion/financial_disclosures_ingestion.py --chambers house,senate --years 2020:2025 --workers 8

# Limit for testing
python3 scripts/ingestion/financial_disclosures_ingestion.py --chambers senate --limit 10 --workers 2
```

## CapitolGains Integration

### Installation
```bash
cd /home/cbwinslow/workspace/epstein/scripts/political_disclosures/CapitolGains
pip install --break-system-packages -e .
playwright install chromium
```

### API Usage

```python
from capitolgains import Congress, Representative, Senator
from capitolgains.utils.representative_scraper import HouseDisclosureScraper
from capitolgains.utils.senator_scraper import SenateDisclosureScraper

# Get Congress members
congress = Congress(api_key='YOUR_API_KEY')
members = congress.get_all_members()

# Get House disclosures
with HouseDisclosureScraper(headless=True) as scraper:
    rep = Representative("Pelosi", state="CA", district="11")
    disclosures = rep.get_disclosures(scraper, year="2023")

# Get Senate disclosures
with SenateDisclosureScraper(headless=True) as scraper:
    sen = Senator("Warren", first_name="Elizabeth", state="MA")
    disclosures = sen.get_disclosures(scraper, year="2023")
```

### CapitolGains Capabilities vs Limitations

**What CapitolGains Provides:**
- Filing-level metadata (filing_id, report_id, dates, names, states)
- Report types (PTR, Annual, Amendment, Blind Trust, etc.)
- PDF URLs for accessing full documents
- Congress member database

**What CapitolGains Does NOT Provide:**
- Individual transaction details (buy/sell amounts, tickers, prices)
- Transaction-level data requires OCR extraction from PDFs
- This is why House OCR pipeline (18,521 transactions) is separate from filing metadata

**Important Note:** CapitolGains "trades" = filing records, NOT individual transactions.
Individual transaction extraction requires OCR of PDF content.

### Senate Ingestion Status

**Current Status:** ⚠️ **BLOCKED** - Senate efts.senate.gov API not accessible

- DNS resolution fails for efts.senate.gov in current environment
- CapitolGains Senate scraper requires this API
- Test records (3) loaded manually using direct API calls
- Full Senate ingestion (100 members, 2012-2026) requires network fix

**Options:**
1. Fix DNS/network access to efts.senate.gov (RECOMMENDED)
2. Use CapitolGains with manual Senator list (very slow, rate-limited)
3. Direct PDF download + OCR (gets transaction data but very slow)

## Data Quality

### House Data Validation ✅
- All 50,429 records validated
- 8,150 PTRs OCR'd successfully
- 18,521 transactions extracted
- 100% OCR completion rate (2013-2026)

### Senate Data Validation ⚠️
- 3 test records loaded (Warren, Sanders, Graham)
- Full 100-member Senate pending (requires efts.senate.gov access)
- Years 2012-2026 not yet available

## Known Issues

1. **Congress.gov API**: Requires valid API key for member lookup
   - Workaround: Manual member list or database fallback available

2. **Senate Portal (efts.senate.gov)**: DNS resolution fails in current environment
   - Blocks all bulk Senate ingestion
   - Test records loaded via direct API calls

3. **State Validation**: Territories (PR, DC, VI, etc.) not valid for Senate
   - Only 50-state codes work with CapitolGains Senate scraper

4. **OCR Quality**: Variable based on PDF quality
   - Tesseract with rotation detection mitigates most issues

## Next Steps

1. **Immediate**: Fix DNS/access to efts.senate.gov for Senate bulk ingestion
2. **Short-term**: Run Senate ingestion (2012-2026) once network fixed
3. **Medium-term**: Implement Senate PTR OCR for transaction extraction
4. **Long-term**: Regular automated updates for new disclosures

## Monitoring

### Data Inventory
```sql
SELECT * FROM data_inventory
WHERE source_name LIKE '%Financial%';
```

### Quality Checks
```sql
-- House coverage
SELECT year, COUNT(*)
FROM house_financial_disclosures
GROUP BY year ORDER BY year;

-- Senate coverage
SELECT report_year, COUNT(*)
FROM senate_financial_disclosures
GROUP BY report_year ORDER BY report_year;

-- Transaction summary
SELECT
    EXTRACT(YEAR FROM transaction_date)::INT as year,
    COUNT(*) as transactions,
    COUNT(DISTINCT politician_name) as politicians
FROM congress_trading
GROUP BY year ORDER BY year;
```

## Contact & Support

- **Data Source**: CapitolGains (https://github.com/thewillmundy/capitolgains)
- **Original API**: Congress.gov, House Clerk, Senate EFS
- **Database**: PostgreSQL (epstein)
- **Logs**: `/home/cbwinslow/workspace/epstein/epstein-data/raw-files/financial_disclosures/`

## License

Data sourced from public government records (House Clerk, Senate EFS, Congress.gov).
CapitolGains library: MIT License.

### API Usage

```python
from capitolgains import Congress, Representative, Senator
from capitolgains.utils.representative_scraper import HouseDisclosureScraper
from capitolgains.utils.senator_scraper import SenateDisclosureScraper

# Get Congress members
congress = Congress(api_key='YOUR_API_KEY')
members = congress.get_all_members()

# Get House disclosures
with HouseDisclosureScraper(headless=True) as scraper:
    rep = Representative("Pelosi", state="CA", district="11")
    disclosures = rep.get_disclosures(scraper, year="2023")

# Get Senate disclosures
with SenateDisclosureScraper(headless=True) as scraper:
    sen = Senator("Warren", first_name="Elizabeth", state="MA")
    disclosures = sen.get_disclosures(scraper, year="2023")
```

## Data Quality

### House Data Validation
- ✅ All 50,429 records validated
- ✅ 8,150 PTRs OCR'd successfully
- ✅ 18,521 transactions extracted
- ✅ 100% OCR completion rate (2013-2026)

### Senate Data Validation
- ⚠️ Initial ingestion in progress
- ⚠️ 3 records loaded (test set)
- ⚠️ Full 100-member Senate pending

## Known Issues

1. **Congress.gov API**: Requires valid API key for member lookup
   - Workaround: Manual member list or database fallback

2. **Senate Portal**: Rate limiting on efts.senate.gov
   - Mitigation: Throttled requests, retry logic

3. **State Validation**: Some territories (PR, DC, etc.) not valid for Senate
   - Mitigation: Filter to 50 states only

4. **OCR Quality**: Variable based on PDF quality
   - Mitigation: Tesseract with rotation detection

## Next Steps

1. **Complete Senate Ingestion**
   - Target: All 100 senators
   - Years: 2012-2026
   - Estimated: 500-1000 disclosures

2. **Historical House Expansion**
   - Target: Pre-2008 records (if available)
   - Method: Archive.org, manual digitization

3. **Transaction Enrichment**
   - Ticker symbol standardization
   - Asset classification
   - Industry tagging

4. **Real-time Monitoring**
   - Automated periodic updates
   - New filing alerts
   - Change detection

## Monitoring

### Data Inventory
```sql
SELECT * FROM data_inventory
WHERE source_name LIKE '%Financial%';
```

### Quality Checks
```sql
-- House coverage
SELECT year, COUNT(*)
FROM house_financial_disclosures
GROUP BY year ORDER BY year;

-- Senate coverage
SELECT report_year, COUNT(*)
FROM senate_financial_disclosures
GROUP BY report_year ORDER BY report_year;

-- Transaction summary
SELECT
    EXTRACT(YEAR FROM transaction_date)::INT as year,
    COUNT(*) as transactions,
    COUNT(DISTINCT politician_name) as politicians
FROM congress_trading
GROUP BY year ORDER BY year;
```

## Contact & Support

- **Data Source**: CapitolGains (https://github.com/thewillmundy/capitolgains)
- **Original API**: Congress.gov, House Clerk, Senate EFS
- **Database**: PostgreSQL (epstein)
- **Logs**: `/home/cbwinslow/workspace/epstein/epstein-data/raw-files/financial_disclosures/`

## License

Data sourced from public government records (House Clerk, Senate EFS, Congress.gov).
CapitolGains library: MIT License.
