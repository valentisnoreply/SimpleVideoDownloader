from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

VALID_THEMES = {"light", "dark"}


@dataclass(slots=True)
class AppSettings:
    theme: str = "dark"
    output_dir: str = "videos"

    def normalized(self) -> "AppSettings":
        theme = self.theme if self.theme in VALID_THEMES else "dark"
        output_dir = self.output_dir.strip() or "videos"
        return AppSettings(theme=theme, output_dir=output_dir)


class SettingsStore:
    def __init__(self, path: Path) -> None:
        self.path = path

    def load(self) -> AppSettings:
        if not self.path.exists():
            return AppSettings()

        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return AppSettings()

        return AppSettings(
            theme=str(data.get("theme", "dark")),
            output_dir=str(data.get("output_dir", "videos")),
        ).normalized()

    def save(self, settings: AppSettings) -> None:
        payload = asdict(settings.normalized())
        self.path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
