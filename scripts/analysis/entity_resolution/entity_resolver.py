#!/usr/bin/env python3
import logging
import re
import time
import unicodedata

import pandas as pd
import psycopg2

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class EntityResolver:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
            logger.info("Connected to database")
        except Exception as e:
            logger.error(f"DB connection failed: {e}")
            raise

    def close(self):
        if self.conn:
            self.conn.close()

    @staticmethod
    def normalize_name(name):
        if not name or not isinstance(name, str):
            return ""
        name = name.lower().strip()
        name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("ASCII")
        titles = ["mr\\.?", "mrs\\.?", "ms\\.?", "dr\\.?", "hon\\.?", "rep\\.?", "sen\\.?"]
        for title in titles:
            name = re.sub(r"^" + title + r"\\s+", "", name)
        name = re.sub(r"[^a-z0-9\\s\\-]", " ", name)
        name = re.sub(r"\\s+", " ", name)
        return name.strip()

    def resolve_entities(self):
        logger.info("Extracting entities...")
        start = time.time()

        query = """
        SELECT DISTINCT
            politician_name as name_field,
            'politician' as etype,
            politician_state as state,
            politician_party as extra
        FROM congress_trading
        WHERE politician_name IS NOT NULL AND politician_name != ''

        UNION

        SELECT DISTINCT
            first_name || ' ' || last_name,
            'politician',
            state_dst,
            filing_type
        FROM house_financial_disclosures
        WHERE first_name IS NOT NULL AND last_name IS NOT NULL

        UNION

        SELECT DISTINCT
            first_name || ' ' || last_name,
            'politician',
            NULL,
            office_name
        FROM senate_financial_disclosures
        WHERE first_name IS NOT NULL AND last_name IS NOT NULL

        UNION

        SELECT DISTINCT
            asset_name,
            'company',
            NULL,
            asset_type
        FROM congress_trading
        WHERE asset_name IS NOT NULL AND asset_name != ''

        UNION

        SELECT DISTINCT
            client_name,
            'lobbying_client',
            NULL,
            registrant_name
        FROM lda_filings
        WHERE client_name IS NOT NULL AND client_name != ''

        UNION

        SELECT DISTINCT
            name,
            'donor',
            state,
            occupation
        FROM fec_individual_contributions
        WHERE name IS NOT NULL AND name != '' AND transaction_amt > 0
        """

        cur = self.conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        cur.close()

        df = pd.DataFrame(rows, columns=["full_name", "etype", "state", "extra"])
        df = df.dropna(subset=["full_name"])
        df = df[df["full_name"].str.strip() != ""]
        df["std_name"] = df["full_name"].apply(self.normalize_name)
        df = df[df["std_name"] != ""]

        logger.info(f"Processing {len(df)} name records ({time.time() - start:.1f}s)")

        # FAST GROUPING: Use pandas groupby on standardized name
        # This is much faster than iterating
        df["group_id"] = df.groupby("std_name").ngroup()

        total_groups = df["group_id"].nunique()
        logger.info(f"Created {total_groups} entity groups ({time.time() - start:.1f}s)")
        return df

    def save_resolutions(self, df):
        logger.info("Saving to database...")
        start = time.time()

        cur = self.conn.cursor()
        cur.execute("""
        DROP TABLE IF EXISTS entity_raw_names;
        DROP TABLE IF EXISTS entity_resolutions;

        CREATE TABLE entity_resolutions (
            resolution_id SERIAL PRIMARY KEY,
            standardized_name VARCHAR(500),
            entity_type VARCHAR(50),
            state VARCHAR(2),
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
            state VARCHAR(2)
        );

        CREATE INDEX idx_entity_std ON entity_resolutions(standardized_name);
        CREATE INDEX idx_entity_type ON entity_resolutions(entity_type);
        CREATE INDEX idx_raw_resolution ON entity_raw_names(resolution_id);
        """)

        total_groups = df["group_id"].nunique()
        logger.info(f"Inserting {total_groups} entity groups...")

        # Process in batches
        batch_size = 5000
        groups = df["group_id"].unique()

        for i in range(0, len(groups), batch_size):
            batch_groups = groups[i : i + batch_size]
            batch_df = df[df["group_id"].isin(batch_groups)]

            for gid in batch_groups:
                group = batch_df[batch_df["group_id"] == gid]
                std_name = group["std_name"].iloc[0][:499]  # Truncate for safety
                etype = group["etype"].mode()[0] if not group["etype"].mode().empty else "unknown"
                state = group["state"].mode()[0] if not group["state"].mode().empty else None

                try:
                    cur.execute(
                        """
                    INSERT INTO entity_resolutions (standardized_name, entity_type, state, source_count, unique_sources)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING resolution_id;
                    """,
                        (std_name, etype, state, len(group), group["etype"].nunique()),
                    )

                    rid = cur.fetchone()[0]
                except Exception as e:
                    logger.warning(f"Error inserting {std_name}: {e}")
                    continue

                # Batch insert raw names
                raw_values = []
                for _, row in group.iterrows():
                    raw_name = row["full_name"][:499] if row["full_name"] else ""
                    raw_values.append(
                        (rid, raw_name, row["etype"], "combined_sources", row["state"])
                    )

                args_str = ",".join(
                    cur.mogrify("(%s,%s,%s,%s,%s)", v).decode("utf-8") for v in raw_values
                )
                cur.execute(
                    "INSERT INTO entity_raw_names (resolution_id, raw_name, entity_type, source_table, state) VALUES "
                    + args_str
                )

            self.conn.commit()
            logger.info(
                f"  Progress: {i + len(batch_groups)}/{total_groups} ({time.time() - start:.1f}s)"
            )

        cur.close()
        logger.info(f"Saved all resolutions ({time.time() - start:.1f}s)")


def main():
    db_config = {"host": "localhost", "database": "epstein", "user": "cbwinslow"}
    resolver = EntityResolver(db_config)
    try:
        resolver.connect()
        df = resolver.resolve_entities()
        resolver.save_resolutions(df)
        print(f"\n{'=' * 80}")
        print("ENTITY RESOLUTION SUMMARY")
        print(f"{'=' * 80}")
        print(f"Total records processed: {len(df)}")
        print(f"Unique entities resolved: {df['group_id'].nunique()}")
        print("\nEntity types:")
        print(df["etype"].value_counts())
        print(f"\n{'=' * 80}")
    finally:
        resolver.close()


if __name__ == "__main__":
    main()
