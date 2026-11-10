#!/bin/bash
# Quick start script for the UniHub API. Run from the backend/ directory.
set -e

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi
echo "Python found: $(python3 --version)"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting API server..."
echo "   API:  http://localhost:8084"
echo "   Docs: http://localhost:8084/docs"
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn app.main:app --host 0.0.0.0 --port 8084
