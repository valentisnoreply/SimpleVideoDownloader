# SimpleVideoDonwloader

## Run

```bash
python app_ctk.py
```

## What changed in v2

- Single architecture (no duplicated Tkinter vs CustomTkinter stacks)
- Service layer for yt-dlp logic (`services.py`)
- UI layer separated from controller (`ui.py`)
- Central controller with thread-safe UI updates (`controller.py`)
- Persistent settings (`.vvd_settings.json`) for theme and output folder
- Better error handling and cleaner progress reporting

## Main structure

- `main.py`: app startup
- `controller.py`: orchestration and user actions
- `ui.py`: interface construction and widget state
- `services.py`: format discovery and downloads
- `settings.py`: load/save local settings
- `theme.py`: color palettes and fonts
- `models.py`: dataclasses for app entities
- `utils.py`: utility helpers (file naming, folder open, duration format)
- `tools/`: helper scripts (`.bat`)

## Dependencies

```bash
pip install customtkinter yt-dlp
```

Optional:

- `ffmpeg` for max quality merge support.

## FFmpeg behavior

- If FFmpeg is available, the app can merge best video + best audio (higher quality).
- If FFmpeg is missing, the app falls back to combined streams only (often lower quality, e.g. 360p).

## EXE build options

- `tools/06_COMPILAR_EXE_SEM_FFMPEG.bat`
  - generates `dist/SimpleVideoDonwloader-lite.exe`
  - smaller EXE, depends on FFmpeg installed on target PC
- `tools/07_COMPILAR_EXE_COM_FFMPEG_EMBUTIDO.bat`
  - generates `dist/SimpleVideoDonwloader-full.exe`
  - includes FFmpeg inside EXE (larger), works on PCs without FFmpeg
  - requires local files in `./ffmpeg/bin/ffmpeg.exe` and `./ffmpeg/bin/ffprobe.exe`
