import os
import json
import subprocess
from datetime import datetime

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
