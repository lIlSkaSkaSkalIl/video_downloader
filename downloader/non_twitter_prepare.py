# downloader/non_twitter_prepare.py

import os
from datetime import datetime
from core.setup_directories import prepare_directories

dirs = prepare_directories()

def prepare_download(video_url: str, file_name: str = "", download_type: str = "auto") -> dict:
    if not file_name.strip():
        timestamp = datetime.now().strftime("video_%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.mp4"
    elif not file_name.endswith(".mp4"):
        file_name += ".mp4"

    output_path = os.path.join(dirs["video"], file_name)

    print(f"🎯 Link: {video_url}")
    print(f"🧩 Jenis Unduhan: {download_type}")
    print(f"📁 File akan disimpan di: {output_path}")

    return {
        "video_url": video_url,
        "file_name": file_name,
        "output_path": output_path,
        "download_type": download_type
    }
