#!/usr/bin/env python3
"""
Database Migration Runner
Applies schema migrations to the PostgreSQL database.
"""

import argparse
import hashlib
import logging
import os
import re
import sys
import time
from pathlib import Path

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DEFAULT_DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://cbwinslow:123qweasd@localhost:5432/epstein'
)
MIGRATIONS_DIR = Path(__file__).parent


class MigrationRunner:
    """Manages database migrations."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.conn = None
    
    def connect(self):
        """Connect to database."""
        self.conn = psycopg2.connect(self.database_url)
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        logger.info(f"✓ Connected to database")
    
    def disconnect(self):
        """Disconnect from database."""
        if self.conn:
            self.conn.close()
            logger.info("✓ Disconnected from database")
    
    def ensure_migrations_table(self):
        """Ensure schema_migrations table exists."""
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id SERIAL PRIMARY KEY,
                    version VARCHAR(50) NOT NULL UNIQUE,
                    name TEXT NOT NULL,
                    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    applied_by TEXT DEFAULT CURRENT_USER,
                    checksum VARCHAR(64),
                    execution_time_ms INTEGER
                )
            """)
        logger.info("✓ Migrations table ready")
    
    def get_applied_migrations(self) -> set:
        """Get set of already applied migration versions."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT version FROM schema_migrations")
                return {row[0] for row in cur.fetchall()}
        except psycopg2.errors.UndefinedTable:
            return set()
    
    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of migration file."""
        with open(file_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    
    def parse_migration_file(self, file_path: Path) -> dict:
        """Parse migration file for version and name."""
        content = file_path.read_text()
        
        # Extract version from filename (001_description.sql -> 001)
        version_match = re.match(r'^(\d+)_.*\.sql$', file_path.name)
        if not version_match:
            raise ValueError(f"Invalid migration filename: {file_path.name}")
        
        version = version_match.group(1)
        
        # Extract name from first comment or filename
        name_match = re.search(r'--\s*Migration:\s*(.+)', content)
        if name_match:
            name = name_match.group(1).strip()
        else:
            # Use filename without extension and version
            name = file_path.stem.replace(f'{version}_', '').replace('_', ' ').title()
        
        return {
            'version': version,
            'name': name,
            'content': content,
            'file': file_path
        }
    
    def apply_migration(self, migration: dict, dry_run: bool = False) -> bool:
        """Apply a single migration."""
        version = migration['version']
        name = migration['name']
        content = migration['content']
        
        logger.info(f"Applying migration {version}: {name}")
        
        if dry_run:
            logger.info(f"  [DRY RUN] Would execute {len(content)} characters of SQL")
            return True
        
        try:
            start_time = time.time()
            
            with self.conn.cursor() as cur:
                # Execute migration
                cur.execute(content)
                
                # Record migration
                checksum = self.calculate_checksum(migration['file'])
                execution_time = int((time.time() - start_time) * 1000)
                
                cur.execute("""
                    INSERT INTO schema_migrations (version, name, checksum, execution_time_ms)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (version) DO UPDATE SET
                        name = EXCLUDED.name,
                        checksum = EXCLUDED.checksum,
                        execution_time_ms = EXCLUDED.execution_time_ms,
                        applied_at = NOW()
                """, (version, name, checksum, execution_time))
            
            logger.info(f"  ✓ Applied in {execution_time}ms")
            return True
            
        except Exception as e:
            logger.error(f"  ✗ Failed: {e}")
            self.conn.rollback()
            return False
    
    def list_pending_migrations(self) -> list:
        """Get list of pending migrations."""
        applied = self.get_applied_migrations()
        
        pending = []
        for sql_file in sorted(MIGRATIONS_DIR.glob('*.sql')):
            if sql_file.name == '001_create_media_tables.sql':
                migration = self.parse_migration_file(sql_file)
                if migration['version'] not in applied:
                    pending.append(migration)
        
        return pending
    
    def apply_all(self, dry_run: bool = False) -> bool:
        """Apply all pending migrations."""
        pending = self.list_pending_migrations()
        
        if not pending:
            logger.info("No pending migrations")
            return True
        
        logger.info(f"Found {len(pending)} pending migration(s)")
        
        success = True
        for migration in pending:
            if not self.apply_migration(migration, dry_run):
                success = False
                break
        
        return success
    
    def apply_version(self, version: str, dry_run: bool = False) -> bool:
        """Apply specific migration version."""
        applied = self.get_applied_migrations()
        
        if version in applied:
            logger.info(f"Migration {version} already applied")
            return True
        
        # Find migration file
        for sql_file in MIGRATIONS_DIR.glob('*.sql'):
            migration = self.parse_migration_file(sql_file)
            if migration['version'] == version:
                return self.apply_migration(migration, dry_run)
        
        logger.error(f"Migration {version} not found")
        return False
    
    def show_status(self):
        """Show migration status."""
        applied = self.get_applied_migrations()
        pending = self.list_pending_migrations()
        
        print("\n" + "=" * 60)
        print("MIGRATION STATUS")
        print("=" * 60)
        
        print(f"\nApplied ({len(applied)}):")
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT version, name, applied_at, execution_time_ms
                FROM schema_migrations
                ORDER BY version
            """)
            for row in cur.fetchall():
                print(f"  ✓ {row[0]}: {row[1]} (applied: {row[2].strftime('%Y-%m-%d %H:%M')}, {row[3]}ms)")
        
        print(f"\nPending ({len(pending)}):")
        for migration in pending:
            print(f"  ○ {migration['version']}: {migration['name']}")
        
        print("=" * 60 + "\n")
    
    def verify_schema(self) -> bool:
        """Verify database schema is correct."""
        required_tables = [
            'media_collection_queue',
            'media_news_articles',
            'media_videos',
            'media_documents',
            'media_entities',
            'media_entity_mentions',
            'schema_migrations'
        ]
        
        logger.info("Verifying schema...")
        
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            existing_tables = {row[0] for row in cur.fetchall()}
        
        missing = set(required_tables) - existing_tables
        
        if missing:
            logger.error(f"✗ Missing tables: {', '.join(missing)}")
            return False
        else:
            logger.info(f"✓ All {len(required_tables)} required tables present")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="Database Migration Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                      # Apply all pending migrations
  %(prog)s --status             # Show migration status
  %(prog)s --version 001        # Apply specific version
  %(prog)s --dry-run            # Preview changes without applying
  %(prog)s --verify             # Verify schema integrity
        """
    )
    
    parser.add_argument(
        '--database-url',
        default=DEFAULT_DATABASE_URL,
        help='PostgreSQL connection string'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show migration status'
    )
    
    parser.add_argument(
        '--version',
        help='Apply specific migration version'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying'
    )
    
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify schema integrity'
    )
    
    args = parser.parse_args()
    
    runner = MigrationRunner(args.database_url)
    
    try:
        runner.connect()
        runner.ensure_migrations_table()
        
        if args.status:
            runner.show_status()
            return 0
        
        if args.verify:
            success = runner.verify_schema()
            return 0 if success else 1
        
        if args.version:
            success = runner.apply_version(args.version, args.dry_run)
        else:
            success = runner.apply_all(args.dry_run)
        
        if success and not args.dry_run:
            runner.verify_schema()
        
        return 0 if success else 1
        
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return 1
    finally:
        runner.disconnect()


if __name__ == "__main__":
    sys.exit(main())
