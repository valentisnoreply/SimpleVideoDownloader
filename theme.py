from __future__ import annotations

THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "window": "#10131A",
        "panel": "#1A1F2B",
        "panel_alt": "#202635",
        "input": "#0D1118",
        "text": "#F4F7FF",
        "muted": "#98A2B3",
        "accent": "#3AA8FF",
        "accent_hover": "#2E8FD9",
        "secondary": "#6D7CFF",
        "secondary_hover": "#5A68D6",
        "border": "#2B3346",
        "progress": "#26D18D",
        "link": "#8BA4FF",
    },
    "light": {
        "window": "#EEF2F8",
        "panel": "#FFFFFF",
        "panel_alt": "#F6F8FC",
        "input": "#FFFFFF",
        "text": "#172033",
        "muted": "#5F6C84",
        "accent": "#1967FF",
        "accent_hover": "#1456D1",
        "secondary": "#00A38C",
        "secondary_hover": "#008775",
        "border": "#D4DCE9",
        "progress": "#00A38C",
        "link": "#1967FF",
    },
}

FONTS: dict[str, tuple[str, int, str] | tuple[str, int]] = {
    "title": ("Segoe UI", 30, "bold"),
    "subtitle": ("Segoe UI", 13),
    "label": ("Segoe UI", 13, "bold"),
    "text": ("Segoe UI", 12),
    "text_small": ("Segoe UI", 11),
    "button": ("Segoe UI", 12, "bold"),
    "mono": ("Consolas", 11),
}


def get_palette(theme: str) -> dict[str, str]:
    return THEMES.get(theme, THEMES["dark"])


def toggle_theme(theme: str) -> str:
    return "light" if theme == "dark" else "dark"
