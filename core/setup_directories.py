# core/setup_directories.py

import os

def prepare_directories(base_dir="/content/media_toolkit"):
    paths = {
        "base": base_dir,
        "video": os.path.join(base_dir, "video"),
        "output": os.path.join(base_dir, "output"),
        "meta": os.path.join(base_dir, "meta"),
        "thumb": os.path.join(base_dir, "thumb"),
    }
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    return paths
