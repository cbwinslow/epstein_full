#!/usr/bin/env python3
"""
Comprehensive Download Orchestrator
Downloads all missing DOJ datasets, FEC data, government docs, and politician records
without duplication. Uses existing file checks to avoid re-downloading.
"""

import os
import sys
import json
import subprocess
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Configuration
PROJECT_ROOT = "/home/cbwinslow/workspace/epstein"
DATA_ROOT = "/home/cbwinslow/workspace/epstein-data/raw-files"
LOG_DIR = "/home/cbwinslow/workspace/epstein-data/logs"
STATE_FILE = f"{LOG_DIR}/download_state.json"

# Ensure directories exist
os.makedirs(DATA_ROOT, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Dataset configuration
DATASETS = {
    "data0": {"name": "Dataset 0", "type": "doj", "priority": 1},
    "data1": {"name": "Dataset 1", "type": "doj", "priority": 1, "exists": True},  # Already have this
    "data2": {"name": "Dataset 2", "type": "doj", "priority": 1},
    "data3": {"name": "Dataset 3", "type": "doj", "priority": 1},
    "data4": {"name": "Dataset 4", "type": "doj", "priority": 1},
    "data5": {"name": "Dataset 5", "type": "doj", "priority": 1},
    "data6": {"name": "Dataset 6", "type": "doj", "priority": 1},
    "data7": {"name": "Dataset 7", "type": "doj", "priority": 1},
    "data8": {"name": "Dataset 8", "type": "doj", "priority": 1},
    "data9": {"name": "Dataset 9", "type": "doj", "priority": 1},
    "data10": {"name": "Dataset 10", "type": "doj", "priority": 1, "exists": True},  # Already have this
    "data11": {"name": "Dataset 11", "type": "doj", "priority": 1, "exists": True},  # Already have this
    "data12": {"name": "Dataset 12", "type": "doj", "priority": 1},
    "fec": {"name": "FEC Data", "type": "fec", "priority": 2},
    "government": {"name": "Government Documents", "type": "gov", "priority": 2},
    "politicians": {"name": "Politician Records", "type": "pol", "priority": 2},
}

def load_state():
    """Load download state from file"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"completed": [], "in_progress": [], "failed": [], "skipped": []}

def save_state(state):
    """Save download state to file"""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_existing_files(dataset_name):
    """Check if dataset already has files"""
    dataset_path = os.path.join(DATA_ROOT, dataset_name)
    if not os.path.exists(dataset_path):
        return 0
    
    count = 0
    for root, dirs, files in os.walk(dataset_path):
        count += len(files)
    return count

def get_file_hash(filepath):
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def run_download_doj(dataset_num):
    """Download specific DOJ dataset using download_doj.py"""
    script_path = f"{PROJECT_ROOT}/scripts/download_doj.py"
    
    print(f"[DOJ] Starting download for dataset {dataset_num}...")
    
    # Run the download script with correct arguments
    cmd = [
        sys.executable, script_path,
        "--datasets", str(dataset_num)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=86400,  # 24 hour timeout for large datasets
            cwd=PROJECT_ROOT
        )
        
        if result.returncode == 0:
            print(f"[DOJ] Dataset {dataset_num} download completed successfully")
            return True
        else:
            print(f"[DOJ] Dataset {dataset_num} download failed:")
            print(result.stderr)
            return False
    except subprocess.TimeoutExpired:
        print(f"[DOJ] Dataset {dataset_num} download timed out after 24 hours")
        return False
    except Exception as e:
        print(f"[DOJ] Error downloading dataset {dataset_num}: {e}")
        return False

def run_download_fec():
    """Download FEC bulk data"""
    script_path = f"{PROJECT_ROOT}/scripts/download_fec_bulk.py"
    target_dir = f"{DATA_ROOT}/fec"
    
    os.makedirs(target_dir, exist_ok=True)
    
    print("[FEC] Starting FEC bulk data download...")
    print(f"[FEC] Target directory: {target_dir}")
    
    # Check if already has files
    existing = check_existing_files("fec")
    if existing > 0:
        print(f"[FEC] Found {existing} existing files, checking for completeness...")
        # FEC bulk data typically has ~100 files (indiv, cm, cn for each cycle)
        if existing >= 50:  # Assume mostly complete if >50 files
            print("[FEC] FEC data appears complete, skipping download")
            return True
    
    cmd = [
        sys.executable, script_path,
        "--output", target_dir,
        "--years", "2000-2024",
        "--types", "indiv,cm,cn"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=14400)
        if result.returncode == 0:
            print("[FEC] FEC download completed successfully")
            return True
        else:
            print("[FEC] FEC download failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"[FEC] Error: {e}")
        return False

def run_download_government():
    """Download government documents"""
    script_path = f"{PROJECT_ROOT}/scripts/download_gov_data.py"
    target_dir = f"{DATA_ROOT}/government"
    
    os.makedirs(target_dir, exist_ok=True)
    
    print("[GOV] Starting government documents download...")
    
    existing = check_existing_files("government")
    if existing > 100:  # Arbitrary threshold
        print(f"[GOV] Found {existing} existing files, skipping")
        return True
    
    cmd = [sys.executable, script_path, "--output", target_dir]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=14400)
        return result.returncode == 0
    except Exception as e:
        print(f"[GOV] Error: {e}")
        return False

def run_download_politicians():
    """Download politician financial records"""
    script_path = f"{PROJECT_ROOT}/scripts/download_politicians_financial.py"
    target_dir = f"{DATA_ROOT}/politicians"
    
    os.makedirs(target_dir, exist_ok=True)
    
    print("[POL] Starting politician records download...")
    
    existing = check_existing_files("politicians")
    if existing > 50:
        print(f"[POL] Found {existing} existing files, skipping")
        return True
    
    cmd = [sys.executable, script_path, "--output", target_dir]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=14400)
        return result.returncode == 0
    except Exception as e:
        print(f"[POL] Error: {e}")
        return False

def run_epstein_ripper(dataset_num):
    """Run epstein-ripper for DOJ dataset"""
    ripper_path = f"{PROJECT_ROOT}/epstein-ripper/auto_ep_rip.py"
    target_dir = f"{DATA_ROOT}/data{dataset_num}"
    
    if not os.path.exists(ripper_path):
        print(f"[RIPPER] auto_ep_rip.py not found at {ripper_path}")
        return False
    
    print(f"[RIPPER] Starting epstein-ripper for dataset {dataset_num}...")
    
    # epstein-ripper has interactive features, need to handle carefully
    cmd = [sys.executable, ripper_path, "--dataset", str(dataset_num)]
    
    try:
        # Run with 24 hour timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=86400,
            cwd=os.path.dirname(ripper_path)
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[RIPPER] Error: {e}")
        return False

def main():
    """Main orchestrator"""
    print("="*80)
    print("COMPREHENSIVE DATA DOWNLOAD ORCHESTRATOR")
    print("="*80)
    print(f"Started: {datetime.now().isoformat()}")
    print()
    
    # Load state
    state = load_state()
    print(f"Loaded state: {len(state['completed'])} completed, {len(state['failed'])} failed")
    print()
    
    # Check existing datasets
    print("Checking existing datasets...")
    for dataset_name, config in DATASETS.items():
        existing = check_existing_files(dataset_name)
        if existing > 0:
            print(f"  ✓ {dataset_name}: {existing} files already present")
            config["exists"] = True
            config["file_count"] = existing
        else:
            print(f"  ✗ {dataset_name}: Not found (needs download)")
            config["exists"] = False
    print()
    
    # Priority 1: DOJ datasets (data0-9, data12)
    print("="*80)
    print("PHASE 1: DOJ DATASETS")
    print("="*80)
    
    doj_datasets = [k for k, v in DATASETS.items() if v["type"] == "doj" and not v.get("exists")]
    doj_datasets.sort()  # Process in order
    
    print(f"Datasets to download: {doj_datasets}")
    print()
    
    for dataset in doj_datasets:
        if dataset in state["completed"]:
            print(f"[{dataset}] Already completed, skipping")
            continue
            
        if dataset in state["in_progress"]:
            print(f"[{dataset}] Resuming previous download...")
        else:
            print(f"[{dataset}] Starting fresh download...")
            state["in_progress"].append(dataset)
            save_state(state)
        
        # Extract dataset number
        dataset_num = int(dataset.replace("data", ""))
        
        # Try download_doj.py first, fallback to epstein-ripper
        success = False
        
        # Method 1: download_doj.py
        if os.path.exists(f"{PROJECT_ROOT}/scripts/download_doj.py"):
            success = run_download_doj(dataset_num)
        
        # Method 2: epstein-ripper (if method 1 fails)
        if not success and os.path.exists(f"{PROJECT_ROOT}/epstein-ripper/auto_ep_rip.py"):
            print(f"[{dataset}] Trying epstein-ripper...")
            success = run_epstein_ripper(dataset_num)
        
        # Update state
        if success:
            state["completed"].append(dataset)
            if dataset in state["in_progress"]:
                state["in_progress"].remove(dataset)
            print(f"[{dataset}] ✓ Download completed")
        else:
            if dataset not in state["failed"]:
                state["failed"].append(dataset)
            if dataset in state["in_progress"]:
                state["in_progress"].remove(dataset)
            print(f"[{dataset}] ✗ Download failed")
        
        save_state(state)
        print()
    
    # Priority 2: FEC, Government, Politicians
    print("="*80)
    print("PHASE 2: SUPPLEMENTARY DATA")
    print("="*80)
    
    # FEC Data
    if "fec" not in state["completed"]:
        print("[FEC] Starting FEC data download...")
        if run_download_fec():
            state["completed"].append("fec")
            print("[FEC] ✓ Completed")
        else:
            state["failed"].append("fec")
            print("[FEC] ✗ Failed")
        save_state(state)
    else:
        print("[FEC] Already completed, skipping")
    
    # Government documents
    if "government" not in state["completed"]:
        print("[GOV] Starting government docs download...")
        if run_download_government():
            state["completed"].append("government")
            print("[GOV] ✓ Completed")
        else:
            state["failed"].append("government")
            print("[GOV] ✗ Failed")
        save_state(state)
    else:
        print("[GOV] Already completed, skipping")
    
    # Politician records
    if "politicians" not in state["completed"]:
        print("[POL] Starting politician records download...")
        if run_download_politicians():
            state["completed"].append("politicians")
            print("[POL] ✓ Completed")
        else:
            state["failed"].append("politicians")
            print("[POL] ✗ Failed")
        save_state(state)
    else:
        print("[POL] Already completed, skipping")
    
    # Final summary
    print()
    print("="*80)
    print("DOWNLOAD ORCHESTRATION COMPLETE")
    print("="*80)
    print(f"Completed:  {len(state['completed'])} datasets")
    print(f"Failed:     {len(state['failed'])} datasets")
    print(f"In Progress: {len(state['in_progress'])} datasets")
    print()
    
    if state['completed']:
        print("Completed datasets:")
        for d in state['completed']:
            count = check_existing_files(d)
            print(f"  ✓ {d}: {count} files")
    
    if state['failed']:
        print("\nFailed datasets (retry needed):")
        for d in state['failed']:
            print(f"  ✗ {d}")
    
    print()
    print(f"State saved to: {STATE_FILE}")
    print(f"Finished: {datetime.now().isoformat()}")
    print("="*80)
    
    return len(state['failed']) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
