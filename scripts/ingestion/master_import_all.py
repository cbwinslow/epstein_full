#!/usr/bin/env python3
"""
Epstein Data Ingestion - Master Orchestration Script

Coordinates all data ingestion processes across multiple sources.
Handles dependencies, progress tracking, and error recovery.
"""

import argparse
import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add scripts directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.utils.epstein_config import DATA_ROOT, ensure_dirs
from scripts.utils.tracker import register_task, update_task, done_task

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class IngestionOrchestrator:
    """Master orchestration for Epstein data ingestion."""
    
    def __init__(self):
        self.sources = {
            'doj': {
                'download': 'download/doj_epstein_library.py',
                'import': 'import/doj_epstein_library.py',
                'status': 'pending',
                'priority': 1
            },
            'jmail': {
                'download': 'download/jmail_world.py',
                'import': 'import/jmail_world.py',
                'status': 'pending',
                'priority': 2
            },
            'gdelt': {
                'download': 'download/gdelt_news.py',
                'import': 'import/gdelt_news.py',
                'status': 'pending',
                'priority': 3
            },
            'icij': {
                'download': 'download/icij_offshore_leaks.py',
                'import': 'import/icij_offshore_leaks.py',
                'status': 'pending',
                'priority': 4
            },
            'hf': {
                'download': 'download/huggingface_datasets.py',
                'import': 'import/huggingface_datasets.py',
                'status': 'pending',
                'priority': 5
            },
            'third_party': {
                'download': 'download/third_party_repos.py',
                'import': 'import/third_party_repos.py',
                'status': 'pending',
                'priority': 6
            }
        }
    
    async def run_source(self, source_name: str, force: bool = False) -> bool:
        """Run ingestion for a specific source."""
        source = self.sources.get(source_name)
        if not source:
            logger.error(f"Unknown source: {source_name}")
            return False
        
        logger.info(f"Starting ingestion for source: {source_name}")
        
        # Register task
        task_id = f"ingest-{source_name}"
        register_task(task_id, f"Ingest {source_name}", expected=100)
        
        try:
            # Download phase
            if force or source['status'] == 'pending':
                logger.info(f"Running download for {source_name}")
                download_cmd = f"python3 {source['download']}"
                if os.system(download_cmd) != 0:
                    logger.error(f"Download failed for {source_name}")
                    update_task(task_id, 50)
                    return False
                
                update_task(task_id, 30)
            
            # Import phase
            logger.info(f"Running import for {source_name}")
            import_cmd = f"python3 {source['import']}"
            if os.system(import_cmd) != 0:
                logger.error(f"Import failed for {source_name}")
                update_task(task_id, 80)
                return False
            
            update_task(task_id, 100)
            done_task(task_id, "completed")
            
            logger.info(f"Successfully completed ingestion for {source_name}")
            self.sources[source_name]['status'] = 'completed'
            return True
            
        except Exception as e:
            logger.error(f"Error during {source_name} ingestion: {e}")
            done_task(task_id, "failed")
            return False
    
    async def run_all(self, force: bool = False) -> Dict[str, bool]:
        """Run ingestion for all sources."""
        results = {}
        
        # Sort sources by priority
        sorted_sources = sorted(
            self.sources.items(), 
            key=lambda x: x[1]['priority']
        )
        
        for source_name, source in sorted_sources:
            result = await self.run_source(source_name, force)
            results[source_name] = result
        
        return results
    
    async def run_dependencies(self, source_name: str) -> bool:
        """Run dependency sources before main source."""
        # Define dependencies
        dependencies = {
            'hf': ['doj', 'jmail'],
            'third_party': ['doj', 'jmail', 'icij']
        }
        
        deps = dependencies.get(source_name, [])
        if not deps:
            return True
        
        logger.info(f"Running dependencies for {source_name}: {deps}")
        
        for dep in deps:
            if self.sources[dep]['status'] != 'completed':
                result = await self.run_source(dep)
                if not result:
                    logger.error(f"Dependency {dep} failed for {source_name}")
                    return False
        
        return True

async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Epstein Data Ingestion Orchestrator")
    parser.add_argument("--source", "-s", type=str, help="Specific source to ingest")
    parser.add_argument("--force", "-f", action="store_true", help="Force re-ingestion")
    parser.add_argument("--all", "-a", action="store_true", help="Ingest all sources")
    parser.add_argument("--status", action="store_true", help="Show ingestion status")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_dirs()
    
    orchestrator = IngestionOrchestrator()
    
    if args.status:
        print("Current Ingestion Status:")
        for source, info in orchestrator.sources.items():
            print(f"  {source}: {info['status']}")
        return
    
    if args.source:
        await orchestrator.run_source(args.source, args.force)
    elif args.all:
        results = await orchestrator.run_all(args.force)
        print("Ingestion Results:")
        for source, success in results.items():
            status = "✅ Completed" if success else "❌ Failed"
            print(f"  {source}: {status}")
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())
