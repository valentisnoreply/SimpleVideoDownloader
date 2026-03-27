"""Tema visual da aplicação."""

# Paleta base
COLORS = {
    # Fundo
    'bg_principal': '#fce9f3',
    'bg_secundario': '#fdf4f9',
    'bg_inputs': '#f5d8ed',
    
    # Texto
    'text_principal': '#d67ba6',
    'text_secundario': '#a0708f',
    'text_tertiary': '#c09ab5',
    'text_input': '#5a4a5a',
    
    # Botões
    'btn_primary': '#d67ba6',
    'btn_primary_hover': '#c0679b',
    'btn_secondary': '#e8a4c2',
    'btn_secondary_hover': '#d67ba6',
    
    # Seleção e contraste
    'btn_text': 'white',
    'select_bg': '#d67ba6',
    'select_text': 'white',
}

# Fontes
FONTS = {
    'title_main': ('Segoe UI', 28, 'bold'),
    'title_sub': ('Segoe UI', 11),
    'label_main': ('Segoe UI', 12, 'bold'),
    'label_secondary': ('Segoe UI', 11, 'bold'),
    'label_tertiary': ('Segoe UI', 10),
    'button_main': ('Segoe UI', 13, 'bold'),
    'button_secondary': ('Segoe UI', 11, 'bold'),
    'button_tertiary': ('Segoe UI', 10, 'bold'),
    'text_normal': ('Segoe UI', 10),
    'text_small': ('Segoe UI', 9),
    'monospace': ('Segoe UI', 10),
}

# Espaçamento
PADDING = {
    'large': 20,
    'medium': 15,
    'small': 5,
    'tiny': 2,
}

# Dimensões da janela
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750

# Configurações dos componentes
COMPONENT_CONFIG = {
    'entry': {
        'relief': 'flat',
        'bd': 5,
        'ipady': 8,
    },
    'button': {
        'relief': 'flat',
        'cursor': 'hand2',
    },
    'listbox': {
        'relief': 'flat',
        'bd': 5,
        'height': 10,
    },
}
