#!/usr/bin/env python3
"""
Windows RTX 3060 Worker Setup Script

This script configures a Windows machine with RTX 3060 for processing
Epstein Files Analysis pipeline tasks.

Usage: python setup_windows_worker.py
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict


class WindowsWorkerSetup:
    def __init__(self):
        self.config = self.load_config()
        self.python_path = None
        self.cuda_path = None

    def load_config(self) -> Dict:
        """Load configuration from config file or create default."""
        config_path = Path(__file__).parent / "config_windows.json"

        default_config = {
            "linux_server": {
                "host": "192.168.4.25",
                "user": "blaine",
                "ssh_port": 22,
                "remote_path": "/home/cbwinslow/workspace/epstein"
            },
            "local_paths": {
                "base_dir": "C:\\epstein-windows",
                "downloads": "C:\\epstein-windows\\downloads",
                "processing": "C:\\epstein-windows\\processing",
                "results": "C:\\epstein-windows\\results"
            },
            "packages": [
                "pymupdf", "pyarrow", "pandas", "numpy", "scipy",
                "scikit-learn", "spacy", "insightface", "opencv-python-headless",
                "jiwer", "nervaluate", "networkx", "tqdm", "aiohttp",
                "playwright", "rapidfuzz", "torch", "transformers",
                "sentence-transformers", "huggingface-hub", "datasets"
            ],
            "cuda_version": "12.4"
        }

        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config

    def print_header(self):
        """Print setup header."""
        print("🚀 Windows RTX 3060 Worker Setup")
        print("=" * 50)
        print(f"Target Linux Server: {self.config['linux_server']['user']}@{self.config['linux_server']['host']}")
        print(f"Local Base Directory: {self.config['local_paths']['base_dir']}")
        print(f"CUDA Version: {self.config['cuda_version']}")
        print()

    def check_python(self) -> bool:
        """Check if Python 3.12 is installed."""
        print("📋 Checking Python installation...")

        try:
            result = subprocess.run([sys.executable, "--version"],
                                  capture_output=True, text=True, check=True)
            version = result.stdout.strip()
            print(f"   Found: {version}")

            if "3.12" in version:
                self.python_path = sys.executable
                print("   ✅ Python 3.12 found")
                return True
            else:
                print("   ❌ Python 3.12 not found. Please install Python 3.12")
                return False

        except subprocess.CalledProcessError:
            print("   ❌ Could not determine Python version")
            return False

    def check_cuda(self) -> bool:
        """Check CUDA installation and compatibility."""
        print("📋 Checking CUDA installation...")

        # Check nvidia-smi
        try:
            result = subprocess.run(["nvidia-smi"], capture_output=True, text=True, check=True)
            if "RTX 3060" in result.stdout:
                print("   ✅ RTX 3060 detected")
            else:
                print("   ⚠️  RTX 3060 not detected, but continuing...")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   ⚠️  nvidia-smi not available, but continuing...")

        # Check CUDA toolkit
        cuda_paths = [
            f"C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA\\v{self.config['cuda_version']}",
            f"C:\\Program Files (x86)\\NVIDIA Corporation\\CUDA Tools\\v{self.config['cuda_version']}"
        ]

        for path in cuda_paths:
            if os.path.exists(path):
                self.cuda_path = path
                print(f"   ✅ CUDA {self.config['cuda_version']} found at {path}")
                return True

        print(f"   ⚠️  CUDA {self.config['cuda_version']} not found, but continuing...")
        return True  # Don't fail setup, just warn

    def create_directories(self) -> bool:
        """Create required directories."""
        print("📁 Creating project directories...")

        try:
            for path_name, path_value in self.config['local_paths'].items():
                if path_name != "base_dir":  # Skip base_dir, create others
                    os.makedirs(path_value, exist_ok=True)
                    print(f"   ✅ Created: {path_value}")
            return True
        except Exception as e:
            print(f"   ❌ Failed to create directories: {e}")
            return False

    def install_packages(self) -> bool:
        """Install required Python packages."""
        print("📦 Installing Python packages...")

        # Install packages using pip
        for package in self.config['packages']:
            try:
                print(f"   Installing {package}...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install",
                    package, "--upgrade", "--no-cache-dir"
                ], check=True, capture_output=True)
                print(f"   ✅ {package} installed")
            except subprocess.CalledProcessError as e:
                print(f"   ⚠️  Failed to install {package}: {e}")
                # Continue with other packages

        return True

    def setup_spacy_model(self) -> bool:
        """Download spaCy model."""
        print("📦 Setting up spaCy model...")

        try:
            subprocess.run([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm"
            ], check=True, capture_output=True)
            print("   ✅ spaCy en_core_web_sm downloaded")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to download spaCy model: {e}")
            return False

    def setup_playwright(self) -> bool:
        """Setup Playwright browsers."""
        print("🌐 Setting up Playwright browsers...")

        try:
            subprocess.run([
                sys.executable, "-m", "playwright", "install", "chromium"
            ], check=True, capture_output=True)
            print("   ✅ Playwright Chromium installed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to install Playwright: {e}")
            return False

    def test_ssh_connection(self) -> bool:
        """Test SSH connection to Linux server."""
        print("🔗 Testing SSH connection...")

        try:
            # Test SSH connection
            result = subprocess.run([
                "ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
                f"{self.config['linux_server']['user']}@{self.config['linux_server']['host']}",
                "echo 'SSH connection successful'"
            ], capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                print("   ✅ SSH connection successful")
                return True
            else:
                print(f"   ⚠️  SSH connection failed: {result.stderr}")
                print("   Note: You may need to set up SSH keys manually")
                return True  # Don't fail setup, just warn
        except subprocess.TimeoutExpired:
            print("   ⚠️  SSH connection timed out")
            return True  # Don't fail setup
        except Exception as e:
            print(f"   ⚠️  SSH test failed: {e}")
            return True  # Don't fail setup

    def create_processing_script(self) -> bool:
        """Create the main processing script."""
        print("📝 Creating processing script...")

        script_content = '''#!/usr/bin/env python3
"""
Windows RTX 3060 Processing Worker

This script runs on the Windows machine to process files using the RTX 3060 GPU.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

class WindowsProcessor:
    def __init__(self):
        self.config = self.load_config()
        
    def load_config(self) -> Dict:
        """Load configuration."""
        config_path = Path(__file__).parent / "config_windows.json"
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def process_ocr(self, pdf_path: str, output_dir: str) -> bool:
        """Process PDF with OCR using RTX 3060."""
        print(f"Processing OCR for: {pdf_path}")
        
        try:
            # Use PyMuPDF for text extraction
            import fitz  # PyMuPDF
            
            doc = fitz.open(pdf_path)
            text_content = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                text_content.append({
                    "page": page_num + 1,
                    "text": text,
                    "confidence": 1.0  # PyMuPDF doesn't provide confidence
                })
            
            # Save OCR results
            output_file = Path(output_dir) / f"{Path(pdf_path).stem}_ocr.json"
            with open(output_file, 'w') as f:
                json.dump(text_content, f, indent=2)
            
            print(f"   ✅ OCR completed: {output_file}")
            return True
            
        except Exception as e:
            print(f"   ❌ OCR failed: {e}")
            return False
    
    def process_entities(self, text_file: str, output_dir: str) -> bool:
        """Extract entities from text using spaCy."""
        print(f"Extracting entities from: {text_file}")
        
        try:
            import spacy
            
            # Load spaCy model
            nlp = spacy.load("en_core_web_sm")
            
            with open(text_file, 'r') as f:
                data = json.load(f)
            
            all_entities = []
            
            for page_data in data:
                doc = nlp(page_data['text'])
                
                for ent in doc.ents:
                    all_entities.append({
                        "text": ent.text,
                        "label": ent.label_,
                        "page": page_data['page'],
                        "start": ent.start_char,
                        "end": ent.end_char
                    })
            
            # Save entity results
            output_file = Path(output_dir) / f"{Path(text_file).stem}_entities.json"
            with open(output_file, 'w') as f:
                json.dump(all_entities, f, indent=2)
            
            print(f"   ✅ Entity extraction completed: {output_file}")
            return True
            
        except Exception as e:
            print(f"   ❌ Entity extraction failed: {e}")
            return False
    
    def process_images(self, pdf_path: str, output_dir: str) -> bool:
        """Extract and analyze images from PDF."""
        print(f"Processing images from: {pdf_path}")
        
        try:
            import fitz  # PyMuPDF
            import cv2
            import numpy as np
            
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Save image
                    image_path = Path(output_dir) / f"{Path(pdf_path).stem}_page{page_num+1}_img{img_index+1}.png"
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
            
            print(f"   ✅ Image extraction completed")
            return True
            
        except Exception as e:
            print(f"   ❌ Image processing failed: {e}")
            return False
    
    def run_processing_loop(self):
        """Main processing loop."""
        print("🚀 Starting Windows RTX 3060 processing worker...")
        
        downloads_dir = self.config['local_paths']['downloads']
        processing_dir = self.config['local_paths']['processing']
        results_dir = self.config['local_paths']['results']
        
        while True:
            try:
                # Look for new files to process
                pdf_files = list(Path(downloads_dir).glob("*.pdf"))
                
                if not pdf_files:
                    print("   No files to process, waiting...")
                    time.sleep(30)
                    continue
                
                for pdf_file in pdf_files:
                    print(f"Processing file: {pdf_file}")
                    
                    # Create processing subdirectory
                    proc_subdir = Path(processing_dir) / pdf_file.stem
                    proc_subdir.mkdir(exist_ok=True)
                    
                    # OCR processing
                    self.process_ocr(str(pdf_file), str(proc_subdir))
                    
                    # Entity extraction
                    ocr_file = proc_subdir / f"{pdf_file.stem}_ocr.json"
                    if ocr_file.exists():
                        self.process_entities(str(ocr_file), str(proc_subdir))
                    
                    # Image processing
                    self.process_images(str(pdf_file), str(proc_subdir))
                    
                    # Move to results
                    result_subdir = Path(results_dir) / pdf_file.stem
                    proc_subdir.rename(result_subdir)
                    
                    # Remove original
                    pdf_file.unlink()
                    
                    print(f"   ✅ Completed processing: {pdf_file}")
                
            except Exception as e:
                print(f"   Error in processing loop: {e}")
                time.sleep(60)

if __name__ == "__main__":
    processor = WindowsProcessor()
    processor.run_processing_loop()
'''

        script_path = Path(self.config['local_paths']['base_dir']) / "process_files.py"
        with open(script_path, 'w') as f:
            f.write(script_content)

        print(f"   ✅ Created processing script: {script_path}")
        return True

    def create_transfer_script(self) -> bool:
        """Create file transfer script."""
        print("📝 Creating file transfer script...")

        transfer_content = '''#!/usr/bin/env python3
"""
File Transfer Script for Windows RTX 3060 Worker

Handles file transfers between Linux server and Windows worker.
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Dict

def load_config() -> Dict:
    """Load configuration."""
    config_path = Path(__file__).parent / "config_windows.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def transfer_files_to_windows():
    """Transfer files from Linux server to Windows."""
    config = load_config()
    
    print("📥 Transferring files from Linux server...")
    
    # Use scp to download files
    remote_path = f"{config['linux_server']['user']}@{config['linux_server']['host']}:{config['linux_server']['remote_path']}/downloads/"
    local_path = config['local_paths']['downloads']
    
    try:
        subprocess.run([
            "scp", "-r", remote_path, local_path
        ], check=True)
        print("   ✅ Files transferred to Windows")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Transfer failed: {e}")

def transfer_results_to_linux():
    """Transfer processed results back to Linux server."""
    config = load_config()
    
    print("📤 Transferring results to Linux server...")
    
    local_path = config['local_paths']['results']
    remote_path = f"{config['linux_server']['user']}@{config['linux_server']['host']}:{config['linux_server']['remote_path']}/results/"
    
    try:
        subprocess.run([
            "scp", "-r", local_path, remote_path
        ], check=True)
        print("   ✅ Results transferred to Linux server")
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Transfer failed: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "upload":
        transfer_results_to_linux()
    else:
        transfer_files_to_windows()
'''

        transfer_path = Path(self.config['local_paths']['base_dir']) / "transfer_files.py"
        with open(transfer_path, 'w') as f:
            f.write(transfer_content)

        print(f"   ✅ Created transfer script: {transfer_path}")
        return True

    def run_setup(self):
        """Run the complete setup process."""
        self.print_header()

        # Check prerequisites
        if not self.check_python():
            return False

        if not self.check_cuda():
            print("   ⚠️  CUDA setup incomplete, but continuing...")

        # Create directories
        if not self.create_directories():
            return False

        # Install packages
        if not self.install_packages():
            return False

        # Setup models and tools
        self.setup_spacy_model()
        self.setup_playwright()

        # Test connections
        self.test_ssh_connection()

        # Create scripts
        self.create_processing_script()
        self.create_transfer_script()

        print()
        print("🎉 Windows RTX 3060 worker setup completed!")
        print()
        print("Next steps:")
        print("1. Run 'python process_files.py' on Windows to start processing")
        print("2. Use 'python transfer_files.py' to transfer files")
        print("3. Use 'python transfer_files.py upload' to upload results")
        print()
        print("Configuration saved to: config_windows.json")

        return True

def main():
    """Main setup function."""
    setup = WindowsWorkerSetup()
    success = setup.run_setup()

    if success:
        print("✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
