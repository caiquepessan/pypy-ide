import sys
import subprocess
import io
import contextlib
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPlainTextEdit, QAction, 
                             QFileDialog, QMessageBox, QToolBar, QVBoxLayout, 
                             QWidget, QSplitter, QShortcut, QMenu, QMenuBar,
                             QStatusBar, QProgressBar, QLabel, QSize)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt, QTimer
from .constants import IDE_TITLE, DRACULA_COLORS
from .code_editor import CodeEditor
from .syntax_highlighter import PythonHighlighter
from .tab_manager import TabManager
from .input_dialog import InputManager, CodeExecutor
from .package_manager import PackageManagerDialog
from .autocomplete import CodeEditorCompleter, SnippetManager
from .theme_manager import ThemeManager
from .file_explorer import FileExplorer


class IDEMainWindow(QMainWindow):
    """Janela principal da IDE PyPy"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(IDE_TITLE)
        self.setGeometry(100, 100, 1200, 800)

        # Inicializar componentes
        self.tab_manager = TabManager()
        self.output_console = self._create_console()
        
        # Sistema de input/output
        self.input_manager = InputManager(self)
        self.code_executor = CodeExecutor(self.input_manager, self.append_to_console)
        
        # Gerenciador de snippets
        self.snippet_manager = SnippetManager()
        
        # Gerenciador de temas
        self.theme_manager = ThemeManager()
        self.theme_manager.set_theme('vscode_dark')  # Usar tema VS Code por padrão
        
        # Explorador de arquivos
        self.file_explorer = FileExplorer()
        self.file_explorer.file_double_clicked.connect(self.open_file_from_explorer)
        
        # Configurar layout
        self._setup_layout()
        self._create_toolbar()
        self._create_menu()
        self._create_status_bar()
        
        # Aplicar tema
        self.theme_manager.apply_theme_to_widget(self)

        # Variáveis de estado
        self.filename = ""
        self.process = None
        self.current_tab_index = 0

        # Conectar sinais
        self.tab_manager.tab_closed.connect(self.on_tab_closed)
        self.tab_manager.tab_saved.connect(self.on_tab_saved)
        
        # Configurar autocompletar para a primeira aba
        self._setup_autocomplete()
        
        # Adicionar primeira aba
        self.tab_manager.add_new_tab()
        
        # Atalhos de teclado
        self._setup_shortcuts()

    def _create_console(self):
        """Cria o console de saída"""
        console = QPlainTextEdit()
        console.setStyleSheet(f"background-color: {DRACULA_COLORS['background']}; color: {DRACULA_COLORS['foreground']};")
        console.installEventFilter(self)
        console.setPlainText(">> ")  # Prefixo do terminal
        console.setUndoRedoEnabled(False)  # Não permitir desfazer para manter o terminal consistente
        return console

    def _setup_layout(self):
        """Configura o layout da janela"""
        # Splitter principal horizontal
        main_splitter = QSplitter(Qt.Horizontal)
        
        # Adiciona explorador de arquivos
        main_splitter.addWidget(self.file_explorer)
        
        # Splitter vertical para editor e console
        editor_splitter = QSplitter(Qt.Vertical)
        editor_splitter.addWidget(self.tab_manager)
        editor_splitter.addWidget(self.output_console)
        editor_splitter.setSizes([600, 200])
        
        main_splitter.addWidget(editor_splitter)
        main_splitter.setSizes([250, 950])

        layout = QVBoxLayout()
        layout.addWidget(main_splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # Botão Novo Arquivo
        new_action = QAction("📄", self)
        new_action.setToolTip("Novo Arquivo (Ctrl+N)")
        new_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_action)
        
        # Botão Abrir
        open_action = QAction("📂", self)
        open_action.setToolTip("Abrir Arquivo (Ctrl+O)")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # Botão Salvar
        save_action = QAction("💾", self)
        save_action.setToolTip("Salvar (Ctrl+S)")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Botão Executar
        run_action = QAction("▶️", self)
        run_action.setToolTip("Executar Código (F5)")
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)
        
        toolbar.addSeparator()
        
        # Botão Nova Aba
        new_tab_action = QAction("➕", self)
        new_tab_action.setToolTip("Nova Aba (Ctrl+T)")
        new_tab_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_tab_action)
        
        # Botão Pacotes
        packages_action = QAction("📦", self)
        packages_action.setToolTip("Gerenciador de Pacotes")
        packages_action.triggered.connect(self.show_package_manager)
        toolbar.addAction(packages_action)
        
        # Botão Explorador
        explorer_action = QAction("🗂️", self)
        explorer_action.setToolTip("Mostrar/Ocultar Explorador")
        explorer_action.triggered.connect(self.toggle_file_explorer)
        toolbar.addAction(explorer_action)
        
        # Botão Temas
        themes_action = QAction("🎨", self)
        themes_action.setToolTip("Selecionar Tema")
        themes_action.triggered.connect(self.show_theme_selector)
        toolbar.addAction(themes_action)
        
        self.addToolBar(toolbar)

    def _create_menu(self):
        """Cria o menu da aplicação"""
        # Menu Arquivo
        file_menu = self.menuBar().addMenu("Arquivo")

        # Ação Nova Aba
        new_tab = QAction("Nova Aba", self)
        new_tab.setShortcut("Ctrl+T")
        new_tab.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab)

        # Ação Abrir
        open_file = QAction("Abrir", self)
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)
        file_menu.addAction(open_file)

        # Ação Salvar
        save_file = QAction("Salvar", self)
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)
        file_menu.addAction(save_file)

        # Ação Salvar Como
        save_as_file = QAction("Salvar Como", self)
        save_as_file.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_file)

        # Separador
        file_menu.addSeparator()

        # Ação Sair
        exit_app = QAction("Sair", self)
        exit_app.setShortcut("Ctrl+Q")
        exit_app.triggered.connect(self.close)
        file_menu.addAction(exit_app)

        # Menu Editar
        edit_menu = self.menuBar().addMenu("Editar")
        
        # Ação Desfazer
        undo_action = QAction("Desfazer", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        # Ação Refazer
        redo_action = QAction("Refazer", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Menu Snippets
        snippets_menu = edit_menu.addMenu("Snippets")
        self._populate_snippets_menu(snippets_menu)

        # Menu Ferramentas
        tools_menu = self.menuBar().addMenu("Ferramentas")
        
        # Ação Gerenciador de Pacotes
        package_action = QAction("Gerenciador de Pacotes", self)
        package_action.triggered.connect(self.show_package_manager)
        tools_menu.addAction(package_action)
        
        # Ação Atualizar Autocompletar
        update_completion_action = QAction("Atualizar Autocompletar", self)
        update_completion_action.triggered.connect(self.update_autocomplete)
        tools_menu.addAction(update_completion_action)
        
        # Menu Visual
        visual_menu = self.menuBar().addMenu("Visual")
        
        # Submenu Temas
        themes_menu = visual_menu.addMenu("Temas")
        self._populate_themes_menu(themes_menu)
        
        # Ação Explorador de Arquivos
        explorer_action = QAction("Mostrar/Ocultar Explorador", self)
        explorer_action.setShortcut("Ctrl+E")
        explorer_action.triggered.connect(self.toggle_file_explorer)
        visual_menu.addAction(explorer_action)

    def open_file(self):
        """Abre um arquivo Python"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(
            self, "Abrir Arquivo", "",
            "Arquivos Python (*.py);;Todos os Arquivos (*)",
            options=options
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Verifica se o arquivo já está aberto em outra aba
                existing_tab = self.tab_manager.find_tab_by_filename(filename)
                if existing_tab >= 0:
                    self.tab_manager.setCurrentIndex(existing_tab)
                else:
                    # Adiciona nova aba com o conteúdo
                    index = self.tab_manager.add_new_tab(filename, content)
                    self._setup_autocomplete_for_tab(index)
                
                self.setWindowTitle(f"{IDE_TITLE} - {filename}")
                self.status_label.setText(f"Arquivo aberto: {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao abrir arquivo: {e}")

    def save_file(self):
        """Salva o arquivo atual"""
        current_editor = self.tab_manager.get_current_editor()
        if not current_editor:
            return
            
        current_index = self.tab_manager.currentIndex()
        tab_info = self.tab_manager.tab_info.get(current_index, {})
        filename = tab_info.get('filename')
        
        if not filename:
            self.save_file_as()
        else:
            try:
                content = current_editor.toPlainText()
                with open(filename, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.tab_manager.set_tab_modified(current_index, False)
                QMessageBox.information(self, "Salvo", "Arquivo salvo com sucesso!")
                self.status_label.setText(f"Arquivo salvo: {filename}")
                
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar arquivo: {e}")

    def save_file_as(self):
        """Salva o arquivo com um novo nome"""
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(
            self, "Salvar Arquivo", "",
            "Arquivos Python (*.py);;Todos os Arquivos (*)",
            options=options
        )
        if filename:
            try:
                current_editor = self.tab_manager.get_current_editor()
                if current_editor:
                    content = current_editor.toPlainText()
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(content)
                    
                    # Atualiza informações da aba
                    current_index = self.tab_manager.currentIndex()
                    if current_index in self.tab_manager.tab_info:
                        self.tab_manager.tab_info[current_index]['filename'] = filename
                        self.tab_manager.set_tab_modified(current_index, False)
                    
                    # Atualiza nome da aba
                    tab_name = filename.split('/')[-1]
                    self.tab_manager.setTabText(current_index, tab_name)
                    
                    self.setWindowTitle(f"{IDE_TITLE} - {filename}")
                    self.status_label.setText(f"Arquivo salvo como: {filename}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar arquivo: {e}")

    def run_code(self):
        """Executa o código Python no editor"""
        code = self.tab_manager.get_current_content()
        if not code.strip():
            self.append_to_console("Nenhum código para executar.\n")
            return
            
        # Limpa o console
        self.output_console.clear()
        self.append_to_console("🚀 Executando código...\n")
        
        # Executa o código com suporte a input/output
        self.code_executor.execute_code(code)
    
    def append_to_console(self, text):
        """Adiciona texto ao console"""
        self.output_console.appendPlainText(text)
    
    def add_new_tab(self):
        """Adiciona uma nova aba"""
        index = self.tab_manager.add_new_tab()
        self._setup_autocomplete_for_tab(index)
    
    def _setup_autocomplete(self):
        """Configura autocompletar para a aba atual"""
        current_editor = self.tab_manager.get_current_editor()
        if current_editor:
            self.completer = CodeEditorCompleter(current_editor)
    
    def _setup_autocomplete_for_tab(self, tab_index):
        """Configura autocompletar para uma aba específica"""
        editor = self.tab_manager.widget(tab_index)
        if editor:
            completer = CodeEditorCompleter(editor)
    
    def update_autocomplete(self):
        """Atualiza o autocompletar com pacotes instalados"""
        if hasattr(self, 'completer'):
            self.completer.update_package_completions()
        self.append_to_console("✅ Autocompletar atualizado!\n")
    
    def show_package_manager(self):
        """Mostra o gerenciador de pacotes"""
        dialog = PackageManagerDialog(self)
        dialog.exec_()
    
    def _populate_snippets_menu(self, menu):
        """Popula o menu de snippets"""
        snippets = self.snippet_manager.get_all_snippets()
        for name, code in snippets.items():
            action = QAction(name, self)
            action.triggered.connect(lambda checked, n=name: self.insert_snippet(n))
            menu.addAction(action)
    
    def insert_snippet(self, snippet_name):
        """Insere um snippet no editor atual"""
        snippet_code = self.snippet_manager.get_snippet(snippet_name)
        if snippet_code:
            current_editor = self.tab_manager.get_current_editor()
            if current_editor:
                cursor = current_editor.textCursor()
                cursor.insertText(snippet_code)
                current_editor.setTextCursor(cursor)
    
    def undo(self):
        """Desfaz a última ação"""
        current_editor = self.tab_manager.get_current_editor()
        if current_editor:
            current_editor.undo()
    
    def redo(self):
        """Refaz a última ação"""
        current_editor = self.tab_manager.get_current_editor()
        if current_editor:
            current_editor.redo()
    
    def _setup_shortcuts(self):
        """Configura atalhos de teclado"""
        # F5 para executar
        run_shortcut = QShortcut(QKeySequence("F5"), self)
        run_shortcut.activated.connect(self.run_code)
        
        # Ctrl+T para nova aba
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)
        
        # Ctrl+E para explorador de arquivos
        explorer_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        explorer_shortcut.activated.connect(self.toggle_file_explorer)
    
    def _create_status_bar(self):
        """Cria a barra de status"""
        status_bar = QStatusBar()
        
        # Informações do arquivo
        self.file_info_label = QLabel("Nenhum arquivo aberto")
        status_bar.addWidget(self.file_info_label)
        
        # Separador
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Posição do cursor
        self.cursor_position_label = QLabel("Linha 1, Coluna 1")
        status_bar.addPermanentWidget(self.cursor_position_label)
        
        # Separador
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Encoding
        self.encoding_label = QLabel("UTF-8")
        status_bar.addPermanentWidget(self.encoding_label)
        
        # Separador
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Modo de inserção
        self.insert_mode_label = QLabel("INS")
        status_bar.addPermanentWidget(self.insert_mode_label)
        
        # Conectar sinais para atualizar posição do cursor
        self.tab_manager.currentChanged.connect(self.update_cursor_position)
        
        # Conectar sinais para atualizar quando o texto mudar
        self.tab_manager.textChanged.connect(self.update_cursor_position)
        
        self.setStatusBar(status_bar)
        
    def update_cursor_position(self):
        """Atualiza a posição do cursor na barra de status"""
        current_editor = self.tab_manager.get_current_editor()
        if current_editor:
            cursor = current_editor.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.positionInBlock() + 1
            self.cursor_position_label.setText(f"Linha {line}, Coluna {column}")
            
            # Atualizar informações do arquivo
            tab_info = self.tab_manager.get_current_tab_info()
            if tab_info and tab_info.get('filename'):
                filename = tab_info['filename']
                modified = "●" if tab_info.get('modified', False) else ""
                self.file_info_label.setText(f"{filename} {modified}")
            else:
                self.file_info_label.setText("Nenhum arquivo aberto")
    
    def on_tab_closed(self, index):
        """Chamado quando uma aba é fechada"""
        self.status_label.setText(f"Aba {index} fechada")
    
    def on_tab_saved(self, index, content):
        """Chamado quando uma aba é salva"""
        self.status_label.setText(f"Aba {index} salva")
        self.tab_manager.set_tab_modified(index, False)
    
    def open_file_from_explorer(self, file_path):
        """Abre arquivo selecionado no explorador"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Verifica se o arquivo já está aberto
            existing_tab = self.tab_manager.find_tab_by_filename(file_path)
            if existing_tab >= 0:
                self.tab_manager.setCurrentIndex(existing_tab)
            else:
                # Adiciona nova aba com o conteúdo
                index = self.tab_manager.add_new_tab(file_path, content)
                self._setup_autocomplete_for_tab(index)
            
            self.setWindowTitle(f"{IDE_TITLE} - {file_path}")
            self.status_label.setText(f"Arquivo aberto: {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir arquivo: {e}")
    
    def toggle_file_explorer(self):
        """Mostra/oculta o explorador de arquivos"""
        if self.file_explorer.isVisible():
            self.file_explorer.hide()
            self.status_label.setText("Explorador de arquivos oculto")
        else:
            self.file_explorer.show()
            self.status_label.setText("Explorador de arquivos visível")
    
    def _populate_themes_menu(self, menu):
        """Popula o menu de temas"""
        themes = self.theme_manager.get_theme_names()
        for theme_id, theme_name in themes.items():
            action = QAction(theme_name, self)
            action.setCheckable(True)
            action.setChecked(theme_id == self.theme_manager.current_theme)
            action.triggered.connect(lambda checked, t=theme_id: self.change_theme(t))
            menu.addAction(action)
    
    def change_theme(self, theme_name):
        """Muda o tema da aplicação"""
        self.theme_manager.set_theme(theme_name)
        self.theme_manager.apply_theme_to_widget(self)
        self.status_label.setText(f"Tema alterado para: {self.theme_manager.get_theme(theme_name)['name']}")
    
    def show_theme_selector(self):
        """Mostra seletor de temas"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Selecionar Tema")
        dialog.setGeometry(300, 200, 400, 150)
        
        layout = QVBoxLayout()
        
        # Label
        layout.addWidget(QLabel("Escolha um tema:"))
        
        # Combo box com temas
        theme_combo = QComboBox()
        themes = self.theme_manager.get_theme_names()
        for theme_id, theme_name in themes.items():
            theme_combo.addItem(theme_name, theme_id)
        
        # Define o tema atual
        current_index = theme_combo.findData(self.theme_manager.current_theme)
        if current_index >= 0:
            theme_combo.setCurrentIndex(current_index)
        
        layout.addWidget(theme_combo)
        
        # Botões
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Aplicar")
        cancel_button = QPushButton("Cancelar")
        
        ok_button.clicked.connect(lambda: self.apply_selected_theme(theme_combo.currentData(), dialog))
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def apply_selected_theme(self, theme_name, dialog):
        """Aplica o tema selecionado"""
        self.change_theme(theme_name)
        dialog.accept()

    def eventFilter(self, obj, event):
        """Intercepta eventos no console"""
        if obj == self.output_console and event.type() == 6:  # Evento de tecla pressionada
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                text = self.output_console.toPlainText().split('\n')[-1].strip()
                command = text[3:]  # Remove o prefixo ">> "
                self.run_terminal_command(command)
                return True
        return super().eventFilter(obj, event)

    def run_terminal_command(self, command):
        """Executa comandos no terminal"""
        if command:
            try:
                process = subprocess.run(command, shell=True, capture_output=True, text=True)
                if process.returncode == 0:
                    if process.stdout:
                        self.output_console.appendPlainText(process.stdout)
                else:
                    if process.stderr:
                        self.output_console.appendPlainText(process.stderr)
            except Exception as e:
                self.output_console.appendPlainText(f"Erro ao executar comando: {e}")
        self.output_console.appendPlainText(">> ")  # Adiciona o prefixo para o próximo comando 