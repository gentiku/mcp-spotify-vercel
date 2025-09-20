#!/bin/bash
echo "=== Railway Startup Debug ==="
echo "PORT: $PORT"
echo "PWD: $(pwd)"
echo "Python version: $(python3 --version)"
echo "Files in directory:"
ls -la
echo "=== Starting uvicorn ==="
exec uvicorn app_minimal:app --host 0.0.0.0 --port $PORT --log-level info
