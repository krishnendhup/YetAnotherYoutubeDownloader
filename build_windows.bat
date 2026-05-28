@echo off
setlocal enabledelayedexpansion

echo Building YouTube Downloader for Windows...
echo.

echo [*] Step 1: Installing dependencies...
pip install -r requirements.txt
pip install cx_Freeze

echo [*] Step 2: Building with PyInstaller...
pyinstaller --onefile ^
    --windowed ^
    --name="YouTube-Downloader" ^
    --icon=icon.ico ^
    --add-data=".;." ^
    main.py

if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
)

echo [*] Step 3: Creating installer files...
rem Create dist folder structure
mkdir dist\YouTube-Downloader\

rem Copy executable
copy dist\YouTube-Downloader.exe dist\YouTube-Downloader\

echo.
echo [SUCCESS] Build complete!
echo Output: dist\YouTube-Downloader.exe
echo All dependencies are bundled inside the executable.
echo.
pause
