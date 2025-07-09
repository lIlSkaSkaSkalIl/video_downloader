# downloader/twitter_downloader.py

import os
import re
import json
import glob
import datetime
from tqdm import tqdm

from downloader.ytdlp import download_with_ytdlp
from core.setup_directories import prepare_directories

dirs = prepare_directories()

def extract_tweet_id(url: str) -> str:
    match = re.search(r"/status/(\d+)", url)
    if not match:
        raise ValueError("❌ URL tidak valid: Tidak ditemukan Tweet ID.")
    return match.group(1)

def simulate_metadata(url: str, use_cookies: bool = False) -> dict:
    try:
        import yt_dlp
    except ImportError:
        raise RuntimeError("yt-dlp belum terinstall. Gunakan `!pip install -U yt-dlp`.")
    
    ydl_opts = {
        "quiet": True,
        "simulate": True,
        "extract_flat": True,
        "dump_single_json": True,
    }
    if use_cookies and os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    print(f"🔍 Mendeteksi metadata tweet... ({url})")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except Exception as e:
        print(f"❌ Gagal mendeteksi metadata: {e}")
        return None

def save_metadata_json(info: dict, tweet_id: str):
    if info is None:
        print("⚠️ Metadata tidak tersedia.")
        return
    path = os.path.join(dirs["meta"], f"deteksi_tweet_{tweet_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    print(f"📄 Metadata disimpan ke: {path}")

def download_tweet_video(url: str, use_cookies: bool = False) -> list:
    output_template = os.path.join(dirs["video"], "%(id)s_video.%(ext)s")
    print("📥 Mulai mengunduh video...\n")
    download_with_ytdlp(url, output_template, use_cookies)
    print("✅ Download selesai.")
    return glob.glob(os.path.join(dirs["video"], "*_video.*"))

def summarize_download(files: list, tweet_id: str, tweet_url: str, metadata: dict = None):
    total_size_mb = sum(os.path.getsize(f) for f in files) / (1024 * 1024)
    file_names = [os.path.basename(f) for f in files]

    print("\n📊 Ringkasan Status:")
    print(f"- 📌 URL Tweet       : {tweet_url}")
    print(f"- 🆔 ID Tweet        : {tweet_id}")
    print(f"- 🔐 Cookies         : {'✅ Digunakan' if os.path.exists('cookies.txt') else '❌ Tidak digunakan'}")
    print(f"- 📄 Metadata JSON   : {'✅ Tersimpan' if metadata else '❌ Tidak ada'}")
    print(f"- 📁 Total Video     : {len(files)} file")
    print(f"- 💾 Ukuran Total    : {total_size_mb:.2f} MB")
    print(f"- 🕒 Selesai pada     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"- 📂 Lokasi Video    : {dirs['video']}")
    print(f"- 📜 Daftar File     :")
    for i, fname in enumerate(file_names, 1):
        print(f"   {i}. {fname}")
