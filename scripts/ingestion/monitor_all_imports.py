#!/usr/bin/env python3
"""
Monitor all data ingestion processes
Reports completion status and progress
April 13, 2026
"""

import json
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

BASE_DIR = Path("/home/cbwinslow/workspace/epstein")
LOG_DIR = BASE_DIR / "logs/ingestion"
RAW_DIR = Path("/home/cbwinslow/workspace/epstein-data/raw-files")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ImportMonitor:
    def __init__(self):
        self.datasets = {
            'whitehouse': {'name': 'White House Visitors', 'files': '*.csv'},
            'sec_edgar': {'name': 'SEC EDGAR', 'files': '*.xml'},
            'usa_spending': {'name': 'USA Spending', 'files': '*.json'},
            'congress': {'name': 'Congress.gov', 'files': '*.json'},
            'govinfo': {'name': 'GovInfo', 'files': '*.json'},
            'fara': {'name': 'FARA', 'files': '*.xml'},
            'lobbying': {'name': 'Lobbying Disclosure', 'files': '*.xml'},
        }
        self.start_time = datetime.now()
        
    def check_processes(self) -> Dict[str, bool]:
        """Check which import/download processes are running"""
        result = subprocess.run(['pgrep', '-f', 'python'], capture_output=True, text=True)
        pids = result.stdout.strip().split('\n') if result.stdout else []
        
        running = {
            'govinfo_bulk': False,
            'master_import': False,
            'whitehouse_import': False,
            'sec_import': False,
            'usa_spending_import': False,
            'congress_import': False,
            'govinfo_import': False,
        }
        
        for pid in pids:
            if not pid:
                continue
            try:
                cmd = subprocess.run(['ps', '-p', pid, '-o', 'comm,args'], 
                                   capture_output=True, text=True)
                cmdline = cmd.stdout.lower()
                if 'govinfo_bulk' in cmdline:
                    running['govinfo_bulk'] = True
                elif 'master_import' in cmdline:
                    running['master_import'] = True
                elif 'import_whitehouse' in cmdline:
                    running['whitehouse_import'] = True
                elif 'import_sec_edgar' in cmdline:
                    running['sec_import'] = True
                elif 'import_usa_spending' in cmdline:
                    running['usa_spending_import'] = True
                elif 'import_congress' in cmdline:
                    running['congress_import'] = True
                elif 'import_govinfo' in cmdline:
                    running['govinfo_import'] = True
            except:
                pass
        
        return running
    
    def count_files(self, dataset: str) -> int:
        """Count files in dataset directory"""
        dataset_dir = RAW_DIR / dataset
        if not dataset_dir.exists():
            return 0
        
        pattern = self.datasets.get(dataset, {}).get('files', '*')
        return len(list(dataset_dir.rglob(pattern)))
    
    def get_directory_size(self, dataset: str) -> str:
        """Get human-readable size of dataset directory"""
        dataset_dir = RAW_DIR / dataset
        if not dataset_dir.exists():
            return "0 B"
        
        try:
            result = subprocess.run(
                ['du', '-sh', str(dataset_dir)],
                capture_output=True, text=True
            )
            return result.stdout.split()[0] if result.stdout else "0 B"
        except:
            return "?"
    
    def check_log_progress(self) -> Dict[str, str]:
        """Check latest log files for progress indicators"""
        progress = {}
        
        for log_file in sorted(LOG_DIR.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    # Get last few lines
                    last_lines = lines[-10:] if len(lines) > 10 else lines
                    progress[log_file.name] = ''.join(last_lines[-3:]) if last_lines else "No content"
            except:
                pass
        
        return progress
    
    def generate_report(self) -> Dict:
        """Generate comprehensive status report"""
        running = self.check_processes()
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'elapsed_time': str(datetime.now() - self.start_time),
            'processes': {
                'govinfo_bulk_download': 'RUNNING' if running.get('govinfo_bulk') else 'NOT RUNNING',
                'master_import': 'RUNNING' if running.get('master_import') else 'NOT RUNNING',
            },
            'datasets': {},
            'total_files': 0,
            'total_size': 0,
        }
        
        for dataset_id, config in self.datasets.items():
            file_count = self.count_files(dataset_id)
            size = self.get_directory_size(dataset_id)
            
            report['datasets'][dataset_id] = {
                'name': config['name'],
                'files': file_count,
                'size': size,
            }
            report['total_files'] += file_count
        
        return report
    
    def print_report(self, report: Dict):
        """Print formatted report to console"""
        print("\n" + "=" * 80)
        print("DATA INGESTION MONITOR REPORT")
        print("=" * 80)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Elapsed: {report['elapsed_time']}")
        print("=" * 80)
        
        print("\n📊 ACTIVE PROCESSES:")
        for proc, status in report['processes'].items():
            icon = "🔄" if status == "RUNNING" else "⏹️"
            print(f"  {icon} {proc}: {status}")
        
        print("\n📁 DATASET STATUS:")
        for dataset_id, info in report['datasets'].items():
            icon = "✅" if info['files'] > 0 else "⏳"
            print(f"  {icon} {info['name']}: {info['files']} files ({info['size']})")
        
        print(f"\n📈 TOTAL FILES: {report['total_files']}")
        print("=" * 80)
    
    def save_report(self, report: Dict):
        """Save report to JSON file"""
        report_file = LOG_DIR / f"monitor_report_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        return report_file
    
    def wait_for_completion(self, check_interval: int = 60):
        """Monitor until all processes complete"""
        print("\n🔍 Starting monitoring (Ctrl+C to stop)...")
        print(f"Checking every {check_interval} seconds\n")
        
        completed = set()
        
        try:
            while True:
                running = self.check_processes()
                report = self.generate_report()
                
                # Check for newly completed processes
                for proc, status in running.items():
                    if not status and proc not in completed:
                        completed.add(proc)
                        print(f"\n✅ PROCESS COMPLETED: {proc}\n")
                
                # Print status
                self.print_report(report)
                
                # Save report
                self.save_report(report)
                
                # Check if all done
                if not any(running.values()):
                    print("\n🎉 ALL PROCESSES COMPLETED!\n")
                    final_report = self.generate_report()
                    self.print_final_summary(final_report)
                    return final_report
                
                print(f"\n⏳ Waiting {check_interval}s for next check...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Monitoring stopped by user")
            return self.generate_report()
    
    def print_final_summary(self, report: Dict):
        """Print final completion summary"""
        print("\n" + "=" * 80)
        print("🎉 FINAL COMPLETION SUMMARY")
        print("=" * 80)
        print(f"Completed at: {datetime.now().isoformat()}")
        print(f"Total elapsed: {report['elapsed_time']}")
        print("\n📊 DATASETS IMPORTED:")
        
        for dataset_id, info in report['datasets'].items():
            if info['files'] > 0:
                print(f"  ✅ {info['name']}: {info['files']} files ({info['size']})")
        
        print(f"\n📈 TOTAL: {report['total_files']} files ingested")
        print("=" * 80)
        
        # Save final report
        final_file = LOG_DIR / f"FINAL_REPORT_{datetime.now():%Y%m%d_%H%M%S}.json"
        with open(final_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\n📄 Report saved to: {final_file}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Monitor data ingestion")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")
    args = parser.parse_args()
    
    monitor = ImportMonitor()
    
    if args.once:
        report = monitor.generate_report()
        monitor.print_report(report)
        monitor.save_report(report)
    else:
        monitor.wait_for_completion(check_interval=args.interval)


if __name__ == "__main__":
    main()
