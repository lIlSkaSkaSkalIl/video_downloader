import os
import json
import subprocess
from glob import glob
from datetime import datetime

from uploader.utils.utils import tulis_log_txt, tulis_log_json
from uploader.utils.messages import tampilkan_ringkasan_metadata  # ✅ Import ringkasan

# 🎞️ Ambil metadata dari satu video
def extract_video_info(path, thumbnail_path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries",
            "format=duration,format_name,size,bit_rate:"
            "stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,bit_rate,channels,sample_rate,pix_fmt,profile",
            "-of", "json", path
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe gagal:\n{result.stderr}")

    data = json.loads(result.stdout)
    fmt = data.get("format", {})
    duration = float(fmt.get("duration", 0))
    size_bytes = int(fmt.get("size", 0))
    bit_rate = int(fmt.get("bit_rate", 0)) if "bit_rate" in fmt else None

    video_stream = next((s for s in data["streams"] if s["codec_type"] == "video"), {})
    audio_stream = next((s for s in data["streams"] if s["codec_type"] == "audio"), {})

    return {
        "video_path": path,
        "thumbnail_path": thumbnail_path,
        "filename": os.path.basename(path),
        "duration": int(duration),
        "duration_str": f"{int(duration // 60)}:{int(duration % 60):02d}",
        "format": fmt.get("format_name", "unknown"),
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "bit_rate": bit_rate,
        "resolution": f"{video_stream.get('width', 0)}x{video_stream.get('height', 0)}",
        "width": video_stream.get("width", 0),
        "height": video_stream.get("height", 0),
        "video_codec": video_stream.get("codec_name", "unknown"),
        "video_pix_fmt": video_stream.get("pix_fmt", "unknown"),
        "video_profile": video_stream.get("profile", "unknown"),
        "video_fps": video_stream.get("avg_frame_rate", "0/1"),
        "video_bitrate": int(video_stream.get("bit_rate", 0)) if "bit_rate" in video_stream else None,
        "audio_codec": audio_stream.get("codec_name", "unknown"),
        "audio_channels": audio_stream.get("channels", 0),
        "audio_sample_rate": int(audio_stream.get("sample_rate", 0)) if "sample_rate" in audio_stream else None,
        "audio_bitrate": int(audio_stream.get("bit_rate", 0)) if "bit_rate" in audio_stream else None,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# 📸 Generate thumbnail dari video
def generate_thumbnail(video_path, thumbnail_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-ss", "00:00:01.000",
        "-vframes", "1",
        "-q:v", "2",
        thumbnail_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# 🔁 Proses banyak file video
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

            # ✅ Log
            ringkas = f"[✅] {metadata['filename']} | {metadata['resolution']} | {metadata['video_codec']}/{metadata['audio_codec']} | {metadata['size_mb']}MB | {metadata['duration_str']}"
            tulis_log_txt(log_txt_path, ringkas)
            tulis_log_json(log_json_path, metadata)

            # 📊 Ringkasan
            tampilkan_ringkasan_metadata(metadata)  # ✅ Dipindah ke messages.py

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
