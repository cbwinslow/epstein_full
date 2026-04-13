-- Populate Master Inventory with all data sources

-- Create master inventory table if not exists
CREATE TABLE IF NOT EXISTS data_inventory (
    id SERIAL PRIMARY KEY,
    source_name VARCHAR(255) NOT NULL UNIQUE,
    source_type VARCHAR(100) NOT NULL,
    description TEXT,
    target_table VARCHAR(255),
    expected_records INTEGER,
    actual_records INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'pending',
    priority INTEGER DEFAULT 5,
    source_path TEXT,
    imported_at TIMESTAMP,
    last_updated TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'
);

-- Clear existing data
TRUNCATE data_inventory;

-- Insert HF Datasets (all COMPLETE)
INSERT INTO data_inventory (source_name, source_type, description, target_table, expected_records, actual_records, status, priority, imported_at) VALUES
('HF epstein-files-20k', 'huggingface', 'Main HF dataset with 20K documents', 'hf_epstein_files_20k', 2136420, 2136420, 'complete', 1, NOW()),
('HF House Oversight TXT', 'huggingface', 'House Oversight document references', 'hf_house_oversight_docs', 1791798, 1791798, 'complete', 1, NOW()),
('HF OCR Complete', 'huggingface', 'OCR text data', 'hf_ocr_complete', 1380932, 1380932, 'complete', 1, NOW()),
('HF Embeddings', 'huggingface', 'Vector embeddings (768-dim)', 'hf_embeddings', 69290, 69290, 'complete', 1, NOW()),
('HF Epstein Data Text', 'huggingface', 'Extracted text content', 'hf_epstein_data_text', 451720, 451720, 'complete', 1, NOW()),
('HF FBI Files', 'huggingface', 'FBI Vault files', 'fbi_vault_pages', 1426, 1426, 'complete', 1, NOW()),
('HF Full Epstein Index', 'huggingface', 'EFTA text extract index', 'full_epstein_index', 8531, 8531, 'complete', 1, NOW()),
('HF House Oversight Embeddings', 'huggingface', 'Document embeddings', 'house_oversight_embeddings', 69290, 69290, 'complete', 1, NOW()),
('HF Email Threads', 'huggingface', 'Duplicate - dropped', NULL, 5082, 0, 'duplicate', 10, NULL);

-- Insert ICIJ Datasets (IN PROGRESS)
INSERT INTO data_inventory (source_name, source_type, description, target_table, expected_records, status, priority) VALUES
('ICIJ Entities', 'icij', 'Offshore companies/entities', 'icij_entities', 814617, 'in_progress', 1),
('ICIJ Officers', 'icij', 'People/officers', 'icij_officers', 1800000, 'in_progress', 1),
('ICIJ Addresses', 'icij', 'Addresses', 'icij_addresses', 700000, 'in_progress', 1),
('ICIJ Intermediaries', 'icij', 'Intermediaries/brokers', 'icij_intermediaries', 38000, 'in_progress', 1),
('ICIJ Others', 'icij', 'Other entities', 'icij_others', 4000, 'in_progress', 1),
('ICIJ Relationships', 'icij', 'Entity relationships', 'icij_relationships', 3339272, 'in_progress', 1);

-- Insert Other Datasets
INSERT INTO data_inventory (source_name, source_type, description, target_table, expected_records, actual_records, status, priority, imported_at) VALUES
('jMail Emails', 'jmail', 'Email dataset', 'jmail_emails_full', 1783792, 1783792, 'complete', 2, NOW()),
('jMail Documents', 'jmail', 'Document metadata', 'jmail_documents', 1413417, 1413417, 'complete', 2, NOW()),
('FEC Contributions', 'fec', 'Campaign finance data', 'fec_individual_contributions', 5420940, 5420940, 'complete', 3, NOW());

-- Create summary view
CREATE OR REPLACE VIEW v_data_inventory_summary AS
SELECT 
    source_type,
    status,
    COUNT(*) as source_count,
    SUM(expected_records) as total_expected,
    SUM(actual_records) as total_actual,
    CASE WHEN SUM(expected_records) > 0 
         THEN ROUND(100.0 * SUM(actual_records) / SUM(expected_records), 2)
         ELSE 0 
    END as completion_pct
FROM data_inventory
GROUP BY source_type, status
ORDER BY source_type, status;

-- Create overall summary view
CREATE OR REPLACE VIEW v_overall_data_summary AS
SELECT 
    SUM(CASE WHEN status = 'complete' THEN 1 ELSE 0 END) as complete_sources,
    SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress_sources,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending_sources,
    SUM(CASE WHEN status = 'duplicate' THEN 1 ELSE 0 END) as duplicate_sources,
    SUM(actual_records) as total_records_imported,
    SUM(expected_records) as total_records_expected
FROM data_inventory;

-- Create function to refresh actual counts
CREATE OR REPLACE FUNCTION refresh_inventory_counts()
RETURNS TABLE (source_name TEXT, old_count INTEGER, new_count INTEGER) AS $$
DECLARE
    v_count INTEGER;
    v_table TEXT;
    rec RECORD;
BEGIN
    FOR rec IN SELECT di.source_name, di.target_table, di.actual_records 
               FROM data_inventory di 
               WHERE di.target_table IS NOT NULL LOOP
        BEGIN
            EXECUTE format('SELECT COUNT(*)::INTEGER FROM %I', rec.target_table) INTO v_count;
            RETURN QUERY SELECT rec.source_name::TEXT, rec.actual_records::INTEGER, v_count;
            
            UPDATE data_inventory 
            SET actual_records = v_count, 
                last_updated = NOW(),
                status = CASE 
                    WHEN v_count >= rec.expected_records * 0.95 THEN 'complete'
                    WHEN v_count > 0 THEN 'in_progress'
                    ELSE 'pending'
                END
            WHERE source_name = rec.source_name;
        EXCEPTION WHEN OTHERS THEN
            RETURN QUERY SELECT rec.source_name::TEXT, rec.actual_records::INTEGER, 0::INTEGER;
        END;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

SELECT 'Master inventory populated with ' || COUNT(*) || ' data sources' as status
FROM data_inventory;
