from __future__ import annotations

import os
import platform
import re
import subprocess
from pathlib import Path


def sanitize_filename(name: str) -> str:
    cleaned = re.sub(r"[\\/:*?\"<>|]+", "", name).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned or "video"


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix
    counter = 1
    while True:
        candidate = path.with_name(f"{stem} ({counter}){suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def format_duration(seconds: int | None) -> str:
    if seconds is None:
        return "--:--"
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{sec:02d}"
    return f"{minutes:02d}:{sec:02d}"


def open_file_location(path: Path) -> None:
    target = path.resolve()
    system = platform.system()
    if system == "Windows":
        os.startfile(str(target.parent))
        return
    if system == "Darwin":
        subprocess.run(["open", str(target.parent)], check=False)
        return
    subprocess.run(["xdg-open", str(target.parent)], check=False)

