import subprocess

def download_from_direct_link(url: str, output_path: str):
    cmd = [
        "yt-dlp",
        "-f", "best",
        "-o", output_path,
        "--no-warnings",
        "--retries", "3",
        url
    ]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        print(f"\r{line.strip()[:150]}", end="", flush=True)
    process.wait()
