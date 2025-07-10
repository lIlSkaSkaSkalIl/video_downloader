import os
import json
import time
import glob
import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode

from uploader.core.upload import kirim_video
from uploader.utils.utils import tulis_log_txt, tulis_log_json
from uploader.utils.messages import (
    build_persiapan_msg,
    build_status_awal,
    build_status_sukses,
    build_status_error,
    build_batch_selesai_msg
)
from uploader.utils.labels import LABELS, SEP


# 🔁 Fungsi utama untuk batch upload semua video
async def batch_upload(meta_dir, log_txt, log_json, CHAT_ID, CHANNEL_ID, API_ID, API_HASH, BOT_TOKEN):
    async with Client(
        "upload_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN,
        workers=32,
        in_memory=True
    ) as app:
        meta_files = sorted(glob.glob(os.path.join(meta_dir, "*_meta.json")))
        total = len(meta_files)

        if total == 0:
            msg = f"⚠️ {LABELS['tidak_ada_file']}"
            print(msg)
            await app.send_message(chat_id=CHAT_ID, text=msg, parse_mode=ParseMode.MARKDOWN)
            return

        persiapan_msg = build_persiapan_msg(total)
        print(persiapan_msg)
        await app.send_message(chat_id=CHAT_ID, text=persiapan_msg, parse_mode=ParseMode.MARKDOWN)

        await asyncio.sleep(20)

        # 🚀 Mulai proses upload
        start_time = time.time()
        total_size_bytes = sum(
            os.path.getsize(json.load(open(f))["video_path"])
            for f in meta_files if os.path.exists(f)
        )

        for idx, meta_path in enumerate(meta_files, start=1):
            await kirim_video(
                app, meta_path, idx, total,
                CHAT_ID, CHANNEL_ID,
                log_txt, log_json
            )
            await asyncio.sleep(2)

        # ✅ Selesai
        elapsed = time.time() - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        total_size_mb = total_size_bytes / (1024 * 1024)

        selesai_msg = build_batch_selesai_msg(total, total_size_mb, minutes, seconds)
        print(selesai_msg)
        await app.send_message(chat_id=CHAT_ID, text=selesai_msg, parse_mode=ParseMode.MARKDOWN)

        tulis_log_txt(log_txt, f"[📦] Batch selesai: {total} file, {total_size_mb:.2f} MB, {minutes}m {seconds}s")
        tulis_log_json(log_json, {
            "status": "batch_done",
            "total_files": total,
            "total_size_mb": round(total_size_mb, 2),
            "elapsed_sec": int(elapsed),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
