#!/bin/bash
# Start Qdrant in the background
echo "Starting Qdrant server..."
/qdrant/qdrant  &
mkdir -p /home/user/.local/bin
echo "Qdrant is ready!"

curl -LsSf https://astral.sh/uv/install.sh | sh
# Start Chainlit application using Uvicorn
echo "Starting Chainlit application..."
echo "Current path: $PATH"
uv run chainlit run app.py --host 0.0.0.0 --port 7860

