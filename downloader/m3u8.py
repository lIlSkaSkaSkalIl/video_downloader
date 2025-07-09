# downloader/m3u8.py

import subprocess
import shutil

def download_from_m3u8(url: str, output_path: str):
    """
    Mengunduh video dari link M3U8 menggunakan downloadm3u8 CLI tool.

    Parameters:
        url (str): URL video M3U8.
        output_path (str): Path file output untuk menyimpan hasil unduhan.

    Raises:
        FileNotFoundError: Jika `downloadm3u8` tidak ditemukan di PATH sistem.
    """
    # Cari path dari downloadm3u8 secara otomatis
    downloader_path = shutil.which("downloadm3u8")
    if not downloader_path:
        raise FileNotFoundError(
            "❌ 'downloadm3u8' tidak ditemukan di PATH. "
            "Pastikan sudah menjalankan: `!pip install --user m3u8downloader` "
            "dan menambahkan ~/.local/bin ke PATH."
        )

    # Jalankan perintah unduhan
    cmd = [
        downloader_path,
        "-o", output_path,
        url
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        print(f"\r{line.strip()[:150]}", end="", flush=True)

    process.wait()
