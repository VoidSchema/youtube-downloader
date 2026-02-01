#!/bin/bash

# YouTube Downloader CLI Environment Activation Script

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "📥 Please run setup.sh first:"
    echo "   bash setup.sh"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

echo "🌍 Virtual environment activated!"
echo "📹 Usage examples:"
echo "   python main.py 'https://youtube.com/watch?v=XXXX'"
echo "   python main.py 'URL' --audio-only"
echo "   python main.py 'URL' --quality 1080"
echo "   python main.py 'PLAYLIST_URL' --playlist"