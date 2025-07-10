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

def build_batch_selesai_msg(total, total_size_mb, minutes, seconds) -> str:
    return f"""✅ *{LABELS['batch_selesai']}*

╭───────── {LABELS['detail_upload']} ─────────╮
├📁 {LABELS['total_file']}{SEP} {total} video
├📦 {LABELS['total_ukuran']}{SEP} {total_size_mb:.2f} MB
├⏱️ {LABELS['total_waktu']}{SEP} {minutes} menit {seconds} detik
╰─────────────────────────────╯

🎉 {LABELS['sukses_upload']}
"""
