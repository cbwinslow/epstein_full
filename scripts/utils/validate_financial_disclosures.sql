-- =============================================================================
-- FINANCIAL DISCLOSURE DATA QUALITY VALIDATION
-- =============================================================================
-- This script validates the quality of financial disclosure data by:
-- 1. Counting records per table
-- 2. Checking NULL values in critical fields
-- 3. Validating amount fields (ranges, formats)
-- 4. Checking date validity
-- 5. Verifying politician name linking
-- 6. Checking data consistency across tables
-- =============================================================================

-- =============================================================================
-- SECTION 1: RECORD COUNTS
-- =============================================================================

SELECT '=== RECORD COUNTS ===' AS section;

SELECT
    'house_financial_disclosures' AS table_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT filing_id) AS unique_filings,
    COUNT(DISTINCT CONCAT(last_name, ', ', first_name)) AS unique_politicians
FROM house_financial_disclosures
UNION ALL
SELECT
    'senate_financial_disclosures' AS table_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT report_id) AS unique_filings,
    COUNT(DISTINCT CONCAT(last_name, ', ', first_name)) AS unique_politicians
FROM senate_financial_disclosures
UNION ALL
SELECT
    'congress_trading' AS table_name,
    COUNT(*) AS total_records,
    COUNT(DISTINCT source_filing_id) AS unique_filings,
    COUNT(DISTINCT politician_name) AS unique_politicians
FROM congress_trading
UNION ALL
SELECT
    'politician_financial_summary' AS table_name,
    COUNT(*) AS total_records,
    NULL AS unique_filings,
    COUNT(DISTINCT politician_name) AS unique_politicians
FROM politician_financial_summary;

-- =============================================================================
-- SECTION 2: NULL VALUE CHECKS
-- =============================================================================

SELECT '=== NULL VALUE CHECKS ===' AS section;

-- House Financial Disclosures
SELECT 'house_financial_disclosures' AS table_name, 'filing_id' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM house_financial_disclosures), 2) AS null_pct
FROM house_financial_disclosures WHERE filing_id IS NULL
UNION ALL
SELECT 'house_financial_disclosures' AS table_name, 'last_name' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM house_financial_disclosures), 2) AS null_pct
FROM house_financial_disclosures WHERE last_name IS NULL
UNION ALL
SELECT 'house_financial_disclosures' AS table_name, 'first_name' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM house_financial_disclosures), 2) AS null_pct
FROM house_financial_disclosures WHERE first_name IS NULL
UNION ALL
SELECT 'house_financial_disclosures' AS table_name, 'year' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM house_financial_disclosures), 2) AS null_pct
FROM house_financial_disclosures WHERE year IS NULL
UNION ALL
SELECT 'house_financial_disclosures' AS table_name, 'pdf_url' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM house_financial_disclosures), 2) AS null_pct
FROM house_financial_disclosures WHERE pdf_url IS NULL;

-- Senate Financial Disclosures
SELECT 'senate_financial_disclosures' AS table_name, 'report_id' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM senate_financial_disclosures), 2) AS null_pct
FROM senate_financial_disclosures WHERE report_id IS NULL
UNION ALL
SELECT 'senate_financial_disclosures' AS table_name, 'last_name' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM senate_financial_disclosures), 2) AS null_pct
FROM senate_financial_disclosures WHERE last_name IS NULL
UNION ALL
SELECT 'senate_financial_disclosures' AS table_name, 'first_name' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM senate_financial_disclosures), 2) AS null_pct
FROM senate_financial_disclosures WHERE first_name IS NULL
UNION ALL
SELECT 'senate_financial_disclosures' AS table_name, 'report_year' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM senate_financial_disclosures), 2) AS null_pct
FROM senate_financial_disclosures WHERE report_year IS NULL;

-- Congress Trading - Critical Fields
SELECT 'congress_trading' AS table_name, 'politician_name' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS null_pct
FROM congress_trading WHERE politician_name IS NULL
UNION ALL
SELECT 'congress_trading' AS table_name, 'transaction_date' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS null_pct
FROM congress_trading WHERE transaction_date IS NULL
UNION ALL
SELECT 'congress_trading' AS table_name, 'ticker' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS null_pct
FROM congress_trading WHERE ticker IS NULL
UNION ALL
SELECT 'congress_trading' AS table_name, 'amount_low' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS null_pct
FROM congress_trading WHERE amount_low IS NULL
UNION ALL
SELECT 'congress_trading' AS table_name, 'amount_high' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS null_pct
FROM congress_trading WHERE amount_high IS NULL
UNION ALL
SELECT 'congress_trading' AS table_name, 'amount_text' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS null_pct
FROM congress_trading WHERE amount_text IS NULL;

-- Politician Financial Summary
SELECT 'politician_financial_summary' AS table_name, 'politician_name' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM politician_financial_summary), 2) AS null_pct
FROM politician_financial_summary WHERE politician_name IS NULL
UNION ALL
SELECT 'politician_financial_summary' AS table_name, 'year' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM politician_financial_summary), 2) AS null_pct
FROM politician_financial_summary WHERE year IS NULL
UNION ALL
SELECT 'politician_financial_summary' AS table_name, 'total_assets_low' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM politician_financial_summary), 2) AS null_pct
FROM politician_financial_summary WHERE total_assets_low IS NULL
UNION ALL
SELECT 'politician_financial_summary' AS table_name, 'total_assets_high' AS column_name,
       COUNT(*) AS null_count, ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM politician_financial_summary), 2) AS null_pct
FROM politician_financial_summary WHERE total_assets_high IS NULL;

-- =============================================================================
-- SECTION 3: AMOUNT VALIDATION (congress_trading)
-- =============================================================================

SELECT '=== AMOUNT VALIDATION (congress_trading) ===' AS section;

-- Check for negative amounts
SELECT 'Negative amount_low' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE amount_low < 0
UNION ALL
SELECT 'Negative amount_high' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE amount_high < 0;

-- Check if amount_high < amount_low (illogical)
SELECT 'amount_high < amount_low (illogical)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE amount_high < amount_low;

-- Check amount ranges (common ranges in STOCK Act disclosures)
SELECT 'Amount range distribution' AS check_type,
       CASE
           WHEN amount_text LIKE '%$1,001 - $15,000%' THEN '$1,001 - $15,000'
           WHEN amount_text LIKE '%$15,001 - $50,000%' THEN '$15,001 - $50,000'
           WHEN amount_text LIKE '%$50,001 - $100,000%' THEN '$50,001 - $100,000'
           WHEN amount_text LIKE '%$100,001 - $250,000%' THEN '$100,001 - $250,000'
           WHEN amount_text LIKE '%$250,001 - $500,000%' THEN '$250,001 - $500,000'
           WHEN amount_text LIKE '%$500,001 - $1,000,000%' THEN '$500,001 - $1,000,000'
           WHEN amount_text LIKE '%$1,000,001 - $5,000,000%' THEN '$1,000,001 - $5,000,000'
           WHEN amount_text LIKE '%$5,000,001 - $25,000,000%' THEN '$5,000,001 - $25,000,000'
           WHEN amount_text LIKE '%$25,000,001 - $50,000,000%' THEN '$25,000,001 - $50,000,000'
           WHEN amount_text LIKE '%Over $50,000,000%' THEN 'Over $50,000,000'
           WHEN amount_text LIKE '%Undisclosed%' THEN 'Undisclosed'
           ELSE 'Other/Unknown'
       END AS amount_range,
       COUNT(*) AS count
FROM congress_trading
WHERE amount_text IS NOT NULL
GROUP BY 2
ORDER BY count DESC;

-- Verify amount_low and amount_high match amount_text where possible
SELECT 'amount_low matches amount_text ($1,001-$15,000)' AS check_type, COUNT(*) AS count
FROM congress_trading
WHERE amount_text LIKE '%$1,001 - $15,000%'
  AND (amount_low != 1001 OR amount_high != 15000)
UNION ALL
SELECT 'amount_low matches amount_text ($15,001-$50,000)' AS check_type, COUNT(*) AS count
FROM congress_trading
WHERE amount_text LIKE '%$15,001 - $50,000%'
  AND (amount_low != 15001 OR amount_high != 50000);

-- =============================================================================
-- SECTION 4: DATE VALIDATION
-- =============================================================================

SELECT '=== DATE VALIDATION ===' AS section;

-- Check for future dates
SELECT 'Future transaction dates (congress_trading)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE transaction_date > CURRENT_DATE
UNION ALL
SELECT 'Future filing dates (congress_trading)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE filing_date > CURRENT_DATE
UNION ALL
SELECT 'Future report years (house)' AS check_type, COUNT(*) AS count
FROM house_financial_disclosures WHERE year > EXTRACT(YEAR FROM CURRENT_DATE)
UNION ALL
SELECT 'Future report years (senate)' AS check_type, COUNT(*) AS count
FROM senate_financial_disclosures WHERE report_year > EXTRACT(YEAR FROM CURRENT_DATE);

-- Check for very old dates (before 2000 - likely errors)
SELECT 'Very old transaction dates (<2000)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE transaction_date < '2000-01-01'
UNION ALL
SELECT 'Very old report years (house, <2000)' AS check_type, COUNT(*) AS count
FROM house_financial_disclosures WHERE year < 2000
UNION ALL
SELECT 'Very old report years (senate, <2000)' AS check_type, COUNT(*) AS count
FROM senate_financial_disclosures WHERE report_year < 2000;

-- =============================================================================
-- SECTION 5: POLITICIAN NAME VALIDATION
-- =============================================================================

SELECT '=== POLITICIAN NAME VALIDATION ===' AS section;

-- Check for empty or whitespace-only names
SELECT 'Empty politician_name (congress_trading)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE politician_name IS NULL OR TRIM(politician_name) = ''
UNION ALL
SELECT 'Empty last_name (house)' AS check_type, COUNT(*) AS count
FROM house_financial_disclosures WHERE last_name IS NULL OR TRIM(last_name) = ''
UNION ALL
SELECT 'Empty last_name (senate)' AS check_type, COUNT(*) AS count
FROM senate_financial_disclosures WHERE last_name IS NULL OR TRIM(last_name) = '';

-- Check for names that look malformed (too short, numeric, etc.)
SELECT 'Very short politician_name (<3 chars, congress_trading)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE LENGTH(TRIM(politician_name)) < 3
UNION ALL
SELECT 'Numeric politician_name (congress_trading)' AS check_type, COUNT(*) AS count
FROM congress_trading WHERE politician_name ~ '^[0-9]+$';

-- Show sample politician names for review
SELECT 'Sample politician names (congress_trading)' AS check_type,
       politician_name, COUNT(*) AS appearances
FROM congress_trading
GROUP BY politician_name
ORDER BY appearances DESC
LIMIT 20;

-- =============================================================================
-- SECTION 6: CROSS-TABLE VALIDATION
-- =============================================================================

SELECT '=== CROSS-TABLE VALIDATION ===' AS section;

-- Check if politicians in congress_trading appear in financial disclosures
SELECT 'Politicians in trading but NOT in house disclosures' AS check_type, COUNT(DISTINCT ct.politician_name) AS count
FROM congress_trading ct
LEFT JOIN house_financial_disclosures hfd
       ON LOWER(ct.politician_name) LIKE '%' || LOWER(hfd.last_name) || '%'
WHERE hfd.last_name IS NULL
UNION ALL
SELECT 'Politicians in trading but NOT in senate disclosures' AS check_type, COUNT(DISTINCT ct.politician_name) AS count
FROM congress_trading ct
LEFT JOIN senate_financial_disclosures sfd
       ON LOWER(ct.politician_name) LIKE '%' || LOWER(sfd.last_name) || '%'
WHERE sfd.last_name IS NULL;

-- Check if source_filing_id in congress_trading links to actual filings
SELECT 'Orphaned source_filing_id (not in house)' AS check_type, COUNT(*) AS count
FROM congress_trading ct
WHERE ct.source_filing_id IS NOT NULL
  AND ct.source_filing_id NOT IN (SELECT filing_id FROM house_financial_disclosures)
  AND ct.source_filing_id NOT IN (SELECT report_id FROM senate_financial_disclosures)
UNION ALL
SELECT 'Valid source_filing_id (links to house or senate)' AS check_type, COUNT(*) AS count
FROM congress_trading ct
WHERE ct.source_filing_id IS NOT NULL
  AND (ct.source_filing_id IN (SELECT filing_id FROM house_financial_disclosures)
       OR ct.source_filing_id IN (SELECT report_id FROM senate_financial_disclosures));

-- =============================================================================
-- SECTION 7: DATA COMPLETENESS OVER TIME
-- =============================================================================

SELECT '=== DATA COMPLETENESS OVER TIME ===' AS section;

-- House disclosures by year
SELECT 'House disclosures by year' AS data_type, year::text AS period, COUNT(*) AS count
FROM house_financial_disclosures
GROUP BY year
ORDER BY year DESC;

-- Senate disclosures by year
SELECT 'Senate disclosures by year' AS data_type, report_year::text AS period, COUNT(*) AS count
FROM senate_financial_disclosures
GROUP BY report_year
ORDER BY report_year DESC;

-- Congress trading by year
SELECT 'Congress trading by year' AS data_type, EXTRACT(YEAR FROM transaction_date)::text AS period, COUNT(*) AS count
FROM congress_trading
WHERE transaction_date IS NOT NULL
GROUP BY EXTRACT(YEAR FROM transaction_date)
ORDER BY EXTRACT(YEAR FROM transaction_date) DESC;

-- Politician financial summary by year
SELECT 'Politician summary by year' AS data_type, year::text AS period, COUNT(*) AS count
FROM politician_financial_summary
GROUP BY year
ORDER BY year DESC;

-- =============================================================================
-- SECTION 8: SOURCE TRACKING VALIDATION
-- =============================================================================

SELECT '=== SOURCE TRACKING VALIDATION ===' AS section;

-- Check source_filing_id completeness
SELECT 'congress_trading source_filing_id NULL' AS check_type,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS pct
FROM congress_trading WHERE source_filing_id IS NULL
UNION ALL
SELECT 'congress_trading source_page_number NULL' AS check_type,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS pct
FROM congress_trading WHERE source_page_number IS NULL
UNION ALL
SELECT 'congress_trading source_row_hash NULL' AS check_type,
       COUNT(*) AS count,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM congress_trading), 2) AS pct
FROM congress_trading WHERE source_row_hash IS NULL;

-- Check for duplicate source_row_hash (should be unique where not NULL)
SELECT 'Duplicate source_row_hash' AS check_type,
       source_row_hash, COUNT(*) AS dup_count
FROM congress_trading
WHERE source_row_hash IS NOT NULL
GROUP BY source_row_hash
HAVING COUNT(*) > 1
LIMIT 10;

-- =============================================================================
-- SECTION 9: ASSET TYPE AND TRANSACTION TYPE VALIDATION
-- =============================================================================

SELECT '=== ASSET & TRANSACTION TYPE VALIDATION ===' AS section;

-- Asset type distribution
SELECT 'Asset type distribution' AS check_type, asset_type, COUNT(*) AS count
FROM congress_trading
WHERE asset_type IS NOT NULL
GROUP BY asset_type
ORDER BY count DESC
LIMIT 20;

-- Transaction type distribution
SELECT 'Transaction type distribution' AS check_type, transaction_type, COUNT(*) AS count
FROM congress_trading
WHERE transaction_type IS NOT NULL
GROUP BY transaction_type
ORDER BY count DESC
LIMIT 20;

-- =============================================================================
-- SECTION 10: SUMMARY STATISTICS
-- =============================================================================

SELECT '=== SUMMARY STATISTICS ===' AS section;

-- Total transaction value (using amount_high as upper bound)
SELECT 'Total estimated value (congress_trading, amount_high sum)' AS stat,
       SUM(amount_high) AS total_value
FROM congress_trading
WHERE amount_high IS NOT NULL
UNION ALL
SELECT 'Average transaction value (amount_high avg)' AS stat,
       AVG(amount_high) AS total_value
FROM congress_trading
WHERE amount_high IS NOT NULL
UNION ALL
SELECT 'Max single transaction (amount_high max)' AS stat,
       MAX(amount_high) AS total_value
FROM congress_trading;

-- Net worth statistics from politician_financial_summary
SELECT 'Average net worth high (politician_financial_summary)' AS stat,
       AVG(net_worth_high) AS avg_value
FROM politician_financial_summary
WHERE net_worth_high IS NOT NULL
UNION ALL
SELECT 'Max net worth high (politician_financial_summary)' AS stat,
       MAX(net_worth_high) AS max_value
FROM politician_financial_summary
UNION ALL
SELECT 'Min net worth low (politician_financial_summary)' AS stat,
       MIN(net_worth_low) AS min_value
FROM politician_financial_summary
WHERE net_worth_low IS NOT NULL;

-- =============================================================================
-- END OF VALIDATION SCRIPT
-- =============================================================================
SELECT '=== VALIDATION COMPLETE ===' AS result;
