import subprocess
import json
import os

def get_video_duration(video_path):
    """Returns duration in seconds, or None if failed."""
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json", video_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        data = json.loads(result.stdout)
        return float(data["format"]["duration"])
    except Exception as e:
        print(f"⚠️ Failed to get duration: {video_path}\n{e}\n{result.stderr.decode(errors='ignore')}")
        return None

def seconds_to_timestamp(seconds):
    """Converts seconds to HH:MM:SS.000 timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.000"

def generate_thumbnail(video_path, thumbnail_path):
    """Generates a thumbnail at 30% of the video duration, with fallbacks."""
    duration = get_video_duration(video_path)

    if duration and duration > 0:
        if duration < 5:
            print(f"⚠️ Video too short (<5s), using 1s mark: {video_path}")
            timestamp = "00:00:01.000"
        else:
            timestamp = seconds_to_timestamp(duration * 0.3)
    else:
        print(f"⚠️ Unknown duration, fallback to 3s: {video_path}")
        timestamp = "00:00:03.000"

    result = subprocess.run([
        "ffmpeg", "-y",
        "-ss", timestamp,
        "-i", video_path,
        "-vframes", "1",
        "-q:v", "2",
        thumbnail_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0 or not os.path.exists(thumbnail_path):
        print(f"❌ Thumbnail generation failed: {video_path}")
        print(result.stderr.decode(errors="ignore"))
