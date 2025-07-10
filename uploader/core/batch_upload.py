import os
import json
import time
import glob
import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode

from uploader.core.upload import send_video
from uploader.utils.utils import write_log_txt, write_log_json
from uploader.utils.messages import (
    build_preparation_message,
    build_upload_start_status,
    build_upload_success_status,
    build_upload_error_status,
    build_batch_complete_message
)
from uploader.utils.labels import LABELS, SEPARATOR


async def batch_upload(
    metadata_dir,
    log_txt_path,
    log_json_path,
    chat_id,
    channel_id,
    api_id,
    api_hash,
    bot_token
):
    async with Client(
        "upload_bot",
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        workers=32,
        in_memory=True
    ) as app:
        metadata_files = sorted(glob.glob(os.path.join(metadata_dir, "*_meta.json")))
        total_files = len(metadata_files)

        if total_files == 0:
            warning_msg = f"⚠️ {LABELS['no_file_found']}"
            print(warning_msg)
            await app.send_message(chat_id=chat_id, text=warning_msg, parse_mode=ParseMode.MARKDOWN)
            return

        preparation_msg = build_preparation_msg(total_files)
        print(preparation_msg)
        await app.send_message(chat_id=chat_id, text=preparation_msg, parse_mode=ParseMode.MARKDOWN)

        await asyncio.sleep(20)

        # 🚀 Start upload
        start_time = time.time()
        start_timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        total_size_bytes = 0

        for meta_path in metadata_files:
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                    video_path = metadata.get("video_path", "")
                    if os.path.exists(video_path):
                        total_size_bytes += os.path.getsize(video_path)
            except Exception as e:
                print(f"⚠️ Failed to read metadata: {meta_path} | {e}")

        for index, meta_path in enumerate(metadata_files, start=1):
            await send_video(
                app, meta_path, index, total_files,
                chat_id, channel_id,
                log_txt_path, log_json_path
            )
            await asyncio.sleep(2)

        # ✅ Done
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        total_size_mb = total_size_bytes / (1024 * 1024)

        complete_msg = build_batch_complete_msg(total_files, total_size_mb, minutes, seconds)
        print(complete_msg)
        await app.send_message(chat_id=chat_id, text=complete_msg, parse_mode=ParseMode.MARKDOWN)

        write_log_txt(
            log_txt_path,
            f"[📦] Batch complete: {total_files} files, {total_size_mb:.2f} MB, {minutes}m {seconds}s"
        )

        write_log_json(log_json_path, {
            "status": "batch_done",
            "total_files": total_files,
            "total_size_mb": round(total_size_mb, 2),
            "elapsed_sec": int(elapsed_time),
            "start_time": start_timestamp,
            "end_time": time.strftime("%Y-%m-%d %H:%M:%S")
        })
