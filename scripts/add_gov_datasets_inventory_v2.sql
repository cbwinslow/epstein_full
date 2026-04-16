-- Add government datasets to master inventory (v2 - matching existing schema)
-- Target timeframe: 2000-2025 where applicable

-- FEC 2025 Data
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'FEC 2025 Individual Contributions',
    'fec',
    'Federal Election Commission 2025 election cycle individual contributions',
    'fec_individual_contributions_2025',
    20000000,
    'pending',
    1,
    'https://www.fec.gov/files/bulk-downloads/2025/indiv25.zip',
    '{"format": "CSV", "size_gb": 3, "file_pattern": "indiv25.zip", "bulk_download": true, "api_required": false, "github_issue": "#88", "historical_range": "2000-2025"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- SEC EDGAR Form 4
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'SEC EDGAR Form 4 Insider Trading',
    'sec_edgar',
    'SEC Form 4 insider transaction filings (2000-2025)',
    'sec_insider_transactions',
    8000000,
    'pending',
    1,
    'https://www.sec.gov/Archives/edgar/daily-index/',
    '{"format": "XML/XBRL", "rate_limit": "10/sec", "user_agent_required": true, "forms": ["4", "3", "5"], "api_required": false, "github_issue": "#89", "historical_range": "2000-2025"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- SEC EDGAR Form 13F
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'SEC EDGAR Form 13F Institutional Holdings',
    'sec_edgar',
    'SEC Form 13F institutional investment manager holdings',
    'sec_13f_holdings',
    500000,
    'pending',
    2,
    'https://www.sec.gov/Archives/edgar/daily-index/',
    '{"format": "XML", "threshold": "$100M", "forms": ["13F-HR"], "api_required": false, "github_issue": "#89"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- White House Visitor Logs
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'White House Visitor Logs',
    'whitehouse',
    'White House WAVES visitor access records (2009-2025)',
    'whitehouse_visitors',
    5000000,
    'pending',
    1,
    'https://www.whitehouse.gov/disclosures/visitor-logs/',
    '{"format": "CSV/JSON", "api_available": true, "coverage": "Obama-present", "api_required": false, "github_issue": "#90", "historical_range": "2009-2025"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- Congress.gov Bills
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'Congress.gov Bills & Legislation',
    'congress',
    'Congressional bills, resolutions, and legislative actions (2000-2025)',
    'congress_bills',
    200000,
    'pending',
    2,
    'https://api.congress.gov/v3/',
    '{"format": "JSON", "rate_limit": "5000/day", "endpoints": ["bill", "amendment"], "api_required": true, "api_key_location": ".env CONGRESS_API_KEY", "github_issue": "#91"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- Congress.gov Members
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'Congress.gov Members & Votes',
    'congress',
    'Congress member biographies and roll call votes',
    'congress_members',
    10000,
    'pending',
    2,
    'https://api.congress.gov/v3/',
    '{"format": "JSON", "endpoints": ["member", "vote"], "api_required": true, "api_key_location": ".env CONGRESS_API_KEY", "github_issue": "#91"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- GovInfo Federal Register
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'GovInfo Federal Register',
    'govinfo',
    'Federal Register documents and regulations (2000-2025)',
    'federal_register',
    100000,
    'pending',
    2,
    'https://api.govinfo.gov/',
    '{"format": "JSON", "collections": ["FR"], "api_required": true, "api_key_location": ".env GOVINFO_API_KEY", "github_issue": "#92"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- GovInfo Court Opinions
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'GovInfo Court Opinions',
    'govinfo',
    'Federal court opinions and decisions',
    'court_opinions',
    50000,
    'pending',
    3,
    'https://api.govinfo.gov/',
    '{"format": "JSON/PDF", "collections": ["USCOURTS"], "api_required": true, "api_key_location": ".env GOVINFO_API_KEY", "github_issue": "#92"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- FARA
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'FARA Registrations',
    'fara',
    'Foreign Agent Registration Act registrations (2000-2025)',
    'fara_registrations',
    50000,
    'pending',
    2,
    'https://www.justice.gov/nsd-fara',
    '{"format": "XML/HTML", "method": "web_scraping", "exhibits": ["A", "B", "C", "D"], "api_required": false, "github_issue": "#93"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- Lobbying
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'Lobbying Disclosure Database',
    'lobbying',
    'Senate lobbying registration and reports (2000-2025)',
    'lobbying_disclosures',
    200000,
    'pending',
    2,
    'https://www.senate.gov/legislative/lobbying.htm',
    '{"format": "CSV/XML", "types": ["LD-1", "LD-2"], "method": "download", "api_required": false, "github_issue": "#94"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- USA Spending
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, metadata
) VALUES (
    'USA Spending Federal Awards',
    'usaspending',
    'Federal contract, grant, and loan data (2007-2025)',
    'usa_spending',
    50000000,
    'pending',
    2,
    'https://api.usaspending.gov/',
    '{"format": "JSON", "types": ["contracts", "grants", "loans"], "bulk_available": true, "api_required": false, "github_issue": "#94"}'::jsonb
) ON CONFLICT (source_name) DO NOTHING;

-- Show summary
SELECT 
    source_type,
    COUNT(*) as datasets,
    SUM(expected_records) as total_expected_records,
    COUNT(*) FILTER (WHERE metadata->>'api_required' = 'true') as api_key_required,
    COUNT(*) FILTER (WHERE metadata->>'api_required' = 'false') as no_api_key_required
FROM data_inventory 
WHERE source_type IN ('fec', 'sec_edgar', 'whitehouse', 'congress', 'govinfo', 'fara', 'lobbying', 'usaspending')
GROUP BY source_type
ORDER BY datasets DESC;
