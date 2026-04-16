-- Cross-Reference Queries for Government Datasets
-- Links entities across FEC, Congress, Lobbying, FARA, White House, and more
-- April 13, 2026

-- =====================================================
-- 1. POLITICIAN ENTITY CROSS-REFERENCES
-- =====================================================

-- Find politicians who appear in multiple datasets
-- Links: Congress members -> FEC candidates -> Lobbying clients -> White House visitors
CREATE OR REPLACE VIEW cross_ref_politicians AS
SELECT 
    cm.bioguide_id,
    cm.first_name || ' ' || cm.last_name as politician_name,
    cm.state as congress_state,
    cm.party as congress_party,
    cm.chamber,
    -- FEC data
    fc.candidate_id as fec_candidate_id,
    fc.candidate_election_year as fec_election_year,
    fc.total_receipts as fec_total_receipts,
    -- Check if they have lobbying activity
    lr.registrant_name as lobbying_firm,
    lr.client_name as lobbying_client,
    lr.registration_date as lobbying_registered,
    -- Check White House visits
    wv.name as wh_visitor_name,
    wv.visitee_name as wh_meeting_with,
    wv.visit_date as wh_visit_date,
    -- Check FARA (if they or their firm is a foreign agent)
    fr.registrant_name as fara_registrant
FROM congress_members cm
LEFT JOIN fec_candidates fc ON 
    LOWER(cm.first_name || ' ' || cm.last_name) = LOWER(fc.candidate_name)
    OR LOWER(cm.last_name) = LOWER(SPLIT_PART(fc.candidate_name, ' ', -1))
LEFT JOIN lobbying_registrations lr ON 
    LOWER(cm.first_name || ' ' || cm.last_name) LIKE '%' || LOWER(lr.client_name) || '%'
    OR LOWER(lr.registrant_name) LIKE '%' || LOWER(cm.last_name) || '%'
LEFT JOIN whitehouse_visitors wv ON 
    LOWER(wv.name) LIKE '%' || LOWER(cm.last_name) || '%'
LEFT JOIN fara_registrations fr ON
    LOWER(fr.registrant_name) LIKE '%' || LOWER(cm.last_name) || '%'
WHERE fc.candidate_id IS NOT NULL 
   OR lr.registration_id IS NOT NULL 
   OR wv.id IS NOT NULL
   OR fr.id IS NOT NULL;

-- =====================================================
-- 2. LOBBYIST-CLIENT-FARA CONNECTIONS
-- =====================================================

-- Find lobbyists who also represent foreign principals
-- This is key for identifying foreign influence operations
CREATE OR REPLACE VIEW cross_ref_lobbyist_foreign_agents AS
SELECT DISTINCT
    lr.registrant_name as lobbying_firm,
    lr.client_name as lobbying_client,
    lr.registration_date,
    lr.termination_date as lobbying_termination,
    fr.registration_number as fara_registration,
    fr.foreign_principal as fara_principal,
    fr.foreign_principal_country as fara_country,
    fr.registration_date as fara_registration_date,
    -- Calculate overlap period
    CASE 
        WHEN lr.termination_date IS NULL OR fr.inactivation_date IS NULL 
        THEN 'Active overlap'
        WHEN lr.registration_date < fr.inactivation_date 
        THEN 'Historical overlap'
        ELSE 'No overlap'
    END as overlap_status
FROM lobbying_registrations lr
INNER JOIN fara_registrations fr ON
    -- Match by firm name (fuzzy matching)
    (
        LOWER(lr.registrant_name) = LOWER(fr.registrant_name)
        OR LOWER(lr.registrant_name) LIKE '%' || LOWER(SPLIT_PART(fr.registrant_name, ' ', 1)) || '%'
        OR SOUNDEX(lr.registrant_name) = SOUNDEX(fr.registrant_name)
    )
    AND (
        lr.termination_date IS NULL 
        OR fr.inactivation_date IS NULL
        OR lr.registration_date < fr.inactivation_date
    );

-- =====================================================
-- 3. CAMPAIGN FINANCE TO LOBBYING FLOW
-- =====================================================

-- Track money flow: Contributors -> Politicians -> Lobbying by same entities
CREATE OR REPLACE VIEW cross_ref_money_flow AS
WITH politician_lobbying AS (
    SELECT 
        cm.bioguide_id,
        cm.first_name || ' ' || cm.last_name as politician,
        lr.client_name as lobbying_client,
        lr.income_amount,
        lr.issues,
        lr.lobbying_activity_period_start,
        lr.lobbying_activity_period_end
    FROM congress_members cm
    INNER JOIN lobbying_quarterly_reports lr ON
        LOWER(lr.client_name) LIKE '%' || LOWER(cm.last_name) || '%'
),
campaign_contributions AS (
    SELECT 
        contributor_name,
        recipient_candidate_name,
        election_type,
        contribution_receipt_amount,
        contribution_receipt_date,
        committee_name
    FROM fec_contributions
    WHERE contribution_receipt_amount > 5000  -- Significant contributions
)
SELECT 
    cc.contributor_name,
    cc.recipient_candidate_name,
    cc.contribution_receipt_amount,
    cc.contribution_receipt_date,
    pl.lobbying_client,
    pl.income_amount as lobbying_spending,
    pl.issues as lobbied_issues,
    -- Flag if contributor also lobbies
    CASE 
        WHEN lr.client_id IS NOT NULL THEN 'Contributor is Lobbying Client'
        WHEN lr.registrant_id IS NOT NULL THEN 'Contributor is Lobbying Firm'
        ELSE 'No direct lobbying link'
    END as lobbying_link
FROM campaign_contributions cc
LEFT JOIN politician_lobbying pl ON
    LOWER(cc.recipient_candidate_name) = LOWER(pl.politician)
LEFT JOIN lobbying_registrations lr ON
    LOWER(cc.contributor_name) LIKE '%' || LOWER(lr.client_name) || '%'
ORDER BY cc.contribution_receipt_amount DESC;

-- =====================================================
-- 4. FOREIGN INFLENCE NETWORK ANALYSIS
-- =====================================================

-- Comprehensive view of foreign influence through multiple channels
CREATE OR REPLACE VIEW cross_ref_foreign_influence AS
SELECT 
    fp.principal_country as country,
    COUNT(DISTINCT fr.registration_number) as fara_registrations,
    COUNT(DISTINCT CASE WHEN lr.id IS NOT NULL THEN fr.registration_number END) as fara_with_lobbying,
    COUNT(DISTINCT CASE WHEN wv.id IS NOT NULL THEN fr.registration_number END) as fara_with_wh_visits,
    COUNT(DISTINCT lr.registrant_name) as linked_lobbying_firms,
    STRING_AGG(DISTINCT fp.principal_name, '; ') as foreign_principals,
    STRING_AGG(DISTINCT lr.registrant_name, '; ') as lobbying_firms,
    SUM(CASE WHEN lr.income_amount ~ '^[0-9.,]+$' 
        THEN REPLACE(REPLACE(lr.income_amount, ',', ''), '$', '')::numeric 
        ELSE 0 
    END) as total_lobbying_income
FROM fara_registrations fr
INNER JOIN fara_foreign_principals fp ON fr.registration_number = fp.registration_number
LEFT JOIN lobbying_registrations lr ON
    LOWER(lr.registrant_name) LIKE '%' || LOWER(fr.registrant_name) || '%'
LEFT JOIN whitehouse_visitors wv ON
    LOWER(wv.name) LIKE '%' || LOWER(fr.registrant_name) || '%'
    OR LOWER(wv.visitee_name) LIKE '%' || LOWER(fr.registrant_name) || '%'
GROUP BY fp.principal_country
ORDER BY COUNT(DISTINCT fr.registration_number) DESC;

-- =====================================================
-- 5. WHITE HOUSE VISITOR NETWORK ANALYSIS
-- =====================================================

-- Identify high-frequency visitors and their connections
CREATE OR REPLACE VIEW cross_ref_wh_visitor_network AS
WITH frequent_visitors AS (
    SELECT 
        name,
        COUNT(*) as visit_count,
        STRING_AGG(DISTINCT visitee_name, '; ') as met_with,
        MIN(visit_date) as first_visit,
        MAX(visit_date) as last_visit,
        STRING_AGG(DISTINCT description, '; ') as purposes
    FROM whitehouse_visitors
    WHERE name IS NOT NULL AND name != ''
    GROUP BY name
    HAVING COUNT(*) >= 5  -- At least 5 visits
)
SELECT 
    fv.name,
    fv.visit_count,
    fv.met_with,
    fv.first_visit,
    fv.last_visit,
    -- Check if visitor is a lobbyist
    lr.registrant_name as lobbying_firm,
    lr.client_name as lobbying_client,
    -- Check if visitor is a FARA registrant
    fr.registrant_name as fara_firm,
    fr.foreign_principal as represents,
    -- Check if visitor is a campaign contributor
    fc.contributor_name as fec_contributor,
    SUM(fc.contribution_receipt_amount) as total_contributed,
    -- Check if visitor is a federal contractor
    usa.recipient_name as contract_recipient,
    SUM(usa.federal_action_obligation) as total_contracts
FROM frequent_visitors fv
LEFT JOIN lobbying_registrations lr ON LOWER(fv.name) LIKE '%' || LOWER(lr.registrant_name) || '%'
LEFT JOIN fara_registrations fr ON LOWER(fv.name) LIKE '%' || LOWER(fr.registrant_name) || '%'
LEFT JOIN fec_contributions fc ON LOWER(fv.name) = LOWER(fc.contributor_name)
LEFT JOIN usa_spending_awards usa ON LOWER(fv.name) LIKE '%' || LOWER(usa.recipient_name) || '%'
GROUP BY fv.name, fv.visit_count, fv.met_with, fv.first_visit, fv.last_visit,
         lr.registrant_name, lr.client_name, fr.registrant_name, fr.foreign_principal,
         fc.contributor_name, usa.recipient_name
ORDER BY fv.visit_count DESC;

-- =====================================================
-- 6. SEC INSIDER TRADING - POLITICAL CONNECTIONS
-- =====================================================

-- Find SEC filings by politically connected executives
CREATE OR REPLACE VIEW cross_ref_sec_political AS
SELECT 
    sit.issuer_name as company,
    sit.issuer_ticker_symbol as ticker,
    sit.reporting_owner_name as insider_name,
    sit.transaction_date,
    sit.transaction_shares,
    sit.transaction_price_per_share,
    sit.transaction_acquired_disposed_code as buy_sell,
    -- Check if insider is connected to lobbying
    lr.client_name as lobbying_client,
    lr.issues as lobbied_issues,
    -- Check if company is a federal contractor
    usa.recipient_name as contractor_name,
    SUM(usa.federal_action_obligation) as contract_value,
    -- Check if company has FARA registration
    fr.registrant_name as fara_registrant
FROM sec_insider_transactions sit
LEFT JOIN lobbying_registrations lr ON
    LOWER(sit.issuer_name) LIKE '%' || LOWER(lr.client_name) || '%'
LEFT JOIN usa_spending_awards usa ON
    LOWER(sit.issuer_name) = LOWER(usa.recipient_name)
LEFT JOIN fara_registrations fr ON
    LOWER(sit.issuer_name) LIKE '%' || LOWER(fr.registrant_name) || '%'
WHERE sit.transaction_shares > 10000  -- Significant transactions only
GROUP BY sit.issuer_name, sit.issuer_ticker_symbol, sit.reporting_owner_name,
         sit.transaction_date, sit.transaction_shares, sit.transaction_price_per_share,
         sit.transaction_acquired_disposed_code, lr.client_name, lr.issues,
         usa.recipient_name, fr.registrant_name
ORDER BY sit.transaction_shares * sit.transaction_price_per_share DESC;

-- =====================================================
-- 7. BILL SPONSORSHIP - LOBBYING - CONTRIBUTIONS
-- =====================================================

-- Track bills from sponsorship through lobbying to passage
CREATE OR REPLACE VIEW cross_ref_bill_influence AS
SELECT 
    cb.bill_number,
    cb.title as bill_title,
    cb.introduced_date,
    cb.sponsor_name,
    cb.sponsor_party,
    cb.sponsor_state,
    cb.committees,
    cb.policy_area,
    -- Lobbying on this bill's issues
    lr.issues,
    lr.registrant_name as lobbying_firm,
    lr.client_name as lobbying_client,
    lr.income_amount,
    -- Sponsor's campaign finance
    fc.candidate_name,
    fc.total_receipts,
    fc.total_contributions,
    -- Committee members who received contributions from lobbying client
    cm2.first_name || ' ' || cm2.last_name as committee_member,
    cm2.party as committee_member_party
FROM congress_bills cb
LEFT JOIN lobbying_quarterly_reports lr ON
    LOWER(cb.policy_area) LIKE '%' || LOWER(lr.issues) || '%'
    OR LOWER(lr.specific_issues) LIKE '%' || LOWER(cb.bill_number) || '%'
LEFT JOIN fec_candidates fc ON
    LOWER(cb.sponsor_name) = LOWER(fc.candidate_name)
LEFT JOIN congress_members cm2 ON
    cb.committees LIKE '%' || cm2.last_name || '%'
WHERE cb.sponsor_name IS NOT NULL
ORDER BY cb.introduced_date DESC;

-- =====================================================
-- 8. ENTITY CONSOLIDATION VIEW
-- =====================================================

-- Master entity lookup across all datasets
CREATE OR REPLACE VIEW entity_master_lookup AS
-- Congress Members
SELECT 
    'congress_member' as entity_type,
    cm.bioguide_id as entity_id,
    cm.first_name || ' ' || cm.last_name as entity_name,
    cm.state as state,
    cm.party as party_affiliation,
    NULL as company,
    NULL as country,
    'Congress.gov' as source_dataset,
    cm.imported_at as last_seen
FROM congress_members cm
UNION ALL
-- FEC Candidates
SELECT 
    'fec_candidate' as entity_type,
    fc.candidate_id as entity_id,
    fc.candidate_name as entity_name,
    NULL as state,
    fc.candidate_party as party_affiliation,
    NULL as company,
    NULL as country,
    'FEC' as source_dataset,
    fc.imported_at as last_seen
FROM fec_candidates fc
UNION ALL
-- Lobbying Firms
SELECT 
    'lobbying_firm' as entity_type,
    lr.registrant_id as entity_id,
    lr.registrant_name as entity_name,
    lr.registrant_state as state,
    NULL as party_affiliation,
    NULL as company,
    NULL as country,
    'Lobbying Disclosure' as source_dataset,
    lr.imported_at as last_seen
FROM lobbying_registrations lr
UNION ALL
-- Lobbying Clients
SELECT 
    'lobbying_client' as entity_type,
    lr.client_id as entity_id,
    lr.client_name as entity_name,
    lr.client_state as state,
    NULL as party_affiliation,
    NULL as company,
    lr.client_country as country,
    'Lobbying Disclosure' as source_dataset,
    lr.imported_at as last_seen
FROM lobbying_registrations lr
WHERE lr.client_id IS NOT NULL
UNION ALL
-- FARA Registrants
SELECT 
    'fara_registrant' as entity_type,
    fr.registration_number as entity_id,
    fr.registrant_name as entity_name,
    NULL as state,
    NULL as party_affiliation,
    NULL as company,
    fr.registrant_country as country,
    'FARA' as source_dataset,
    fr.imported_at as last_seen
FROM fara_registrations fr
UNION ALL
-- FARA Foreign Principals
SELECT 
    'fara_foreign_principal' as entity_type,
    fp.id::text as entity_id,
    fp.principal_name as entity_name,
    NULL as state,
    NULL as party_affiliation,
    NULL as company,
    fp.principal_country as country,
    'FARA' as source_dataset,
    fp.imported_at as last_seen
FROM fara_foreign_principals fp
UNION ALL
-- SEC Companies
SELECT 
    'sec_company' as entity_type,
    sit.issuer_cik as entity_id,
    sit.issuer_name as entity_name,
    NULL as state,
    NULL as party_affiliation,
    sit.issuer_name as company,
    NULL as country,
    'SEC EDGAR' as source_dataset,
    sit.imported_at as last_seen
FROM sec_insider_transactions sit
GROUP BY sit.issuer_cik, sit.issuer_name, sit.imported_at;

-- =====================================================
-- 9. DEGREES OF SEPARATION QUERY
-- =====================================================

-- Find connections between any two entities through intermediaries
CREATE OR REPLACE FUNCTION find_entity_connections(
    entity_name_1 TEXT,
    entity_name_2 TEXT
) RETURNS TABLE (
    path TEXT,
    connection_type TEXT,
    details TEXT
) AS $$
BEGIN
    RETURN QUERY
    
    -- Direct connections (same person)
    SELECT 
        entity_name_1 || ' <-> ' || entity_name_2,
        'Direct Match',
        'Names match directly or partially'
    WHERE LOWER(entity_name_1) = LOWER(entity_name_2)
       OR LOWER(entity_name_1) LIKE '%' || LOWER(entity_name_2) || '%'
       OR LOWER(entity_name_2) LIKE '%' || LOWER(entity_name_1) || '%'
    
    UNION ALL
    
    -- Connection through lobbying (entity1 lobbies for entity2)
    SELECT 
        entity_name_1 || ' -> (lobbies for) -> ' || entity_name_2,
        'Lobbying Relationship',
        lr.registrant_name || ' lobbies for ' || lr.client_name
    FROM lobbying_registrations lr
    WHERE (LOWER(lr.registrant_name) LIKE '%' || LOWER(entity_name_1) || '%'
           AND LOWER(lr.client_name) LIKE '%' || LOWER(entity_name_2) || '%')
       OR (LOWER(lr.registrant_name) LIKE '%' || LOWER(entity_name_2) || '%'
           AND LOWER(lr.client_name) LIKE '%' || LOWER(entity_name_1) || '%')
    
    UNION ALL
    
    -- Connection through FARA (entity1 represents entity2's foreign principal)
    SELECT 
        entity_name_1 || ' -> (represents) -> ' || entity_name_2,
        'FARA Representation',
        fr.registrant_name || ' represents ' || fr.foreign_principal
    FROM fara_registrations fr
    WHERE (LOWER(fr.registrant_name) LIKE '%' || LOWER(entity_name_1) || '%'
           AND LOWER(fr.foreign_principal) LIKE '%' || LOWER(entity_name_2) || '%')
       OR (LOWER(fr.registrant_name) LIKE '%' || LOWER(entity_name_2) || '%'
           AND LOWER(fr.foreign_principal) LIKE '%' || LOWER(entity_name_1) || '%')
    
    UNION ALL
    
    -- Connection through campaign finance (entity1 contributes to entity2)
    SELECT 
        entity_name_1 || ' -> (contributes to) -> ' || entity_name_2,
        'Campaign Finance',
        fc.contributor_name || ' contributed $' || fc.contribution_receipt_amount || ' to ' || fc.recipient_candidate_name
    FROM fec_contributions fc
    WHERE (LOWER(fc.contributor_name) LIKE '%' || LOWER(entity_name_1) || '%'
           AND LOWER(fc.recipient_candidate_name) LIKE '%' || LOWER(entity_name_2) || '%')
       OR (LOWER(fc.contributor_name) LIKE '%' || LOWER(entity_name_2) || '%'
           AND LOWER(fc.recipient_candidate_name) LIKE '%' || LOWER(entity_name_1) || '%');
           
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- 10. DAILY SUMMARY STATISTICS
-- =====================================================

-- Generate daily summary of cross-dataset activity
CREATE OR REPLACE VIEW cross_ref_daily_summary AS
SELECT 
    CURRENT_DATE as report_date,
    (SELECT COUNT(*) FROM congress_members WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_congress_members,
    (SELECT COUNT(*) FROM congress_bills WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_bills,
    (SELECT COUNT(*) FROM lobbying_registrations WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_lobbying_registrations,
    (SELECT COUNT(*) FROM lobbying_quarterly_reports WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_lobbying_reports,
    (SELECT COUNT(*) FROM fara_registrations WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_fara_registrations,
    (SELECT COUNT(*) FROM whitehouse_visitors WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_wh_visits,
    (SELECT COUNT(*) FROM sec_insider_transactions WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_sec_filings,
    (SELECT COUNT(*) FROM fec_contributions WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_fec_contributions,
    (SELECT COUNT(*) FROM usa_spending_awards WHERE imported_at > CURRENT_DATE - INTERVAL '1 day') as new_contracts;

-- =====================================================
-- USAGE EXAMPLES
-- =====================================================

-- Example 1: Find all foreign influence on a specific politician
-- SELECT * FROM cross_ref_politicians WHERE politician_name LIKE '%Schumer%';

-- Example 2: Find lobbyists who also represent foreign governments
-- SELECT * FROM cross_ref_lobbyist_foreign_agents WHERE fara_country = 'Saudi Arabia';

-- Example 3: Track money from specific contributor to lobbying
-- SELECT * FROM cross_ref_money_flow WHERE contributor_name LIKE '%Bloomberg%';

-- Example 4: Find connections between two entities
-- SELECT * FROM find_entity_connections('Goldman Sachs', 'Biden');

-- Example 5: Get daily activity summary
-- SELECT * FROM cross_ref_daily_summary;
