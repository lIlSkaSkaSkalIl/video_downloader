import os
import datetime
from .labels import LABELS, SEP
from utils.utils import log

# ══════════════════════════════════════════════
# 📦 Status Persiapan Batch
# ══════════════════════════════════════════════

def build_preparation_message(total: int) -> str:
    return f"""📦 {LABELS['preparation']}

{LABELS['info']} 

╭📁 {LABELS['total_files']}{SEP} {total} videos found
├⚠️ {LABELS['warning']}{SEP} Send a message to the channel
│     first to allow bot access.
╰⏳ {LABELS['status']}{SEP} Waiting for 20 seconds...
"""

# ══════════════════════════════════════════════
# 🚀 Status Upload
# ══════════════════════════════════════════════

def build_upload_start_status(filename, filesize_mb, duration, current_index, total_count):
    return f"""🚀 Uploading Video ({current_index}/{total_count})

{LABELS['upload_details']} 

╭📁 {LABELS['name']}{SEP} {filename}
├📦 {LABELS['size']}{SEP} {filesize_mb:.2f} MB
├🕒 {LABELS['duration']}{SEP} {duration} seconds
╰⏳ {LABELS['status']}{SEP} Uploading...
"""

def build_upload_success_status(filename, current_index, total_count, upload_time, meta):
    return f"""✅ Upload Successful! ({current_index}/{total_count})

 {LABELS['upload_details']} 
 
╭🎬 {LABELS['file']}{SEP} {filename}
├📐 {LABELS['resolution']}{SEP} {meta.get("resolution", "?")}
├🎥 {LABELS['video']}{SEP} {meta.get("video_codec", "?")} ({meta.get("video_bitrate", "?")} bps)
├🎧 {LABELS['audio']}{SEP} {meta.get("audio_codec", "?")} ({meta.get("audio_bitrate", "?")} bps)
├📊 {LABELS['bitrate']}{SEP} {meta.get("bit_rate", "?")} bps
├📦 {LABELS['size']}{SEP} {meta.get("size_mb", 0):.2f} MB
├🕒 {LABELS['duration']}{SEP} {meta.get("duration", 0)} seconds
├📤 {LABELS['status']}{SEP} Success
├🧹 {LABELS['cleanup']}{SEP} File auto-deleted
╰⏱️ {LABELS['time']}{SEP} {upload_time:.2f} seconds
"""

def build_upload_error_status(filename, error_text, current_index, total_count):
    return f"""❌ Upload Failed! ({current_index}/{total_count})

╭───────── {LABELS['upload_details']} ─────────╮
├📁 {LABELS['file']}{SEP} {filename}
├⚠️ {LABELS['error']}{SEP} {error_text}
╰─────────────────────────────╯
"""

def build_batch_complete_message(total, total_size_mb, minutes, seconds):
    return f"""✅ {LABELS['batch_done']}

{LABELS['upload_details']} 

╭📁 {LABELS['total_files']}{SEP} {total} videos
├📦 {LABELS['total_size']}{SEP} {total_size_mb:.2f} MB
╰⏱️ {LABELS['total_time']}{SEP} {minutes} minutes {seconds} seconds

🎉 {LABELS['upload_success']}
"""

# ══════════════════════════════════════════════
# 📊 Ringkasan Metadata
# ══════════════════════════════════════════════

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

tampilkan_ringkasan_metadata = print_metadata_summary  # alias kompatibel

# ══════════════════════════════════════════════
# 📥 Download Twitter Summary
# ══════════════════════════════════════════════

def build_twitter_summary(tweet_url, tweet_id, use_cookies, downloaded_files, video_dir, duration_seconds):
    total_size_mb = sum(os.path.getsize(f) for f in downloaded_files) / (1024 * 1024)
    file_names = [os.path.basename(f) for f in downloaded_files]
    duration_str = f"{int(duration_seconds // 60)} menit {int(duration_seconds % 60)} detik"

    summary = f"""
📊 Download Summary:

╭📌 Tweet URL       : {tweet_url}
├🆔 Tweet ID        : {tweet_id}
├🔐 Cookies Used    : {'✅ Yes' if use_cookies else '❌ No'}
├📁 Total Videos    : {len(downloaded_files)} file(s)
├💾 Total Size      : {total_size_mb:.2f} MB
├⏱️ Saved Time      : {duration_str}
├🕒 Finished At     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
├📂 Output Folder   : {video_dir}
╰📜 File List       :
"""
    for i, fname in enumerate(file_names, 1):
        summary += f"   {i}. {fname}\n"
    return summary.strip()

# ══════════════════════════════════════════════
# 📺 Download Non-Twitter (m3u8, GDrive, Direct)
# ══════════════════════════════════════════════

def show_download_info(video_url, download_type, output_path):
    print(f"┌─🎯 Link           : {video_url}")
    print(f"├─🧩 Jenis Unduhan  : {download_type}")
    print(f"└─📁 Lokasi Simpan  : {output_path}")

def download_summary(path, duration_sec=None): 
    if os.path.exists(path):
        size = os.path.getsize(path) / (1024 * 1024)
        print(f"\n✅ Selesai! File disimpan di: {path}")
        print(f"📦 Ukuran file: {size:.2f} MB")
        if duration_sec is not None:
            print(f"⏱️ Waktu unduhan: {duration_sec:.2f} detik")
    else:
        log("Download selesai tapi file tidak ditemukan.", icon="⚠️")

def show_tool_detection(tool):
    log(f"Menggunakan alat unduhan: {tool}", icon="🚀")

def build_m3u8_download_start(video_url, output_dir, output_name):
    return f"""
📥 Starting download:

┌🔗 Link         : {video_url}
├📂 Output Dir   : {output_dir}
├📄 File Name    : {output_name}
└🛠️ Downloader   : yt-dlp + aria2c (16 parallel connections)
"""

def build_m3u8_summary(output_dir, output_name, size_mb, duration_sec):
    return f"""
✅ Download Complete!

┌📂 Folder saved   : {output_dir}
├📄 File name      : {output_name}
├📦 File size      : {size_mb:.2f} MB
└⏱️ Download time  : {duration_sec:.2f} seconds
"""
