# downloader/cookies_uploader.py

import os

def handle_uploaded_cookies(uploaded_files: dict, target_dir: str = ".") -> None:
    """
    Memproses file cookies.txt yang diupload via Colab dan menyimpannya ke folder yang ditentukan.

    Parameters:
        uploaded_files (dict): Dictionary dari files.upload() di Colab
        target_dir (str): Direktori tujuan penyimpanan cookies.txt
    """
    os.makedirs(target_dir, exist_ok=True)
    cookies_file = None
    for name in uploaded_files.keys():
        if name.endswith(".txt"):
            cookies_file = name
            break

    final_path = os.path.join(target_dir, "cookies.txt")

    if cookies_file and os.path.exists(cookies_file):
        os.rename(cookies_file, final_path)
        print(f"📁 File '{cookies_file}' di-rename dan dipindahkan ke '{final_path}'")

        print("📄 Contoh isi cookies.txt:")
        with open(final_path, "r", encoding="utf-8") as f:
            for i in range(3):
                line = f.readline()
                if line:
                    print("  ", line.strip())
    else:
        print("❌ File .txt tidak valid ditemukan atau gagal upload.")
