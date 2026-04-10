"""
Document Discovery Agent
Discovers Epstein-related documents from CourtListener and GovInfo.
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests

# Import base classes
import sys
sys.path.insert(0, '/home/cbwinslow/workspace/epstein')
from media_acquisition.base import (
    DiscoveryAgent, AgentConfig, TaskResult,
    DocumentMetadata, MediaURL
)

logger = logging.getLogger(__name__)


class CourtListenerClient:
    """Client for CourtListener (Free.law) API."""
    
    BASE_URL = "https://www.courtlistener.com/api/rest/v3"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'Authorization': f'Token {api_key}'})
    
    def search_cases(self,
                    query: str,
                    date_filed_after: Optional[str] = None,
                    date_filed_before: Optional[str] = None,
                    court: Optional[str] = None,
                    max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Search for cases on CourtListener.
        
        Args:
            query: Search query
            date_filed_after: 'YYYY-MM-DD'
            date_filed_before: 'YYYY-MM-DD'
            court: Court ID (e.g., 'scotus', 'ca2')
            max_results: Maximum results (max 100 per request)
            
        Returns:
            List of case dictionaries
        """
        url = f"{self.BASE_URL}/opinions/"
        
        params = {
            'q': query,
            'order_by': 'dateFiled desc',
            'page_size': min(max_results, 100)
        }
        
        if date_filed_after:
            params['filed_after'] = date_filed_after
        if date_filed_before:
            params['filed_before'] = date_filed_before
        if court:
            params['court'] = court
        
        cases = []
        
        try:
            while len(cases) < max_results:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for result in data.get('results', []):
                    cases.append({
                        'id': result.get('id'),
                        'title': result.get('caseName'),
                        'docket_number': result.get('docketNumber'),
                        'court': result.get('court'),
                        'date_filed': result.get('dateFiled'),
                        'download_url': result.get('download_url'),
                        'absolute_url': f"https://www.courtlistener.com{result.get('absolute_url', '')}",
                        'snippet': result.get('snippet', '')
                    })
                
                # Pagination
                next_url = data.get('next')
                if not next_url or len(cases) >= max_results:
                    break
                    
                url = next_url
                time.sleep(0.5)  # Rate limiting
                
        except Exception as e:
            logger.error(f"CourtListener search failed: {e}")
            
        return cases[:max_results]
    
    def search_dockets(self,
                      query: str,
                      date_filed_after: Optional[str] = None,
                      date_filed_before: Optional[str] = None,
                      max_results: int = 100) -> List[Dict[str, Any]]:
        """Search for dockets."""
        url = f"{self.BASE_URL}/dockets/"
        
        params = {
            'q': query,
            'order_by': '-date_last_filing',
            'page_size': min(max_results, 100)
        }
        
        if date_filed_after:
            params['date_filed__gte'] = date_filed_after
        if date_filed_before:
            params['date_filed__lte'] = date_filed_before
        
        dockets = []
        
        try:
            while len(dockets) < max_results:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for result in data.get('results', []):
                    dockets.append({
                        'id': result.get('id'),
                        'case_name': result.get('case_name'),
                        'docket_number': result.get('docket_number'),
                        'court': result.get('court'),
                        'date_filed': result.get('date_filed'),
                        'date_last_filing': result.get('date_last_filing'),
                        'absolute_url': f"https://www.courtlistener.com{result.get('absolute_url', '')}",
                        'pacer_case_id': result.get('pacer_case_id')
                    })
                
                next_url = data.get('next')
                if not next_url or len(dockets) >= max_results:
                    break
                    
                url = next_url
                time.sleep(0.5)
                
        except Exception as e:
            logger.error(f"CourtListener docket search failed: {e}")
            
        return dockets[:max_results]
    
    def get_document_content(self, opinion_id: int) -> Optional[str]:
        """Get the text content of an opinion."""
        url = f"{self.BASE_URL}/opinions/{opinion_id}/"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # Plain text is usually available
            return data.get('plain_text') or data.get('html')
            
        except Exception as e:
            logger.error(f"Failed to get document content: {e}")
            return None


class GovInfoClient:
    """Client for GovInfo.gov API."""
    
    BASE_URL = "https://api.govinfo.gov"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({'X-Api-Key': api_key})
    
    def search_collections(self,
                          query: str,
                      date_start: Optional[str] = None,
                          date_end: Optional[str] = None,
                          max_results: int = 100) -> List[Dict[str, Any]]:
        """
        Search GovInfo collections.
        
        Args:
            query: Search query
            date_start: 'YYYY-MM-DD'
            date_end: 'YYYY-MM-DD'
            max_results: Maximum results
            
        Returns:
            List of document dictionaries
        """
        url = f"{self.BASE_URL}/search"
        
        params = {
            'query': query,
            'pageSize': min(max_results, 100)
        }
        
        if date_start:
            params['startDate'] = date_start
        if date_end:
            params['endDate'] = date_end
        
        documents = []
        
        try:
            offset = 0
            while len(documents) < max_results:
                params['offset'] = offset
                
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                for result in data.get('results', []):
                    documents.append({
                        'package_id': result.get('packageId'),
                        'title': result.get('title'),
                        'collection': result.get('collectionCode'),
                        'date_issued': result.get('dateIssued'),
                        'download_url': result.get('download',
                            f"{self.BASE_URL}/packages/{result.get('packageId')}/summary"),
                        'last_modified': result.get('lastModified')
                    })
                
                if len(data.get('results', [])) == 0:
                    break
                    
                offset += len(data.get('results', []))
                time.sleep(0.5)
                
        except Exception as e:
            logger.error(f"GovInfo search failed: {e}")
            
        return documents[:max_results]
    
    def get_package_content(self, package_id: str) -> Optional[Dict[str, Any]]:
        """Get package content details."""
        url = f"{self.BASE_URL}/packages/{package_id}/summary"
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Failed to get package content: {e}")
            return None


class DocumentDiscoveryAgent(DiscoveryAgent):
    """
    Agent for discovering Epstein-related court documents and government releases.
    
    Sources:
    1. CourtListener (Free.law) - Free, no API key needed for basic use
    2. GovInfo.gov - Free tier available
    
    Document types:
    - Court opinions
    - Dockets
    - Filings
    - Government releases
    - Congressional records
    """
    
    AGENT_ID = 'document-discovery-v2'
    VERSION = '2.0.0'
    
    DEFAULT_KEYWORDS = [
        'Epstein',
        'Jeffrey Epstein',
        'Ghislaine Maxwell',
        'Virginia Giuffre',
        'John Doe',
        'Jane Doe',
        'Epstein v.',
        'United States v. Maxwell',
        'Epstein sex trafficking',
        'Epstein prosecution',
        'Epstein investigation'
    ]
    
    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(config)
        
        # Initialize clients
        self.courtlistener = CourtListenerClient(
            api_key=getattr(config, 'courtlistener_api_key', None)
        )
        self.govinfo = GovInfoClient(
            api_key=getattr(config, 'govinfo_api_key', None)
        )
        
    def _validate_config(self):
        """Validate agent configuration."""
        pass  # API keys are optional
    
    def _initialize_resources(self):
        """Initialize resources."""
        logger.info("DocumentDiscoveryAgent initialized")
    
    async def search(self,
                    keywords: List[str] = None,
                    date_range: Tuple[str, str] = None,
                    sources: List[str] = None,
                    max_results: int = 500,
                    **kwargs) -> List[DocumentMetadata]:
        """
        Search for documents across sources.
        
        Args:
            keywords: Search terms
            date_range: (start_date, end_date) as 'YYYY-MM-DD'
            sources: ['courtlistener', 'govinfo'] or None for both
            max_results: Maximum documents to discover
            
        Returns:
            List of DocumentMetadata objects
        """
        keywords = keywords or self.DEFAULT_KEYWORDS
        date_range = date_range or ('1990-01-01', '2025-12-31')
        sources = sources or ['courtlistener', 'govinfo']
        
        all_documents = []
        
        # Search CourtListener
        if 'courtlistener' in sources:
            logger.info("Searching CourtListener...")
            try:
                cl_results = await self._search_courtlistener(
                    keywords, date_range, max_results
                )
                all_documents.extend(cl_results)
                logger.info(f"CourtListener: Found {len(cl_results)} documents")
            except Exception as e:
                logger.error(f"CourtListener search failed: {e}")
        
        # Search GovInfo
        if 'govinfo' in sources:
            logger.info("Searching GovInfo...")
            try:
                gov_results = await self._search_govinfo(
                    keywords, date_range, max_results
                )
                all_documents.extend(gov_results)
                logger.info(f"GovInfo: Found {len(gov_results)} documents")
            except Exception as e:
                logger.error(f"GovInfo search failed: {e}")
        
        # Deduplicate
        deduplicated = self._deduplicate_documents(all_documents)
        
        # Update metrics
        self.metrics['total_discovered'] = len(all_documents)
        self.metrics['unique_documents'] = len(deduplicated)
        self.metrics['sources_breakdown'] = {
            'courtlistener': len([d for d in all_documents if d.source == 'court_listener']),
            'govinfo': len([d for d in all_documents if d.source == 'govinfo'])
        }
        
        return deduplicated
    
    async def _search_courtlistener(self,
                                   keywords: List[str],
                                   date_range: Tuple[str, str],
                                   max_results: int) -> List[DocumentMetadata]:
        """Search CourtListener for documents."""
        loop = asyncio.get_event_loop()
        
        all_results = []
        
        # Search primary keywords
        for keyword in keywords[:5]:  # Limit to avoid rate limiting
            try:
                # Search opinions
                results = await loop.run_in_executor(
                    None,
                    lambda: self.courtlistener.search_cases(
                        query=keyword,
                        date_filed_after=date_range[0],
                        date_filed_before=date_range[1],
                        max_results=20
                    )
                )
                
                for result in results:
                    doc = DocumentMetadata(
                        url=result['download_url'] or result['absolute_url'],
                        title=result['title'],
                        source='court_listener',
                        document_type='opinion',
                        docket_number=result['docket_number'],
                        filing_date=result['date_filed'],
                        priority=1,
                        discovery_method='courtlistener_api',
                        metadata={
                            'court': result.get('court'),
                            'snippet': result.get('snippet')
                        }
                    )
                    all_results.append(doc)
                
                # Search dockets
                dockets = await loop.run_in_executor(
                    None,
                    lambda: self.courtlistener.search_dockets(
                        query=keyword,
                        date_filed_after=date_range[0],
                        date_filed_before=date_range[1],
                        max_results=20
                    )
                )
                
                for docket in dockets:
                    doc = DocumentMetadata(
                        url=docket['absolute_url'],
                        title=docket['case_name'],
                        source='court_listener',
                        document_type='docket',
                        docket_number=docket['docket_number'],
                        filing_date=docket['date_filed'],
                        priority=2,  # Lower priority than opinions
                        discovery_method='courtlistener_api',
                        metadata={
                            'court': docket.get('court'),
                            'pacer_case_id': docket.get('pacer_case_id')
                        }
                    )
                    all_results.append(doc)
                
                await asyncio.sleep(0.5)  # Rate limiting
                
            except Exception as e:
                logger.warning(f"CourtListener search failed for '{keyword}': {e}")
        
        return all_results
    
    async def _search_govinfo(self,
                             keywords: List[str],
                             date_range: Tuple[str, str],
                             max_results: int) -> List[DocumentMetadata]:
        """Search GovInfo for documents."""
        loop = asyncio.get_event_loop()
        
        all_results = []
        
        # Search primary keywords
        for keyword in keywords[:3]:  # Limit for rate limiting
            try:
                results = await loop.run_in_executor(
                    None,
                    lambda: self.govinfo.search_collections(
                        query=keyword,
                        date_start=date_range[0],
                        date_end=date_range[1],
                        max_results=30
                    )
                )
                
                for result in results:
                    doc = DocumentMetadata(
                        url=result['download_url'],
                        title=result['title'],
                        source='govinfo',
                        document_type='government_document',
                        filing_date=result['date_issued'],
                        priority=2,
                        discovery_method='govinfo_api',
                        metadata={
                            'package_id': result['package_id'],
                            'collection': result['collection'],
                            'last_modified': result['last_modified']
                        }
                    )
                    all_results.append(doc)
                
                await asyncio.sleep(0.5)
                
            except Exception as e:
                logger.warning(f"GovInfo search failed for '{keyword}': {e}")
        
        return all_results
    
    def _deduplicate_documents(self, documents: List[DocumentMetadata]) -> List[DocumentMetadata]:
        """Remove duplicate documents by URL."""
        seen = set()
        unique = []
        
        for doc in documents:
            # Normalize URL
            url = doc.url.lower().rstrip('/') if doc.url else ''
            
            if url and url not in seen:
                seen.add(url)
                unique.append(doc)
            elif not url:
                # Keep documents without URLs but with docket numbers
                unique.append(doc)
        
        return unique
    
    async def execute(self, task: Dict[str, Any]) -> TaskResult:
        """Execute discovery task."""
        keywords = task.get("keywords", self.DEFAULT_KEYWORDS)
        date_range = task.get("date_range", ('1990-01-01', '2025-12-31'))
        sources = task.get("sources", ['courtlistener', 'govinfo'])
        max_results = task.get("max_results", 500)
        
        try:
            results = await self.search(
                keywords=keywords,
                date_range=date_range,
                sources=sources,
                max_results=max_results
            )
            
            return TaskResult(
                status="success",
                output=results,
                metrics=self.metrics
            )
            
        except Exception as e:
            return TaskResult(
                status="failure",
                error=str(e),
                retry_allowed=self._should_retry(e)
            )


# CLI interface for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Document Discovery Agent')
    parser.add_argument('--keywords', nargs='+', default=['Epstein'])
    parser.add_argument('--start-date', default='2020-01-01')
    parser.add_argument('--end-date', default='2025-12-31')
    parser.add_argument('--max-results', type=int, default=100)
    parser.add_argument('--sources', nargs='+', default=['courtlistener', 'govinfo'])
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Create agent
    agent = DocumentDiscoveryAgent()
    
    # Run discovery
    async def main():
        results = await agent.search(
            keywords=args.keywords,
            date_range=(args.start_date, args.end_date),
            max_results=args.max_results,
            sources=args.sources
        )
        
        print(f"\nDiscovered {len(results)} documents:")
        for i, doc in enumerate(results[:10], 1):
            print(f"{i}. {doc.title or 'N/A'}")
            print(f"   Source: {doc.source}")
            print(f"   Type: {doc.document_type}")
            print(f"   Date: {doc.filing_date}")
            print(f"   URL: {doc.url}")
            print()
    
    asyncio.run(main())
