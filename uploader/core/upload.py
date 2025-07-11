import os
import json
import time
import traceback
from tqdm import tqdm
from pyrogram.enums import ParseMode

from utils.utils import escape_md, write_log_txt, write_log_json
from utils.messages import (
    build_upload_start_status,
    build_upload_success_status,
    build_upload_error_status
)

def create_progress_callback(total_size):
    bar = tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        desc="📤 Uploading",
        dynamic_ncols=True
    )
    def progress(current, total):
        bar.update(current - bar.n)
    return progress, bar


async def send_video(app, meta_path, index, total_count, chat_id, channel_id, log_txt_path, log_json_path):
    try:
        start_time = time.time()

        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        video_path = meta["video_path"]
        thumbnail_path = meta["thumbnail_path"]
        filename = escape_md(meta["filename"])
        duration = meta["duration"]
        file_size = os.path.getsize(video_path)
        file_size_mb = file_size / (1024 * 1024)

        await app.send_message(
            chat_id=chat_id,
            text=build_upload_start_status(filename, file_size_mb, duration, index, total_count),
            parse_mode=ParseMode.MARKDOWN
        )

        progress_callback, bar = create_progress_callback(file_size)

        await app.send_video(
            chat_id=channel_id,
            video=video_path,
            thumb=thumbnail_path,
            caption=filename,
            duration=duration,
            supports_streaming=True,
            progress=progress_callback
        )
        bar.close()

        upload_time = round(time.time() - start_time, 2)

        await app.send_message(
            chat_id=chat_id,
            text=build_upload_success_status(filename, index, total_count, upload_time, meta),
            parse_mode=ParseMode.MARKDOWN
        )

        write_log_txt(
            log_txt_path,
            f"[✅] {meta['filename']} | {meta.get('resolution')} | "
            f"{meta.get('video_codec')}/{meta.get('audio_codec')} | "
            f"{meta.get('size_mb')}MB | {meta.get('duration')}s | {upload_time}s"
        )
        write_log_json(log_json_path, {
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
            "upload_time": upload_time,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

        for path in [thumbnail_path, meta_path, video_path]:
            if os.path.exists(path):
                os.remove(path)

    except Exception as e:
        error_msg = str(e) or traceback.format_exc()
        err_filename = meta.get("filename", os.path.basename(meta_path))

        await app.send_message(
            chat_id=chat_id,
            text=build_upload_error_status(escape_md(err_filename), escape_md(error_msg), index, total_count),
            parse_mode=ParseMode.MARKDOWN
        )

        write_log_txt(
            log_txt_path,
            f"[❌] {err_filename} | FAILED - {error_msg.strip().splitlines()[0]}"
        )
        write_log_json(log_json_path, {
            "status": "error",
            "filename": err_filename,
            "error": error_msg.strip().splitlines()[0],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
