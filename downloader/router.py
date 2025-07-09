# downloader/router.py

import time
import os

from downloader.google_drive import download_from_google_drive
from downloader.m3u8 import download_from_m3u8
from downloader.ytdlp import download_with_ytdlp
from core.setup_directories import prepare_directories

dirs = prepare_directories()

def is_m3u8(url: str) -> bool:
    return url.endswith(".m3u8") or ".m3u8?" in url

def is_drive(url: str) -> bool:
    return "drive.google.com" in url

def process_download(video_url: str, output_path: str = None, download_type: str = "auto"):
    print("🎯 Link:", video_url)
    print("🧩 Jenis Unduhan:", download_type)
    print("────────────────────────────")

    # Deteksi jenis jika auto
    tool = download_type
    if tool == "auto":
        if is_drive(video_url):
            tool = "google_drive"
        elif is_m3u8(video_url):
            tool = "m3u8"
        else:
            tool = "direct"

    print(f"🚀 Menggunakan alat: {tool}")
    start_time = time.time()

    try:
        if tool == "google_drive":
            output = download_from_google_drive(video_url)
        elif tool == "m3u8":
            output = download_from_m3u8(video_url)
        elif tool == "direct":
            if not output_path:
                output_path = os.path.join(dirs["video"], "direct_video.mp4")
            download_with_ytdlp(video_url, output_path)
            output = output_path
        else:
            raise ValueError("❌ Jenis download tidak dikenali!")

        if os.path.exists(output):
            size = os.path.getsize(output) / (1024 * 1024)
            elapsed = time.time() - start_time
            print(f"\n✅ Selesai! File: {output}")
            print(f"📦 Ukuran file: {size:.2f} MB")
            print(f"⏱️ Waktu download: {elapsed:.2f} detik")
        else:
            print("\n⚠️ Download selesai tapi file tidak ditemukan.")

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat mengunduh: {e}")
