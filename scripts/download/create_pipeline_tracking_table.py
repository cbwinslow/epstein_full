#!/usr/bin/env python3
import config

conn = config.get_db_connection()
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS data_pipeline_tracking (
        id SERIAL PRIMARY KEY,
        source_name TEXT NOT NULL,
        source_type TEXT NOT NULL,  -- 'government', 'financial', 'legal', 'media', 'research'
        source_url TEXT,

        -- Download tracking
        download_status TEXT DEFAULT 'pending',  -- 'pending', 'downloading', 'completed', 'failed'
        download_started_at TIMESTAMPTZ,
        download_completed_at TIMESTAMPTZ,
        download_error TEXT,
        download_size_bytes BIGINT,
        download_files_count INT,
        download_path TEXT,

        -- Ingestion tracking
        ingestion_status TEXT DEFAULT 'pending',  -- 'pending', 'in_progress', 'completed', 'failed'
        ingestion_started_at TIMESTAMPTZ,
        ingestion_completed_at TIMESTAMPTZ,
        ingestion_error TEXT,
        records_imported BIGINT DEFAULT 0,
        target_table TEXT,

        -- Metadata
        description TEXT,
        priority TEXT DEFAULT 'medium',  -- 'high', 'medium', 'low'
        notes TEXT,
        last_checked_at TIMESTAMPTZ DEFAULT NOW(),
        created_at TIMESTAMPTZ DEFAULT NOW(),
        updated_at TIMESTAMPTZ DEFAULT NOW()
    );

    -- Indexes for common queries
    CREATE INDEX IF NOT EXISTS idx_pipeline_source_name ON data_pipeline_tracking(source_name);
    CREATE INDEX IF NOT EXISTS idx_pipeline_download_status ON data_pipeline_tracking(download_status);
    CREATE INDEX IF NOT EXISTS idx_pipeline_ingestion_status ON data_pipeline_tracking(ingestion_status);
    CREATE INDEX IF NOT EXISTS idx_pipeline_priority ON data_pipeline_tracking(priority);

    -- Trigger to update updated_at timestamp
    CREATE OR REPLACE FUNCTION update_pipeline_updated_at()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = NOW();
        RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS trigger_update_pipeline_updated_at ON data_pipeline_tracking;
    CREATE TRIGGER trigger_update_pipeline_updated_at
        BEFORE UPDATE ON data_pipeline_tracking
        FOR EACH ROW
        EXECUTE FUNCTION update_pipeline_updated_at();
""")

conn.commit()
conn.close()
print("data_pipeline_tracking table created successfully")
