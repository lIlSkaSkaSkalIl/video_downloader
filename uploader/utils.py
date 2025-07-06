import os
import json
import re

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
    NAMA_LABEL = "𝙉𝙖𝙢𝙖"
    UKURAN_LABEL = "𝙐𝙠𝙪𝙧𝙖𝙣"
    DURASI_LABEL = "𝘿𝙪𝙧𝙖𝙨𝙞"
    STATUS_LABEL = "𝙎𝙩𝙖𝙩𝙪𝙨"
    SEP = " »"

    return f"""🚀 Upload Video ({current_index}/{total_count})

╭────────── Detail Upload ──────────╮
├ 📁 {NAMA_LABEL} {SEP} {filename}
├ 📦 {UKURAN_LABEL} {SEP} {filesize_mb:.2f} MB
├ 🕒 {DURASI_LABEL} {SEP} {duration} detik
├ ⏳ {STATUS_LABEL} {SEP} Mengunggah...
╰─────────────────────────────╯
"""

# ✅ Status sukses upload
def status_sukses(filename, current_index, total_count, waktu_upload, meta):
    FILE_LABEL = "𝙁𝙞𝙡𝙚"
    RESOLUSI_LABEL = "𝙍𝙚𝙨𝙤𝙡𝙪𝙨𝙞"
    VIDEO_LABEL = "𝙑𝙞𝙙𝙚𝙤"
    AUDIO_LABEL = "𝘼𝙪𝙙𝙞𝙤"
    BITRATE_LABEL = "𝘽𝙞𝙩𝙧𝙖𝙩𝙚"
    UKURAN_LABEL = "𝙐𝙠𝙪𝙧𝙖𝙣"
    DURASI_LABEL = "𝘿𝙪𝙧𝙖𝙨𝙞"
    STATUS_LABEL = "𝙎𝙩𝙖𝙩𝙪𝙨"
    CLEANUP_LABEL = "𝘾𝙡𝙚𝙖𝙣𝙪𝙥"
    WAKTU_LABEL = "𝙒𝙖𝙠𝙩𝙪"
    SEP = " »"

    return f"""✅ Upload Berhasil! ({current_index}/{total_count})

╭────────── Detail Upload ──────────╮
├ 🎬 {FILE_LABEL} {SEP} {filename}
├ 📐 {RESOLUSI_LABEL} {SEP} {meta.get("resolution", "?")}
├ 🎥 {VIDEO_LABEL} {SEP} {meta.get("video_codec", "?")} ({meta.get("video_bitrate", "?")} bps)
├ 🎧 {AUDIO_LABEL} {SEP} {meta.get("audio_codec", "?")} ({meta.get("audio_bitrate", "?")} bps)
├ 📊 {BITRATE_LABEL} {SEP} {meta.get("bit_rate", "?")} bps
├ 📦 {UKURAN_LABEL} {SEP} {meta.get("size_mb", 0):.2f} MB
├ 🕒 {DURASI_LABEL} {SEP} {meta.get("duration", 0)} detik
├ 📤 {STATUS_LABEL} {SEP} Sukses
├ 🧹 {CLEANUP_LABEL} {SEP} File dihapus otomatis
├ ⏱️ {WAKTU_LABEL} {SEP} {waktu_upload:.2f} detik
╰─────────────────────────────╯
"""

# ❌ Status gagal upload
def status_error(filename, error_text, current_index, total_count):
    FILE_LABEL = "𝙁𝙞𝙡𝙚"
    ERROR_LABEL = "𝙀𝙧𝙧𝙤𝙧"
    SEP = " »"

    return f"""❌ Upload Gagal! ({current_index}/{total_count})

╭────────── Detail Upload ──────────╮
├ 📁 {FILE_LABEL} {SEP} {filename}
├ ⚠️ {ERROR_LABEL} {SEP} {error_text}
╰─────────────────────────────╯
"""
