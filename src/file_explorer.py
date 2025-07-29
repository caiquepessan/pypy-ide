import os
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem, QVBoxLayout, 
                             QHBoxLayout, QWidget, QPushButton, QLineEdit,
                             QFileDialog, QMenu, QAction, QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont


class FileExplorer(QWidget):
    """Explorador de arquivos para a IDE"""
    
    file_selected = pyqtSignal(str)  # Emite o caminho do arquivo selecionado
    file_double_clicked = pyqtSignal(str)  # Emite quando arquivo é clicado duas vezes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_directory = os.getcwd()
        self.setup_ui()
        self.load_directory(self.current_directory)
    
    def setup_ui(self):
        """Configura a interface do explorador"""
        layout = QVBoxLayout()
        
        # Barra de ferramentas
        toolbar = QHBoxLayout()
        
        # Botão para voltar
        self.back_button = QPushButton("←")
        self.back_button.setToolTip("Voltar")
        self.back_button.clicked.connect(self.go_back)
        toolbar.addWidget(self.back_button)
        
        # Campo de caminho
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText("Caminho atual...")
        toolbar.addWidget(self.path_edit)
        
        # Botão para navegar
        self.browse_button = QPushButton("📁")
        self.browse_button.setToolTip("Navegar para pasta")
        self.browse_button.clicked.connect(self.browse_directory)
        toolbar.addWidget(self.browse_button)
        
        layout.addLayout(toolbar)
        
        # Árvore de arquivos
        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Arquivos")
        self.tree.setFont(QFont("Consolas", 9))
        self.tree.itemDoubleClicked.connect(self.on_item_double_clicked)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.tree)
        
        self.setLayout(layout)
        self.setMaximumWidth(300)
    
    def load_directory(self, path):
        """Carrega um diretório na árvore"""
        self.current_directory = path
        self.path_edit.setText(path)
        self.tree.clear()
        
        try:
            # Adiciona item para voltar (se não estiver na raiz)
            if path != os.path.dirname(path):
                back_item = QTreeWidgetItem(self.tree, [".."])
                back_item.setIcon(0, QIcon.fromTheme("go-up"))
            
            # Lista arquivos e pastas
            items = os.listdir(path)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower()))
            
            for item in items:
                item_path = os.path.join(path, item)
                tree_item = QTreeWidgetItem(self.tree, [item])
                
                # Define ícone baseado no tipo
                if os.path.isdir(item_path):
                    tree_item.setIcon(0, QIcon.fromTheme("folder"))
                    tree_item.setForeground(0, self.palette().color(self.palette().Link))
                else:
                    # Ícone baseado na extensão
                    ext = os.path.splitext(item)[1].lower()
                    if ext == '.py':
                        tree_item.setIcon(0, QIcon.fromTheme("text-x-python"))
                    elif ext in ['.txt', '.md', '.rst']:
                        tree_item.setIcon(0, QIcon.fromTheme("text-x-generic"))
                    elif ext in ['.json', '.xml', '.html', '.css', '.js']:
                        tree_item.setIcon(0, QIcon.fromTheme("text-x-script"))
                    else:
                        tree_item.setIcon(0, QIcon.fromTheme("text-x-generic"))
                
                # Armazena o caminho completo no item
                tree_item.setData(0, Qt.UserRole, item_path)
                
        except PermissionError:
            QMessageBox.warning(self, "Erro", "Sem permissão para acessar este diretório.")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar diretório: {e}")
    
    def go_back(self):
        """Volta para o diretório pai"""
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir != self.current_directory:
            self.load_directory(parent_dir)
    
    def browse_directory(self):
        """Abre dialog para escolher diretório"""
        directory = QFileDialog.getExistingDirectory(
            self, "Selecionar Diretório", self.current_directory
        )
        if directory:
            self.load_directory(directory)
    
    def on_item_double_clicked(self, item, column):
        """Chamado quando um item é clicado duas vezes"""
        item_path = item.data(0, Qt.UserRole)
        if item_path:
            if os.path.isdir(item_path):
                self.load_directory(item_path)
            else:
                self.file_double_clicked.emit(item_path)
    
    def show_context_menu(self, position):
        """Mostra menu de contexto"""
        item = self.tree.itemAt(position)
        if not item:
            return
        
        item_path = item.data(0, Qt.UserRole)
        if not item_path:
            return
        
        menu = QMenu()
        
        if os.path.isdir(item_path):
            # Menu para pastas
            open_action = QAction("Abrir Pasta", self)
            open_action.triggered.connect(lambda: self.load_directory(item_path))
            menu.addAction(open_action)
            
            menu.addSeparator()
            
            new_file_action = QAction("Novo Arquivo", self)
            new_file_action.triggered.connect(lambda: self.create_new_file(item_path))
            menu.addAction(new_file_action)
            
            new_folder_action = QAction("Nova Pasta", self)
            new_folder_action.triggered.connect(lambda: self.create_new_folder(item_path))
            menu.addAction(new_folder_action)
            
        else:
            # Menu para arquivos
            open_action = QAction("Abrir Arquivo", self)
            open_action.triggered.connect(lambda: self.file_double_clicked.emit(item_path))
            menu.addAction(open_action)
            
            menu.addSeparator()
            
            delete_action = QAction("Excluir", self)
            delete_action.triggered.connect(lambda: self.delete_item(item_path))
            menu.addAction(delete_action)
        
        menu.exec_(self.tree.mapToGlobal(position))
    
    def create_new_file(self, directory):
        """Cria um novo arquivo"""
        from PyQt5.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Novo Arquivo", "Nome do arquivo:")
        if ok and name:
            file_path = os.path.join(directory, name)
            try:
                with open(file_path, 'w') as f:
                    pass
                self.load_directory(self.current_directory)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar arquivo: {e}")
    
    def create_new_folder(self, directory):
        """Cria uma nova pasta"""
        from PyQt5.QtWidgets import QInputDialog
        
        name, ok = QInputDialog.getText(self, "Nova Pasta", "Nome da pasta:")
        if ok and name:
            folder_path = os.path.join(directory, name)
            try:
                os.makedirs(folder_path, exist_ok=True)
                self.load_directory(self.current_directory)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao criar pasta: {e}")
    
    def delete_item(self, item_path):
        """Exclui um item"""
        reply = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja excluir '{os.path.basename(item_path)}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if os.path.isdir(item_path):
                    os.rmdir(item_path)
                else:
                    os.remove(item_path)
                self.load_directory(self.current_directory)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir item: {e}")
    
    def get_current_directory(self):
        """Retorna o diretório atual"""
        return self.current_directory
    
    def set_current_directory(self, path):
        """Define o diretório atual"""
        if os.path.exists(path):
            self.load_directory(path) 