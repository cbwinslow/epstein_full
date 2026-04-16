-- Add government datasets to master inventory
-- Target timeframe: 2000-2025 where applicable

-- FEC 2025 Data (Phase 1 - No API Key)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'FEC 2025 Individual Contributions',
    'fec',
    'Federal Election Commission 2025 election cycle individual contributions',
    'fec_individual_contributions_2025',
    20000000, -- ~20M estimated
    'pending',
    1,
    'https://www.fec.gov/files/bulk-downloads/2025/indiv25.zip',
    'https://github.com/cbwinslow/epstein/issues/88',
    false,
    NULL,
    'free',
    'weekly',
    '2025-01-01',
    '2025-12-31',
    '{"format": "CSV", "size_gb": 3, "file_pattern": "indiv25.zip", "bulk_download": true}'::jsonb
);

-- SEC EDGAR Insider Trading (Phase 1 - No API Key)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'SEC EDGAR Form 4 Insider Trading',
    'sec_edgar',
    'SEC Form 4 insider transaction filings',
    'sec_insider_transactions',
    8000000, -- ~8M estimated (2000-2025)
    'pending',
    1,
    'https://www.sec.gov/Archives/edgar/daily-index/',
    'https://github.com/cbwinslow/epstein/issues/89',
    false,
    NULL,
    'free',
    'daily',
    '2000-01-01',
    '2025-12-31',
    '{"format": "XML/XBRL", "rate_limit": "10/sec", "user_agent_required": true, "forms": ["4", "3", "5"]}'::jsonb
);

INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'SEC EDGAR Form 13F Institutional Holdings',
    'sec_edgar',
    'SEC Form 13F institutional investment manager holdings',
    'sec_13f_holdings',
    500000, -- ~500K estimated
    'pending',
    2,
    'https://www.sec.gov/Archives/edgar/daily-index/',
    'https://github.com/cbwinslow/epstein/issues/89',
    false,
    NULL,
    'free',
    'quarterly',
    '2000-01-01',
    '2025-12-31',
    '{"format": "XML", "threshold": "$100M", "forms": ["13F-HR"]}'::jsonb
);

-- White House Visitor Logs (Phase 1 - No API Key)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'White House Visitor Logs',
    'whitehouse',
    'White House WAVES visitor access records',
    'whitehouse_visitors',
    5000000, -- ~5M estimated (2009-2025)
    'pending',
    1,
    'https://www.whitehouse.gov/disclosures/visitor-logs/',
    'https://github.com/cbwinslow/epstein/issues/90',
    false,
    NULL,
    'free',
    'monthly',
    '2009-01-01',
    '2025-12-31',
    '{"format": "CSV/JSON", "api_available": true, "coverage": "Obama-present"}'::jsonb
);

-- Congress.gov (Phase 2 - API Key Required)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'Congress.gov Bills & Legislation',
    'congress',
    'Congressional bills, resolutions, and legislative actions',
    'congress_bills',
    200000, -- ~200K estimated
    'pending',
    2,
    'https://api.congress.gov/v3/',
    'https://github.com/cbwinslow/epstein/issues/91',
    true,
    '.env (CONGRESS_API_KEY)',
    'free',
    'realtime',
    '2000-01-01',
    '2025-12-31',
    '{"format": "JSON", "rate_limit": "5000/day", "endpoints": ["bill", "amendment"]}'::jsonb
);

INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'Congress.gov Members & Votes',
    'congress',
    'Congress member biographies and roll call votes',
    'congress_members',
    10000, -- ~10K members
    'pending',
    2,
    'https://api.congress.gov/v3/',
    'https://github.com/cbwinslow/epstein/issues/91',
    true,
    '.env (CONGRESS_API_KEY)',
    'free',
    'realtime',
    '2000-01-01',
    '2025-12-31',
    '{"format": "JSON", "endpoints": ["member", "vote"], "vote_details": true}'::jsonb
);

-- GovInfo.gov (Phase 2 - API Key Required)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'GovInfo Federal Register',
    'govinfo',
    'Federal Register documents and regulations',
    'federal_register',
    100000, -- ~100K estimated
    'pending',
    2,
    'https://api.govinfo.gov/',
    'https://github.com/cbwinslow/epstein/issues/92',
    true,
    '.env (GOVINFO_API_KEY)',
    'free',
    'daily',
    '2000-01-01',
    '2025-12-31',
    '{"format": "JSON", "collections": ["FR"], "searchable": true}'::jsonb
);

INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'GovInfo Court Opinions',
    'govinfo',
    'Federal court opinions and decisions',
    'court_opinions',
    50000, -- ~50K estimated
    'pending',
    3,
    'https://api.govinfo.gov/',
    'https://github.com/cbwinslow/epstein/issues/92',
    true,
    '.env (GOVINFO_API_KEY)',
    'free',
    'weekly',
    '2004-01-01',
    '2025-12-31',
    '{"format": "JSON/PDF", "collections": ["USCOURTS"]}'::jsonb
);

-- FARA (Phase 1 - Web Scraping)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'FARA Registrations',
    'fara',
    'Foreign Agent Registration Act registrations',
    'fara_registrations',
    50000, -- ~50K estimated
    'pending',
    2,
    'https://www.justice.gov/nsd-fara',
    'https://github.com/cbwinslow/epstein/issues/93',
    false,
    NULL,
    'free',
    'continuous',
    '2000-01-01',
    '2025-12-31',
    '{"format": "XML/HTML", "method": "web_scraping", "exhibits": ["A", "B", "C", "D"]}'::jsonb
);

-- Lobbying (Phase 1 - Web Download)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'Lobbying Disclosure Database',
    'lobbying',
    'Senate lobbying registration and reports',
    'lobbying_disclosures',
    200000, -- ~200K estimated
    'pending',
    2,
    'https://www.senate.gov/legislative/lobbying.htm',
    'https://github.com/cbwinslow/epstein/issues/94',
    false,
    NULL,
    'free',
    'quarterly',
    '2000-01-01',
    '2025-12-31',
    '{"format": "CSV/XML", "types": ["LD-1", "LD-2"], "method": "download"}'::jsonb
);

-- USA Spending (Phase 1 - API No Key)
INSERT INTO data_inventory (
    source_name, source_type, description, target_table, 
    expected_records, status, priority, source_path, 
    github_issue_url, api_key_required, api_key_location, 
    cost, update_frequency, historical_start, historical_end,
    metadata
) VALUES (
    'USA Spending Federal Awards',
    'usaspending',
    'Federal contract, grant, and loan data',
    'usa_spending',
    50000000, -- ~50M estimated (2007-2025)
    'pending',
    2,
    'https://api.usaspending.gov/',
    'https://github.com/cbwinslow/epstein/issues/95',
    false,
    NULL,
    'free',
    'daily',
    '2007-01-01',
    '2025-12-31',
    '{"format": "JSON", "types": ["contracts", "grants", "loans"], "bulk_available": true}'::jsonb
);

-- Update summary
SELECT 
    source_type,
    COUNT(*) as datasets,
    SUM(expected_records) as total_expected_records,
    COUNT(*) FILTER (WHERE api_key_required) as api_key_required,
    COUNT(*) FILTER (WHERE NOT api_key_required) as no_api_key_required
FROM data_inventory 
WHERE source_type IN ('fec', 'sec_edgar', 'whitehouse', 'congress', 'govinfo', 'fara', 'lobbying', 'usaspending')
GROUP BY source_type
ORDER BY datasets DESC;
