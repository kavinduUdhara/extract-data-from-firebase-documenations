#!/bin/bash
# Setup script for Firebase Documentation Extractor

echo "🔥 Firebase Documentation Extractor Setup"
echo "=========================================="

# Check if Python is installed
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python found: $($PYTHON_CMD --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv .venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

echo "✅ Virtual environment activated"

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo "🎉 Setup complete!"
echo ""
echo "To use the tool:"
echo "1. Activate the virtual environment:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "   source .venv/Scripts/activate"
else
    echo "   source .venv/bin/activate"
fi
echo "2. Run the extractor:"
echo "   python firebase_docs_extractor.py \"<FIREBASE_URL>\""
echo ""
echo "Example:"
echo "   python firebase_docs_extractor.py \"https://firebase.google.com/docs/ai-logic/get-started?api=vertex\""
