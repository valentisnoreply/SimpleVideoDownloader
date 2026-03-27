"""
Arquivo principal da aplicação
Gerencia a integração entre UI, Lógica e Tema
"""

import tkinter as tk
from ui_builder import UIBuilder
from downloader_logic import DownloaderLogic
import theme


class VideoDownloaderApp:
    """Classe principal que gerencia a aplicação"""
    
    def __init__(self, root):
        self.root = root
        
        # Variáveis de controle
        self.url_var = tk.StringVar()
        self.pasta_var = tk.StringVar(value='videos')
        
        # Cria a UI
        self.ui = UIBuilder(root, self)
        self.ui.build_interface()
        
        # Cria a lógica
        self.logic = DownloaderLogic(self)
        
        # Inicializa verificações
        self.logic.check_ffmpeg()
    
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
        current = theme.CURRENT_THEME
        new_theme = 'dark' if current == 'light' else 'light'
        theme.set_theme(new_theme)
        
        # Recarregar a interface
        self.ui.update_theme_button()
        self.refresh_colors()
    
    def refresh_colors(self):
        """Atualiza todas as cores da interface"""
        from theme import CURRENT_THEME, THEMES
        
        # Obter cores do tema atual
        colors = THEMES[CURRENT_THEME]['colors']
        
        # Atualizar janela principal
        self.root.configure(bg=colors['bg_principal'])
        
        # Atualizar todos os widgets
        for widget_name, widget in self.ui.widgets.items():
            try:
                # Frames e divisórias
                if 'frame' in widget_name.lower():
                    if 'title' in widget_name:
                        widget.config(bg=colors['bg_principal'])
                    else:
                        widget.config(bg=colors['bg_secundario'])
                # Labels de entrada (url_label, quality_label, pasta_label, log_label)
                elif widget_name in ['url_label', 'quality_label', 'pasta_label', 'log_label']:
                    widget.config(
                        bg=colors['bg_secundario'],
                        fg=colors['text_principal']
                    )
                # Título e Subtítulo
                elif widget_name == 'title_label':
                    widget.config(
                        bg=colors['bg_principal'],
                        fg=colors['text_principal']
                    )
                elif widget_name == 'subtitle_label':
                    widget.config(
                        bg=colors['bg_principal'],
                        fg=colors['text_tertiary']
                    )
                # Status label
                elif 'status_label' in widget_name:
                    widget.config(
                        bg=colors['bg_secundario'],
                        fg=colors['text_secundario']
                    )
                # Botões
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
                # Entradas de texto
                elif 'entry' in widget_name:
                    widget.config(
                        bg=colors['bg_inputs'],
                        fg=colors['text_input'],
                        insertbackground=colors['text_input']
                    )
                # Listbox (qualidades)
                elif 'listbox' in widget_name:
                    widget.config(
                        bg=colors['bg_inputs'],
                        fg=colors['text_input'],
                        selectbackground=colors['select_bg'],
                        selectforeground=colors['select_text']
                    )
                # Log de texto
                elif 'log_text' in widget_name:
                    widget.config(
                        bg=colors['bg_inputs'],
                        fg=colors['text_principal']
                    )
            except Exception as e:
                pass
        
        self.root.update()


def main():
    """Função principal que inicia a aplicação"""
    root = tk.Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
