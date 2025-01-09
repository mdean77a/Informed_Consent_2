#!/bin/bash

# Start Qdrant in the background
echo "Starting Qdrant server..."
/qdrant/qdrant  &

# Run my chainlit app using uv  
echo "Starting Chainlit application..."
uv run chainlit run app.py --host 0.0.0.0 --port 7860

