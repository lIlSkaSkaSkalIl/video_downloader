import os

def prepare_directories(base_dir="/content/media_toolkit", verbose=False):
    """
    Create necessary directories for video processing and return their paths.

    Parameters:
    - base_dir (str): Base working directory.
    - verbose (bool): If True, prints the directories created.

    Returns:
    - dict: A dictionary containing all relevant directory paths.
    """
    dirs = {
        "base": base_dir,
        "video": os.path.join(base_dir, "video"),
        "output": os.path.join(base_dir, "output"),
        "meta": os.path.join(base_dir, "meta"),
        "thumb": os.path.join(base_dir, "thumb"),
        "cookies": os.path.join(base_dir, "cookies"),
        "logs": os.path.join(base_dir, "logs"),
    }

    for name, path in dirs.items():
        os.makedirs(path, exist_ok=True)
        if verbose:
            print(f"📁 Directory prepared: {name} → {path}")

    return dirs
