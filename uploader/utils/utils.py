import os
import json
import re

# 🔠 Escape special characters for Markdown (Telegram)
def escape_md(text: str) -> str:
    return re.sub(r'([*\[\]~`>#+=|{}!])', r'\\\1', text)

# 📓 Append plain log line to .txt file
def write_log_txt(log_txt_path: str, message: str):
    with open(log_txt_path, "a", encoding="utf-8") as f:
        f.write(message.strip() + "\n")

# 📦 Append JSON entry to structured .json log file
def write_log_json(log_json_path: str, entry: dict):
    try:
        if os.path.exists(log_json_path):
            with open(log_json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = []
        else:
            data = []
    except (json.JSONDecodeError, IOError):
        data = []

    data.append(entry)

    with open(log_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# Alias lama (opsional jika sudah tersebar)
tulis_log_txt = write_log_txt
tulis_log_json = write_log_json
