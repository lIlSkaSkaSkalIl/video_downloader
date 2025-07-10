from .labels import LABELS, SEP

def build_persiapan_msg(total: int) -> str:
    return f"""📦 *{LABELS['persiapan']}*

╭─────────── {LABELS['informasi']} ───────────╮
├📁 {LABELS['total_file']}{SEP} {total} video ditemukan
├⚠️ {LABELS['peringatan']}{SEP} Kirim satu pesan ke channel
│     terlebih dahulu, agar bot mendapatkan izin.
├⏳ {LABELS['status']}{SEP} Menunggu 20 detik...
╰──────────────────────────────╯
"""

def build_status_awal(filename, filesize_mb, duration, current_index, total_count):
    return f"""🚀 Upload Video ({current_index}/{total_count})

╭───────── {LABELS['detail_upload']} ─────────╮
├📁 {LABELS['nama']}{SEP} {filename}
├📦 {LABELS['ukuran']}{SEP} {filesize_mb:.2f} MB
├🕒 {LABELS['durasi']}{SEP} {duration} detik
├⏳ {LABELS['status']}{SEP} Mengunggah...
╰─────────────────────────────╯
"""

def build_status_sukses(filename, current_index, total_count, waktu_upload, meta):
    return f"""✅ Upload Berhasil! ({current_index}/{total_count})

╭───────── {LABELS['detail_upload']} ─────────╮
├🎬 {LABELS['file']}{SEP} {filename}
├📐 {LABELS['resolusi']}{SEP} {meta.get("resolution", "?")}
├🎥 {LABELS['video']}{SEP} {meta.get("video_codec", "?")} ({meta.get("video_bitrate", "?")} bps)
├🎧 {LABELS['audio']}{SEP} {meta.get("audio_codec", "?")} ({meta.get("audio_bitrate", "?")} bps)
├📊 {LABELS['bitrate']}{SEP} {meta.get("bit_rate", "?")} bps
├📦 {LABELS['ukuran']}{SEP} {meta.get("size_mb", 0):.2f} MB
├🕒 {LABELS['durasi']}{SEP} {meta.get("duration", 0)} detik
├📤 {LABELS['status']}{SEP} Sukses
├🧹 {LABELS['cleanup']}{SEP} File dihapus otomatis
├⏱️ {LABELS['waktu']}{SEP} {waktu_upload:.2f} detik
╰─────────────────────────────╯
"""

def build_status_error(filename, error_text, current_index, total_count):
    return f"""❌ Upload Gagal! ({current_index}/{total_count})

╭───────── {LABELS['detail_upload']} ─────────╮
├📁 {LABELS['file']}{SEP} {filename}
├⚠️ {LABELS['error']}{SEP} {error_text}
╰─────────────────────────────╯
"""

def build_batch_selesai_msg(total, total_size_mb, minutes, seconds):
    return f"""✅ *{LABELS['batch_selesai']}*

╭───────── {LABELS['detail_upload']} ─────────╮
├📁 {LABELS['total_file']}{SEP} {total} video
├📦 {LABELS['total_ukuran']}{SEP} {total_size_mb:.2f} MB
├⏱️ {LABELS['total_waktu']}{SEP} {minutes} menit {seconds} detik
╰─────────────────────────────╯

🎉 {LABELS['sukses_upload']}
"""
