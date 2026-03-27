"""Construção da interface Tkinter."""

import tkinter as tk
from tkinter import ttk, scrolledtext
from theme import COLORS, FONTS, PADDING, COMPONENT_CONFIG


class UIBuilder:
    """Monta os componentes visuais da aplicação."""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.widgets = {}
        
    def build_interface(self):
        """Constrói a interface completa"""
        self.setup_window()
        self.create_title_section()
        self.create_main_frame()
        
    def setup_window(self):
        """Configura a janela principal."""
        self.root.title("Video Downloader Pro")
        self.root.geometry("800x1200")
        self.root.configure(bg=COLORS['bg_principal'])
        
    def create_title_section(self):
        """Cria a seção de título"""
        title_frame = tk.Frame(self.root, bg=COLORS['bg_principal'])
        title_frame.pack(pady=PADDING['large'])
        
        title_label = tk.Label(
            title_frame,
            text=" Simple Video Downloader",
            font=FONTS['title_main'],
            bg=COLORS['bg_principal'],
            fg=COLORS['text_principal']
        )
        title_label.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="YouTube • Vimeo • TikTok • Instagram e muito mais",
            font=FONTS['title_sub'],
            bg=COLORS['bg_principal'],
            fg=COLORS['text_tertiary']
        )
        subtitle.pack()
        
    def create_main_frame(self):
        """Cria o frame principal e todos os seus componentes"""
        main_frame = tk.Frame(
            self.root,
            bg=COLORS['bg_secundario'],
            relief=tk.RAISED,
            bd=2
        )
        main_frame.pack(
            padx=PADDING['large'],
            pady=PADDING['medium'],
            fill=tk.BOTH,
            expand=True
        )
        
        self.create_url_section(main_frame)
        self.create_video_info_section(main_frame)
        self.create_quality_section(main_frame)
        self.create_folder_section(main_frame)
        self.create_buttons_section(main_frame)
        self.create_progress_section(main_frame)
        self.create_status_section(main_frame)
        self.create_log_section(main_frame)
        
    def create_url_section(self, parent):
        """Seção de entrada de URL"""
        url_frame = tk.Frame(parent, bg=COLORS['bg_secundario'])
        url_frame.pack(padx=PADDING['large'], pady=PADDING['medium'], fill=tk.X)
        
        tk.Label(
            url_frame,
            text="📎 URL do Vídeo:",
            font=FONTS['label_secondary'],
            bg=COLORS['bg_secundario'],
            fg=COLORS['text_secundario']
        ).pack(anchor=tk.W)
        
        url_entry_frame = tk.Frame(url_frame, bg=COLORS['bg_secundario'])
        url_entry_frame.pack(fill=tk.X, pady=PADDING['small'])
        
        self.widgets['url_entry'] = tk.Entry(
            url_entry_frame,
            textvariable=self.controller.url_var,
            font=FONTS['text_normal'],
            bg=COLORS['bg_inputs'],
            fg=COLORS['text_input'],
            insertbackground=COLORS['text_principal'],
            relief=COMPONENT_CONFIG['entry']['relief'],
            bd=COMPONENT_CONFIG['entry']['bd']
        )
        self.widgets['url_entry'].pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=COMPONENT_CONFIG['entry']['ipady']
        )
        
        self.widgets['info_btn'] = tk.Button(
            url_entry_frame,
            text="🔍 Ver Qualidades",
            command=self.controller.listar_qualidades,
            bg=COLORS['btn_primary'],
            fg=COLORS['btn_text'],
            font=FONTS['button_secondary'],
            padx=PADDING['medium'],
            activebackground=COLORS['btn_primary_hover'],
            relief=COMPONENT_CONFIG['button']['relief'],
            cursor=COMPONENT_CONFIG['button']['cursor']
        )
        self.widgets['info_btn'].pack(side=tk.LEFT, padx=(PADDING['small'], 0))
        
    def create_video_info_section(self, parent):
        """Seção de informações do vídeo"""
        self.widgets['info_frame'] = tk.Frame(parent, bg=COLORS['bg_inputs'])
        
        self.widgets['info_label'] = tk.Label(
            self.widgets['info_frame'],
            text="",
            font=FONTS['text_small'],
            bg=COLORS['bg_inputs'],
            fg=COLORS['text_principal'],
            justify=tk.LEFT,
            wraplength=800
        )
        self.widgets['info_label'].pack(padx=PADDING['medium'], pady=PADDING['medium'])
        
    def create_quality_section(self, parent):
        """Seção de qualidades disponíveis"""
        self.widgets['quality_frame'] = tk.Frame(parent, bg=COLORS['bg_secundario'])
        self.widgets['quality_frame'].pack(
            padx=PADDING['large'],
            pady=PADDING['medium'],
            fill=tk.BOTH,
            expand=True
        )
        
        tk.Label(
            self.widgets['quality_frame'],
            text="🎯 Qualidades Disponíveis:",
            font=FONTS['label_main'],
            bg=COLORS['bg_secundario'],
            fg=COLORS['text_secundario']
        ).pack(anchor=tk.W, pady=(0, PADDING['small']))
        
        list_frame = tk.Frame(self.widgets['quality_frame'], bg=COLORS['bg_secundario'])
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.widgets['quality_listbox'] = tk.Listbox(
            list_frame,
            font=FONTS['text_normal'],
            bg=COLORS['bg_inputs'],
            fg=COLORS['text_input'],
            selectbackground=COLORS['select_bg'],
            selectforeground=COLORS['select_text'],
            yscrollcommand=scrollbar.set,
            relief=COMPONENT_CONFIG['listbox']['relief'],
            bd=COMPONENT_CONFIG['listbox']['bd'],
            height=COMPONENT_CONFIG['listbox']['height']
        )
        self.widgets['quality_listbox'].pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )
        scrollbar.config(command=self.widgets['quality_listbox'].yview)
        
        self.widgets['quality_listbox'].insert(
            0,
            "Clique em 'Ver Qualidades' para listar os formatos disponíveis"
        )
        
    def create_folder_section(self, parent):
        """Seção de seleção de pasta"""
        pasta_frame = tk.Frame(parent, bg=COLORS['bg_secundario'])
        pasta_frame.pack(padx=PADDING['large'], pady=PADDING['medium'], fill=tk.X)
        
        tk.Label(
            pasta_frame,
            text="📁 Pasta de Destino:",
            font=FONTS['label_main'],
            bg=COLORS['bg_secundario'],
            fg=COLORS['text_secundario']
        ).pack(anchor=tk.W)
        
        pasta_entry_frame = tk.Frame(pasta_frame, bg=COLORS['bg_secundario'])
        pasta_entry_frame.pack(fill=tk.X, pady=PADDING['small'])
        
        self.widgets['pasta_entry'] = tk.Entry(
            pasta_entry_frame,
            textvariable=self.controller.pasta_var,
            font=FONTS['text_small'],
            bg=COLORS['bg_inputs'],
            fg=COLORS['text_input'],
            insertbackground=COLORS['text_principal'],
            relief=COMPONENT_CONFIG['entry']['relief'],
            bd=COMPONENT_CONFIG['entry']['bd']
        )
        self.widgets['pasta_entry'].pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=True,
            ipady=5
        )
        
        self.widgets['browse_btn'] = tk.Button(
            pasta_entry_frame,
            text="📂 Escolher",
            command=self.controller.escolher_pasta,
            bg=COLORS['btn_primary'],
            fg=COLORS['btn_text'],
            font=FONTS['button_tertiary'],
            padx=PADDING['medium'],
            activebackground=COLORS['btn_primary_hover'],
            relief=COMPONENT_CONFIG['button']['relief'],
            cursor=COMPONENT_CONFIG['button']['cursor']
        )
        self.widgets['browse_btn'].pack(side=tk.LEFT, padx=(PADDING['small'], 0))
        
    def create_buttons_section(self, parent):
        """Seção de botões de download"""
        button_frame = tk.Frame(parent, bg=COLORS['bg_secundario'])
        button_frame.pack(padx=PADDING['large'], pady=PADDING['medium'], fill=tk.X)
        
        self.widgets['smart_btn'] = tk.Button(
            button_frame,
            text="⚡ DOWNLOAD INTELIGENTE (Melhor Qualidade)",
            command=self.controller.download_inteligente,
            bg=COLORS['btn_secondary'],
            fg=COLORS['btn_text'],
            font=FONTS['button_main'],
            padx=PADDING['large'],
            pady=PADDING['large'],
            activebackground=COLORS['btn_secondary_hover'],
            relief=COMPONENT_CONFIG['button']['relief'],
            cursor=COMPONENT_CONFIG['button']['cursor']
        )
        self.widgets['smart_btn'].pack(fill=tk.X, pady=(0, PADDING['small']))
        
        self.widgets['download_btn'] = tk.Button(
            button_frame,
            text="⬇️  BAIXAR QUALIDADE SELECIONADA",
            command=self.controller.start_download,
            bg=COLORS['btn_primary'],
            fg=COLORS['btn_text'],
            font=FONTS['button_main'],
            padx=PADDING['large'],
            pady=PADDING['large'],
            activebackground=COLORS['btn_primary_hover'],
            state=tk.DISABLED,
            relief=COMPONENT_CONFIG['button']['relief'],
            cursor=COMPONENT_CONFIG['button']['cursor']
        )
        self.widgets['download_btn'].pack(fill=tk.X)
        
    def create_progress_section(self, parent):
        """Seção de barra de progresso"""
        self.widgets['progress'] = ttk.Progressbar(
            parent,
            orient=tk.HORIZONTAL,
            mode='indeterminate',
            length=300
        )
        self.widgets['progress'].pack(
            padx=PADDING['large'],
            pady=(PADDING['small'], PADDING['small']),
            fill=tk.X
        )
        
    def create_status_section(self, parent):
        """Seção de status"""
        self.widgets['status_label'] = tk.Label(
            parent,
            text="Cole uma URL e use Download Inteligente ou veja as qualidades disponíveis",
            font=FONTS['text_small'],
            bg=COLORS['bg_secundario'],
            fg=COLORS['text_secundario']
        )
        self.widgets['status_label'].pack(pady=(0, PADDING['small']))
        
    def create_log_section(self, parent):
        """Seção de log"""
        log_frame = tk.Frame(parent, bg=COLORS['bg_secundario'])
        log_frame.pack(
            padx=PADDING['large'],
            pady=(0, PADDING['large']),
            fill=tk.BOTH,
            expand=True
        )
        
        tk.Label(
            log_frame,
            text="📋 Log:",
            font=FONTS['label_secondary'],
            bg=COLORS['bg_secundario'],
            fg=COLORS['text_secundario']
        ).pack(anchor=tk.W)
        
        self.widgets['log_text'] = scrolledtext.ScrolledText(
            log_frame,
            height=6,
            font=FONTS['text_small'],
            bg=COLORS['bg_inputs'],
            fg=COLORS['text_principal'],
            relief=tk.FLAT,
            bd=5
        )
        self.widgets['log_text'].pack(fill=tk.BOTH, expand=True, pady=PADDING['small'])
