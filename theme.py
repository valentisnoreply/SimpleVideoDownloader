"""Temas, paleta e configuracoes visuais."""

THEMES = {
    'light': {
        'name': 'â˜€ï¸ Light Mode',
        'colors': {
            'bg_principal': '#fce9f3',
            'bg_secundario': '#fdf4f9',
            'bg_inputs': '#f5d8ed',
            
            'text_principal': '#d67ba6',
            'text_secundario': '#a0708f',
            'text_tertiary': '#c09ab5',
            'text_input': '#5a4a5a',
            
            'btn_primary': '#d67ba6',
            'btn_primary_hover': '#c0679b',
            'btn_secondary': '#e8a4c2',
            'btn_secondary_hover': '#d67ba6',
            
            'btn_text': 'white',
            'select_bg': '#d67ba6',
            'select_text': 'white',
        }
    },
    'dark': {
        'name': 'ðŸŒ™ Dark Mode',
        'colors': {
            'bg_principal': "#1a1a2e",
            'bg_secundario': '#2d2d44',
            'bg_inputs': '#383838',
            
            'text_principal': '#00d4ff',
            'text_secundario': '#00d4ff',
            'text_tertiary': '#00d4ff',
            'text_input': '#00d4ff',
            
            'btn_primary': '#00d4ff',
            'btn_primary_hover': '#00a8cc',
            'btn_secondary': '#533483',
            'btn_secondary_hover': '#6d47a0',
            
            'btn_text': 'white',
            'select_bg': '#533483',
            'select_text': '#00d4ff',
        }
    }
}

CURRENT_THEME = 'light'

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

COLORS = get_colors()


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

PADDING = {
    'large': 20,
    'medium': 15,
    'small': 5,
    'tiny': 2,
}

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 750

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



