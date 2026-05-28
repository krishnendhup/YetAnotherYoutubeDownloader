# Building YouTube Downloader

This guide explains how to build standalone executables that bundle all Python dependencies, including `yt-dlp`.

## What Gets Bundled

✅ Python runtime
✅ All pip dependencies (yt-dlp, tkinter, etc.)
✅ Your application code
✅ No need for users to install Python or pip

## Quick Start

### macOS (DMG file)
```bash
python3 build.py
# Creates: dist/YouTube-Downloader.dmg
```

### Windows (EXE file)
```cmd
python build.py
# Creates: dist/YouTube-Downloader.exe
```

### Linux
```bash
python3 build.py
# Creates: dist/YouTube-Downloader (executable)
```

## Detailed Instructions

### Prerequisites
- Python 3.7+ installed
- Git (optional, for version control)

### macOS Build

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build DMG:**
   ```bash
   python3 build.py
   ```

3. **Distribute:**
   - Share `dist/YouTube-Downloader.dmg` with users
   - Users double-click to install the .app bundle

### Windows Build

1. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

2. **Build EXE:**
   ```cmd
   python build.py
   ```

3. **Distribute:**
   - Share `dist/YouTube-Downloader.exe` with users
   - Optionally create an installer using NSIS or Inno Setup

4. **Optional: Advanced Installer (NSIS)**
   ```cmd
   pip install nsis
   # Then use NSIS to create a professional installer
   ```

## Build Options

### Custom Build with PyInstaller

For advanced customization, use PyInstaller directly:

```bash
pyinstaller --onefile \
    --windowed \
    --name=YouTube-Downloader \
    --icon=icon.icns \
    main.py
```

### Adding an Icon

1. **macOS**: Create `icon.icns` and place in project root
2. **Windows**: Create `icon.ico` and place in project root

The build script will automatically use these if present.

## Troubleshooting

### "yt-dlp command not found" after building

This usually means:
- yt-dlp wasn't bundled correctly
- Solution: Rebuild with `python3 build.py`

### DMG creation fails on macOS

Install the dmg tool:
```bash
pip install dmg
```

### PyInstaller not found

Install all dependencies:
```bash
pip install -r requirements.txt
```

## File Structure After Build

```
dist/
├── YouTube-Downloader.app/        # macOS app bundle
│   └── Contents/
│       ├── MacOS/
│       │   └── YouTube-Downloader  # Executable
│       └── Resources/
├── YouTube-Downloader.dmg         # macOS installer (drag-and-drop)
├── YouTube-Downloader.exe         # Windows executable
├── build/                          # PyInstaller build files
└── YouTube-Downloader.spec        # PyInstaller spec file
```

## Release Checklist

- [ ] Test the built executable on target OS
- [ ] Verify yt-dlp works inside the bundled app
- [ ] Test downloading a video in the bundled app
- [ ] Version bump in `setup.py` and `main.py`
- [ ] Create release notes
- [ ] Upload to GitHub releases or website

## Technical Details

### How PyInstaller Works

1. **Analysis**: Scans your code for imports
2. **Compilation**: Bundles Python, stdlib, and dependencies
3. **Collection**: Packages everything into a single file or directory
4. **Encryption**: Optional - encrypts Python bytecode

### Why "One File" Build?

- Simpler distribution
- Single download/installer
- Harder to modify
- Slightly slower startup

### If You Need Faster Startup

Use `--onedir` instead of `--onefile`:

```bash
pyinstaller --onedir --windowed --name YouTube-Downloader main.py
```

This creates a directory with all files, faster to load but more files to distribute.

## Advanced: Custom Packaging

### macOS: Create Custom DMG with Background

```bash
# After building the app, customize the DMG
# Use Apple Disk Utility or dmg tool for background images
```

### Windows: Create MSI Installer

```bash
pip install cx_Freeze
cxfreeze main.py --target-dir dist --target-name YouTube-Downloader.exe
```

## Support

If you encounter issues:
1. Check the [PyInstaller documentation](https://pyinstaller.org/)
2. Review [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp)
3. Check console output for error messages
