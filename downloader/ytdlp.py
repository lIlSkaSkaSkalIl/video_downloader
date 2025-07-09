# downloader/ytdlp.py

import subprocess
import os
from typing import List

def download_with_ytdlp(
    url: str,
    output_template: str,
    use_cookies: bool = False,
    extra_args: List[str] = []
):
    cmd = ["yt-dlp", "-f", "best", "-o", output_template] + extra_args
    if use_cookies and os.path.exists("cookies.txt"):
        cmd += ["--cookies", "cookies.txt"]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(f"\r{line.strip()[:150]}", end="", flush=True)
    process.wait()
