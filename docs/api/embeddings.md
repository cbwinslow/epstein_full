# Embeddings API Documentation

## Overview

REST API for generating text embeddings using nomic-embed-text-v2-moe model on Windows RTX3060 GPU.

## Base URL

```
http://<WINDOWS_IP>:8000
```

Replace `<WINDOWS_IP>` with the actual IP address of the Windows machine (e.g., `192.168.1.100`)

## Authentication

Currently no authentication (LAN-only access). In production, implement API key authentication.

## Endpoints

### GET /

Health check endpoint.

**Response:**
```json
{
  "service": "Embeddings API",
  "model": "nomic-ai/nomic-embed-text-v2-moe",
  "device": "cuda",
  "dimensions": 768
}
```

### GET /health

Health check endpoint with device status.

**Response:**
```json
{
  "status": "healthy",
  "device": "cuda"
}
```

### POST /embed

Generate embeddings for multiple texts in batch.

**Request Body:**
```json
{
  "texts": ["First article title", "Second article title"],
  "batch_size": 32
}
```

**Parameters:**
- `texts` (required): Array of strings to embed
- `batch_size` (optional): Batch size for processing (default: 32)

**Response:**
```json
{
  "embeddings": [
    [0.1, 0.2, 0.3, ...],
    [0.4, 0.5, 0.6, ...]
  ],
  "dimension": 768,
  "model": "nomic-ai/nomic-embed-text-v2-moe"
}
```

**Example:**
```bash
curl -X POST http://192.168.1.100:8000/embed \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Hello world", "Goodbye world"], "batch_size": 32}'
```

### POST /embed/title

Generate embedding for a single article title.

**Query Parameters:**
- `text` (required): Title text to embed

**Response:**
```json
{
  "embedding": [0.1, 0.2, 0.3, ...],
  "dimension": 768
}
```

**Example:**
```bash
curl -X POST "http://192.168.1.100:8000/embed/title?text=Jeffrey%20Epstein%20case"
```

### POST /embed/summary

Generate embedding for a single article summary.

**Query Parameters:**
- `text` (required): Summary text to embed

**Response:**
```json
{
  "embedding": [0.1, 0.2, 0.3, ...],
  "dimension": 768
}
```

**Example:**
```bash
curl -X POST "http://192.168.1.100:8000/embed/summary?text=This%20article%20discusses%20the%20Epstein%20case"
```

### POST /embed/content

Generate embedding for article content (full text).

**Query Parameters:**
- `text` (required): Content text to embed

**Response:**
```json
{
  "embedding": [0.1, 0.2, 0.3, ...],
  "dimension": 768
}
```

**Example:**
```bash
curl -X POST "http://192.168.1.100:8000/embed/content?text=Full%20article%20content%20goes%20here"
```

## Error Responses

### 400 Bad Request

Invalid request parameters.

```json
{
  "detail": "Error message"
}
```

### 500 Internal Server Error

Server error during embedding generation.

```json
{
  "detail": "CUDA out of memory"
}
```

## Rate Limiting

Currently no rate limiting (LAN-only). Recommended:
- 100 requests/second per client
- Batch requests for multiple texts

## Performance

- **Single embedding**: ~0.1-0.2 seconds
- **Batch of 32**: ~1-2 seconds
- **Throughput**: ~100-200 embeddings/second

## Model Information

**Model**: nomic-ai/nomic-embed-text-v2-moe
- **Dimensions**: 768
- **Architecture**: Mixture of Experts
- **Max Sequence Length**: 8192 tokens
- **License**: Apache 2.0
- **Compute**: Requires CUDA 11.8+ (RTX3060 compatible)

## Python Client

### Installation

```bash
pip install requests
```

### Usage

```python
import requests

class EmbeddingsClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
    
    def health(self) -> dict:
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def embed(self, texts: list, batch_size: int = 32) -> list:
        response = requests.post(
            f"{self.base_url}/embed",
            json={"texts": texts, "batch_size": batch_size}
        )
        return response.json()["embeddings"]
    
    def embed_title(self, text: str) -> list:
        response = requests.post(
            f"{self.base_url}/embed/title",
            params={"text": text}
        )
        return response.json()["embedding"]

# Usage
client = EmbeddingsClient("http://192.168.1.100:8000")
print(client.health())
embedding = client.embed_title("Jeffrey Epstein case")
print(len(embedding))  # 768
```

## Integration with PostgreSQL

### Store Embeddings

```python
import psycopg2
import requests

# Generate embedding
embedding = requests.post(
    "http://192.168.1.100:8000/embed/title",
    params={"text": "Article title"}
).json()["embedding"]

# Store in database
conn = psycopg2.connect("postgresql://user:pass@localhost:5432/epstein")
cur = conn.cursor()
cur.execute("""
    UPDATE media_news_articles
    SET title_embedding = %s
    WHERE id = %s
""", (embedding, article_id))
conn.commit()
```

### Semantic Search

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
- Verify IP address
- Ensure server is running

### CUDA Out of Memory
- Reduce batch size
- Process fewer texts at once
- Restart server

### Slow Performance
- Check GPU utilization (nvidia-smi on Windows)
- Verify CUDA is being used
- Check network latency
- Use batch processing

## Security Considerations

**Current**: No authentication (LAN-only)

**Production Recommendations**:
1. Add API key authentication
2. Use HTTPS/TLS
3. Implement rate limiting
4. Add request logging
5. Use VPN for remote access

## Monitoring

### Health Checks

```bash
# Check if service is running
curl http://192.168.1.100:8000/health

# Expected response
{"status": "healthy", "device": "cuda"}
```

### GPU Monitoring (Windows)

```powershell
nvidia-smi
```

### Logs

Server logs output to console. For production, implement file logging:

```python
import logging

logging.basicConfig(
    filename='embeddings_server.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```
