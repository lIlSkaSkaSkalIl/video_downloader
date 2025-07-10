import os
import json
import subprocess
from datetime import datetime

def parse_fps(fps_str):
    try:
        num, denom = map(int, fps_str.split("/"))
        return round(num / denom, 2) if denom else 0
    except:
        return 0

def safe_int(val):
    try:
        return int(val)
    except:
        return 0

def extract_video_info(video_path, thumbnail_path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error",
            "-show_entries",
            "format=duration,format_name,size,bit_rate:"
            "stream=index,codec_type,codec_name,width,height,r_frame_rate,avg_frame_rate,bit_rate,channels,sample_rate,pix_fmt,profile",
            "-of", "json", video_path
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed:\n{result.stderr}")

    data = json.loads(result.stdout)
    fmt = data.get("format", {})
    duration = float(fmt.get("duration", 0))
    size_bytes = safe_int(fmt.get("size"))
    bit_rate = safe_int(fmt.get("bit_rate"))

    video_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    audio_stream = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), {})

    return {
        "video_path": video_path,
        "thumbnail_path": thumbnail_path,
        "filename": os.path.basename(video_path),
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
        "video_fps_float": parse_fps(video_stream.get("avg_frame_rate", "0/1")),
        "video_bitrate": safe_int(video_stream.get("bit_rate")),
        "audio_codec": audio_stream.get("codec_name", "unknown"),
        "audio_channels": audio_stream.get("channels", 0),
        "audio_sample_rate": safe_int(audio_stream.get("sample_rate")),
        "audio_bitrate": safe_int(audio_stream.get("bit_rate")),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
