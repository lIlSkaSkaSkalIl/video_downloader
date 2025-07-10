import os
import json
import time
import glob
import asyncio
from pyrogram import Client
from pyrogram.enums import ParseMode

from uploader.core.upload import kirim_video
from uploader.utils.utils import tulis_log_txt, tulis_log_json
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
            await app.send_message(
                chat_id=CHAT_ID,
                text=msg,
                parse_mode=ParseMode.MARKDOWN
            )
            return

        # ⏳ Tampilkan info persiapan di Telegram
        persiapan_msg = f"""📦 *{LABELS['persiapan']}*

╭─────────── {LABELS['informasi']} ───────────╮
├📁 {LABELS['total_file']}{SEP} {total} video ditemukan
├⚠️ {LABELS['peringatan']}{SEP} Kirim satu pesan ke channel
│     terlebih dahulu, agar bot mendapatkan izin.
├⏳ {LABELS['status']}{SEP} Menunggu 20 detik...
╰──────────────────────────────╯
"""
        await app.send_message(chat_id=CHAT_ID, text=persiapan_msg, parse_mode=ParseMode.MARKDOWN)
        print(persiapan_msg)

        await asyncio.sleep(20)

        # 🚀 Mulai proses upload
        start_time = time.time()
        total_size_bytes = sum(
            os.path.getsize(json.load(open(f))["video_path"])
            for f in meta_files if os.path.exists(f)
        )

        for idx, meta_path in enumerate(meta_files, start=1):
            await kirim_video(app, meta_path, idx, total, CHAT_ID, CHANNEL_ID, log_txt, log_json)
            await asyncio.sleep(2)

        # ✅ Upload selesai
        elapsed = time.time() - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        total_size_mb = total_size_bytes / (1024 * 1024)

        selesai_msg = f"""✅ *{LABELS['batch_selesai']}*

╭───────── {LABELS['detail_upload']} ─────────╮
├📁 {LABELS['total_file']}{SEP} {total} video
├📦 {LABELS['total_ukuran']}{SEP} {total_size_mb:.2f} MB
├⏱️ {LABELS['total_waktu']}{SEP} {minutes} menit {seconds} detik
╰─────────────────────────────╯

🎉 {LABELS['sukses_upload']}
"""
        await app.send_message(chat_id=CHAT_ID, text=selesai_msg, parse_mode=ParseMode.MARKDOWN)
        print(selesai_msg)

        tulis_log_txt(log_txt, f"[📦] Batch selesai: {total} file, {total_size_mb:.2f} MB, {minutes}m {seconds}s")
        tulis_log_json(log_json, {
            "status": "batch_done",
            "total_files": total,
            "total_size_mb": round(total_size_mb, 2),
            "elapsed_sec": int(elapsed),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
