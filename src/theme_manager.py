from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt


class ThemeManager:
    """Gerenciador de temas para a IDE"""
    
    def __init__(self):
        self.themes = {
            'dracula': {
                'name': 'Dracula',
                'background': '#282a36',
                'foreground': '#f8f8f2',
                'line_highlight': '#44475a',
                'line_number_bg': '#44475a',
                'line_number_fg': '#f8f8f2',
                'keyword': '#ff79c6',
                'function': '#50fa7b',
                'variable': '#f1fa8c',
                'class': '#8be9fd',
                'identifier': '#ffb86c',
                'comment': '#6272a4',
                'string': '#f1fa8c',
                'error': '#ff5555',
                'number': '#bd93f9',
                'operator': '#ff79c6',
                'breakpoint': '#ff5555',
                'selection': '#44475a',
                'cursor': '#f8f8f2',
                'sidebar': '#21222c',
                'statusbar': '#282a36',
                'toolbar': '#21222c'
            },
            'monokai': {
                'name': 'Monokai',
                'background': '#272822',
                'foreground': '#f8f8f2',
                'line_highlight': '#3e3d32',
                'line_number_bg': '#3e3d32',
                'line_number_fg': '#f8f8f2',
                'keyword': '#f92672',
                'function': '#a6e22e',
                'variable': '#fd971f',
                'class': '#66d9ef',
                'identifier': '#f8f8f2',
                'comment': '#75715e',
                'string': '#e6db74',
                'error': '#f92672',
                'number': '#ae81ff',
                'operator': '#f92672',
                'breakpoint': '#f92672',
                'selection': '#49483e',
                'cursor': '#f8f8f2',
                'sidebar': '#1d1e19',
                'statusbar': '#272822',
                'toolbar': '#1d1e19'
            },
            'solarized_dark': {
                'name': 'Solarized Dark',
                'background': '#002b36',
                'foreground': '#839496',
                'line_highlight': '#073642',
                'line_number_bg': '#073642',
                'line_number_fg': '#586e75',
                'keyword': '#cb4b16',
                'function': '#859900',
                'variable': '#b58900',
                'class': '#268bd2',
                'identifier': '#839496',
                'comment': '#586e75',
                'string': '#2aa198',
                'error': '#dc322f',
                'number': '#d33682',
                'operator': '#cb4b16',
                'breakpoint': '#dc322f',
                'selection': '#073642',
                'cursor': '#839496',
                'sidebar': '#001e26',
                'statusbar': '#002b36',
                'toolbar': '#001e26'
            },
            'github_dark': {
                'name': 'GitHub Dark',
                'background': '#0d1117',
                'foreground': '#c9d1d9',
                'line_highlight': '#161b22',
                'line_number_bg': '#161b22',
                'line_number_fg': '#8b949e',
                'keyword': '#ff7b72',
                'function': '#d2a8ff',
                'variable': '#79c0ff',
                'class': '#ffa657',
                'identifier': '#c9d1d9',
                'comment': '#8b949e',
                'string': '#a5d6ff',
                'error': '#ff7b72',
                'number': '#79c0ff',
                'operator': '#ff7b72',
                'breakpoint': '#ff7b72',
                'selection': '#1f6feb',
                'cursor': '#c9d1d9',
                'sidebar': '#010409',
                'statusbar': '#0d1117',
                'toolbar': '#010409'
            },
            'one_dark': {
                'name': 'One Dark',
                'background': '#282c34',
                'foreground': '#abb2bf',
                'line_highlight': '#3e4451',
                'line_number_bg': '#3e4451',
                'line_number_fg': '#5c6370',
                'keyword': '#c678dd',
                'function': '#61afef',
                'variable': '#e06c75',
                'class': '#e5c07b',
                'identifier': '#abb2bf',
                'comment': '#5c6370',
                'string': '#98c379',
                'error': '#e06c75',
                'number': '#d19a66',
                'operator': '#c678dd',
                'breakpoint': '#e06c75',
                'selection': '#3e4451',
                'cursor': '#abb2bf',
                'sidebar': '#21252b',
                'statusbar': '#282c34',
                'toolbar': '#21252b'
            }
        }
        self.current_theme = 'dracula'
    
    def get_theme(self, theme_name=None):
        """Retorna um tema específico"""
        if theme_name is None:
            theme_name = self.current_theme
        return self.themes.get(theme_name, self.themes['dracula'])
    
    def set_theme(self, theme_name):
        """Define o tema atual"""
        if theme_name in self.themes:
            self.current_theme = theme_name
    
    def get_available_themes(self):
        """Retorna lista de temas disponíveis"""
        return list(self.themes.keys())
    
    def get_theme_names(self):
        """Retorna nomes dos temas"""
        return {name: theme['name'] for name, theme in self.themes.items()}
    
    def apply_theme_to_widget(self, widget, theme_name=None):
        """Aplica um tema a um widget"""
        theme = self.get_theme(theme_name)
        
        # Cria paleta de cores
        palette = QPalette()
        
        # Cores básicas
        palette.setColor(QPalette.Window, QColor(theme['background']))
        palette.setColor(QPalette.WindowText, QColor(theme['foreground']))
        palette.setColor(QPalette.Base, QColor(theme['background']))
        palette.setColor(QPalette.AlternateBase, QColor(theme['line_highlight']))
        palette.setColor(QPalette.ToolTipBase, QColor(theme['background']))
        palette.setColor(QPalette.ToolTipText, QColor(theme['foreground']))
        palette.setColor(QPalette.Text, QColor(theme['foreground']))
        palette.setColor(QPalette.Button, QColor(theme['toolbar']))
        palette.setColor(QPalette.ButtonText, QColor(theme['foreground']))
        palette.setColor(QPalette.BrightText, QColor(theme['error']))
        palette.setColor(QPalette.Link, QColor(theme['function']))
        palette.setColor(QPalette.Highlight, QColor(theme['selection']))
        palette.setColor(QPalette.HighlightedText, QColor(theme['foreground']))
        
        # Aplica a paleta
        widget.setPalette(palette)
        
        # Aplica estilo CSS
        css = f"""
        QWidget {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: none;
        }}
        
        QTextEdit, QPlainTextEdit {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: none;
            selection-background-color: {theme['selection']};
        }}
        
        QTabWidget::pane {{
            border: none;
            background-color: {theme['background']};
        }}
        
        QTabBar::tab {{
            background-color: {theme['sidebar']};
            color: {theme['foreground']};
            padding: 8px 12px;
            margin-right: 2px;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme['background']};
            color: {theme['foreground']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {theme['line_highlight']};
        }}
        
        QMenuBar {{
            background-color: {theme['toolbar']};
            color: {theme['foreground']};
            border: none;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 8px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme['line_highlight']};
        }}
        
        QMenu {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: 1px solid {theme['line_highlight']};
        }}
        
        QMenu::item {{
            padding: 6px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {theme['line_highlight']};
        }}
        
        QToolBar {{
            background-color: {theme['toolbar']};
            border: none;
            spacing: 3px;
        }}
        
        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 3px;
            padding: 4px;
        }}
        
        QToolButton:hover {{
            background-color: {theme['line_highlight']};
        }}
        
        QStatusBar {{
            background-color: {theme['statusbar']};
            color: {theme['foreground']};
        }}
        
        QScrollBar:vertical {{
            background-color: {theme['sidebar']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {theme['line_highlight']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {theme['foreground']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        """
        
        widget.setStyleSheet(css)
    
    def get_theme_colors(self, theme_name=None):
        """Retorna as cores do tema atual"""
        return self.get_theme(theme_name) 