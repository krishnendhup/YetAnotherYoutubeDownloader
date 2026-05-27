# GitHub CI/CD Setup Guide

This project includes automated GitHub Actions workflows to build and package the YouTube Downloader application for Linux, Windows, and macOS ARM.

## Setup Instructions

### 1. Initialize Git Repository

```bash
cd /Users/krishnendhu/Code/Youtube\ downloader
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/Youtube-downloader.git
git push -u origin main
```

### 2. Create Releases via Tags

To trigger the GitHub Actions workflow and create releases:

```bash
# Create and push a version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This will:
- Build the app on all three platforms (Ubuntu, Windows, macOS ARM)
- Create a GitHub Release with downloadable executables

### 3. Build Locally (Optional)

To build locally before releasing:

```bash
# Make build script executable
chmod +x build.sh

# Run the build script
./build.sh
```

## Workflow Details

The `.github/workflows/build.yml` file defines:

- **Trigger**: Activates when you push a git tag (v*) or manually via `workflow_dispatch`
- **Platforms**:
  - Ubuntu latest → Linux executable
  - Windows latest → Windows .exe
  - macOS 14 (ARM64) → macOS ARM executable

- **Build Process**:
  1. Checks out code
  2. Sets up Python 3.11
  3. Installs dependencies (including PyInstaller)
  4. Builds platform-specific executable
  5. Uploads as GitHub Release asset

## Release Management

### Creating a Release

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push
   ```

2. Create a tag (version):
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

3. Watch GitHub Actions build automatically
4. Download executables from the GitHub Release page

### Version Numbering

Follow semantic versioning:
- `v1.0.0` - Major release
- `v1.0.1` - Patch/bug fix
- `v1.1.0` - Minor feature release

## Icons

To customize application icons, replace files in the `assets/` folder:

- **Linux**: `assets/icon.png` (512x512 PNG)
- **Windows**: `assets/icon.ico` (multiple sizes)
- **macOS**: `assets/icon.icns` (Apple Icon format)

Online tools for conversion:
- [PNG to ICO](https://icoconvert.com/)
- [PNG to ICNS](https://www.icoconvert.com/)

## GitHub Actions Permissions

Ensure your GitHub repository settings allow:
- ✅ Actions enabled
- ✅ Workflow permissions set to "Read and write permissions"
- ✅ Allow GitHub Actions to create and approve pull requests

## Troubleshooting

### Build fails on Windows
- Ensure path has no spaces or use quotes in commands
- Check Windows Defender isn't blocking PyInstaller

### Build fails on macOS
- Ensure M1/M2/M3 (ARM) Mac is being used for ARM builds
- May need to run: `xcode-select --install`

### Build fails on Linux
- Run: `sudo apt-get install python3-tk` for tkinter support
- Ensure libffi-dev is installed: `sudo apt-get install libffi-dev`

## Continuous Integration

The workflow automatically:
- ✅ Builds on every tag push
- ✅ Creates GitHub Releases
- ✅ Uploads executables as release assets
- ✅ Runs on specified runners for each OS

## Next Steps

1. Replace `yourusername` in setup.py with your actual GitHub username
2. Add proper icons to the `assets/` folder
3. Customize the README with your project details
4. Push to GitHub and create your first release tag!
