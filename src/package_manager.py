import subprocess
import sys
import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal


class PackageInstallerThread(QThread):
    """Thread para instalar pacotes sem bloquear a interface"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)
    
    def __init__(self, package_name):
        super().__init__()
        self.package_name = package_name
    
    def run(self):
        try:
            self.output_signal.emit(f"Instalando {self.package_name}...\n")
            
            # Executa pip install
            process = subprocess.Popen(
                [sys.executable, "-m", "pip", "install", self.package_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Captura saída em tempo real
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.output_signal.emit(output)
            
            # Verifica se houve erro
            return_code = process.poll()
            if return_code == 0:
                self.finished_signal.emit(True, f"Pacote {self.package_name} instalado com sucesso!")
            else:
                error_output = process.stderr.read()
                self.finished_signal.emit(False, f"Erro ao instalar {self.package_name}: {error_output}")
                
        except Exception as e:
            self.finished_signal.emit(False, f"Erro: {str(e)}")


class PackageManagerDialog(QDialog):
    """Dialog para gerenciar pacotes Python"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciador de Pacotes")
        self.setGeometry(300, 300, 500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Campo para nome do pacote
        package_layout = QHBoxLayout()
        self.package_input = QLineEdit()
        self.package_input.setPlaceholderText("Nome do pacote (ex: requests, numpy)")
        package_layout.addWidget(QLabel("Pacote:"))
        package_layout.addWidget(self.package_input)
        
        # Botões
        button_layout = QHBoxLayout()
        self.install_button = QPushButton("Instalar")
        self.install_button.clicked.connect(self.install_package)
        self.list_button = QPushButton("Listar Instalados")
        self.list_button.clicked.connect(self.list_installed_packages)
        button_layout.addWidget(self.install_button)
        button_layout.addWidget(self.list_button)
        
        # Área de saída
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        
        layout.addLayout(package_layout)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("Saída:"))
        layout.addWidget(self.output_area)
        
        self.setLayout(layout)
    
    def install_package(self):
        package_name = self.package_input.text().strip()
        if not package_name:
            QMessageBox.warning(self, "Erro", "Digite o nome do pacote!")
            return
        
        self.install_button.setEnabled(False)
        self.output_area.clear()
        
        # Cria e inicia thread de instalação
        self.installer_thread = PackageInstallerThread(package_name)
        self.installer_thread.output_signal.connect(self.update_output)
        self.installer_thread.finished_signal.connect(self.installation_finished)
        self.installer_thread.start()
    
    def update_output(self, text):
        self.output_area.append(text)
        # Auto-scroll para o final
        cursor = self.output_area.textCursor()
        cursor.movePosition(cursor.End)
        self.output_area.setTextCursor(cursor)
    
    def installation_finished(self, success, message):
        self.install_button.setEnabled(True)
        if success:
            self.output_area.append(f"\n✅ {message}")
            QMessageBox.information(self, "Sucesso", message)
        else:
            self.output_area.append(f"\n❌ {message}")
            QMessageBox.critical(self, "Erro", message)
    
    def list_installed_packages(self):
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.output_area.clear()
                self.output_area.append("📦 Pacotes Instalados:\n")
                self.output_area.append(result.stdout)
            else:
                self.output_area.append(f"Erro ao listar pacotes: {result.stderr}")
        except Exception as e:
            self.output_area.append(f"Erro: {str(e)}")


def get_installed_packages():
    """Retorna lista de pacotes instalados"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=freeze"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            packages = []
            for line in result.stdout.split('\n'):
                if line.strip():
                    package_name = line.split('==')[0].lower()
                    packages.append(package_name)
            return packages
        return []
    except:
        return [] 