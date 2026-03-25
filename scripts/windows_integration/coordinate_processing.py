#!/usr/bin/env python3
"""
Linux Server Coordination Script for Windows RTX 3060 Processing

This script runs on the Linux server to coordinate file transfers
and processing with the Windows RTX 3060 worker.

Usage: python coordinate_processing.py
"""

import hashlib
import json
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


@dataclass
class ProcessingTask:
    """Represents a file processing task."""
    file_path: str
    file_hash: str
    file_size: int
    status: str  # pending, processing, completed, failed
    assigned_worker: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result_path: Optional[str] = None

class LinuxCoordinator:
    def __init__(self):
        self.config = self.load_config()
        self.tasks_db = Path(self.config['local_paths']['downloads']) / "tasks.json"
        self.tasks = self.load_tasks()

    def load_config(self) -> Dict:
        """Load configuration from config file."""
        config_path = Path(__file__).parent / "config_windows.json"
        with open(config_path, 'r') as f:
            return json.load(f)

    def load_tasks(self) -> Dict[str, ProcessingTask]:
        """Load existing tasks from database."""
        if self.tasks_db.exists():
            with open(self.tasks_db, 'r') as f:
                data = json.load(f)
                return {k: ProcessingTask(**v) for k, v in data.items()}
        return {}

    def save_tasks(self):
        """Save tasks to database."""
        data = {}
        for task_id, task in self.tasks.items():
            task_dict = task.__dict__.copy()
            # Convert datetime objects to strings
            if task_dict['start_time']:
                task_dict['start_time'] = task_dict['start_time'].isoformat()
            if task_dict['end_time']:
                task_dict['end_time'] = task_dict['end_time'].isoformat()
            data[task_id] = task_dict

        with open(self.tasks_db, 'w') as f:
            json.dump(data, f, indent=2)

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()

    def transfer_files_to_windows(self) -> bool:
        """Transfer pending files to Windows worker."""
        print("📤 Transferring files to Windows worker...")

        downloads_dir = Path(self.config['local_paths']['downloads'])
        pending_files = list(downloads_dir.glob("*.pdf"))

        if not pending_files:
            print("   No files to transfer")
            return True

        # Transfer files via scp
        remote_path = f"{self.config['linux_server']['user']}@{self.config['linux_server']['host']}:{self.config['linux_server']['remote_path']}/downloads/"

        for pdf_file in pending_files:
            try:
                print(f"   Transferring: {pdf_file.name}")

                # Calculate hash for integrity check
                file_hash = self.calculate_file_hash(str(pdf_file))
                file_size = pdf_file.stat().st_size

                # Transfer file
                subprocess.run([
                    "scp", str(pdf_file), remote_path
                ], check=True, capture_output=True)

                # Create task record
                task = ProcessingTask(
                    file_path=str(pdf_file),
                    file_hash=file_hash,
                    file_size=file_size,
                    status="pending",
                    assigned_worker="windows_rtx3060"
                )

                self.tasks[pdf_file.name] = task
                self.save_tasks()

                print(f"   ✅ Transferred: {pdf_file.name}")

            except subprocess.CalledProcessError as e:
                print(f"   ❌ Transfer failed for {pdf_file.name}: {e}")
                return False

        return True

    def check_windows_processing_status(self) -> bool:
        """Check if Windows worker has completed processing."""
        print("📡 Checking Windows processing status...")

        remote_results_path = f"{self.config['linux_server']['user']}@{self.config['linux_server']['host']}:{self.config['linux_server']['remote_path']}/results/"

        try:
            # List remote results directory
            result = subprocess.run([
                "ssh", f"{self.config['linux_server']['user']}@{self.config['linux_server']['host']}",
                f"ls -la {self.config['linux_server']['remote_path']}/results/"
            ], capture_output=True, text=True, check=True)

            if result.stdout.strip():
                print("   Windows worker has results ready")
                return True
            else:
                print("   No results from Windows worker yet")
                return False

        except subprocess.CalledProcessError:
            print("   Could not check Windows worker status")
            return False

    def transfer_results_from_windows(self) -> bool:
        """Transfer processed results from Windows back to Linux."""
        print("📥 Transferring results from Windows worker...")

        remote_results_path = f"{self.config['linux_server']['user']}@{self.config['linux_server']['host']}:{self.config['linux_server']['remote_path']}/results/"
        local_results_dir = Path(self.config['local_paths']['results'])
        local_results_dir.mkdir(exist_ok=True)

        try:
            # Transfer results directory
            subprocess.run([
                "scp", "-r", remote_results_path, str(local_results_dir)
            ], check=True, capture_output=True)

            print("   ✅ Results transferred from Windows")
            return True

        except subprocess.CalledProcessError as e:
            print(f"   ❌ Results transfer failed: {e}")
            return False

    def integrate_results(self) -> bool:
        """Integrate Windows results into main pipeline."""
        print("🔗 Integrating Windows results into main pipeline...")

        results_dir = Path(self.config['local_paths']['results'])

        # Look for new results directories
        result_dirs = [d for d in results_dir.iterdir() if d.is_dir()]

        for result_dir in result_dirs:
            try:
                # Find OCR results
                ocr_files = list(result_dir.glob("*_ocr.json"))
                entity_files = list(result_dir.glob("*_entities.json"))

                if ocr_files:
                    # Process OCR results
                    self.process_ocr_results(ocr_files[0])

                if entity_files:
                    # Process entity results
                    self.process_entity_results(entity_files[0])

                # Update task status
                task_name = result_dir.name + ".pdf"
                if task_name in self.tasks:
                    self.tasks[task_name].status = "completed"
                    self.tasks[task_name].end_time = datetime.now()
                    self.tasks[task_name].result_path = str(result_dir)

                # Clean up
                import shutil
                shutil.rmtree(result_dir)

                print(f"   ✅ Integrated results for: {result_dir.name}")

            except Exception as e:
                print(f"   ❌ Failed to integrate results for {result_dir.name}: {e}")
                return False

        self.save_tasks()
        return True

    def process_ocr_results(self, ocr_file: Path):
        """Process OCR results and integrate into database."""
        print(f"   Processing OCR results: {ocr_file}")

        # This would integrate with the main Epstein pipeline
        # For now, just log the integration
        print("   📊 OCR results ready for pipeline integration")

    def process_entity_results(self, entity_file: Path):
        """Process entity results and integrate into database."""
        print(f"   Processing entity results: {entity_file}")

        # This would integrate with the main Epstein pipeline
        # For now, just log the integration
        print("   📊 Entity results ready for pipeline integration")

    def cleanup_completed_tasks(self):
        """Clean up completed tasks from the task database."""
        current_time = datetime.now()

        # Remove tasks older than 7 days
        cutoff_time = current_time.replace(day=current_time.day - 7)

        tasks_to_remove = []
        for task_id, task in self.tasks.items():
            if task.end_time and task.end_time < cutoff_time:
                tasks_to_remove.append(task_id)

        for task_id in tasks_to_remove:
            del self.tasks[task_id]

        if tasks_to_remove:
            self.save_tasks()
            print(f"   🧹 Cleaned up {len(tasks_to_remove)} old tasks")

    def print_status(self):
        """Print current processing status."""
        print("📊 Processing Status:")
        print(f"   Total tasks: {len(self.tasks)}")

        pending = sum(1 for task in self.tasks.values() if task.status == "pending")
        processing = sum(1 for task in self.tasks.values() if task.status == "processing")
        completed = sum(1 for task in self.tasks.values() if task.status == "completed")
        failed = sum(1 for task in self.tasks.values() if task.status == "failed")

        print(f"   Pending: {pending}")
        print(f"   Processing: {processing}")
        print(f"   Completed: {completed}")
        print(f"   Failed: {failed}")
        print()

    def run_coordination_loop(self):
        """Main coordination loop."""
        print("🚀 Starting Linux-Windows coordination...")
        print(f"Target Windows Worker: {self.config['linux_server']['user']}@{self.config['linux_server']['host']}")
        print()

        while True:
            try:
                # Check for new files to process
                downloads_dir = Path(self.config['local_paths']['downloads'])
                pending_files = list(downloads_dir.glob("*.pdf"))

                if pending_files:
                    print(f"📁 Found {len(pending_files)} new files to process")
                    self.transfer_files_to_windows()

                # Check if Windows has completed processing
                if self.check_windows_processing_status():
                    self.transfer_results_from_windows()
                    self.integrate_results()

                # Clean up old tasks
                self.cleanup_completed_tasks()

                # Print status
                self.print_status()

                # Wait before next check
                print("⏳ Waiting for next coordination cycle...")
                time.sleep(60)

            except KeyboardInterrupt:
                print("\n🛑 Coordination stopped by user")
                break
            except Exception as e:
                print(f"❌ Coordination error: {e}")
                time.sleep(60)

def main():
    """Main coordination function."""
    coordinator = LinuxCoordinator()
    coordinator.run_coordination_loop()

if __name__ == "__main__":
    main()
