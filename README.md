# YouTube Video Downloader

A simple Python GUI application to download YouTube videos at your desired quality.

## Features

- **Easy-to-use GUI** with tkinter (no external GUI dependencies)
- **Multiple quality options**: Best, 1080p, 720p, 480p, 360p, or audio only
- **Custom download location**: Choose where to save your videos
- **Progress indication**: Visual feedback during downloads
- **Error handling**: Helpful error messages if something goes wrong
- **Automatic installation**: Offers to install yt-dlp on first run if needed

## Requirements

- Python 3.6 or higher
- yt-dlp (automatically installed on first run)

## Installation

1. **Clone or download this project** to your desired location

2. **Install dependencies** (optional - the app will prompt you on first run):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application**:
   ```bash
   python main.py
   ```

2. **Paste a YouTube URL** in the text field

3. **Select desired quality** from the dropdown (default: best)

4. **(Optional) Choose download location** using the Browse button

5. **Click Download** and wait for completion

Videos are saved by default to: `~/Downloads/YouTube Videos/`

## Quality Options

- **best**: Downloads the best available video and audio quality
- **1080p**: Full HD video (1920x1080)
- **720p**: HD video (1280x720)
- **480p**: Standard definition video
- **360p**: Lower resolution (faster download)
- **audio_only**: Extract audio as M4A format

## Troubleshooting

- **"yt-dlp not found" error**: The app will offer to install it automatically. Or run: `pip install yt-dlp`
- **Download fails**: Make sure the URL is valid and YouTube hasn't blocked yt-dlp
- **Permission denied**: Ensure the download folder has write permissions

## Notes

- Uses yt-dlp, which is maintained and more reliable than youtube-dl
- Videos are automatically merged with audio (for video quality options)
- Download times depend on video length, quality, and internet speed
- Respects YouTube's Terms of Service - only download content you have rights to

## License

MIT - Feel free to modify and use as needed.

## Building Executables

### Automatic Builds (GitHub Actions)

Executables are automatically built for Windows, Linux, and macOS via GitHub Actions when you push a version tag:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Downloads will be available on the [Releases](../../releases) page.

### Local Builds

Build an executable for your current platform:

```bash
# Install PyInstaller
pip install PyInstaller

# Run build script
chmod +x build.sh
./build.sh
```

See [CI_CD_SETUP.md](CI_CD_SETUP.md) for detailed build and release instructions.
# YetAnotherYoutubeDownloader
