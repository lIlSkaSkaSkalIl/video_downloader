import os
import json
from glob import glob
from datetime import datetime

from uploader.utils.utils import write_log_txt, write_log_json
from uploader.utils.messages import display_metadata_summary
from uploader.tools.metadata.extractor import extract_video_info
from uploader.tools.metadata.thumbnail import generate_thumbnail

VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov", ".webm"]

def process_all_videos(video_dir, metadata_dir, thumbnail_dir, log_txt_path, log_json_path):
    video_files = sorted(glob(os.path.join(video_dir, "*.*")))
    processed_count = 0

    for video_path in video_files:
        try:
            ext = os.path.splitext(video_path)[1].lower()
            if ext not in VIDEO_EXTENSIONS:
                print(f"⏩ Skipping non-video file: {video_path}")
                continue

            basename = os.path.splitext(os.path.basename(video_path))[0]
            thumbnail_path = os.path.join(thumbnail_dir, f"{basename}_thumb.jpg")
            metadata_path = os.path.join(metadata_dir, f"{basename}_meta.json")

            print(f"📸 Generating thumbnail for: {basename}")
            generate_thumbnail(video_path, thumbnail_path)

            metadata = extract_video_info(video_path, thumbnail_path)

            with open(metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)

            summary_line = (
                f"[✅] {metadata['filename']} | {metadata['resolution']} | "
                f"{metadata['video_codec']}/{metadata['audio_codec']} | "
                f"{metadata['size_mb']}MB | {metadata['duration_str']}"
            )

            write_log_txt(log_txt_path, summary_line)
            write_log_json(log_json_path, metadata)

            display_metadata_summary(metadata)
            processed_count += 1

        except Exception as e:
            error_filename = os.path.basename(video_path)
            print(f"❌ Failed: {error_filename} | {e}")

            write_log_txt(log_txt_path, f"[❌] {error_filename} | FAILED - {str(e).splitlines()[0]}")
            write_log_json(log_json_path, {
                "status": "error",
                "filename": error_filename,
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    print(f"\n📁 Total processed: {processed_count} videos\n")
