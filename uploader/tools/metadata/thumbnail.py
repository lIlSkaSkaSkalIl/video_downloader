import subprocess
import json

def get_video_duration(video_path):
    """Mengambil durasi video dalam detik."""
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", video_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        duration = float(json.loads(result.stdout)["format"]["duration"])
        return duration
    except Exception as e:
        print(f"⚠️ Gagal mendapatkan durasi: {video_path}\n{e}\n{result.stderr.decode()}")
        return None

def seconds_to_timestamp(seconds):
    """Mengubah detik ke format HH:MM:SS.000"""
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}.000"

def generate_thumbnail(video_path, thumbnail_path):
    duration = get_video_duration(video_path)

    if duration is not None and duration > 0:
        if duration < 5:
            print(f"⚠️ Video terlalu pendek (<5s): {video_path}")
            timestamp = "00:00:01.000"
        else:
            timestamp = seconds_to_timestamp(duration * 0.3)
    else:
        print(f"⚠️ Durasi tidak ditemukan, fallback ke detik ke-3: {video_path}")
        timestamp = "00:00:03.000"

    subprocess.run([
        "ffmpeg", "-y",
        "-ss", timestamp,
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        thumbnail_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
