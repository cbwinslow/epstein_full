#!/usr/bin/env python3
"""
Epstein Full — Development Environment Verification

Quick verification that all components are installed and working.
Run after setup.sh or manually:

  uv run python scripts/setup_dev.py
"""

import sys
import importlib
from pathlib import Path


def check_import(module_name: str, display_name: str = None) -> bool:
    """Check if a module can be imported."""
    name = display_name or module_name
    try:
        importlib.import_module(module_name)
        print(f"  ✓ {name}")
        return True
    except ImportError as e:
        print(f"  ✗ {name}: {e}")
        return False


def check_spacy_model() -> bool:
    """Check if spaCy model loads."""
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("Jeffrey Epstein traveled with Ghislaine Maxwell.")
        ents = [(e.text, e.label_) for e in doc.ents]
        print(f"  ✓ spaCy en_core_web_sm (extracted: {ents})")
        return True
    except Exception as e:
        print(f"  ✗ spaCy model: {e}")
        return False


def check_parquet() -> bool:
    """Check if PyArrow can read parquet files."""
    try:
        import pyarrow.parquet as pq
        import pyarrow
        print(f"  ✓ pyarrow.parquet (version {pyarrow.__version__})")
        return True
    except Exception as e:
        print(f"  ✗ pyarrow.parquet: {e}")
        return False


def check_sqlite() -> bool:
    """Check SQLite with WAL mode."""
    try:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        wal = conn.execute("PRAGMA journal_mode").fetchone()[0]
        conn.close()
        print(f"  ✓ sqlite3 (version {sqlite3.sqlite_version}, mode: {wal})")
        return True
    except Exception as e:
        print(f"  ✗ sqlite3: {e}")
        return False


def check_data_dirs() -> bool:
    """Check data directories exist."""
    dirs = [
        "/mnt/data/epstein-project",
        "/mnt/data/epstein-project/raw-files",
        "/mnt/data/epstein-project/databases",
        "/mnt/data/epstein-project/hf-parquet",
    ]
    all_ok = True
    for d in dirs:
        if Path(d).exists():
            print(f"  ✓ {d}")
        else:
            print(f"  ⚠ {d} (not found — create with mkdir)")
            all_ok = False
    return all_ok


def check_scripts() -> bool:
    """Check our scripts are importable."""
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir.parent))
    
    scripts = ["tracker", "dashboard", "download_cdn", "metrics"]
    all_ok = True
    for s in scripts:
        try:
            importlib.import_module(f"scripts.{s}")
            print(f"  ✓ scripts.{s}")
        except Exception as e:
            print(f"  ✗ scripts.{s}: {e}")
            all_ok = False
    return all_ok


def main():
    print("\n" + "=" * 50)
    print("  Epstein Full — Environment Verification")
    print("=" * 50)
    
    results = {}
    
    print("\n--- Python ---")
    print(f"  Python {sys.version}")
    
    print("\n--- Core Dependencies ---")
    for mod, name in [
        ("spacy", "spaCy NLP"),
        ("fitz", "PyMuPDF (PDF extraction)"),
        ("pyarrow.parquet", "Apache Parquet"),
        ("pandas", "Pandas"),
        ("numpy", "NumPy"),
        ("scipy", "SciPy"),
        ("sklearn", "scikit-learn"),
        ("rich", "Rich (terminal UI)"),
        ("click", "Click (CLI)"),
        ("aiohttp", "aiohttp (async HTTP)"),
        ("playwright", "Playwright (browser)"),
        ("rapidfuzz", "rapidfuzz (fuzzy matching)"),
        ("insightface", "InsightFace (face recognition)"),
        ("cv2", "OpenCV"),
        ("jiwer", "jiwer (OCR eval)"),
        ("nervaluate", "nervaluate (NER eval)"),
        ("networkx", "NetworkX (graph)"),
        ("datasets", "HuggingFace Datasets"),
        ("huggingface_hub", "HuggingFace Hub"),
        ("gliner", "GLiNER (zero-shot NER)"),
        ("tqdm", "tqdm (progress)"),
    ]:
        results[name] = check_import(mod, name)
    
    print("\n--- Models ---")
    results["spaCy model"] = check_spacy_model()
    
    print("\n--- Data Formats ---")
    results["Parquet"] = check_parquet()
    results["SQLite"] = check_sqlite()
    
    print("\n--- Data Directories ---")
    results["Data dirs"] = check_data_dirs()
    
    print("\n--- Our Scripts ---")
    results["Scripts"] = check_scripts()
    
    # Summary
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print("\n" + "=" * 50)
    if passed == total:
        print(f"  ✓ ALL {total} CHECKS PASSED — Ready!")
    else:
        failed = total - passed
        print(f"  ⚠ {passed}/{total} passed, {failed} issues")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
