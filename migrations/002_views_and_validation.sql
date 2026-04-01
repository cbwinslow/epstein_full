-- Database Views and Validation Schema
-- Created: March 31, 2026
-- Purpose: Standardized views and constraints for data cleanliness

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Document summary with page count
CREATE OR REPLACE VIEW v_document_summary AS
SELECT 
    d.id,
    d.efta_number,
    d.dataset,
    d.title,
    d.date,
    d.source,
    COUNT(p.id) AS page_count,
    SUM(LENGTH(p.text_content)) AS total_text_length,
    MAX(pe.created_at) AS last_embedded
FROM documents d
LEFT JOIN pages p ON d.id = p.document_id
LEFT JOIN page_embeddings pe ON p.id = pe.page_id
GROUP BY d.id, d.efta_number, d.dataset, d.title, d.date, d.source;

-- View: Pages missing embeddings (for batch processing)
CREATE OR REPLACE VIEW v_pages_missing_embeddings AS
SELECT 
    p.id AS page_id,
    p.efta_number,
    p.page_number,
    p.document_id,
    LEFT(p.text_content, 200) AS text_preview
FROM pages p
LEFT JOIN page_embeddings pe ON p.id = pe.page_id
WHERE pe.page_id IS NULL 
  AND p.text_content IS NOT NULL
  AND LENGTH(p.text_content) > 50;

-- View: Entity frequency across documents
CREATE OR REPLACE VIEW v_entity_frequency AS
SELECT 
    de.entity_text,
    de.entity_label,
    COUNT(DISTINCT de.document_id) AS document_count,
    COUNT(*) AS mention_count
FROM document_entities de
WHERE de.entity_text IS NOT NULL
GROUP BY de.entity_text, de.entity_label
HAVING COUNT(*) > 5
ORDER BY mention_count DESC;

-- View: Cross-reference between emails and documents
CREATE OR REPLACE VIEW v_email_document_links AS
SELECT 
    e.id AS email_id,
    e.sender,
    e.recipients,
    e.subject,
    d.id AS document_id,
    d.efta_number,
    d.title AS document_title
FROM emails e
JOIN documents d ON e.content LIKE '%' || d.efta_number || '%'
WHERE d.efta_number IS NOT NULL;

-- View: Document relationships via entity co-occurrence
CREATE OR REPLACE VIEW v_document_relationships AS
SELECT 
    de1.document_id AS doc1_id,
    de2.document_id AS doc2_id,
    de1.entity_text AS shared_entity,
    de1.entity_label AS entity_type,
    COUNT(*) AS shared_mentions
FROM document_entities de1
JOIN document_entities de2 
    ON de1.entity_text = de2.entity_text 
    AND de1.document_id < de2.document_id
WHERE de1.entity_label IN ('PERSON', 'ORG', 'GPE', 'LAW')
GROUP BY de1.document_id, de2.document_id, de1.entity_text, de1.entity_label
HAVING COUNT(*) >= 2;

-- View: Redaction analysis per document
CREATE OR REPLACE VIEW v_document_redactions AS
SELECT 
    r.document_id,
    d.efta_number,
    COUNT(*) AS redaction_count,
    SUM(CASE WHEN r.redaction_type = 'TEXT' THEN 1 ELSE 0 END) AS text_redactions,
    SUM(CASE WHEN r.redaction_type = 'IMAGE' THEN 1 ELSE 0 END) AS image_redactions,
    STRING_AGG(DISTINCT r.redaction_reason, '; ') AS reasons
FROM redactions r
JOIN documents d ON r.document_id = d.id
GROUP BY r.document_id, d.efta_number;

-- View: Communication network (emails + connections)
CREATE OR REPLACE VIEW v_communication_network AS
SELECT 
    ep.email,
    ep.name,
    ep.entity_type,
    COUNT(DISTINCT ep.email_id) AS email_count,
    STRING_AGG(DISTINCT ep.role, ', ') AS roles
FROM email_participants ep
GROUP BY ep.email, ep.name, ep.entity_type
HAVING COUNT(DISTINCT ep.email_id) > 1
ORDER BY email_count DESC;

-- View: Dataset completeness status
CREATE OR REPLACE VIEW v_dataset_status AS
SELECT 
    dataset,
    COUNT(*) AS document_count,
    SUM(CASE WHEN text_content IS NOT NULL THEN 1 ELSE 0 END) AS with_text,
    SUM(CASE WHEN text_content IS NULL THEN 1 ELSE 0 END) AS missing_text,
    MIN(created_at) AS earliest,
    MAX(created_at) AS latest
FROM documents
GROUP BY dataset
ORDER BY dataset;

-- View: Duplicate detection candidates
CREATE OR REPLACE VIEW v_duplicate_candidates AS
SELECT 
    d1.id AS doc1_id,
    d2.id AS doc2_id,
    d1.efta_number AS efta1,
    d2.efta_number AS efta2,
    d1.sha256_hash,
    similarity(d1.title, d2.title) AS title_similarity
FROM documents d1
JOIN documents d2 
    ON d1.sha256_hash = d2.sha256_hash 
    AND d1.id < d2.id
WHERE d1.sha256_hash IS NOT NULL;

-- View: Persons mentioned across multiple sources
CREATE OR REPLACE VIEW v_cross_source_persons AS
SELECT 
    p.full_name,
    COUNT(DISTINCT p.source_table) AS source_count,
    STRING_AGG(DISTINCT p.source_table, ', ') AS sources,
    SUM(p.mention_count) AS total_mentions
FROM (
    SELECT full_name, 'exposed_persons' AS source_table, 1 AS mention_count FROM exposed_persons
    UNION ALL
    SELECT name, 'entities' AS source_table, mention_count FROM entities WHERE type = 'PERSON'
    UNION ALL
    SELECT entity_text, 'document_entities' AS source_table, COUNT(*) FROM document_entities WHERE entity_label = 'PERSON' GROUP BY entity_text
) p
GROUP BY p.full_name
HAVING COUNT(DISTINCT p.source_table) > 1
ORDER BY source_count DESC, total_mentions DESC;

-- View: Flight passenger analysis
CREATE OR REPLACE VIEW v_flight_analysis AS
SELECT 
    f.tail_number,
    f.date,
    f.origin,
    f.destination,
    f.pilot,
    f.passengers,
    STRING_AGG(DISTINCT p.name, ', ') AS passenger_list,
    COUNT(DISTINCT p.name) AS passenger_count
FROM exposed_flights f
LEFT JOIN LATERAL unnest(string_to_array(f.passengers, ',')) AS p(name) ON true
GROUP BY f.tail_number, f.date, f.origin, f.destination, f.pilot, f.passengers
ORDER BY f.date;

-- ============================================================================
-- DATA VALIDATION FUNCTIONS
-- ============================================================================

-- Function: Validate EFTA number format
CREATE OR REPLACE FUNCTION validate_efta_number(efta TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    -- EFTA format: EFTA + 8 digits
    RETURN efta ~ '^EFTA[0-9]{8}$';
END;
$$ LANGUAGE plpgsql;

-- Function: Check document has required fields
CREATE OR REPLACE FUNCTION check_document_completeness(doc_id INTEGER)
RETURNS TABLE (
    field_name TEXT,
    is_valid BOOLEAN,
    details TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        'EFTa Number'::TEXT,
        d.efta_number IS NOT NULL AND validate_efta_number(d.efta_number),
        CASE 
            WHEN d.efta_number IS NULL THEN 'Missing EFTA number'
            WHEN NOT validate_efta_number(d.efta_number) THEN 'Invalid format: ' || d.efta_number
            ELSE 'Valid'
        END
    FROM documents d WHERE d.id = doc_id
    UNION ALL
    SELECT 
        'Text Content'::TEXT,
        EXISTS(SELECT 1 FROM pages p WHERE p.document_id = doc_id AND p.text_content IS NOT NULL),
        CASE 
            WHEN NOT EXISTS(SELECT 1 FROM pages p WHERE p.document_id = doc_id AND p.text_content IS NOT NULL)
            THEN 'No text content available'
            ELSE 'Has text content'
        END;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS FOR DATA VALIDATION
-- ============================================================================

-- Trigger function: Validate before insert/update on documents
CREATE OR REPLACE FUNCTION validate_document()
RETURNS TRIGGER AS $$
BEGIN
    -- Validate EFTA format
    IF NEW.efta_number IS NOT NULL AND NOT validate_efta_number(NEW.efta_number) THEN
        RAISE EXCEPTION 'Invalid EFTA number format: %', NEW.efta_number;
    END IF;
    
    -- Set default source if not provided
    IF NEW.source IS NULL THEN
        NEW.source := 'imported';
    END IF;
    
    -- Update timestamp
    NEW.updated_at := NOW();
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger (uncomment when ready)
-- CREATE TRIGGER trg_validate_document
--     BEFORE INSERT OR UPDATE ON documents
--     FOR EACH ROW EXECUTE FUNCTION validate_document();

-- ============================================================================
-- INDEXES FOR VIEW PERFORMANCE
-- ============================================================================

-- Index for entity lookups
CREATE INDEX IF NOT EXISTS idx_document_entities_text_label 
ON document_entities(entity_text, entity_label);

-- Index for email searches
CREATE INDEX IF NOT EXISTS idx_emails_content_gin 
ON emails USING gin(to_tsvector('english', content));

-- Index for page text search
CREATE INDEX IF NOT EXISTS idx_pages_text_gin 
ON pages USING gin(to_tsvector('english', text_content));

-- ============================================================================
-- CONSTRAINTS TO ADD (review before applying)
-- ============================================================================

-- Add NOT NULL constraints where appropriate
-- ALTER TABLE documents ALTER COLUMN dataset SET NOT NULL;

-- Add check constraints
-- ALTER TABLE documents ADD CONSTRAINT chk_efta_format CHECK (efta_number IS NULL OR efta_number ~ '^EFTA[0-9]{8}$');

-- Add foreign key relationships (verify data integrity first)
-- ALTER TABLE pages ADD CONSTRAINT fk_pages_documents 
--     FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

-- ALTER TABLE document_entities ADD CONSTRAINT fk_doc_entities_documents 
--     FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON VIEW v_document_summary IS 'Summary of documents with page counts and embedding status';
COMMENT ON VIEW v_pages_missing_embeddings IS 'Pages ready for embedding generation';
COMMENT ON VIEW v_entity_frequency IS 'Most frequently mentioned entities across documents';
COMMENT ON VIEW v_document_relationships IS 'Documents connected by shared entity mentions';
COMMENT ON VIEW v_cross_source_persons IS 'Persons appearing in multiple data sources';

COMMENT ON FUNCTION validate_efta_number IS 'Validates EFTA number format (EFTA + 8 digits)';
COMMENT ON FUNCTION check_document_completeness IS 'Returns validation status for a document';
