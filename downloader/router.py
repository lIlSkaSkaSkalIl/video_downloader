# video_downloader/downloader/router.py

import re
import shutil
import subprocess
import os
from datetime import datetime
from utils.messages import log, download_summary, show_tool_detection, show_download_info

def prepare_download(video_url: str, download_type: str, file_name: str, video_dir: str) -> str:
    """
    Prepare the final output path and valid filename for video download.

    Returns the full output_path.
    """
    os.makedirs(video_dir, exist_ok=True)
    log("Video folder is ready.", icon="📂")

    # Generate filename if not provided
    if not file_name.strip():
        timestamp = datetime.now().strftime("video_%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.mp4"
        log("Filename generated based on current time.", icon="🕒")
    elif not file_name.endswith(".mp4"):
        file_name += ".mp4"
        log("Added .mp4 extension to the filename.", icon="✏️")

    output_path = os.path.join(video_dir, file_name)
    show_download_info(video_url, download_type, output_path)

    return output_path


def is_m3u8(url: str) -> bool:
    return url.endswith(".m3u8") or ".m3u8?" in url


def is_drive(url: str) -> bool:
    return "drive.google.com" in url


def extract_drive_id(url: str) -> str | None:
    patterns = [
        r"drive\.google\.com\/file\/d\/([^\/]+)",
        r"drive\.google\.com\/open\?id=([^&]+)",
        r"drive\.google\.com\/uc\?id=([^&]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def download_video_by_type(download_type: str, video_url: str, output_path: str, video_dir: str):
    """
    Download video from given URL based on the detected or selected type.
    """

    # 🔍 Detect tool type
    tool = download_type
    if tool == "auto":
        if is_drive(video_url):
            tool = "google_drive"
        elif is_m3u8(video_url):
            tool = "m3u8"
        else:
            tool = "direct"

    show_tool_detection(tool)

    # ===================== DOWNLOAD PROCESS =====================

    if tool == "google_drive":
        log("Downloading from Google Drive...", icon="📁")
        import gdown
        drive_id = extract_drive_id(video_url)
        if not drive_id:
            raise ValueError("❌ Cannot detect Google Drive ID.")
        gdown.download(f"https://drive.google.com/uc?id={drive_id}", output_path, quiet=False)

    elif tool == "m3u8":
        log("Downloading from M3U8 with yt-dlp + aria2c...", icon="📺")

        temp_path = os.path.join(video_dir, "temp_m3u8")
        os.makedirs(temp_path, exist_ok=True)

        cmd = [
            "yt-dlp",
            "--downloader", "aria2c",
            "--downloader-args", "aria2c:-x 16 -j 32 -s 32 -k 1M",
            "-f", "best",
            "-o", os.path.join(temp_path, "%(id)s.%(ext)s"),
            video_url
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(f"\r{line.strip()[:150]}", end="", flush=True)
        process.wait()

        downloaded_files = [f for f in os.listdir(temp_path) if f.endswith((".mp4", ".mkv", ".webm"))]
        if not downloaded_files:
            raise FileNotFoundError("❌ No video file found in temp folder.")
        
        temp_download_path = os.path.join(temp_path, downloaded_files[0])
        shutil.move(temp_download_path, output_path)
        log(f"File moved to: {output_path}", icon="✅")

    elif tool == "direct":
        log("Downloading from Direct Link using yt-dlp...", icon="📥")
        cmd = [
            "yt-dlp",
            "-f", "best",
            "-o", output_path,
            "--no-warnings",
            "--retries", "3",
            video_url
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(f"\r{line.strip()[:150]}", end="", flush=True)
        process.wait()

    else:
        raise ValueError("❌ Unknown download type!")

    # ✅ Ringkasan
    download_summary(output_path)
