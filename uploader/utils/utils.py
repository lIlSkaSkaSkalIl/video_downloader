import os
import json
import re

# 🔠 Escape karakter Markdown agar tidak error saat parsing
def escape_md(text):
    return re.sub(r'([*\[\]~`>#+\=|{}!])', r'\\\1', text)

# 📓 Menulis log ringkas ke file .txt
def tulis_log_txt(log_txt, teks):
    with open(log_txt, "a", encoding="utf-8") as f:
        f.write(teks.strip() + "\n")

# 📦 Menulis log terstruktur ke file .json
def tulis_log_json(log_json, entry):
    try:
        if os.path.exists(log_json):
            with open(log_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except:
        data = []
    data.append(entry)
    with open(log_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
