import os
from google.colab import files
from utils.directories import prepare_directories
from utils.utils import log

def upload_cookies():
    # 📁 Siapkan direktori
    dirs = prepare_directories()
    cookies_dir = dirs["cookies"]
    cookies_path = os.path.join(cookies_dir, "cookies.txt")

    log("Waiting for cookies.txt upload...", icon="📤")
    uploaded = files.upload()

    # Temukan file .txt yang diupload
    cookies_file = None
    for name in uploaded.keys():
        if name.endswith(".txt"):
            cookies_file = name
            break

    if cookies_file and os.path.exists(cookies_file):
        os.makedirs(cookies_dir, exist_ok=True)

        if cookies_file != "cookies.txt":
            os.rename(cookies_file, "cookies.txt")

        os.replace("cookies.txt", cookies_path)
        log(f"Cookies file saved to → {cookies_path}", icon="✅")

        # Tampilkan 3 baris awal dari cookies.txt
        print("📄 Preview cookies.txt (first 3 lines):")
        with open(cookies_path, "r", encoding="utf-8") as f:
            for i in range(3):
                line = f.readline()
                if line:
                    print("  ", line.strip())
    else:
        log("No valid .txt file uploaded or upload failed.", icon="❌")
