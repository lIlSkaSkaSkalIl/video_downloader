import os
from .labels import LABELS, SEP


def build_preparation_message(total: int) -> str:
    return f"""📦 {LABELS['preparation']}

{LABELS['info']} 

╭📁 {LABELS['total_files']}{SEP} {total} videos found
├⚠️ {LABELS['warning']}{SEP} Send a message to the channel
│     first to allow bot access.
╰⏳ {LABELS['status']}{SEP} Waiting for 20 seconds...
"""


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


# Backward compatibility alias
tampilkan_ringkasan_metadata = print_metadata_summary
