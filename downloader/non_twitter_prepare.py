import os
from datetime import datetime

def prepare_download(video_url: str, file_name: str = "", download_type: str = "auto", base_dir: str = "/content/video_downloader/video") -> dict:
    """
    Menyiapkan parameter unduhan dan path penyimpanan berdasarkan input pengguna.

    Parameters:
        video_url (str): Link video yang ingin diunduh.
        file_name (str): Nama file output (boleh kosong).
        download_type (str): Jenis unduhan ("auto", "google_drive", "direct", "m3u8").
        base_dir (str): Direktori output video.

    Returns:
        dict: Berisi informasi lengkap path, nama file, jenis unduhan, dll.
    """
    os.makedirs(base_dir, exist_ok=True)

    if not file_name.strip():
        timestamp = datetime.now().strftime("video_%Y%m%d_%H%M%S")
        file_name = f"{timestamp}.mp4"
    elif not file_name.endswith(".mp4"):
        file_name += ".mp4"

    output_path = os.path.join(base_dir, file_name)

    print(f"🎯 Link: {video_url}")
    print(f"🧩 Jenis Unduhan: {download_type}")
    print(f"📁 File akan disimpan di: {output_path}")

    return {
        "video_url": video_url,
        "file_name": file_name,
        "output_path": output_path,
        "download_type": download_type
    }
