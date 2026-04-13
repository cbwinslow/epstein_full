-- Data Validation Views and Procedures
-- For monitoring data integrity across all tables

-- 1. View: Record counts for all main tables
CREATE OR REPLACE VIEW v_table_record_counts AS
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.tables t2 
     WHERE t2.table_name = t1.table_name 
     AND t2.table_schema = 'public') as exists,
    pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as total_size
FROM (VALUES 
    ('hf_epstein_files_20k'),
    ('hf_house_oversight_docs'),
    ('hf_ocr_complete'),
    ('hf_embeddings'),
    ('hf_epstein_data_text'),
    ('full_epstein_index'),
    ('fbi_vault_pages'),
    ('house_oversight_embeddings'),
    ('icij_entities'),
    ('icij_officers'),
    ('icij_addresses'),
    ('icij_intermediaries'),
    ('icij_others'),
    ('icij_relationships'),
    ('icij_import_progress')
) AS t1(table_name)
ORDER BY table_name;

-- 2. View: ICIJ Import Progress Summary
CREATE OR REPLACE VIEW v_icij_import_summary AS
SELECT 
    filename,
    status,
    worker_id,
    total_rows as expected,
    rows_imported as imported,
    CASE WHEN total_rows > 0 
         THEN ROUND(100.0 * rows_imported / total_rows, 2) 
         ELSE 0 
    END as percent_complete,
    started_at,
    completed_at,
    EXTRACT(EPOCH FROM (COALESCE(completed_at, NOW()) - started_at))/60 as minutes_elapsed,
    error_message
FROM icij_import_progress
ORDER BY 
    CASE status 
        WHEN 'running' THEN 0 
        WHEN 'pending' THEN 1 
        WHEN 'complete' THEN 2 
        ELSE 3 
    END,
    filename;

-- 3. View: Cross-table relationship validation
CREATE OR REPLACE VIEW v_icij_relationship_validation AS
SELECT 
    'Orphaned relationships (entities)' as check_type,
    COUNT(*) as orphaned_count
FROM icij_relationships r
LEFT JOIN icij_entities e ON r.node_id_start = e.node_id
WHERE e.node_id IS NULL

UNION ALL

SELECT 
    'Orphaned relationships (officers)' as check_type,
    COUNT(*) as orphaned_count
FROM icij_relationships r
LEFT JOIN icij_officers o ON r.node_id_start = o.node_id
WHERE o.node_id IS NULL AND r.node_id_start NOT IN (SELECT node_id FROM icij_entities)

UNION ALL

SELECT 
    'Total relationships' as check_type,
    COUNT(*) as count
FROM icij_relationships;

-- 4. View: Data quality checks for ICIJ
CREATE OR REPLACE VIEW v_icij_data_quality AS
SELECT 
    'Entities with no name' as check_name,
    COUNT(*) as issue_count,
    'High' as severity
FROM icij_entities
WHERE name IS NULL OR TRIM(name) = ''

UNION ALL

SELECT 
    'Officers with no name',
    COUNT(*),
    'High'
FROM icij_officers
WHERE name IS NULL OR TRIM(name) = ''

UNION ALL

SELECT 
    'Entities with no jurisdiction',
    COUNT(*),
    'Medium'
FROM icij_entities
WHERE jurisdiction IS NULL OR TRIM(jurisdiction) = ''

UNION ALL

SELECT 
    'Relationships with missing start node',
    COUNT(*),
    'Critical'
FROM icij_relationships
WHERE node_id_start IS NULL OR TRIM(node_id_start) = ''

UNION ALL

SELECT 
    'Relationships with missing end node',
    COUNT(*),
    'Critical'
FROM icij_relationships
WHERE node_id_end IS NULL OR TRIM(node_id_end) = '';

-- 5. Function: Get overall import status
CREATE OR REPLACE FUNCTION get_import_status()
RETURNS TABLE (
    source_name TEXT,
    records_imported BIGINT,
    status TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'HF epstein-files-20k'::TEXT, (SELECT COUNT(*) FROM hf_epstein_files_20k), 'Complete'::TEXT
    UNION ALL SELECT 'HF House Oversight', (SELECT COUNT(*) FROM hf_house_oversight_docs), 'Complete'
    UNION ALL SELECT 'HF OCR Complete', (SELECT COUNT(*) FROM hf_ocr_complete), 'Complete'
    UNION ALL SELECT 'HF Embeddings', (SELECT COUNT(*) FROM hf_embeddings), 'Complete'
    UNION ALL SELECT 'HF Data Text', (SELECT COUNT(*) FROM hf_epstein_data_text), 'Complete'
    UNION ALL SELECT 'HF FBI Files', (SELECT COUNT(*) FROM fbi_vault_pages), 'Complete'
    UNION ALL SELECT 'HF Full Index', (SELECT COUNT(*) FROM full_epstein_index), 'Complete'
    UNION ALL SELECT 'ICIJ Entities', (SELECT COUNT(*) FROM icij_entities), 
        CASE WHEN (SELECT COUNT(*) FROM icij_entities) > 800000 THEN 'Complete' ELSE 'In Progress' END
    UNION ALL SELECT 'ICIJ Officers', (SELECT COUNT(*) FROM icij_officers),
        CASE WHEN (SELECT COUNT(*) FROM icij_officers) > 1500000 THEN 'Complete' ELSE 'In Progress' END
    UNION ALL SELECT 'ICIJ Relationships', (SELECT COUNT(*) FROM icij_relationships),
        CASE WHEN (SELECT COUNT(*) FROM icij_relationships) > 3000000 THEN 'Complete' ELSE 'In Progress' END;
END;
$$ LANGUAGE plpgsql;

-- 6. Function: Check for duplicate node_ids (critical integrity check)
CREATE OR REPLACE FUNCTION check_duplicate_node_ids()
RETURNS TABLE (
    table_name TEXT,
    duplicate_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 'icij_entities'::TEXT, COUNT(*) - COUNT(DISTINCT node_id)
    FROM icij_entities
    HAVING COUNT(*) > COUNT(DISTINCT node_id)
    
    UNION ALL
    
    SELECT 'icij_officers'::TEXT, COUNT(*) - COUNT(DISTINCT node_id)
    FROM icij_officers
    HAVING COUNT(*) > COUNT(DISTINCT node_id)
    
    UNION ALL
    
    SELECT 'icij_addresses'::TEXT, COUNT(*) - COUNT(DISTINCT node_id)
    FROM icij_addresses
    HAVING COUNT(*) > COUNT(DISTINCT node_id)
    
    UNION ALL
    
    SELECT 'icij_intermediaries'::TEXT, COUNT(*) - COUNT(DISTINCT node_id)
    FROM icij_intermediaries
    HAVING COUNT(*) > COUNT(DISTINCT node_id);
END;
$$ LANGUAGE plpgsql;

-- 7. View: HF Dataset Summary
CREATE OR REPLACE VIEW v_hf_dataset_summary AS
SELECT 
    'hf_epstein_files_20k' as table_name,
    COUNT(*) as total_records,
    COUNT(DISTINCT source_file) as source_files,
    pg_size_pretty(pg_total_relation_size('hf_epstein_files_20k')) as table_size
FROM hf_epstein_files_20k

UNION ALL

SELECT 
    'hf_house_oversight_docs',
    COUNT(*),
    COUNT(DISTINCT source_file),
    pg_size_pretty(pg_total_relation_size('hf_house_oversight_docs'))
FROM hf_house_oversight_docs

UNION ALL

SELECT 
    'hf_ocr_complete',
    COUNT(*),
    COUNT(DISTINCT source_file),
    pg_size_pretty(pg_total_relation_size('hf_ocr_complete'))
FROM hf_ocr_complete

UNION ALL

SELECT 
    'hf_embeddings',
    COUNT(*),
    NULL,
    pg_size_pretty(pg_total_relation_size('hf_embeddings'))
FROM hf_embeddings

UNION ALL

SELECT 
    'hf_epstein_data_text',
    COUNT(*),
    COUNT(DISTINCT source_file),
    pg_size_pretty(pg_total_relation_size('hf_epstein_data_text'))
FROM hf_epstein_data_text

UNION ALL

SELECT 
    'full_epstein_index',
    COUNT(*),
    NULL,
    pg_size_pretty(pg_total_relation_size('full_epstein_index'))
FROM full_epstein_index;

-- 8. Function: Run full validation report
CREATE OR REPLACE FUNCTION run_full_validation()
RETURNS TABLE (
    check_category TEXT,
    check_name TEXT,
    result TEXT,
    severity TEXT
) AS $$
DECLARE
    v_count BIGINT;
    v_expected BIGINT;
BEGIN
    -- HF Dataset checks
    RETURN QUERY SELECT 'HF Datasets'::TEXT, 'epstein-files-20k count', 
        (SELECT COUNT(*)::TEXT FROM hf_epstein_files_20k), 'Info'::TEXT;
    
    RETURN QUERY SELECT 'HF Datasets'::TEXT, 'house-oversight count',
        (SELECT COUNT(*)::TEXT FROM hf_house_oversight_docs), 'Info'::TEXT;
    
    -- ICIJ Checks
    SELECT COUNT(*) INTO v_count FROM icij_entities;
    v_expected := 814617;
    RETURN QUERY SELECT 'ICIJ Entities'::TEXT, 'Record count',
        v_count::TEXT || ' / ' || v_expected::TEXT || 
        ' (' || ROUND(100.0 * v_count / v_expected, 1)::TEXT || '%)',
        CASE WHEN v_count >= v_expected THEN 'Success' ELSE 'In Progress' END::TEXT;
    
    SELECT COUNT(*) INTO v_count FROM icij_officers;
    v_expected := 1800000;
    RETURN QUERY SELECT 'ICIJ Officers'::TEXT, 'Record count',
        v_count::TEXT || ' / ' || v_expected::TEXT || 
        ' (' || ROUND(100.0 * v_count / v_expected, 1)::TEXT || '%)',
        CASE WHEN v_count >= v_expected THEN 'Success' ELSE 'In Progress' END::TEXT;
    
    SELECT COUNT(*) INTO v_count FROM icij_relationships;
    v_expected := 3339272;
    RETURN QUERY SELECT 'ICIJ Relationships'::TEXT, 'Record count',
        v_count::TEXT || ' / ' || v_expected::TEXT || 
        ' (' || ROUND(100.0 * v_count / v_expected, 1)::TEXT || '%)',
        CASE WHEN v_count >= v_expected THEN 'Success' ELSE 'In Progress' END::TEXT;
    
    -- Overall status
    RETURN QUERY SELECT 'Overall'::TEXT, 'Total HF Records',
        (SELECT SUM(count)::TEXT FROM v_hf_dataset_summary), 'Info'::TEXT;
    
    RETURN QUERY SELECT 'Overall'::TEXT, 'ICIJ Import Status',
        (SELECT COUNT(*)::TEXT || ' of 6 files complete' 
         FROM icij_import_progress WHERE status = 'complete'), 'Info'::TEXT;
END;
$$ LANGUAGE plpgsql;
