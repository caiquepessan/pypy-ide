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
            },
            'vscode_dark': {
                'name': 'VS Code Dark',
                'background': '#1e1e1e',
                'foreground': '#d4d4d4',
                'line_highlight': '#2d2d30',
                'line_number_bg': '#007acc',
                'line_number_fg': '#858585',
                'keyword': '#569cd6',
                'function': '#dcdcaa',
                'variable': '#9cdcfe',
                'class': '#4ec9b0',
                'identifier': '#d4d4d4',
                'comment': '#6a9955',
                'string': '#ce9178',
                'error': '#f44747',
                'number': '#b5cea8',
                'operator': '#d4d4d4',
                'breakpoint': '#f44747',
                'selection': '#264f78',
                'cursor': '#d4d4d4',
                'sidebar': '#252526',
                'statusbar': '#007acc',
                'toolbar': '#333333'
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
        
        # Aplica estilo CSS moderno e profissional
        css = f"""
        QWidget {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: none;
            font-family: 'Segoe UI', 'Consolas', 'Monaco', 'Courier New', monospace;
            font-size: 13px;
        }}
        
        QTextEdit, QPlainTextEdit {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: none;
            selection-background-color: {theme['selection']};
            selection-color: {theme['foreground']};
            padding: 8px;
            line-height: 1.4;
        }}
        
        QTextEdit:focus, QPlainTextEdit:focus {{
            border: 1px solid {theme['function']};
            border-radius: 4px;
        }}
        
        QTabWidget::pane {{
            border: none;
            background-color: {theme['background']};
        }}
        
        QTabBar::tab {{
            background-color: {theme['sidebar']};
            color: {theme['foreground']};
            padding: 10px 16px;
            margin-right: 1px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            font-weight: 500;
            min-width: 120px;
            max-width: 200px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border-bottom: 2px solid {theme['function']};
        }}
        
        QTabBar::tab:hover {{
            background-color: {theme['line_highlight']};
        }}
        
        QTabBar::close-button {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTkgM0w2IDZMMyAzIiBzdHJva2U9IiM5Q0E5Q0EiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPHBhdGggZD0iTTMgOUw2IDZMOSA5IiBzdHJva2U9IiM5Q0E5Q0EiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
            subcontrol-position: right;
            subcontrol-origin: margin;
            left: 2px;
            top: 2px;
        }}
        
        QTabBar::close-button:hover {{
            background-color: {theme['error']};
            border-radius: 3px;
        }}
        
        QMenuBar {{
            background-color: {theme['toolbar']};
            color: {theme['foreground']};
            border: none;
            padding: 4px;
            font-weight: 500;
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {theme['line_highlight']};
        }}
        
        QMenu {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: 1px solid {theme['line_highlight']};
            border-radius: 6px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
            margin: 2px;
        }}
        
        QMenu::item:selected {{
            background-color: {theme['line_highlight']};
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {theme['line_highlight']};
            margin: 4px 8px;
        }}
        
        QToolBar {{
            background-color: {theme['toolbar']};
            border: none;
            spacing: 4px;
            padding: 4px;
        }}
        
        QToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 4px;
            padding: 6px;
            min-width: 32px;
            min-height: 32px;
        }}
        
        QToolButton:hover {{
            background-color: {theme['line_highlight']};
            border: 1px solid {theme['function']};
        }}
        
        QToolButton:pressed {{
            background-color: {theme['selection']};
        }}
        
        QStatusBar {{
            background-color: {theme['statusbar']};
            color: {theme['foreground']};
            border-top: 1px solid {theme['line_highlight']};
            padding: 4px 8px;
        }}
        
        QStatusBar::item {{
            border: none;
        }}
        
        QScrollBar:vertical {{
            background-color: {theme['sidebar']};
            width: 14px;
            border-radius: 7px;
            margin: 0px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {theme['line_highlight']};
            border-radius: 7px;
            min-height: 30px;
            margin: 2px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {theme['foreground']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}
        
        QScrollBar:horizontal {{
            background-color: {theme['sidebar']};
            height: 14px;
            border-radius: 7px;
            margin: 0px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {theme['line_highlight']};
            border-radius: 7px;
            min-width: 30px;
            margin: 2px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {theme['foreground']};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        
        QSplitter::handle {{
            background-color: {theme['line_highlight']};
            border: none;
        }}
        
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        
        QSplitter::handle:vertical {{
            height: 2px;
        }}
        
        QTreeWidget {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: none;
            outline: none;
        }}
        
        QTreeWidget::item {{
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        QTreeWidget::item:selected {{
            background-color: {theme['selection']};
        }}
        
        QTreeWidget::item:hover {{
            background-color: {theme['line_highlight']};
        }}
        
        QLineEdit {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: 1px solid {theme['line_highlight']};
            border-radius: 4px;
            padding: 6px 8px;
        }}
        
        QLineEdit:focus {{
            border: 1px solid {theme['function']};
        }}
        
        QPushButton {{
            background-color: {theme['toolbar']};
            color: {theme['foreground']};
            border: 1px solid {theme['line_highlight']};
            border-radius: 4px;
            padding: 6px 12px;
            font-weight: 500;
        }}
        
        QPushButton:hover {{
            background-color: {theme['line_highlight']};
            border: 1px solid {theme['function']};
        }}
        
        QPushButton:pressed {{
            background-color: {theme['selection']};
        }}
        
        QComboBox {{
            background-color: {theme['background']};
            color: {theme['foreground']};
            border: 1px solid {theme['line_highlight']};
            border-radius: 4px;
            padding: 6px 8px;
        }}
        
        QComboBox:focus {{
            border: 1px solid {theme['function']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 20px;
        }}
        
        QComboBox::down-arrow {{
            image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTMgNEw2IDdMOSA0IiBzdHJva2U9IiM5Q0E5Q0EiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz4KPC9zdmc+);
        }}
        
        QDialog {{
            background-color: {theme['background']};
            color: {theme['foreground']};
        }}
        
        QDialog QLabel {{
            color: {theme['foreground']};
        }}
        
        QProgressBar {{
            border: 1px solid {theme['line_highlight']};
            border-radius: 4px;
            text-align: center;
            background-color: {theme['background']};
        }}
        
        QProgressBar::chunk {{
            background-color: {theme['function']};
            border-radius: 3px;
        }}
        """
        
        widget.setStyleSheet(css)
    
    def get_theme_colors(self, theme_name=None):
        """Retorna as cores do tema atual"""
        return self.get_theme(theme_name) 