from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Iterable, Optional

import yt_dlp

from models import DownloadResult, FormatOption, VideoDetails
from utils import sanitize_filename, unique_path

LogCallback = Callable[[str], None]
ProgressCallback = Callable[[float, str], None]


class DownloaderService:
    def __init__(
        self,
        *,
        on_log: Optional[LogCallback] = None,
        on_progress: Optional[ProgressCallback] = None,
    ) -> None:
        self.on_log = on_log
        self.on_progress = on_progress
        self.ffmpeg_path = self._find_ffmpeg()
        self.ffmpeg_available = self.ffmpeg_path is not None

    def check_ffmpeg(self) -> bool:
        return self._find_ffmpeg() is not None

    def fetch_video_details(self, url: str) -> VideoDetails:
        options = self._base_options()
        options.update(
            {
                "quiet": True,
                "extract_flat": False,
                "skip_download": True,
            }
        )
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=False)

        title = str(info.get("title") or "video")
        duration = info.get("duration")
        formats = self._parse_formats(info.get("formats") or [])
        return VideoDetails(title=title, duration_seconds=duration, formats=formats)

    def download_best(self, url: str, output_dir: Path) -> DownloadResult:
        if self.ffmpeg_available:
            selector = (
                "bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
                "bestvideo+bestaudio/best[ext=mp4]/best"
            )
        else:
            selector = "best[ext=mp4]/best"
        self._emit_log("Iniciando download inteligente...")
        return self._download(
            url=url,
            output_dir=output_dir,
            format_selector=selector,
            height_hint=None,
        )

    def download_format(
        self,
        *,
        url: str,
        output_dir: Path,
        format_option: FormatOption,
    ) -> DownloadResult:
        format_selector = format_option.format_id
        if self.ffmpeg_available and not format_option.has_audio:
            format_selector = (
                f"{format_option.format_id}+bestaudio[ext=m4a]/"
                f"{format_option.format_id}+bestaudio/{format_option.format_id}"
            )
        self._emit_log(f"Iniciando download em {format_option.height}p...")
        return self._download(
            url=url,
            output_dir=output_dir,
            format_selector=format_selector,
            height_hint=format_option.height,
        )

    def _download(
        self,
        *,
        url: str,
        output_dir: Path,
        format_selector: str,
        height_hint: int | None,
    ) -> DownloadResult:
        output_dir.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="vvd_") as temp_dir:
            temp_path = Path(temp_dir)
            options = {
                **self._base_options(),
                "format": format_selector,
                "outtmpl": str(temp_path / "%(title)s.%(ext)s"),
                "merge_output_format": "mp4",
                "quiet": False,
                "concurrent_fragment_downloads": 8,
                "http_chunk_size": 10 * 1024 * 1024,
                "progress_hooks": [self._progress_hook],
            }
            if self.ffmpeg_path is not None and self.ffmpeg_path.is_absolute():
                options["ffmpeg_location"] = str(self.ffmpeg_path.parent)

            try:
                with yt_dlp.YoutubeDL(options) as ydl:
                    info = ydl.extract_info(url, download=True)
            except Exception as exc:
                if "403" not in str(exc):
                    raise
                retry_options = {
                    **options,
                    "extractor_args": {
                        "youtube": {"player_client": ["web", "android"]},
                    },
                }
                self._emit_log("403 detectado, tentando estrategia alternativa...")
                with yt_dlp.YoutubeDL(retry_options) as ydl:
                    info = ydl.extract_info(url, download=True)

            source_file = self._resolve_downloaded_file(temp_path, info)
            title = str(info.get("title") or source_file.stem)
            height = info.get("height") or height_hint
            name = sanitize_filename(title)
            suffix = f" [{height}p]" if height else ""
            ext = source_file.suffix or ".mp4"
            destination = unique_path(output_dir / f"{name}{suffix}{ext}")
            shutil.move(str(source_file), str(destination))

        self._emit_progress(100.0, "Download concluido")
        self._emit_log(f"Arquivo salvo em: {destination}")
        return DownloadResult(title=title, height=height, filepath=destination)

    def _resolve_downloaded_file(self, temp_path: Path, info: dict) -> Path:
        requested_downloads = info.get("requested_downloads")
        if isinstance(requested_downloads, list):
            for item in requested_downloads:
                filepath = item.get("filepath") if isinstance(item, dict) else None
                if filepath and Path(filepath).exists():
                    return Path(filepath)

        for key in ("_filename", "filepath"):
            candidate = info.get(key)
            if candidate and Path(candidate).exists():
                return Path(candidate)

        files = [p for p in temp_path.iterdir() if p.is_file()]
        if not files:
            raise RuntimeError("Nao foi possivel localizar o arquivo baixado.")
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return files[0]

    def _parse_formats(self, formats: Iterable[dict]) -> list[FormatOption]:
        best_by_key: dict[tuple, FormatOption] = {}
        for fmt in formats:
            vcodec = str(fmt.get("vcodec") or "none")
            acodec = str(fmt.get("acodec") or "none")
            if vcodec == "none":
                continue

            height = fmt.get("height")
            if not isinstance(height, int) or height <= 0:
                continue

            has_audio = acodec != "none"
            if not self.ffmpeg_available and not has_audio:
                continue

            fps = float(fmt.get("fps") or 30)
            ext = str(fmt.get("ext") or "mp4")
            format_id = str(fmt.get("format_id") or "")
            if not format_id:
                continue

            tbr = float(fmt.get("tbr") or 0.0)
            filesize = fmt.get("filesize") or fmt.get("filesize_approx")
            filesize_mb = float(filesize) / (1024 * 1024) if filesize else None
            codec = self._codec_name(vcodec)

            tag = "A+V" if has_audio else "Video only"
            size = f" - {filesize_mb:.1f}MB" if filesize_mb else ""
            label = f"{height}p @ {int(fps)}fps {tag} [{codec}] ({ext}){size}"
            option = FormatOption(
                format_id=format_id,
                label=label,
                height=height,
                fps=fps,
                codec=codec,
                ext=ext,
                tbr=tbr,
                has_audio=has_audio,
                filesize_mb=filesize_mb,
            )
            key = (height, int(fps), codec, has_audio, ext)
            previous = best_by_key.get(key)
            if previous is None or option.tbr > previous.tbr:
                best_by_key[key] = option

        options = list(best_by_key.values())
        options.sort(key=lambda item: (item.height, item.fps, item.tbr), reverse=True)
        return options[:25]

    def _progress_hook(self, payload: dict) -> None:
        status = payload.get("status")
        if status == "downloading":
            percent = self._extract_percent(payload)
            speed = payload.get("speed")
            if isinstance(speed, (int, float)) and speed > 0:
                speed_msg = f"{(speed / (1024 * 1024)):.2f} MB/s"
                message = f"Baixando... {percent:.1f}% - {speed_msg}"
            else:
                message = f"Baixando... {percent:.1f}%"
            self._emit_progress(percent, message)
            return
        if status == "finished":
            self._emit_progress(100.0, "Processando arquivo...")

    @staticmethod
    def _extract_percent(payload: dict) -> float:
        downloaded = payload.get("downloaded_bytes")
        total = payload.get("total_bytes") or payload.get("total_bytes_estimate")
        if not downloaded or not total:
            return 0.0
        return min((float(downloaded) / float(total)) * 100, 100.0)

    @staticmethod
    def _codec_name(vcodec: str) -> str:
        lower = vcodec.lower()
        if "avc" in lower:
            return "h264"
        if "vp9" in lower:
            return "vp9"
        if "av01" in lower:
            return "av1"
        return lower[:8]

    def _emit_log(self, message: str) -> None:
        if self.on_log:
            self.on_log(message)

    def _emit_progress(self, value: float, message: str) -> None:
        if self.on_progress:
            self.on_progress(value, message)

    @staticmethod
    def _base_options() -> dict:
        return {
            "no_warnings": True,
            "noplaylist": True,
            "retries": 10,
            "fragment_retries": 10,
            "file_access_retries": 3,
            "socket_timeout": 30,
            "geo_bypass": True,
            "http_headers": {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36"
                )
            },
        }

    @staticmethod
    def _ffmpeg_candidates() -> list[Path]:
        root = Path.cwd()
        candidates = [
            root / "ffmpeg.exe",
            root / "ffmpeg" / "ffmpeg.exe",
            root / "ffmpeg" / "bin" / "ffmpeg.exe",
            root / "bin" / "ffmpeg.exe",
        ]

        meipass = getattr(sys, "_MEIPASS", None)
        if meipass:
            bundle = Path(meipass)
            candidates.extend(
                [
                    bundle / "ffmpeg.exe",
                    bundle / "ffmpeg" / "ffmpeg.exe",
                    bundle / "ffmpeg" / "bin" / "ffmpeg.exe",
                ]
            )

        return candidates

    def _find_ffmpeg(self) -> Path | None:
        for candidate in self._ffmpeg_candidates():
            if candidate.exists():
                return candidate.resolve()

        try:
            completed = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                check=True,
                timeout=4,
            )
            if completed.returncode == 0:
                return Path("ffmpeg")
        except Exception:
            return None
        return None
