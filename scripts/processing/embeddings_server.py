
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
