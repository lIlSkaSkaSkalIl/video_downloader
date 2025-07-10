import os
import json
from glob import glob
from datetime import datetime

from uploader.utils.utils import tulis_log_txt, tulis_log_json
from uploader.utils.messages import tampilkan_ringkasan_metadata
from uploader.tools.metadata.extractor import extract_video_info
from uploader.tools.metadata.thumbnail import generate_thumbnail

def proses_semua_video(video_dir, meta_dir, thumb_dir, log_txt_path, log_json_path):
    video_files = sorted(glob(os.path.join(video_dir, "*.*")))
    processed = 0

    for video_path in video_files:
        try:
            ext = os.path.splitext(video_path)[1].lower()
            if ext not in [".mp4", ".mkv", ".avi", ".mov", ".webm"]:
                print(f"⏩ Melewati non-video: {video_path}")
                continue

            basename = os.path.splitext(os.path.basename(video_path))[0]
            thumbnail_path = os.path.join(thumb_dir, f"{basename}_thumb.jpg")
            json_path = os.path.join(meta_dir, f"{basename}_meta.json")

            print(f"📸 Thumbnail: {basename}")
            generate_thumbnail(video_path, thumbnail_path)

            metadata = extract_video_info(video_path, thumbnail_path)

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            ringkas = f"[✅] {metadata['filename']} | {metadata['resolution']} | {metadata['video_codec']}/{metadata['audio_codec']} | {metadata['size_mb']}MB | {metadata['duration_str']}"
            tulis_log_txt(log_txt_path, ringkas)
            tulis_log_json(log_json_path, metadata)

            tampilkan_ringkasan_metadata(metadata)
            processed += 1

        except Exception as e:
            err_filename = os.path.basename(video_path)
            print(f"❌ Gagal: {err_filename} | {e}")
            tulis_log_txt(log_txt_path, f"[❌] {err_filename} | GAGAL - {str(e).splitlines()[0]}")
            tulis_log_json(log_json_path, {
                "status": "error",
                "filename": err_filename,
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    print(f"\n📁 Total diproses: {processed} video\n")
