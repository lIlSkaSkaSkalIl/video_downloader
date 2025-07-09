# downloader/cookies_uploader.py

import os

def handle_uploaded_cookies(uploaded_files: dict) -> None:
    """
    Proses file cookies yang diupload dari browser.
    Rename file .txt menjadi cookies.txt dan tampilkan 3 baris pertama.
    
    Parameters:
        uploaded_files (dict): Dictionary dari files.upload() di Colab
    """
    cookies_file = None
    for name in uploaded_files.keys():
        if name.endswith(".txt"):
            cookies_file = name
            break

    # Rename ke cookies.txt
    if cookies_file and os.path.exists(cookies_file):
        if cookies_file != "cookies.txt":
            os.rename(cookies_file, "cookies.txt")
            print(f"📁 File '{cookies_file}' di-rename menjadi 'cookies.txt'")
        else:
            print("✅ File sudah bernama cookies.txt")

        print("📄 Contoh isi cookies.txt:")
        with open("cookies.txt", "r", encoding="utf-8") as f:
            for i in range(3):
                line = f.readline()
                if line:
                    print("  ", line.strip())
    else:
        print("❌ File .txt tidak valid ditemukan atau gagal upload.")
