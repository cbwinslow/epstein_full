
# Windows Embeddings Endpoint Setup
# Run as Administrator

# 1. Install Python 3.11+ if not installed
# Download from: https://www.python.org/downloads/

# 2. Install CUDA toolkit (if using NVIDIA GPU)
# Download from: https://developer.nvidia.com/cuda-downloads

# 3. Create virtual environment
python -m venv C:\epstein-embeddings
.\epstein-embeddings\Scripts\Activate.ps1

# 4. Install dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers sentence-transformers fastapi uvicorn psycopg2-binary
pip install numpy pandas tqdm aiofiles

# 5. Download embedding model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('nomic-ai/nomic-embed-text-v2-moe', trust_remote_code=True)"

# 6. Run the embedding server
python embeddings_server.py
