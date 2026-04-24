-- Create table to track download scripts with their content
CREATE TABLE IF NOT EXISTS download_scripts (
    id SERIAL PRIMARY KEY,
    script_name TEXT NOT NULL UNIQUE,
    script_path TEXT NOT NULL,
    script_content TEXT NOT NULL,
    script_hash TEXT NOT NULL,  -- SHA-256 hash of script content for version tracking
    version TEXT,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on script_name for quick lookups
CREATE INDEX IF NOT EXISTS idx_download_scripts_name ON download_scripts(script_name);
CREATE INDEX IF NOT EXISTS idx_download_scripts_hash ON download_scripts(script_hash);

-- Add foreign key to data_pipeline_tracking to link to the script used
ALTER TABLE data_pipeline_tracking 
ADD COLUMN IF NOT EXISTS download_script_id INTEGER REFERENCES download_scripts(id);

-- Add index on download_script_id for joins
CREATE INDEX IF NOT EXISTS idx_data_pipeline_tracking_script ON data_pipeline_tracking(download_script_id);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_download_scripts_updated_at 
    BEFORE UPDATE ON download_scripts 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE download_scripts IS 'Tracks download scripts with their content for reproducibility';
COMMENT ON COLUMN download_scripts.script_content IS 'Full source code of the download script';
COMMENT ON COLUMN download_scripts.script_hash IS 'SHA-256 hash for version tracking';
COMMENT ON COLUMN data_pipeline_tracking.download_script_id IS 'Foreign key to the script used for this download';
