#!/usr/bin/env python3
"""
Cross-reference analysis for supplementary datasets.

Analyzes overlaps between:
- FBI embeddings vs DOJ documents
- House Oversight embeddings vs existing House data
- Full Epstein Index vs existing EFTA documents
"""

import psycopg2
from collections import Counter

# PostgreSQL connection
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "epstein",
    "user": "cbwinslow",
    "password": "123qweasd"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def analyze_fbi_doj_overlap():
    """Analyze overlap between FBI embeddings and DOJ documents."""
    print("\n" + "="*80)
    print("ANALYSIS 1: FBI Embeddings vs DOJ Documents")
    print("="*80)
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Get FBI bates numbers
    cur.execute("SELECT COUNT(DISTINCT bates_number) FROM fbi_embeddings")
    fbi_unique_docs = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM fbi_embeddings")
    fbi_total_chunks = cur.fetchone()[0]
    
    print(f"\n📊 FBI Embeddings Dataset:")
    print(f"   Unique documents (by bates_number): {fbi_unique_docs:,}")
    print(f"   Total embedding chunks: {fbi_total_chunks:,}")
    print(f"   Avg chunks per document: {fbi_total_chunks/fbi_unique_docs:.1f}")
    
    # Check overlap with DOJ documents
    cur.execute("""
        SELECT COUNT(DISTINCT fe.bates_number)
        FROM fbi_embeddings fe
        JOIN documents d ON fe.bates_number = d.efta_number
    """)
    overlap_count = cur.fetchone()[0]
    
    print(f"\n🔍 Overlap Analysis:")
    print(f"   FBI docs matching DOJ EFTA numbers: {overlap_count:,}")
    print(f"   Overlap percentage: {overlap_count/fbi_unique_docs*100:.1f}%")
    print(f"   FBI-exclusive documents: {fbi_unique_docs - overlap_count:,}")
    
    # Sample FBI-exclusive documents
    cur.execute("""
        SELECT DISTINCT fe.bates_number
        FROM fbi_embeddings fe
        LEFT JOIN documents d ON fe.bates_number = d.efta_number
        WHERE d.efta_number IS NULL
        LIMIT 10
    """)
    fbi_exclusive = cur.fetchall()
    
    print(f"\n📋 Sample FBI-exclusive documents:")
    for (bates,) in fbi_exclusive[:5]:
        print(f"   - {bates}")
    
    # Document types in FBI data
    cur.execute("""
        SELECT doc_type, COUNT(*) as count
        FROM fbi_embeddings
        WHERE doc_type IS NOT NULL
        GROUP BY doc_type
        ORDER BY count DESC
        LIMIT 10
    """)
    doc_types = cur.fetchall()
    
    print(f"\n📄 FBI Document Types:")
    for doc_type, count in doc_types:
        print(f"   - {doc_type}: {count:,} chunks")
    
    cur.close()
    conn.close()
    
    return {
        'fbi_unique_docs': fbi_unique_docs,
        'fbi_total_chunks': fbi_total_chunks,
        'overlap_count': overlap_count,
        'fbi_exclusive': fbi_unique_docs - overlap_count
    }


def analyze_house_oversight_overlap():
    """Analyze overlap between House Oversight embeddings and existing data."""
    print("\n" + "="*80)
    print("ANALYSIS 2: House Oversight Embeddings vs Existing Data")
    print("="*80)
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Get House Oversight stats
    cur.execute("SELECT COUNT(*) FROM house_oversight_embeddings")
    house_total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(DISTINCT source_file) FROM house_oversight_embeddings")
    house_unique_files = cur.fetchone()[0]
    
    print(f"\n📊 House Oversight Dataset:")
    print(f"   Total embedding chunks: {house_total:,}")
    print(f"   Unique source files: {house_unique_files:,}")
    
    # Get existing House Oversight email count
    cur.execute("""
        SELECT COUNT(*) 
        FROM jmail_emails 
        WHERE release_batch LIKE '%House Oversight%' 
           OR release_batch LIKE '%house_oversight%'
           OR account_email LIKE '%jeevacation%'
    """)
    existing_emails = cur.fetchone()[0]
    
    print(f"\n🔍 Comparison with Existing Data:")
    print(f"   Existing House Oversight emails: {existing_emails:,}")
    print(f"   New House Oversight chunks: {house_total:,}")
    print(f"   Ratio: {house_total/existing_emails:.1f}x more content with embeddings")
    
    # Sample source files
    cur.execute("""
        SELECT DISTINCT source_file, COUNT(*) as chunks
        FROM house_oversight_embeddings
        GROUP BY source_file
        ORDER BY chunks DESC
        LIMIT 10
    """)
    top_files = cur.fetchall()
    
    print(f"\n📋 Top Source Files by Chunk Count:")
    for source_file, chunks in top_files:
        short_name = source_file[:50] + "..." if len(source_file) > 50 else source_file
        print(f"   - {short_name}: {chunks} chunks")
    
    cur.close()
    conn.close()
    
    return {
        'house_total': house_total,
        'house_unique_files': house_unique_files,
        'existing_emails': existing_emails
    }


def analyze_full_epstein_index():
    """Analyze Full Epstein Index coverage."""
    print("\n" + "="*80)
    print("ANALYSIS 3: Full Epstein Index Coverage")
    print("="*80)
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Get index stats
    cur.execute("SELECT COUNT(*) FROM full_epstein_index")
    index_total = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(DISTINCT efta_id) FROM full_epstein_index")
    index_unique = cur.fetchone()[0]
    
    print(f"\n📊 Full Epstein Index Dataset:")
    print(f"   Total index entries: {index_total:,}")
    print(f"   Unique EFTA IDs: {index_unique:,}")
    
    # Check coverage of our documents
    cur.execute("""
        SELECT COUNT(DISTINCT fei.efta_id)
        FROM full_epstein_index fei
        JOIN documents d ON fei.efta_id = d.efta_number
    """)
    covered_docs = cur.fetchone()[0]
    
    cur.execute("SELECT COUNT(*) FROM documents")
    total_docs = cur.fetchone()[0]
    
    print(f"\n🔍 Coverage Analysis:")
    print(f"   Documents in our database: {total_docs:,}")
    print(f"   Documents covered by index: {covered_docs:,}")
    print(f"   Coverage percentage: {covered_docs/total_docs*100:.1f}%")
    print(f"   Documents not in index: {total_docs - covered_docs:,}")
    
    # Sample EFTAs not in our database
    cur.execute("""
        SELECT fei.efta_id
        FROM full_epstein_index fei
        LEFT JOIN documents d ON fei.efta_id = d.efta_number
        WHERE d.efta_number IS NULL
        LIMIT 10
    """)
    missing_docs = cur.fetchall()
    
    print(f"\n📋 Sample EFTA IDs in index but not our DB:")
    for (efta,) in missing_docs:
        print(f"   - {efta}")
    
    cur.close()
    conn.close()
    
    return {
        'index_total': index_total,
        'index_unique': index_unique,
        'covered_docs': covered_docs,
        'total_docs': total_docs,
        'missing_docs': total_docs - covered_docs
    }


def generate_summary_report(fbi_stats, house_stats, index_stats):
    """Generate summary report."""
    print("\n" + "="*80)
    print("SUMMARY REPORT: Supplementary Dataset Cross-Reference Analysis")
    print("="*80)
    
    print("\n📈 Key Findings:")
    print(f"\n1. FBI Embeddings:")
    print(f"   - {fbi_stats['fbi_unique_docs']:,} unique FBI documents")
    print(f"   - {fbi_stats['overlap_count']:,} overlap with DOJ ({fbi_stats['overlap_count']/fbi_stats['fbi_unique_docs']*100:.1f}%)")
    print(f"   - {fbi_stats['fbi_exclusive']:,} FBI-exclusive documents")
    
    print(f"\n2. House Oversight:")
    print(f"   - {house_stats['house_total']:,} embedding chunks")
    print(f"   - {house_stats['house_unique_files']:,} unique source files")
    print(f"   - Complements {house_stats['existing_emails']:,} existing House Oversight emails")
    
    print(f"\n3. Full Epstein Index:")
    print(f"   - {index_stats['index_unique']:,} unique EFTA IDs")
    print(f"   - {index_stats['covered_docs']:,}/{index_stats['total_docs']:,} documents covered ({index_stats['covered_docs']/index_stats['total_docs']*100:.1f}%)")
    
    print(f"\n💡 Value Added:")
    print(f"   - FBI embeddings provide {fbi_stats['fbi_exclusive']:,} new documents not in DOJ EFTA")
    print(f"   - House Oversight adds document-level embeddings vs thread-level emails we had")
    print(f"   - Full Epstein Index provides text extracts for {index_stats['covered_docs']:,} documents")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    print("🔍 Starting Cross-Reference Analysis...")
    
    # Run analyses
    fbi_stats = analyze_fbi_doj_overlap()
    house_stats = analyze_house_oversight_overlap()
    index_stats = analyze_full_epstein_index()
    
    # Generate summary
    generate_summary_report(fbi_stats, house_stats, index_stats)
    
    print("\n✅ Cross-reference analysis complete!")
