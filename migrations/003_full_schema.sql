-- PostgreSQL Schema for Epstein Document Analysis
-- Creates all tables needed for cross-referencing with EpsteinExposed

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- For text search

-- Main documents table
CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    efta_id VARCHAR(20) UNIQUE NOT NULL,  -- EFTA00000001 format
    dataset VARCHAR(20) NOT NULL,  -- data1, data10, etc.
    filename VARCHAR(255) NOT NULL,
    filepath TEXT NOT NULL,
    file_size BIGINT,
    file_hash VARCHAR(64),  -- SHA256
    page_count INTEGER,
    document_type VARCHAR(50),  -- court_filing, deposition, email, etc.
    classification VARCHAR(100),
    extraction_status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Pages table (extracted text per page)
CREATE TABLE IF NOT EXISTS pages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    page_number INTEGER NOT NULL,
    ocr_text TEXT,
    ocr_confidence FLOAT,
    extracted_text TEXT,  -- Cleaned/extracted text
    has_redactions BOOLEAN DEFAULT FALSE,
    redaction_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(document_id, page_number)
);

-- Named entities table
CREATE TABLE IF NOT EXISTS entities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50) NOT NULL,  -- person, organization, location, date, amount
    normalized_name VARCHAR(255),
    aliases JSONB,  -- Array of alternative names
    category VARCHAR(50),  -- victim, perpetrator, witness, associate, etc.
    confidence FLOAT DEFAULT 1.0,
    source VARCHAR(50),  -- spaCy, GLiNER, regex, manual
    document_count INTEGER DEFAULT 0,
    mention_count INTEGER DEFAULT 0,
    first_appeared TIMESTAMP,
    last_appeared TIMESTAMP,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, entity_type)
);

-- Entity mentions (linking entities to documents)
CREATE TABLE IF NOT EXISTS entity_mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_id UUID REFERENCES entities(id) ON DELETE CASCADE,
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    page_id UUID REFERENCES pages(id) ON DELETE CASCADE,
    mention_text TEXT,
    context TEXT,  -- Surrounding text
    position_start INTEGER,
    position_end INTEGER,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Entity relationships (knowledge graph edges)
CREATE TABLE IF NOT EXISTS entity_relationships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_entity_id UUID REFERENCES entities(id) ON DELETE CASCADE,
    target_entity_id UUID REFERENCES entities(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL,  -- knows, employed, visited, communicated, etc.
    evidence_document_id UUID REFERENCES documents(id),
    evidence_text TEXT,
    confidence FLOAT DEFAULT 1.0,
    first_observed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_observed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    occurrence_count INTEGER DEFAULT 1,
    metadata JSONB,
    UNIQUE(source_entity_id, target_entity_id, relationship_type)
);

-- Communications (emails, messages)
CREATE TABLE IF NOT EXISTS communications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    communication_type VARCHAR(50) NOT NULL,  -- email, message, call
    sender_entity_id UUID REFERENCES entities(id),
    sent_date TIMESTAMP,
    subject TEXT,
    content TEXT,
    source_document_id UUID REFERENCES documents(id),
    thread_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Communication recipients
CREATE TABLE IF NOT EXISTS communication_recipients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    communication_id UUID REFERENCES communications(id) ON DELETE CASCADE,
    recipient_entity_id UUID REFERENCES entities(id),
    recipient_type VARCHAR(20)  -- to, cc, bcc
);

-- FEC Individual Contributions
CREATE TABLE IF NOT EXISTS fec_individual_contributions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cmte_id VARCHAR(20) NOT NULL,  -- Committee ID
    amndt_ind VARCHAR(2),
    rpt_tp VARCHAR(5),
    transaction_pgi VARCHAR(10),
    image_num VARCHAR(20),
    transaction_tp VARCHAR(5),
    entity_tp VARCHAR(5),
    name VARCHAR(255),
    city VARCHAR(50),
    state VARCHAR(5),
    zip_code VARCHAR(15),
    employer VARCHAR(100),
    occupation VARCHAR(100),
    transaction_dt DATE,
    transaction_amt DECIMAL(14,2),
    other_id VARCHAR(20),
    tran_id VARCHAR(25),
    file_num BIGINT,
    memo_cd VARCHAR(5),
    memo_text TEXT,
    sub_id BIGINT UNIQUE,
    cycle INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FEC Committee Master
CREATE TABLE IF NOT EXISTS fec_committee_master (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cmte_id VARCHAR(20) UNIQUE NOT NULL,
    cmte_nm VARCHAR(255),
    tres_nm VARCHAR(100),
    cmte_tp VARCHAR(5),
    cmte_dsgn VARCHAR(5),
    cmte_filing_freq VARCHAR(5),
    org_tp VARCHAR(5),
    connected_org_nm VARCHAR(255),
    cand_id VARCHAR(20),
    cycle INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- FEC Candidate Master
CREATE TABLE IF NOT EXISTS fec_candidate_master (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cand_id VARCHAR(20) UNIQUE NOT NULL,
    cand_name VARCHAR(255),
    cand_pty_affiliation VARCHAR(5),
    cand_election_yr INTEGER,
    cand_office_st VARCHAR(5),
    cand_office VARCHAR(5),
    cand_office_district VARCHAR(5),
    cand_ici VARCHAR(5),
    cand_status VARCHAR(5),
    cand_pcc VARCHAR(20),
    cand_st1 VARCHAR(100),
    cand_st2 VARCHAR(100),
    cand_city VARCHAR(50),
    cand_st VARCHAR(5),
    cand_zip VARCHAR(15),
    cycle INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flight logs (if available)
CREATE TABLE IF NOT EXISTS flight_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    flight_date DATE,
    departure_airport VARCHAR(10),
    arrival_airport VARCHAR(10),
    aircraft_tail VARCHAR(20),
    pilot_entity_id UUID REFERENCES entities(id),
    source_document_id UUID REFERENCES documents(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flight passengers
CREATE TABLE IF NOT EXISTS flight_passengers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    flight_id UUID REFERENCES flight_logs(id) ON DELETE CASCADE,
    passenger_entity_id UUID REFERENCES entities(id),
    passenger_type VARCHAR(20)  -- passenger, crew
);

-- Financial transactions
CREATE TABLE IF NOT EXISTS financial_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_date DATE,
    amount DECIMAL(14,2),
    currency VARCHAR(5) DEFAULT 'USD',
    transaction_type VARCHAR(50),  -- wire_transfer, cash_withdrawal, payment
    from_entity_id UUID REFERENCES entities(id),
    to_entity_id UUID REFERENCES entities(id),
    description TEXT,
    source_document_id UUID REFERENCES documents(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Images extracted from documents
CREATE TABLE IF NOT EXISTS images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    page_id UUID REFERENCES pages(id),
    image_path TEXT NOT NULL,
    image_type VARCHAR(20),  -- photo, document_scan, chart
    extracted_text TEXT,
    has_faces BOOLEAN DEFAULT FALSE,
    face_count INTEGER DEFAULT 0,
    analysis_results JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Redactions tracking
CREATE TABLE IF NOT EXISTS redactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    page_id UUID REFERENCES pages(id),
    x1 FLOAT, y1 FLOAT, x2 FLOAT, y2 FLOAT,  -- Bounding box
    redaction_type VARCHAR(50),  -- personal_info, classified, legal
    content_category VARCHAR(50),  -- What was redacted (name, address, etc.)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Document cross-references (links between documents)
CREATE TABLE IF NOT EXISTS document_crossrefs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    target_document_id UUID REFERENCES documents(id) ON DELETE CASCADE,
    reference_type VARCHAR(50),  -- cites, references, attachment
    reference_text TEXT,
    confidence FLOAT DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_efta_id ON documents(efta_id);
CREATE INDEX IF NOT EXISTS idx_documents_dataset ON documents(dataset);
CREATE INDEX IF NOT EXISTS idx_documents_type ON documents(document_type);
CREATE INDEX IF NOT EXISTS idx_documents_metadata ON documents USING GIN(metadata);

CREATE INDEX IF NOT EXISTS idx_pages_document_id ON pages(document_id);
CREATE INDEX IF NOT EXISTS idx_pages_ocr_text ON pages USING GIN(to_tsvector('english', ocr_text));

CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_normalized ON entities(normalized_name);

CREATE INDEX IF NOT EXISTS idx_entity_mentions_entity ON entity_mentions(entity_id);
CREATE INDEX IF NOT EXISTS idx_entity_mentions_document ON entity_mentions(document_id);

CREATE INDEX IF NOT EXISTS idx_relationships_source ON entity_relationships(source_entity_id);
CREATE INDEX IF NOT EXISTS idx_relationships_target ON entity_relationships(target_entity_id);
CREATE INDEX IF NOT EXISTS idx_relationships_type ON entity_relationships(relationship_type);

CREATE INDEX IF NOT EXISTS idx_fec_contributions_cmte ON fec_individual_contributions(cmte_id);
CREATE INDEX IF NOT EXISTS idx_fec_contributions_name ON fec_individual_contributions(name);
CREATE INDEX IF NOT EXISTS idx_fec_contributions_date ON fec_individual_contributions(transaction_dt);
CREATE INDEX IF NOT EXISTS idx_fec_contributions_cycle ON fec_individual_contributions(cycle);

CREATE INDEX IF NOT EXISTS idx_fec_cm_id ON fec_committee_master(cmte_id);
CREATE INDEX IF NOT EXISTS idx_fec_cn_id ON fec_candidate_master(cand_id);

-- Create views for common queries
CREATE OR REPLACE VIEW entity_summary AS
SELECT 
    e.id,
    e.name,
    e.entity_type,
    e.category,
    e.document_count,
    e.mention_count,
    COUNT(DISTINCT r.id) as relationship_count,
    e.first_appeared,
    e.last_appeared
FROM entities e
LEFT JOIN entity_relationships r ON e.id = r.source_entity_id OR e.id = r.target_entity_id
GROUP BY e.id, e.name, e.entity_type, e.category, e.document_count, e.mention_count, e.first_appeared, e.last_appeared;

CREATE OR REPLACE VIEW document_stats AS
SELECT 
    d.dataset,
    COUNT(*) as document_count,
    SUM(d.page_count) as total_pages,
    COUNT(DISTINCT e.id) as entity_count,
    COUNT(DISTINCT CASE WHEN p.has_redactions THEN d.id END) as redacted_document_count
FROM documents d
LEFT JOIN entity_mentions em ON d.id = em.document_id
LEFT JOIN entities e ON em.entity_id = e.id
LEFT JOIN pages p ON d.id = p.document_id
GROUP BY d.dataset;

-- Functions for updating timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_documents_updated_at 
    BEFORE UPDATE ON documents 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Audit table for tracking data changes
CREATE TABLE IF NOT EXISTS audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_name VARCHAR(50) NOT NULL,
    record_id UUID NOT NULL,
    action VARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    performed_by VARCHAR(100),
    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search configuration
CREATE OR REPLACE VIEW document_search AS
SELECT 
    d.id as document_id,
    d.efta_id,
    d.dataset,
    d.document_type,
    string_agg(p.ocr_text, ' ') as full_text
FROM documents d
LEFT JOIN pages p ON d.id = p.document_id
GROUP BY d.id, d.efta_id, d.dataset, d.document_type;

-- Create materialized view for faster entity lookups (refresh periodically)
CREATE MATERIALIZED VIEW IF NOT EXISTS entity_lookup AS
SELECT 
    e.id,
    e.name,
    e.normalized_name,
    e.entity_type,
    e.aliases,
    array_agg(DISTINCT em.document_id) as document_ids
FROM entities e
LEFT JOIN entity_mentions em ON e.id = em.entity_id
GROUP BY e.id, e.name, e.normalized_name, e.entity_type, e.aliases;

CREATE INDEX IF NOT EXISTS idx_entity_lookup_name ON entity_lookup USING gin(name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_entity_lookup_normalized ON entity_lookup USING gin(normalized_name gin_trgm_ops);
