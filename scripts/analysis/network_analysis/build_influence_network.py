#!/usr/bin/env python3
import matplotlib
import networkx as nx
import pandas as pd
import psycopg2

matplotlib.use("Agg")
import logging

import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class InfluenceNetworkBuilder:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self.G = nx.Graph()

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

    def add_politician_nodes(self):
        logger.info("Adding politician nodes...")
        query = """
        SELECT DISTINCT politician_name as name, politician_state as state, 'politician' as type
        FROM congress_trading WHERE politician_name IS NOT NULL AND politician_name != ''
        UNION
        SELECT DISTINCT first_name || ' ' || last_name, state_dst, 'politician'
        FROM house_financial_disclosures WHERE first_name IS NOT NULL AND last_name IS NOT NULL
        UNION
        SELECT DISTINCT first_name || ' ' || last_name, NULL, 'politician'
        FROM senate_financial_disclosures WHERE first_name IS NOT NULL AND last_name IS NOT NULL
        """
        df = pd.read_sql(query, self.conn)
        for _, row in df.iterrows():
            node_id = f"politician:{row['name']}"
            self.G.add_node(
                node_id,
                name=str(row["name"]),
                state=str(row["state"]) if pd.notna(row["state"]) else "",
                type="politician",
                bipartite=0,
            )
        logger.info(
            f"Added {len([n for n in self.G.nodes() if self.G.nodes[n]['type'] == 'politician'])} politician nodes"
        )

    def add_company_nodes(self):
        logger.info("Adding company nodes...")
        query = "SELECT DISTINCT asset_name, asset_type FROM congress_trading WHERE asset_name IS NOT NULL AND asset_name != ''"
        df = pd.read_sql(query, self.conn)
        for _, row in df.iterrows():
            node_id = f"company:{row['asset_name']}"
            self.G.add_node(
                node_id,
                name=str(row["asset_name"]),
                asset_type=str(row["asset_type"]) if pd.notna(row["asset_type"]) else "",
                type="company",
                bipartite=1,
            )
        logger.info(
            f"Added {len([n for n in self.G.nodes() if self.G.nodes[n]['type'] == 'company'])} company nodes"
        )

    def add_donor_nodes(self, min_donation=10000):
        logger.info(f"Adding donor nodes (min: ${min_donation})...")
        query = f"""
        SELECT name, employer, occupation, state, SUM(transaction_amt) as total_donated
        FROM fec_individual_contributions
        WHERE transaction_amt > 0 AND transaction_tp IN ('15','15J','15E') AND cycle >= 2020
        GROUP BY name, employer, occupation, state HAVING SUM(transaction_amt) > {min_donation}
        """
        df = pd.read_sql(query, self.conn)
        for _, row in df.iterrows():
            node_id = f"donor:{row['name']}"
            self.G.add_node(
                node_id,
                name=str(row["name"]),
                employer=str(row["employer"]) if pd.notna(row["employer"]) else "",
                occupation=str(row["occupation"]) if pd.notna(row["occupation"]) else "",
                state=str(row["state"]) if pd.notna(row["state"]) else "",
                total_donated=float(row["total_donated"]),
                type="donor",
                bipartite=2,
            )
        logger.info(
            f"Added {len([n for n in self.G.nodes() if self.G.nodes[n]['type'] == 'donor'])} donor nodes"
        )

    def add_trading_edges(self, min_trades=3):
        logger.info("Adding trading edges...")
        query = f"""
        SELECT politician_name, asset_name, COUNT(*) as trade_count,
               SUM(CASE WHEN transaction_type='p' THEN 1 ELSE 0 END) as purchases,
               SUM(CASE WHEN transaction_type='s' THEN 1 ELSE 0 END) as sales
        FROM congress_trading
        WHERE transaction_date >= '2020-01-01' AND politician_name IS NOT NULL AND asset_name IS NOT NULL
        GROUP BY politician_name, asset_name HAVING COUNT(*) >= {min_trades}
        """
        df = pd.read_sql(query, self.conn)
        edges_added = 0
        for _, row in df.iterrows():
            pol_node = f"politician:{row['politician_name']}"
            comp_node = f"company:{row['asset_name']}"
            if pol_node in self.G and comp_node in self.G:
                self.G.add_edge(
                    pol_node,
                    comp_node,
                    weight=int(row["trade_count"]),
                    purchases=int(row["purchases"]),
                    sales=int(row["sales"]),
                    relationship="trading",
                )
                edges_added += 1
        logger.info(f"Added {edges_added} trading edges")

    def add_contribution_edges(self, min_donation=5000):
        logger.info("Adding contribution edges...")
        query = f"""
        SELECT name, SUM(transaction_amt) as total_donated, COUNT(*) as donation_count
        FROM fec_individual_contributions
        WHERE transaction_amt > 0 AND transaction_tp IN ('15','15J','15E') AND cycle >= 2020
        GROUP BY name HAVING SUM(transaction_amt) > {min_donation}
        """
        donor_df = pd.read_sql(query, self.conn)

        query = """
        SELECT DISTINCT politician_name as name FROM congress_trading WHERE politician_name IS NOT NULL
        UNION
        SELECT DISTINCT first_name || ' ' || last_name FROM house_financial_disclosures WHERE first_name IS NOT NULL
        UNION
        SELECT DISTINCT first_name || ' ' || last_name FROM senate_financial_disclosures WHERE first_name IS NOT NULL
        """
        pol_df = pd.read_sql(query, self.conn)
        politician_names = set(pol_df["name"].dropna().str.strip().str.lower())

        edges_added = 0
        for _, row in donor_df.iterrows():
            donor_name = row["name"].strip().lower()
            if donor_name in politician_names:
                donor_node = f"donor:{row['name']}"
                pol_node = f"politician:{row['name']}"
                if donor_node in self.G and pol_node in self.G:
                    self.G.add_edge(
                        donor_node,
                        pol_node,
                        weight=float(row["total_donated"]),
                        donation_count=int(row["donation_count"]),
                        relationship="self_funding",
                    )
                    edges_added += 1
        logger.info(f"Added {edges_added} contribution edges")

    def analyze_network(self):
        logger.info("Analyzing network...")
        stats = {
            "total_nodes": self.G.number_of_nodes(),
            "total_edges": self.G.number_of_edges(),
            "politicians": len(
                [n for n in self.G.nodes() if self.G.nodes[n]["type"] == "politician"]
            ),
            "companies": len([n for n in self.G.nodes() if self.G.nodes[n]["type"] == "company"]),
            "donors": len([n for n in self.G.nodes() if self.G.nodes[n]["type"] == "donor"]),
        }
        if stats["total_edges"] > 0:
            degree_centrality = nx.degree_centrality(self.G)
            pol_centrality = {
                n: degree_centrality[n]
                for n in self.G.nodes()
                if self.G.nodes[n]["type"] == "politician"
            }
            stats["top_politicians"] = sorted(
                pol_centrality.items(), key=lambda x: x[1], reverse=True
            )[:10]
            stats["density"] = nx.density(self.G)
            stats["connected_components"] = nx.number_connected_components(self.G)
        return stats

    def save_network(self, filepath):
        logger.info(f"Saving network to {filepath}...")
        # Remove None values before saving
        for node in self.G.nodes():
            for key in list(self.G.nodes[node].keys()):
                if self.G.nodes[node][key] is None:
                    del self.G.nodes[node][key]
        nx.write_graphml(self.G, filepath)

    def visualize_network(self, output_path, max_nodes=100):
        logger.info(f"Creating visualization (max {max_nodes} nodes)...")
        if self.G.number_of_nodes() > max_nodes:
            components = list(nx.connected_components(self.G))
            largest = max(components, key=len)
            subgraph = self.G.subgraph(largest).copy()
            if subgraph.number_of_nodes() > max_nodes:
                nodes = list(subgraph.nodes())[:max_nodes]
                subgraph = self.G.subgraph(nodes).copy()
        else:
            subgraph = self.G

        plt.figure(figsize=(20, 15))
        pos = nx.spring_layout(subgraph, k=2, iterations=50)
        node_colors = [
            "#FF6B6B"
            if subgraph.nodes[n]["type"] == "politician"
            else "#4ECDC4"
            if subgraph.nodes[n]["type"] == "company"
            else "#45B7D1"
            for n in subgraph.nodes()
        ]
        nx.draw_networkx_nodes(subgraph, pos, node_color=node_colors, node_size=300, alpha=0.8)
        edge_colors = [
            "#E74C3C" if subgraph.edges[e].get("relationship") == "trading" else "#3498DB"
            for e in subgraph.edges()
        ]
        nx.draw_networkx_edges(subgraph, pos, edge_color=edge_colors, alpha=0.3, width=1)
        if subgraph.number_of_nodes() <= 50:
            labels = {n: subgraph.nodes[n]["name"][:20] for n in subgraph.nodes()}
            nx.draw_networkx_labels(subgraph, pos, labels, font_size=8)
        plt.title(
            f"Influence Network: {self.G.number_of_nodes()} nodes, {self.G.number_of_edges()} edges",
            fontsize=16,
        )
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info(f"Visualization saved to {output_path}")


def main():
    db_config = {"host": "localhost", "database": "epstein", "user": "cbwinslow"}
    builder = InfluenceNetworkBuilder(db_config)
    try:
        builder.connect()
        builder.add_politician_nodes()
        builder.add_company_nodes()
        builder.add_donor_nodes(min_donation=10000)
        builder.add_trading_edges(min_trades=3)
        builder.add_contribution_edges(min_donation=5000)
        stats = builder.analyze_network()
        print("\n" + "=" * 80)
        print("INFLUENCE NETWORK ANALYSIS")
        print("=" * 80)
        print(f"Total Nodes: {stats['total_nodes']}")
        print(f"Total Edges: {stats['total_edges']}")
        print(
            f"\nNode Types: Politicians={stats['politicians']}, Companies={stats['companies']}, Donors={stats['donors']}"
        )
        if stats["total_edges"] > 0:
            print(
                f"\nNetwork Metrics: Density={stats['density']:.4f}, Components={stats['connected_components']}"
            )
            print("\nTop 10 Most Central Politicians:")
            for node, centrality in stats.get("top_politicians", []):
                print(f"  {builder.G.nodes[node]['name']}: {centrality:.4f}")
        print("=" * 80)
        builder.save_network("/home/cbwinslow/workspace/epstein/data/influence_network.graphml")
        builder.visualize_network(
            "/home/cbwinslow/workspace/epstein/reports/influence_network.png", max_nodes=100
        )
    finally:
        builder.close()


if __name__ == "__main__":
    main()
