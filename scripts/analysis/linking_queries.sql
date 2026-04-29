-- ============================================================================
-- LINKING QUERIES: Connecting Financial Disclosures, Trading, FEC, and LDA
-- ============================================================================

-- ============================================================================
-- Query 1: Direct Stock Holdings + Trading Activity
-- Find politicians who traded stocks they held in previous period
-- ============================================================================
\echo 'Query 1: Trading Activity by Politician'
\echo '========================================'
SELECT
    ct.politician_name,
    ct.politician_state,
    ct.transaction_date,
    ct.asset_name,
    ct.transaction_type,
    ct.amount_text,
    COUNT(*) as trade_count
FROM congress_trading ct
WHERE ct.transaction_date >= '2020-01-01'
    AND ct.transaction_type IN ('p', 's', 'r', 'd')
GROUP BY ct.politician_name, ct.politician_state, ct.transaction_date,
         ct.asset_name, ct.transaction_type, ct.amount_text
ORDER BY trade_count DESC, ct.politician_name, ct.transaction_date
LIMIT 100;

-- ============================================================================
-- Query 2: FEC Contributions + Entity Resolution
-- Match campaign contributions to entities with financial disclosures
-- ============================================================================
\echo ''
\echo 'Query 2: Top Donors to Politicians with Financial Disclosures'
\echo '============================================================='
SELECT
    fec.name as donor_name,
    fec.state as donor_state,
    er.standardized_name as recipient_entity,
    er.entity_type as recipient_type,
    SUM(fec.transaction_amt) as total_donated,
    COUNT(*) as donation_count
FROM fec_individual_contributions fec
JOIN entity_raw_names ern ON ern.raw_name = fec.name
JOIN entity_resolutions er ON er.resolution_id = ern.resolution_id
WHERE fec.transaction_amt > 0
    AND fec.transaction_tp IN ('15', '15J', '15E')
    AND fec.cycle >= 2020
GROUP BY fec.name, fec.state, er.standardized_name, er.entity_type
HAVING SUM(fec.transaction_amt) > 5000
ORDER BY total_donated DESC
LIMIT 50;

-- ============================================================================
-- Query 3: LDA Lobbying + Entity Resolution
-- Find lobbying clients that match financial disclosure entities
-- ============================================================================
\echo ''
\echo 'Query 3: Lobbying Clients with Financial Disclosures'
\echo '====================================================='
SELECT
    lf.client_name,
    er.standardized_name as matched_entity,
    er.entity_type,
    er.state,
    COUNT(DISTINCT lf.filing_uuid) as filing_count,
    SUM(lf.income) as total_lobbying_income
FROM lda_filings lf
JOIN entity_raw_names ern ON ern.raw_name = lf.client_name
JOIN entity_resolutions er ON er.resolution_id = ern.resolution_id
WHERE lf.client_name IS NOT NULL AND lf.client_name != ''
GROUP BY lf.client_name, er.standardized_name, er.entity_type, er.state
ORDER BY total_lobbying_income DESC NULLS LAST
LIMIT 50;

-- ============================================================================
-- Query 4: Sector Concentration - Politicians with Holdings in Sector
-- ============================================================================
\echo ''
\echo 'Query 4: Politicians with Multiple Holdings in Same Sector'
\echo '=========================================================='
SELECT
    er.standardized_name as politician,
    er.state,
    ct.asset_name,
    ct.asset_type,
    COUNT(DISTINCT ct.id) as trade_count,
    COUNT(DISTINCT ct.transaction_date) as trading_days
FROM entity_resolutions er
JOIN entity_raw_names ern ON ern.resolution_id = er.resolution_id
JOIN congress_trading ct ON ct.politician_name = ern.raw_name
WHERE er.entity_type = 'politician'
    AND ct.transaction_date >= '2020-01-01'
GROUP BY er.standardized_name, er.state, ct.asset_name, ct.asset_type
HAVING COUNT(DISTINCT ct.id) >= 5
ORDER BY trade_count DESC, politician
LIMIT 100;

-- ============================================================================
-- Query 5: Temporal Correlation - Trading Around LDA Filings
-- ============================================================================
\echo ''
\echo 'Query 5: Trading Activity Around LDA Filing Dates'
\echo '=================================================='
SELECT
    ct.politician_name,
    ct.transaction_date,
    ct.asset_name,
    ct.transaction_type,
    lf.client_name,
    lf.signed_date as lda_date,
    ABS(ct.transaction_date - lf.signed_date) as days_diff
FROM congress_trading ct
JOIN lda_filings lf ON ct.politician_name = lf.client_name
WHERE ABS(ct.transaction_date - lf.signed_date) <= 180
    AND ct.transaction_date >= '2020-01-01'
    AND ct.transaction_type IN ('p', 's')
ORDER BY days_diff, ct.politician_name, ct.transaction_date
LIMIT 100;

-- ============================================================================
-- Query 6: Cross-Source Entity Matching
-- Find entities appearing in multiple data sources
-- ============================================================================
\echo ''
\echo 'Query 6: Entities Across Multiple Data Sources'
\echo '==============================================='
SELECT
    er.standardized_name,
    er.entity_type,
    er.state,
    er.source_count,
    er.unique_sources,
    COUNT(DISTINCT ern.source_table) as data_sources,
    STRING_AGG(DISTINCT ern.source_table, ', ' ORDER BY ern.source_table) as sources
FROM entity_resolutions er
JOIN entity_raw_names ern ON ern.resolution_id = er.resolution_id
GROUP BY er.resolution_id, er.standardized_name, er.entity_type, er.state,
         er.source_count, er.unique_sources
HAVING COUNT(DISTINCT ern.source_table) >= 2
ORDER BY data_sources DESC, source_count DESC
LIMIT 100;

-- ============================================================================
-- Query 7: FEC Contributions to Politicians by Sector
-- ============================================================================
\echo ''
\echo 'Query 7: FEC Contributions by Recipient and Sector'
\echo '==================================================='
SELECT
    fec.recipient_name,
    fec.state as recipient_state,
    fec.employer,
    fec.occupation,
    SUM(fec.transaction_amt) as total_donated,
    COUNT(*) as donation_count
FROM fec_individual_contributions fec
WHERE fec.transaction_amt > 0
    AND fec.transaction_tp IN ('15', '15J', '15E')
    AND fec.cycle >= 2020
    AND fec.employer IS NOT NULL
GROUP BY fec.recipient_name, fec.state, fec.employer, fec.occupation
HAVING SUM(fec.transaction_amt) > 10000
ORDER BY total_donated DESC
LIMIT 100;

-- ============================================================================
-- Query 8: Top Trading Politicians by Volume
-- ============================================================================
\echo ''
\echo 'Query 8: Top Trading Politicians (2020-2026)'
\echo '============================================='
SELECT
    ct.politician_name,
    ct.politician_state,
    ct.politician_party,
    COUNT(DISTINCT ct.id) as total_trades,
    COUNT(DISTINCT ct.asset_name) as unique_assets,
    COUNT(DISTINCT ct.transaction_date) as trading_days,
    SUM(CASE WHEN ct.transaction_type = 'p' THEN 1 ELSE 0 END) as purchases,
    SUM(CASE WHEN ct.transaction_type = 's' THEN 1 ELSE 0 END) as sales
FROM congress_trading ct
WHERE ct.transaction_date >= '2020-01-01'
GROUP BY ct.politician_name, ct.politician_state, ct.politician_party
ORDER BY total_trades DESC
LIMIT 50;

-- ============================================================================
-- Query 9: Entity Resolution Summary
-- ============================================================================
\echo ''
\echo 'Query 9: Entity Resolution Summary'
\echo '==================================='
SELECT
    er.entity_type,
    er.state,
    COUNT(*) as entity_count,
    AVG(er.source_count) as avg_sources,
    MAX(er.source_count) as max_sources,
    SUM(er.source_count) as total_mentions
FROM entity_resolutions er
GROUP BY er.entity_type, er.state
ORDER BY entity_count DESC, total_mentions DESC;

-- ============================================================================
-- Query 10: Potential Conflicts - Donors who are also Lobbying Clients
-- ============================================================================
\echo ''
\echo 'Query 10: Entities as Both Donors and Lobbying Clients'
\echo '======================================================='
SELECT
    er.standardized_name,
    er.entity_type,
    er.state,
    STRING_AGG(DISTINCT ern.source_table, ', ' ORDER BY ern.source_table) as data_sources,
    er.source_count
FROM entity_resolutions er
JOIN entity_raw_names ern ON ern.resolution_id = er.resolution_id
WHERE er.resolution_id IN (
    SELECT resolution_id
    FROM entity_raw_names
    WHERE source_table = 'fec_contribution'
    INTERSECT
    SELECT resolution_id
    FROM entity_raw_names
    WHERE source_table = 'lda_filing'
)
GROUP BY er.resolution_id, er.standardized_name, er.entity_type, er.state, er.source_count
ORDER BY er.source_count DESC;

\echo ''
\echo 'All linking queries complete!'
