DROP TABLE IF EXISTS entity_raw_names;
DROP TABLE IF EXISTS entity_resolutions;

CREATE TABLE entity_resolutions (
    resolution_id SERIAL PRIMARY KEY,
    standardized_name VARCHAR(500),
    entity_type VARCHAR(50),
    state VARCHAR(10),
    source_count INTEGER,
    unique_sources INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE entity_raw_names (
    id SERIAL PRIMARY KEY,
    resolution_id INTEGER REFERENCES entity_resolutions(resolution_id),
    raw_name VARCHAR(500),
    entity_type VARCHAR(50),
    source_table VARCHAR(50),
    state VARCHAR(10)
);

CREATE INDEX idx_entity_std ON entity_resolutions(standardized_name);
CREATE INDEX idx_entity_type ON entity_resolutions(entity_type);
CREATE INDEX idx_raw_resolution ON entity_raw_names(resolution_id);

-- Insert all unique standardized names
INSERT INTO entity_resolutions (standardized_name, entity_type, state, source_count, unique_sources)
SELECT
    std_name,
    etype,
    state,
    COUNT(*) as source_count,
    COUNT(DISTINCT etype) as unique_sources
FROM (
    SELECT DISTINCT
        politician_name as full_name,
        'politician' as etype,
        politician_state as state
    FROM congress_trading
    WHERE politician_name IS NOT NULL AND politician_name != ''

    UNION ALL

    SELECT DISTINCT
        first_name || ' ' || last_name,
        'politician',
        state_dst
    FROM house_financial_disclosures
    WHERE first_name IS NOT NULL AND last_name IS NOT NULL

    UNION ALL

    SELECT DISTINCT
        first_name || ' ' || last_name,
        'politician',
        NULL
    FROM senate_financial_disclosures
    WHERE first_name IS NOT NULL AND last_name IS NOT NULL

    UNION ALL

    SELECT DISTINCT
        asset_name,
        'company',
        NULL
    FROM congress_trading
    WHERE asset_name IS NOT NULL AND asset_name != ''

    UNION ALL

    SELECT DISTINCT
        client_name,
        'lobbying_client',
        NULL
    FROM lda_filings
    WHERE client_name IS NOT NULL AND client_name != ''

    UNION ALL

    SELECT DISTINCT
        name,
        'donor',
        state
    FROM fec_individual_contributions
    WHERE name IS NOT NULL AND name != '' AND transaction_amt > 0
) all_names
CROSS JOIN LATERAL (
    SELECT
        LOWER(TRIM(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    TRANSLATE(
                        UNACCENT(full_name),
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'abcdefghijklmnopqrstuvwxyz'
                    ),
                    '[^a-z0-9\\s\\-]', ' ', 'g'
                ),
                '\\s+', ' ', 'g'
            )
        )) as std_name
) normalized
GROUP BY std_name, etype, state
ORDER BY source_count DESC;

-- Insert raw names
INSERT INTO entity_raw_names (resolution_id, raw_name, entity_type, source_table, state)
SELECT
    er.resolution_id,
    an.full_name,
    an.etype,
    'combined_sources',
    an.state
FROM (
    SELECT DISTINCT
        politician_name as full_name,
        'politician' as etype,
        politician_state as state
    FROM congress_trading
    WHERE politician_name IS NOT NULL AND politician_name != ''

    UNION ALL

    SELECT DISTINCT
        first_name || ' ' || last_name,
        'politician',
        state_dst
    FROM house_financial_disclosures
    WHERE first_name IS NOT NULL AND last_name IS NOT NULL

    UNION ALL

    SELECT DISTINCT
        first_name || ' ' || last_name,
        'politician',
        NULL
    FROM senate_financial_disclosures
    WHERE first_name IS NOT NULL AND last_name IS NOT NULL

    UNION ALL

    SELECT DISTINCT
        asset_name,
        'company',
        NULL
    FROM congress_trading
    WHERE asset_name IS NOT NULL AND asset_name != ''

    UNION ALL

    SELECT DISTINCT
        client_name,
        'lobbying_client',
        NULL
    FROM lda_filings
    WHERE client_name IS NOT NULL AND client_name != ''

    UNION ALL

    SELECT DISTINCT
        name,
        'donor',
        state
    FROM fec_individual_contributions
    WHERE name IS NOT NULL AND name != '' AND transaction_amt > 0
) an
CROSS JOIN LATERAL (
    SELECT
        LOWER(TRIM(
            REGEXP_REPLACE(
                REGEXP_REPLACE(
                    TRANSLATE(
                        UNACCENT(an.full_name),
                        'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
                        'abcdefghijklmnopqrstuvwxyz'
                    ),
                    '[^a-z0-9\\s\\-]', ' ', 'g'
                ),
                '\\s+', ' ', 'g'
            )
        )) as std_name
) normalized
JOIN entity_resolutions er ON er.standardized_name = normalized.std_name;

SELECT 'Entity resolution complete!' as status;
SELECT entity_type, COUNT(*) as count FROM entity_resolutions GROUP BY entity_type ORDER BY count DESC;
