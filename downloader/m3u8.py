# downloader/m3u8.py

import os
import subprocess
import time
from pathlib import Path

def ensure_dependencies():
    """Install aria2c and yt-dlp silently."""
    def silent_install(cmd):
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
    silent_install(["apt", "-qq", "install", "-y", "aria2"])
    silent_install(["pip", "install", "-q", "--upgrade", "yt-dlp"])

def auto_detect_filename(video_url: str) -> str:
    """Coba deteksi nama file dari yt-dlp, fallback ke default."""
    try:
        filename = subprocess.check_output([
            "yt-dlp", "--get-filename", "-o", "%(title)s.%(ext)s", video_url
        ], text=True).strip()
        if not filename:
            raise ValueError("Empty filename")
        return filename
    except Exception:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        return f"video_{timestamp}.mp4"

def download_m3u8_video(video_url: str, output_dir: str = "/content/download/video", output_name: str = ""):
    ensure_dependencies()
    os.makedirs(output_dir, exist_ok=True)

    # Deteksi otomatis jika output_name kosong
    if not output_name.strip():
        output_name = auto_detect_filename(video_url)

    # Pastikan output_name berakhiran .mp4
    base = Path(output_name).stem
    output_name = f"{base}.mp4"
    output_path = os.path.join(output_dir, output_name)

    print(f"\n📥 Mulai mengunduh:")
    print(f"╭🔗 Link   : {video_url}")
    print(f"├🗃 Output : {output_path}")
    print("╰🛠️ Downloader : yt-dlp + aria2c (16 koneksi paralel)\n")

    start_time = time.time()

    cmd = [
        "yt-dlp",
        "-o", output_path,
        "--downloader", "aria2c",
        "--downloader-args", "aria2c:-x 16 -s 16 -k 1M",
        video_url
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    for line in process.stdout:
        if line.strip():
            print(f"⏳ {line.strip()[:100]}", flush=True)

    process.wait()

    if os.path.exists(output_path):
        size = os.path.getsize(output_path) / (1024 * 1024)
        duration = time.time() - start_time
        print(f"\n✅ Selesai! \n╭🗃 File disimpan di: {output_path}")
        print(f"├📦 Ukuran file: {size:.2f} MB")
        print(f"╰⏱️ Durasi download: {duration:.2f} detik")
    else:
        print("\n❌ Download gagal atau file tidak ditemukan.")
