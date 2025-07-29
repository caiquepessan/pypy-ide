# Ícones modernos para o PyPy IDE
# Usando Font Awesome e ícones Unicode modernos

class ModernIcons:
    """Classe com ícones modernos para a interface"""
    
    # Ícones de arquivo
    NEW_FILE = "📄"  # Alternativa: "📝" ou "➕"
    OPEN_FILE = "📂"  # Alternativa: "📁" ou "🔍"
    SAVE_FILE = "💾"  # Alternativa: "💿" ou "🖫"
    SAVE_AS = "💾+"  # Alternativa: "💿+" ou "🖫+"
    
    # Ícones de execução
    RUN_CODE = "▶️"  # Alternativa: "🚀" ou "⚡"
    STOP_CODE = "⏹️"  # Alternativa: "🛑" ou "⏸️"
    DEBUG = "🐛"  # Alternativa: "🔍" ou "🔧"
    
    # Ícones de interface
    NEW_TAB = "➕"  # Alternativa: "📑" ou "📋"
    CLOSE_TAB = "❌"  # Alternativa: "✖️" ou "🗑️"
    EXPLORER = "🗂️"  # Alternativa: "📁" ou "📂"
    SETTINGS = "⚙️"  # Alternativa: "🔧" ou "🎛️"
    
    # Ícones de ferramentas
    PACKAGES = "📦"  # Alternativa: "📚" ou "🔧"
    THEMES = "🎨"  # Alternativa: "🌈" ou "🎭"
    SNIPPETS = "📝"  # Alternativa: "✂️" ou "📋"
    SEARCH = "🔍"  # Alternativa: "🔎" ou "📖"
    
    # Ícones de terminal
    TERMINAL = "💻"  # Alternativa: "🖥️" ou "⌨️"
    CONSOLE = "📟"  # Alternativa: "🖥️" ou "💻"
    COMMAND = "⌨️"  # Alternativa: "💻" ou "🖥️"
    
    # Ícones de status
    SUCCESS = "✅"  # Alternativa: "✓" ou "🎉"
    ERROR = "❌"  # Alternativa: "⚠️" ou "💥"
    WARNING = "⚠️"  # Alternativa: "⚡" ou "🔶"
    INFO = "ℹ️"  # Alternativa: "💡" ou "📌"
    
    # Ícones de menu
    FILE_MENU = "📁"
    EDIT_MENU = "✏️"
    VIEW_MENU = "👁️"
    TOOLS_MENU = "🔧"
    HELP_MENU = "❓"
    
    # Ícones de ações
    UNDO = "↶"  # Alternativa: "⏪" ou "🔄"
    REDO = "↷"  # Alternativa: "⏩" ou "🔄"
    CUT = "✂️"
    COPY = "📋"
    PASTE = "📌"
    FIND = "🔍"
    REPLACE = "🔄"
    
    # Ícones de desenvolvimento
    GIT = "📚"  # Alternativa: "🔗" ou "🌿"
    DEBUG_BREAKPOINT = "🔴"
    DEBUG_STEP = "👣"
    DEBUG_CONTINUE = "▶️"
    
    # Ícones de terminal/console
    CLEAR_CONSOLE = "🧹"  # Alternativa: "🗑️" ou "💨"
    COMMAND_HISTORY = "📜"  # Alternativa: "📚" ou "📖"
    AUTOCOMPLETE = "💡"  # Alternativa: "🔤" ou "📝"
    
    # Ícones de temas
    LIGHT_THEME = "☀️"
    DARK_THEME = "🌙"
    CUSTOM_THEME = "🎨"
    
    # Ícones de arquivos por tipo
    PYTHON_FILE = "🐍"
    TEXT_FILE = "📄"
    FOLDER = "📁"
    IMAGE_FILE = "🖼️"
    AUDIO_FILE = "🎵"
    VIDEO_FILE = "🎬"
    
    # Ícones de comandos do terminal
    COMMAND_CLS = "🧹"
    COMMAND_HELP = "❓"
    COMMAND_EXIT = "🚪"
    COMMAND_CLEAR = "🗑️"
    COMMAND_HISTORY = "📜"
    COMMAND_LS = "📋"
    COMMAND_CD = "📁"
    COMMAND_PWD = "📍"
    
    @staticmethod
    def get_icon_for_file_type(filename):
        """Retorna o ícone apropriado para o tipo de arquivo"""
        if filename.endswith('.py'):
            return ModernIcons.PYTHON_FILE
        elif filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
            return ModernIcons.IMAGE_FILE
        elif filename.endswith(('.mp3', '.wav', '.flac')):
            return ModernIcons.AUDIO_FILE
        elif filename.endswith(('.mp4', '.avi', '.mkv')):
            return ModernIcons.VIDEO_FILE
        else:
            return ModernIcons.TEXT_FILE
    
    @staticmethod
    def get_icon_for_command(command):
        """Retorna o ícone apropriado para o comando"""
        command = command.lower().strip()
        if command in ['cls', 'clear']:
            return ModernIcons.COMMAND_CLS
        elif command in ['help', '?']:
            return ModernIcons.COMMAND_HELP
        elif command in ['exit', 'quit']:
            return ModernIcons.COMMAND_EXIT
        elif command in ['ls', 'dir']:
            return ModernIcons.COMMAND_LS
        elif command.startswith('cd'):
            return ModernIcons.COMMAND_CD
        elif command == 'pwd':
            return ModernIcons.COMMAND_PWD
        else:
            return ModernIcons.COMMAND 