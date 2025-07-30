import sys
import subprocess
import io
import contextlib
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPlainTextEdit, QAction,
                                    QFileDialog, QMessageBox, QToolBar, QVBoxLayout,
                                    QWidget, QSplitter, QShortcut, QMenu, QMenuBar,
                                    QStatusBar, QProgressBar, QLabel)
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QKeySequence
from .constants import IDE_TITLE, DRACULA_COLORS
from .code_editor import CodeEditor
from .syntax_highlighter import PythonHighlighter
from .tab_manager import TabManager
from .input_dialog import InputManager, CodeExecutor
from .package_manager import PackageManagerDialog
from .autocomplete import CodeEditorCompleter, SnippetManager
from .theme_manager import ThemeManager
from .file_explorer import FileExplorer
from .icons import modern_icons, TextIcons
from .terminal_commands import TerminalCommands


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
        
        # Sistema de comandos do terminal
        self.terminal_commands = TerminalCommands(self)
        
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
        """Cria a barra de ferramentas com ícones SVG modernos"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        
        # Botão Novo Arquivo
        new_action = QAction("", self)
        new_action.setIcon(modern_icons.new_file(24))
        new_action.setToolTip("Novo Arquivo (Ctrl+N)")
        new_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_action)
        
        # Botão Abrir
        open_action = QAction("", self)
        open_action.setIcon(modern_icons.open_file(24))
        open_action.setToolTip("Abrir Arquivo (Ctrl+O)")
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)
        
        # Botão Salvar
        save_action = QAction("", self)
        save_action.setIcon(modern_icons.save_file(24))
        save_action.setToolTip("Salvar (Ctrl+S)")
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Botão Executar
        run_action = QAction("", self)
        run_action.setIcon(modern_icons.run_code(24))
        run_action.setToolTip("Executar Código (F5)")
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)
        
        # Botão Debug
        debug_action = QAction("", self)
        debug_action.setIcon(modern_icons.debug(24))
        debug_action.setToolTip("Debug (F6)")
        debug_action.triggered.connect(self.debug_code)
        toolbar.addAction(debug_action)
        
        toolbar.addSeparator()
        
        # Botão Nova Aba
        new_tab_action = QAction("", self)
        new_tab_action.setIcon(modern_icons.new_file(24))
        new_tab_action.setToolTip("Nova Aba (Ctrl+T)")
        new_tab_action.triggered.connect(self.add_new_tab)
        toolbar.addAction(new_tab_action)
        
        # Botão Pacotes
        packages_action = QAction("", self)
        packages_action.setIcon(modern_icons.packages(24))
        packages_action.setToolTip("Gerenciador de Pacotes")
        packages_action.triggered.connect(self.show_package_manager)
        toolbar.addAction(packages_action)
        
        # Botão Explorador
        explorer_action = QAction("", self)
        explorer_action.setIcon(modern_icons.explorer(24))
        explorer_action.setToolTip("Mostrar/Ocultar Explorador (Ctrl+E)")
        explorer_action.triggered.connect(self.toggle_file_explorer)
        toolbar.addAction(explorer_action)
        
        # Botão Temas
        themes_action = QAction("", self)
        themes_action.setIcon(modern_icons.themes(24))
        themes_action.setToolTip("Selecionar Tema")
        themes_action.triggered.connect(self.show_theme_selector)
        toolbar.addAction(themes_action)
        
        # Botão Terminal
        terminal_action = QAction("", self)
        terminal_action.setIcon(modern_icons.terminal(24))
        terminal_action.setToolTip("Terminal Integrado (Ctrl+`)")
        terminal_action.triggered.connect(self.toggle_terminal)
        toolbar.addAction(terminal_action)
        
        # Botão Configurações
        settings_action = QAction("", self)
        settings_action.setIcon(modern_icons.settings(24))
        settings_action.setToolTip("Configurações")
        settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(settings_action)
        
        self.addToolBar(toolbar)

    def _create_menu(self):
        """Cria o menu da aplicação com ícones modernos"""
        # Menu Arquivo
        file_menu = self.menuBar().addMenu(f"{TextIcons.FILE_MENU} Arquivo")

        # Ação Nova Aba
        new_tab = QAction(f"{TextIcons.NEW_TAB} Nova Aba", self)
        new_tab.setShortcut("Ctrl+T")
        new_tab.triggered.connect(self.add_new_tab)
        file_menu.addAction(new_tab)

        # Ação Abrir
        open_file = QAction(f"{TextIcons.OPEN_FILE} Abrir", self)
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)
        file_menu.addAction(open_file)

        # Ação Salvar
        save_file = QAction(f"{TextIcons.SAVE_FILE} Salvar", self)
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)
        file_menu.addAction(save_file)

        # Ação Salvar Como
        save_as_file = QAction(f"{TextIcons.SAVE_AS} Salvar Como", self)
        save_as_file.triggered.connect(self.save_file_as)
        file_menu.addAction(save_as_file)

        # Separador
        file_menu.addSeparator()

        # Ação Sair
        exit_app = QAction(f"{TextIcons.COMMAND_EXIT} Sair", self)
        exit_app.setShortcut("Ctrl+Q")
        exit_app.triggered.connect(self.close)
        file_menu.addAction(exit_app)

        # Menu Editar
        edit_menu = self.menuBar().addMenu(f"{TextIcons.EDIT_MENU} Editar")
        
        # Ação Desfazer
        undo_action = QAction(f"{TextIcons.UNDO} Desfazer", self)
        undo_action.setShortcut("Ctrl+Z")
        undo_action.triggered.connect(self.undo)
        edit_menu.addAction(undo_action)
        
        # Ação Refazer
        redo_action = QAction(f"{TextIcons.REDO} Refazer", self)
        redo_action.setShortcut("Ctrl+Y")
        redo_action.triggered.connect(self.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Menu Snippets
        snippets_menu = edit_menu.addMenu(f"{TextIcons.SNIPPETS} Snippets")
        self._populate_snippets_menu(snippets_menu)

        # Menu Ferramentas
        tools_menu = self.menuBar().addMenu(f"{TextIcons.TOOLS_MENU} Ferramentas")
        
        # Ação Gerenciador de Pacotes
        package_action = QAction(f"{TextIcons.PACKAGES} Gerenciador de Pacotes", self)
        package_action.triggered.connect(self.show_package_manager)
        tools_menu.addAction(package_action)
        
        # Ação Atualizar Autocompletar
        update_completion_action = QAction(f"{TextIcons.AUTOCOMPLETE} Atualizar Autocompletar", self)
        update_completion_action.triggered.connect(self.update_autocomplete)
        tools_menu.addAction(update_completion_action)
        
        # Ação Terminal
        terminal_action = QAction(f"{TextIcons.TERMINAL} Terminal Integrado", self)
        terminal_action.setShortcut("Ctrl+`")
        terminal_action.triggered.connect(self.toggle_terminal)
        tools_menu.addAction(terminal_action)
        
        # Menu Visual
        visual_menu = self.menuBar().addMenu(f"{TextIcons.VIEW_MENU} Visual")
        
        # Submenu Temas
        themes_menu = visual_menu.addMenu(f"{TextIcons.THEMES} Temas")
        self._populate_themes_menu(themes_menu)
        
        # Ação Explorador de Arquivos
        explorer_action = QAction(f"{TextIcons.EXPLORER} Mostrar/Ocultar Explorador", self)
        explorer_action.setShortcut("Ctrl+E")
        explorer_action.triggered.connect(self.toggle_file_explorer)
        visual_menu.addAction(explorer_action)
        
        # Menu Ajuda
        help_menu = self.menuBar().addMenu(f"{TextIcons.HELP_MENU} Ajuda")
        
        # Ação Sobre
        about_action = QAction(f"{TextIcons.ABOUT} Sobre", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Ação Ajuda
        help_action = QAction(f"{TextIcons.HELP} Ajuda", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

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
                self.file_info_label.setText(f"Arquivo aberto: {filename}")
                
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
                self.file_info_label.setText(f"Arquivo salvo: {filename}")
                
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
                    self.file_info_label.setText(f"Arquivo salvo como: {filename}")
                    
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar arquivo: {e}")

    def run_code(self):
        """Executa o código Python no editor"""
        code = self.tab_manager.get_current_content()
        if not code.strip():
            self.append_to_console(f"{TextIcons.ERROR} Nenhum código para executar.\n")
            return
            
        # Limpa o console
        self.output_console.clear()
        self.append_to_console(f"{TextIcons.RUN_CODE} Executando código...\n")
        
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
        self.append_to_console(f"{TextIcons.SUCCESS} Autocompletar atualizado!\n")
    
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
        self.file_info_label.setText(f"Aba {index} fechada")
    
    def on_tab_saved(self, index, content):
        """Chamado quando uma aba é salva"""
        self.file_info_label.setText(f"Aba {index} salva")
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
            self.file_info_label.setText(f"Arquivo aberto: {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir arquivo: {e}")
    
    def toggle_file_explorer(self):
        """Mostra/oculta o explorador de arquivos"""
        if self.file_explorer.isVisible():
            self.file_explorer.hide()
            self.file_info_label.setText(f"{TextIcons.EXPLORER} Explorador oculto")
        else:
            self.file_explorer.show()
            self.file_info_label.setText(f"{TextIcons.EXPLORER} Explorador visível")
    
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
        self.file_info_label.setText(f"{TextIcons.THEMES} Tema: {self.theme_manager.get_theme(theme_name)['name']}")
    
    def show_theme_selector(self):
        """Mostra seletor de temas"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{TextIcons.THEMES} Selecionar Tema")
        dialog.setGeometry(300, 200, 400, 150)
        
        layout = QVBoxLayout()
        
        # Label
        layout.addWidget(QLabel(f"{TextIcons.THEMES} Escolha um tema:"))
        
        # Combo box com temas
        theme_combo = QComboBox()
        themes = self.theme_manager.get_theme_names()
        for theme_id, theme_name in themes.items():
            theme_combo.addItem(f"{TextIcons.THEMES} {theme_name}", theme_id)
        
        # Define o tema atual
        current_index = theme_combo.findData(self.theme_manager.current_theme)
        if current_index >= 0:
            theme_combo.setCurrentIndex(current_index)
        
        layout.addWidget(theme_combo)
        
        # Botões
        button_layout = QHBoxLayout()
        ok_button = QPushButton(f"{TextIcons.SUCCESS} Aplicar")
        cancel_button = QPushButton(f"{TextIcons.ERROR} Cancelar")
        
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
    
    def debug_code(self):
        """Executa o código em modo debug"""
        code = self.tab_manager.get_current_content()
        if not code.strip():
            self.append_to_console(f"{TextIcons.ERROR} Nenhum código para executar em debug.\n")
            return
        
        self.append_to_console(f"{TextIcons.DEBUG} Iniciando debug...\n")
        # Aqui você pode implementar funcionalidades de debug mais avançadas
        self.append_to_console(f"{TextIcons.INFO} Debug iniciado. Use breakpoints para controlar a execução.\n")
    
    def toggle_terminal(self):
        """Mostra/oculta o terminal integrado"""
        if self.output_console.isVisible():
            self.output_console.hide()
            self.file_info_label.setText(f"{TextIcons.TERMINAL} Terminal oculto")
        else:
            self.output_console.show()
            self.file_info_label.setText(f"{TextIcons.TERMINAL} Terminal visível")
    
    def show_settings(self):
        """Mostra a janela de configurações"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QSpinBox, QCheckBox, QTabWidget, QWidget
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{TextIcons.SETTINGS} Configurações - PyPy IDE")
        dialog.setGeometry(400, 300, 600, 400)
        
        layout = QVBoxLayout()
        
        # Abas para diferentes categorias
        tab_widget = QTabWidget()
        
        # Aba Geral
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        
        # Configurações do editor
        general_layout.addWidget(QLabel("Configurações do Editor:"))
        
        # Tamanho da fonte
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("Tamanho da fonte:"))
        font_size_spin = QSpinBox()
        font_size_spin.setRange(8, 24)
        font_size_spin.setValue(12)
        font_layout.addWidget(font_size_spin)
        general_layout.addLayout(font_layout)
        
        # Largura da tabulação
        tab_layout = QHBoxLayout()
        tab_layout.addWidget(QLabel("Largura da tabulação:"))
        tab_width_spin = QSpinBox()
        tab_width_spin.setRange(2, 8)
        tab_width_spin.setValue(4)
        tab_layout.addWidget(tab_width_spin)
        general_layout.addLayout(tab_layout)
        
        # Opções
        auto_save_check = QCheckBox("Salvar automaticamente")
        auto_save_check.setChecked(True)
        general_layout.addWidget(auto_save_check)
        
        line_numbers_check = QCheckBox("Mostrar números de linha")
        line_numbers_check.setChecked(True)
        general_layout.addWidget(line_numbers_check)
        
        general_tab.setLayout(general_layout)
        tab_widget.addTab(general_tab, "Geral")
        
        # Aba Terminal
        terminal_tab = QWidget()
        terminal_layout = QVBoxLayout()
        
        terminal_layout.addWidget(QLabel("Configurações do Terminal:"))
        
        # Histórico de comandos
        history_layout = QHBoxLayout()
        history_layout.addWidget(QLabel("Histórico de comandos:"))
        history_spin = QSpinBox()
        history_spin.setRange(10, 100)
        history_spin.setValue(50)
        history_layout.addWidget(history_spin)
        terminal_layout.addLayout(history_layout)
        
        # Comandos personalizados
        custom_commands_check = QCheckBox("Permitir comandos personalizados")
        custom_commands_check.setChecked(True)
        terminal_layout.addWidget(custom_commands_check)
        
        terminal_tab.setLayout(terminal_layout)
        tab_widget.addTab(terminal_tab, "Terminal")
        
        # Aba Temas
        themes_tab = QWidget()
        themes_layout = QVBoxLayout()
        
        themes_layout.addWidget(QLabel("Configurações de Tema:"))
        
        # Tema padrão
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Tema padrão:"))
        theme_combo = QComboBox()
        themes = self.theme_manager.get_theme_names()
        for theme_id, theme_name in themes.items():
            theme_combo.addItem(theme_name, theme_id)
        theme_layout.addWidget(theme_combo)
        themes_layout.addLayout(theme_layout)
        
        themes_tab.setLayout(themes_layout)
        tab_widget.addTab(themes_tab, "Temas")
        
        layout.addWidget(tab_widget)
        
        # Botões
        button_layout = QHBoxLayout()
        ok_button = QPushButton(f"{TextIcons.SUCCESS} Aplicar")
        cancel_button = QPushButton(f"{TextIcons.ERROR} Cancelar")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def open_file_from_path(self, file_path):
        """Abre arquivo a partir de um caminho específico"""
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
            self.file_info_label.setText(f"Arquivo aberto: {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao abrir arquivo: {e}")
    
    def show_about(self):
        """Mostra a janela Sobre"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
        from PyQt5.QtCore import Qt
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{TextIcons.INFO} Sobre PyPy IDE")
        dialog.setGeometry(300, 200, 500, 300)
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel("🐍 PyPy IDE")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #50fa7b;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Versão
        version_label = QLabel("Versão 2.0 - IDE Moderna em Python")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        # Descrição
        desc_label = QLabel("""
        Uma IDE Python moderna e elegante com:
        • Editor de código com syntax highlighting
        • Terminal integrado com comandos avançados
        • Gerenciador de pacotes
        • Sistema de temas
        • Autocompletar inteligente
        • Explorador de arquivos
        • Snippets de código
        • Interface moderna com ícones Unicode
        
        Desenvolvido com PyQt5 e Python 3
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(desc_label)
        
        # Botão OK
        ok_button = QPushButton(f"{TextIcons.SUCCESS} OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def show_help(self):
        """Mostra a janela de ajuda"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit
        from PyQt5.QtCore import Qt
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"{TextIcons.COMMAND_HELP} Ajuda - PyPy IDE")
        dialog.setGeometry(400, 300, 700, 500)
        dialog.setModal(True)
        
        layout = QVBoxLayout()
        
        # Título
        title_label = QLabel(f"{TextIcons.COMMAND_HELP} Ajuda do PyPy IDE")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #50fa7b;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Área de texto com ajuda
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setPlainText("""
ATALHOS DE TECLADO:
═══════════════════

📄 Arquivo:
  Ctrl+N     - Novo arquivo
  Ctrl+O     - Abrir arquivo
  Ctrl+S     - Salvar
  Ctrl+T     - Nova aba
  Ctrl+Q     - Sair

✏️ Editar:
  Ctrl+Z     - Desfazer
  Ctrl+Y     - Refazer
  Ctrl+C     - Copiar
  Ctrl+V     - Colar
  Ctrl+X     - Recortar

🚀 Execução:
  F5         - Executar código
  F6         - Debug
  Ctrl+`     - Terminal integrado

🗂️ Navegação:
  Ctrl+E     - Mostrar/ocultar explorador
  Ctrl+F     - Buscar
  Ctrl+H     - Substituir

🎨 Interface:
  F1         - Ajuda
  Ctrl+,     - Configurações

COMANDOS DO TERMINAL:
══════════════════════

📁 Navegação:
  cd <dir>   - Mudar diretório
  pwd        - Diretório atual
  ls, dir    - Listar arquivos

📄 Arquivos:
  new        - Novo arquivo
  open <file> - Abrir arquivo
  save       - Salvar arquivo
  del <file> - Deletar arquivo

🔧 Sistema:
  cls, clear - Limpar console
  python <script> - Executar Python
  pip <cmd>  - Executar pip
  git <cmd>  - Executar git

🎨 IDE:
  theme      - Mudar tema
  snippets   - Gerenciar snippets
  packages   - Gerenciar pacotes
  status     - Status da IDE
  help       - Mostrar ajuda

💡 DICAS:
═══════════

• Use ↑↓ no terminal para navegar no histórico
• Digite 'help' no terminal para ver todos os comandos
• Use Ctrl+` para abrir o terminal integrado
• Os ícones modernos tornam a interface mais intuitiva
• O sistema de temas permite personalizar a aparência
• O autocompletar ajuda na produtividade
• Os snippets aceleram o desenvolvimento

Para mais informações, consulte a documentação ou digite 'help' no terminal.
        """)
        layout.addWidget(help_text)
        
        # Botão OK
        ok_button = QPushButton(f"{TextIcons.SUCCESS} OK")
        ok_button.clicked.connect(dialog.accept)
        layout.addWidget(ok_button)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def eventFilter(self, obj, event):
        """Intercepta eventos no console com suporte a histórico"""
        if obj == self.output_console and event.type() == 6:  # Evento de tecla pressionada
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                text = self.output_console.toPlainText().split('\n')[-1].strip()
                command = text[3:]  # Remove o prefixo ">> "
                self.terminal_commands.execute_command(command)
                self.output_console.appendPlainText(">> ")
                return True
            elif event.key() == Qt.Key_Up:
                # Navegação no histórico - comando anterior
                prev_command = self.terminal_commands.get_previous_command()
                if prev_command:
                    # Substitui a linha atual pelo comando anterior
                    lines = self.output_console.toPlainText().split('\n')
                    lines[-1] = f">> {prev_command}"
                    self.output_console.setPlainText('\n'.join(lines))
                return True
            elif event.key() == Qt.Key_Down:
                # Navegação no histórico - próximo comando
                next_command = self.terminal_commands.get_next_command()
                if next_command:
                    # Substitui a linha atual pelo próximo comando
                    lines = self.output_console.toPlainText().split('\n')
                    lines[-1] = f">> {next_command}"
                    self.output_console.setPlainText('\n'.join(lines))
                return True
        return super().eventFilter(obj, event) 