# Embeddings Processing

## Overview

The embeddings processing agent generates vector embeddings for news articles, documents, and other content to enable semantic search and similarity analysis.

## Model

**Model**: `nomic-ai/nomic-embed-text-v2-moe`
- **Dimensions**: 768
- **Matryoshka**: 256-dim support
- **Architecture**: Mixture of Experts
- **License**: Apache 2.0

## GPU Requirements

### Server GPU (Tesla K80/K40m) - INCOMPATIBLE
- **Issue**: Tesla K80 compute capability 3.7 is too old for nomic model
- **Error**: "no kernel image is available for execution on the device"
- **Workaround**: Use CPU fallback (slow)

### Windows GPU (RTX3060) - RECOMMENDED
- **Compute Capability**: 8.6 (compatible)
- **VRAM**: 12GB (sufficient for 768-dim embeddings)
- **Performance**: ~10-20x faster than CPU

## Windows GPU Embeddings Endpoint

### Architecture

The embeddings endpoint runs on the Windows machine with RTX3060 GPU and is accessible from the Linux server via LAN.

```
Linux Server (cbwinslow/workspace/epstein)
    ↓ HTTP API
Windows Machine (RTX3060 GPU)
    └── Embeddings Server (FastAPI + CUDA)
```

### Setup Instructions

#### 1. Windows Machine Setup

```powershell
# Install Python 3.12
# Create virtual environment
python -m venv embeddings_env
embeddings_env\Scripts\activate

# Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install fastapi uvicorn sentence-transformers
pip install python-multipart
```

#### 2. Create Embeddings Server

Save as `embeddings_server.py` on Windows:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import List, Optional

app = FastAPI(title="Embeddings API", version="1.0.0")

# Load model on GPU
model = SentenceTransformer('nomic-ai/nomic-embed-text-v2-moe', 
                          trust_remote_code=True,
                          device='cuda')

class EmbeddingRequest(BaseModel):
    texts: List[str]
    batch_size: Optional[int] = 32

class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]
    dimension: int
    model: str

@app.get("/")
async def root():
    return {
        "service": "Embeddings API",
        "model": "nomic-ai/nomic-embed-text-v2-moe",
        "device": str(model.device),
        "dimensions": 768
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "device": str(model.device)}

@app.post("/embed", response_model=EmbeddingResponse)
async def embed(request: EmbeddingRequest):
    try:
        embeddings = model.encode(
            request.texts,
            batch_size=request.batch_size,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        return EmbeddingResponse(
            embeddings=embeddings.tolist(),
            dimension=embeddings.shape[1],
            dimension=768,
            model="nomic-ai/nomic-embed-text-v2-moe"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/embed/title")
async def embed_title(text: str):
    """Generate embedding for article title"""
    embedding = model.encode(text, show_progress_bar=False)
    return {"embedding": embedding.tolist(), "dimension": 768}

@app.post("/embed/summary")
async def embed_summary(text: str):
    """Generate embedding for article summary"""
    embedding = model.encode(text, show_progress_bar=False)
    return {"embedding": embedding.tolist(), "dimension": 768}

@app.post("/embed/content")
async def embed_content(text: str):
    """Generate embedding for article content"""
    embedding = model.encode(text, show_progress_bar=False)
    return {"embedding": embedding.tolist(), "dimension": 768}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 3. Start Server on Windows

```powershell
# Allow network access in Windows Firewall
# Or run with admin privileges
python embeddings_server.py
```

Server will run on `http://0.0.0.0:8000`

#### 4. Get Windows IP Address

```powershell
ipconfig
```

Note the IPv4 address (e.g., `192.168.1.100`)

#### 5. Update Linux Client

Create `scripts/embeddings_client.py` on Linux server:

```python
import requests
import psycopg2
from typing import List, Optional

class EmbeddingsClient:
    """Client for Windows GPU embeddings endpoint"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        
    def health(self) -> dict:
        """Check if endpoint is healthy"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def embed(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        response = requests.post(
            f"{self.base_url}/embed",
            json={"texts": texts, "batch_size": batch_size}
        )
        return response.json()["embeddings"]
    
    def embed_title(self, text: str) -> List[float]:
        """Generate embedding for title"""
        response = requests.post(
            f"{self.base_url}/embed/title",
            params={"text": text}
        )
        return response.json()["embedding"]
    
    def embed_summary(self, text: str) -> List[float]:
        """Generate embedding for summary"""
        response = requests.post(
            f"{self.base_url}/embed/summary",
            params={"text": text}
        )
        return response.json()["embedding"]
    
    def embed_content(self, text: str) -> List[float]:
        """Generate embedding for content"""
        response = requests.post(
            f"{self.base_url}/embed/content",
            params={"text": text}
        )
        return response.json()["embedding"]

# Usage
client = EmbeddingsClient("http://192.168.1.100:8000")
print(client.health())
```

#### 6. Generate Embeddings for Articles

Create `scripts/generate_news_embeddings_remote.py`:

```python
import requests
import psycopg2
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows GPU endpoint
EMBEDDINGS_URL = "http://192.168.1.100:8000"  # Update with Windows IP

def get_articles_without_embeddings(conn, limit=1000):
    """Get articles that don't have embeddings yet"""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, title, summary, content
        FROM media_news_articles
        WHERE title_embedding IS NULL
        AND title IS NOT NULL
        ORDER BY collected_at DESC
        LIMIT %s
    """, (limit,))
    return cur.fetchall()

def update_article_embeddings(conn, article_id, title_emb, summary_emb, content_emb):
    """Update article with embeddings"""
    cur = conn.cursor()
    cur.execute("""
        UPDATE media_news_articles
        SET title_embedding = %s,
            summary_embedding = %s,
            content_embedding = %s
        WHERE id = %s
    """, (title_emb, summary_emb, content_emb, article_id))
    conn.commit()

def main():
    logger.info("Connecting to embeddings endpoint...")
    try:
        health = requests.get(f"{EMBEDDINGS_URL}/health").json()
        logger.info(f"Endpoint healthy: {health}")
    except Exception as e:
        logger.error(f"Cannot connect to embeddings endpoint: {e}")
        return
    
    conn = psycopg2.connect('postgresql://cbwinslow:123qweasd@localhost:5432/epstein')
    
    articles = get_articles_without_embeddings(conn, limit=1000)
    logger.info(f"Found {len(articles)} articles to process")
    
    processed = 0
    for i, (article_id, title, summary, content) in enumerate(articles, 1):
        try:
            # Generate embeddings via Windows GPU
            title_emb = requests.post(
                f"{EMBEDDINGS_URL}/embed/title",
                params={"text": title}
            ).json()["embedding"]
            
            summary_emb = None
            if summary:
                summary_emb = requests.post(
                    f"{EMBEDDINGS_URL}/embed/summary",
                    params={"text": summary}
                ).json()["embedding"]
            
            content_emb = None
            if content and len(content) > 100:
                content_emb = requests.post(
                    f"{EMBEDDINGS_URL}/embed/content",
                    params={"text": content}
                ).json()["embedding"]
            
            # Update database
            update_article_embeddings(conn, article_id, title_emb, summary_emb, content_emb)
            processed += 1
            
            if i % 10 == 0:
                logger.info(f"Progress: {i}/{len(articles)} processed")
                
        except Exception as e:
            logger.error(f"Error processing article {article_id}: {e}")
    
    conn.close()
    logger.info(f"Complete: {processed} articles processed")

if __name__ == '__main__':
    main()
```

#### 7. Run Embedding Generation

```bash
python3 scripts/generate_news_embeddings_remote.py
```

### Network Configuration

#### Windows Firewall
```powershell
# Allow port 8000
New-NetFirewallRule -DisplayName "Embeddings API" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

#### Linux to Windows Connection Test
```bash
# From Linux server
curl http://192.168.1.100:8000/health
```

### Performance

- **CPU (Tesla K80)**: ~1-2 seconds per embedding (incompatible)
- **CPU (Linux)**: ~5-10 seconds per embedding
- **GPU (RTX3060)**: ~0.1-0.2 seconds per embedding (50x faster)

### Batch Processing

For large batches, use the batch endpoint:

```python
# Get 100 articles
texts = [article.title for article in articles]
embeddings = client.embed(texts, batch_size=32)
```

## Database Schema

Embeddings are stored in `media_news_articles`:

```sql
ALTER TABLE media_news_articles 
ADD COLUMN title_embedding vector(768),
ADD COLUMN summary_embedding vector(768),
ADD COLUMN content_embedding vector(768);

CREATE INDEX idx_news_title_embedding 
ON media_news_articles USING ivfflat(title_embedding vector_cosine_ops);
```

## Semantic Search

Once embeddings are generated, use pgvector for semantic search:

```sql
-- Find similar articles
SELECT id, title, 
       1 - (title_embedding <=> '[0.1,0.2,...]'::vector) as similarity
FROM media_news_articles
ORDER BY title_embedding <=> '[0.1,0.2,...]'::vector
LIMIT 10;
```

## Troubleshooting

### Connection Refused
- Check Windows firewall settings
- Verify Windows IP address
- Ensure server is running on Windows

### CUDA Out of Memory
- Reduce batch size
- Use smaller model (e.g., all-MiniLM-L6-v2)
- Process articles in smaller batches

### Slow Performance
- Verify GPU is being used (check nvidia-smi on Windows)
- Check network latency between Linux and Windows
- Use batch processing for multiple texts
