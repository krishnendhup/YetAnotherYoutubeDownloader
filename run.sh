#!/bin/bash

# YouTube Downloader Quick Start Script

echo "Starting YouTube Video Downloader..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if yt-dlp is installed, if not, install it
if ! python3 -c "import yt_dlp" 2>/dev/null; then
    echo "Installing yt-dlp..."
    pip install yt-dlp
fi

# Run the main application
python3 main.py
