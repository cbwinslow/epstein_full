#!/bin/bash
cd /home/cbwinslow/workspace/epstein/scripts/processing
exec /usr/bin/python3 rtx3060_embeddings.py >> /tmp/rtx3060_embeddings.log 2>&1
