#!/usr/bin/env python3
"""
Import Black Book from dleerdefi/epstein-network-data

Source: /home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/black_book/processed/complete.json
"""

import asyncio
import asyncpg
import json
from pathlib import Path
from datetime import datetime

JSON_FILE = Path("/home/cbwinslow/workspace/epstein-data/external_repos/epstein-network-data/data/external_sources/black_book/processed/complete.json")
BATCH_SIZE = 500
DB_URL = "postgresql://cbwinslow:123qweasd@localhost:5432/epstein"

async def create_tables(conn):
    """Create tables for Black Book data."""
    print("Creating tables...")
    
    # Drop existing tables to ensure clean state
    await conn.execute("DROP TABLE IF EXISTS black_book_phones CASCADE")
    await conn.execute("DROP TABLE IF EXISTS black_book_emails CASCADE")
    await conn.execute("DROP TABLE IF EXISTS black_book_addresses CASCADE")
    await conn.execute("DROP TABLE IF EXISTS black_book_contacts CASCADE")
    
    # Main contacts table
    await conn.execute("""
        CREATE TABLE black_book_contacts (
            id SERIAL PRIMARY KEY,
            entry_id TEXT,
            full_name TEXT,
            first_name TEXT,
            last_name TEXT,
            prefix TEXT,
            suffix TEXT,
            couple BOOLEAN,
            partner_name TEXT,
            page_number INTEGER,
            alphabetical_section TEXT,
            overall_legibility TEXT,
            formatting_notes TEXT,
            imported_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    
    # Phone numbers table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS black_book_phones (
            id SERIAL PRIMARY KEY,
            contact_entry_id TEXT,
            phone_type TEXT,
            number TEXT,
            formatting TEXT
        )
    """)
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_phones_entry_id ON black_book_phones(contact_entry_id)")
    
    # Emails table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS black_book_emails (
            id SERIAL PRIMARY KEY,
            contact_entry_id TEXT,
            email TEXT
        )
    """)
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_emails_entry_id ON black_book_emails(contact_entry_id)")
    
    # Addresses table
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS black_book_addresses (
            id SERIAL PRIMARY KEY,
            contact_entry_id TEXT,
            address TEXT
        )
    """)
    await conn.execute("CREATE INDEX IF NOT EXISTS idx_addresses_entry_id ON black_book_addresses(contact_entry_id)")
    
    print("✅ Tables created")

async def import_data(conn):
    """Import Black Book JSON data."""
    print(f"Importing from {JSON_FILE}...")
    
    with open(JSON_FILE, 'r') as f:
        data = json.load(f)
    
    metadata = data.get('metadata', {})
    pages = data.get('pages', {})
    
    print(f"Metadata: {metadata}")
    print(f"Pages: {len(pages)}")
    
    contacts_batch = []
    phones_batch = []
    emails_batch = []
    addresses_batch = []
    
    total_contacts = 0
    
    for page_num, page_data in pages.items():
        contacts = page_data.get('contacts', [])
        
        for contact in contacts:
            entry_id = contact.get('entry_id')
            name = contact.get('name', {})
            confidence = contact.get('confidence', {})
            
            # Main contact data
            contacts_batch.append((
                entry_id,
                name.get('full_name'),
                name.get('first_name'),
                name.get('last_name'),
                name.get('prefix'),
                name.get('suffix'),
                name.get('couple', False),
                name.get('partner_name'),
                page_data.get('page_number'),
                page_data.get('alphabetical_section'),
                confidence.get('overall_legibility'),
                contact.get('formatting_notes')
            ))
            
            # Phone numbers
            for phone in contact.get('phones', []):
                phones_batch.append((
                    entry_id,
                    phone.get('type'),
                    phone.get('number'),
                    phone.get('formatting')
                ))
            
            # Emails - handle both string and dict formats
            for email in contact.get('emails', []):
                if isinstance(email, dict):
                    email_str = email.get('address') or email.get('email') or str(email)
                else:
                    email_str = str(email)
                emails_batch.append((entry_id, email_str))
            
            # Addresses - handle both string and dict formats
            for address in contact.get('addresses', []):
                if isinstance(address, dict):
                    # Build address string from components
                    parts = []
                    if address.get('street'): parts.append(address.get('street'))
                    if address.get('city'): parts.append(address.get('city'))
                    if address.get('state'): parts.append(address.get('state'))
                    if address.get('zip'): parts.append(address.get('zip'))
                    if address.get('country'): parts.append(address.get('country'))
                    address_str = ', '.join(parts) if parts else str(address)
                else:
                    address_str = str(address)
                addresses_batch.append((entry_id, address_str))
            
            total_contacts += 1
            
            if len(contacts_batch) >= BATCH_SIZE:
                await conn.copy_records_to_table(
                    'black_book_contacts',
                    records=contacts_batch,
                    columns=['entry_id', 'full_name', 'first_name', 'last_name', 
                            'prefix', 'suffix', 'couple', 'partner_name',
                            'page_number', 'alphabetical_section', 'overall_legibility', 'formatting_notes']
                )
                
                if phones_batch:
                    await conn.copy_records_to_table(
                        'black_book_phones',
                        records=phones_batch,
                        columns=['contact_entry_id', 'phone_type', 'number', 'formatting']
                    )
                
                if emails_batch:
                    await conn.copy_records_to_table(
                        'black_book_emails',
                        records=emails_batch,
                        columns=['contact_entry_id', 'email']
                    )
                
                if addresses_batch:
                    await conn.copy_records_to_table(
                        'black_book_addresses',
                        records=addresses_batch,
                        columns=['contact_entry_id', 'address']
                    )
                
                print(f"   Imported {total_contacts} contacts...")
                contacts_batch = []
                phones_batch = []
                emails_batch = []
                addresses_batch = []
    
    # Insert remaining
    if contacts_batch:
        await conn.copy_records_to_table(
            'black_book_contacts',
            records=contacts_batch,
            columns=['entry_id', 'full_name', 'first_name', 'last_name',
                    'prefix', 'suffix', 'couple', 'partner_name',
                    'page_number', 'alphabetical_section', 'overall_legibility', 'formatting_notes']
        )
    
    if phones_batch:
        await conn.copy_records_to_table(
            'black_book_phones',
            records=phones_batch,
            columns=['contact_entry_id', 'phone_type', 'number', 'formatting']
        )
    
    if emails_batch:
        await conn.copy_records_to_table(
            'black_book_emails',
            records=emails_batch,
            columns=['contact_entry_id', 'email']
        )
    
    if addresses_batch:
        await conn.copy_records_to_table(
            'black_book_addresses',
            records=addresses_batch,
            columns=['contact_entry_id', 'address']
        )
    
    print(f"✅ Import complete: {total_contacts} contacts")
    return total_contacts

async def verify(conn):
    """Verify import."""
    print("\nVerification:")
    
    contacts = await conn.fetchval("SELECT COUNT(*) FROM black_book_contacts")
    phones = await conn.fetchval("SELECT COUNT(*) FROM black_book_phones")
    emails = await conn.fetchval("SELECT COUNT(*) FROM black_book_emails")
    addresses = await conn.fetchval("SELECT COUNT(*) FROM black_book_addresses")
    
    print(f"Contacts: {contacts}")
    print(f"Phone numbers: {phones}")
    print(f"Emails: {emails}")
    print(f"Addresses: {addresses}")
    
    # Sample
    samples = await conn.fetch("""
        SELECT c.full_name, c.alphabetical_section, c.page_number,
               array_agg(DISTINCT p.number) as phones
        FROM black_book_contacts c
        LEFT JOIN black_book_phones p ON c.entry_id = p.contact_entry_id
        WHERE c.full_name IS NOT NULL
        GROUP BY c.id, c.full_name, c.alphabetical_section, c.page_number
        LIMIT 5
    """)
    
    print("\nSample contacts:")
    for s in samples:
        print(f"   - {s['full_name']} (Section {s['alphabetical_section']}, Page {s['page_number']})")

async def main():
    print("="*70)
    print("BLACK BOOK JSON IMPORT")
    print("="*70)
    print(f"Started: {datetime.now()}")
    print(f"Source: {JSON_FILE}")
    print("="*70)
    
    conn = await asyncpg.connect(DB_URL)
    try:
        await create_tables(conn)
        imported = await import_data(conn)
        await verify(conn)
        print("\n" + "="*70)
        print(f"✅ COMPLETE - {imported} contacts imported")
        print("="*70)
    finally:
        await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
