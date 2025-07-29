from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QMenu, QAction, QMessageBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from .code_editor import CodeEditor
from .syntax_highlighter import PythonHighlighter


class TabManager(QTabWidget):
    """Gerencia múltiplas abas de código"""
    
    tab_closed = pyqtSignal(int)
    tab_saved = pyqtSignal(int, str)
    textChanged = pyqtSignal()  # Sinal para mudanças de texto
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setup_context_menu()
        
        # Configurar fonte das abas
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
        # Contador para nomes de abas
        self.tab_counter = 1
        
        # Dicionário para armazenar informações das abas
        self.tab_info = {}
        
        # Conectar sinais para detectar mudanças
        self.currentChanged.connect(self._on_tab_changed)
    
    def setup_context_menu(self):
        """Configura menu de contexto para as abas"""
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
    
    def show_context_menu(self, position):
        """Mostra menu de contexto"""
        menu = QMenu()
        
        # Ações do menu
        new_tab_action = QAction("📄 Nova Aba", self)
        new_tab_action.triggered.connect(self.add_new_tab)
        
        save_action = QAction("💾 Salvar", self)
        save_action.triggered.connect(self.save_current_tab)
        
        save_as_action = QAction("💾 Salvar Como", self)
        save_as_action.triggered.connect(self.save_as_current_tab)
        
        close_action = QAction("❌ Fechar Aba", self)
        close_action.triggered.connect(lambda: self.close_tab(self.currentIndex()))
        
        close_others_action = QAction("🔒 Fechar Outras Abas", self)
        close_others_action.triggered.connect(self.close_other_tabs)
        
        close_all_action = QAction("🚪 Fechar Todas as Abas", self)
        close_all_action.triggered.connect(self.close_all_tabs)
        
        # Adiciona ações ao menu
        menu.addAction(new_tab_action)
        menu.addSeparator()
        menu.addAction(save_action)
        menu.addAction(save_as_action)
        menu.addSeparator()
        menu.addAction(close_action)
        menu.addAction(close_others_action)
        menu.addAction(close_all_action)
        
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
            'modified': False,
            'editor': editor
        }
        
        # Conectar sinais do editor
        editor.document().contentsChanged.connect(lambda: self._on_text_changed(index))
        
        return index
    
    def close_tab(self, index):
        """Fecha uma aba"""
        if index >= 0 and index < self.count():
            # Verifica se há mudanças não salvas
            editor = self.widget(index)
            if editor and hasattr(editor, 'document'):
                if editor.document().isModified():
                    reply = QMessageBox.question(
                        self, "Salvar Alterações",
                        f"Deseja salvar as alterações em '{self.tabText(index)}'?",
                        QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
                    )
                    
                    if reply == QMessageBox.Save:
                        if not self.save_current_tab():
                            return  # Usuário cancelou o salvamento
                    elif reply == QMessageBox.Cancel:
                        return  # Usuário cancelou o fechamento
            
            # Remove a aba
            self.removeTab(index)
            
            # Emite sinal
            self.tab_closed.emit(index)
            
            # Reorganiza o dicionário de informações
            new_tab_info = {}
            for i in range(self.count()):
                if i < index:
                    new_tab_info[i] = self.tab_info.get(i, {})
                else:
                    new_tab_info[i] = self.tab_info.get(i + 1, {})
            self.tab_info = new_tab_info
    
    def close_other_tabs(self):
        """Fecha todas as abas exceto a atual"""
        current_index = self.currentIndex()
        for i in range(self.count() - 1, -1, -1):
            if i != current_index:
                self.close_tab(i)
    
    def close_all_tabs(self):
        """Fecha todas as abas"""
        while self.count() > 0:
            if not self.close_tab(0):
                break  # Usuário cancelou
    
    def _on_tab_changed(self, index):
        """Chamado quando a aba atual muda"""
        self.textChanged.emit()
    
    def _on_text_changed(self, tab_index):
        """Chamado quando o texto de uma aba muda"""
        if tab_index in self.tab_info:
            self.tab_info[tab_index]['modified'] = True
            # Adiciona indicador de modificação no nome da aba
            current_text = self.tabText(tab_index)
            if not current_text.endswith('●'):
                self.setTabText(tab_index, current_text + '●')
        
        self.textChanged.emit()
    
    def save_current_tab(self):
        """Salva a aba atual"""
        current_index = self.currentIndex()
        if current_index >= 0:
            editor = self.widget(current_index)
            if editor:
                content = editor.toPlainText()
                self.tab_saved.emit(current_index, content)
                self.tab_info[current_index]['modified'] = False # Marca como salva
                self.setTabText(current_index, self.tabText(current_index)[:-1]) # Remove asterisco
                return True
        return False
    
    def save_as_current_tab(self):
        """Salva a aba atual com novo nome"""
        current_index = self.currentIndex()
        if current_index >= 0:
            editor = self.widget(current_index)
            if editor:
                content = editor.toPlainText()
                # Emite sinal para que a janela principal trate do "Salvar Como"
                self.tab_saved.emit(current_index, content)
                self.tab_info[current_index]['modified'] = False # Marca como salva
                self.setTabText(current_index, self.tabText(current_index)[:-1]) # Remove asterisco
    
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
    
    def get_current_tab_info(self):
        """Retorna informações da aba atual"""
        current_index = self.currentIndex()
        if current_index >= 0:
            return self.tab_info.get(current_index, {})
        return {}
    
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