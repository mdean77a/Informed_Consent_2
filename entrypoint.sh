#!/bin/bash
echo "Current directory: $(pwd)"
echo "Current path: $PATH"

directory="../root/.local/bin"
if [ -d "$directory" ];
then
    echo "Directory exists: $directory"
    echo "Files in $directory:"
    find "$directory" -type f
else
    echo "Directory does not exist: $directory"
fi
# Start Qdrant in the background
echo "Starting Qdrant server..."
/qdrant/qdrant  &

# Run my chainlit app using uv  
echo "Starting Chainlit application..."
uv run chainlit run app.py --host 0.0.0.0 --port 7860

