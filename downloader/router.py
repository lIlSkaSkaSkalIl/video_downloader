import time
import os
from downloader.google_drive import download_from_google_drive
from downloader.ytdlp import download_with_ytdlp

def is_m3u8(url: str) -> bool:
    return url.endswith(".m3u8") or ".m3u8?" in url or ".ts" in url

def is_drive(url: str) -> bool:
    return "drive.google.com" in url

def process_download(video_url: str, output_path: str, download_type: str = "auto"):
    print("🎯 Link:", video_url)
    print("🧩 Jenis Unduhan:", download_type)
    print("────────────────────────────")

    tool = download_type
    if tool == "auto":
        if is_drive(video_url):
            tool = "google_drive"
        elif is_m3u8(video_url):
            tool = "ytdlp"
        else:
            tool = "ytdlp"

    print(f"🚀 Menggunakan alat: {tool}")
    start_time = time.time()

    try:
        if tool == "google_drive":
            download_from_google_drive(video_url, os.path.basename(output_path))
        elif tool == "ytdlp":
            download_with_ytdlp(url=video_url, output_template=output_path)
        else:
            raise ValueError("❌ Jenis download tidak dikenali!")

        if os.path.exists(output_path):
            size = os.path.getsize(output_path) / (1024 * 1024)
            elapsed = time.time() - start_time
            print(f"\n\n✅ Selesai! File disimpan di: {output_path}")
            print(f"📦 Ukuran file: {size:.2f} MB")
            print(f"⏱️ Waktu download: {elapsed:.2f} detik")
        else:
            print("\n⚠️ Download selesai tapi file tidak ditemukan.")

    except Exception as e:
        print(f"\n❌ Terjadi kesalahan saat mengunduh: {e}")
