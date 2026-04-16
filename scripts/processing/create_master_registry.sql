-- Master Registry Tracking System for Epstein Data
-- Centralized tracking of all data sources, imports, and embeddings

-- ============================================
-- 1. MASTER DATA SOURCE REGISTRY
-- Tracks all downloaded/imported data sources
-- ============================================

CREATE TABLE IF NOT EXISTS master_data_registry (
    id SERIAL PRIMARY KEY,
    
    -- Source Identification
    source_name VARCHAR(100) NOT NULL,           -- e.g., "DOJ_Epstein_Library", "jMail_Emails"
    source_type VARCHAR(50) NOT NULL,            -- "DOJ", "HuggingFace", "GitHub", "API", "ThirdParty"
    source_url TEXT,                             -- Original URL
    source_dataset_id VARCHAR(100),              -- Dataset identifier (e.g., "data1", "epstein-files-20k")
    
    -- File/Content Tracking
    file_path TEXT,                              -- Local filesystem path
    file_count INTEGER,                          -- Number of files
    total_size_bytes BIGINT,                     -- Total size in bytes
    content_hash VARCHAR(64),                    -- SHA-256 of entire dataset (if applicable)
    
    -- Status Tracking
    download_status VARCHAR(20) DEFAULT 'pending',  -- pending, downloading, complete, failed
    import_status VARCHAR(20) DEFAULT 'pending',      -- pending, importing, complete, failed, partial
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, processing, complete, failed
    
    -- Timestamps
    download_started_at TIMESTAMPTZ,
    download_completed_at TIMESTAMPTZ,
    import_started_at TIMESTAMPTZ,
    import_completed_at TIMESTAMPTZ,
    last_verified_at TIMESTAMPTZ,
    
    -- Record Counts
    expected_records INTEGER,                    -- Expected from source
    downloaded_records INTEGER,                  -- Actually downloaded
    imported_records INTEGER,                    -- Actually imported to DB
    failed_records INTEGER DEFAULT 0,            -- Failed to import
    
    -- Metadata
    source_format VARCHAR(50),                   -- "PDF", "JSON", "Parquet", "CSV", "XML"
    compression VARCHAR(20),                     -- "gzip", "zip", "none"
    description TEXT,                            -- Human-readable description
    license TEXT,                                -- License info
    
    -- Quality Metrics
    duplicate_count INTEGER DEFAULT 0,           -- Duplicates found/removed
    quality_score DECIMAL(5,2),                    -- 0-100 quality score
    issues JSONB,                                -- Array of issues found
    
    -- Versioning
    source_version VARCHAR(20),                  -- Dataset version
    schema_version INTEGER DEFAULT 1,            -- Internal schema version
    replaces_registry_id INTEGER REFERENCES master_data_registry(id), -- If this replaces an older version
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_by VARCHAR(50) DEFAULT CURRENT_USER,
    notes TEXT,
    
    -- Constraints
    UNIQUE(source_name, source_dataset_id, source_version)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_registry_source_name ON master_data_registry(source_name);
CREATE INDEX IF NOT EXISTS idx_registry_status ON master_data_registry(download_status, import_status);
CREATE INDEX IF NOT EXISTS idx_registry_type ON master_data_registry(source_type);
CREATE INDEX IF NOT EXISTS idx_registry_content_hash ON master_data_registry(content_hash) WHERE content_hash IS NOT NULL;

-- ============================================
-- 2. FILE-LEVEL REGISTRY (Granular tracking)
-- Individual file tracking with hashes
-- ============================================

CREATE TABLE IF NOT EXISTS file_registry_detail (
    id SERIAL PRIMARY KEY,
    registry_id INTEGER REFERENCES master_data_registry(id) ON DELETE CASCADE,
    
    -- File Identification
    filename VARCHAR(255) NOT NULL,
    relative_path TEXT,                          -- Path relative to dataset root
    full_path TEXT,                              -- Absolute path
    
    -- Hashes for deduplication
    md5_hash VARCHAR(32),                        -- Fast MD5 for quick comparison
    sha256_hash VARCHAR(64),                       -- Secure SHA-256 for verification
    sha1_hash VARCHAR(40),                         -- Alternative hash
    
    -- File Metadata
    file_size_bytes BIGINT,
    file_type VARCHAR(50),                         -- MIME type or extension
    modified_time TIMESTAMPTZ,
    
    -- Content Analysis
    is_valid BOOLEAN DEFAULT TRUE,                 -- File integrity check passed
    corruption_type VARCHAR(50),                   -- If invalid: "HTML_POISON", "TRUNCATED", etc.
    header_signature VARCHAR(20),                  -- File header (e.g., "%PDF-1.4")
    
    -- Database Linking
    efta_number VARCHAR(20),                       -- Links to documents.efta_number
    document_id INTEGER REFERENCES documents(id),  -- Links to documents.id
    page_ids INTEGER[],                            -- Array of linked page IDs
    
    -- Status
    processing_status VARCHAR(20) DEFAULT 'pending', -- pending, ocr_complete, embedded, failed
    
    -- Timestamps
    scanned_at TIMESTAMPTZ DEFAULT NOW(),
    processed_at TIMESTAMPTZ,
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    UNIQUE(registry_id, relative_path)
);

-- Indexes for file registry
CREATE INDEX IF NOT EXISTS idx_file_registry_registry_id ON file_registry_detail(registry_id);
CREATE INDEX IF NOT EXISTS idx_file_registry_md5 ON file_registry_detail(md5_hash) WHERE md5_hash IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_file_registry_sha256 ON file_registry_detail(sha256_hash) WHERE sha256_hash IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_file_registry_efta ON file_registry_detail(efta_number) WHERE efta_number IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_file_registry_document ON file_registry_detail(document_id) WHERE document_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_file_registry_status ON file_registry_detail(processing_status);

-- ============================================
-- 3. EMBEDDING REGISTRY
-- Track all embeddings by model and source
-- ============================================

CREATE TABLE IF NOT EXISTS embedding_registry (
    id SERIAL PRIMARY KEY,
    
    -- Source Reference
    registry_id INTEGER REFERENCES master_data_registry(id) ON DELETE CASCADE,
    
    -- Embedding Model Info
    model_name VARCHAR(100) NOT NULL,              -- e.g., "all-MiniLM-L6-v2", "nomic-embed-text-v2-moe"
    model_dimensions INTEGER NOT NULL,             -- 384, 768, 1024
    model_version VARCHAR(50),                     -- Model version/tag
    model_source VARCHAR(50),                      -- "HuggingFace", "Ollama", "OpenAI", "Local"
    
    -- Hardware/Performance
    compute_device VARCHAR(50),                    -- "RTX3060", "K80", "CPU"
    compute_host VARCHAR(100),                     -- Hostname/IP
    avg_generation_rate DECIMAL(10,2),               -- Pages/sec
    
    -- Coverage
    total_pages INTEGER,                           -- Total pages processed
    unique_pages INTEGER,                          -- Deduplicated count
    failed_pages INTEGER DEFAULT 0,                -- Failed embeddings
    
    -- Storage
    storage_table VARCHAR(100),                    -- "page_embeddings", "pages.embedding_nomic"
    storage_column VARCHAR(100),                   -- Column name if in pages table
    estimated_size_bytes BIGINT,                   -- Storage used
    
    -- Status
    generation_status VARCHAR(20) DEFAULT 'pending', -- pending, generating, complete, failed, partial
    
    -- Timestamps
    generation_started_at TIMESTAMPTZ,
    generation_completed_at TIMESTAMPTZ,
    
    -- Quality
    quality_score DECIMAL(5,2),                    -- 0-100 based on validation
    sample_query_results JSONB,                    -- Test query results
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    notes TEXT,
    
    UNIQUE(registry_id, model_name, model_dimensions)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_embedding_registry_model ON embedding_registry(model_name);
CREATE INDEX IF NOT EXISTS idx_embedding_registry_status ON embedding_registry(generation_status);

-- ============================================
-- 4. DUPLICATE TRACKING
-- Central record of all duplicates found
-- ============================================

CREATE TABLE IF NOT EXISTS duplicate_registry (
    id SERIAL PRIMARY KEY,
    
    -- Duplicate Group
    content_hash VARCHAR(64) NOT NULL,             -- MD5 or SHA256 of content
    duplicate_type VARCHAR(50) NOT NULL,           -- "exact_file", "exact_text", "near_duplicate"
    
    -- Canonical (master) record
    canonical_file_id INTEGER REFERENCES file_registry_detail(id),
    canonical_page_id INTEGER REFERENCES pages(id),
    
    -- Duplicate records (JSON array for flexibility)
    duplicate_file_ids JSONB,                      -- Array of file_registry_detail IDs
    duplicate_page_ids JSONB,                      -- Array of page IDs
    
    -- Analysis
    duplicate_count INTEGER,                       -- Number of duplicates (excluding canonical)
    total_size_bytes BIGINT,                       -- Total size of all duplicates
    space_saved_bytes BIGINT,                      -- Space if duplicates removed
    
    -- Status
    resolution_status VARCHAR(20) DEFAULT 'identified', -- identified, verified, resolved, ignored
    resolution_action VARCHAR(50),                 -- "kept_canonical", "merged", "deleted"
    
    -- Timestamps
    identified_at TIMESTAMPTZ DEFAULT NOW(),
    resolved_at TIMESTAMPTZ,
    
    -- Audit
    identified_by VARCHAR(50) DEFAULT CURRENT_USER,
    notes TEXT,
    
    UNIQUE(content_hash, duplicate_type)
);

CREATE INDEX IF NOT EXISTS idx_duplicate_registry_hash ON duplicate_registry(content_hash);
CREATE INDEX IF NOT EXISTS idx_duplicate_registry_status ON duplicate_registry(resolution_status);
CREATE INDEX IF NOT EXISTS idx_duplicate_registry_type ON duplicate_registry(duplicate_type);

-- ============================================
-- 5. PROCESSING PIPELINE LOG
-- Track all data processing operations
-- ============================================

CREATE TABLE IF NOT EXISTS processing_log (
    id SERIAL PRIMARY KEY,
    
    -- Operation Info
    operation_name VARCHAR(100) NOT NULL,          -- e.g., "OCR", "NER", "Embedding Generation"
    operation_type VARCHAR(50) NOT NULL,           -- "download", "import", "transform", "generate"
    registry_id INTEGER REFERENCES master_data_registry(id),
    
    -- Status
    status VARCHAR(20) NOT NULL,                   -- started, running, completed, failed, cancelled
    
    -- Progress
    total_items INTEGER,                           -- Total items to process
    processed_items INTEGER DEFAULT 0,             -- Items completed
    failed_items INTEGER DEFAULT 0,                -- Items failed
    
    -- Performance
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    duration_seconds INTEGER,                      -- Calculated
    items_per_second DECIMAL(10,2),                  -- Performance metric
    
    -- Resources
    cpu_percent DECIMAL(5,2),                        -- CPU usage
    memory_mb BIGINT,                                -- Memory used
    gpu_device VARCHAR(50),                          -- GPU used (if any)
    gpu_memory_mb BIGINT,                            -- GPU memory used
    
    -- Error Tracking
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    error_log TEXT,                                  -- Full error details
    
    -- Metadata
    command_line TEXT,                               -- Command/script that ran
    config JSONB,                                    -- Configuration used
    
    -- Audit
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    hostname VARCHAR(100) DEFAULT (SELECT inet_server_addr()::TEXT),
    pid INTEGER,
    
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_processing_log_operation ON processing_log(operation_name);
CREATE INDEX IF NOT EXISTS idx_processing_log_status ON processing_log(status);
CREATE INDEX IF NOT EXISTS idx_processing_log_registry ON processing_log(registry_id);
CREATE INDEX IF NOT EXISTS idx_processing_log_time ON processing_log(created_at);

-- ============================================
-- 6. VIEWS FOR EASY QUERYING
-- ============================================

-- View: Data Source Summary
CREATE OR REPLACE VIEW v_data_source_summary AS
SELECT 
    source_type,
    COUNT(*) as total_sources,
    SUM(file_count) as total_files,
    SUM(total_size_bytes) as total_size,
    SUM(imported_records) as total_records,
    COUNT(CASE WHEN import_status = 'complete' THEN 1 END) as completed_sources,
    COUNT(CASE WHEN import_status = 'pending' THEN 1 END) as pending_sources,
    COUNT(CASE WHEN import_status = 'failed' THEN 1 END) as failed_sources
FROM master_data_registry
GROUP BY source_type
ORDER BY total_records DESC;

-- View: Embedding Coverage Summary
CREATE OR REPLACE VIEW v_embedding_coverage_summary AS
SELECT 
    er.model_name,
    er.model_dimensions,
    er.compute_device,
    er.generation_status,
    er.total_pages,
    er.unique_pages,
    er.avg_generation_rate,
    mdr.source_name,
    mdr.source_dataset_id
FROM embedding_registry er
JOIN master_data_registry mdr ON er.registry_id = mdr.id
ORDER BY er.created_at DESC;

-- View: Duplicate Summary
CREATE OR REPLACE VIEW v_duplicate_summary AS
SELECT 
    duplicate_type,
    COUNT(*) as duplicate_groups,
    SUM(duplicate_count) as total_duplicates,
    SUM(total_size_bytes) as total_duplicate_size,
    SUM(space_saved_bytes) as potential_space_savings,
    COUNT(CASE WHEN resolution_status = 'resolved' THEN 1 END) as resolved_count,
    COUNT(CASE WHEN resolution_status = 'identified' THEN 1 END) as pending_count
FROM duplicate_registry
GROUP BY duplicate_type;

-- View: Processing Status Dashboard
CREATE OR REPLACE VIEW v_processing_dashboard AS
SELECT 
    operation_name,
    COUNT(*) as total_runs,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
    COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed,
    COUNT(CASE WHEN status = 'running' THEN 1 END) as running,
    AVG(duration_seconds) as avg_duration_sec,
    AVG(items_per_second) as avg_rate,
    MAX(started_at) as last_run
FROM processing_log
WHERE started_at > NOW() - INTERVAL '30 days'
GROUP BY operation_name
ORDER BY last_run DESC;

-- ============================================
-- 7. HELPER FUNCTIONS
-- ============================================

-- Function: Register new data source
CREATE OR REPLACE FUNCTION register_data_source(
    p_source_name VARCHAR(100),
    p_source_type VARCHAR(50),
    p_source_url TEXT,
    p_source_dataset_id VARCHAR(100),
    p_file_path TEXT,
    p_expected_records INTEGER,
    p_source_format VARCHAR(50),
    p_description TEXT
) RETURNS INTEGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO master_data_registry (
        source_name, source_type, source_url, source_dataset_id,
        file_path, expected_records, source_format, description,
        download_status, import_status
    ) VALUES (
        p_source_name, p_source_type, p_source_url, p_source_dataset_id,
        p_file_path, p_expected_records, p_source_format, p_description,
        'pending', 'pending'
    )
    ON CONFLICT (source_name, source_dataset_id, source_version) 
    DO UPDATE SET
        file_path = EXCLUDED.file_path,
        expected_records = EXCLUDED.expected_records,
        updated_at = NOW(),
        notes = COALESCE(master_data_registry.notes, '') || E'\nUpdated: ' || NOW()
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Update download status
CREATE OR REPLACE FUNCTION update_download_status(
    p_registry_id INTEGER,
    p_status VARCHAR(20),
    p_file_count INTEGER DEFAULT NULL,
    p_size_bytes BIGINT DEFAULT NULL,
    p_content_hash VARCHAR(64) DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    UPDATE master_data_registry SET
        download_status = p_status,
        file_count = COALESCE(p_file_count, file_count),
        total_size_bytes = COALESCE(p_size_bytes, total_size_bytes),
        content_hash = COALESCE(p_content_hash, content_hash),
        download_started_at = CASE WHEN p_status = 'downloading' AND download_started_at IS NULL THEN NOW() ELSE download_started_at END,
        download_completed_at = CASE WHEN p_status = 'complete' THEN NOW() ELSE download_completed_at END,
        updated_at = NOW()
    WHERE id = p_registry_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Update import status
CREATE OR REPLACE FUNCTION update_import_status(
    p_registry_id INTEGER,
    p_status VARCHAR(20),
    p_imported_records INTEGER DEFAULT NULL,
    p_failed_records INTEGER DEFAULT NULL
) RETURNS VOID AS $$
BEGIN
    UPDATE master_data_registry SET
        import_status = p_status,
        imported_records = COALESCE(p_imported_records, imported_records),
        failed_records = COALESCE(p_failed_records, failed_records),
        import_started_at = CASE WHEN p_status = 'importing' AND import_started_at IS NULL THEN NOW() ELSE import_started_at END,
        import_completed_at = CASE WHEN p_status = 'complete' THEN NOW() ELSE import_completed_at END,
        updated_at = NOW()
    WHERE id = p_registry_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Register embedding generation
CREATE OR REPLACE FUNCTION register_embedding_generation(
    p_registry_id INTEGER,
    p_model_name VARCHAR(100),
    p_model_dimensions INTEGER,
    p_compute_device VARCHAR(50),
    p_total_pages INTEGER,
    p_storage_table VARCHAR(100),
    p_storage_column VARCHAR(100)
) RETURNS INTEGER AS $$
DECLARE
    v_id INTEGER;
BEGIN
    INSERT INTO embedding_registry (
        registry_id, model_name, model_dimensions, compute_device,
        total_pages, storage_table, storage_column, generation_status
    ) VALUES (
        p_registry_id, p_model_name, p_model_dimensions, p_compute_device,
        p_total_pages, p_storage_table, p_storage_column, 'pending'
    )
    ON CONFLICT (registry_id, model_name, model_dimensions)
    DO UPDATE SET
        generation_status = 'regenerating',
        updated_at = NOW()
    RETURNING id INTO v_id;
    
    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Get data source status
CREATE OR REPLACE FUNCTION get_source_status(p_source_name VARCHAR(100))
RETURNS TABLE (
    source_name VARCHAR(100),
    source_dataset_id VARCHAR(100),
    download_status VARCHAR(20),
    import_status VARCHAR(20),
    processing_status VARCHAR(20),
    file_count INTEGER,
    imported_records INTEGER,
    last_updated TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        mdr.source_name,
        mdr.source_dataset_id,
        mdr.download_status,
        mdr.import_status,
        mdr.processing_status,
        mdr.file_count,
        mdr.imported_records,
        mdr.updated_at
    FROM master_data_registry mdr
    WHERE mdr.source_name = p_source_name
    ORDER BY mdr.updated_at DESC;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- 8. INITIAL DATA POPULATION
-- Populate with known existing sources
-- ============================================

-- Insert known data sources
INSERT INTO master_data_registry (
    source_name, source_type, source_dataset_id, source_url,
    file_path, file_count, imported_records, source_format,
    download_status, import_status, processing_status, description
) VALUES 
    ('DOJ_Epstein_Library', 'DOJ', 'data1-12', 'https://www.justice.gov/epstein-library',
     '/home/cbwinslow/workspace/epstein-data/raw-files', 260000, 1400000, 'PDF',
     'complete', 'complete', 'complete', 'Primary DOJ Epstein document releases'),
    
    ('jMail_Emails', 'API', 'emails_full', 'https://jmail.world',
     '/home/cbwinslow/workspace/epstein-data/downloads', NULL, 1783792, 'Parquet',
     'complete', 'complete', 'complete', 'jMail World email archive'),
    
    ('jMail_Documents', 'API', 'documents', 'https://jmail.world',
     '/home/cbwinslow/workspace/epstein-data/downloads', NULL, 1413417, 'Parquet',
     'complete', 'complete', 'complete', 'jMail World document metadata'),
    
    ('HF_epstein_files_20k', 'HuggingFace', 'epstein-files-20k', 'https://huggingface.co/datasets/teyler/epstein-files-20k',
     '/home/cbwinslow/workspace/epstein-data/hf-epstein-files-20k', NULL, 2136420, 'JSONL',
     'complete', 'complete', 'complete', 'House Oversight documents from HuggingFace'),
    
    ('GDELT_News', 'API', 'gdelt_gkg', 'http://data.gdeltproject.org/gdeltv2/',
     '/home/cbwinslow/workspace/epstein-data/downloads/gdelt', NULL, 23413, 'CSV',
     'complete', 'complete', 'complete', 'GDELT news articles mentioning Epstein'),
    
    ('ICIJ_Offshore_Leaks', 'ThirdParty', 'full-oldb', 'https://offshoreleaks-data.icij.org/',
     '/home/cbwinslow/workspace/epstein-data/downloads/icij_extracted', NULL, 3339272, 'CSV',
     'complete', 'complete', 'complete', 'ICIJ Offshore Leaks database'),
    
    ('FEC_Contributions', 'API', 'individual_contributions', 'https://www.fec.gov/data/',
     '/home/cbwinslow/workspace/epstein-data/raw-files/fec', NULL, 5420940, 'CSV',
     'complete', 'complete', 'complete', 'FEC campaign finance data'),
    
    ('FBI_Vault', 'ThirdParty', 'fbi-files', 'https://vault.fbi.gov/',
     '/home/cbwinslow/workspace/epstein-data/hf-datasets/fbi-files', 355, 236174, 'PDF',
     'complete', 'partial', 'complete', 'FBI Vault Epstein files')

ON CONFLICT (source_name, source_dataset_id, source_version) DO NOTHING;

-- Insert known embeddings
INSERT INTO embedding_registry (
    registry_id, model_name, model_dimensions, compute_device,
    total_pages, storage_table, generation_status
)
SELECT 
    mdr.id,
    CASE 
        WHEN mdr.source_name = 'DOJ_Epstein_Library' THEN 'all-MiniLM-L6-v2'
        WHEN mdr.source_name = 'FBI_Vault' THEN 'HuggingFace-768'
        ELSE 'unknown'
    END,
    CASE 
        WHEN mdr.source_name IN ('DOJ_Epstein_Library', 'FBI_Vault') THEN 768
        ELSE 768
    END,
    CASE 
        WHEN mdr.source_name = 'DOJ_Epstein_Library' THEN 'K80'
        WHEN mdr.source_name = 'FBI_Vault' THEN 'Pre-computed'
        ELSE 'Unknown'
    END,
    mdr.imported_records,
    CASE 
        WHEN mdr.source_name = 'DOJ_Epstein_Library' THEN 'page_embeddings'
        WHEN mdr.source_name = 'FBI_Vault' THEN 'fbi_embeddings'
        ELSE 'unknown'
    END,
    'complete'
FROM master_data_registry mdr
WHERE mdr.source_name IN ('DOJ_Epstein_Library', 'FBI_Vault', 'HF_epstein_files_20k')
ON CONFLICT (registry_id, model_name, model_dimensions) DO NOTHING;

-- ============================================
-- 9. SUMMARY REPORT
-- ============================================

SELECT 'Master Registry System Created Successfully' as status;
SELECT 'Tables created:' as info;
SELECT '  - master_data_registry (data sources)' as table_name;
SELECT '  - file_registry_detail (individual files)' as table_name;
SELECT '  - embedding_registry (embedding tracking)' as table_name;
SELECT '  - duplicate_registry (duplicate tracking)' as table_name;
SELECT '  - processing_log (operation logging)' as table_name;
SELECT 'Views created:' as info;
SELECT '  - v_data_source_summary' as view_name;
SELECT '  - v_embedding_coverage_summary' as view_name;
SELECT '  - v_duplicate_summary' as view_name;
SELECT '  - v_processing_dashboard' as view_name;
SELECT 'Functions created:' as info;
SELECT '  - register_data_source()' as function_name;
SELECT '  - update_download_status()' as function_name;
SELECT '  - update_import_status()' as function_name;
SELECT '  - register_embedding_generation()' as function_name;
SELECT '  - get_source_status()' as function_name;

-- Show initial data
SELECT '' as separator;
SELECT '=== INITIAL DATA SOURCES REGISTERED ===' as report;
SELECT source_name, source_dataset_id, import_status, imported_records, source_type 
FROM master_data_registry 
ORDER BY imported_records DESC;
