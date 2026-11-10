#!/usr/bin/env bash
# Quick start script for the UniHub API (macOS, Linux, Git Bash on Windows).
# Works from any directory:  ./backend/start_api.sh   or   cd backend && ./start_api.sh
# On Windows PowerShell use start_api.ps1 instead.
set -e

# Always run from this script's directory (backend/), wherever it was called from.
cd "$(dirname "$0")"

if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi
echo "Python found: $($PYTHON --version)"

if [ ! -d "venv" ]; then
    echo "Creating virtual environment in backend/venv..."
    "$PYTHON" -m venv venv
fi

# venv layout differs: bin/ on macOS/Linux, Scripts/ on Windows (Git Bash).
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    source venv/Scripts/activate
fi

echo "Installing dependencies..."
python -m pip install -q -r requirements.txt

echo ""
echo "Starting API server..."
echo "   API:  http://localhost:8084"
echo "   Docs: http://localhost:8084/docs"
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --host 0.0.0.0 --port 8084
