import os
import json
import time
import glob
import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode
from .upload import kirim_video
from .utils import tulis_log_txt, tulis_log_json

# 🔁 Fungsi utama untuk batch upload semua video
async def batch_upload(meta_dir, log_txt, log_json, CHAT_ID, CHANNEL_ID, API_ID, API_HASH, BOT_TOKEN):
    async with Client("upload_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        meta_files = sorted(glob.glob(os.path.join(meta_dir, "*_meta.json")))
        total = len(meta_files)

        if total == 0:
            await app.send_message(
                chat_id=CHAT_ID,
                text="⚠️ Tidak ada file video yang ditemukan untuk diupload.",
                parse_mode=ParseMode.MARKDOWN
            )
            return

        start_time = time.time()
        total_size_bytes = sum(
            os.path.getsize(json.load(open(f))["video_path"])
            for f in meta_files if os.path.exists(f)
        )

        for idx, meta_path in enumerate(meta_files, start=1):
            await kirim_video(app, meta_path, idx, total, CHAT_ID, CHANNEL_ID, log_txt, log_json)
            await asyncio.sleep(2)

        elapsed = time.time() - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        total_size_mb = total_size_bytes / (1024 * 1024)

        await app.send_message(
            chat_id=CHAT_ID,
            text=f"""✅ Batch Upload Selesai!!

📁 Total File   : {total} video
📦 Total Ukuran : {total_size_mb:.2f} MB
⏱️ Total Waktu  : {minutes} menit {seconds} detik

🎉 Semua video berhasil diupload!
""",
            parse_mode=ParseMode.MARKDOWN
        )

        tulis_log_txt(log_txt, f"[📦] Batch selesai: {total} file, {total_size_mb:.2f} MB, {minutes}m {seconds}s")

        tulis_log_json(log_json, {
            "status": "batch_done",
            "total_files": total,
            "total_size_mb": round(total_size_mb, 2),
            "elapsed_sec": int(elapsed),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
