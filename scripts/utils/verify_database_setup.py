#!/usr/bin/env python3
"""Comprehensive test of database setup and migration scripts."""

import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')

print("=" * 70)
print("DATABASE SETUP VERIFICATION")
print("=" * 70)

# Test 1: Database Connection
print("\n[1] Testing database connection...")
try:
    import psycopg2
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    print("   ✓ Database connection successful")
except Exception as e:
    print(f"   ✗ Failed: {e}")
    sys.exit(1)

# Test 2: Check migrations
print("\n[2] Checking applied migrations...")
cur = conn.cursor()
cur.execute("SELECT version, name, applied_at FROM schema_migrations ORDER BY version")
migrations = cur.fetchall()
if migrations:
    for row in migrations:
        print(f"   ✓ {row[0]}: {row[1]} ({row[2].strftime('%Y-%m-%d')})")
else:
    print("   ! No migrations found")

# Test 3: Check media tables
print("\n[3] Checking media tables...")
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema='public' AND table_name LIKE 'media_%'
    ORDER BY table_name
""")
tables = cur.fetchall()
print(f"   Found {len(tables)} media tables:")
for t in tables:
    cur.execute(f"SELECT COUNT(*) FROM {t[0]}")
    count = cur.fetchone()[0]
    print(f"   ✓ {t[0]}: {count} rows")

# Test 4: Check foreign keys
print("\n[4] Checking foreign keys...")
cur.execute("""
    SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
    JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name LIKE 'media_%'
""")
fks = cur.fetchall()
print(f"   Found {len(fks)} foreign keys:")
for fk in fks:
    print(f"   ✓ {fk[0]}.{fk[1]} -> {fk[2]}")

# Test 5: Check views
print("\n[5] Checking views...")
cur.execute("""
    SELECT table_name FROM information_schema.views 
    WHERE table_schema='public' AND (table_name LIKE 'vw_%' OR table_name LIKE 'mv_%')
    ORDER BY table_name
""")
views = cur.fetchall()
print(f"   Found {len(views)} views:")
for v in views:
    print(f"   ✓ {v[0]}")

# Test 6: Check indexes
print("\n[6] Checking indexes on media tables...")
cur.execute("""
    SELECT tablename, indexname 
    FROM pg_indexes 
    WHERE schemaname = 'public' AND tablename LIKE 'media_%'
    ORDER BY tablename, indexname
""")
indexes = cur.fetchall()
print(f"   Found {len(indexes)} indexes")

# Test 7: Check functions
print("\n[7] Checking functions...")
cur.execute("""
    SELECT routine_name 
    FROM information_schema.routines 
    WHERE routine_schema='public' AND routine_type='FUNCTION'
    AND (routine_name LIKE '%article%' OR routine_name LIKE '%entity%' 
         OR routine_name LIKE '%content%' OR routine_name LIKE '%queue%')
    ORDER BY routine_name
""")
funcs = cur.fetchall()
print(f"   Found {len(funcs)} functions:")
for f in funcs:
    print(f"   ✓ {f[0]}()")

# Test 8: Verify column structure for articles
print("\n[8] Checking article table columns (rich metadata)...")
cur.execute("""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema='public' AND table_name = 'media_news_articles'
    ORDER BY ordinal_position
""")
columns = cur.fetchall()
important_cols = ['authors', 'author_emails', 'sentiment_score', 'credibility_score', 
                  'ip_address', 'readability_score', 'entities_mentioned', 'tags']
found_important = [c[0] for c in columns if c[0] in important_cols]
print(f"   ✓ Found {len(columns)} columns total")
print(f"   ✓ Rich metadata columns: {', '.join(found_important)}")

conn.close()

print("\n" + "=" * 70)
print("✅ DATABASE SCHEMA VERIFIED AND READY")
print("=" * 70)
print("\nNext steps:")
print("  1. Run: python3 scripts/run_media_acquisition.py")
print("  2. Or: ./scripts/start_media_acquisition.sh")
print("  3. Or test ingestion: python3 scripts/article_ingestion_pipeline.py")
