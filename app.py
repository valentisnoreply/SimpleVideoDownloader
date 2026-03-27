"""Ponto de entrada da aplicacao."""

import tkinter as tk
from ui_builder import UIBuilder
from downloader_logic import DownloaderLogic
import theme


class VideoDownloaderApp:
    """Coordena UI, tema e logica de download."""

    def __init__(self, root):
        self.root = root

        self.url_var = tk.StringVar()
        self.pasta_var = tk.StringVar(value='videos')

        self.ui = UIBuilder(root, self)
        self.ui.build_interface()

        self.logic = DownloaderLogic(self)
        self.logic.check_ffmpeg()

    def listar_qualidades(self):
        """Encaminha para a camada de logica."""
        self.logic.listar_qualidades()

    def download_inteligente(self):
        """Encaminha para a camada de logica."""
        self.logic.download_inteligente()

    def start_download(self):
        """Encaminha para a camada de logica."""
        self.logic.start_download()

    def escolher_pasta(self):
        """Encaminha para a camada de logica."""
        self.logic.escolher_pasta()

    def toggle_theme(self):
        """Alterna entre tema claro e escuro."""
        current = theme.CURRENT_THEME
        new_theme = 'dark' if current == 'light' else 'light'
        theme.set_theme(new_theme)

        self.ui.update_theme_button()
        self.refresh_colors()

    def refresh_colors(self):
        """Reaplica as cores no tema atual."""
        from theme import CURRENT_THEME, THEMES

        colors = THEMES[CURRENT_THEME]['colors']
        self.root.configure(bg=colors['bg_principal'])

        for widget_name, widget in self.ui.widgets.items():
            try:
                if 'frame' in widget_name.lower():
                    if 'title' in widget_name:
                        widget.config(bg=colors['bg_principal'])
                    else:
                        widget.config(bg=colors['bg_secundario'])
                elif widget_name in ['url_label', 'quality_label', 'pasta_label', 'log_label']:
                    widget.config(bg=colors['bg_secundario'], fg=colors['text_principal'])
                elif widget_name == 'title_label':
                    widget.config(bg=colors['bg_principal'], fg=colors['text_principal'])
                elif widget_name == 'subtitle_label':
                    widget.config(bg=colors['bg_principal'], fg=colors['text_tertiary'])
                elif 'status_label' in widget_name:
                    widget.config(bg=colors['bg_secundario'], fg=colors['text_secundario'])
                elif 'btn' in widget_name:
                    if 'smart' in widget_name or 'download_btn' in widget_name:
                        widget.config(
                            bg=colors['btn_secondary'],
                            fg=colors['btn_text'],
                            activebackground=colors['btn_secondary_hover']
                        )
                    elif 'theme' in widget_name or 'browse' in widget_name:
                        widget.config(
                            bg=colors['btn_primary'],
                            fg=colors['btn_text'],
                            activebackground=colors['btn_primary_hover']
                        )
                    else:
                        widget.config(
                            bg=colors['btn_primary'],
                            fg=colors['btn_text'],
                            activebackground=colors['btn_primary_hover']
                        )
                elif 'entry' in widget_name:
                    widget.config(
                        bg=colors['bg_inputs'],
                        fg=colors['text_input'],
                        insertbackground=colors['text_input']
                    )
                elif 'listbox' in widget_name:
                    widget.config(
                        bg=colors['bg_inputs'],
                        fg=colors['text_input'],
                        selectbackground=colors['select_bg'],
                        selectforeground=colors['select_text']
                    )
                elif 'log_text' in widget_name:
                    widget.config(bg=colors['bg_inputs'], fg=colors['text_principal'])
            except Exception:
                pass

        self.root.update()


def main():
    """Inicia a aplicacao."""
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
