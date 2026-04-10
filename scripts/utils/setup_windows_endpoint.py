#!/usr/bin/env python3
"""
Windows endpoint configuration for embeddings generation
This script creates the configuration and API endpoint spec
"""

import json
import logging
import os

logging.basicConfig(level=logging.INFO)

CONFIG = {
    "endpoint": {
        "host": "0.0.0.0",
        "port": 8000,
        "auth_token": "epstein-embeddings-2024"
    },
    "models": {
        "embedding": {
            "model_name": "nomic-ai/nomic-embed-text-v2-moe",
            "device": "cuda",
            "batch_size": 32,
            "max_length": 8192,
            "trust_remote_code": True
        },
        "reranker": {
            "model_name": "jinaai/jina-reranker-v2-base-multilingual",
            "device": "cuda"
        }
    },
    "postgres": {
        "host": "windows-host",  # User will update this
        "port": 5432,
        "user": "cbwinslow",
        "password": "123qweasd",
        "dbname": "epstein"
    },
    "batch": {
        "chunk_size": 512,
        "overlap": 128,
        "max_workers": 4
    }
}


def generate_windows_script():
    """Generate Windows PowerShell setup script."""
    script = '''
# Windows Embeddings Endpoint Setup
# Run as Administrator

# 1. Install Python 3.11+ if not installed
# Download from: https://www.python.org/downloads/

# 2. Install CUDA toolkit (if using NVIDIA GPU)
# Download from: https://developer.nvidia.com/cuda-downloads

# 3. Create virtual environment
python -m venv C:\\epstein-embeddings
.\\epstein-embeddings\\Scripts\\Activate.ps1

# 4. Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers sentence-transformers fastapi uvicorn psycopg2-binary
pip install numpy pandas tqdm aiofiles

# 5. Download embedding model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('nomic-ai/nomic-embed-text-v2-moe', trust_remote_code=True)"

# 6. Run the embedding server
python embeddings_server.py
'''
    return script


def generate_embeddings_server():
    """Generate the FastAPI embeddings server code."""
    code = '''
"""
Windows Embeddings Server for Epstein Data
Run this on your Windows machine with GPU
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
import torch
import psycopg2
from sentence_transformers import SentenceTransformer
import numpy as np
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Epstein Embeddings API")
security = HTTPBearer()

# Load config
AUTH_TOKEN = "epstein-embeddings-2024"

# Load model
logger.info("Loading embedding model...")
model = SentenceTransformer(
    "nomic-ai/nomic-embed-text-v2-moe",
    trust_remote_code=True,
    device="cuda" if torch.cuda.is_available() else "cpu"
)
logger.info(f"Model loaded on {model.device}")

# DB connection
PG_CONFIG = {
    "host": "localhost",  # Update to your Linux host IP
    "port": 5432,
    "user": "cbwinslow",
    "password": "123qweasd",
    "dbname": "epstein"
}

class EmbedRequest(BaseModel):
    texts: List[str]
    batch_size: Optional[int] = 32

class EmbedResponse(BaseModel):
    embeddings: List[List[float]]
    model: str
    device: str
    count: int

class SearchRequest(BaseModel):
    query: str
    top_k: int = 10

class SearchResponse(BaseModel):
    results: List[dict]

@app.post("/embed", response_model=EmbedResponse)
async def embed_texts(
    request: EmbedRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Generate embeddings for text batch."""
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    embeddings = model.encode(
        request.texts,
        batch_size=request.batch_size,
        show_progress_bar=True,
        convert_to_numpy=True
    )
    
    return EmbedResponse(
        embeddings=embeddings.tolist(),
        model="nomic-embed-text-v2-moe",
        device=str(model.device),
        count=len(request.texts)
    )

@app.post("/search", response_model=SearchResponse)
async def semantic_search(
    request: SearchRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Semantic search using pre-computed embeddings."""
    if credentials.credentials != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Generate query embedding
    query_emb = model.encode([request.query], convert_to_numpy=True)[0]
    
    # Connect to DB and search (requires embeddings to be stored)
    conn = psycopg2.connect(**PG_CONFIG)
    with conn.cursor() as cur:
        # This requires pgvector extension
        cur.execute("""
            SELECT id, document_id, filename, content,
                   embedding <=> %s::vector AS distance
            FROM documents_content
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """, (query_emb.tolist(), query_emb.tolist(), request.top_k))
        
        results = []
        for row in cur.fetchall():
            results.append({
                "id": row[0],
                "document_id": row[1],
                "filename": row[2],
                "content": row[3][:500],
                "distance": float(row[4])
            })
    
    conn.close()
    return SearchResponse(results=results)

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "model": "nomic-embed-text-v2-moe",
        "device": str(model.device),
        "cuda_available": torch.cuda.is_available()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    return code


def main():
    """Generate all Windows endpoint files."""
    logging.info("Generating Windows endpoint files...")
    
    # Save config
    config_path = "/home/cbwinslow/workspace/epstein/windows_endpoint_config.json"
    with open(config_path, 'w') as f:
        json.dump(CONFIG, f, indent=2)
    logging.info(f"✓ Config saved to {config_path}")
    
    # Save PowerShell setup script
    ps_path = "/home/cbwinslow/workspace/epstein/scripts/windows_setup.ps1"
    with open(ps_path, 'w') as f:
        f.write(generate_windows_script())
    logging.info(f"✓ PowerShell setup saved to {ps_path}")
    
    # Save embeddings server
    server_path = "/home/cbwinslow/workspace/epstein/scripts/embeddings_server.py"
    with open(server_path, 'w') as f:
        f.write(generate_embeddings_server())
    logging.info(f"✓ Embeddings server saved to {server_path}")
    
    # Print instructions
    print("\n" + "=" * 60)
    print("WINDOWS ENDPOINT SETUP")
    print("=" * 60)
    print("\n1. Copy these files to your Windows machine:")
    print(f"   - {server_path}")
    print(f"   - {ps_path}")
    print(f"   - {config_path}")
    print("\n2. On Windows, run PowerShell as Administrator:")
    print("   .\\scripts\\windows_setup.ps1")
    print("\n3. Update postgres host in config to your Linux IP")
    print("\n4. Start the server:")
    print("   python embeddings_server.py")
    print("\n5. From this Linux machine, test the endpoint:")
    print("   curl http://<WINDOWS_IP>:8000/health")
    print("=" * 60)


if __name__ == "__main__":
    main()
