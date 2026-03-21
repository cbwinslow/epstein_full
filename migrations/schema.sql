--
-- PostgreSQL database dump
--


-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE IF EXISTS ONLY public.subpoena_return_links DROP CONSTRAINT IF EXISTS subpoena_return_links_subpoena_id_fkey;
ALTER TABLE IF EXISTS ONLY public.subpoena_return_links DROP CONSTRAINT IF EXISTS subpoena_return_links_return_id_fkey;
ALTER TABLE IF EXISTS ONLY public.rider_clauses DROP CONSTRAINT IF EXISTS rider_clauses_subpoena_id_fkey;
ALTER TABLE IF EXISTS ONLY public.relationships DROP CONSTRAINT IF EXISTS relationships_target_entity_id_fkey;
ALTER TABLE IF EXISTS ONLY public.relationships DROP CONSTRAINT IF EXISTS relationships_source_entity_id_fkey;
ALTER TABLE IF EXISTS ONLY public.external_references DROP CONSTRAINT IF EXISTS external_references_entity_id_fkey;
ALTER TABLE IF EXISTS ONLY public.email_participants DROP CONSTRAINT IF EXISTS email_participants_email_id_fkey;
ALTER TABLE IF EXISTS ONLY public.edge_sources DROP CONSTRAINT IF EXISTS edge_sources_relationship_id_fkey;
ALTER TABLE IF EXISTS ONLY public.clause_fulfillment DROP CONSTRAINT IF EXISTS clause_fulfillment_return_id_fkey;
ALTER TABLE IF EXISTS ONLY public.clause_fulfillment DROP CONSTRAINT IF EXISTS clause_fulfillment_clause_id_fkey;
DROP TRIGGER IF EXISTS pages_search_update ON public.pages;
DROP INDEX IF EXISTS public.idx_transcripts_efta;
DROP INDEX IF EXISTS public.idx_task_history_ts;
DROP INDEX IF EXISTS public.idx_relationships_type;
DROP INDEX IF EXISTS public.idx_relationships_target;
DROP INDEX IF EXISTS public.idx_relationships_source;
DROP INDEX IF EXISTS public.idx_redactions_type;
DROP INDEX IF EXISTS public.idx_redactions_efta;
DROP INDEX IF EXISTS public.idx_pages_search;
DROP INDEX IF EXISTS public.idx_pages_efta;
DROP INDEX IF EXISTS public.idx_ocr_efta;
DROP INDEX IF EXISTS public.idx_images_efta;
DROP INDEX IF EXISTS public.idx_file_registry_source;
DROP INDEX IF EXISTS public.idx_file_registry_hash;
DROP INDEX IF EXISTS public.idx_file_registry_efta;
DROP INDEX IF EXISTS public.idx_external_refs_source;
DROP INDEX IF EXISTS public.idx_external_refs_entity;
DROP INDEX IF EXISTS public.idx_entities_type;
DROP INDEX IF EXISTS public.idx_entities_name_trgm;
DROP INDEX IF EXISTS public.idx_entities_name;
DROP INDEX IF EXISTS public.idx_emails_from;
DROP INDEX IF EXISTS public.idx_emails_efta;
DROP INDEX IF EXISTS public.idx_emails_date;
DROP INDEX IF EXISTS public.idx_doc_class_type;
DROP INDEX IF EXISTS public.idx_doc_class_efta;
DROP INDEX IF EXISTS public.idx_crosswalk_efta;
ALTER TABLE IF EXISTS ONLY public.transcripts DROP CONSTRAINT IF EXISTS transcripts_pkey;
ALTER TABLE IF EXISTS ONLY public.transcripts DROP CONSTRAINT IF EXISTS transcripts_efta_number_key;
ALTER TABLE IF EXISTS ONLY public.transcript_segments DROP CONSTRAINT IF EXISTS transcript_segments_pkey;
ALTER TABLE IF EXISTS ONLY public.tasks DROP CONSTRAINT IF EXISTS tasks_pkey;
ALTER TABLE IF EXISTS ONLY public.task_history DROP CONSTRAINT IF EXISTS task_history_pkey;
ALTER TABLE IF EXISTS ONLY public.subpoenas DROP CONSTRAINT IF EXISTS subpoenas_pkey;
ALTER TABLE IF EXISTS ONLY public.subpoena_return_links DROP CONSTRAINT IF EXISTS subpoena_return_links_pkey;
ALTER TABLE IF EXISTS ONLY public.rider_clauses DROP CONSTRAINT IF EXISTS rider_clauses_pkey;
ALTER TABLE IF EXISTS ONLY public.returns DROP CONSTRAINT IF EXISTS returns_pkey;
ALTER TABLE IF EXISTS ONLY public.resolved_identities DROP CONSTRAINT IF EXISTS resolved_identities_pkey;
ALTER TABLE IF EXISTS ONLY public.relationships DROP CONSTRAINT IF EXISTS relationships_pkey;
ALTER TABLE IF EXISTS ONLY public.redactions DROP CONSTRAINT IF EXISTS redactions_pkey;
ALTER TABLE IF EXISTS ONLY public.redaction_entities DROP CONSTRAINT IF EXISTS redaction_entities_pkey;
ALTER TABLE IF EXISTS ONLY public.reconstructed_pages DROP CONSTRAINT IF EXISTS reconstructed_pages_pkey;
ALTER TABLE IF EXISTS ONLY public.pages DROP CONSTRAINT IF EXISTS pages_pkey;
ALTER TABLE IF EXISTS ONLY public.pages DROP CONSTRAINT IF EXISTS pages_efta_number_page_number_key;
ALTER TABLE IF EXISTS ONLY public.ocr_results DROP CONSTRAINT IF EXISTS ocr_results_pkey;
ALTER TABLE IF EXISTS ONLY public.investigative_gaps DROP CONSTRAINT IF EXISTS investigative_gaps_pkey;
ALTER TABLE IF EXISTS ONLY public.images DROP CONSTRAINT IF EXISTS images_pkey;
ALTER TABLE IF EXISTS ONLY public.graph_nodes DROP CONSTRAINT IF EXISTS graph_nodes_pkey;
ALTER TABLE IF EXISTS ONLY public.graph_edges DROP CONSTRAINT IF EXISTS graph_edges_pkey;
ALTER TABLE IF EXISTS ONLY public.file_registry DROP CONSTRAINT IF EXISTS file_registry_pkey;
ALTER TABLE IF EXISTS ONLY public.external_references DROP CONSTRAINT IF EXISTS external_references_pkey;
ALTER TABLE IF EXISTS ONLY public.entities DROP CONSTRAINT IF EXISTS entities_pkey;
ALTER TABLE IF EXISTS ONLY public.emails DROP CONSTRAINT IF EXISTS emails_pkey;
ALTER TABLE IF EXISTS ONLY public.email_participants DROP CONSTRAINT IF EXISTS email_participants_pkey;
ALTER TABLE IF EXISTS ONLY public.efta_crosswalk DROP CONSTRAINT IF EXISTS efta_crosswalk_pkey;
ALTER TABLE IF EXISTS ONLY public.efta_crosswalk DROP CONSTRAINT IF EXISTS efta_crosswalk_efta_number_key;
ALTER TABLE IF EXISTS ONLY public.edge_sources DROP CONSTRAINT IF EXISTS edge_sources_pkey;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_pkey;
ALTER TABLE IF EXISTS ONLY public.documents DROP CONSTRAINT IF EXISTS documents_efta_number_key;
ALTER TABLE IF EXISTS ONLY public.document_summary DROP CONSTRAINT IF EXISTS document_summary_pkey;
ALTER TABLE IF EXISTS ONLY public.document_classification DROP CONSTRAINT IF EXISTS document_classification_pkey;
ALTER TABLE IF EXISTS ONLY public.document_classification DROP CONSTRAINT IF EXISTS document_classification_efta_number_key;
ALTER TABLE IF EXISTS ONLY public.communication_pairs DROP CONSTRAINT IF EXISTS communication_pairs_pkey;
ALTER TABLE IF EXISTS ONLY public.clause_fulfillment DROP CONSTRAINT IF EXISTS clause_fulfillment_pkey;
ALTER TABLE IF EXISTS public.transcripts ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.transcript_segments ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.task_history ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.subpoenas ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.subpoena_return_links ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.rider_clauses ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.returns ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.resolved_identities ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.relationships ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.redactions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.redaction_entities ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.reconstructed_pages ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.pages ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.ocr_results ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.investigative_gaps ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.images ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.graph_nodes ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.graph_edges ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.file_registry ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.external_references ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.entities ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.emails ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.email_participants ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.efta_crosswalk ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.edge_sources ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.documents ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.document_summary ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.document_classification ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.communication_pairs ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS public.clause_fulfillment ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE IF EXISTS public.transcripts_id_seq;
DROP TABLE IF EXISTS public.transcripts;
DROP SEQUENCE IF EXISTS public.transcript_segments_id_seq;
DROP TABLE IF EXISTS public.transcript_segments;
DROP TABLE IF EXISTS public.tasks;
DROP SEQUENCE IF EXISTS public.task_history_id_seq;
DROP TABLE IF EXISTS public.task_history;
DROP SEQUENCE IF EXISTS public.subpoenas_id_seq;
DROP TABLE IF EXISTS public.subpoenas;
DROP SEQUENCE IF EXISTS public.subpoena_return_links_id_seq;
DROP TABLE IF EXISTS public.subpoena_return_links;
DROP SEQUENCE IF EXISTS public.rider_clauses_id_seq;
DROP TABLE IF EXISTS public.rider_clauses;
DROP SEQUENCE IF EXISTS public.returns_id_seq;
DROP TABLE IF EXISTS public.returns;
DROP SEQUENCE IF EXISTS public.resolved_identities_id_seq;
DROP TABLE IF EXISTS public.resolved_identities;
DROP SEQUENCE IF EXISTS public.relationships_id_seq;
DROP TABLE IF EXISTS public.relationships;
DROP SEQUENCE IF EXISTS public.redactions_id_seq;
DROP TABLE IF EXISTS public.redactions;
DROP SEQUENCE IF EXISTS public.redaction_entities_id_seq;
DROP TABLE IF EXISTS public.redaction_entities;
DROP SEQUENCE IF EXISTS public.reconstructed_pages_id_seq;
DROP TABLE IF EXISTS public.reconstructed_pages;
DROP SEQUENCE IF EXISTS public.pages_id_seq;
DROP TABLE IF EXISTS public.pages;
DROP SEQUENCE IF EXISTS public.ocr_results_id_seq;
DROP TABLE IF EXISTS public.ocr_results;
DROP SEQUENCE IF EXISTS public.investigative_gaps_id_seq;
DROP TABLE IF EXISTS public.investigative_gaps;
DROP SEQUENCE IF EXISTS public.images_id_seq;
DROP TABLE IF EXISTS public.images;
DROP SEQUENCE IF EXISTS public.graph_nodes_id_seq;
DROP TABLE IF EXISTS public.graph_nodes;
DROP SEQUENCE IF EXISTS public.graph_edges_id_seq;
DROP TABLE IF EXISTS public.graph_edges;
DROP SEQUENCE IF EXISTS public.file_registry_id_seq;
DROP TABLE IF EXISTS public.file_registry;
DROP SEQUENCE IF EXISTS public.external_references_id_seq;
DROP TABLE IF EXISTS public.external_references;
DROP SEQUENCE IF EXISTS public.entities_id_seq;
DROP TABLE IF EXISTS public.entities;
DROP SEQUENCE IF EXISTS public.emails_id_seq;
DROP TABLE IF EXISTS public.emails;
DROP SEQUENCE IF EXISTS public.email_participants_id_seq;
DROP TABLE IF EXISTS public.email_participants;
DROP SEQUENCE IF EXISTS public.efta_crosswalk_id_seq;
DROP TABLE IF EXISTS public.efta_crosswalk;
DROP SEQUENCE IF EXISTS public.edge_sources_id_seq;
DROP TABLE IF EXISTS public.edge_sources;
DROP SEQUENCE IF EXISTS public.documents_id_seq;
DROP TABLE IF EXISTS public.documents;
DROP SEQUENCE IF EXISTS public.document_summary_id_seq;
DROP TABLE IF EXISTS public.document_summary;
DROP SEQUENCE IF EXISTS public.document_classification_id_seq;
DROP TABLE IF EXISTS public.document_classification;
DROP SEQUENCE IF EXISTS public.communication_pairs_id_seq;
DROP TABLE IF EXISTS public.communication_pairs;
DROP SEQUENCE IF EXISTS public.clause_fulfillment_id_seq;
DROP TABLE IF EXISTS public.clause_fulfillment;
DROP FUNCTION IF EXISTS public.search_entities_fuzzy(query text, threshold real);
DROP FUNCTION IF EXISTS public.pages_search_trigger();
DROP EXTENSION IF EXISTS vector;
DROP EXTENSION IF EXISTS unaccent;
DROP EXTENSION IF EXISTS pg_trgm;
DROP EXTENSION IF EXISTS pg_stat_statements;
--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: pages_search_trigger(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.pages_search_trigger() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.efta_number, '')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.text_content, '')), 'B');
    RETURN NEW;
END
$$;


--
-- Name: search_entities_fuzzy(text, real); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.search_entities_fuzzy(query text, threshold real DEFAULT 0.3) RETURNS TABLE(id integer, name text, entity_type text, similarity real)
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN QUERY
    SELECT e.id, e.name, e.entity_type, similarity(e.name, query) AS sim
    FROM entities e
    WHERE similarity(e.name, query) > threshold
    ORDER BY sim DESC
    LIMIT 20;
END
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clause_fulfillment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.clause_fulfillment (
    id integer NOT NULL,
    clause_id integer,
    return_id integer,
    status text,
    evidence text,
    page_count_relevant integer,
    notes text
);


--
-- Name: clause_fulfillment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.clause_fulfillment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: clause_fulfillment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.clause_fulfillment_id_seq OWNED BY public.clause_fulfillment.id;


--
-- Name: communication_pairs; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.communication_pairs (
    id integer NOT NULL,
    person_a character varying(100),
    person_b character varying(100),
    email_count integer,
    first_date text,
    last_date text,
    a_to_b_count integer,
    b_to_a_count integer,
    sample_subjects text,
    sample_eftas text
);


--
-- Name: communication_pairs_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.communication_pairs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: communication_pairs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.communication_pairs_id_seq OWNED BY public.communication_pairs.id;


--
-- Name: document_classification; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_classification (
    id integer NOT NULL,
    efta_number character varying(50) NOT NULL,
    dataset integer,
    doc_type character varying(50),
    doc_type_confidence real,
    max_char_count integer,
    total_pages integer,
    has_redactions integer DEFAULT 0,
    redaction_count integer DEFAULT 0,
    has_image_analysis integer DEFAULT 0,
    has_ocr integer DEFAULT 0,
    has_transcript integer DEFAULT 0,
    has_concordance integer DEFAULT 0,
    classified_at text
);


--
-- Name: document_classification_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_classification_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_classification_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_classification_id_seq OWNED BY public.document_classification.id;


--
-- Name: document_summary; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_summary (
    id integer NOT NULL,
    pdf_path text,
    efta_number character varying(50),
    total_redactions integer,
    text_near_bar_count integer,
    proper_redactions integer,
    has_ocr_text boolean DEFAULT false,
    scanned_at text,
    dataset_source text
);


--
-- Name: document_summary_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_summary_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_summary_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_summary_id_seq OWNED BY public.document_summary.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    efta_number character varying(50) NOT NULL,
    dataset integer,
    file_path text,
    total_pages integer DEFAULT 1,
    file_size integer,
    pdf_url text,
    error text,
    extraction_timestamp text,
    document_type character varying(50),
    classification_confidence real,
    has_redactions boolean DEFAULT false,
    has_transcript boolean DEFAULT false,
    has_image_analysis boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: edge_sources; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.edge_sources (
    id integer NOT NULL,
    relationship_id integer,
    source_type text,
    source_id integer,
    source_detail text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: edge_sources_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.edge_sources_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: edge_sources_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.edge_sources_id_seq OWNED BY public.edge_sources.id;


--
-- Name: efta_crosswalk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.efta_crosswalk (
    id integer NOT NULL,
    efta_number character varying(50) NOT NULL,
    dataset integer,
    total_pages integer,
    max_char_count integer,
    in_concordance integer DEFAULT 0,
    concordance_extension text,
    concordance_filename text,
    in_redaction_db integer DEFAULT 0,
    redaction_total integer DEFAULT 0,
    redaction_proper integer DEFAULT 0,
    redaction_text_near integer DEFAULT 0,
    redaction_has_ocr integer DEFAULT 0,
    in_image_analysis integer DEFAULT 0,
    in_ocr_db integer DEFAULT 0,
    in_transcripts integer DEFAULT 0,
    doc_type text,
    doc_type_confidence real
);


--
-- Name: efta_crosswalk_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.efta_crosswalk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: efta_crosswalk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.efta_crosswalk_id_seq OWNED BY public.efta_crosswalk.id;


--
-- Name: email_participants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.email_participants (
    id integer NOT NULL,
    email_id integer,
    role character varying(20),
    name text,
    email_address text,
    resolved_entity_id integer
);


--
-- Name: email_participants_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.email_participants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: email_participants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.email_participants_id_seq OWNED BY public.email_participants.id;


--
-- Name: emails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.emails (
    id integer NOT NULL,
    efta_number character varying(50),
    dataset integer,
    page_number integer,
    source text,
    from_name text,
    from_email text,
    to_raw text,
    cc_raw text,
    subject text,
    date_sent text,
    date_normalized text,
    is_noise integer DEFAULT 0,
    parse_confidence real
);


--
-- Name: emails_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.emails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: emails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.emails_id_seq OWNED BY public.emails.id;


--
-- Name: entities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.entities (
    id integer NOT NULL,
    name text NOT NULL,
    entity_type character varying(50),
    source_id integer,
    source_table text,
    aliases jsonb DEFAULT '[]'::jsonb,
    metadata jsonb DEFAULT '{}'::jsonb,
    mention_count integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: entities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: entities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.entities_id_seq OWNED BY public.entities.id;


--
-- Name: external_references; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.external_references (
    id integer NOT NULL,
    entity_id integer,
    external_source character varying(50),
    external_id text,
    external_url text,
    confidence real DEFAULT 0.0,
    metadata jsonb DEFAULT '{}'::jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: external_references_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.external_references_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: external_references_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.external_references_id_seq OWNED BY public.external_references.id;


--
-- Name: file_registry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.file_registry (
    id integer NOT NULL,
    file_path text NOT NULL,
    sha256_hash character varying(64),
    efta_number character varying(50),
    dataset integer,
    file_size_bytes bigint,
    source character varying(50),
    downloaded_at timestamp without time zone,
    validated boolean DEFAULT false,
    notes text
);


--
-- Name: file_registry_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.file_registry_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: file_registry_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.file_registry_id_seq OWNED BY public.file_registry.id;


--
-- Name: graph_edges; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.graph_edges (
    id integer NOT NULL,
    source_node integer,
    target_node integer,
    edge_type text,
    weight real,
    properties text
);


--
-- Name: graph_edges_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.graph_edges_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: graph_edges_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.graph_edges_id_seq OWNED BY public.graph_edges.id;


--
-- Name: graph_nodes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.graph_nodes (
    id integer NOT NULL,
    node_type text,
    node_id text,
    label text,
    properties text
);


--
-- Name: graph_nodes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.graph_nodes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: graph_nodes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.graph_nodes_id_seq OWNED BY public.graph_nodes.id;


--
-- Name: images; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.images (
    id integer NOT NULL,
    image_name text,
    efta_number character varying(50),
    source_pdf text,
    page_number integer,
    analysis_text text,
    people text,
    text_content text,
    objects text,
    setting text,
    activity text,
    notable text,
    analyzed_at text
);


--
-- Name: images_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.images_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: images_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.images_id_seq OWNED BY public.images.id;


--
-- Name: investigative_gaps; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.investigative_gaps (
    id integer NOT NULL,
    gap_type text,
    severity text,
    description text,
    related_subpoena_ids text,
    related_clause_ids text,
    evidence text
);


--
-- Name: investigative_gaps_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.investigative_gaps_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: investigative_gaps_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.investigative_gaps_id_seq OWNED BY public.investigative_gaps.id;


--
-- Name: ocr_results; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ocr_results (
    id integer NOT NULL,
    image_path text,
    efta_number character varying(50),
    ocr_text text,
    orientation integer,
    processed_at text
);


--
-- Name: ocr_results_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.ocr_results_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ocr_results_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.ocr_results_id_seq OWNED BY public.ocr_results.id;


--
-- Name: pages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pages (
    id integer NOT NULL,
    efta_number character varying(50) NOT NULL,
    page_number integer NOT NULL,
    text_content text,
    char_count integer,
    search_vector tsvector,
    embedding public.vector(768),
    ocr_confidence real,
    ocr_backend character varying(20),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: pages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pages_id_seq OWNED BY public.pages.id;


--
-- Name: reconstructed_pages; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.reconstructed_pages (
    id integer NOT NULL,
    efta_number character varying(50),
    page_number integer,
    num_fragments integer,
    reconstructed_text text,
    document_type text,
    interest_score real,
    names_found text,
    dataset_source text
);


--
-- Name: reconstructed_pages_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.reconstructed_pages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: reconstructed_pages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.reconstructed_pages_id_seq OWNED BY public.reconstructed_pages.id;


--
-- Name: redaction_entities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.redaction_entities (
    id integer NOT NULL,
    source_redaction_id integer,
    efta_number character varying(50),
    page_number integer,
    entity_type text,
    entity_value text,
    context text,
    dataset_source text
);


--
-- Name: redaction_entities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.redaction_entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: redaction_entities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.redaction_entities_id_seq OWNED BY public.redaction_entities.id;


--
-- Name: redactions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.redactions (
    id integer NOT NULL,
    pdf_path text,
    efta_number character varying(50),
    page_number integer,
    redaction_type character varying(20),
    rect_x0 real,
    rect_y0 real,
    rect_x1 real,
    rect_y1 real,
    ocr_text text,
    confidence real,
    detected_at text,
    dataset_source text
);


--
-- Name: redactions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.redactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: redactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.redactions_id_seq OWNED BY public.redactions.id;


--
-- Name: relationships; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.relationships (
    id integer NOT NULL,
    source_entity_id integer,
    target_entity_id integer,
    relationship_type character varying(50) NOT NULL,
    weight real DEFAULT 1.0,
    date_first text,
    date_last text,
    metadata jsonb DEFAULT '{}'::jsonb,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: relationships_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.relationships_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: relationships_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.relationships_id_seq OWNED BY public.relationships.id;


--
-- Name: resolved_identities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resolved_identities (
    id integer NOT NULL,
    raw_name text,
    raw_email text,
    canonical_name text,
    person_registry_slug text,
    kg_entity_id integer,
    confidence real,
    match_method text
);


--
-- Name: resolved_identities_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.resolved_identities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: resolved_identities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.resolved_identities_id_seq OWNED BY public.resolved_identities.id;


--
-- Name: returns; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.returns (
    id integer NOT NULL,
    source text,
    production_id integer,
    sdny_bates_start text,
    sdny_bates_end text,
    efta_range_start text,
    efta_range_end text,
    page_count integer,
    description text,
    date_received text,
    responding_entity text
);


--
-- Name: returns_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.returns_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: returns_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.returns_id_seq OWNED BY public.returns.id;


--
-- Name: rider_clauses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.rider_clauses (
    id integer NOT NULL,
    subpoena_id integer,
    clause_number integer,
    clause_text text,
    data_class text,
    date_range_start text,
    date_range_end text,
    target_accounts text
);


--
-- Name: rider_clauses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.rider_clauses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: rider_clauses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.rider_clauses_id_seq OWNED BY public.rider_clauses.id;


--
-- Name: subpoena_return_links; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subpoena_return_links (
    id integer NOT NULL,
    subpoena_id integer,
    return_id integer,
    confidence text,
    match_method text,
    match_evidence text
);


--
-- Name: subpoena_return_links_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subpoena_return_links_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: subpoena_return_links_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.subpoena_return_links_id_seq OWNED BY public.subpoena_return_links.id;


--
-- Name: subpoenas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subpoenas (
    id integer NOT NULL,
    efta_number character varying(50),
    target text,
    target_category text,
    date_issued text,
    statutes text,
    total_pages integer,
    rider_page_numbers text,
    full_rider_text text,
    clause_count integer
);


--
-- Name: subpoenas_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subpoenas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: subpoenas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.subpoenas_id_seq OWNED BY public.subpoenas.id;


--
-- Name: task_history; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.task_history (
    id integer NOT NULL,
    task_id text,
    ts text NOT NULL,
    value integer NOT NULL
);


--
-- Name: task_history_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.task_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: task_history_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.task_history_id_seq OWNED BY public.task_history.id;


--
-- Name: tasks; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.tasks (
    id text NOT NULL,
    label text NOT NULL,
    type text DEFAULT 'download'::text,
    expected integer DEFAULT 0,
    current integer DEFAULT 0,
    rate_bps real DEFAULT 0,
    status text DEFAULT 'running'::text,
    started_at text,
    last_update text,
    finished_at text
);


--
-- Name: transcript_segments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transcript_segments (
    id integer NOT NULL,
    efta_number character varying(50),
    segment_id integer,
    start_time real,
    end_time real,
    text text
);


--
-- Name: transcript_segments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.transcript_segments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: transcript_segments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.transcript_segments_id_seq OWNED BY public.transcript_segments.id;


--
-- Name: transcripts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.transcripts (
    id integer NOT NULL,
    efta_number character varying(50),
    file_path text,
    file_type character varying(10),
    duration_secs real,
    language character varying(10),
    language_prob real,
    transcript text,
    word_count integer,
    dataset_source text,
    transcribed_at text
);


--
-- Name: transcripts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.transcripts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: transcripts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.transcripts_id_seq OWNED BY public.transcripts.id;


--
-- Name: clause_fulfillment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clause_fulfillment ALTER COLUMN id SET DEFAULT nextval('public.clause_fulfillment_id_seq'::regclass);


--
-- Name: communication_pairs id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_pairs ALTER COLUMN id SET DEFAULT nextval('public.communication_pairs_id_seq'::regclass);


--
-- Name: document_classification id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_classification ALTER COLUMN id SET DEFAULT nextval('public.document_classification_id_seq'::regclass);


--
-- Name: document_summary id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_summary ALTER COLUMN id SET DEFAULT nextval('public.document_summary_id_seq'::regclass);


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: edge_sources id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.edge_sources ALTER COLUMN id SET DEFAULT nextval('public.edge_sources_id_seq'::regclass);


--
-- Name: efta_crosswalk id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.efta_crosswalk ALTER COLUMN id SET DEFAULT nextval('public.efta_crosswalk_id_seq'::regclass);


--
-- Name: email_participants id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_participants ALTER COLUMN id SET DEFAULT nextval('public.email_participants_id_seq'::regclass);


--
-- Name: emails id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails ALTER COLUMN id SET DEFAULT nextval('public.emails_id_seq'::regclass);


--
-- Name: entities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entities ALTER COLUMN id SET DEFAULT nextval('public.entities_id_seq'::regclass);


--
-- Name: external_references id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.external_references ALTER COLUMN id SET DEFAULT nextval('public.external_references_id_seq'::regclass);


--
-- Name: file_registry id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file_registry ALTER COLUMN id SET DEFAULT nextval('public.file_registry_id_seq'::regclass);


--
-- Name: graph_edges id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.graph_edges ALTER COLUMN id SET DEFAULT nextval('public.graph_edges_id_seq'::regclass);


--
-- Name: graph_nodes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.graph_nodes ALTER COLUMN id SET DEFAULT nextval('public.graph_nodes_id_seq'::regclass);


--
-- Name: images id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images ALTER COLUMN id SET DEFAULT nextval('public.images_id_seq'::regclass);


--
-- Name: investigative_gaps id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.investigative_gaps ALTER COLUMN id SET DEFAULT nextval('public.investigative_gaps_id_seq'::regclass);


--
-- Name: ocr_results id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ocr_results ALTER COLUMN id SET DEFAULT nextval('public.ocr_results_id_seq'::regclass);


--
-- Name: pages id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pages ALTER COLUMN id SET DEFAULT nextval('public.pages_id_seq'::regclass);


--
-- Name: reconstructed_pages id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reconstructed_pages ALTER COLUMN id SET DEFAULT nextval('public.reconstructed_pages_id_seq'::regclass);


--
-- Name: redaction_entities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.redaction_entities ALTER COLUMN id SET DEFAULT nextval('public.redaction_entities_id_seq'::regclass);


--
-- Name: redactions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.redactions ALTER COLUMN id SET DEFAULT nextval('public.redactions_id_seq'::regclass);


--
-- Name: relationships id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relationships ALTER COLUMN id SET DEFAULT nextval('public.relationships_id_seq'::regclass);


--
-- Name: resolved_identities id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resolved_identities ALTER COLUMN id SET DEFAULT nextval('public.resolved_identities_id_seq'::regclass);


--
-- Name: returns id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.returns ALTER COLUMN id SET DEFAULT nextval('public.returns_id_seq'::regclass);


--
-- Name: rider_clauses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rider_clauses ALTER COLUMN id SET DEFAULT nextval('public.rider_clauses_id_seq'::regclass);


--
-- Name: subpoena_return_links id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subpoena_return_links ALTER COLUMN id SET DEFAULT nextval('public.subpoena_return_links_id_seq'::regclass);


--
-- Name: subpoenas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subpoenas ALTER COLUMN id SET DEFAULT nextval('public.subpoenas_id_seq'::regclass);


--
-- Name: task_history id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_history ALTER COLUMN id SET DEFAULT nextval('public.task_history_id_seq'::regclass);


--
-- Name: transcript_segments id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transcript_segments ALTER COLUMN id SET DEFAULT nextval('public.transcript_segments_id_seq'::regclass);


--
-- Name: transcripts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transcripts ALTER COLUMN id SET DEFAULT nextval('public.transcripts_id_seq'::regclass);


--
-- Name: clause_fulfillment clause_fulfillment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clause_fulfillment
    ADD CONSTRAINT clause_fulfillment_pkey PRIMARY KEY (id);


--
-- Name: communication_pairs communication_pairs_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.communication_pairs
    ADD CONSTRAINT communication_pairs_pkey PRIMARY KEY (id);


--
-- Name: document_classification document_classification_efta_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_classification
    ADD CONSTRAINT document_classification_efta_number_key UNIQUE (efta_number);


--
-- Name: document_classification document_classification_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_classification
    ADD CONSTRAINT document_classification_pkey PRIMARY KEY (id);


--
-- Name: document_summary document_summary_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_summary
    ADD CONSTRAINT document_summary_pkey PRIMARY KEY (id);


--
-- Name: documents documents_efta_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_efta_number_key UNIQUE (efta_number);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: edge_sources edge_sources_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.edge_sources
    ADD CONSTRAINT edge_sources_pkey PRIMARY KEY (id);


--
-- Name: efta_crosswalk efta_crosswalk_efta_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.efta_crosswalk
    ADD CONSTRAINT efta_crosswalk_efta_number_key UNIQUE (efta_number);


--
-- Name: efta_crosswalk efta_crosswalk_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.efta_crosswalk
    ADD CONSTRAINT efta_crosswalk_pkey PRIMARY KEY (id);


--
-- Name: email_participants email_participants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_participants
    ADD CONSTRAINT email_participants_pkey PRIMARY KEY (id);


--
-- Name: emails emails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_pkey PRIMARY KEY (id);


--
-- Name: entities entities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.entities
    ADD CONSTRAINT entities_pkey PRIMARY KEY (id);


--
-- Name: external_references external_references_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.external_references
    ADD CONSTRAINT external_references_pkey PRIMARY KEY (id);


--
-- Name: file_registry file_registry_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.file_registry
    ADD CONSTRAINT file_registry_pkey PRIMARY KEY (id);


--
-- Name: graph_edges graph_edges_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.graph_edges
    ADD CONSTRAINT graph_edges_pkey PRIMARY KEY (id);


--
-- Name: graph_nodes graph_nodes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.graph_nodes
    ADD CONSTRAINT graph_nodes_pkey PRIMARY KEY (id);


--
-- Name: images images_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.images
    ADD CONSTRAINT images_pkey PRIMARY KEY (id);


--
-- Name: investigative_gaps investigative_gaps_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.investigative_gaps
    ADD CONSTRAINT investigative_gaps_pkey PRIMARY KEY (id);


--
-- Name: ocr_results ocr_results_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ocr_results
    ADD CONSTRAINT ocr_results_pkey PRIMARY KEY (id);


--
-- Name: pages pages_efta_number_page_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pages
    ADD CONSTRAINT pages_efta_number_page_number_key UNIQUE (efta_number, page_number);


--
-- Name: pages pages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pages
    ADD CONSTRAINT pages_pkey PRIMARY KEY (id);


--
-- Name: reconstructed_pages reconstructed_pages_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.reconstructed_pages
    ADD CONSTRAINT reconstructed_pages_pkey PRIMARY KEY (id);


--
-- Name: redaction_entities redaction_entities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.redaction_entities
    ADD CONSTRAINT redaction_entities_pkey PRIMARY KEY (id);


--
-- Name: redactions redactions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.redactions
    ADD CONSTRAINT redactions_pkey PRIMARY KEY (id);


--
-- Name: relationships relationships_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_pkey PRIMARY KEY (id);


--
-- Name: resolved_identities resolved_identities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resolved_identities
    ADD CONSTRAINT resolved_identities_pkey PRIMARY KEY (id);


--
-- Name: returns returns_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.returns
    ADD CONSTRAINT returns_pkey PRIMARY KEY (id);


--
-- Name: rider_clauses rider_clauses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rider_clauses
    ADD CONSTRAINT rider_clauses_pkey PRIMARY KEY (id);


--
-- Name: subpoena_return_links subpoena_return_links_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subpoena_return_links
    ADD CONSTRAINT subpoena_return_links_pkey PRIMARY KEY (id);


--
-- Name: subpoenas subpoenas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subpoenas
    ADD CONSTRAINT subpoenas_pkey PRIMARY KEY (id);


--
-- Name: task_history task_history_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.task_history
    ADD CONSTRAINT task_history_pkey PRIMARY KEY (id);


--
-- Name: tasks tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (id);


--
-- Name: transcript_segments transcript_segments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transcript_segments
    ADD CONSTRAINT transcript_segments_pkey PRIMARY KEY (id);


--
-- Name: transcripts transcripts_efta_number_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transcripts
    ADD CONSTRAINT transcripts_efta_number_key UNIQUE (efta_number);


--
-- Name: transcripts transcripts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.transcripts
    ADD CONSTRAINT transcripts_pkey PRIMARY KEY (id);


--
-- Name: idx_crosswalk_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_crosswalk_efta ON public.efta_crosswalk USING btree (efta_number);


--
-- Name: idx_doc_class_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doc_class_efta ON public.document_classification USING btree (efta_number);


--
-- Name: idx_doc_class_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_doc_class_type ON public.document_classification USING btree (doc_type);


--
-- Name: idx_emails_date; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_emails_date ON public.emails USING btree (date_normalized);


--
-- Name: idx_emails_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_emails_efta ON public.emails USING btree (efta_number);


--
-- Name: idx_emails_from; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_emails_from ON public.emails USING btree (from_email);


--
-- Name: idx_entities_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_entities_name ON public.entities USING btree (name);


--
-- Name: idx_entities_name_trgm; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_entities_name_trgm ON public.entities USING gin (name public.gin_trgm_ops);


--
-- Name: idx_entities_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_entities_type ON public.entities USING btree (entity_type);


--
-- Name: idx_external_refs_entity; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_external_refs_entity ON public.external_references USING btree (entity_id);


--
-- Name: idx_external_refs_source; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_external_refs_source ON public.external_references USING btree (external_source);


--
-- Name: idx_file_registry_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_file_registry_efta ON public.file_registry USING btree (efta_number);


--
-- Name: idx_file_registry_hash; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_file_registry_hash ON public.file_registry USING btree (sha256_hash);


--
-- Name: idx_file_registry_source; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_file_registry_source ON public.file_registry USING btree (source);


--
-- Name: idx_images_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_images_efta ON public.images USING btree (efta_number);


--
-- Name: idx_ocr_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_ocr_efta ON public.ocr_results USING btree (efta_number);


--
-- Name: idx_pages_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pages_efta ON public.pages USING btree (efta_number);


--
-- Name: idx_pages_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pages_search ON public.pages USING gin (search_vector);


--
-- Name: idx_redactions_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_redactions_efta ON public.redactions USING btree (efta_number);


--
-- Name: idx_redactions_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_redactions_type ON public.redactions USING btree (redaction_type);


--
-- Name: idx_relationships_source; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_relationships_source ON public.relationships USING btree (source_entity_id);


--
-- Name: idx_relationships_target; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_relationships_target ON public.relationships USING btree (target_entity_id);


--
-- Name: idx_relationships_type; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_relationships_type ON public.relationships USING btree (relationship_type);


--
-- Name: idx_task_history_ts; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_task_history_ts ON public.task_history USING btree (task_id, ts DESC);


--
-- Name: idx_transcripts_efta; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_transcripts_efta ON public.transcripts USING btree (efta_number);


--
-- Name: pages pages_search_update; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER pages_search_update BEFORE INSERT OR UPDATE ON public.pages FOR EACH ROW EXECUTE FUNCTION public.pages_search_trigger();

ALTER TABLE public.pages DISABLE TRIGGER pages_search_update;


--
-- Name: clause_fulfillment clause_fulfillment_clause_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clause_fulfillment
    ADD CONSTRAINT clause_fulfillment_clause_id_fkey FOREIGN KEY (clause_id) REFERENCES public.rider_clauses(id);


--
-- Name: clause_fulfillment clause_fulfillment_return_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.clause_fulfillment
    ADD CONSTRAINT clause_fulfillment_return_id_fkey FOREIGN KEY (return_id) REFERENCES public.returns(id);


--
-- Name: edge_sources edge_sources_relationship_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.edge_sources
    ADD CONSTRAINT edge_sources_relationship_id_fkey FOREIGN KEY (relationship_id) REFERENCES public.relationships(id);


--
-- Name: email_participants email_participants_email_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.email_participants
    ADD CONSTRAINT email_participants_email_id_fkey FOREIGN KEY (email_id) REFERENCES public.emails(id);


--
-- Name: external_references external_references_entity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.external_references
    ADD CONSTRAINT external_references_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES public.entities(id);


--
-- Name: relationships relationships_source_entity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_source_entity_id_fkey FOREIGN KEY (source_entity_id) REFERENCES public.entities(id);


--
-- Name: relationships relationships_target_entity_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relationships
    ADD CONSTRAINT relationships_target_entity_id_fkey FOREIGN KEY (target_entity_id) REFERENCES public.entities(id);


--
-- Name: rider_clauses rider_clauses_subpoena_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.rider_clauses
    ADD CONSTRAINT rider_clauses_subpoena_id_fkey FOREIGN KEY (subpoena_id) REFERENCES public.subpoenas(id);


--
-- Name: subpoena_return_links subpoena_return_links_return_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subpoena_return_links
    ADD CONSTRAINT subpoena_return_links_return_id_fkey FOREIGN KEY (return_id) REFERENCES public.returns(id);


--
-- Name: subpoena_return_links subpoena_return_links_subpoena_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subpoena_return_links
    ADD CONSTRAINT subpoena_return_links_subpoena_id_fkey FOREIGN KEY (subpoena_id) REFERENCES public.subpoenas(id);


--
-- PostgreSQL database dump complete
--


