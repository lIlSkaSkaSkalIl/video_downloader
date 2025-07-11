# downloader/twitter_downloader.py

import os
import re
import subprocess
import glob
import datetime
from tqdm import tqdm
from yt_dlp import YoutubeDL

def extract_tweet_id(tweet_url: str) -> str:
    match = re.search(r"/status/(\d+)", tweet_url)
    if not match:
        raise ValueError("❌ URL tidak valid: Tidak ditemukan Tweet ID.")
    return match.group(1)

def simulate_metadata(tweet_url: str) -> dict | None:
    ydl_opts = {
        "quiet": True,
        "simulate": True,
        "extract_flat": True,
        "dump_single_json": True,
    }
    print(f"🔍 Mendeteksi metadata tweet... ({tweet_url})")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(tweet_url, download=False)
    except Exception as e:
        print(f"❌ Gagal mendeteksi metadata: {e}")
        if "authentication" in str(e).lower():
            print("🔐 Tweet ini kemungkinan membutuhkan cookies.txt (login).")
        return None

def download_tweet_video(tweet_url: str, video_dir: str = "/content/download/video", cookies_path: str = "cookies.txt"):
    os.makedirs(video_dir, exist_ok=True)
    tweet_id = extract_tweet_id(tweet_url)
    use_cookies = os.path.exists(cookies_path)

    # Siapkan perintah yt-dlp
    command = ["yt-dlp"]
    if use_cookies:
        command += ["--cookies", cookies_path]
    command += [
        "-f", "best",
        "-o", f"{video_dir}/%(id)s_video.%(ext)s",
        tweet_url
    ]

    print("🔐 Menggunakan cookies.txt" if use_cookies else "🔓 Tidak menggunakan cookies")
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

    return tweet_id, use_cookies, video_dir
