from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, Qt
from .code_editor import CodeEditor
from .syntax_highlighter import PythonHighlighter


class TabManager(QTabWidget):
    """Gerencia múltiplas abas de código"""
    
    tab_closed = pyqtSignal(int)
    tab_saved = pyqtSignal(int, str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setup_context_menu()
        
        # Contador para nomes de abas
        self.tab_counter = 1
        
        # Dicionário para armazenar informações das abas
        self.tab_info = {}
    
    def setup_context_menu(self):
        """Configura menu de contexto para as abas"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        """Mostra menu de contexto"""
        menu = QMenu()
        
        # Ações do menu
        new_tab_action = QAction("Nova Aba", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        
        save_action = QAction("Salvar", self)
        save_action.triggered.connect(self.save_current_tab)
        
        save_as_action = QAction("Salvar Como", self)
        save_as_action.triggered.connect(self.save_as_current_tab)
        
        close_action = QAction("Fechar Aba", self)
        close_action.triggered.connect(lambda: self.close_tab(self.currentIndex()))
        
        # Adiciona ações ao menu
        menu.addAction(new_tab_action)
        menu.addSeparator()
        menu.addAction(save_action)
        menu.addAction(save_as_action)
        menu.addSeparator()
        menu.addAction(close_action)
        
        menu.exec_(self.mapToGlobal(position))
    
    def add_new_tab(self, filename=None, content=""):
        """Adiciona uma nova aba"""
        # Cria o editor
        editor = CodeEditor()
        highlighter = PythonHighlighter(editor.document())
        
        # Define o conteúdo se fornecido
        if content:
            editor.setPlainText(content)
        
        # Nome da aba
        if filename:
            tab_name = filename.split('/')[-1]  # Pega apenas o nome do arquivo
        else:
            tab_name = f"Novo {self.tab_counter}"
            self.tab_counter += 1
        
        # Adiciona a aba
        index = self.addTab(editor, tab_name)
        self.setCurrentIndex(index)
        
        # Armazena informações da aba
        self.tab_info[index] = {
            'filename': filename,
            'saved': False,
            'editor': editor
        }
        
        return index
    
    def close_tab(self, index):
        """Fecha uma aba"""
        if index >= 0 and index < self.count():
            # Verifica se há mudanças não salvas
            editor = self.widget(index)
            if editor and hasattr(editor, 'document'):
                if editor.document().isModified():
                    # Aqui você pode adicionar um dialog para perguntar se quer salvar
                    pass
            
            # Remove a aba
            self.removeTab(index)
            
            # Remove informações da aba
            if index in self.tab_info:
                del self.tab_info[index]
            
            # Emite sinal
            self.tab_closed.emit(index)
    
    def save_current_tab(self):
        """Salva a aba atual"""
        current_index = self.currentIndex()
        if current_index >= 0:
            editor = self.widget(current_index)
            if editor:
                content = editor.toPlainText()
                self.tab_saved.emit(current_index, content)
    
    def save_as_current_tab(self):
        """Salva a aba atual com novo nome"""
        current_index = self.currentIndex()
        if current_index >= 0:
            editor = self.widget(current_index)
            if editor:
                content = editor.toPlainText()
                # Emite sinal para que a janela principal trate do "Salvar Como"
                self.tab_saved.emit(current_index, content)
    
    def get_current_editor(self):
        """Retorna o editor da aba atual"""
        current_index = self.currentIndex()
        if current_index >= 0:
            return self.widget(current_index)
        return None
    
    def get_current_content(self):
        """Retorna o conteúdo da aba atual"""
        editor = self.get_current_editor()
        if editor:
            return editor.toPlainText()
        return ""
    
    def set_current_content(self, content):
        """Define o conteúdo da aba atual"""
        editor = self.get_current_editor()
        if editor:
            editor.setPlainText(content)
    
    def get_all_tabs_content(self):
        """Retorna conteúdo de todas as abas"""
        tabs_content = {}
        for i in range(self.count()):
            editor = self.widget(i)
            if editor:
                tabs_content[i] = {
                    'name': self.tabText(i),
                    'content': editor.toPlainText(),
                    'filename': self.tab_info.get(i, {}).get('filename')
                }
        return tabs_content
    
    def find_tab_by_filename(self, filename):
        """Encontra aba pelo nome do arquivo"""
        for index, info in self.tab_info.items():
            if info.get('filename') == filename:
                return index
        return -1
    
    def set_tab_modified(self, index, modified=True):
        """Marca aba como modificada"""
        if index in self.tab_info:
            self.tab_info[index]['saved'] = not modified
            # Adiciona asterisco ao nome da aba se modificada
            current_name = self.tabText(index)
            if modified and not current_name.endswith('*'):
                self.setTabText(index, current_name + '*')
            elif not modified and current_name.endswith('*'):
                self.setTabText(index, current_name[:-1]) 