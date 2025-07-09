import gdown
import re

def extract_drive_id(url: str) -> str:
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

def download_from_google_drive(url: str, output_path: str):
    file_id = extract_drive_id(url)
    if not file_id:
        raise ValueError("❌ Tidak dapat mendeteksi ID file dari URL Google Drive.")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)
