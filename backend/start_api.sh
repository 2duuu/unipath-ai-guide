#!/bin/bash
# Quick start script for UniHub API

echo "🎓 UniHub API - Quick Start"
echo "============================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -r api_requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting API server..."
echo "   API will be available at: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the API
python api.py
