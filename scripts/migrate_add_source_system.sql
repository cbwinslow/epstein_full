-- Migration: Add source_system columns for Windows RTX 3060 processing
-- This script adds source_system tracking to identify data processed by Windows RTX 3060

-- Safety check: ensure we have a backup before proceeding
-- Backup should be completed before running this script

BEGIN;

-- Add source_system column to documents table
ALTER TABLE documents ADD COLUMN IF NOT EXISTS source_system VARCHAR(50);

-- Add source_system column to pages table  
ALTER TABLE pages ADD COLUMN IF NOT EXISTS source_system VARCHAR(50);

-- Add source_system column to entities table
ALTER TABLE entities ADD COLUMN IF NOT EXISTS source_system VARCHAR(50);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_documents_source_system ON documents(source_system);
CREATE INDEX IF NOT EXISTS idx_pages_source_system ON pages(source_system);
CREATE INDEX IF NOT EXISTS idx_entities_source_system ON entities(source_system);

-- Update existing documents to have a default source_system value
UPDATE documents SET source_system = 'Linux_Server' WHERE source_system IS NULL;

-- Update existing pages to have a default source_system value  
UPDATE pages SET source_system = 'Linux_Server' WHERE source_system IS NULL;

-- Update existing entities to have a default source_system value
UPDATE entities SET source_system = 'Linux_Server' WHERE source_system IS NULL;

-- Verify the columns were added successfully
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name IN ('documents', 'pages', 'entities') 
    AND column_name = 'source_system'
ORDER BY table_name;

-- Show sample data to verify the migration worked
SELECT 
    'documents' as table_name,
    COUNT(*) as total_rows,
    COUNT(source_system) as rows_with_source,
    COUNT(CASE WHEN source_system = 'Linux_Server' THEN 1 END) as linux_server_rows,
    COUNT(CASE WHEN source_system = 'Windows_RTX3060' THEN 1 END) as windows_rtx3060_rows
FROM documents

UNION ALL

SELECT 
    'pages' as table_name,
    COUNT(*) as total_rows,
    COUNT(source_system) as rows_with_source,
    COUNT(CASE WHEN source_system = 'Linux_Server' THEN 1 END) as linux_server_rows,
    COUNT(CASE WHEN source_system = 'Windows_RTX3060' THEN 1 END) as windows_rtx3060_rows
FROM pages

UNION ALL

SELECT 
    'entities' as table_name,
    COUNT(*) as total_rows,
    COUNT(source_system) as rows_with_source,
    COUNT(CASE WHEN source_system = 'Linux_Server' THEN 1 END) as linux_server_rows,
    COUNT(CASE WHEN source_system = 'Windows_RTX3060' THEN 1 END) as windows_rtx3060_rows
FROM entities;

COMMIT;

-- Test queries to verify the migration
-- Query 1: Count documents by source system
SELECT source_system, COUNT(*) as document_count 
FROM documents 
WHERE source_system IS NOT NULL 
GROUP BY source_system 
ORDER BY document_count DESC;

-- Query 2: Count pages by source system
SELECT source_system, COUNT(*) as page_count 
FROM pages 
WHERE source_system IS NOT NULL 
GROUP BY source_system 
ORDER BY page_count DESC;

-- Query 3: Count entities by source system
SELECT source_system, COUNT(*) as entity_count 
FROM entities 
WHERE source_system IS NOT NULL 
GROUP BY source_system 
ORDER BY entity_count DESC;

-- Query 4: Show recent Windows RTX 3060 processed documents (will be empty initially)
SELECT efta_number, file_name, source_system, ocr_method, word_count, page_count
FROM documents 
WHERE source_system = 'Windows_RTX3060'
ORDER BY updated_at DESC
LIMIT 10;