#!/usr/bin/env python3
"""
Cross-platform build script for YouTube Downloader
Bundles all pip dependencies into standalone executables
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class YouTubeDownloaderBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        self.system = platform.system()

    def install_dependencies(self):
        """Install required build tools"""
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

        if self.system == "Windows":
            subprocess.run([sys.executable, "-m", "pip", "install", "cx_Freeze"], check=True)
        elif self.system == "Darwin":
            subprocess.run([sys.executable, "-m", "pip", "install", "dmg"], check=True)

    def build_exe(self):
        """Build executable with PyInstaller"""
        print("\n🔨 Building with PyInstaller...")

        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=YouTube-Downloader",
            "--add-data=.",
        ]

        # Add icon if it exists
        if (self.project_root / "icon.ico").exists():
            cmd.append(f"--icon={self.project_root / 'icon.ico'}")

        cmd.append("main.py")

        subprocess.run(cmd, cwd=self.project_root, check=True)

    def build_macos_dmg(self):
        """Build macOS DMG file"""
        print("\n🍎 Creating macOS DMG...")

        # Create temporary directory for DMG contents
        dmg_temp = self.dist_dir / "dmg_temp"
        dmg_temp.mkdir(exist_ok=True)

        # Copy app bundle
        app_source = self.dist_dir / "YouTube-Downloader.app"
        app_dest = dmg_temp / "YouTube-Downloader.app"
        if app_dest.exists():
            shutil.rmtree(app_dest)
        shutil.copytree(app_source, app_dest)

        # Create Applications symlink
        applications_link = dmg_temp / "Applications"
        if applications_link.exists():
            applications_link.unlink()
        os.symlink("/Applications", applications_link)

        # Create DMG
        dmg_path = self.dist_dir / "YouTube-Downloader.dmg"
        if dmg_path.exists():
            dmg_path.unlink()

        subprocess.run([
            "dmg",
            "create",
            f"--source={dmg_temp}",
            f"--destination={dmg_path}",
            "--volname=YouTube Downloader",
        ], check=True)

        # Cleanup
        shutil.rmtree(dmg_temp)
        print(f"✅ DMG created: {dmg_path}")

    def build_windows_installer(self):
        """Build Windows installer"""
        print("\n🪟 Creating Windows installer...")

        exe_path = self.dist_dir / "YouTube-Downloader.exe"
        print(f"✅ Executable created: {exe_path}")
        print("💡 The .exe file includes all Python dependencies and yt-dlp")

    def build(self):
        """Main build process"""
        try:
            print("=" * 60)
            print("YouTube Downloader - Build Script")
            print("=" * 60)

            self.install_dependencies()
            self.build_exe()

            if self.system == "Darwin":
                self.build_macos_dmg()
            elif self.system == "Windows":
                self.build_windows_installer()
            else:
                print("\n✅ Build complete! Linux executable ready in dist/")

            print("\n" + "=" * 60)
            print("✅ Build successful!")
            print("=" * 60)

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Build failed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    builder = YouTubeDownloaderBuilder()
    builder.build()
