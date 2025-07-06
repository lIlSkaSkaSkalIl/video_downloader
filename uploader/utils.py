import os
import json
import re
from .labels import LABELS, SEP

# 🔠 Escape karakter Markdown agar tidak error saat parsing
def escape_md(text):
    return re.sub(r'([*\[\]~`>#+\-=|{}!])', r'\\\1', text)

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

# ⏳ Status awal upload
def status_awal(filename, filesize_mb, duration, current_index, total_count):
    return f"""🚀 Upload Video ({current_index}/{total_count})

╭────────── {LABELS['detail_upload']} ──────────╮
├ 📁 {LABELS['nama']}{SEP} {filename}
├ 📦 {LABELS['ukuran']}{SEP} {filesize_mb:.2f} MB
├ 🕒 {LABELS['durasi']}{SEP} {duration} detik
├ ⏳ {LABELS['status']}{SEP} Mengunggah...
╰─────────────────────────────╯
"""

# ✅ Status sukses upload
def status_sukses(filename, current_index, total_count, waktu_upload, meta):
    return f"""✅ Upload Berhasil! ({current_index}/{total_count})

╭────────── {LABELS['detail_upload']} ──────────╮
├ 🎬 {LABELS['file']}{SEP} {filename}
├ 📐 {LABELS['resolusi']}{SEP} {meta.get("resolution", "?")}
├ 🎥 {LABELS['video']}{SEP} {meta.get("video_codec", "?")} ({meta.get("video_bitrate", "?")} bps)
├ 🎧 {LABELS['audio']}{SEP} {meta.get("audio_codec", "?")} ({meta.get("audio_bitrate", "?")} bps)
├ 📊 {LABELS['bitrate']}{SEP} {meta.get("bit_rate", "?")} bps
├ 📦 {LABELS['ukuran']}{SEP} {meta.get("size_mb", 0):.2f} MB
├ 🕒 {LABELS['durasi']}{SEP} {meta.get("duration", 0)} detik
├ 📤 {LABELS['status']}{SEP} Sukses
├ 🧹 {LABELS['cleanup']}{SEP} File dihapus otomatis
├ ⏱️ {LABELS['waktu']}{SEP} {waktu_upload:.2f} detik
╰─────────────────────────────╯
"""

# ❌ Status gagal upload
def status_error(filename, error_text, current_index, total_count):
    return f"""❌ Upload Gagal! ({current_index}/{total_count})

╭────────── {LABELS['detail_upload']} ──────────╮
├ 📁 {LABELS['file']}{SEP} {filename}
├ ⚠️ {LABELS['error']}{SEP} {error_text}
╰─────────────────────────────╯
"""
