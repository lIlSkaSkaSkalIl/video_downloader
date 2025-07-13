import os
import re
import subprocess
import time
from tqdm import tqdm
from yt_dlp import YoutubeDL

from utils.directories import prepare_directories
from utils.utils import log  # ⬅️ log custom buatan sendiri


def extract_tweet_id(tweet_url: str) -> str:
    match = re.search(r"/status/(\d+)", tweet_url)
    if not match:
        raise ValueError("❌ Invalid URL: Tweet ID not found.")
    return match.group(1)


def simulate_metadata(tweet_url: str) -> dict | None:
    ydl_opts = {
        "quiet": True,
        "simulate": True,
        "extract_flat": True,
        "dump_single_json": True,
    }
    log(f"Detecting tweet metadata... ({tweet_url})", "🔍")
    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(tweet_url, download=False)
    except Exception as e:
        log(f"Failed to detect metadata: {e}", "❌")
        if "authentication" in str(e).lower():
            log("This tweet may require cookies.txt (login).", "🔐")
        return None


def download_tweet_video(
    tweet_url: str,
    base_dir: str = "/content/media_toolkit",
    cookies_file: str = "cookies.txt"
):
    # 📁 Prepare directory structure
    dirs = prepare_directories(base_dir)
    video_dir = dirs["video"]
    cookies_dir = dirs["cookies"]
    cookies_path = os.path.join(cookies_dir, cookies_file)

    os.makedirs(video_dir, exist_ok=True)
    tweet_id = extract_tweet_id(tweet_url)
    use_cookies = os.path.isfile(cookies_path)

    # 🧠 Build yt-dlp command
    command = ["yt-dlp"]
    if use_cookies:
        command += ["--cookies", cookies_path]
    command += [
        "-f", "best",
        "-o", f"{video_dir}/%(id)s_video.%(ext)s",
        tweet_url
    ]

    log("Using cookies.txt" if use_cookies else "Not using cookies", "🔐" if use_cookies else "🔓")
    log("Starting download using yt-dlp", "📥")

    progress_bar = tqdm(total=100, desc="📥 Download", unit="%")
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    start_time = time.time()

    for line in process.stdout:
        line = line.strip()
        if "%" in line:
            match = re.search(r'(\d{1,3}\.\d+)%', line)
            if match:
                percent = float(match.group(1))
                progress_bar.n = int(percent)
                progress_bar.refresh()
        elif "[download]" in line or "Destination" in line:
            log(line, "📄")

    process.wait()
    duration_seconds = time.time() - start_time
    progress_bar.n = 100
    progress_bar.refresh()
    progress_bar.close()

    log("Download completed", "✅")

    return tweet_id, use_cookies, video_dir, duration_seconds
