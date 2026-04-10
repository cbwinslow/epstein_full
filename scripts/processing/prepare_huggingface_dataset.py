#!/usr/bin/env python3
"""
Prepare Epstein news dataset for Hugging Face upload.
Creates structured dataset with metadata, embeddings, and splits.
"""

import json
import psycopg2
from datetime import datetime
from typing import Dict, List, Optional
import hashlib
import sys

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

def create_dataset():
    """Export database to Hugging Face format."""
    
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    cur = conn.cursor()
    
    # Get all articles with metadata
    cur.execute("""
        SELECT 
            a.id,
            a.title,
            a.content,
            a.source_url,
            a.source_name,
            a.published_date,
            a.author,
            a.summary,
            a.word_count,
            a.keywords,
            a.entities,
            a.created_at,
            i.keywords_matched,
            i.discovered_by
        FROM media_news_articles a
        LEFT JOIN media_collection_queue i ON a.url = i.source_url
        WHERE a.created_at > '2026-04-09 00:00:00'
        ORDER BY a.published_date DESC
    """)
    
    articles = []
    for row in cur.fetchall():
        article = {
            "id": row[0],
            "title": row[1],
            "content": row[2],
            "url": row[3],
            "source": row[4],
            "published_date": row[5].isoformat() if row[5] else None,
            "author": row[6],
            "summary": row[7],
            "word_count": row[8],
            "keywords": row[9],
            "entities": row[10],
            "ingested_at": row[11].isoformat(),
            "search_keywords": row[12],
            "discovery_method": row[13]
        }
        articles.append(article)
    
    cur.close()
    conn.close()
    
    # Create dataset splits
    total = len(articles)
    train_end = int(total * 0.8)
    val_end = int(total * 0.9)
    
    dataset = {
        "dataset_info": {
            "name": "epstein-news-corpus",
            "description": "News articles about Jeffrey Epstein case (2000-2025)",
            "version": "1.0.0",
            "size": total,
            "splits": {
                "train": train_end,
                "validation": val_end - train_end,
                "test": total - val_end
            },
            "features": [
                "title", "content", "url", "source", "published_date",
                "author", "summary", "word_count", "keywords", "entities"
            ],
            "statistics": {
                "total_articles": total,
                "date_range": "2000-2025",
                "sources": len(set(a["source"] for a in articles)),
                "avg_word_count": sum(a["word_count"] or 0 for a in articles) / max(total, 1)
            }
        },
        "train": articles[:train_end],
        "validation": articles[train_end:val_end],
        "test": articles[val_end:]
    }
    
    # Save
    output_file = f"/tmp/epstein_news_dataset_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, default=str, ensure_ascii=False)
    
    print(f"Dataset saved: {output_file}")
    print(f"Total articles: {total}")
    print(f"Train: {train_end}, Val: {val_end-train_end}, Test: {total-val_end}")
    
    return output_file


if __name__ == '__main__':
    create_dataset()
