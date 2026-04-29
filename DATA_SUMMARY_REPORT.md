# Financial Disclosure Data Summary Report
**Generated:** April 29, 2026
**Database:** Epstein Analysis Database

## Executive Summary

The database contains **561,752 total records** across 5 financial disclosure tables, covering political contributions, lobbying activities, and financial disclosures from members of Congress. Data spans from 2008 to 2026, with complete year coverage for most datasets.

---

## Table-by-Table Breakdown

### 1. House Financial Disclosures (house_financial_disclosures)
- **Total Records:** 50,429
- **Years Covered:** 19 years (2008–2026)
- **Year Coverage:** 100% (all years present)
- **Unique Politicians:** 14,297
- **Most Recent Data:** 2026 (391 records)
- **Description:** Financial disclosure filings from members of the U.S. House of Representatives
- **Key Fields:** filing_id, year, last_name, first_name, suffix, filing_type, state_dst, pdf_url

### 2. Senate Financial Disclosures (senate_financial_disclosures)
- **Total Records:** 2,602
- **Years Covered:** 15 years (2012–2026)
- **Year Coverage:** 100% (all years present)
- **Unique Politicians:** 131
- **Most Recent Data:** 2026 (58 records)
- **Description:** Financial disclosure filings from members of the U.S. Senate
- **Key Fields:** report_id, first_name, last_name, office_name, filing_type, report_year, date_received, pdf_url

### 3. Congress Trading (congress_trading)
- **Total Records:** 18,521
- **Years Covered:** 15 years (2012–2026)
- **Year Coverage:** 100% (all years present)
- **Unique Politicians:** 326
- **Most Recent Data:** 2026 (423 records)
- **Description:** Stock trading transactions reported by members of Congress
- **Key Fields:** id, politician_name, politician_party, politician_state, politician_district, transaction_date, ticker, asset_name, asset_type, transaction_type, amount_low, amount_high, amount_text, description, data_source, filing_date, disclosure_url

### 4. FEC Individual Contributions (fec_individual_contributions)
- **Total Records:** 490,000
- **Years Covered:** 1 year (2024)
- **Year Coverage:** 100% (single cycle)
- **Unique Contributors:** 249,242
- **Most Recent Data:** 2024 cycle (490,000 records)
- **Description:** Individual campaign contributions to federal candidates and committees
- **Key Fields:** id, cmte_id, amndt_ind, rpt_tp, transaction_pgi, image_num, transaction_tp, entity_tp, name, city, state, zip_code, employer, occupation, transaction_dt, transaction_amt, employer, occupation, cycle

### 5. LDA Filings (lda_filings)
- **Total Records:** 30,600
- **Years Covered:** 1 year (2015)
- **Year Coverage:** 100% (single year)
- **Unique Registrants:** 4,354
- **Most Recent Data:** 2015 (30,600 records)
- **Description:** Lobbying Disclosure Act filings - quarterly reports from registered lobbyists
- **Key Fields:** filing_uuid, filing_type, filing_year, filing_period, registrant_name, registrant_id, client_name, client_id, lobbyist_names (jsonb), lobbying_activities (jsonb), income, expenses, signed_date, url

---

## Data Coverage Analysis

### Strengths:
1. **Complete Year Coverage:** House, Senate, and Congress Trading data show 100% year coverage with no gaps
2. **Recent Data:** All major disclosure types have current 2026 data
3. **Large Sample Sizes:** Particularly strong in FEC contributions (490K records) and House disclosures (50K+ records)
4. **Long Historical Range:** House data goes back to 2008 (19 years)

### Limitations:
1. **LDA Filings:** Only contains 2015 data - needs update for recent years (2016–2026)
2. **FEC Contributions:** Only contains 2024 cycle data - missing 2020, 2022 cycles
3. **Senate vs House Disparity:** Far fewer Senate records (2,602) vs House (50,429) due to smaller chamber size

---

## Cross-Reference Opportunities

### Potential Analysis:
1. **Politician Matching:** 326 politicians in trading data could be cross-referenced with 14,297 House + 131 Senate politicians
2. **Contribution-Trading Links:** FEC contributions (249K unique contributors) could be analyzed against trading patterns
3. **Lobbying-Trading Connections:** 4,354 LDA registrants could be matched against trading activities
4. **Temporal Analysis:** 2012–2026 continuous data enables time-series analysis of disclosure patterns

---

## Data Quality Notes

- All tables show 100% year coverage where applicable
- Most recent data is current (2026) for disclosure and trading tables
- JSONB fields in LDA filings provide structured activity/income data
- PDF URLs available for primary source verification in disclosure tables
- Transaction-level detail in trading data (amount ranges, dates, tickers)

## Recommendations

1. **Priority Updates:**
   - Update LDA filings for 2016–2026
   - Add missing FEC election cycles (2020, 2022)

2. **Data Enhancement:**
   - Consider adding politician_id foreign keys for cross-table analysis
   - Standardize name fields for better matching across tables

3. **Analysis Opportunities:**
   - Trading pattern analysis by party/state
   - Contribution influence studies
   - Lobbying expenditure trends
   - Financial disclosure completeness audits

---

*Report generated from Epstein Analysis Database on 2026-04-29*
