"""
Configuração de temas e cores da aplicação
Suporta múltiplos temas: light (pastel rosa) e dark (night mode)
"""

# Temas disponíveis
THEMES = {
    'light': {
        'name': '☀️ Light Mode',
        'colors': {
            # Fundos
            'bg_window': "#fff4fa",         # Fundo da janela principal
            'bg_principal': "#fff4fa",      # Rosa pastel muito claro
            'bg_secundario': "#ffe6f8",     # Rosa pastel claro
            'bg_inputs': "#f1c0e3",         # Rosa pastel suave
            
            # Textos
            'text_principal': "#be6d93",    # Rosa médio
            'text_secundario': "#be6d93",   # Rosa roxo suave
            'text_tertiary': '#be6d93',     # Rosa lavanda
            'text_input': '#be6d93',        # Roxo escuro suave
            
            # Botões
            'btn_primary': '#d67ba6',       # Rosa médio
            'btn_primary_hover': '#c0679b', # Rosa médio escuro
            'btn_secondary': '#e8a4c2',     # Rosa claro
            'btn_secondary_hover': '#d67ba6',  # Rosa médio
            
            # Status
            'btn_text': 'white',            # Branco
            'select_bg': '#d67ba6',         # Rosa médio (seleção)
            'select_text': 'white',         # Branco
        }
    },
    'dark': {
        'name': '🌙 Dark Mode',
        'colors': {
            # Fundos
            'bg_window': "#202020",         # Fundo da janela principal (mais escuro)
            'bg_principal': "#202020",      # Azul muito escuro
            'bg_secundario': "#202020",     # Azul escuro
            'bg_inputs': "#202020",         # Azul bem escuro
            
            # Textos
            'text_principal': "#ffc2dd",    # Ciano brilhante
            'text_secundario': "#ffc2dd",   # Cinza claro
            'text_tertiary': '#ffc2dd',     # Azul claro
            'text_input': '#ffc2dd',        # Cinza muito claro
            
            # Botões
            'btn_primary': "#c8ff00",       # Ciano brilhante
            'btn_primary_hover': '#c8ff00', # Ciano médio
            'btn_secondary': '#533483',     # Roxo
            'btn_secondary_hover': '#6d47a0',  # Roxo claro
            
            # Status
            'btn_text': 'white',            # Branco
            'select_bg': '#533483',         # Roxo (seleção)
            'select_text': '#d67ba6',       # Ciano
        }
    }
}

# Tema padrão
CURRENT_THEME = 'dark'

def get_colors(theme=None):
    """Retorna as cores do tema especificado"""
    if theme is None:
        theme = CURRENT_THEME
    return THEMES[theme]['colors']

def set_theme(theme):
    """Define o tema atual"""
    global CURRENT_THEME
    if theme in THEMES:
        CURRENT_THEME = theme
        return True
    return False

def get_theme_name(theme=None):
    """Retorna o nome do tema"""
    if theme is None:
        theme = CURRENT_THEME
    return THEMES[theme]['name']

# Exportar cores do tema atual
COLORS = get_colors()


# Configuração de Fontes
FONTS = {
    'title_main': ('Segoe UI', 28, 'bold'),
    'title_sub': ('Segoe UI', 11),
    'label_main': ('Segoe UI', 16, 'bold'),
    'label_secondary': ('Segoe UI', 16, 'bold'),
    'label_tertiary': ('Segoe UI', 10),
    'button_main': ('Segoe UI', 13, 'bold'),
    'button_secondary': ('Segoe UI', 11, 'bold'),
    'button_tertiary': ('Segoe UI', 10, 'bold'),
    'text_normal': ('Segoe UI', 10),
    'text_small': ('Segoe UI', 11),
    'monospace': ('Segoe UI', 10),
}

# Tamanhos e Espaçamento
PADDING = {
    'large': 15,
    'medium': 10,
    'small': 3,
    'tiny': 1,
}

# Dimensões da janela
WINDOW_WIDTH = 880
WINDOW_HEIGHT = 600

# Configurações de componentes
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
