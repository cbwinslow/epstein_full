-- Epstein Database Schema
-- PostgreSQL database for Epstein case investigation data

-- ============================================================================
-- CORE ENTITIES
-- ============================================================================

-- Documents table - Main document repository
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    efta_number TEXT UNIQUE NOT NULL,
    document_type TEXT,
    title TEXT,
    description TEXT,
    date_created DATE,
    date_modified DATE,
    source_system TEXT DEFAULT 'doj',
    status TEXT DEFAULT 'active',
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Pages table - Individual document pages
CREATE TABLE pages (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    efta_number TEXT NOT NULL,
    page_number INTEGER NOT NULL,
    text_content TEXT,
    ocr_confidence REAL,
    image_path TEXT,
    page_type TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(efta_number, page_number)
);

-- Entities table - People, organizations, locations
CREATE TABLE entities (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    entity_type TEXT NOT NULL, -- 'person', 'organization', 'location'
    description TEXT,
    aliases TEXT[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(name, entity_type)
);

-- Relationships table - Connections between entities
CREATE TABLE relationships (
    id SERIAL PRIMARY KEY,
    source_entity_id INTEGER REFERENCES entities(id),
    target_entity_id INTEGER REFERENCES entities(id),
    relationship_type TEXT NOT NULL,
    description TEXT,
    confidence REAL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- MEDIA ACQUISITION (Phase 22)
-- ============================================================================

-- News articles table
CREATE TABLE media_news_articles (
    id SERIAL PRIMARY KEY,
    article_url TEXT UNIQUE NOT NULL,
    title TEXT,
    author TEXT[],
    publish_date DATE,
    content TEXT,
    word_count INTEGER,
    language TEXT,
    source_domain TEXT,
    discovery_source TEXT, -- 'gdelt', 'rss', 'manual'
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Transcripts table
CREATE TABLE transcripts (
    id SERIAL PRIMARY KEY,
    efta_number TEXT NOT NULL,
    media_type TEXT, -- 'video', 'audio'
    duration_seconds INTEGER,
    text_content TEXT,
    speaker_segments JSONB,
    confidence REAL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Images table
CREATE TABLE images (
    id SERIAL PRIMARY KEY,
    efta_number TEXT NOT NULL,
    image_path TEXT UNIQUE NOT NULL,
    description TEXT,
    detected_objects JSONB,
    face_detection JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- COMMUNICATIONS
-- ============================================================================

-- Emails table
CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    efta_number TEXT NOT NULL,
    from_name TEXT,
    from_email TEXT,
    to_names TEXT[],
    to_emails TEXT[],
    cc_names TEXT[],
    cc_emails TEXT[],
    bcc_names TEXT[],
    bcc_emails TEXT[],
    subject TEXT,
    body_text TEXT,
    body_html TEXT,
    sent_date TIMESTAMP,
    received_date TIMESTAMP,
    attachments JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Email participants table
CREATE TABLE email_participants (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails(id),
    participant_name TEXT,
    participant_email TEXT,
    participant_type TEXT, -- 'to', 'cc', 'bcc'
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- LEGAL & SUBPOENA
-- ============================================================================

-- Subpoenas table
CREATE TABLE subpoenas (
    id SERIAL PRIMARY KEY,
    subpoena_number TEXT UNIQUE NOT NULL,
    issued_to TEXT,
    issued_by TEXT,
    issue_date DATE,
    due_date DATE,
    status TEXT,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Rider clauses table
CREATE TABLE rider_clauses (
    id SERIAL PRIMARY KEY,
    subpoena_id INTEGER REFERENCES subpoenas(id),
    clause_number TEXT,
    clause_text TEXT,
    clause_type TEXT,
    status TEXT,
    fulfillment_status TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Clause fulfillment table
CREATE TABLE clause_fulfillment (
    id SERIAL PRIMARY KEY,
    clause_id INTEGER REFERENCES rider_clauses(id),
    return_id INTEGER REFERENCES returns(id),
    fulfillment_date DATE,
    status TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Returns table
CREATE TABLE returns (
    id SERIAL PRIMARY KEY,
    return_number TEXT UNIQUE NOT NULL,
    received_date DATE,
    received_by TEXT,
    status TEXT,
    description TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- FINANCIAL DATA
-- ============================================================================

-- Credit card transactions table
CREATE TABLE financial_transactions (
    id SERIAL PRIMARY KEY,
    efta_number TEXT NOT NULL,
    transaction_date DATE,
    amount DECIMAL(10,2),
    currency TEXT,
    merchant_name TEXT,
    merchant_category TEXT,
    cardholder_name TEXT,
    card_last_four TEXT,
    transaction_type TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- FEC campaign finance table
CREATE TABLE fec_contributions (
    id SERIAL PRIMARY KEY,
    contributor_name TEXT,
    contributor_address TEXT,
    contributor_city TEXT,
    contributor_state TEXT,
    contributor_zip TEXT,
    contributor_employer TEXT,
    contributor_occupation TEXT,
    recipient_name TEXT,
    recipient_party TEXT,
    recipient_state TEXT,
    election_type TEXT,
    contribution_date DATE,
    contribution_amount DECIMAL(10,2),
    contribution_type TEXT,
    memo_text TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- SEC EDGAR filings table
CREATE TABLE sec_filings (
    id SERIAL PRIMARY KEY,
    filing_date DATE,
    filing_type TEXT,
    company_name TEXT,
    company_ticker TEXT,
    company_cik TEXT,
    filing_number TEXT,
    filing_url TEXT,
    filing_text TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- REDACTION & RECONSTRUCTION
-- ============================================================================

-- Redactions table
CREATE TABLE redactions (
    id SERIAL PRIMARY KEY,
    efta_number TEXT NOT NULL,
    page_number INTEGER,
    redaction_type TEXT, -- 'text', 'image', 'metadata'
    redaction_reason TEXT,
    redaction_text TEXT,
    confidence REAL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Reconstruction table
CREATE TABLE reconstructions (
    id SERIAL PRIMARY KEY,
    efta_number TEXT NOT NULL,
    reconstruction_method TEXT,
    reconstructed_text TEXT,
    confidence REAL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- VECTOR EMBEDDINGS
-- ============================================================================

-- Document embeddings table
CREATE TABLE document_embeddings (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    embedding_vector FLOAT8[] NOT NULL,
    embedding_model TEXT,
    embedding_date TIMESTAMP DEFAULT NOW(),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Page embeddings table
CREATE TABLE page_embeddings (
    id SERIAL PRIMARY KEY,
    page_id INTEGER REFERENCES pages(id),
    embedding_vector FLOAT8[] NOT NULL,
    embedding_model TEXT,
    embedding_date TIMESTAMP DEFAULT NOW(),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Entity embeddings table
CREATE TABLE entity_embeddings (
    id SERIAL PRIMARY KEY,
    entity_id INTEGER REFERENCES entities(id),
    embedding_vector FLOAT8[] NOT NULL,
    embedding_model TEXT,
    embedding_date TIMESTAMP DEFAULT NOW(),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- SYSTEM & METADATA
-- ============================================================================

-- Processing jobs table
CREATE TABLE processing_jobs (
    id SERIAL PRIMARY KEY,
    job_type TEXT NOT NULL, -- 'download', 'ocr', 'ner', 'embed'
    source_system TEXT,
    status TEXT DEFAULT 'pending',
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    progress INTEGER DEFAULT 0,
    total_items INTEGER DEFAULT 0,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Data quality checks table
CREATE TABLE data_quality_checks (
    id SERIAL PRIMARY KEY,
    check_type TEXT NOT NULL, -- 'duplicate', 'foreign_key', 'completeness'
    table_name TEXT,
    column_name TEXT,
    check_date TIMESTAMP DEFAULT NOW(),
    passed BOOLEAN,
    details TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Document indexes
CREATE INDEX idx_documents_efta_number ON documents(efta_number);
CREATE INDEX idx_documents_source_system ON documents(source_system);
CREATE INDEX idx_documents_status ON documents(status);

-- Page indexes
CREATE INDEX idx_pages_efta_number ON pages(efta_number);
CREATE INDEX idx_pages_document_id ON pages(document_id);
CREATE INDEX idx_pages_page_number ON pages(page_number);

-- Entity indexes
CREATE INDEX idx_entities_name ON entities(name);
CREATE INDEX idx_entities_entity_type ON entities(entity_type);
CREATE INDEX idx_entities_aliases ON entities USING GIN (aliases);

-- Relationship indexes
CREATE INDEX idx_relationships_source_entity_id ON relationships(source_entity_id);
CREATE INDEX idx_relationships_target_entity_id ON relationships(target_entity_id);
CREATE INDEX idx_relationships_relationship_type ON relationships(relationship_type);

-- Email indexes
CREATE INDEX idx_emails_efta_number ON emails(efta_number);
CREATE INDEX idx_emails_from_email ON emails USING HASH (from_email);
CREATE INDEX idx_emails_to_emails ON emails USING GIN (to_emails);

-- FEC indexes
CREATE INDEX idx_fec_contributions_contributor_name ON fec_contributions(contributor_name);
CREATE INDEX idx_fec_contributions_recipient_name ON fec_contributions(recipient_name);
CREATE INDEX idx_fec_contributions_contribution_date ON fec_contributions(contribution_date);

-- Vector indexes (for pgvector)
-- CREATE INDEX idx_document_embeddings_vector ON document_embeddings 
-- USING ivfflat (embedding_vector vector_cosine_ops) WITH (lists = 100);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Document summary view
CREATE VIEW document_summary AS
SELECT 
    d.id,
    d.efta_number,
    d.document_type,
    d.title,
    COUNT(p.id) as page_count,
    d.status,
    d.source_system,
    d.created_at
FROM documents d
LEFT JOIN pages p ON d.id = p.document_id
GROUP BY d.id, d.efta_number, d.document_type, d.title, d.status, d.source_system, d.created_at;

-- Entity relationship view
CREATE VIEW entity_relationships AS
SELECT 
    e1.name as source_name,
    e1.entity_type as source_type,
    r.relationship_type,
    e2.name as target_name,
    e2.entity_type as target_type,
    r.confidence,
    r.created_at
FROM relationships r
JOIN entities e1 ON r.source_entity_id = e1.id
JOIN entities e2 ON r.target_entity_id = e2.id;

-- Email summary view
CREATE VIEW email_summary AS
SELECT 
    e.id,
    e.efta_number,
    e.from_name,
    e.subject,
    COUNT(ep.id) as recipient_count,
    e.sent_date,
    e.status
FROM emails e
LEFT JOIN email_participants ep ON e.id = ep.email_id
GROUP BY e.id, e.efta_number, e.from_name, e.subject, e.sent_date, e.status;

-- ============================================================================
-- CONSTRAINTS
-- ============================================================================

-- Foreign key constraints
ALTER TABLE pages ADD CONSTRAINT fk_pages_document_id 
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE;

ALTER TABLE relationships ADD CONSTRAINT fk_relationships_source_entity_id 
    FOREIGN KEY (source_entity_id) REFERENCES entities(id) ON DELETE CASCADE;

ALTER TABLE relationships ADD CONSTRAINT fk_relationships_target_entity_id 
    FOREIGN KEY (target_entity_id) REFERENCES entities(id) ON DELETE CASCADE;

ALTER TABLE email_participants ADD CONSTRAINT fk_email_participants_email_id 
    FOREIGN KEY (email_id) REFERENCES emails(id) ON DELETE CASCADE;

ALTER TABLE rider_clauses ADD CONSTRAINT fk_rider_clauses_subpoena_id 
    FOREIGN KEY (subpoena_id) REFERENCES subpoenas(id) ON DELETE CASCADE;

ALTER TABLE clause_fulfillment ADD CONSTRAINT fk_clause_fulfillment_clause_id 
    FOREIGN KEY (clause_id) REFERENCES rider_clauses(id) ON DELETE CASCADE;

ALTER TABLE clause_fulfillment ADD CONSTRAINT fk_clause_fulfillment_return_id 
    FOREIGN KEY (return_id) REFERENCES returns(id) ON DELETE SET NULL;

-- ============================================================================
-- TRIGGERS FOR AUDIT TRAIL
-- ============================================================================

-- Update timestamp on documents
CREATE OR REPLACE FUNCTION update_document_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_document_update 
    BEFORE UPDATE ON documents 
    FOR EACH ROW EXECUTE FUNCTION update_document_timestamp();

-- Update timestamp on pages
CREATE TRIGGER trigger_page_update 
    BEFORE UPDATE ON pages 
    FOR EACH ROW EXECUTE FUNCTION update_document_timestamp();

-- Update timestamp on entities
CREATE TRIGGER trigger_entity_update 
    BEFORE UPDATE ON entities 
    FOR EACH ROW EXECUTE FUNCTION update_document_timestamp();

-- Update timestamp on relationships
CREATE TRIGGER trigger_relationship_update 
    BEFORE UPDATE ON relationships 
    FOR EACH ROW EXECUTE FUNCTION update_document_timestamp();