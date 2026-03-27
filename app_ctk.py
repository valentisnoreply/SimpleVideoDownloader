"""
Arquivo principal da aplicação com CustomTkinter
Gerencia a integração entre UI, Lógica e Tema
"""

import customtkinter as ctk
from ui_builder_ctk import UIBuilder
from downloader_logic_ctk import DownloaderLogic
import theme
import threading
import time


class VideoDownloaderApp:
    """Classe principal que gerencia a aplicação"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Valentina's Video Downloader")
        
        # Variáveis de controle
        self.url_var = ctk.StringVar()
        self.pasta_var = ctk.StringVar(value='videos')
        
        # Configura a cor da janela mãe
        from theme import get_colors, CURRENT_THEME
        ctk.set_appearance_mode(CURRENT_THEME)
        colors = get_colors(CURRENT_THEME)
        self.root.configure(fg_color=colors['bg_window'])
        
        # Cria a UI
        self.ui = UIBuilder(root, self)
        self.ui.build_interface()
        
        # Cria a lógica
        self.logic = DownloaderLogic(self)
        
        # Inicializa verificações
        self.logic.check_ffmpeg()
        
        # Criar overlay preto DEPOIS (fica na frente)
        self.overlay = ctk.CTkFrame(self.root, fg_color="#181818")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lift()  # Força ficar na frente
        # Adicionar texto "Loading..."
        ctk.CTkLabel(
            self.overlay,
            text="Pururin... ♥",
            font=("Segoe UI", 50),
            text_color="#ffc2dd"
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Remove overlay depois que tudo carregou
        self.root.after(2500, self.overlay.destroy)


    
    # Métodos delegados para a lógica
    def listar_qualidades(self):
        """Delega para a lógica"""
        self.logic.listar_qualidades()
    
    def download_inteligente(self):
        """Delega para a lógica"""
        self.logic.download_inteligente()
    
    def start_download(self):
        """Delega para a lógica"""
        self.logic.start_download()
    
    def escolher_pasta(self):
        """Delega para a lógica"""
        self.logic.escolher_pasta()
    
    def toggle_theme(self):
        """Alterna entre temas light e dark"""
        self.show_overlay(800)
        current = theme.CURRENT_THEME
        new_theme = 'dark' if current == 'light' else 'light'
        theme.set_theme(new_theme)
        
        # Atualizar CustomTkinter theme
        ctk.set_appearance_mode(new_theme)
        
        # Atualizar cor da janela mãe
        from theme import get_colors
        colors = get_colors()
        self.root.configure(fg_color=colors['bg_window'])
        
        # Atualizar botão
        self.ui.update_theme_button()
    
    def log_message(self, message):
        """Adiciona mensagem ao log"""
        try:
            log_widget = self.ui.widgets['log_text']
            log_widget.configure(state="normal")
            log_widget.insert("end", f"{message}\n")
            log_widget.see("end")
            log_widget.configure(state="disabled")
        except:
            pass
    
    def update_progress(self, value):
        """Atualiza a barra de progresso"""
        try:
            self.ui.widgets['progress'].set(value / 100)
        except:
            pass
    
    def update_status(self, message):
        """Atualiza a label de status"""
        try:
            self.ui.widgets['status_label'].configure(text=message)
        except:
            pass
    
    def update_quality_list(self, qualities):
        """Atualiza a lista de qualidades"""
        try:
            combo_widget = self.ui.widgets['quality_listbox']
            combo_widget.configure(values=qualities)
            combo_widget.set(qualities[0] if qualities else "Selecione uma qualidade")
        except:
            pass
    
    def enable_download_button(self, enabled=True):
        """Habilita ou desabilita o botão de download"""
        try:
            state = "normal" if enabled else "disabled"
            self.ui.widgets['download_btn'].configure(state=state)
        except:
            pass

    def show_overlay(self, duration=500):
        """Mostra overlay preto  com loading"""
        self.overlay = ctk.CTkFrame(self.root, fg_color="#303030")
        self.overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self.overlay.lift()
        
        ctk.CTkLabel(
            self.overlay,
            text="Guenta aí...",
            font=("Segoe UI", 30),
            text_color="#ffc2dd"
        ).place(relx=0.5, rely=0.5, anchor="center")
        
        self.root.after(duration, self.hide_overlay)

    def hide_overlay(self):
        """Remove overlay"""
        if hasattr(self, 'overlay'):
            self.overlay.destroy()

def main():
    """Função principal que inicia a aplicação"""
    root = ctk.CTk()
    app = VideoDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


