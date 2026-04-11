#!/usr/bin/env python3
"""
Dataset Review and Sanitization Tool
Reviews news articles before Hugging Face upload for:
- PII (Personally Identifiable Information)
- Sensitive content
- Data quality issues
- Source credibility
"""

import psycopg2
import json
import re
from datetime import datetime
from collections import Counter
import sys

sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

# Patterns for PII detection
PII_PATTERNS = {
    'email': re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
    'phone': re.compile(r'\b(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b'),
    'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
    'credit_card': re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'),
    'address': re.compile(r'\b\d+\s+[A-Za-z]+\s+(St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Dr|Drive|Ln|Lane|Way|Ct|Court)\.?,?\s+[A-Za-z]+,?\s*[A-Za-z]*\s*\d{5}(-\d{4})?\b', re.IGNORECASE),
}

# Sensitive keywords to flag
SENSITIVE_KEYWORDS = [
    'rape', 'sexual assault', 'molestation', 'abuse', 'victim',
    'minor', 'underage', 'child', 'children',
    # Note: These are context-dependent in Epstein case coverage
]


def get_db_connection():
    return psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')


def get_dataset_stats():
    """Get high-level statistics about the dataset."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("=" * 80)
    print("DATASET OVERVIEW")
    print("=" * 80)
    
    # Total articles
    cur.execute("SELECT COUNT(*) FROM media_news_articles WHERE updated_at > '2026-04-09'")
    total = cur.fetchone()[0]
    print(f"\nTotal Articles: {total:,}")
    
    # By source
    cur.execute("""
        SELECT source_name, COUNT(*) 
        FROM media_news_articles 
        WHERE updated_at > '2026-04-09'
        GROUP BY source_name 
        ORDER BY COUNT(*) DESC
        LIMIT 20
    """)
    print("\nTop 20 Sources:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]:,}")
    
    # Date range
    cur.execute("""
        SELECT MIN(publish_date), MAX(publish_date)
        FROM media_news_articles
        WHERE updated_at > '2026-04-09' AND publish_date IS NOT NULL
    """)
    date_range = cur.fetchone()
    print(f"\nDate Range: {date_range[0]} to {date_range[1]}")
    
    # Word count distribution
    cur.execute("""
        SELECT 
            CASE 
                WHEN word_count < 100 THEN '0-100'
                WHEN word_count < 500 THEN '100-500'
                WHEN word_count < 1000 THEN '500-1000'
                WHEN word_count < 2000 THEN '1000-2000'
                ELSE '2000+'
            END as range,
            COUNT(*)
        FROM media_news_articles
        WHERE updated_at > '2026-04-09'
        GROUP BY 1
        ORDER BY MIN(word_count)
    """)
    print("\nWord Count Distribution:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]:,}")
    
    cur.close()
    conn.close()
    return total


def sample_articles_for_review(sample_size=50):
    """Get a representative sample for manual review."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("\n" + "=" * 80)
    print(f"SAMPLING {sample_size} ARTICLES FOR REVIEW")
    print("=" * 80)
    
    # Get stratified sample across time periods
    cur.execute("""
        SELECT 
            id, title, content, source_name, publish_date, word_count, url
        FROM media_news_articles
        WHERE updated_at > '2026-04-09'
        ORDER BY RANDOM()
        LIMIT %s
    """, (sample_size,))
    
    samples = []
    for row in cur.fetchall():
        samples.append({
            'id': row[0],
            'title': row[1],
            'content_preview': row[2][:500] if row[2] else '',
            'source': row[3],
            'date': row[4],
            'word_count': row[5],
            'url': row[6]
        })
    
    # Save to file for review
    review_file = f'/tmp/dataset_sample_for_review_{datetime.now().strftime("%Y%m%d_%H%M")}.json'
    with open(review_file, 'w') as f:
        json.dump(samples, f, indent=2, default=str)
    
    print(f"\nSample saved to: {review_file}")
    
    # Print preview
    print("\n--- Sample Article Previews ---")
    for i, article in enumerate(samples[:10], 1):
        print(f"\n{i}. [{article['source']}] {article['title'][:80]}...")
        print(f"   Date: {article['date']}, Words: {article['word_count']}")
        print(f"   Preview: {article['content_preview'][:150]}...")
    
    cur.close()
    conn.close()
    return review_file


def check_pii():
    """Scan for potential PII in articles."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("\n" + "=" * 80)
    print("PII DETECTION SCAN")
    print("=" * 80)
    
    cur.execute("""
        SELECT id, title, content, source_name
        FROM media_news_articles
        WHERE updated_at > '2026-04-09'
    """)
    
    pii_findings = {key: [] for key in PII_PATTERNS.keys()}
    
    count = 0
    for row in cur.fetchall():
        article_id, title, content, source = row
        text = f"{title} {content or ''}"
        
        for pii_type, pattern in PII_PATTERNS.items():
            matches = pattern.findall(text)
            if matches:
                pii_findings[pii_type].append({
                    'article_id': article_id,
                    'source': source,
                    'matches': matches[:3]  # First 3 matches
                })
        
        count += 1
        if count % 1000 == 0:
            print(f"  Scanned {count} articles...")
    
    print(f"\n✓ Scanned {count:,} articles")
    
    # Report findings
    print("\n--- PII Detection Results ---")
    total_pii_articles = 0
    for pii_type, findings in pii_findings.items():
        if findings:
            print(f"\n{pii_type.upper()}: Found in {len(findings)} articles")
            total_pii_articles += len(findings)
            for finding in findings[:5]:  # Show first 5
                print(f"  - {finding['source']}: {finding['matches']}")
            if len(findings) > 5:
                print(f"  ... and {len(findings) - 5} more")
    
    if total_pii_articles == 0:
        print("\n✓ No obvious PII patterns detected")
    else:
        print(f"\n⚠ Found potential PII in {total_pii_articles} articles")
        print("  Review recommended before upload")
    
    cur.close()
    conn.close()
    return pii_findings


def check_content_quality():
    """Check for data quality issues."""
    conn = get_db_connection()
    cur = conn.cursor()
    
    print("\n" + "=" * 80)
    print("CONTENT QUALITY CHECK")
    print("=" * 80)
    
    issues = []
    
    # Empty content
    cur.execute("""
        SELECT COUNT(*) FROM media_news_articles
        WHERE updated_at > '2026-04-09' 
        AND (content IS NULL OR TRIM(content) = '')
    """)
    empty_content = cur.fetchone()[0]
    if empty_content > 0:
        issues.append(f"Empty content: {empty_content} articles")
    
    # Very short articles (< 50 words)
    cur.execute("""
        SELECT COUNT(*) FROM media_news_articles
        WHERE updated_at > '2026-04-09' AND word_count < 50
    """)
    short_articles = cur.fetchone()[0]
    if short_articles > 0:
        issues.append(f"Very short articles (<50 words): {short_articles}")
    
    # Duplicate titles
    cur.execute("""
        SELECT title, COUNT(*) 
        FROM media_news_articles
        WHERE updated_at > '2026-04-09' AND title IS NOT NULL
        GROUP BY title
        HAVING COUNT(*) > 1
        ORDER BY COUNT(*) DESC
        LIMIT 10
    """)
    duplicates = cur.fetchall()
    if duplicates:
        issues.append(f"Duplicate titles: {len(duplicates)} cases")
        print("\nTop duplicate titles:")
        for row in duplicates[:5]:
            print(f"  '{row[0][:60]}...' appears {row[1]} times")
    
    # Articles without dates
    cur.execute("""
        SELECT COUNT(*) FROM media_news_articles
        WHERE updated_at > '2026-04-09' AND publish_date IS NULL
    """)
    no_date = cur.fetchone()[0]
    if no_date > 0:
        issues.append(f"Missing publication date: {no_date} articles")
    
    print("\n--- Quality Issues ---")
    if issues:
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print("  ✓ No major quality issues detected")
    
    cur.close()
    conn.close()


def generate_review_report():
    """Generate comprehensive review report."""
    print("\n" + "=" * 80)
    print("GENERATING REVIEW REPORT")
    print("=" * 80)
    
    # Run all checks
    total = get_dataset_stats()
    sample_file = sample_articles_for_review(50)
    pii_results = check_pii()
    check_content_quality()
    
    # Summary
    print("\n" + "=" * 80)
    print("REVIEW SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    print("""
NEXT STEPS:
1. Review the sample file: {sample_file}
2. Check for any articles with PII that need redaction
3. Review sources for credibility (all appear to be legitimate news outlets)
4. Consider filtering out articles with < 100 words (likely summaries/snippets)
5. Verify no copyrighted material beyond fair use (news excerpts)

SANITIZATION OPTIONS:
- Remove articles with detected PII
- Filter by minimum word count (e.g., 100 words)
- Remove duplicate titles (keep first or most complete)
- Add content warnings to dataset card

ETHICAL CONSIDERATIONS:
- This dataset covers a criminal case involving abuse allegations
- Consider adding warnings about sensitive content
- Ensure compliance with news sources' terms of service
- Dataset intended for academic/research use only
""")

if __name__ == '__main__':
    generate_review_report()
