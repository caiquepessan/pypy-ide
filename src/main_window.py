import sys
import subprocess
import io
import contextlib
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPlainTextEdit, QAction, 
                             QFileDialog, QMessageBox, QToolBar, QVBoxLayout, 
                             QWidget, QSplitter, QShortcut)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt
from .constants import IDE_TITLE, DRACULA_COLORS
from .code_editor import CodeEditor
from .syntax_highlighter import PythonHighlighter


class IDEMainWindow(QMainWindow):
    """Janela principal da IDE PyPy"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(IDE_TITLE)
        self.setGeometry(100, 100, 800, 600)

        # Inicializar componentes
        self.editor = CodeEditor()
        self.highlighter = PythonHighlighter(self.editor.document())
        self.output_console = self._create_console()
        
        # Configurar layout
        self._setup_layout()
        self._create_toolbar()
        self._create_menu()

        # Variáveis de estado
        self.filename = ""
        self.process = None

        # Atalho F5 para executar o código
        shortcut = QShortcut(QKeySequence("F5"), self)
        shortcut.activated.connect(self.run_code)

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
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.output_console)
        splitter.setSizes([400, 200])

        layout = QVBoxLayout()
        layout.addWidget(splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _create_toolbar(self):
        """Cria a barra de ferramentas"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Botão de executar
        run_action = QAction(QIcon.fromTheme("media-playback-start"), "Executar", self)
        run_action.triggered.connect(self.run_code)
        toolbar.addAction(run_action)

    def _create_menu(self):
        """Cria o menu da aplicação"""
        menu = self.menuBar().addMenu("Arquivo")

        # Ação Abrir
        open_file = QAction("Abrir", self)
        open_file.setShortcut("Ctrl+O")
        open_file.triggered.connect(self.open_file)
        menu.addAction(open_file)

        # Ação Salvar
        save_file = QAction("Salvar", self)
        save_file.setShortcut("Ctrl+S")
        save_file.triggered.connect(self.save_file)
        menu.addAction(save_file)

        # Ação Salvar Como
        save_as_file = QAction("Salvar Como", self)
        save_as_file.triggered.connect(self.save_file_as)
        menu.addAction(save_as_file)

        # Separador
        menu.addSeparator()

        # Ação Sair
        exit_app = QAction("Sair", self)
        exit_app.setShortcut("Ctrl+Q")
        exit_app.triggered.connect(self.close)
        menu.addAction(exit_app)

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
                    self.editor.setPlainText(file.read())
                self.filename = filename
                self.setWindowTitle(f"{IDE_TITLE} - {self.filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao abrir arquivo: {e}")

    def save_file(self):
        """Salva o arquivo atual"""
        if self.filename == "":
            self.save_file_as()
        else:
            try:
                with open(self.filename, 'w', encoding='utf-8') as file:
                    file.write(self.editor.toPlainText())
                QMessageBox.information(self, "Salvo", "Arquivo salvo com sucesso!")
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
            self.filename = filename
            self.save_file()
            self.setWindowTitle(f"{IDE_TITLE} - {self.filename}")

    def run_code(self):
        """Executa o código Python no editor"""
        code = self.editor.toPlainText()
        if not code.strip():
            self.output_console.appendPlainText("Nenhum código para executar.")
            return
            
        try:
            # Redireciona a saída padrão
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec(code, {})
            
            result = output.getvalue()
            if result:
                self.output_console.appendPlainText(result)
            else:
                self.output_console.appendPlainText("Código executado com sucesso!")
                
        except Exception as e:
            self.output_console.appendPlainText(f"Erro:\n{e}")

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