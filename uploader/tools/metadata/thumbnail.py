import subprocess

def generate_thumbnail(video_path, thumbnail_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-ss", "00:00:01.000",
        "-vframes", "1",
        "-q:v", "2",
        thumbnail_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
