import os
import json
import time
import traceback
from tqdm import tqdm
from pyrogram.enums import ParseMode
from .utils import (
    escape_md,
    tulis_log_txt,
    tulis_log_json,
    status_awal,
    status_sukses,
    status_error
)

# 📊 Fungsi progress bar
def progress(current, total):
    global bar
    bar.update(current - bar.n)

# 📤 Fungsi upload satu video
async def kirim_video(app, meta_path, current_index, total_count, CHAT_ID, CHANNEL_ID, log_txt, log_json):
    try:
        start_upload = time.time()

        with open(meta_path, "r") as f:
            meta = json.load(f)

        video_path = meta["video_path"]
        thumbnail_path = meta["thumbnail_path"]
        filename = escape_md(meta["filename"])
        duration = meta["duration"]
        filesize = os.path.getsize(video_path)
        filesize_mb = filesize / (1024 * 1024)

        await app.send_message(
            chat_id=CHAT_ID,
            text=status_awal(filename, filesize_mb, duration, current_index, total_count),
            parse_mode=ParseMode.MARKDOWN
        )

        global bar
        bar = tqdm(
            total=filesize,
            unit='B',
            unit_scale=True,
            desc=f"📤 Upload {current_index}/{total_count}",
            dynamic_ncols=True
        )

        await app.send_video(
            chat_id=CHANNEL_ID,
            video=video_path,
            thumb=thumbnail_path,
            caption=filename,
            duration=duration,
            supports_streaming=True,
            progress=progress
        )
        bar.close()

        waktu_upload = round(time.time() - start_upload, 2)

        await app.send_message(
            chat_id=CHAT_ID,
            text=status_sukses(filename, current_index, total_count, waktu_upload, meta),
            parse_mode=ParseMode.MARKDOWN
        )

        tulis_log_txt(
            log_txt,
            f"[✅] {meta['filename']} | {meta.get('resolution')} | {meta.get('video_codec')}/{meta.get('audio_codec')} | {meta.get('size_mb')}MB | {meta.get('duration')}s | {waktu_upload}s"
        )

        tulis_log_json(log_json, {
            "status": "success",
            "filename": meta["filename"],
            "resolution": meta.get("resolution"),
            "video_codec": meta.get("video_codec"),
            "audio_codec": meta.get("audio_codec"),
            "duration": meta.get("duration"),
            "size_mb": meta.get("size_mb"),
            "bit_rate": meta.get("bit_rate"),
            "video_bitrate": meta.get("video_bitrate"),
            "audio_bitrate": meta.get("audio_bitrate"),
            "upload_time": waktu_upload,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

        for f in [thumbnail_path, meta_path, video_path]:
            if os.path.exists(f):
                os.remove(f)

    except Exception as e:
        error_msg = str(e) or traceback.format_exc()
        err_filename = meta.get("filename", os.path.basename(meta_path))

        await app.send_message(
            chat_id=CHAT_ID,
            text=status_error(escape_md(err_filename), escape_md(error_msg), current_index, total_count),
            parse_mode=ParseMode.MARKDOWN
        )

        tulis_log_txt(
            log_txt,
            f"[❌] {err_filename} | GAGAL - {error_msg.strip().splitlines()[0]}"
        )

        tulis_log_json(log_json, {
            "status": "error",
            "filename": err_filename,
            "error": error_msg.strip().splitlines()[0],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
