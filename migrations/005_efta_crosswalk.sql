-- =============================================================================
-- EFTA Crosswalk and Data Source Tracking System
-- =============================================================================
-- Uses EFTA numbers as canonical identifiers to track document provenance
-- across multiple sources (DOJ datasets, HF datasets, raw files, etc.)

-- =============================================================================
-- Table: efta_crosswalk
-- Tracks which EFTA numbers exist in which data sources
-- =============================================================================

CREATE TABLE IF NOT EXISTS efta_crosswalk (
    efta_number VARCHAR(50) PRIMARY KEY,
    
    -- Source flags (boolean for quick filtering)
    in_postgresql BOOLEAN DEFAULT FALSE,
    in_raw_files BOOLEAN DEFAULT FALSE,
    in_hf_ocr_complete BOOLEAN DEFAULT FALSE,
    in_hf_house_oversight BOOLEAN DEFAULT FALSE,
    in_hf_embeddings BOOLEAN DEFAULT FALSE,
    in_hf_emails BOOLEAN DEFAULT FALSE,
    
    -- Detailed source info
    postgresql_dataset INTEGER,
    postgresql_ingested_at TIMESTAMP,
    raw_file_path TEXT,
    raw_file_size BIGINT,
    hf_dataset_name TEXT,
    hf_downloaded_at TIMESTAMP,
    
    -- Data quality tracking
    has_ocr BOOLEAN DEFAULT FALSE,
    has_embeddings BOOLEAN DEFAULT FALSE,
    has_entities BOOLEAN DEFAULT FALSE,
    has_classification BOOLEAN DEFAULT FALSE,
    
    -- Cross-validation
    content_hash TEXT,  -- MD5 hash of content for deduplication
    last_verified_at TIMESTAMP,
    verification_status VARCHAR(20) DEFAULT 'unknown',
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_efta_crosswalk_pg ON efta_crosswalk(in_postgresql);
CREATE INDEX IF NOT EXISTS idx_efta_crosswalk_raw ON efta_crosswalk(in_raw_files);
CREATE INDEX IF NOT EXISTS idx_efta_crosswalk_hf_ocr ON efta_crosswalk(in_hf_ocr_complete);
CREATE INDEX IF NOT EXISTS idx_efta_crosswalk_verification ON efta_crosswalk(verification_status);
CREATE INDEX IF NOT EXISTS idx_efta_crosswalk_content_hash ON efta_crosswalk(content_hash);

-- =============================================================================
-- Function: Update EFTA crosswalk from PostgreSQL documents
-- =============================================================================

CREATE OR REPLACE FUNCTION sync_efta_crosswalk_from_postgresql()
RETURNS TABLE (inserted INTEGER, updated INTEGER) AS $$
DECLARE
    v_inserted INTEGER := 0;
    v_updated INTEGER := 0;
BEGIN
    -- Insert new EFTA numbers from documents
    WITH inserted AS (
        INSERT INTO efta_crosswalk (efta_number, in_postgresql, postgresql_dataset, postgresql_ingested_at)
        SELECT 
            d.efta_number,
            TRUE,
            d.dataset,
            d.created_at
        FROM documents d
        LEFT JOIN efta_crosswalk ec ON d.efta_number = ec.efta_number
        WHERE ec.efta_number IS NULL
        RETURNING efta_number
    )
    SELECT COUNT(*) INTO v_inserted FROM inserted;
    
    -- Update existing records
    WITH updated AS (
        UPDATE efta_crosswalk ec
        SET 
            in_postgresql = TRUE,
            postgresql_dataset = d.dataset,
            postgresql_ingested_at = d.created_at,
            updated_at = CURRENT_TIMESTAMP
        FROM documents d
        WHERE ec.efta_number = d.efta_number
          AND (ec.in_postgresql IS NULL OR ec.in_postgresql = FALSE)
        RETURNING ec.efta_number
    )
    SELECT COUNT(*) INTO v_updated FROM updated;
    
    RETURN QUERY SELECT v_inserted, v_updated;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Function: Update EFTA crosswalk from HF dataset
-- =============================================================================

CREATE OR REPLACE FUNCTION sync_efta_crosswalk_from_hf(
    p_dataset_name TEXT,
    p_efta_numbers TEXT[]
)
RETURNS INTEGER AS $$
DECLARE
    v_updated INTEGER := 0;
BEGIN
    -- Insert or update EFTA numbers
    WITH upserted AS (
        INSERT INTO efta_crosswalk (efta_number, hf_dataset_name)
        SELECT UNNEST(p_efta_numbers), p_dataset_name
        ON CONFLICT (efta_number) 
        DO UPDATE SET
            hf_dataset_name = EXCLUDED.hf_dataset_name,
            updated_at = CURRENT_TIMESTAMP,
            hf_downloaded_at = CURRENT_TIMESTAMP
        RETURNING efta_number
    )
    SELECT COUNT(*) INTO v_updated FROM upserted;
    
    -- Update the specific source flag based on dataset name
    CASE p_dataset_name
        WHEN 'hf-ocr-complete' THEN
            UPDATE efta_crosswalk SET in_hf_ocr_complete = TRUE 
            WHERE efta_number = ANY(p_efta_numbers) AND in_hf_ocr_complete = FALSE;
        WHEN 'hf-house-oversight' THEN
            UPDATE efta_crosswalk SET in_hf_house_oversight = TRUE 
            WHERE efta_number = ANY(p_efta_numbers) AND in_hf_house_oversight = FALSE;
        WHEN 'hf-embeddings' THEN
            UPDATE efta_crosswalk SET in_hf_embeddings = TRUE 
            WHERE efta_number = ANY(p_efta_numbers) AND in_hf_embeddings = FALSE;
        WHEN 'hf-emails' THEN
            UPDATE efta_crosswalk SET in_hf_emails = TRUE 
            WHERE efta_number = ANY(p_efta_numbers) AND in_hf_emails = FALSE;
    END CASE;
    
    RETURN v_updated;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- View: EFTA Source Coverage Summary
-- =============================================================================

CREATE OR REPLACE VIEW efta_source_coverage AS
SELECT
    COUNT(*) as total_efta_numbers,
    SUM(CASE WHEN in_postgresql THEN 1 ELSE 0 END) as in_postgresql,
    SUM(CASE WHEN in_raw_files THEN 1 ELSE 0 END) as in_raw_files,
    SUM(CASE WHEN in_hf_ocr_complete THEN 1 ELSE 0 END) as in_hf_ocr_complete,
    SUM(CASE WHEN in_hf_house_oversight THEN 1 ELSE 0 END) as in_hf_house_oversight,
    SUM(CASE WHEN in_hf_embeddings THEN 1 ELSE 0 END) as in_hf_embeddings,
    SUM(CASE WHEN in_hf_emails THEN 1 ELSE 0 END) as in_hf_emails,
    
    -- Calculate overlaps
    SUM(CASE WHEN in_postgresql AND in_hf_ocr_complete THEN 1 ELSE 0 END) as pg_and_hf_ocr,
    SUM(CASE WHEN in_postgresql AND NOT in_hf_ocr_complete THEN 1 ELSE 0 END) as pg_only,
    SUM(CASE WHEN NOT in_postgresql AND in_hf_ocr_complete THEN 1 ELSE 0 END) as hf_ocr_only,
    
    -- Data quality
    SUM(CASE WHEN has_ocr THEN 1 ELSE 0 END) as with_ocr,
    SUM(CASE WHEN has_embeddings THEN 1 ELSE 0 END) as with_embeddings,
    SUM(CASE WHEN has_entities THEN 1 ELSE 0 END) as with_entities
FROM efta_crosswalk;

-- =============================================================================
-- View: Missing Data Analysis by EFTA
-- =============================================================================

CREATE OR REPLACE VIEW efta_missing_data_analysis AS
SELECT
    efta_number,
    CASE 
        WHEN in_postgresql AND NOT has_ocr THEN 'missing_ocr'
        WHEN in_postgresql AND NOT has_embeddings THEN 'missing_embeddings'
        WHEN in_hf_ocr_complete AND NOT in_postgresql THEN 'not_in_pg'
        WHEN NOT in_postgresql AND NOT in_raw_files THEN 'missing_all_sources'
        ELSE 'complete'
    END as missing_status,
    in_postgresql,
    in_raw_files,
    in_hf_ocr_complete,
    has_ocr,
    has_embeddings,
    has_entities
FROM efta_crosswalk
WHERE 
    (in_postgresql AND NOT has_ocr)
    OR (in_postgresql AND NOT has_embeddings)
    OR (in_hf_ocr_complete AND NOT in_postgresql)
    OR (NOT in_postgresql AND NOT in_raw_files);

-- =============================================================================
-- Function: Find Duplicate Content by Hash
-- =============================================================================

CREATE OR REPLACE FUNCTION find_duplicate_efta_by_hash()
RETURNS TABLE (
    content_hash TEXT,
    efta_numbers TEXT[],
    duplicate_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ec.content_hash,
        ARRAY_AGG(ec.efta_number) as efta_numbers,
        COUNT(*)::INTEGER as duplicate_count
    FROM efta_crosswalk ec
    WHERE ec.content_hash IS NOT NULL
    GROUP BY ec.content_hash
    HAVING COUNT(*) > 1
    ORDER BY COUNT(*) DESC;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Function: Validate EFTA Crosswalk
-- =============================================================================

CREATE OR REPLACE FUNCTION validate_efta_crosswalk()
RETURNS TABLE (
    check_name TEXT,
    status TEXT,
    details TEXT,
    severity TEXT
) AS $$
BEGIN
    -- Check 1: EFTA numbers in PostgreSQL but not in crosswalk
    RETURN QUERY
    SELECT 
        'PG docs missing from crosswalk'::TEXT,
        'FAIL'::TEXT,
        COUNT(*)::TEXT || ' documents not tracked in crosswalk',
        'HIGH'::TEXT
    FROM documents d
    LEFT JOIN efta_crosswalk ec ON d.efta_number = ec.efta_number
    WHERE ec.efta_number IS NULL;
    
    -- Check 2: Orphaned crosswalk entries (no actual data)
    RETURN QUERY
    SELECT 
        'Orphaned crosswalk entries'::TEXT,
        CASE WHEN COUNT(*) > 0 THEN 'WARNING' ELSE 'PASS' END,
        COUNT(*)::TEXT || ' EFTA numbers with no source flags set',
        'MEDIUM'::TEXT
    FROM efta_crosswalk
    WHERE NOT (in_postgresql OR in_raw_files OR in_hf_ocr_complete OR in_hf_house_oversight);
    
    -- Check 3: Duplicate content hashes
    RETURN QUERY
    SELECT 
        'Duplicate content by hash'::TEXT,
        CASE WHEN COUNT(*) > 0 THEN 'WARNING' ELSE 'PASS' END,
        COUNT(*)::TEXT || ' content hashes appear multiple times',
        'MEDIUM'::TEXT
    FROM (
        SELECT content_hash
        FROM efta_crosswalk
        WHERE content_hash IS NOT NULL
        GROUP BY content_hash
        HAVING COUNT(*) > 1
    ) dupes;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;

-- =============================================================================
-- Trigger: Auto-update updated_at timestamp
-- =============================================================================

CREATE OR REPLACE FUNCTION update_efta_crosswalk_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_efta_crosswalk ON efta_crosswalk;

CREATE TRIGGER trigger_update_efta_crosswalk
    BEFORE UPDATE ON efta_crosswalk
    FOR EACH ROW
    EXECUTE FUNCTION update_efta_crosswalk_timestamp();

-- Grant permissions
GRANT SELECT, INSERT, UPDATE ON efta_crosswalk TO PUBLIC;
GRANT USAGE, SELECT ON SEQUENCE efta_crosswalk_id_seq TO PUBLIC;
GRANT EXECUTE ON FUNCTION sync_efta_crosswalk_from_postgresql() TO PUBLIC;
GRANT EXECUTE ON FUNCTION sync_efta_crosswalk_from_hf(TEXT, TEXT[]) TO PUBLIC;
GRANT EXECUTE ON FUNCTION find_duplicate_efta_by_hash() TO PUBLIC;
GRANT EXECUTE ON FUNCTION validate_efta_crosswalk() TO PUBLIC;
