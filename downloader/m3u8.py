# downloader/m3u8.py

import subprocess
import os
from core.setup_directories import prepare_directories

dirs = prepare_directories()

def download_from_m3u8(url: str, filename: str = "video_m3u8.mp4") -> str:
    downloader_path = os.path.expanduser("~/.local/bin/downloadm3u8")
    if not os.path.exists(downloader_path):
        raise FileNotFoundError("❌ 'downloadm3u8' tidak ditemukan di ~/.local/bin/. Restart runtime setelah install.")

    output_path = os.path.join(dirs["video"], filename)

    cmd = [
        downloader_path,
        "-o", output_path,
        url
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(f"\r{line.strip()[:150]}", end="", flush=True)
    process.wait()
    return output_path
