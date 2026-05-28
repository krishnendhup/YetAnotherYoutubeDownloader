#!/bin/bash
set -e

echo "Building YouTube Downloader for macOS..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Step 1: Installing dependencies...${NC}"
pip install -r requirements.txt
pip install dmg

echo -e "${BLUE}Step 2: Building with PyInstaller...${NC}"
pyinstaller --onefile \
    --windowed \
    --name="YouTube-Downloader" \
    --icon=icon.icns \
    --osx-bundle-identifier="com.youtube.downloader" \
    --add-data=".:." \
    main.py

echo -e "${BLUE}Step 3: Creating DMG file...${NC}"
mkdir -p dist/dmg_temp
cp -r "dist/YouTube-Downloader.app" dist/dmg_temp/

# Create a symlink to Applications folder
ln -s /Applications dist/dmg_temp/Applications

# Create DMG file
dmg create \
    --source dist/dmg_temp \
    --destination "dist/YouTube-Downloader.dmg" \
    --volname "YouTube Downloader" \
    --icon icon.icns

echo -e "${GREEN}✓ Build complete!${NC}"
echo -e "${GREEN}Output: dist/YouTube-Downloader.dmg${NC}"

# Cleanup
rm -rf dist/dmg_temp
