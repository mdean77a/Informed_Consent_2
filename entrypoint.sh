#!/bin/bash
echo "Current directory: $(pwd)"
echo "Current path: $PATH"



# Specify the starting directory (e.g., root or home)
start_directory="../"

# Use find to locate 'uv'
found=$(find "$start_directory" -name "uv" 2>/dev/null)

if [ -n "$found" ]; then
    echo "'uv' found at:"
    echo "$found"
else
    echo "'uv' not found in $start_directory or its subdirectories"
fi


directory = "/"
# directory="../root/.local/bin"
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

