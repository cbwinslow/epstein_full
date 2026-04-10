-- =============================================================================
-- Data Quality Views and Functions for Epstein Project
-- =============================================================================
-- These views and functions provide automated data quality checks,
-- cross-validation, and integrity monitoring.

-- =============================================================================
-- VIEW: Data Quality Overview
-- Shows summary statistics for all tables
-- =============================================================================
CREATE OR REPLACE VIEW data_quality_overview AS
SELECT 
    schemaname,
    relname AS table_name,
    n_live_tup AS row_count,
    n_dead_tup AS dead_rows,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;

-- =============================================================================
-- VIEW: Orphaned Records - Foreign Key Violations
-- =============================================================================
CREATE OR REPLACE VIEW orphaned_records AS

-- Orphaned relationships (source_entity_id)
SELECT 
    'relationships.source_entity_id' AS reference_column,
    'entities.id' AS parent_column,
    COUNT(*) AS orphan_count,
    MIN(r.id) AS sample_orphan_id
FROM relationships r
LEFT JOIN entities e ON r.source_entity_id = e.id
WHERE e.id IS NULL AND r.source_entity_id IS NOT NULL

UNION ALL

-- Orphaned relationships (target_entity_id)
SELECT 
    'relationships.target_entity_id',
    'entities.id',
    COUNT(*),
    MIN(r.id)
FROM relationships r
LEFT JOIN entities e ON r.target_entity_id = e.id
WHERE e.id IS NULL AND r.target_entity_id IS NOT NULL

UNION ALL

-- Orphaned rider_clauses
SELECT 
    'rider_clauses.subpoena_id',
    'subpoenas.id',
    COUNT(*),
    MIN(rc.id)
FROM rider_clauses rc
LEFT JOIN subpoenas s ON rc.subpoena_id = s.id
WHERE s.id IS NULL AND rc.subpoena_id IS NOT NULL

UNION ALL

-- Orphaned email_participants
SELECT 
    'email_participants.email_id',
    'emails.id',
    COUNT(*),
    MIN(ep.id)
FROM email_participants ep
LEFT JOIN emails e ON ep.email_id = e.id
WHERE e.id IS NULL AND ep.email_id IS NOT NULL

UNION ALL

-- Orphaned pages
SELECT 
    'pages.efta_number',
    'documents.efta_number',
    COUNT(*),
    MIN(p.id)
FROM pages p
LEFT JOIN documents d ON p.efta_number = d.efta_number
WHERE d.efta_number IS NULL AND p.efta_number IS NOT NULL;

-- =============================================================================
-- VIEW: Duplicate Detection
-- =============================================================================
CREATE OR REPLACE VIEW duplicate_detection AS

-- Duplicate documents by efta_number
SELECT 
    'documents' AS table_name,
    'efta_number' AS duplicate_columns,
    efta_number AS duplicate_value,
    COUNT(*) AS duplicate_count
FROM documents
WHERE efta_number IS NOT NULL
GROUP BY efta_number
HAVING COUNT(*) > 1

UNION ALL

-- Duplicate entities by name+type
SELECT 
    'entities',
    'name, entity_type',
    name || ' (' || entity_type || ')',
    COUNT(*)
FROM entities
WHERE name IS NOT NULL
GROUP BY name, entity_type
HAVING COUNT(*) > 1

UNION ALL

-- Duplicate emails
SELECT 
    'emails',
    'efta_number, subject',
    efta_number || ' - ' || LEFT(subject, 50),
    COUNT(*)
FROM emails
WHERE efta_number IS NOT NULL
GROUP BY efta_number, subject
HAVING COUNT(*) > 1;

-- =============================================================================
-- VIEW: Data Completeness by Table
-- =============================================================================
CREATE OR REPLACE VIEW data_completeness AS

-- Documents completeness
SELECT 
    'documents' AS table_name,
    COUNT(*) AS total_rows,
    COUNT(efta_number) AS has_efta,
    COUNT(title) AS has_title,
    COUNT(document_date) AS has_date,
    COUNT(content) AS has_content,
    ROUND(COUNT(title) * 100.0 / COUNT(*), 2) AS title_completeness_pct
FROM documents

UNION ALL

-- Entities completeness
SELECT 
    'entities',
    COUNT(*),
    COUNT(name),
    COUNT(entity_type),
    COUNT(description),
    NULL,
    ROUND(COUNT(name) * 100.0 / COUNT(*), 2)
FROM entities

UNION ALL

-- Relationships completeness
SELECT 
    'relationships',
    COUNT(*),
    COUNT(source_entity_id),
    COUNT(target_entity_id),
    COUNT(relationship_type),
    COUNT(evidence),
    ROUND(COUNT(source_entity_id) * 100.0 / COUNT(*), 2)
FROM relationships

UNION ALL

-- Emails completeness
SELECT 
    'emails',
    COUNT(*),
    COUNT(efta_number),
    COUNT(from_address),
    COUNT(subject),
    COUNT(body),
    ROUND(COUNT(subject) * 100.0 / COUNT(*), 2)
FROM emails;

-- =============================================================================
-- VIEW: Document Processing Status
-- =============================================================================
CREATE OR REPLACE VIEW document_processing_status AS
SELECT 
    d.efta_number,
    d.title,
    CASE 
        WHEN o.ocr_text IS NOT NULL THEN 'OCR_COMPLETE'
        ELSE 'OCR_PENDING'
    END AS ocr_status,
    CASE 
        WHEN dc.classification IS NOT NULL THEN 'CLASSIFIED'
        ELSE 'UNCLASSIFIED'
    END AS classification_status,
    CASE 
        WHEN de.entity_count > 0 THEN 'ENTITIES_EXTRACTED'
        WHEN de.entity_count = 0 THEN 'NO_ENTITIES'
        ELSE 'NOT_PROCESSED'
    END AS entity_extraction_status,
    CASE 
        WHEN r.redaction_count > 0 THEN 'REDACTIONS_FOUND'
        WHEN r.redaction_count = 0 THEN 'NO_REDACTIONS'
        ELSE 'NOT_ANALYZED'
    END AS redaction_status,
    ds.summary IS NOT NULL AS has_summary
FROM documents d
LEFT JOIN ocr_results o ON d.efta_number = o.efta_number
LEFT JOIN document_classification dc ON d.efta_number = dc.efta_number
LEFT JOIN (
    SELECT efta_number, COUNT(*) AS entity_count 
    FROM document_entities 
    GROUP BY efta_number
) de ON d.efta_number = de.efta_number
LEFT JOIN (
    SELECT efta_number, COUNT(*) AS redaction_count 
    FROM redactions 
    GROUP BY efta_number
) r ON d.efta_number = r.efta_number
LEFT JOIN document_summary ds ON d.efta_number = ds.efta_number;

-- =============================================================================
-- FUNCTION: Run Full Data Quality Check
-- =============================================================================
CREATE OR REPLACE FUNCTION run_data_quality_check()
RETURNS TABLE (
    check_type TEXT,
    check_name TEXT,
    status TEXT,
    details TEXT,
    severity TEXT
) AS $$
BEGIN
    -- Foreign Key Integrity
    RETURN QUERY
    SELECT 
        'FK Integrity'::TEXT,
        reference_column::TEXT,
        CASE WHEN orphan_count = 0 THEN 'PASS' ELSE 'FAIL' END,
        orphan_count::TEXT || ' orphaned records',
        CASE WHEN orphan_count = 0 THEN 'INFO' ELSE 'HIGH' END
    FROM orphaned_records;
    
    -- Duplicate Detection
    RETURN QUERY
    SELECT 
        'Duplicates'::TEXT,
        table_name::TEXT || ' (' || duplicate_columns::TEXT || ')',
        'WARNING',
        duplicate_count::TEXT || ' duplicates of ' || duplicate_value::TEXT,
        'MEDIUM'
    FROM duplicate_detection
    WHERE duplicate_count > 1;
    
    -- Completeness Checks
    RETURN QUERY
    SELECT 
        'Completeness'::TEXT,
        table_name::TEXT,
        CASE 
            WHEN title_completeness_pct >= 95 THEN 'PASS'
            WHEN title_completeness_pct >= 80 THEN 'WARNING'
            ELSE 'FAIL'
        END,
        title_completeness_pct::TEXT || '% complete',
        CASE 
            WHEN title_completeness_pct >= 95 THEN 'INFO'
            WHEN title_completeness_pct >= 80 THEN 'MEDIUM'
            ELSE 'HIGH'
        END
    FROM data_completeness;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- FUNCTION: Get Table Statistics
-- =============================================================================
CREATE OR REPLACE FUNCTION get_table_stats(p_table_name TEXT)
RETURNS TABLE (
    column_name TEXT,
    data_type TEXT,
    total_rows BIGINT,
    non_null_count BIGINT,
    null_count BIGINT,
    completeness_pct NUMERIC
) AS $$
DECLARE
    v_column RECORD;
    v_total BIGINT;
BEGIN
    -- Get total row count
    EXECUTE format('SELECT COUNT(*) FROM %I', p_table_name) INTO v_total;
    
    -- For each column, get statistics
    FOR v_column IN 
        SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS dtype
        FROM pg_attribute a
        JOIN pg_class c ON a.attrelid = c.oid
        JOIN pg_namespace n ON c.relnamespace = n.oid
        WHERE c.relname = p_table_name 
          AND n.nspname = 'public'
          AND a.attnum > 0 
          AND NOT a.attisdropped
        ORDER BY a.attnum
    LOOP
        RETURN QUERY EXECUTE format(
            'SELECT 
                %L::TEXT,
                %L::TEXT,
                %s::BIGINT,
                COUNT(%I)::BIGINT,
                (%s - COUNT(%I))::BIGINT,
                ROUND(COUNT(%I) * 100.0 / %s, 2)
            FROM %I',
            v_column.attname,
            v_column.dtype,
            v_total,
            v_column.attname,
            v_total,
            v_column.attname,
            v_column.attname,
            v_total,
            p_table_name
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Create metadata tracking table for data quality runs
-- =============================================================================
CREATE TABLE IF NOT EXISTS data_quality_runs (
    id SERIAL PRIMARY KEY,
    run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    run_by TEXT DEFAULT CURRENT_USER,
    total_tables INTEGER,
    total_issues INTEGER,
    critical_issues INTEGER,
    warning_issues INTEGER,
    info_issues INTEGER,
    report_json JSONB,
    notes TEXT
);

-- =============================================================================
-- Function to log data quality run
-- =============================================================================
CREATE OR REPLACE FUNCTION log_data_quality_run(
    p_total_tables INTEGER,
    p_total_issues INTEGER,
    p_critical INTEGER,
    p_warning INTEGER,
    p_info INTEGER,
    p_report JSONB,
    p_notes TEXT DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO data_quality_runs (
        total_tables, total_issues, critical_issues, 
        warning_issues, info_issues, report_json, notes
    ) VALUES (
        p_total_tables, p_total_issues, p_critical,
        p_warning, p_info, p_report, p_notes
    ) RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions
GRANT SELECT ON data_quality_overview TO PUBLIC;
GRANT SELECT ON orphaned_records TO PUBLIC;
GRANT SELECT ON duplicate_detection TO PUBLIC;
GRANT SELECT ON data_completeness TO PUBLIC;
GRANT SELECT ON document_processing_status TO PUBLIC;
GRANT EXECUTE ON FUNCTION run_data_quality_check() TO PUBLIC;
GRANT EXECUTE ON FUNCTION get_table_stats(TEXT) TO PUBLIC;
