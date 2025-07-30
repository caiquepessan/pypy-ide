import os
from PyQt5.QtGui import QIcon, QPixmap, QPainter
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtCore import QSize, QByteArray, Qt
from PyQt5.QtWidgets import QApplication

class ModernIcons:
    """Sistema de ícones SVG modernos para a interface"""
    
    def __init__(self):
        self.icon_cache = {}
        self.icons_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons')
        
    def get_icon(self, icon_name, size=24):
        """Retorna um ícone SVG como QIcon"""
        cache_key = f"{icon_name}_{size}"
        
        if cache_key in self.icon_cache:
            return self.icon_cache[cache_key]
            
        svg_path = os.path.join(self.icons_path, f"{icon_name}.svg")
        
        if not os.path.exists(svg_path):
            # Fallback para ícone padrão se não encontrar o SVG
            return QIcon()
            
        try:
            # Carrega o SVG
            with open(svg_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
                
            # Cria o renderizador SVG
            renderer = QSvgRenderer(QByteArray(svg_content.encode()))
            
            # Cria um pixmap do tamanho desejado
            pixmap = QPixmap(size, size)
            pixmap.fill(Qt.transparent)
            
            # Renderiza o SVG no pixmap
            renderer.render(QPainter(pixmap))
            
            # Cria o ícone
            icon = QIcon(pixmap)
            
            # Cache o ícone
            self.icon_cache[cache_key] = icon
            
            return icon
            
        except Exception as e:
            print(f"Erro ao carregar ícone {icon_name}: {e}")
            return QIcon()
    
    # Métodos para acessar ícones específicos
    def new_file(self, size=24):
        return self.get_icon("new_file", size)
        
    def open_file(self, size=24):
        return self.get_icon("open_file", size)
        
    def save_file(self, size=24):
        return self.get_icon("save_file", size)
        
    def run_code(self, size=24):
        return self.get_icon("run_code", size)
        
    def debug(self, size=24):
        return self.get_icon("debug", size)
        
    def terminal(self, size=24):
        return self.get_icon("terminal", size)
        
    def settings(self, size=24):
        return self.get_icon("settings", size)
        
    def explorer(self, size=24):
        return self.get_icon("explorer", size)
        
    def themes(self, size=24):
        return self.get_icon("themes", size)
        
    def packages(self, size=24):
        return self.get_icon("packages", size)
        
    def close(self, size=24):
        return self.get_icon("close", size)
        
    def help(self, size=24):
        return self.get_icon("help", size)
        
    def info(self, size=24):
        return self.get_icon("info", size)
        
    def success(self, size=24):
        return self.get_icon("success", size)
        
    def error(self, size=24):
        return self.get_icon("error", size)

# Instância global
modern_icons = ModernIcons()

# Ícones de texto para menus (fallback)
class TextIcons:
    """Ícones de texto para menus"""
    FILE_MENU = "📁"
    EDIT_MENU = "✏️"
    VIEW_MENU = "👁️"
    TOOLS_MENU = "🔧"
    HELP_MENU = "❓"
    NEW_TAB = "➕"
    OPEN_FILE = "📂"
    SAVE_FILE = "💾"
    SAVE_AS = "💾+"
    COMMAND_EXIT = "🚪"
    UNDO = "↶"
    REDO = "↷"
    SNIPPETS = "📝"
    PACKAGES = "📦"
    AUTOCOMPLETE = "💡"
    TERMINAL = "💻"
    THEMES = "🎨"
    EXPLORER = "🗂️"
    ABOUT = "ℹ️"
    HELP = "❓"
    SUCCESS = "✅"
    ERROR = "❌"
    INFO = "ℹ️"
    DEBUG = "🐛"
    RUN_CODE = "▶️"
    COMMAND_HELP = "❓"
    CLEAR_CONSOLE = "🧹"
    COMMAND_EXIT = "🚪"
    COMMAND_PWD = "📍"
    COMMAND_LS = "📋"
    COMMAND_CD = "📁"
    COMMAND_HISTORY = "📜"
    FOLDER = "📁"
    SNIPPETS = "📝"
    PACKAGES = "📦"
    EXPLORER = "🗂️"
    THEMES = "🎨"
    TERMINAL = "💻"
    SETTINGS = "⚙️"
    
    @staticmethod
    def get_icon_for_file_type(filename):
        """Retorna o ícone apropriado para o tipo de arquivo"""
        if filename.endswith('.py'):
            return "🐍"
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return "🖼️"
        elif filename.endswith(('.mp3', '.wav', '.flac')):
            return "🎵"
        elif filename.endswith(('.mp4', '.avi', '.mkv')):
            return "🎬"
        else:
            return "📄" 