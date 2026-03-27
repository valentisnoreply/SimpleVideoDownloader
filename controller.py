from __future__ import annotations

import threading
import webbrowser
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox

import customtkinter as ctk

from models import DownloadResult, VideoDetails
from services import DownloaderService
from settings import SettingsStore
from theme import get_palette, toggle_theme
from ui import MainView
from utils import format_duration, open_file_location


class AppController:
    def __init__(self, root: ctk.CTk) -> None:
        self.root = root
        self.settings_store = SettingsStore(Path(".vvd_settings.json"))
        self.settings = self.settings_store.load()
        self.url_var = ctk.StringVar()
        self.output_var = ctk.StringVar(value=self.settings.output_dir)
        self._busy = False
        self._video_details: VideoDetails | None = None
        self._set_window_icon()

        ctk.set_appearance_mode(self.settings.theme)
        ctk.set_default_color_theme("blue")

        self.view = MainView(
            root,
            url_var=self.url_var,
            output_var=self.output_var,
            on_analyze=self.analyze_url,
            on_download_best=self.download_best,
            on_download_selected=self.download_selected,
            on_browse_output=self.choose_output_folder,
            on_toggle_theme=self.change_theme,
            on_open_repo=self.open_repo,
        )
        self.apply_theme(self.settings.theme)

        self.downloader = DownloaderService(
            on_log=lambda msg: self._on_ui(lambda: self.log(msg)),
            on_progress=lambda pct, msg: self._on_ui(
                lambda: self._handle_progress(pct, msg)
            ),
        )
        self._show_startup_status()

    def _set_window_icon(self) -> None:
        icon_path = Path("icon.ico")
        if icon_path.exists():
            try:
                self.root.iconbitmap(str(icon_path))
            except Exception:
                pass

    def _show_startup_status(self) -> None:
        if self.downloader.ffmpeg_available:
            ffmpeg_path = str(self.downloader.ffmpeg_path)
            self.log(f"FFmpeg detectado ({ffmpeg_path}). Melhor qualidade ativada.")
        else:
            self.log("FFmpeg nao encontrado. Algumas qualidades podem nao aparecer.")
        self.view.set_status("Pronto. Cole uma URL e clique em Analisar.")

    def apply_theme(self, theme_name: str) -> None:
        palette = get_palette(theme_name)
        self.view.apply_theme(palette=palette, theme_name=theme_name)

    def change_theme(self) -> None:
        new_theme = toggle_theme(self.settings.theme)
        self.settings.theme = new_theme
        self.settings_store.save(self.settings)
        ctk.set_appearance_mode(new_theme)
        self.apply_theme(new_theme)
        self.log(f"Tema alterado para {new_theme}.")

    def choose_output_folder(self) -> None:
        current = Path(self.output_var.get().strip() or ".").resolve()
        selected = filedialog.askdirectory(initialdir=str(current))
        if not selected:
            return
        self.output_var.set(selected)
        self.settings.output_dir = selected
        self.settings_store.save(self.settings)
        self.log(f"Pasta de destino: {selected}")

    def analyze_url(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL faltando", "Cole uma URL de video primeiro.")
            return

        def work() -> VideoDetails:
            return self.downloader.fetch_video_details(url)

        def success(result: VideoDetails) -> None:
            self._video_details = result
            self.view.set_formats(result.formats)
            duration = format_duration(result.duration_seconds)
            ffmpeg_state = "ON" if self.downloader.ffmpeg_available else "OFF"
            self.view.set_video_info(
                f"Titulo: {result.title}\nDuracao: {duration}\nFFmpeg: {ffmpeg_state}"
            )
            if result.formats:
                self.view.set_status(f"{len(result.formats)} opcoes de qualidade encontradas.")
                self.log(f"{len(result.formats)} opcoes de qualidade carregadas.")
            else:
                self.view.set_status("Nenhum formato encontrado para essa URL.")
                self.log("A URL nao retornou formatos de video.")

        self.log("Analisando URL...")
        self._run_background(work, success, busy_message="Analisando URL...")

    def download_best(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL faltando", "Cole uma URL de video primeiro.")
            return

        output_dir = self._resolve_output_dir()
        if output_dir is None:
            return

        def work() -> DownloadResult:
            return self.downloader.download_best(url, output_dir)

        def success(result: DownloadResult) -> None:
            self._finalize_download(result)

        self._run_background(work, success, busy_message="Rodando download inteligente...")

    def download_selected(self) -> None:
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("URL faltando", "Cole uma URL de video primeiro.")
            return

        selected = self.view.get_selected_format()
        if selected is None:
            messagebox.showwarning("Qualidade faltando", "Analise a URL e escolha uma qualidade.")
            return

        output_dir = self._resolve_output_dir()
        if output_dir is None:
            return

        def work() -> DownloadResult:
            return self.downloader.download_format(
                url=url,
                output_dir=output_dir,
                format_option=selected,
            )

        def success(result: DownloadResult) -> None:
            self._finalize_download(result)

        msg = f"Baixando qualidade selecionada ({selected.height}p)..."
        self._run_background(work, success, busy_message=msg)

    def _resolve_output_dir(self) -> Path | None:
        value = self.output_var.get().strip()
        if not value:
            messagebox.showwarning("Pasta faltando", "Escolha uma pasta de destino primeiro.")
            return None
        output_dir = Path(value)
        self.settings.output_dir = value
        self.settings_store.save(self.settings)
        return output_dir

    def _finalize_download(self, result: DownloadResult) -> None:
        resolution = f"{result.height}p" if result.height else "unknown"
        self.view.set_progress(100)
        self.view.set_status(f"Concluido: {result.title} ({resolution})")
        self.log(f"Download concluido: {result.title} ({resolution})")
        self.log(f"Salvo em: {result.filepath}")

        prompt = (
            f"Download concluido.\n\nTitulo: {result.title}\n"
            f"Qualidade: {resolution}\n\nDeseja abrir a pasta?"
        )
        if messagebox.askyesno("Download concluido", prompt):
            try:
                open_file_location(result.filepath)
            except Exception as exc:
                messagebox.showerror("Erro ao abrir pasta", str(exc))

    def _handle_progress(self, percent: float, message: str) -> None:
        self.view.set_progress(percent)
        self.view.set_status(message)

    def _run_background(self, work, on_success, *, busy_message: str) -> None:
        if self._busy:
            return
        self._busy = True
        self.view.set_busy(True)
        self.view.set_progress(0)
        self.view.set_status(busy_message)

        def runner() -> None:
            try:
                result = work()
            except Exception as exc:
                self._on_ui(lambda err=exc: self._handle_error(err))
            else:
                self._on_ui(lambda value=result: on_success(value))
            finally:
                self._on_ui(self._release_busy)

        threading.Thread(target=runner, daemon=True).start()

    def _handle_error(self, error: Exception) -> None:
        text = str(error) or error.__class__.__name__
        if "403" in text:
            text += (
                "\n\nGeralmente e bloqueio temporario da plataforma. "
                "Atualize o yt-dlp e tente de novo."
            )
        self.log(f"Erro: {text}")
        self.view.set_status("A operacao falhou. Veja o log.")
        messagebox.showerror("Operacao falhou", text)

    def _release_busy(self) -> None:
        self._busy = False
        self.view.set_busy(False)

    def _on_ui(self, callback) -> None:
        self.root.after(0, callback)

    def log(self, message: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.view.append_log(f"[{timestamp}] {message}")

    @staticmethod
    def open_repo() -> None:
        webbrowser.open("https://github.com/valentisnoreply")
