#!/bin/bash

# YouTube Downloader CLI Setup Script
echo "🚀 Setting up YouTube Downloader CLI..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install dependencies"
    exit 1
fi

# Create output directories
echo "📁 Creating output directories..."
mkdir -p videos
mkdir -p audio
mkdir -p downloads

echo "✅ Setup complete!"
echo ""
echo "🌍 To activate the environment, run:"
echo "   source activate.sh"
echo ""
echo "📹 To download a video, run:"
echo "   python main.py 'https://youtube.com/watch?v=XXXX'"
echo ""