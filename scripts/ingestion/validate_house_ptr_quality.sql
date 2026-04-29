-- House PTR financial disclosure OCR/transaction quality checks.
-- Usage:
--   PGPASSWORD=123qweasd psql -h localhost -U cbwinslow -d epstein \
--     -f scripts/ingestion/validate_house_ptr_quality.sql

\echo '1. Required field completeness'
SELECT COUNT(*) AS total_rows,
       COUNT(*) FILTER (WHERE politician_name IS NULL OR politician_name = '') AS missing_politician,
       COUNT(*) FILTER (WHERE asset_name IS NULL OR asset_name = '') AS missing_asset,
       COUNT(*) FILTER (WHERE transaction_type IS NULL OR transaction_type = '') AS missing_transaction_type,
       COUNT(*) FILTER (WHERE transaction_date IS NULL) AS missing_transaction_date,
       COUNT(*) FILTER (WHERE amount_text IS NULL OR amount_text = '') AS missing_amount_text,
       COUNT(*) FILTER (WHERE amount_low IS NULL) AS missing_amount_low,
       COUNT(*) FILTER (WHERE source_filing_id IS NULL OR source_filing_id = '') AS missing_source_filing,
       COUNT(*) FILTER (WHERE source_page_number IS NULL) AS missing_source_page,
       COUNT(*) FILTER (WHERE source_raw_text IS NULL OR source_raw_text = '') AS missing_source_raw_text
FROM congress_trading
WHERE data_source = 'House PTR OCR';

\echo '2. Identifier coverage'
SELECT COUNT(*) AS total_rows,
       COUNT(*) FILTER (WHERE ticker IS NOT NULL AND ticker <> '') AS rows_with_ticker,
       COUNT(*) FILTER (WHERE ticker IS NULL OR ticker = '') AS rows_without_ticker,
       COUNT(*) FILTER (WHERE asset_type IS NOT NULL AND asset_type <> '') AS rows_with_house_asset_type,
       COUNT(*) FILTER (WHERE ticker IS NOT NULL AND ticker !~ '^[A-Z][A-Z0-9.-]{0,9}$') AS suspicious_ticker_format,
       COUNT(DISTINCT ticker) FILTER (WHERE ticker IS NOT NULL AND ticker <> '') AS distinct_tickers,
       COUNT(DISTINCT asset_type) FILTER (WHERE asset_type IS NOT NULL AND asset_type <> '') AS distinct_house_asset_types,
       COUNT(DISTINCT asset_name) AS distinct_asset_names
FROM congress_trading
WHERE data_source = 'House PTR OCR';

\echo '3. House asset type distribution'
SELECT asset_type, COUNT(*) AS rows
FROM congress_trading
WHERE data_source = 'House PTR OCR'
  AND asset_type IS NOT NULL
GROUP BY asset_type
ORDER BY rows DESC, asset_type;

\echo '4. Amount disclosure type and aggregate range exposure'
SELECT CASE
           WHEN amount_text ~ '-' THEN 'range'
           WHEN amount_text ~ '\+' THEN 'open_ended_minimum'
           ELSE 'exact_or_single_value'
       END AS amount_kind,
       COUNT(*) AS rows,
       MIN(amount_low) AS min_amount_low,
       MAX(amount_high) AS max_amount_high,
       SUM(amount_low) AS aggregate_low_bound,
       SUM(COALESCE(amount_high, amount_low)) AS aggregate_high_bound
FROM congress_trading
WHERE data_source = 'House PTR OCR'
GROUP BY 1
ORDER BY rows DESC;

\echo '5. Date, amount, and duplicate sanity checks'
SELECT COUNT(*) FILTER (WHERE transaction_date < DATE '2000-01-01') AS transaction_before_2000,
       COUNT(*) FILTER (WHERE transaction_date > DATE '2026-12-31') AS transaction_after_2026,
       COUNT(*) FILTER (WHERE filing_date IS NOT NULL AND transaction_date > filing_date + INTERVAL '90 days') AS transaction_after_notice_plus_90_days,
       COUNT(*) FILTER (WHERE amount_low <= 0) AS nonpositive_low_amount,
       COUNT(*) FILTER (WHERE amount_high IS NOT NULL AND amount_high < amount_low) AS high_less_than_low,
       COUNT(*) FILTER (WHERE source_row_hash IS NULL) AS missing_source_hash,
       COUNT(*) - COUNT(DISTINCT source_row_hash) AS duplicate_source_hash_delta
FROM congress_trading
WHERE data_source = 'House PTR OCR';

\echo '6. Source traceability back to House metadata and OCR page'
SELECT COUNT(*) AS total_rows,
       COUNT(*) FILTER (WHERE h.filing_id IS NOT NULL) AS rows_joining_house_metadata,
       COUNT(*) FILTER (WHERE p.filing_id IS NOT NULL) AS rows_joining_ocr_page,
       COUNT(DISTINCT t.source_filing_id) AS source_filings,
       COUNT(DISTINCT t.source_filing_id || ':' || t.source_page_number) AS source_pages,
       COUNT(DISTINCT t.source_row_hash) AS unique_source_hashes
FROM congress_trading t
LEFT JOIN house_financial_disclosures h ON h.filing_id = t.source_filing_id
LEFT JOIN house_ptr_ocr_pages p
       ON p.filing_id = t.source_filing_id
      AND p.page_number = t.source_page_number
WHERE t.data_source = 'House PTR OCR';

\echo '7. Year-level OCR and parser coverage'
WITH ptr AS (
    SELECT year, COUNT(*) AS ptr_filings
    FROM house_financial_disclosures
    WHERE filing_type = 'P'
    GROUP BY year
),
ocr AS (
    SELECT year,
           COUNT(*) FILTER (WHERE status = 'complete') AS ocr_complete,
           COUNT(*) FILTER (WHERE status = 'error') AS ocr_errors
    FROM house_ptr_ocr_status
    GROUP BY year
),
txn_filings AS (
    SELECT year,
           COUNT(DISTINCT filing_id) AS transaction_ocr_filings
    FROM house_ptr_ocr_pages
    WHERE ocr_text ILIKE '%TRANSACTIONS%'
    GROUP BY year
),
parsed AS (
    SELECT h.year,
           COUNT(*) AS parsed_rows,
           COUNT(DISTINCT t.source_filing_id) AS parsed_filings,
           COUNT(*) FILTER (WHERE t.ticker IS NOT NULL AND t.ticker <> '') AS ticker_rows,
           COUNT(*) FILTER (WHERE t.asset_type IS NOT NULL AND t.asset_type <> '') AS asset_type_rows,
           COUNT(*) FILTER (WHERE t.amount_text ~ '-') AS range_amount_rows,
           COUNT(*) FILTER (WHERE t.amount_text !~ '-' AND t.amount_text !~ '\+') AS exact_amount_rows
    FROM congress_trading t
    JOIN house_financial_disclosures h ON h.filing_id = t.source_filing_id
    WHERE t.data_source = 'House PTR OCR'
    GROUP BY h.year
)
SELECT ptr.year,
       ptr.ptr_filings,
       COALESCE(ocr.ocr_complete, 0) AS ocr_complete,
       COALESCE(ocr.ocr_errors, 0) AS ocr_errors,
       COALESCE(txn_filings.transaction_ocr_filings, 0) AS transaction_ocr_filings,
       COALESCE(parsed.parsed_filings, 0) AS parsed_filings,
       COALESCE(parsed.parsed_rows, 0) AS parsed_rows,
       COALESCE(parsed.ticker_rows, 0) AS ticker_rows,
       COALESCE(parsed.asset_type_rows, 0) AS asset_type_rows,
       COALESCE(parsed.range_amount_rows, 0) AS range_amount_rows,
       COALESCE(parsed.exact_amount_rows, 0) AS exact_amount_rows,
       ROUND(COALESCE(parsed.parsed_filings, 0)::numeric / NULLIF(txn_filings.transaction_ocr_filings, 0) * 100, 1) AS parsed_pct_of_transaction_ocr_filings
FROM ptr
LEFT JOIN ocr USING (year)
LEFT JOIN txn_filings USING (year)
LEFT JOIN parsed USING (year)
WHERE ptr.year BETWEEN 2013 AND 2026
ORDER BY ptr.year;

\echo '8. Top politicians by aggregate disclosed high-bound exposure'
SELECT politician_name,
       COUNT(*) AS rows,
       COUNT(*) FILTER (WHERE ticker IS NOT NULL AND ticker <> '') AS ticker_rows,
       SUM(amount_low) AS aggregate_low_bound,
       SUM(COALESCE(amount_high, amount_low)) AS aggregate_high_bound,
       MIN(transaction_date) AS first_transaction_date,
       MAX(transaction_date) AS last_transaction_date
FROM congress_trading
WHERE data_source = 'House PTR OCR'
GROUP BY politician_name
ORDER BY aggregate_high_bound DESC NULLS LAST
LIMIT 25;

\echo '9. Review samples for suspicious dates or OCR noise'
SELECT h.year,
       t.politician_name,
       t.asset_name,
       t.ticker,
       t.asset_type,
       t.transaction_type,
       t.transaction_date,
       t.filing_date AS notification_date,
       t.amount_text,
       t.amount_low,
       t.amount_high,
       t.source_filing_id,
       t.source_page_number,
       t.source_raw_text
FROM congress_trading t
JOIN house_financial_disclosures h ON h.filing_id = t.source_filing_id
WHERE t.data_source = 'House PTR OCR'
  AND (
      (t.ticker IS NOT NULL AND t.ticker !~ '^[A-Z][A-Z0-9.-]{0,9}$')
      OR (t.filing_date IS NOT NULL AND t.transaction_date > t.filing_date + INTERVAL '90 days')
      OR t.asset_name ~ '[|]{2,}|__'
  )
ORDER BY h.year, t.politician_name
LIMIT 50;
