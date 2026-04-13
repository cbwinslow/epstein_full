-- Performance Indexes for Epstein Database
-- Creates indexes on frequently queried columns

-- HF Datasets Indexes
CREATE INDEX IF NOT EXISTS idx_hf_files_source ON hf_epstein_files_20k(source_file);
CREATE INDEX IF NOT EXISTS idx_hf_files_date ON hf_epstein_files_20k(date);
CREATE INDEX IF NOT EXISTS idx_hf_files_author ON hf_epstein_files_20k(author);

CREATE INDEX IF NOT EXISTS idx_hf_oversight_source ON hf_house_oversight_docs(source_file);
CREATE INDEX IF NOT EXISTS idx_hf_oversight_doc_type ON hf_house_oversight_docs(doc_type);

CREATE INDEX IF NOT EXISTS idx_hf_ocr_source ON hf_ocr_complete(source_file);
CREATE INDEX IF NOT EXISTS idx_hf_ocr_page ON hf_ocr_complete(page_number);

CREATE INDEX IF NOT EXISTS idx_hf_data_text_source ON hf_epstein_data_text(source_file);

-- ICIJ Indexes (for when data is loaded)
CREATE INDEX IF NOT EXISTS idx_icij_entities_name ON icij_entities(name);
CREATE INDEX IF NOT EXISTS idx_icij_entities_jurisdiction ON icij_entities(jurisdiction);
CREATE INDEX IF NOT EXISTS idx_icij_entities_country ON icij_entities(country_codes);
CREATE INDEX IF NOT EXISTS idx_icij_entities_source ON icij_entities(sourceid);

CREATE INDEX IF NOT EXISTS idx_icij_officers_name ON icij_officers(name);
CREATE INDEX IF NOT EXISTS idx_icij_officers_country ON icij_officers(country_codes);
CREATE INDEX IF NOT EXISTS idx_icij_officers_source ON icij_officers(sourceid);

CREATE INDEX IF NOT EXISTS idx_icij_addresses_country ON icij_addresses(country);
CREATE INDEX IF NOT EXISTS idx_icij_addresses_source ON icij_addresses(sourceid);

CREATE INDEX IF NOT EXISTS idx_icij_intermediaries_name ON icij_intermediaries(name);
CREATE INDEX IF NOT EXISTS idx_icij_intermediaries_country ON icij_intermediaries(country_codes);
CREATE INDEX IF NOT EXISTS idx_icij_intermediaries_source ON icij_intermediaries(sourceid);

CREATE INDEX IF NOT EXISTS idx_icij_others_name ON icij_others(name);
CREATE INDEX IF NOT EXISTS idx_icij_others_source ON icij_others(sourceid);

-- Critical: Relationship indexes for graph queries
CREATE INDEX IF NOT EXISTS idx_icij_rel_start ON icij_relationships(node_id_start);
CREATE INDEX IF NOT EXISTS idx_icij_rel_end ON icij_relationships(node_id_end);
CREATE INDEX IF NOT EXISTS idx_icij_rel_type ON icij_relationships(rel_type);
CREATE INDEX IF NOT EXISTS idx_icij_rel_source ON icij_relationships(sourceid);

-- Full-text search indexes
CREATE INDEX IF NOT EXISTS idx_hf_files_text_search ON hf_epstein_files_20k USING gin(to_tsvector('english', content));
CREATE INDEX IF NOT EXISTS idx_hf_ocr_text_search ON hf_ocr_complete USING gin(to_tsvector('english', text_content));

-- Full Epstein Index indexes
CREATE INDEX IF NOT EXISTS idx_full_index_file ON full_epstein_index(file_name);
CREATE INDEX IF NOT EXISTS idx_full_index_status ON full_epstein_index(processing_status);

-- Analysis queries
CREATE INDEX IF NOT EXISTS idx_hf_files_length ON hf_epstein_files_20k(content_length) WHERE content_length IS NOT NULL;

-- Composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_icij_entities_jur_country ON icij_entities(jurisdiction, country_codes);
CREATE INDEX IF NOT EXISTS idx_icij_officers_country_name ON icij_officers(country_codes, name);

-- Vacuum analyze for statistics
VACUUM ANALYZE hf_epstein_files_20k;
VACUUM ANALYZE hf_house_oversight_docs;
VACUUM ANALYZE hf_ocr_complete;
VACUUM ANALYZE hf_embeddings;
VACUUM ANALYZE hf_epstein_data_text;
VACUUM ANALYZE full_epstein_index;
VACUUM ANALYZE fbi_vault_pages;

SELECT 'Performance indexes created successfully' as status;
