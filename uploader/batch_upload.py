import os, json, time, glob, re, traceback
from tqdm import tqdm
from pyrogram import Client
from pyrogram.enums import ParseMode

# 🔠 Markdown escape
def escape_md(text):
    return re.sub(r'([*\[\]~`>#+\-=|{}!])', r'\\\1', text)

def tulis_log_txt(log_txt, teks):
    with open(log_txt, "a", encoding="utf-8") as f:
        f.write(teks.strip() + "\n")

def tulis_log_json(log_json, entry):
    try:
        if os.path.exists(log_json):
            with open(log_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = []
    except:
        data = []
    data.append(entry)
    with open(log_json, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def progress(current, total):
    global bar
    bar.update(current - bar.n)

def status_awal(filename, filesize_mb, duration, current_index, total_count):
    return f"""🚀 Upload Video ({current_index}/{total_count})

╭────────── Detail Upload ──────────╮
📁 Nama     : {filename}
📦 Ukuran   : {filesize_mb:.2f} MB
🕒 Durasi   : {duration} detik
⏳ Status   : Mengunggah...
╰─────────────────────────────╯
"""

def status_sukses(filename, current_index, total_count, waktu_upload, meta):
    return f"""✅ Upload Berhasil! ({current_index}/{total_count})

╭────────── Detail Upload ──────────╮
🎬 File     : {filename}
📐 Resolusi: {meta.get("resolution", "?")}
🎥 Video    : {meta.get("video_codec", "?")} ({meta.get("video_bitrate", "?")} bps)
🎧 Audio    : {meta.get("audio_codec", "?")} ({meta.get("audio_bitrate", "?")} bps)
📊 Bitrate  : {meta.get("bit_rate", "?")} bps
📦 Ukuran   : {meta.get("size_mb", 0):.2f} MB
🕒 Durasi   : {meta.get("duration", 0)} detik
📤 Status   : Sukses
🧹 Cleanup  : File dihapus otomatis
⏱️ Waktu    : {waktu_upload:.2f} detik
╰─────────────────────────────╯
"""

def status_error(filename, error_text, current_index, total_count):
    return f"""❌ Upload Gagal! ({current_index}/{total_count})

╭────────── Detail Upload ──────────╮
📁 File     : {filename}
⚠️ Error    : {error_text}
╰─────────────────────────────╯
"""

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

        await app.send_message(chat_id=CHAT_ID, text=status_awal(filename, filesize_mb, duration, current_index, total_count), parse_mode=ParseMode.MARKDOWN)

        global bar
        bar = tqdm(total=filesize, unit='B', unit_scale=True, desc=f"📤 Upload {current_index}/{total_count}", dynamic_ncols=True)

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
        await app.send_message(chat_id=CHAT_ID, text=status_sukses(filename, current_index, total_count, waktu_upload, meta), parse_mode=ParseMode.MARKDOWN)

        tulis_log_txt(log_txt, f"[✅] {meta['filename']} | {meta.get('resolution')} | {meta.get('video_codec')}/{meta.get('audio_codec')} | {meta.get('size_mb')}MB | {meta.get('duration')}s | {waktu_upload}s")
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

        await app.send_message(chat_id=CHAT_ID, text=status_error(escape_md(err_filename), escape_md(error_msg), current_index, total_count), parse_mode=ParseMode.MARKDOWN)
        tulis_log_txt(log_txt, f"[❌] {err_filename} | GAGAL - {error_msg.strip().splitlines()[0]}")
        tulis_log_json(log_json, {
            "status": "error",
            "filename": err_filename,
            "error": error_msg.strip().splitlines()[0],
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })

async def batch_upload(meta_dir, log_txt, log_json, CHAT_ID, CHANNEL_ID, API_ID, API_HASH, BOT_TOKEN):
    async with Client("upload_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN) as app:
        meta_files = sorted(glob.glob(os.path.join(meta_dir, "*_meta.json")))
        total = len(meta_files)

        if total == 0:
            await app.send_message(chat_id=CHAT_ID, text="⚠️ Tidak ada file video yang ditemukan untuk diupload.", parse_mode=ParseMode.MARKDOWN)
            return

        start_time = time.time()
        total_size_bytes = sum(os.path.getsize(json.load(open(f))["video_path"]) for f in meta_files if os.path.exists(f))

        for idx, meta_path in enumerate(meta_files, start=1):
            await kirim_video(app, meta_path, idx, total, CHAT_ID, CHANNEL_ID, log_txt, log_json)
            await asyncio.sleep(2)

        elapsed = time.time() - start_time
        minutes, seconds = divmod(int(elapsed), 60)
        total_size_mb = total_size_bytes / (1024 * 1024)

        await app.send_message(chat_id=CHAT_ID, text=f"""✅ Batch Upload Selesai!!

📁 Total File   : {total} video
📦 Total Ukuran : {total_size_mb:.2f} MB
⏱️ Total Waktu  : {minutes} menit {seconds} detik

🎉 Semua video berhasil diupload!
""", parse_mode=ParseMode.MARKDOWN)

        tulis_log_txt(log_txt, f"[📦] Batch selesai: {total} file, {total_size_mb:.2f} MB, {minutes}m {seconds}s")
        tulis_log_json(log_json, {
            "status": "batch_done",
            "total_files": total,
            "total_size_mb": round(total_size_mb, 2),
            "elapsed_sec": int(elapsed),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        })
