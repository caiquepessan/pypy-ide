import sys
import io
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QTextEdit, QLabel, QMessageBox)
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QFont


class InputDialog(QDialog):
    """Dialog para entrada de dados do usuário"""
    
    input_received = pyqtSignal(str)
    
    def __init__(self, prompt="Digite algo:", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Entrada de Dados")
        self.setGeometry(300, 200, 400, 150)
        self.setup_ui(prompt)
    
    def setup_ui(self, prompt):
        layout = QVBoxLayout()
        
        # Label com o prompt
        self.prompt_label = QLabel(prompt)
        layout.addWidget(self.prompt_label)
        
        # Campo de entrada
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.accept_input)
        layout.addWidget(self.input_field)
        
        # Botões
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_input)
        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Foca no campo de entrada
        self.input_field.setFocus()
    
    def accept_input(self):
        text = self.input_field.text()
        self.input_received.emit(text)
        self.accept()


class InputManager:
    """Gerencia entradas de dados durante execução de código"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.input_queue = []
        self.current_input_index = 0
        self.input_dialog = None
    
    def get_input(self, prompt="Digite algo:"):
        """Solicita entrada do usuário"""
        if self.current_input_index < len(self.input_queue):
            # Usa entrada pré-definida
            value = self.input_queue[self.current_input_index]
            self.current_input_index += 1
            return value
        else:
            # Solicita entrada interativa
            self.input_dialog = InputDialog(prompt, self.parent)
            result = self.input_dialog.exec_()
            if result == QDialog.Accepted:
                return self.input_dialog.input_field.text()
            else:
                return ""
    
    def set_input_queue(self, inputs):
        """Define uma fila de entradas para testes"""
        self.input_queue = inputs
        self.current_input_index = 0


class InputRedirector:
    """Redireciona input() para usar o dialog da IDE"""
    
    def __init__(self, input_manager):
        self.input_manager = input_manager
        self.original_input = input
    
    def __call__(self, prompt=""):
        return self.input_manager.get_input(prompt)


class OutputRedirector:
    """Redireciona print() para a área de saída da IDE"""
    
    def __init__(self, output_callback):
        self.output_callback = output_callback
        self.buffer = ""
    
    def write(self, text):
        self.buffer += text
        if text.endswith('\n'):
            self.output_callback(self.buffer)
            self.buffer = ""
    
    def flush(self):
        if self.buffer:
            self.output_callback(self.buffer)
            self.buffer = ""


class CodeExecutor:
    """Executor de código com suporte a input/output"""
    
    def __init__(self, input_manager, output_callback):
        self.input_manager = input_manager
        self.output_callback = output_callback
        self.output_redirector = OutputRedirector(output_callback)
        self.input_redirector = InputRedirector(input_manager)
    
    def execute_code(self, code):
        """Executa código Python com suporte a input/output"""
        try:
            # Salva funções originais
            original_stdout = sys.stdout
            original_stdin = sys.stdin
            original_input = __builtins__.input
            
            # Redireciona input/output
            sys.stdout = self.output_redirector
            __builtins__.input = self.input_redirector
            
            # Executa o código
            exec(code, {})
            
            # Restaura funções originais
            sys.stdout = original_stdout
            __builtins__.input = original_input
            
        except Exception as e:
            self.output_callback(f"Erro: {str(e)}\n")
        finally:
            # Garante que stdout seja restaurado
            if hasattr(self, 'original_stdout'):
                sys.stdout = self.original_stdout 