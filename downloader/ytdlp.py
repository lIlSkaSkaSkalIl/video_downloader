import subprocess
import os
from typing import List
from core.setup_directories import prepare_directories

# Ambil path cookies dari struktur yang telah disiapkan
dirs = prepare_directories()
COOKIES_PATH = os.path.join(dirs["cookies"], "cookies.txt")

def download_with_ytdlp(
    url: str,
    output_template: str,
    use_cookies: bool = False,
    extra_args: List[str] = []
):
    cmd = ["yt-dlp", "-f", "best", "-o", output_template] + extra_args

    if use_cookies and os.path.exists(COOKIES_PATH):
        cmd += ["--cookies", COOKIES_PATH]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(f"\r{line.strip()[:150]}", end="", flush=True)
    process.wait()
