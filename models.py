from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(slots=True)
class FormatOption:
    format_id: str
    label: str
    height: int
    fps: float
    codec: str
    ext: str
    tbr: float
    has_audio: bool
    filesize_mb: Optional[float]


@dataclass(slots=True)
class VideoDetails:
    title: str
    duration_seconds: Optional[int]
    formats: list[FormatOption]


@dataclass(slots=True)
class DownloadResult:
    title: str
    height: Optional[int]
    filepath: Path
