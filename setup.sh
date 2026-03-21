#!/bin/bash
# =============================================================================
# Epstein Full — Development Environment Setup
# =============================================================================
#
# One-command bootstrap for the Epstein Files Analysis Pipeline.
# Installs uv, creates venv, installs all dependencies, verifies setup.
#
# Usage:
#   ./setup.sh              # Full setup (core + GPU deps)
#   ./setup.sh --core       # Core only (no GPU deps)
#   ./setup.sh --verify     # Just verify existing setup
#   ./setup.sh --docker     # Setup inside Docker container
#
# Requirements:
#   - Python 3.12 (system or via uv)
#   - ~10GB disk for dependencies
#   - NVIDIA GPU + CUDA 11.4 (for GPU deps, optional)
#
# =============================================================================

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
VENV_DIR="$PROJECT_DIR/.venv"
UV="$HOME/.local/bin/uv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log() { echo -e "${CYAN}[setup]${NC} $1"; }
ok()  { echo -e "${GREEN}  ✓${NC} $1"; }
warn(){ echo -e "${YELLOW}  ⚠${NC} $1"; }
err() { echo -e "${RED}  ✗${NC} $1"; }

# =============================================================================
# Parse arguments
# =============================================================================
MODE="full"
while [[ $# -gt 0 ]]; do
    case $1 in
        --core)  MODE="core"; shift ;;
        --verify) MODE="verify"; shift ;;
        --docker) MODE="docker"; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# =============================================================================
# Step 1: Install uv
# =============================================================================
install_uv() {
    log "Installing uv..."
    if command -v "$UV" &>/dev/null; then
        ok "uv already installed: $($UV --version)"
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
        ok "uv installed: $($UV --version)"
    fi
    export PATH="$HOME/.local/bin:$PATH"
}

# =============================================================================
# Step 2: Create virtual environment
# =============================================================================
create_venv() {
    log "Creating virtual environment..."
    if [ -d "$VENV_DIR" ]; then
        warn "Removing existing .venv"
        rm -rf "$VENV_DIR"
    fi
    "$UV" venv --python 3.12 "$VENV_DIR"
    ok "Virtual environment created at $VENV_DIR"
}

# =============================================================================
# Step 3: Install dependencies
# =============================================================================
install_deps() {
    log "Installing dependencies from pyproject.toml..."
    
    # Core deps
    "$UV" pip install -e "$PROJECT_DIR" 2>&1 | tail -3
    ok "Core dependencies installed"
    
    # GPU deps (if not --core mode)
    if [ "$MODE" = "full" ] || [ "$MODE" = "docker" ]; then
        log "Installing GPU dependencies..."
        "$UV" pip install onnxruntime-gpu>=1.16 2>/dev/null && ok "onnxruntime-gpu installed" || warn "onnxruntime-gpu not available (CPU fallback)"
    fi
}

# =============================================================================
# Step 4: Install spaCy model
# =============================================================================
install_spacy() {
    log "Installing spaCy model..."
    "$VENV_DIR/bin/python" -m spacy download en_core_web_sm 2>&1 | tail -1
    ok "spaCy en_core_web_sm installed"
}

# =============================================================================
# Step 5: Install Playwright browsers
# =============================================================================
install_playwright() {
    log "Installing Playwright Chromium..."
    "$VENV_DIR/bin/playwright" install chromium 2>&1 | tail -1
    "$VENV_DIR/bin/playwright" install-deps chromium 2>&1 | tail -1
    ok "Playwright Chromium installed"
}

# =============================================================================
# Step 6: Install system dependencies
# =============================================================================
install_system_deps() {
    log "Installing system dependencies..."
    
    # Check if we can use apt
    if command -v apt-get &>/dev/null; then
        sudo apt-get install -y \
            sqlite3 \
            aria2 \
            curl \
            jq \
            build-essential \
            libgl1 \
            libglib2.0-0 2>/dev/null || warn "Some system deps may need manual install"
        ok "System dependencies installed"
    else
        warn "apt-get not available — install manually: sqlite3, aria2, curl, jq"
    fi
}

# =============================================================================
# Step 7: Verify installation
# =============================================================================
verify() {
    log "Verifying installation..."
    
    local errors=0
    
    # Python version
    PY_VER=$("$VENV_DIR/bin/python" --version 2>&1 | awk '{print $2}')
    if [[ "$PY_VER" == 3.12* ]]; then
        ok "Python $PY_VER"
    else
        err "Python $PY_VER (expected 3.12.x)"
        errors=$((errors + 1))
    fi
    
    # Critical imports
    for pkg in spacy pymupdf pyarrow rich click numpy scipy sklearn rapidfuzz insightface cv2; do
        if "$VENV_DIR/bin/python" -c "import $pkg" 2>/dev/null; then
            ok "$pkg"
        else
            err "$pkg import failed"
            errors=$((errors + 1))
        fi
    done
    
    # spaCy model
    if "$VENV_DIR/bin/python" -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
        ok "spaCy en_core_web_sm"
    else
        err "spaCy model not loaded"
        errors=$((errors + 1))
    fi
    
    # Playwright
    if "$VENV_DIR/bin/python" -c "import playwright" 2>/dev/null; then
        ok "playwright"
    else
        err "playwright import failed"
        errors=$((errors + 1))
    fi
    
    # PyArrow (Apache Parquet)
    if "$VENV_DIR/bin/python" -c "import pyarrow.parquet" 2>/dev/null; then
        ok "pyarrow.parquet (Apache Parquet reader)"
    else
        err "pyarrow.parquet failed"
        errors=$((errors + 1))
    fi
    
    # SQLite
    if "$VENV_DIR/bin/python" -c "import sqlite3; print(sqlite3.sqlite_version)" 2>/dev/null; then
        ok "sqlite3"
    else
        err "sqlite3 failed"
        errors=$((errors + 1))
    fi
    
    # System tools
    for tool in aria2c curl jq sqlite3; do
        if command -v $tool &>/dev/null; then
            ok "$tool"
        else
            err "$tool not found"
            errors=$((errors + 1))
        fi
    done
    
    echo ""
    if [ $errors -eq 0 ]; then
        echo -e "${GREEN}============================================${NC}"
        echo -e "${GREEN}  ALL CHECKS PASSED — Environment ready!${NC}"
        echo -e "${GREEN}============================================${NC}"
        echo ""
        echo "  Activate:  source $VENV_DIR/bin/activate"
        echo "  Dashboard: python scripts/dashboard.py"
        echo "  Tracker:   python scripts/tracker.py watch"
        echo ""
    else
        echo -e "${RED}============================================${NC}"
        echo -e "${RED}  $errors CHECK(S) FAILED${NC}"
        echo -e "${RED}============================================${NC}"
        exit 1
    fi
}

# =============================================================================
# Docker-specific setup
# =============================================================================
docker_setup() {
    log "Docker environment detected"
    install_uv
    create_venv
    install_deps
    install_spacy
    verify
}

# =============================================================================
# Main
# =============================================================================
main() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Epstein Full — Environment Setup           ║${NC}"
    echo -e "${CYAN}║  Mode: $(printf '%-38s' $MODE)║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
    echo ""
    
    cd "$PROJECT_DIR"
    
    case $MODE in
        verify)
            verify
            ;;
        docker)
            docker_setup
            ;;
        *)
            install_uv
            install_system_deps
            create_venv
            install_deps
            install_spacy
            install_playwright
            verify
            ;;
    esac
}

main
