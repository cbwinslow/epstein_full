-- Master Data Inventory Schema
CREATE TABLE IF NOT EXISTS data_sources (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL UNIQUE,
    source_type VARCHAR(100) NOT NULL,
    description TEXT,
    base_path TEXT,
    file_pattern VARCHAR(255),
    total_files INTEGER,
    total_size_gb DECIMAL(10,2),
    expected_records INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    priority INTEGER DEFAULT 5,
    target_table VARCHAR(255),
    records_imported INTEGER DEFAULT 0,
    source_url TEXT,
    license TEXT,
    last_updated TIMESTAMP DEFAULT NOW(),
    import_started TIMESTAMP,
    import_completed TIMESTAMP,
    error_message TEXT,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX IF NOT EXISTS idx_data_sources_status ON data_sources(status);
CREATE INDEX IF NOT EXISTS idx_data_sources_type ON data_sources(source_type);

CREATE TABLE IF NOT EXISTS data_files (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES data_sources(id) ON DELETE CASCADE,
    filename VARCHAR(500) NOT NULL,
    full_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    file_hash VARCHAR(64),
    status VARCHAR(50) DEFAULT 'pending',
    records_in_file INTEGER,
    records_imported INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    processed_at TIMESTAMP,
    error_count INTEGER DEFAULT 0,
    last_error TEXT,
    processing_lock_id VARCHAR(100),
    locked_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_data_files_source ON data_files(source_id);
CREATE INDEX IF NOT EXISTS idx_data_files_status ON data_files(status);

CREATE TABLE IF NOT EXISTS import_queue (
    id SERIAL PRIMARY KEY,
    file_id INTEGER REFERENCES data_files(id) ON DELETE CASCADE,
    source_type VARCHAR(100),
    priority INTEGER DEFAULT 5,
    status VARCHAR(50) DEFAULT 'pending',
    worker_id VARCHAR(100),
    assigned_at TIMESTAMP,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    progress_percent INTEGER DEFAULT 0,
    records_processed INTEGER DEFAULT 0,
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,
    last_error TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_import_queue_status ON import_queue(status, priority, created_at);

CREATE TABLE IF NOT EXISTS import_log (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES data_sources(id),
    file_id INTEGER REFERENCES data_files(id),
    action VARCHAR(100),
    status VARCHAR(50),
    message TEXT,
    details JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- View for summary
CREATE OR REPLACE VIEW v_data_source_summary AS
SELECT 
    ds.id,
    ds.source_name,
    ds.source_type,
    ds.status,
    ds.priority,
    ds.expected_records,
    ds.records_imported,
    CASE WHEN ds.expected_records > 0 THEN ROUND(100.0 * ds.records_imported / ds.expected_records, 2) ELSE 0 END as completion_percent,
    COUNT(df.id) as total_files,
    COUNT(CASE WHEN df.status = 'complete' THEN 1 END) as files_complete,
    SUM(df.file_size_bytes) / (1024.0 * 1024 * 1024) as total_size_gb,
    ds.last_updated
FROM data_sources ds
LEFT JOIN data_files df ON ds.id = df.source_id
GROUP BY ds.id, ds.source_name, ds.source_type, ds.status, ds.priority, ds.expected_records, ds.records_imported, ds.last_updated;

-- View for pending work
CREATE OR REPLACE VIEW v_pending_imports AS
SELECT 
    ds.source_name,
    ds.source_type,
    ds.priority,
    COUNT(df.id) as files_pending,
    SUM(df.file_size_bytes) / (1024.0 * 1024 * 1024) as pending_size_gb
FROM data_sources ds
JOIN data_files df ON ds.id = df.source_id
WHERE ds.status IN ('pending', 'importing') OR df.status IN ('pending', 'failed')
GROUP BY ds.id, ds.source_name, ds.source_type, ds.priority
ORDER BY ds.priority, ds.source_name;
