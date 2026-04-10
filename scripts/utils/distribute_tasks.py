#!/usr/bin/env python3
"""
Task Distribution Script for Epstein Files Analysis

This script coordinates distributed processing between the Linux server
and Windows RTX 3060 machine for optimal performance.

Usage:
    uv run python scripts/distribute_tasks.py --task ocr --dataset data9 --batch-size 100
"""

import argparse
import json
import logging
import os
import sqlite3
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple


@dataclass
class Task:
    task_id: str
    task_type: str
    files: List[str]
    status: str = "pending"
    assigned_to: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    results: Optional[Dict] = None
    error: Optional[str] = None


class TaskDistributor:
    def __init__(self):
        self.linux_server = "localhost"
        self.windows_host = "192.168.4.25"
        self.windows_user = "blaine"
        self.windows_path = "C:\\epstein-windows"

        # Task queues
        self.pending_tasks: List[Task] = []
        self.running_tasks: List[Task] = []
        self.completed_tasks: List[Task] = []

        # Performance tracking
        self.performance_metrics = {
            "linux": {"ocr_speed": 0, "face_speed": 0, "ner_speed": 0},
            "windows": {"ocr_speed": 0, "face_speed": 0, "ner_speed": 0}
        }

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/task_distribution.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Create database for task tracking
        self.db_path = "logs/task_distribution.db"
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database for task tracking"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    task_type TEXT,
                    files TEXT,
                    status TEXT,
                    assigned_to TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    results TEXT,
                    error TEXT
                )
            """)
            conn.commit()

    def run_ssh_command(self, host: str, command: str, timeout: int = 300) -> Tuple[bool, str, str]:
        """Execute SSH command and return success, stdout, stderr"""
        if host == "windows":
            full_command = f"ssh {self.windows_user}@{self.windows_host} \"{command}\""
        else:
            full_command = command

        try:
            result = subprocess.run(
                full_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            success = result.returncode == 0
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if not success:
                self.logger.error(f"Command failed: {command}")
                self.logger.error(f"Error: {stderr}")

            return success, stdout, stderr

        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out: {command}")
            return False, "", "Timeout"
        except Exception as e:
            self.logger.error(f"Command error: {e}")
            return False, "", str(e)

    def discover_files(self, dataset: str, file_type: str = "pdf") -> List[str]:
        """Discover files to process in a dataset"""
        data_path = f"/home/cbwinslow/workspace/epstein-data/raw-files/{dataset}"

        if file_type == "pdf":
            pattern = "*.pdf"
        elif file_type == "image":
            pattern = "*.{jpg,jpeg,png,gif}"
        else:
            pattern = "*"

        success, stdout, stderr = self.run_ssh_command(
            "linux",
            f"find {data_path} -name '{pattern}' | head -1000"
        )

        if success:
            files = stdout.split('\n')
            self.logger.info(f"Discovered {len(files)} files in {dataset}")
            return files
        else:
            self.logger.error(f"Failed to discover files: {stderr}")
            return []

    def estimate_task_time(self, task_type: str, file_count: int, target_machine: str) -> float:
        """Estimate task completion time based on historical data"""
        # Base performance estimates (files per minute)
        base_performance = {
            "linux": {"ocr": 60, "face": 30, "ner": 200},
            "windows": {"ocr": 200, "face": 80, "ner": 1500}
        }

        if target_machine in self.performance_metrics:
            # Use historical performance if available
            perf = self.performance_metrics[target_machine]
        else:
            perf = base_performance[target_machine]

        speed = perf.get(task_type, 1)
        estimated_minutes = file_count / speed

        return estimated_minutes

    def select_optimal_machine(self, task_type: str, file_count: int) -> str:
        """Select the optimal machine for a task based on performance"""
        linux_time = self.estimate_task_time(task_type, file_count, "linux")
        windows_time = self.estimate_task_time(task_type, file_count, "windows")

        # Add overhead for data transfer to Windows
        windows_overhead = 2.0  # 2 minutes transfer overhead
        windows_total = windows_time + windows_overhead

        if windows_total < linux_time:
            return "windows"
        else:
            return "linux"

    def create_task(self, task_type: str, files: List[str], dataset: str) -> Task:
        """Create a new task"""
        task_id = f"{task_type}_{dataset}_{int(time.time())}"

        return Task(
            task_id=task_id,
            task_type=task_type,
            files=files
        )

    def transfer_data_to_windows(self, files: List[str], dataset: str) -> bool:
        """Transfer files to Windows machine"""
        self.logger.info(f"Transferring {len(files)} files to Windows...")

        # Create dataset directory on Windows
        success, _, _ = self.run_ssh_command(
            "windows",
            f"mkdir {self.windows_path}\\data\\{dataset}"
        )

        if not success:
            self.logger.error("Failed to create directory on Windows")
            return False

        # Transfer files using rsync
        for file_path in files:
            # Extract just the filename
            filename = os.path.basename(file_path)
            windows_dest = f"{self.windows_user}@{self.windows_host}:{self.windows_path}\\data\\{dataset}\\{filename}"

            success, _, stderr = self.run_ssh_command(
                "linux",
                f"rsync -avz {file_path} {windows_dest}",
                timeout=120
            )

            if not success:
                self.logger.error(f"Failed to transfer {filename}: {stderr}")
                return False

        self.logger.info("Data transfer to Windows completed")
        return True

    def execute_linux_task(self, task: Task) -> Dict:
        """Execute task on Linux server"""
        self.logger.info(f"Executing {task.task_type} task on Linux: {task.task_id}")

        start_time = time.time()

        if task.task_type == "ocr":
            # Use existing Linux OCR pipeline
            result = self._run_linux_ocr(task.files)
        elif task.task_type == "face":
            # Use existing Linux face detection
            result = self._run_linux_face_detection(task.files)
        elif task.task_type == "ner":
            # Use existing Linux NER pipeline
            result = self._run_linux_ner(task.files)
        else:
            result = {"error": f"Unknown task type: {task.task_type}"}

        end_time = time.time()
        result["processing_time"] = end_time - start_time

        return result

    def execute_windows_task(self, task: Task) -> Dict:
        """Execute task on Windows RTX 3060"""
        self.logger.info(f"Executing {task.task_type} task on Windows: {task.task_id}")

        # Transfer data to Windows
        if not self.transfer_data_to_windows(task.files, "batch"):
            return {"error": "Data transfer failed"}

        # Execute task on Windows
        start_time = time.time()

        if task.task_type == "ocr":
            result = self._run_windows_ocr(task.files)
        elif task.task_type == "face":
            result = self._run_windows_face_detection(task.files)
        elif task.task_type == "ner":
            result = self._run_windows_ner(task.files)
        else:
            result = {"error": f"Unknown task type: {task.task_type}"}

        end_time = time.time()
        result["processing_time"] = end_time - start_time

        return result

    def _run_linux_ocr(self, files: List[str]) -> Dict:
        """Run OCR on Linux using existing pipeline"""
        # Use existing epstein-pipeline OCR
        cmd = f"epstein-pipeline ocr {' '.join(files)} -o /tmp/ocr_output --backend surya"
        success, stdout, stderr = self.run_ssh_command("linux", cmd, timeout=600)

        return {
            "processed": len(files) if success else 0,
            "success": success,
            "output": stdout,
            "error": stderr if not success else None
        }

    def _run_linux_face_detection(self, files: List[str]) -> Dict:
        """Run face detection on Linux"""
        # Use existing InsightFace setup
        cmd = f"python3 scripts/face_detection.py --files {' '.join(files)}"
        success, stdout, stderr = self.run_ssh_command("linux", cmd, timeout=600)

        return {
            "detected_faces": 0,  # Parse from output
            "processed": len(files) if success else 0,
            "success": success,
            "error": stderr if not success else None
        }

    def _run_linux_ner(self, files: List[str]) -> Dict:
        """Run NER on Linux"""
        # Use existing NER pipeline
        cmd = f"epstein-pipeline extract-entities {' '.join(files)} -o /tmp/ner_output"
        success, stdout, stderr = self.run_ssh_command("linux", cmd, timeout=600)

        return {
            "extracted_entities": 0,  # Parse from output
            "processed": len(files) if success else 0,
            "success": success,
            "error": stderr if not success else None
        }

    def _run_windows_ocr(self, files: List[str]) -> Dict:
        """Run OCR on Windows RTX 3060"""
        # Use Windows worker script
        cmd = f"python {self.windows_path}\\scripts\\windows_worker.py --task ocr --files {' '.join(files)}"
        success, stdout, stderr = self.run_ssh_command("windows", cmd, timeout=600)

        return {
            "processed": len(files) if success else 0,
            "success": success,
            "output": stdout,
            "error": stderr if not success else None
        }

    def _run_windows_face_detection(self, files: List[str]) -> Dict:
        """Run face detection on Windows RTX 3060"""
        cmd = f"python {self.windows_path}\\scripts\\windows_worker.py --task face --files {' '.join(files)}"
        success, stdout, stderr = self.run_ssh_command("windows", cmd, timeout=600)

        return {
            "detected_faces": 0,  # Parse from output
            "processed": len(files) if success else 0,
            "success": success,
            "error": stderr if not success else None
        }

    def _run_windows_ner(self, files: List[str]) -> Dict:
        """Run NER on Windows RTX 3060"""
        cmd = f"python {self.windows_path}\\scripts\\windows_worker.py --task ner --files {' '.join(files)}"
        success, stdout, stderr = self.run_ssh_command("windows", cmd, timeout=600)

        return {
            "extracted_entities": 0,  # Parse from output
            "processed": len(files) if success else 0,
            "success": success,
            "error": stderr if not success else None
        }

    def process_task(self, task: Task) -> bool:
        """Process a single task"""
        self.logger.info(f"Starting task: {task.task_id}")

        # Select optimal machine
        optimal_machine = self.select_optimal_machine(task.task_type, len(task.files))
        task.assigned_to = optimal_machine
        task.start_time = datetime.now().isoformat()

        # Update database
        self._update_task_in_db(task)

        try:
            if optimal_machine == "linux":
                result = self.execute_linux_task(task)
            else:
                result = self.execute_windows_task(task)

            task.end_time = datetime.now().isoformat()
            task.results = result
            task.status = "completed" if result.get("success", False) else "failed"

            self.logger.info(f"Task {task.task_id} completed: {task.status}")

        except Exception as e:
            task.end_time = datetime.now().isoformat()
            task.error = str(e)
            task.status = "failed"

            self.logger.error(f"Task {task.task_id} failed: {e}")

        # Update database
        self._update_task_in_db(task)

        return task.status == "completed"

    def _update_task_in_db(self, task: Task):
        """Update task in database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO tasks 
                (task_id, task_type, files, status, assigned_to, start_time, end_time, results, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id,
                task.task_type,
                json.dumps(task.files),
                task.status,
                task.assigned_to,
                task.start_time,
                task.end_time,
                json.dumps(task.results) if task.results else None,
                task.error
            ))
            conn.commit()

    def run_batch_processing(self, task_type: str, dataset: str, batch_size: int = 100):
        """Run batch processing for a dataset"""
        self.logger.info(f"Starting batch processing: {task_type} on {dataset}")

        # Discover files
        files = self.discover_files(dataset, "pdf" if task_type == "ocr" else "image")

        if not files:
            self.logger.error("No files discovered")
            return

        # Create batches
        batches = [files[i:i+batch_size] for i in range(0, len(files), batch_size)]
        self.logger.info(f"Created {len(batches)} batches of {batch_size} files each")

        # Process batches
        completed = 0
        failed = 0

        for i, batch_files in enumerate(batches):
            self.logger.info(f"Processing batch {i+1}/{len(batches)}")

            task = self.create_task(task_type, batch_files, dataset)

            if self.process_task(task):
                completed += 1
            else:
                failed += 1

        self.logger.info(f"Batch processing completed: {completed} success, {failed} failed")

    def monitor_performance(self):
        """Monitor and update performance metrics"""
        self.logger.info("Monitoring performance...")

        # Get task statistics from database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT assigned_to, task_type, AVG(processing_time), COUNT(*)
                FROM tasks 
                WHERE status = 'completed' AND processing_time IS NOT NULL
                GROUP BY assigned_to, task_type
            """)

            for row in cursor.fetchall():
                machine, task_type, avg_time, count = row
                if avg_time and count > 0:
                    # Calculate speed (files per minute)
                    speed = (count * 100) / (avg_time / 60)  # Assuming 100 files per task
                    self.performance_metrics[machine][task_type] = speed

        self.logger.info(f"Updated performance metrics: {self.performance_metrics}")

    def generate_report(self):
        """Generate processing report"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT task_type, assigned_to, status, COUNT(*), SUM(processing_time)
                FROM tasks GROUP BY task_type, assigned_to, status
            """)

            report = {
                "summary": {},
                "performance": self.performance_metrics,
                "tasks": []
            }

            for row in cursor.fetchall():
                task_type, machine, status, count, total_time = row
                key = f"{task_type}_{machine}"

                if key not in report["summary"]:
                    report["summary"][key] = {
                        "completed": 0,
                        "failed": 0,
                        "total_time": 0
                    }

                if status == "completed":
                    report["summary"][key]["completed"] = count
                    report["summary"][key]["total_time"] = total_time or 0
                else:
                    report["summary"][key]["failed"] = count

            # Save report
            report_path = "logs/task_distribution_report.json"
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)

            self.logger.info(f"Report saved to {report_path}")


def main():
    parser = argparse.ArgumentParser(description="Distribute tasks between Linux and Windows")
    parser.add_argument("--task", choices=["ocr", "face", "ner"], required=True,
                       help="Type of task to distribute")
    parser.add_argument("--dataset", required=True,
                       help="Dataset to process (e.g., data9)")
    parser.add_argument("--batch-size", type=int, default=100,
                       help="Number of files per batch")
    parser.add_argument("--monitor", action="store_true",
                       help="Monitor performance and generate report")

    args = parser.parse_args()

    distributor = TaskDistributor()

    if args.monitor:
        distributor.monitor_performance()
        distributor.generate_report()
    else:
        distributor.run_batch_processing(args.task, args.dataset, args.batch_size)


if __name__ == "__main__":
    main()
