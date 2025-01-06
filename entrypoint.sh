#!/bin/bash

# Start Qdrant in the background
echo "Starting Qdrant server..."
/qdrant/qdrant  &

# Wait for Qdrant to be ready
# echo "Waiting for Qdrant to be ready..."
# until curl -s http://localhost:6333/health | grep '"status":"ok"'; do
#   sleep 1
# done
echo "Qdrant is ready!"

# Start Chainlit application using Uvicorn
echo "Starting Chainlit application..."
uv run chainlit run app.py --host 0.0.0.0 --port 7860

