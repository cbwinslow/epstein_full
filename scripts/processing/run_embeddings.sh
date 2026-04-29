#!/bin/bash
cd /home/cbwinslow/workspace/epstein/scripts/processing
export OLLAMA_EMBED_ENDPOINT="${OLLAMA_EMBED_ENDPOINT:-http://192.168.4.25:11343/api/embed}"
export OLLAMA_EMBED_MODEL="${OLLAMA_EMBED_MODEL:-nomic-embed-text:latest}"
export OLLAMA_EMBED_COLUMN="${OLLAMA_EMBED_COLUMN:-rtx3060_embedding}"
export OLLAMA_EMBED_DIMS="${OLLAMA_EMBED_DIMS:-768}"
export OLLAMA_EMBED_MAX_TEXT="${OLLAMA_EMBED_MAX_TEXT:-1500}"
exec /usr/bin/python3 rtx3060_embeddings.py >> /tmp/rtx3060_embeddings.log 2>&1
