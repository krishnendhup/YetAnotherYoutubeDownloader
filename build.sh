#!/bin/bash

# Local Build Script for YouTube Downloader

echo "Building YouTube Downloader for current platform..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if PyInstaller is installed
if ! python3 -m pip show PyInstaller > /dev/null 2>&1; then
    echo "Installing PyInstaller..."
    pip install PyInstaller
fi

# Determine OS
OS_TYPE="$(uname -s)"

case "$OS_TYPE" in
    Darwin*)
        echo "Building for macOS..."
        pyinstaller --onefile --windowed \
            --name youtube-downloader \
            --icon assets/icon.icns \
            main.py
        echo "Build complete! App location: dist/youtube-downloader.app"
        ;;
    Linux*)
        echo "Building for Linux..."
        pyinstaller --onefile --windowed \
            --name youtube-downloader \
            --icon assets/icon.png \
            main.py
        echo "Build complete! Executable location: dist/youtube-downloader"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "Building for Windows..."
        pyinstaller --onefile --windowed \
            --name youtube-downloader \
            --icon assets/icon.ico \
            main.py
        echo "Build complete! Executable location: dist/youtube-downloader.exe"
        ;;
    *)
        echo "Unknown OS: $OS_TYPE"
        exit 1
        ;;
esac

echo ""
echo "Build directory: dist/"
