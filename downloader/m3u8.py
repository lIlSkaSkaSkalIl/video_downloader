import subprocess
import os

def download_from_m3u8(url: str, output_path: str):
    downloader_path = os.path.expanduser("~/.local/bin/downloadm3u8")
    if not os.path.exists(downloader_path):
        raise FileNotFoundError("❌ 'downloadm3u8' tidak ditemukan di ~/.local/bin/. Restart runtime setelah install.")

    cmd = [
        downloader_path,
        "-o", output_path,
        url
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(f"\r{line.strip()[:150]}", end="", flush=True)
    process.wait()
