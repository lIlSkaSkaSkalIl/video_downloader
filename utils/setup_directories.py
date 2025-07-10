# core/setup_directories.py

import os

def prepare_directories(base_dir="/content/media_toolkit"):
    dirs = {
        "base": base_dir,
        "video": os.path.join(base_dir, "video"),
        "output": os.path.join(base_dir, "output"),
        "meta": os.path.join(base_dir, "meta"),
        "thumb": os.path.join(base_dir, "thumb"),
        "cookies": os.path.join(base_dir, "cookies"),
    }

    for path in dirs.values():
        os.makedirs(path, exist_ok=True)

    return dirs
