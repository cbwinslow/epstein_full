#!/usr/bin/env python3
"""
PostgreSQL Setup and Schema Application
Handles authentication and schema setup programmatically
"""

import os
import sys
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "cbwinslow",
    "password": "123qweasd"
}

ADMIN_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres"
}

def run_as_postgres(cmd):
    """Run command as postgres user"""
    full_cmd = ['sudo', '-u', 'postgres'] + cmd
    result = subprocess.run(full_cmd, capture_output=True, text=True)
    return result

def setup_trust_authentication():
    """Configure PostgreSQL for trust authentication"""
    print("Setting up PostgreSQL trust authentication...")
    
    # Find pg_hba.conf
    find_result = run_as_postgres(['psql', '-c', 'SHOW hba_file;'])
    pg_hba = find_result.stdout.strip().split('\n')[0] if find_result.returncode == 0 else None
    
    if not pg_hba:
        # Try common locations
        for path in ['/etc/postgresql/16/main/pg_hba.conf', 
                     '/etc/postgresql/14/main/pg_hba.conf',
                     '/var/lib/pgsql/data/pg_hba.conf']:
            if os.path.exists(path):
                pg_hba = path
                break
    
    if not pg_hba:
        print("ERROR: Could not find pg_hba.conf")
        return False
    
    print(f"Found: {pg_hba}")
    
    # Backup current config
    run_as_postgres(['cp', pg_hba, f"{pg_hba}.backup"])
    
    # Create trust authentication config
    trust_config = """# Trust authentication for epstein project
local   all             postgres                                trust
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
"""
    
    # Write new config
    with open('/tmp/pg_hba_new.conf', 'w') as f:
        f.write(trust_config)
    
    # Copy to PostgreSQL location
    run_as_postgres(['cp', '/tmp/pg_hba_new.conf', pg_hba])
    
    # Reload PostgreSQL
    reload_result = subprocess.run(['sudo', 'systemctl', 'reload', 'postgresql'], 
                                  capture_output=True, text=True)
    
    if reload_result.returncode != 0:
        # Try alternative reload method
        subprocess.run(['sudo', '-u', 'postgres', 'pg_ctl', 'reload'], 
                      capture_output=True, text=True)
    
    print("✓ PostgreSQL reconfigured for trust authentication")
    return True

def create_database_and_user():
    """Create the epstein database and cbwinslow user"""
    print("\nCreating database and user...")
    
    try:
        # Connect as postgres
        conn = psycopg2.connect(**ADMIN_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT 1 FROM pg_roles WHERE rolname='cbwinslow';")
        if not cursor.fetchone():
            cursor.execute("CREATE USER cbwinslow WITH PASSWORD '123qweasd' SUPERUSER;")
            print("✓ Created user cbwinslow")
        else:
            print("✓ User cbwinslow already exists")
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='epstein';")
        if not cursor.fetchone():
            cursor.execute("CREATE DATABASE epstein OWNER cbwinslow;")
            print("✓ Created database epstein")
        else:
            print("✓ Database epstein already exists")
            # Ensure correct ownership
            cursor.execute("ALTER DATABASE epstein OWNER TO cbwinslow;")
        
        # Grant privileges
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE epstein TO cbwinslow;")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def apply_schema():
    """Apply the database schema"""
    print("\nApplying database schema...")
    
    schema_file = "/home/cbwinslow/workspace/epstein/migrations/003_full_schema.sql"
    
    if not os.path.exists(schema_file):
        print(f"ERROR: Schema file not found: {schema_file}")
        return False
    
    try:
        # Connect to epstein database
        config = DB_CONFIG.copy()
        config['dbname'] = 'epstein'
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Read and execute schema
        with open(schema_file, 'r') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        
        # Verify tables were created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"✓ Schema applied successfully")
        print(f"✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR applying schema: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_setup():
    """Verify the PostgreSQL setup"""
    print("\nVerifying PostgreSQL setup...")
    
    try:
        config = DB_CONFIG.copy()
        config['dbname'] = 'epstein'
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Get table counts
        cursor.execute("""
            SELECT table_name, 
                   (SELECT COUNT(*) FROM information_schema.columns 
                    WHERE table_name = t.table_name AND table_schema = 'public') as column_count
            FROM information_schema.tables t
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        print("\nTable Status:")
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]} columns")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("="*80)
    print("POSTGRESQL SETUP AND INITIALIZATION")
    print("="*80)
    
    # Step 1: Configure authentication
    if not setup_trust_authentication():
        print("WARNING: Could not reconfigure authentication, continuing anyway...")
    
    # Step 2: Create database and user
    if not create_database_and_user():
        print("ERROR: Failed to create database/user")
        return False
    
    # Step 3: Apply schema
    if not apply_schema():
        print("ERROR: Failed to apply schema")
        return False
    
    # Step 4: Verify
    if not verify_setup():
        print("ERROR: Verification failed")
        return False
    
    print("\n" + "="*80)
    print("POSTGRESQL SETUP COMPLETE")
    print("="*80)
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
