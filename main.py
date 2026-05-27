import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import subprocess
import sys
from pathlib import Path

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YAYD (Yet Another Youtube Downloader)")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        self.download_path = Path.home() / "Downloads" / "YouTube Videos"
        self.is_downloading = False
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title Label
        title_label = ttk.Label(
            self.root, 
            text="YAYD (Yet Another Youtube Downloader)", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # URL Input Frame (restored)
        url_frame = ttk.Frame(self.root)
        url_frame.pack(pady=10, padx=20, fill="x")
        ttk.Label(url_frame, text="Video URL:").pack(side="left", padx=5)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Progress Label and Bar
        self.progress_label = ttk.Label(
            self.root,
            text="0%",
            font=("Arial", 12)
        )
        self.progress_label.pack()
        self.progress = ttk.Progressbar(
            self.root,
            length=400,
            mode="determinate",
            maximum=100
        )
        self.progress.pack(pady=5)
        
        # Download Path Frame
        path_frame = ttk.Frame(self.root)
        path_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(path_frame, text="Save to:").pack(side="left", padx=5)
        
        self.path_var = tk.StringVar(value=str(self.download_path))
        self.path_label = ttk.Label(
            path_frame, 
            textvariable=self.path_var, 
            relief="sunken",
            foreground="gray"
        )
        self.path_label.pack(side="left", fill="x", expand=True, padx=5)
        
        browse_btn = ttk.Button(
            path_frame, 
            text="Browse", 
            command=self.browse_folder,
            width=10
        )
        browse_btn.pack(side="left", padx=5)
        
        # Quality Selection Frame
        quality_frame = ttk.Frame(self.root)
        quality_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(quality_frame, text="Quality:").pack(side="left", padx=5)
        
        self.quality_var = tk.StringVar(value="best")
        quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=["best", "1080p", "720p", "480p", "360p", "audio_only"],
            state="readonly",
            width=15
        )
        quality_combo.pack(side="left", padx=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            self.root,
            length=400,
            mode="determinate",
            maximum=100
        )
        self.progress.pack(pady=15)
        
        # Status Label
        self.status_label = ttk.Label(
            self.root,
            text="Ready",
            relief="sunken",
            foreground="green"
        )
        self.status_label.pack(pady=10, padx=20, fill="x")
        
        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15)
        
        self.download_btn = ttk.Button(
            button_frame,
            text="Download",
            command=self.download_video,
            width=15
        )
        self.download_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_inputs,
            width=15
        )
        clear_btn.pack(side="left", padx=5)
        
    def browse_folder(self):
        """Open folder browser dialog"""
        folder = filedialog.askdirectory(
            title="Select Download Folder",
            initialdir=str(self.download_path)
        )
        if folder:
            self.download_path = Path(folder)
            self.path_var.set(str(self.download_path))
    
    def update_status(self, message, color="black"):
        """Update status label"""
        self.status_label.config(text=message, foreground=color)
        self.root.update()
    
    def download_video(self):
        """Download the video"""
        url = self.url_entry.get().strip()
        
        # Validation
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return
        
        if not url.startswith(("https://", "http://")):
            messagebox.showerror("Error", "Please enter a valid URL")
            return
        
        # Start download in separate thread
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, self.quality_var.get())
        )
        thread.daemon = True
        thread.start()
    
    def _download_thread(self, url, quality):
        """Download video in separate thread"""
        self.is_downloading = True
        self.download_btn.config(state="disabled")
        self.progress["value"] = 0
        self.update_status("Starting download...", "blue")
        
        try:
            # Create download directory if it doesn't exist
            self.download_path.mkdir(parents=True, exist_ok=True)
            
            # Prepare yt-dlp format options
            format_dict = {
                "best": "bestvideo+bestaudio/best",
                "1080p": "bestvideo[height=1080]+bestaudio/best",
                "720p": "bestvideo[height=720]+bestaudio/best",
                "480p": "bestvideo[height=480]+bestaudio/best",
                "360p": "bestvideo[height=360]+bestaudio/best",
                "audio_only": "bestaudio/best"
            }
            
            format_option = format_dict.get(quality, "bestvideo+bestaudio/best")
            
            # Build yt-dlp command
            output_template = str(self.download_path / "%(title)s.%(ext)s")
            
            command = [
                "yt-dlp",
                "-f", format_option,
                "--merge-output-format", "mp4" if quality != "audio_only" else "m4a",
                "-o", output_template,
                url
            ]
            
            # Run yt-dlp with real-time output
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # Parse progress from output
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                
                # Parse download progress
                # Format: [download]  35.5% of ~1.2GiB at 1.23MiB/s ETA 12:34
                if "[download]" in line:
                    self._parse_progress(line)
                
                # Parse post-processing (merging, converting)
                if "[Merger]" in line or "[ffmpeg]" in line:
                    self.update_status("Post-processing (merging video and audio)...", "blue")
                
                self.root.update()
            
            # Wait for process to complete
            returncode = process.wait()
            
            if returncode == 0:
                self.progress["value"] = 100
                self.update_status(
                    f"✓ Download completed! Saved to {self.download_path}",
                    "green"
                )
                messagebox.showinfo(
                    "Success",
                    f"Video downloaded successfully!\n\nLocation: {self.download_path}"
                )
                self.url_entry.delete(0, tk.END)
            else:
                stderr = process.stderr.read() if process.stderr else "Unknown error"
                raise Exception(stderr if stderr else "Download failed")
        
        except FileNotFoundError:
            self.progress["value"] = 0
            self.update_status("Error: yt-dlp not found. Install it first.", "red")
            messagebox.showerror(
                "Error",
                "yt-dlp is not installed.\n\n"
                "Install it using: pip install yt-dlp"
            )
        except Exception as e:
            self.progress["value"] = 0
            error_text = str(e)[:100]
            self.update_status(f"Error: {error_text}", "red")
            messagebox.showerror("Download Error", f"An error occurred:\n\n{str(e)}")
        
        finally:
            self.is_downloading = False
            self.download_btn.config(state="normal")
    
    def _parse_progress(self, line):
        """Parse progress line from yt-dlp output"""
        import re
        
        try:
            # Extract percentage
            percent_match = re.search(r"(\d+\.?\d*)%", line)
            if percent_match:
                percent = float(percent_match.group(1))
                self.progress["value"] = min(percent, 100)
                self.progress_label.config(text=f"{percent:.1f}%")
            
            # Extract size and speed info
            # Format: [download]  35.5% of ~1.2GiB at 1.23MiB/s ETA 12:34
            size_match = re.search(r"of\s+([\d.]+\s*[KMGT]i?B)", line)
            speed_match = re.search(r"at\s+([\d.]+\s*[KMGT]i?B/s)", line)
            eta_match = re.search(r"ETA\s+([\d:]+)", line)
            
            status_parts = [f"{percent:.1f}%"]
            
            if size_match:
                status_parts.append(f"of {size_match.group(1)}")
            if speed_match:
                status_parts.append(f"@ {speed_match.group(1)}")
            if eta_match:
                status_parts.append(f"ETA {eta_match.group(1)}")
            
            status_text = " | ".join(status_parts)
            self.update_status(f"Downloading... {status_text}", "blue")
        
        except Exception:
            pass  # Silently ignore parsing errorsnfig(state="normal")
            self.progress.stop()
    
    def clear_inputs(self):
        """Clear input fields"""
        self.url_entry.delete(0, tk.END)
        self.update_status("Ready", "green")


def main():
    # Check if yt-dlp is installed
    try:
        subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            check=True
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        root = tk.Tk()
        root.withdraw()
        result = messagebox.askyesno(
            "yt-dlp Not Found",
            "yt-dlp is required but not installed.\n\n"
            "Click 'Yes' to install it now via pip.\n"
            "Click 'No' to continue without it (downloads will fail)."
        )
        root.destroy()
        
        if result:
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
            except Exception as e:
                messagebox.showerror("Installation Error", f"Failed to install yt-dlp:\n{e}")
                return
    
    # Run the application
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
