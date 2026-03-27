"""
Arquivo de layout e interface visual da aplicação usando CustomTkinter
Responsável por criar e configurar todos os componentes visuais
"""

import customtkinter as ctk
from tkinter import scrolledtext
from theme import FONTS, PADDING, get_colors, THEMES


class UIBuilder:
    """Classe responsável por construir a interface visual com CustomTkinter"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.widgets = {}
    
    def get_color(self, key):
        """Retorna cor do tema atual dinamicamente"""
        from theme import CURRENT_THEME
        colors = get_colors(CURRENT_THEME)
        return colors.get(key, '#000000')
        
    def build_interface(self):
        """Constrói a interface completa"""
        self.setup_window()
        self.create_theme_button()
        self.create_title_section()
        self.create_main_frame()
        # Atualiza as cores para sincronizar com o tema padrão
        self.root.after(100, self.update_all_colors)
        
    def setup_window(self):
        """Configura a janela principal"""
        self.root.title("Valentina's Video Downloader")
        self.root.geometry("600x880")
        self.root.resizable(False, False)
        
        # Definir tema padrão conforme CURRENT_THEME
        from theme import CURRENT_THEME
        ctk.set_appearance_mode(CURRENT_THEME)
        ctk.set_default_color_theme("blue")
        
    def create_theme_button(self):
        """Cria botão de alternância de tema"""
        self.widgets['theme_frame'] = ctk.CTkFrame(self.root, fg_color="transparent")
        self.widgets['theme_frame'].pack(pady=(10, 0), padx=20, fill="x")
        
        self.widgets['theme_btn'] = ctk.CTkButton(
            self.widgets['theme_frame'],
            text="🌙 Night Mode",
            command=self.controller.toggle_theme,
            font=FONTS['button_tertiary'],
            width=150,
            height=35
        )
        self.widgets['theme_btn'].pack(side="right")
        
    def update_theme_button(self):
        """Atualiza o texto do botão de tema"""
        from theme import CURRENT_THEME
        if CURRENT_THEME == 'light':
            self.widgets['theme_btn'].configure(text="🌙 Night Mode")
        else:
            self.widgets['theme_btn'].configure(text="☀️ Light Mode")
        
        # Atualizar cores de todos os frames
        self.update_all_colors()
    
    def update_all_colors(self):
        """Atualiza todas as cores dos widgets para o tema atual"""
        try:
            # Frames
            self.widgets['url_frame'].configure(fg_color=(self.get_color('bg_secundario'), self.get_color('bg_secundario')))
            self.widgets['quality_frame'].configure(fg_color=(self.get_color('bg_secundario'), self.get_color('bg_secundario')))
            self.widgets['pasta_frame'].configure(fg_color=(self.get_color('bg_secundario'), self.get_color('bg_secundario')))
            self.widgets['button_frame'].configure(fg_color=(self.get_color('bg_secundario'), self.get_color('bg_secundario')))
            self.widgets['log_frame'].configure(fg_color=(self.get_color('bg_secundario'), self.get_color('bg_secundario')))
            self.widgets['main_frame'].configure(fg_color=(self.get_color('bg_principal'), self.get_color('bg_principal')))
            
            # Labels
            self.widgets['title_label'].configure(text_color=(self.get_color('text_principal'), self.get_color('text_principal')))
            self.widgets['subtitle_label'].configure(text_color=(self.get_color('text_secundario'), self.get_color('text_secundario')))
            self.widgets['url_label'].configure(text_color=(self.get_color('text_principal'), self.get_color('text_principal')))
            self.widgets['quality_label'].configure(text_color=(self.get_color('text_principal'), self.get_color('text_principal')))
            self.widgets['pasta_label'].configure(text_color=(self.get_color('text_principal'), self.get_color('text_principal')))
            self.widgets['status_label'].configure(text_color=(self.get_color('text_secundario'), self.get_color('text_secundario')))
            self.widgets['log_label'].configure(text_color=(self.get_color('text_principal'), self.get_color('text_principal')))
            
            # Botões
            self.widgets['smart_btn'].configure(fg_color=(self.get_color('btn_secondary'), self.get_color('btn_secondary')))
        except:
            pass
        
    def create_title_section(self):
        """Cria a seção de título"""
        self.widgets['title_frame'] = ctk.CTkFrame(self.root, fg_color="transparent")
        self.widgets['title_frame'].pack(pady=20)
        
        self.widgets['title_label'] = ctk.CTkLabel(
            self.widgets['title_frame'],
            text="🎬 Valentina's Video Downloader",
            font=FONTS['title_main'],
            text_color=(self.get_color('text_principal'), self.get_color('text_principal'))
        )
        self.widgets['title_label'].pack()
        
        self.widgets['subtitle_label'] = ctk.CTkLabel(
            self.widgets['title_frame'],
            text="YouTube • Vimeo • TikTok • Instagram e muito mais",
            font=FONTS['title_sub'],
            text_color=(self.get_color('text_secundario'), self.get_color('text_secundario'))
        )
        self.widgets['subtitle_label'].pack()
        
    def create_main_frame(self):
        """Cria o frame principal e todos os seus componentes"""
        self.widgets['main_frame'] = ctk.CTkFrame(
            self.root,
            fg_color=(self.get_color('bg_principal'), "#2d2d44")
        )
        self.widgets['main_frame'].pack(
            padx=20,
            pady=15,
            fill="both",
            expand=False
        )
        
        self.create_url_section(self.widgets['main_frame'])
        self.create_quality_section(self.widgets['main_frame'])
        self.create_folder_section(self.widgets['main_frame'])
        self.create_buttons_section(self.widgets['main_frame'])
        self.create_progress_section(self.widgets['main_frame'])
        self.create_status_section(self.widgets['main_frame'])
        self.create_log_section(self.widgets['main_frame'])
        
    def create_url_section(self, parent):
        """Seção de entrada de URL"""
        self.widgets['url_frame'] = ctk.CTkFrame(parent, fg_color=(self.get_color('bg_secundario'), "#1a1a2e"))
        self.widgets['url_frame'].pack(padx=20, pady=(0, 15), fill="x")
        
        self.widgets['url_label'] = ctk.CTkLabel(
            self.widgets['url_frame'],
            text="📎 URL do Vídeo:",
            font=FONTS['label_secondary'],
            text_color=(self.get_color('text_principal'), self.get_color('text_principal'))
        )
        self.widgets['url_label'].pack(anchor="w", padx=10, pady=(10, 0))
        
        self.widgets['url_entry_frame'] = ctk.CTkFrame(self.widgets['url_frame'], fg_color="transparent")
        self.widgets['url_entry_frame'].pack(fill="x", padx=10, pady=10)
        
        self.widgets['url_entry'] = ctk.CTkEntry(
            self.widgets['url_entry_frame'],
            textvariable=self.controller.url_var,
            font=FONTS['text_normal'],
            placeholder_text="Cole a URL do vídeo aqui..."
        )
        self.widgets['url_entry'].pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )
        
        self.widgets['info_btn'] = ctk.CTkButton(
            self.widgets['url_entry_frame'],
            text="🔍 Ver Qualidades",
            command=self.controller.listar_qualidades,
            font=FONTS['button_secondary'],
            width=140
        )
        self.widgets['info_btn'].pack(side="left")
        
    def create_quality_section(self, parent):
        """Seção de qualidades disponíveis"""
        self.widgets['quality_frame'] = ctk.CTkFrame(parent, fg_color=(self.get_color('bg_secundario'), "#1a1a2e"))
        self.widgets['quality_frame'].pack(
            padx=20,
            pady=15,
            fill="x"
        )
        
        self.widgets['quality_label'] = ctk.CTkLabel(
            self.widgets['quality_frame'],
            text="🎯 Qualidades Disponíveis:",
            font=FONTS['label_main'],
            text_color=(self.get_color('text_principal'), self.get_color('text_principal'))
        )
        self.widgets['quality_label'].pack(anchor="w", padx=10, pady=(10, 5))
        
        # ComboBox para seleção de qualidades
        self.widgets['quality_listbox'] = ctk.CTkComboBox(
            self.widgets['quality_frame'],
            values=["Clique em 'Ver Qualidades' para listar"],
            command=self.on_quality_selected,
            font=FONTS['text_normal'],
            state="readonly"
        )
        self.widgets['quality_listbox'].pack(fill="x", padx=10, pady=10)
        
    def create_folder_section(self, parent):
        """Seção de seleção de pasta"""
        self.widgets['pasta_frame'] = ctk.CTkFrame(parent, fg_color=(self.get_color('bg_secundario'), "#1a1a2e"))
        self.widgets['pasta_frame'].pack(padx=20, pady=15, fill="x")
        
        self.widgets['pasta_label'] = ctk.CTkLabel(
            self.widgets['pasta_frame'],
            text="📁 Pasta de Destino:",
            font=FONTS['label_main'],
            text_color=(self.get_color('text_principal'), self.get_color('text_principal'))
        )
        self.widgets['pasta_label'].pack(anchor="w", padx=10, pady=(10, 0))
        
        pasta_entry_frame = ctk.CTkFrame(self.widgets['pasta_frame'], fg_color="transparent")
        pasta_entry_frame.pack(fill="x", padx=10, pady=10)
        
        self.widgets['pasta_entry'] = ctk.CTkEntry(
            pasta_entry_frame,
            textvariable=self.controller.pasta_var,
            font=FONTS['text_small']
        )
        self.widgets['pasta_entry'].pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 10)
        )
        
        self.widgets['browse_btn'] = ctk.CTkButton(
            pasta_entry_frame,
            text="📂 Escolher",
            command=self.controller.escolher_pasta,
            font=FONTS['button_tertiary'],
            width=120
        )
        self.widgets['browse_btn'].pack(side="left")
        
    def create_buttons_section(self, parent):
        """Seção de botões de download"""
        self.widgets['button_frame'] = ctk.CTkFrame(parent, fg_color=(self.get_color('bg_secundario'), "#1a1a2e"))
        self.widgets['button_frame'].pack(padx=20, pady=15, fill="x")
        
        self.widgets['smart_btn'] = ctk.CTkButton(
            self.widgets['button_frame'],
            text="⚡ DOWNLOAD INTELIGENTE (Melhor Qualidade)",
            command=self.controller.download_inteligente,
            font=FONTS['button_main'],
            height=45,
            corner_radius=8,
            fg_color=(self.get_color('btn_secondary'), "#533483")
        )
        self.widgets['smart_btn'].pack(fill="x", pady=(0, 10))
        
        self.widgets['download_btn'] = ctk.CTkButton(
            self.widgets['button_frame'],
            text="⬇️ BAIXAR QUALIDADE SELECIONADA",
            command=self.controller.start_download,
            font=FONTS['button_main'],
            height=45,
            corner_radius=8,
            state="disabled"
        )
        self.widgets['download_btn'].pack(fill="x")
        
    def create_progress_section(self, parent):
        """Seção de barra de progresso"""
        self.widgets['progress'] = ctk.CTkProgressBar(
            parent,
            progress_color=("#d67ba6", "#00d4ff")
        )
        self.widgets['progress'].pack(
            padx=20,
            pady=10,
            fill="x"
        )
        self.widgets['progress'].set(0)
        
    def create_status_section(self, parent):
        """Seção de status"""
        self.widgets['status_label'] = ctk.CTkLabel(
            parent,
            text="Cole uma URL e use Download Inteligente ou veja as qualidades disponíveis",
            font=FONTS['text_small'],
            text_color=(self.get_color('text_secundario'), self.get_color('text_secundario'))
        )
        self.widgets['status_label'].pack(pady=(0, 10))
        
    def create_log_section(self, parent):
        """Seção de log"""
        self.widgets['log_frame'] = ctk.CTkFrame(parent, fg_color=(self.get_color('bg_secundario'), "#1a1a2e"))
        self.widgets['log_frame'].pack(
            padx=20,
            pady=(0, 20),
            fill="both",
            expand=False
        )
        
        # Frame para header com botão de recolher
        log_header = ctk.CTkFrame(self.widgets['log_frame'], fg_color="transparent")
        log_header.pack(fill="x", padx=10, pady=(10, 5))
        
        self.widgets['log_label'] = ctk.CTkLabel(
            log_header,
            text="📋 Log:",
            font=FONTS['label_secondary'],
            text_color=(self.get_color('text_principal'), self.get_color('text_principal'))
        )
        self.widgets['log_label'].pack(side="left", anchor="w")
        
        self.widgets['log_toggle_btn'] = ctk.CTkButton(
            log_header,
            text="▼",
            font=FONTS['button_tertiary'],
            width=30,
            height=25,
            command=self.toggle_log
        )
        self.widgets['log_toggle_btn'].pack(side="right")
        
        self.widgets['log_text'] = ctk.CTkTextbox(
            self.widgets['log_frame'],
            height=80,
            font=FONTS['text_small']
        )
        self.widgets['log_text'].pack(fill="both", expand=True, padx=10, pady=10)
        self.log_expanded = False
        self.widgets['log_text'].pack_forget()
        self.widgets['log_toggle_btn'].configure(text="▶")
    
    def toggle_log(self):
        """Alterna entre expandido e recolhido"""
        if self.log_expanded:
            self.widgets['log_text'].pack_forget()
            self.widgets['log_toggle_btn'].configure(text="▶")
            self.log_expanded = False
        else:
            self.widgets['log_text'].pack(fill="both", expand=True, padx=10, pady=10)
            self.widgets['log_toggle_btn'].configure(text="▼")
            self.log_expanded = True
    
    def on_quality_selected(self, choice):
        """Callback quando uma qualidade é selecionada"""
        if choice and choice != "Clique em 'Ver Qualidades' para listar":
            self.controller.ui.enable_download_button(True)
