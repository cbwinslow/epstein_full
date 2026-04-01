#!/usr/bin/env python3
"""
Bitwarden API Client - Direct REST API access
Bypasses CLI issues by using the Bitwarden REST API directly
"""

import requests
import json
import os
from pathlib import Path
from typing import Optional, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitwardenClient:
    """Direct Bitwarden REST API client"""
    
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.base_url = "https://api.bitwarden.com"
        self.identity_url = "https://identity.bitwarden.com"
        
        # Load credentials from environment or parameters
        self.client_id = client_id or os.environ.get('BW_CLIENTID')
        self.client_secret = client_secret or os.environ.get('BW_CLIENTSECRET')
        
        self.access_token = None
        self.session = requests.Session()
    
    def authenticate(self) -> bool:
        """Authenticate with Bitwarden API"""
        if not self.client_id or not self.client_secret:
            logger.error("BW_CLIENTID and BW_CLIENTSECRET required")
            return False
        
        url = f"{self.identity_url}/connect/token"
        
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'api'
        }
        
        try:
            response = self.session.post(url, data=data, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            
            if self.access_token:
                self.session.headers.update({
                    'Authorization': f'Bearer {self.access_token}'
                })
                logger.info("Successfully authenticated with Bitwarden")
                return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
        
        return False
    
    def list_items(self, search: str = None) -> List[Dict]:
        """List items in the vault"""
        if not self.access_token and not self.authenticate():
            return []
        
        url = f"{self.base_url}/public/items"
        
        params = {}
        if search:
            params['search'] = search
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Failed to list items: {e}")
            return []
    
    def get_item(self, item_id: str) -> Optional[Dict]:
        """Get a specific item by ID"""
        if not self.access_token and not self.authenticate():
            return None
        
        url = f"{self.base_url}/public/items/{item_id}"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get item: {e}")
            return None
    
    def get_secret_by_name(self, name: str, field: str = 'password') -> Optional[str]:
        """Get a secret value by item name"""
        items = self.list_items(search=name)
        
        for item in items:
            if item.get('name') == name:
                login = item.get('login', {})
                
                if field == 'password':
                    return login.get('password')
                elif field == 'username':
                    return login.get('username')
                elif field == 'notes':
                    return item.get('notes')
                elif field.startswith('custom:'):
                    # Custom field
                    field_name = field.replace('custom:', '')
                    for f in item.get('fields', []):
                        if f.get('name') == field_name:
                            return f.get('value')
                
                return login.get('password')  # Default
        
        return None


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Bitwarden API Client')
    parser.add_argument('--client-id', help='Bitwarden Client ID')
    parser.add_argument('--client-secret', help='Bitwarden Client Secret')
    parser.add_argument('--list', action='store_true', help='List items')
    parser.add_argument('--search', help='Search query')
    parser.add_argument('--get', help='Get item by name')
    parser.add_argument('--field', default='password', help='Field to retrieve')
    
    args = parser.parse_args()
    
    # Use credentials from args or environment
    client = BitwardenClient(
        client_id=args.client_id,
        client_secret=args.client_secret
    )
    
    if not client.authenticate():
        print("Authentication failed. Check BW_CLIENTID and BW_CLIENTSECRET.")
        return 1
    
    if args.list or args.search:
        items = client.list_items(search=args.search)
        for item in items:
            print(f"- {item.get('name')} ({item.get('id')})")
    
    if args.get:
        value = client.get_secret_by_name(args.get, args.field)
        if value:
            print(value)
        else:
            print(f"Secret not found: {args.get}")
            return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
