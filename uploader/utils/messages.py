import os
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

def print_metadata_summary(metadata: dict):
    def get(val, default="N/A"):
        return val if val not in [None, "", 0] else default

    print(f"""
✅ Metadata: {get(metadata['filename'])}
╭🖼️ Thumbnail     : {os.path.basename(get(metadata['thumbnail_path']))}
├⏱️ Duration      : {get(metadata['duration_str'])}
├📐 Resolution    : {get(metadata['resolution'])}
├↔️ Width         : {get(metadata['width'])} px
├↕️ Height        : {get(metadata['height'])} px
├📀 Format        : {get(metadata['format'], 'unknown').upper()}
├💾 Size          : {get(metadata['size_mb'])} MB
├📊 Bitrate Total : {get(metadata.get('bit_rate'))} bps
├🎥 Video Codec   : {get(metadata['video_codec'])}
├🌈 PixFmt        : {get(metadata['video_pix_fmt'])}
├🧬 Profile       : {get(metadata['video_profile'])}
├🎞️ FPS           : {get(metadata['video_fps'])}
├🎞️ Video Bitrate : {get(metadata.get('video_bitrate'))} bps
├🎧 Audio Codec   : {get(metadata['audio_codec'])}
├🔊 Channels      : {get(metadata.get('audio_channels'))}
├🎚️ Sample Rate   : {get(metadata.get('audio_sample_rate'))} Hz
├🎧 Audio Bitrate : {get(metadata.get('audio_bitrate'))} bps
╰🕓 Timestamp     : {get(metadata['timestamp'])}
""")

# Alias lama (opsional untuk backward compatibility)
tampilkan_ringkasan_metadata = print_metadata_summary
