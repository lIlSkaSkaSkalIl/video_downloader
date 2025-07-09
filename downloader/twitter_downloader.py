# downloader/twitter_downloader.py

import os
import re
import json
import glob
import subprocess
import datetime
from tqdm import tqdm

from core.setup_directories import prepare_directories
from pathlib import Path

# Siapkan direktori
dirs = prepare_directories()
VIDEO_DIR = dirs["video"]
META_DIR = dirs["meta"]
COOKIES_PATH = os.path.join(dirs["cookies"], "cookies.txt")

def extract_tweet_id(url: str) -> str:
    match = re.search(r"/status/(\d+)", url)
    if not match:
        raise ValueError("❌ URL tidak valid: Tidak ditemukan Tweet ID.")
    return match.group(1)

def simulate_metadata(url: str, use_cookies: bool = False) -> dict:
    try:
        import yt_dlp
    except ImportError:
        raise RuntimeError("yt-dlp belum terinstall. Gunakan `!pip install -U yt-dlp` di Colab.")

    ydl_opts = {
        "quiet": True,
        "simulate": True,
        "extract_flat": True,
        "dump_single_json": True,
    }

    if use_cookies and os.path.exists(COOKIES_PATH):
        ydl_opts["cookiefile"] = COOKIES_PATH

    print(f"🔍 Mendeteksi metadata tweet... ({url})")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"❌ Gagal mendeteksi metadata: {e}")
        if "authentication" in str(e).lower():
            print("🔐 Tweet ini kemungkinan membutuhkan cookies.txt (login).")
        return None

def save_metadata_json(info: dict, tweet_id: str):
    if info is None:
        print("⚠️ Metadata tidak tersedia, tidak disimpan.")
        return

    path = os.path.join(META_DIR, f"deteksi_tweet_{tweet_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f"📄 Metadata disimpan ke: {path}")

def download_tweet_video(url: str, use_cookies: bool = False) -> list:
    command = ["yt-dlp"]
    if use_cookies and os.path.exists(COOKIES_PATH):
        command += ["--cookies", COOKIES_PATH]

    command += [
        "-f", "best",
        "-o", f"{VIDEO_DIR}/%(id)s_video.%(ext)s",
        url
    ]

    print("📥 Mulai mengunduh video...\n")
    progress_bar = tqdm(total=100, desc="📥 Download", unit="%")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        line = line.strip()
        if "%" in line:
            match = re.search(r'(\d{1,3}\.\d)%', line)
            if match:
                percent = float(match.group(1))
                progress_bar.n = int(percent)
                progress_bar.refresh()
        elif "[download]" in line or "Destination" in line:
            print(line)
    process.wait()
    progress_bar.n = 100
    progress_bar.refresh()
    progress_bar.close()

    print("✅ Download selesai.")
    return glob.glob(os.path.join(VIDEO_DIR, "*_video.*"))

def summarize_download(files: list, tweet_id: str, tweet_url: str, metadata: dict = None):
    total_size_mb = sum(os.path.getsize(f) for f in files) / (1024 * 1024)
    file_names = [os.path.basename(f) for f in files]

    print("\n📊 Ringkasan Status:")
    print(f"- 📌 URL Tweet       : {tweet_url}")
    print(f"- 🆔 ID Tweet        : {tweet_id}")
    print(f"- 🔐 Cookies         : {'✅ Digunakan' if os.path.exists(COOKIES_PATH) else '❌ Tidak digunakan'}")
    print(f"- 📄 Metadata JSON   : {'✅ Tersimpan' if metadata else '❌ Tidak ada'}")
    print(f"- 📁 Total Video     : {len(files)} file")
    print(f"- 💾 Ukuran Total    : {total_size_mb:.2f} MB")
    print(f"- 🕒 Selesai pada     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"- 📂 Lokasi Video    : {VIDEO_DIR}")
    print(f"- 📜 Daftar File     :")
    for i, fname in enumerate(file_names, 1):
        print(f"   {i}. {fname}")
