-- ============================================================================
-- EPSTEIN FILES DATABASE VALIDATION VIEWS - CORRECTED
-- Enterprise-grade data quality and cross-reference validation
-- Created: April 4, 2026
-- ============================================================================

-- ----------------------------------------------------------------------------
-- VIEW 1: Dataset Completeness Summary
-- Shows row counts and completeness percentages for all major tables
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_dataset_completeness AS
SELECT 
    'Core Documents' as category,
    'documents' as table_name,
    COUNT(*) as row_count,
    1397821 as expected_count,
    ROUND(COUNT(*) * 100.0 / 1397821, 2) as completeness_pct,
    'DOJ EFTA documents' as description
FROM documents
UNION ALL
SELECT 
    'Core Documents',
    'pages',
    COUNT(*),
    2892730,
    ROUND(COUNT(*) * 100.0 / 2892730, 2),
    'OCR text pages with FTS'
FROM pages
UNION ALL
SELECT 
    'Emails',
    'jmail_emails_full',
    COUNT(*),
    1783792,
    ROUND(COUNT(*) * 100.0 / 1783792, 2),
    'jMail world emails'
FROM jmail_emails_full
UNION ALL
SELECT 
    'Emails',
    'jmail_documents',
    COUNT(*),
    1413417,
    ROUND(COUNT(*) * 100.0 / 1413417, 2),
    'jMail world documents'
FROM jmail_documents
UNION ALL
SELECT 
    'ICIJ Offshore Leaks',
    'icij_entities',
    COUNT(*),
    814616,
    ROUND(COUNT(*) * 100.0 / 814616, 2),
    'Offshore companies/entities'
FROM icij_entities
UNION ALL
SELECT 
    'ICIJ Offshore Leaks',
    'icij_officers',
    COUNT(*),
    771368,
    ROUND(COUNT(*) * 100.0 / 771368, 2),
    'ICIJ officers/people'
FROM icij_officers
UNION ALL
SELECT 
    'ICIJ Offshore Leaks',
    'icij_relationships',
    COUNT(*),
    3339271,
    ROUND(COUNT(*) * 100.0 / 3339271, 2),
    'Entity relationships'
FROM icij_relationships
UNION ALL
SELECT 
    'Financial',
    'fec_individual_contributions',
    COUNT(*),
    5420940,
    ROUND(COUNT(*) * 100.0 / 5420940, 2),
    'FEC individual donations'
FROM fec_individual_contributions
UNION ALL
SELECT 
    'Entity Extraction',
    'document_entities',
    COUNT(*),
    5709659,
    ROUND(COUNT(*) * 100.0 / 5709659, 2),
    'NER-extracted entities'
FROM document_entities
UNION ALL
SELECT 
    'Knowledge Graph',
    'entities',
    COUNT(*),
    606,
    ROUND(COUNT(*) * 100.0 / 606, 2),
    'Curated KG entities'
FROM entities
UNION ALL
SELECT 
    'Knowledge Graph',
    'relationships',
    COUNT(*),
    2302,
    ROUND(COUNT(*) * 100.0 / 2302, 2),
    'Curated KG relationships'
FROM relationships
UNION ALL
SELECT 
    'Redactions',
    'redactions',
    COUNT(*),
    2587102,
    ROUND(COUNT(*) * 100.0 / 2587102, 2),
    'Redacted sections'
FROM redactions
ORDER BY category, table_name;

COMMENT ON VIEW v_dataset_completeness IS 'Summary of all major datasets with completeness percentages';

-- ----------------------------------------------------------------------------
-- VIEW 2: Cross-Dataset Person Validation
-- Validates persons exist across multiple sources
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_person_cross_reference AS
WITH all_persons AS (
    -- From exposed_persons (epsteinexposed.com)
    SELECT 
        name,
        'exposed_persons' as source,
        id as source_id,
        jsonb_build_object(
            'category', category,
            'aliases', aliases,
            'connected_to', connected_to
        ) as metadata
    FROM exposed_persons
    
    UNION ALL
    
    -- From ICIJ officers
    SELECT 
        name,
        'icij_officers' as source,
        node_id::text as source_id,
        jsonb_build_object(
            'countries', countries,
            'country_codes', country_codes
        ) as metadata
    FROM icij_officers
    WHERE name IS NOT NULL
    
    UNION ALL
    
    -- From jMail email senders (top 100 by volume)
    SELECT 
        sender as name,
        'jmail_emails' as source,
        COUNT(*)::text as source_id,
        jsonb_build_object(
            'email_count', COUNT(*),
            'first_seen', MIN(sent_at),
            'last_seen', MAX(sent_at)
        ) as metadata
    FROM jmail_emails_full
    WHERE sender IS NOT NULL
    GROUP BY sender
    ORDER BY COUNT(*) DESC
    LIMIT 100
)
SELECT 
    name,
    COUNT(DISTINCT source) as source_count,
    array_agg(DISTINCT source) as sources,
    jsonb_object_agg(source, metadata) as combined_metadata
FROM all_persons
GROUP BY name
HAVING COUNT(DISTINCT source) > 1
ORDER BY source_count DESC, name;

COMMENT ON VIEW v_person_cross_reference IS 'Persons appearing in multiple data sources (ICIJ, jMail, epsteinexposed.com)';

-- ----------------------------------------------------------------------------
-- VIEW 3: Data Quality - Orphaned Records Check
-- Finds records without proper parent/child relationships
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_orphaned_records AS
-- Document entities referencing non-existent documents
SELECT 
    'document_entities' as table_name,
    'missing_document' as issue_type,
    COUNT(*) as orphan_count,
    'Entities referencing non-existent documents' as description
FROM document_entities de
LEFT JOIN documents d ON de.document_id = d.id
WHERE d.id IS NULL

UNION ALL

-- Emails without file registry entries
SELECT 
    'jmail_emails_full',
    'missing_file_registry',
    COUNT(*),
    'Emails without corresponding file registry entries'
FROM jmail_emails_full je
LEFT JOIN file_registry fr ON je.doc_id = fr.efta_number
WHERE fr.id IS NULL AND je.doc_id IS NOT NULL

UNION ALL

-- ICIJ relationships with missing start entities
SELECT 
    'icij_relationships',
    'missing_start_entity',
    COUNT(*),
    'Relationships referencing non-existent start entities'
FROM icij_relationships ir
LEFT JOIN icij_entities ie ON ir.node_id_start = ie.node_id
WHERE ie.node_id IS NULL;

COMMENT ON VIEW v_orphaned_records IS 'Data integrity check for orphaned/orphaned records';

-- ----------------------------------------------------------------------------
-- VIEW 4: Index Health Check
-- Shows all indexes and their usage statistics
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_index_health AS
SELECT 
    schemaname,
    relname as tablename,
    indexrelname as indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
    idx_scan as index_scans,
    idx_tup_read as tuples_read,
    idx_tup_fetch as tuples_fetched
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

COMMENT ON VIEW v_index_health IS 'Index usage statistics for performance monitoring';

-- ----------------------------------------------------------------------------
-- VIEW 5: Table Storage Statistics
-- Shows storage usage per table
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_table_storage AS
SELECT 
    schemaname,
    relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size,
    pg_size_pretty(pg_relation_size(relid)) as table_size,
    pg_size_pretty(pg_indexes_size(relid)) as indexes_size,
    n_live_tup as live_tuples,
    n_dead_tup as dead_tuples,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(relid) DESC;

COMMENT ON VIEW v_table_storage IS 'Storage statistics and vacuum status for all tables';

-- ----------------------------------------------------------------------------
-- VIEW 6: jMail Email Pattern Analysis
-- Analyzes email communication patterns
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_jmail_email_patterns AS
SELECT 
    sender,
    COUNT(*) as email_count,
    COUNT(DISTINCT email_drop_id) as unique_drops,
    COUNT(DISTINCT release_batch) as batches,
    MIN(sent_at) as first_email,
    MAX(sent_at) as last_email,
    ROUND(COUNT(*) FILTER (WHERE epstein_is_sender = true) * 100.0 / COUNT(*), 2) as epstein_sender_pct,
    SUM(LENGTH(COALESCE(subject, ''))) as total_subject_length,
    AVG(LENGTH(COALESCE(subject, ''))) as avg_subject_length
FROM jmail_emails_full
WHERE sender IS NOT NULL
GROUP BY sender
ORDER BY email_count DESC;

COMMENT ON VIEW v_jmail_email_patterns IS 'Email communication patterns and statistics by sender';

-- ----------------------------------------------------------------------------
-- VIEW 7: FEC Contribution Analysis - Top Donors
-- Cross-reference FEC data with Epstein entities
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_fec_top_donors AS
SELECT 
    name,
    employer,
    occupation,
    COUNT(*) as contribution_count,
    SUM(transaction_amt) as total_amount,
    MIN(transaction_dt) as first_donation,
    MAX(transaction_dt) as last_donation,
    array_agg(DISTINCT cmte_id) as committees
FROM fec_individual_contributions
WHERE name IS NOT NULL
GROUP BY name, employer, occupation
HAVING SUM(transaction_amt) > 10000
ORDER BY total_amount DESC
LIMIT 1000;

COMMENT ON VIEW v_fec_top_donors IS 'Top 1000 FEC donors by total contribution amount';

-- ----------------------------------------------------------------------------
-- VIEW 8: Document Coverage Analysis
-- Shows document coverage across different sources
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_document_coverage AS
WITH doc_sources AS (
    SELECT 
        d.id,
        d.efta_number,
        d.dataset_id,
        CASE 
            WHEN p.id IS NOT NULL THEN true 
            ELSE false 
        END as has_pages,
        CASE 
            WHEN dc.id IS NOT NULL THEN true 
            ELSE false 
        END as has_classification,
        CASE 
            WHEN de.cnt > 0 THEN true 
            ELSE false 
        END as has_entities,
        CASE 
            WHEN r.cnt > 0 THEN true 
            ELSE false 
        END as has_redactions
    FROM documents d
    LEFT JOIN pages p ON d.efta_number = p.efta_number
    LEFT JOIN document_classification dc ON d.id = dc.document_id
    LEFT JOIN (SELECT document_id, COUNT(*) as cnt FROM document_entities GROUP BY document_id) de ON d.id = de.document_id
    LEFT JOIN (SELECT document_id, COUNT(*) as cnt FROM redactions GROUP BY document_id) r ON d.id = r.document_id
)
SELECT 
    dataset_id,
    COUNT(*) as total_docs,
    COUNT(*) FILTER (WHERE has_pages) as with_pages,
    COUNT(*) FILTER (WHERE has_classification) as with_classification,
    COUNT(*) FILTER (WHERE has_entities) as with_entities,
    COUNT(*) FILTER (WHERE has_redactions) as with_redactions,
    COUNT(*) FILTER (WHERE has_pages AND has_classification AND has_entities) as fully_enriched,
    ROUND(COUNT(*) FILTER (WHERE has_pages) * 100.0 / COUNT(*), 2) as pages_pct,
    ROUND(COUNT(*) FILTER (WHERE fully_enriched) * 100.0 / COUNT(*), 2) as fully_enriched_pct
FROM doc_sources
GROUP BY dataset_id
ORDER BY dataset_id;

COMMENT ON VIEW v_document_coverage IS 'Document enrichment coverage by dataset source';

-- ----------------------------------------------------------------------------
-- VIEW 9: Entity Co-occurrence Network
-- Shows entity co-occurrences across documents for network analysis
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_entity_cooccurrence AS
SELECT 
    de1.entity_text as entity_1,
    de1.entity_type as entity_1_type,
    de2.entity_text as entity_2,
    de2.entity_type as entity_2_type,
    COUNT(DISTINCT de1.document_id) as cooccurrence_count,
    array_agg(DISTINCT de1.document_id) as document_ids
FROM document_entities de1
INNER JOIN document_entities de2 
    ON de1.document_id = de2.document_id 
    AND de1.entity_text < de2.entity_text
WHERE de1.entity_type IN ('PERSON', 'ORGANIZATION')
    AND de2.entity_type IN ('PERSON', 'ORGANIZATION')
GROUP BY de1.entity_text, de1.entity_type, de2.entity_text, de2.entity_type
HAVING COUNT(DISTINCT de1.document_id) >= 5
ORDER BY cooccurrence_count DESC;

COMMENT ON VIEW v_entity_cooccurrence IS 'Entity co-occurrence network (5+ documents) for relationship analysis';

-- ----------------------------------------------------------------------------
-- VIEW 10: ICIJ Cross-Reference Analysis
-- Shows ICIJ officers potentially connected to Epstein network
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW v_icij_epstein_crossref AS
SELECT 
    io.name as icij_officer_name,
    io.countries as icij_countries,
    io.country_codes as icij_country_codes,
    ep.name as exposed_person_name,
    ep.category as exposed_category,
    ep.aliases as exposed_aliases,
    similarity(lower(io.name), lower(ep.name)) as name_similarity
FROM icij_officers io
LEFT JOIN exposed_persons ep 
    ON lower(io.name) ILIKE '%' || lower(ep.name) || '%'
    OR lower(ep.name) ILIKE '%' || lower(io.name) || '%'
WHERE ep.name IS NOT NULL
ORDER BY name_similarity DESC
LIMIT 500;

COMMENT ON VIEW v_icij_epstein_crossref IS 'Potential connections between ICIJ officers and Epstein network persons';

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================
GRANT SELECT ON ALL TABLES IN SCHEMA public TO cbwinslow;

-- ============================================================================
-- DOCUMENTATION
-- ============================================================================
COMMENT ON SCHEMA public IS 'Epstein Files Analysis Database - Enterprise Edition. Contains 44+ tables with 15M+ rows covering DOJ documents, emails, offshore leaks, FEC data, and knowledge graphs.';
