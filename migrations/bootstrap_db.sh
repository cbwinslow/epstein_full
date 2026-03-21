#!/bin/bash
# =============================================================================
# Epstein Full — PostgreSQL Bootstrap Script
# =============================================================================
#
# Recreates the entire PostgreSQL database from scratch.
# Can be run on a fresh server or to reset the database.
#
# Prerequisites:
#   - PostgreSQL 16 installed and running
#   - pgvector extension available
#   - Python 3.12 with psycopg2
#   - SQLite databases in /mnt/data/epstein-project/databases/
#
# Usage:
#   ./bootstrap_db.sh              # Full setup (create DB, schema, migrate data)
#   ./bootstrap_db.sh --schema     # Schema only (no data migration)
#   ./bootstrap_db.sh --migrate    # Migrate data from SQLite only
#   ./bootstrap_db.sh --validate   # Validate existing database
#   ./bootstrap_db.sh --reset      # Drop and recreate everything
#
# =============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
MIGRATIONS_DIR="$PROJECT_DIR/migrations"
SCRIPTS_DIR="$PROJECT_DIR/scripts"

# PostgreSQL config
PG_HOST="${PG_HOST:-localhost}"
PG_PORT="${PG_PORT:-5432}"
PG_USER="${PG_USER:-cbwinslow}"
PG_PASS="${PG_PASS:-123qweasd}"
PG_DB="${PG_DB:-epstein}"
PG_CONN="postgresql://${PG_USER}:${PG_PASS}@${PG_HOST}:${PG_PORT}/${PG_DB}"

# Data paths
DB_DIR="${DB_DIR:-/mnt/data/epstein-project/databases}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${CYAN}[bootstrap]${NC} $1"; }
ok()  { echo -e "${GREEN}  ✓${NC} $1"; }
warn(){ echo -e "${YELLOW}  ⚠${NC} $1"; }
err() { echo -e "${RED}  ✗${NC} $1"; }

# =============================================================================
# Parse arguments
# =============================================================================
MODE="full"
while [[ $# -gt 0 ]]; do
    case $1 in
        --schema)   MODE="schema"; shift ;;
        --migrate)  MODE="migrate"; shift ;;
        --validate) MODE="validate"; shift ;;
        --reset)    MODE="reset"; shift ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

# =============================================================================
# Helper: run psql command
# =============================================================================
run_sql() {
    PGPASSWORD="$PG_PASS" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" -c "$1" 2>/dev/null
}

run_sql_file() {
    PGPASSWORD="$PG_PASS" psql -h "$PG_HOST" -p "$PG_PORT" -U "$PG_USER" -d "$PG_DB" -f "$1" 2>/dev/null
}

# =============================================================================
# Step 1: Install PostgreSQL + extensions
# =============================================================================
install_postgresql() {
    log "Checking PostgreSQL installation..."
    if command -v psql &>/dev/null; then
        ok "PostgreSQL installed: $(psql --version | head -1)"
    else
        log "Installing PostgreSQL 16..."
        sudo apt-get install -y postgresql-16 postgresql-16-dev 2>/dev/null
        ok "PostgreSQL 16 installed"
    fi

    # pgvector
    if run_sql "SELECT 1 FROM pg_extension WHERE extname='vector'" | grep -q 1; then
        ok "pgvector already installed"
    else
        log "Installing pgvector..."
        sudo apt-get install -y postgresql-16-pgvector 2>/dev/null
        ok "pgvector installed"
    fi
}

# =============================================================================
# Step 2: Create database and user
# =============================================================================
create_database() {
    log "Creating database and user..."

    sudo -u postgres psql -c "CREATE DATABASE $PG_DB;" 2>/dev/null || warn "Database already exists"
    sudo -u postgres psql -c "CREATE USER $PG_USER WITH PASSWORD '$PG_PASS';" 2>/dev/null || warn "User already exists"
    sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $PG_DB TO $PG_USER;" 2>/dev/null
    sudo -u postgres psql -d "$PG_DB" -c "GRANT ALL ON SCHEMA public TO $PG_USER;" 2>/dev/null

    ok "Database '$PG_DB' with user '$PG_USER'"
}

# =============================================================================
# Step 3: Enable extensions
# =============================================================================
enable_extensions() {
    log "Enabling extensions..."

    sudo -u postgres psql -d "$PG_DB" -c "CREATE EXTENSION IF NOT EXISTS vector;" 2>/dev/null
    sudo -u postgres psql -d "$PG_DB" -c "CREATE EXTENSION IF NOT EXISTS pg_trgm;" 2>/dev/null
    sudo -u postgres psql -d "$PG_DB" -c "CREATE EXTENSION IF NOT EXISTS unaccent;" 2>/dev/null
    sudo -u postgres psql -d "$PG_DB" -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;" 2>/dev/null

    ext_count=$(run_sql "SELECT COUNT(*) FROM pg_extension WHERE extname IN ('vector','pg_trgm','unaccent','pg_stat_statements')" | grep -o '[0-9]*' | head -1)
    ok "Extensions enabled: $ext_count/4"
}

# =============================================================================
# Step 4: Apply schema
# =============================================================================
apply_schema() {
    log "Applying schema..."

    if [ -f "$MIGRATIONS_DIR/schema.sql" ]; then
        run_sql_file "$MIGRATIONS_DIR/schema.sql"
        ok "Schema applied from schema.sql"
    elif [ -f "$MIGRATIONS_DIR/001_unified_schema.sql" ]; then
        run_sql_file "$MIGRATIONS_DIR/001_unified_schema.sql"
        ok "Schema applied from 001_unified_schema.sql"
    else
        err "No schema file found in $MIGRATIONS_DIR/"
        exit 1
    fi

    table_count=$(run_sql "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'" | grep -o '[0-9]*' | head -1)
    ok "Tables created: $table_count"
}

# =============================================================================
# Step 5: Configure PostgreSQL
# =============================================================================
configure_postgresql() {
    log "Configuring PostgreSQL for workload..."

    PG_CONF="/etc/postgresql/16/main/postgresql.conf"

    if grep -q "Epstein Project" "$PG_CONF" 2>/dev/null; then
        ok "Config already applied"
        return
    fi

    sudo tee -a "$PG_CONF" > /dev/null << 'EOF'

# === Epstein Project Optimizations (125GB RAM, 40 cores) ===
shared_buffers = 32GB
effective_cache_size = 96GB
work_mem = 256MB
maintenance_work_mem = 8GB
wal_buffers = 64MB
max_parallel_workers_per_gather = 4
max_parallel_maintenance_workers = 4
max_parallel_workers = 16
max_worker_processes = 32
max_connections = 200
checkpoint_completion_target = 0.9
random_page_cost = 1.1
effective_io_concurrency = 200
shared_preload_libraries = 'pg_stat_statements'
EOF

    sudo systemctl restart postgresql 2>/dev/null
    sleep 2
    ok "PostgreSQL configured and restarted"
}

# =============================================================================
# Step 6: Create .pgpass
# =============================================================================
create_pgpass() {
    log "Creating .pgpass..."

    echo "${PG_HOST}:${PG_PORT}:${PG_DB}:${PG_USER}:${PG_PASS}" > ~/.pgpass
    chmod 600 ~/.pgpass
    ok "~/.pgpass created"
}

# =============================================================================
# Step 7: Migrate data from SQLite
# =============================================================================
migrate_data() {
    log "Migrating data from SQLite databases..."

    if [ ! -d "$DB_DIR" ]; then
        err "SQLite databases not found at $DB_DIR"
        exit 1
    fi

    python3 "$SCRIPTS_DIR/migrate_sqlite_to_pg.py" 2>&1 | while read line; do
        echo "  $line"
    done

    ok "Data migration complete"
}

# =============================================================================
# Step 8: Populate FTS
# =============================================================================
populate_fts() {
    log "Populating full-text search vectors..."

    python3 << 'PYEOF'
import psycopg2, time

conn = psycopg2.connect(host="localhost", port=5432, user="cbwinslow", password="123qweasd", dbname="epstein")
conn.autocommit = True
cur = conn.cursor()

batch = 50000
total = 0

while True:
    t = time.time()
    cur.execute("""
        UPDATE pages SET search_vector =
            setweight(to_tsvector('english', coalesce(efta_number, '')), 'A') ||
            setweight(to_tsvector('english', substring(coalesce(text_content, ''), 1, 50000)), 'B')
        WHERE id IN (SELECT id FROM pages WHERE search_vector IS NULL LIMIT %s)
    """, (batch,))
    n = cur.rowcount
    total += n
    if n == 0:
        break
    elapsed = time.time() - t
    print(f"    {n:,} rows in {elapsed:.1f}s (total: {total:,})")

cur.execute("SELECT COUNT(search_vector) FROM pages")
final = cur.fetchone()[0]
print(f"    FTS complete: {final:,} pages indexed")
conn.close()
PYEOF

    ok "FTS populated"
}

# =============================================================================
# Step 9: Validate
# =============================================================================
validate() {
    log "Validating database..."

    python3 << 'PYEOF'
import psycopg2

conn = psycopg2.connect(host="localhost", port=5432, user="cbwinslow", password="123qweasd", dbname="epstein")
cur = conn.cursor()

tables = [
    "documents", "pages", "document_classification", "efta_crosswalk",
    "entities", "relationships", "edge_sources",
    "emails", "email_participants", "resolved_identities",
    "redactions", "document_summary", "reconstructed_pages",
    "images", "ocr_results", "transcripts", "transcript_segments",
    "subpoenas", "rider_clauses", "returns",
]

total = 0
for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM {table}")
    count = cur.fetchone()[0]
    total += count
    status = "✓" if count > 0 else "⚠"
    print(f"    {status} {table}: {count:,}")

print(f"\n    Total: {total:,} rows")

# FTS check
cur.execute("SELECT COUNT(search_vector) FROM pages")
fts = cur.fetchone()[0]
print(f"    FTS: {fts:,} pages indexed")

conn.close()
PYEOF

    ok "Validation complete"
}

# =============================================================================
# Step 10: Reset
# =============================================================================
reset_database() {
    log "Resetting database..."

    sudo -u postgres psql -c "DROP DATABASE IF EXISTS $PG_DB;" 2>/dev/null
    sudo -u postgres psql -c "DROP USER IF EXISTS $PG_USER;" 2>/dev/null

    ok "Database dropped. Run again with --full to recreate."
}

# =============================================================================
# Main
# =============================================================================
main() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Epstein Full — PostgreSQL Bootstrap        ║${NC}"
    echo -e "${CYAN}║  Mode: $(printf '%-38s' $MODE)║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
    echo ""

    case $MODE in
        validate)
            validate
            ;;
        reset)
            reset_database
            ;;
        schema)
            install_postgresql
            create_database
            enable_extensions
            configure_postgresql
            create_pgpass
            apply_schema
            ;;
        migrate)
            migrate_data
            populate_fts
            validate
            ;;
        full)
            install_postgresql
            create_database
            enable_extensions
            configure_postgresql
            create_pgpass
            apply_schema
            migrate_data
            populate_fts
            validate
            ;;
    esac

    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Complete!${NC}"
    echo -e "${GREEN}  Connect: psql -h $PG_HOST -U $PG_USER -d $PG_DB${NC}"
    echo -e "${GREEN}  Datasette: http://localhost:8001${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════${NC}"
    echo ""
}

main
