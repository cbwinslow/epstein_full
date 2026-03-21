-- =============================================================================
-- Epstein Files Analysis — Unified PostgreSQL Schema
-- =============================================================================
-- Single database containing all 8 SQLite databases unified.
-- Extensions: vector (pgvector 0.6+), pg_trgm, unaccent, pg_stat_statements
-- =============================================================================

BEGIN;

-- =============================================================================
-- CORE DOCUMENT TABLES
-- =============================================================================

-- Master document registry (from full_text_corpus.db:documents)
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12) UNIQUE NOT NULL,
    dataset INTEGER,
    file_path TEXT,
    total_pages INTEGER DEFAULT 1,
    file_size INTEGER,
    pdf_url TEXT,
    error TEXT,
    extraction_timestamp TEXT,
    -- Enrichment columns
    document_type VARCHAR(50),
    classification_confidence REAL,
    has_redactions BOOLEAN DEFAULT FALSE,
    has_transcript BOOLEAN DEFAULT FALSE,
    has_image_analysis BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document pages with FTS and vector search (from full_text_corpus.db:pages)
CREATE TABLE IF NOT EXISTS pages (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12) NOT NULL,
    page_number INTEGER NOT NULL,
    text_content TEXT,
    char_count INTEGER,
    -- FTS vector (auto-computed)
    search_vector tsvector,
    -- Vector embedding (to be populated)
    embedding vector(768),
    -- OCR metadata
    ocr_confidence REAL,
    ocr_backend VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(efta_number, page_number)
);

-- Document classification (from full_text_corpus.db:document_classification)
CREATE TABLE IF NOT EXISTS document_classification (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12) UNIQUE NOT NULL,
    dataset INTEGER,
    doc_type VARCHAR(50),
    doc_type_confidence REAL,
    max_char_count INTEGER,
    total_pages INTEGER,
    has_redactions INTEGER DEFAULT 0,
    redaction_count INTEGER DEFAULT 0,
    has_image_analysis INTEGER DEFAULT 0,
    has_ocr INTEGER DEFAULT 0,
    has_transcript INTEGER DEFAULT 0,
    has_concordance INTEGER DEFAULT 0,
    classified_at TEXT
);

-- EFTA crosswalk (from full_text_corpus.db:efta_crosswalk)
CREATE TABLE IF NOT EXISTS efta_crosswalk (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12) UNIQUE NOT NULL,
    dataset INTEGER,
    total_pages INTEGER,
    max_char_count INTEGER,
    in_concordance INTEGER DEFAULT 0,
    concordance_extension TEXT,
    concordance_filename TEXT,
    in_redaction_db INTEGER DEFAULT 0,
    redaction_total INTEGER DEFAULT 0,
    redaction_proper INTEGER DEFAULT 0,
    redaction_text_near INTEGER DEFAULT 0,
    redaction_has_ocr INTEGER DEFAULT 0,
    in_image_analysis INTEGER DEFAULT 0,
    in_ocr_db INTEGER DEFAULT 0,
    in_transcripts INTEGER DEFAULT 0,
    doc_type TEXT,
    doc_type_confidence REAL
);

-- =============================================================================
-- ENTITY & KNOWLEDGE GRAPH TABLES
-- =============================================================================

-- Entities (from knowledge_graph.db:entities)
CREATE TABLE IF NOT EXISTS entities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    entity_type VARCHAR(50),
    source_id INTEGER,
    source_table TEXT,
    aliases JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    mention_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relationships (from knowledge_graph.db:relationships)
CREATE TABLE IF NOT EXISTS relationships (
    id SERIAL PRIMARY KEY,
    source_entity_id INTEGER REFERENCES entities(id),
    target_entity_id INTEGER REFERENCES entities(id),
    relationship_type VARCHAR(50) NOT NULL,
    weight REAL DEFAULT 1.0,
    date_first TEXT,
    date_last TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Edge sources (from knowledge_graph.db:edge_sources)
CREATE TABLE IF NOT EXISTS edge_sources (
    id SERIAL PRIMARY KEY,
    relationship_id INTEGER REFERENCES relationships(id),
    source_type TEXT,
    source_id INTEGER,
    source_detail TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================================================
-- COMMUNICATION TABLES
-- =============================================================================

-- Emails (from communications.db:emails)
CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12),
    dataset INTEGER,
    page_number INTEGER,
    source TEXT,
    from_name TEXT,
    from_email TEXT,
    to_raw TEXT,
    cc_raw TEXT,
    subject TEXT,
    date_sent TEXT,
    date_normalized TEXT,
    is_noise INTEGER DEFAULT 0,
    parse_confidence REAL
);

-- Email participants (from communications.db:email_participants)
CREATE TABLE IF NOT EXISTS email_participants (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id),
    role VARCHAR(20),  -- 'from', 'to', 'cc'
    name TEXT,
    email_address TEXT,
    resolved_entity_id INTEGER
);

-- Resolved identities (from communications.db:resolved_identities)
CREATE TABLE IF NOT EXISTS resolved_identities (
    id SERIAL PRIMARY KEY,
    raw_name TEXT,
    raw_email TEXT,
    canonical_name TEXT,
    person_registry_slug TEXT,
    kg_entity_id INTEGER,
    confidence REAL,
    match_method TEXT
);

-- Communication pairs (from communications.db:communication_pairs)
CREATE TABLE IF NOT EXISTS communication_pairs (
    id SERIAL PRIMARY KEY,
    person_a TEXT,
    person_b TEXT,
    email_count INTEGER,
    first_date TEXT,
    last_date TEXT,
    a_to_b_count INTEGER,
    b_to_a_count INTEGER,
    sample_subjects TEXT,
    sample_eftas TEXT
);

-- =============================================================================
-- REDACTION TABLES
-- =============================================================================

-- Redactions (from redaction_analysis_v2.db:redactions)
CREATE TABLE IF NOT EXISTS redactions (
    id SERIAL PRIMARY KEY,
    pdf_path TEXT,
    efta_number VARCHAR(12),
    page_number INTEGER,
    redaction_type VARCHAR(20),  -- 'proper', 'bad_overlay', 'recoverable'
    rect_x0 REAL,
    rect_y0 REAL,
    rect_x1 REAL,
    rect_y1 REAL,
    ocr_text TEXT,
    confidence REAL,
    detected_at TEXT,
    dataset_source TEXT
);

-- Document redaction summary (from redaction_analysis_v2.db:document_summary)
CREATE TABLE IF NOT EXISTS document_summary (
    id SERIAL PRIMARY KEY,
    pdf_path TEXT,
    efta_number VARCHAR(12),
    total_redactions INTEGER,
    text_near_bar_count INTEGER,
    proper_redactions INTEGER,
    has_ocr_text BOOLEAN DEFAULT FALSE,
    scanned_at TEXT,
    dataset_source TEXT
);

-- Reconstructed pages (from redaction_analysis_v2.db:reconstructed_pages)
CREATE TABLE IF NOT EXISTS reconstructed_pages (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12),
    page_number INTEGER,
    num_fragments INTEGER,
    reconstructed_text TEXT,
    document_type TEXT,
    interest_score REAL,
    names_found TEXT,
    dataset_source TEXT
);

-- Extracted entities from redaction context (from redaction_analysis_v2.db:extracted_entities)
CREATE TABLE IF NOT EXISTS redaction_entities (
    id SERIAL PRIMARY KEY,
    source_redaction_id INTEGER,
    efta_number VARCHAR(12),
    page_number INTEGER,
    entity_type TEXT,
    entity_value TEXT,
    context TEXT,
    dataset_source TEXT
);

-- =============================================================================
-- MEDIA TABLES
-- =============================================================================

-- Images (from image_analysis.db:images)
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    image_name TEXT,
    efta_number VARCHAR(12),
    source_pdf TEXT,
    page_number INTEGER,
    analysis_text TEXT,
    people TEXT,
    text_content TEXT,
    objects TEXT,
    setting TEXT,
    activity TEXT,
    notable TEXT,
    analyzed_at TEXT
);

-- OCR results (from ocr_database.db:ocr_results)
CREATE TABLE IF NOT EXISTS ocr_results (
    id SERIAL PRIMARY KEY,
    image_path TEXT,
    efta_number VARCHAR(12),
    ocr_text TEXT,
    orientation INTEGER,
    processed_at TEXT
);

-- Transcripts (from transcripts.db:transcripts)
CREATE TABLE IF NOT EXISTS transcripts (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12) UNIQUE,
    file_path TEXT,
    file_type VARCHAR(10),
    duration_secs REAL,
    language VARCHAR(10),
    language_prob REAL,
    transcript TEXT,
    word_count INTEGER,
    dataset_source TEXT,
    transcribed_at TEXT
);

-- Transcript segments (from transcripts.db:transcript_segments)
CREATE TABLE IF NOT EXISTS transcript_segments (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12),
    segment_id INTEGER,
    start_time REAL,
    end_time REAL,
    text TEXT
);

-- =============================================================================
-- LEGAL/SUBPOENA TABLES
-- =============================================================================

-- Subpoenas (from prosecutorial_query_graph.db:subpoenas)
CREATE TABLE IF NOT EXISTS subpoenas (
    id SERIAL PRIMARY KEY,
    efta_number VARCHAR(12),
    target TEXT,
    target_category TEXT,
    date_issued TEXT,
    statutes TEXT,
    total_pages INTEGER,
    rider_page_numbers TEXT,
    full_rider_text TEXT,
    clause_count INTEGER
);

-- Subpoena rider clauses (from prosecutorial_query_graph.db:rider_clauses)
CREATE TABLE IF NOT EXISTS rider_clauses (
    id SERIAL PRIMARY KEY,
    subpoena_id INTEGER REFERENCES subpoenas(id),
    clause_number INTEGER,
    clause_text TEXT,
    data_class TEXT,
    date_range_start TEXT,
    date_range_end TEXT,
    target_accounts TEXT
);

-- Document returns (from prosecutorial_query_graph.db:returns)
CREATE TABLE IF NOT EXISTS returns (
    id SERIAL PRIMARY KEY,
    source TEXT,
    production_id INTEGER,
    sdny_bates_start TEXT,
    sdny_bates_end TEXT,
    efta_range_start TEXT,
    efta_range_end TEXT,
    page_count INTEGER,
    description TEXT,
    date_received TEXT,
    responding_entity TEXT
);

-- Subpoena-return links (from prosecutorial_query_graph.db:subpoena_return_links)
CREATE TABLE IF NOT EXISTS subpoena_return_links (
    id SERIAL PRIMARY KEY,
    subpoena_id INTEGER REFERENCES subpoenas(id),
    return_id INTEGER REFERENCES returns(id),
    confidence TEXT,
    match_method TEXT,
    match_evidence TEXT
);

-- Clause fulfillment (from prosecutorial_query_graph.db:clause_fulfillment)
CREATE TABLE IF NOT EXISTS clause_fulfillment (
    id SERIAL PRIMARY KEY,
    clause_id INTEGER REFERENCES rider_clauses(id),
    return_id INTEGER REFERENCES returns(id),
    status TEXT,
    evidence TEXT,
    page_count_relevant INTEGER,
    notes TEXT
);

-- Graph nodes (from prosecutorial_query_graph.db:graph_nodes)
CREATE TABLE IF NOT EXISTS graph_nodes (
    id SERIAL PRIMARY KEY,
    node_type TEXT,
    node_id TEXT,
    label TEXT,
    properties TEXT
);

-- Graph edges (from prosecutorial_query_graph.db:graph_edges)
CREATE TABLE IF NOT EXISTS graph_edges (
    id SERIAL PRIMARY KEY,
    source_node INTEGER,
    target_node INTEGER,
    edge_type TEXT,
    weight REAL,
    properties TEXT
);

-- Investigative gaps (from prosecutorial_query_graph.db:investigative_gaps)
CREATE TABLE IF NOT EXISTS investigative_gaps (
    id SERIAL PRIMARY KEY,
    gap_type TEXT,
    severity TEXT,
    description TEXT,
    related_subpoena_ids TEXT,
    related_clause_ids TEXT,
    evidence TEXT
);

-- =============================================================================
-- FILE REGISTRY (NEW — for dedup and cross-reference)
-- =============================================================================

CREATE TABLE IF NOT EXISTS file_registry (
    id SERIAL PRIMARY KEY,
    file_path TEXT NOT NULL,
    sha256_hash VARCHAR(64),
    efta_number VARCHAR(12),
    dataset INTEGER,
    file_size_bytes BIGINT,
    source VARCHAR(50),  -- 'doj', 'hf', 'cdn', 'archive_org', 'prebuilt'
    downloaded_at TIMESTAMP,
    validated BOOLEAN DEFAULT FALSE,
    notes TEXT
);
CREATE INDEX IF NOT EXISTS idx_file_registry_hash ON file_registry(sha256_hash);
CREATE INDEX IF NOT EXISTS idx_file_registry_efta ON file_registry(efta_number);
CREATE INDEX IF NOT EXISTS idx_file_registry_source ON file_registry(source);

-- =============================================================================
-- EXTERNAL REFERENCES (NEW — for cross-referencing external data)
-- =============================================================================

CREATE TABLE IF NOT EXISTS external_references (
    id SERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    external_source VARCHAR(50),  -- 'icij', 'fec', 'opensanctions', 'courtlistener', 'wikidata'
    external_id TEXT,
    external_url TEXT,
    confidence REAL DEFAULT 0.0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_external_refs_entity ON external_references(entity_id);
CREATE INDEX IF NOT EXISTS idx_external_refs_source ON external_references(external_source);

-- =============================================================================
-- TRACKER TABLES (for progress tracking)
-- =============================================================================

CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    type TEXT DEFAULT 'download',
    expected INTEGER DEFAULT 0,
    current INTEGER DEFAULT 0,
    rate_bps REAL DEFAULT 0,
    status TEXT DEFAULT 'running',
    started_at TEXT,
    last_update TEXT,
    finished_at TEXT
);

CREATE TABLE IF NOT EXISTS task_history (
    id SERIAL PRIMARY KEY,
    task_id TEXT,
    ts TEXT NOT NULL,
    value INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_task_history_ts ON task_history(task_id, ts DESC);

-- =============================================================================
-- INDEXES (FTS, Vector, Performance)
-- =============================================================================

-- Pages FTS
CREATE INDEX IF NOT EXISTS idx_pages_efta ON pages(efta_number);
CREATE INDEX IF NOT EXISTS idx_pages_search ON pages USING GIN (search_vector);

-- Vector similarity (HNSW) — built after data migration
-- CREATE INDEX IF NOT EXISTS idx_pages_embedding ON pages USING hnsw (embedding vector_cosine_ops);

-- Entity/relationship lookups
CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_name_trgm ON entities USING GIN (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);
CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);
CREATE INDEX IF NOT EXISTS idx_relationships_type ON relationships(relationship_type);

-- Email lookups
CREATE INDEX IF NOT EXISTS idx_emails_efta ON emails(efta_number);
CREATE INDEX IF NOT EXISTS idx_emails_from ON emails(from_email);
CREATE INDEX IF NOT EXISTS idx_emails_date ON emails(date_normalized);

-- Redaction lookups
CREATE INDEX IF NOT EXISTS idx_redactions_efta ON redactions(efta_number);
CREATE INDEX IF NOT EXISTS idx_redactions_type ON redactions(redaction_type);

-- Image/OCR lookups
CREATE INDEX IF NOT EXISTS idx_images_efta ON images(efta_number);
CREATE INDEX IF NOT EXISTS idx_ocr_efta ON ocr_results(efta_number);
CREATE INDEX IF NOT EXISTS idx_transcripts_efta ON transcripts(efta_number);

-- Document classification
CREATE INDEX IF NOT EXISTS idx_doc_class_efta ON document_classification(efta_number);
CREATE INDEX IF NOT EXISTS idx_doc_class_type ON document_classification(doc_type);
CREATE INDEX IF NOT EXISTS idx_crosswalk_efta ON efta_crosswalk(efta_number);

-- =============================================================================
-- FUNCTIONS
-- =============================================================================

-- Auto-compute search_vector on insert/update
CREATE OR REPLACE FUNCTION pages_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.efta_number, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.text_content, '')), 'B');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER pages_search_update
    BEFORE INSERT OR UPDATE ON pages
    FOR EACH ROW EXECUTE FUNCTION pages_search_trigger();

-- Fuzzy name search function
CREATE OR REPLACE FUNCTION search_entities_fuzzy(query TEXT, threshold REAL DEFAULT 0.3)
RETURNS TABLE(id INTEGER, name TEXT, entity_type TEXT, similarity REAL) AS $$
BEGIN
    RETURN QUERY
    SELECT e.id, e.name, e.entity_type, similarity(e.name, query) AS sim
    FROM entities e
    WHERE similarity(e.name, query) > threshold
    ORDER BY sim DESC
    LIMIT 20;
END
$$ LANGUAGE plpgsql;

COMMIT;
