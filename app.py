"""Ponto de entrada da aplicação."""

import tkinter as tk
from ui_builder import UIBuilder
from downloader_logic import DownloaderLogic


class VideoDownloaderApp:
    """Integra interface e lógica de download."""
    
    def __init__(self, root):
        self.root = root
        
        # Estado básico da tela
        self.url_var = tk.StringVar()
        self.pasta_var = tk.StringVar(value='videos')
        
        # Monta interface
        self.ui = UIBuilder(root, self)
        self.ui.build_interface()
        
        # Inicializa lógica
        self.logic = DownloaderLogic(self)
        
        # Checa FFmpeg na inicialização
        self.logic.check_ffmpeg()
    
    def listar_qualidades(self):
        self.logic.listar_qualidades()
    
    def download_inteligente(self):
        self.logic.download_inteligente()
    
    def start_download(self):
        self.logic.start_download()
    
    def escolher_pasta(self):
        self.logic.escolher_pasta()


def main():
    """Inicia a aplicação."""
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
