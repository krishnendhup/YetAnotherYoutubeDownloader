# Application Icons

This folder contains icons for different platforms. Replace with your own custom icons.

## Icon Files

- **icon.png** - Linux icon (512x512 or larger)
- **icon.ico** - Windows icon (supports multiple sizes, typically 256x256)
- **icon.icns** - macOS icon (1024x1024)

## How to Create Icons

### From a single image:

1. **Online Tools**:
   - [icoconvert.com](https://icoconvert.com/) - Converts PNG to ICO and ICNS
   - [convertio.co](https://convertio.co/) - General image converter

2. **Using ImageMagick (CLI)**:
   ```bash
   # PNG to ICO
   convert icon.png -define icon:auto-resize=256,128,96,64,48,32,16 icon.ico
   
   # PNG to ICNS (macOS)
   convert icon.png -define icon:auto-resize=1024,512,256,128,64,32,16 icon.icns
   ```

3. **Using Python**:
   ```bash
   pip install Pillow
   python -c "from PIL import Image; Image.open('icon.png').resize((256,256)).save('icon.ico')"
   ```

## Recommended Specifications

| Platform | Format | Size | Notes |
|----------|--------|------|-------|
| Linux | PNG | 512×512 | Transparent background |
| Windows | ICO | 256×256 | Multiple sizes embedded |
| macOS | ICNS | 1024×1024 | Apple icon format |

## Using Custom Icons

1. Replace the icon files in this folder
2. The GitHub Actions workflow will automatically use them
3. For local builds, run `./build.sh`

If icons are missing, PyInstaller will use default system icons.
