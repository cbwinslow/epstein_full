-- Data integrity views for Epstein database

-- View: documents_missing_content
-- Documents that should have content but don't
CREATE OR REPLACE VIEW documents_missing_content AS
SELECT d.id, d.efta_number, d.file_path, d.total_pages
FROM documents d
LEFT JOIN documents_content dc ON d.id = dc.document_id
WHERE dc.document_id IS NULL
  AND d.total_pages > 0;

-- View: pages_missing_text
-- Pages that should have text but don't
CREATE OR REPLACE VIEW pages_missing_text AS
SELECT p.id, p.efta_number, p.page_number
FROM pages p
WHERE (p.text_content IS NULL OR length(trim(p.text_content)) < 10)
  AND p.page_number > 0;

-- View: embeddings_coverage
-- Coverage of different embedding types (page_embeddings table)
CREATE OR REPLACE VIEW embeddings_coverage AS
SELECT
  'page_embeddings' as table_name,
  COUNT(*) as total_embeddings,
  COUNT(DISTINCT page_id) as unique_pages,
  model_name,
  COUNT(*) as count_per_model
FROM page_embeddings
GROUP BY model_name;

-- View: entity_extraction_stats
-- Statistics on extracted entities
CREATE OR REPLACE VIEW entity_extraction_stats AS
SELECT
  entity_type,
  COUNT(*) as count,
  AVG(document_count) as avg_docs_per_entity
FROM extracted_entities
GROUP BY entity_type
ORDER BY count DESC;

-- View: redaction_analysis_summary
-- Summary of redaction types and patterns
CREATE OR REPLACE VIEW redaction_analysis_summary AS
SELECT
  redaction_type,
  COUNT(*) as count,
  AVG(length(ocr_text)) as avg_text_length,
  COUNT(DISTINCT efta_number) as documents_affected
FROM redactions
WHERE ocr_text IS NOT NULL
GROUP BY redaction_type
ORDER BY count DESC;

-- View: knowledge_graph_stats
-- Statistics on knowledge graph
CREATE OR REPLACE VIEW knowledge_graph_stats AS
SELECT
  'entities' as type, COUNT(*) as count FROM entities
UNION ALL
SELECT 'relationships' as type, COUNT(*) as count FROM relationships
UNION ALL
SELECT 'nodes' as type, COUNT(*) as count FROM graph_nodes
UNION ALL
SELECT 'edges' as type, COUNT(*) as count FROM graph_edges;

-- View: file_registry_validation
-- Check file registry integrity
CREATE OR REPLACE VIEW file_registry_validation AS
SELECT
  fr.source,
  COUNT(*) as total_files,
  COUNT(CASE WHEN fr.sha256_hash IS NOT NULL THEN 1 END) as hashed_files,
  COUNT(CASE WHEN fr.validated THEN 1 END) as validated_files,
  ROUND(100.0 * COUNT(CASE WHEN fr.validated THEN 1 END) / COUNT(*), 2) as validation_pct
FROM file_registry fr
GROUP BY fr.source;

-- View: embedding_datasets_comparison
-- Compare different embedding datasets
CREATE OR REPLACE VIEW embedding_datasets_comparison AS
SELECT 'kabasshouse' as dataset, COUNT(*) as chunks, '768-dim Gemini' as model FROM kabasshouse_chunk_embeddings
UNION ALL
SELECT 'fbi' as dataset, COUNT(*) as chunks, '768-dim nomic' as model FROM fbi_embeddings
UNION ALL
SELECT 'house_oversight' as dataset, COUNT(*) as chunks, '768-dim nomic' as model FROM house_oversight_embeddings
UNION ALL
SELECT 'page_embeddings' as dataset, COUNT(DISTINCT page_id) as pages, model_name as model FROM page_embeddings GROUP BY model_name;