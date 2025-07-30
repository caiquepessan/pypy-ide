import os
import subprocess
import platform
import shutil
from pathlib import Path
from .icons import TextIcons

class TerminalCommands:
    """Sistema de comandos do terminal integrado"""
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.command_history = []
        self.history_index = -1
        self.current_directory = os.getcwd()
        
        # Comandos internos disponíveis
        self.internal_commands = {
            'cls': self.clear_console,
            'clear': self.clear_console,
            'help': self.show_help,
            '?': self.show_help,
            'exit': self.exit_terminal,
            'quit': self.exit_terminal,
            'pwd': self.show_current_directory,
            'ls': self.list_directory,
            'dir': self.list_directory,
            'cd': self.change_directory,
            'mkdir': self.make_directory,
            'rmdir': self.remove_directory,
            'del': self.delete_file,
            'rm': self.delete_file,
            'copy': self.copy_file,
            'cp': self.copy_file,
            'move': self.move_file,
            'mv': self.move_file,
            'type': self.show_file_content,
            'cat': self.show_file_content,
            'echo': self.echo_text,
            'history': self.show_history,
            'cls': self.clear_console,
            'clear': self.clear_console,
            'python': self.run_python,
            'pip': self.run_pip,
            'git': self.run_git,
            'status': self.show_status,
            'info': self.show_info,
            'theme': self.change_theme,
            'snippets': self.show_snippets,
            'packages': self.show_packages,
            'explorer': self.toggle_explorer,
            'new': self.new_file,
            'open': self.open_file,
            'save': self.save_file,
            'run': self.run_current_file
        }
    
    def execute_command(self, command):
        """Executa um comando do terminal"""
        if not command.strip():
            return
        
        # Adiciona à história
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Divide o comando em partes
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        # Verifica se é um comando interno
        if cmd in self.internal_commands:
            try:
                self.internal_commands[cmd](*args)
            except Exception as e:
                self.print_error(f"Erro ao executar comando interno: {e}")
        else:
            # Executa comando do sistema
            self.run_system_command(command)
    
    def clear_console(self, *args):
        """Limpa o console"""
        self.main_window.output_console.clear()
        self.main_window.append_to_console(f"{TextIcons.CLEAR_CONSOLE} Console limpo!\n")
        self.main_window.append_to_console(">> ")
    
    def show_help(self, *args):
        """Mostra ajuda dos comandos"""
        help_text = f"""
{TextIcons.COMMAND_HELP} Comandos disponíveis:

📁 Navegação:
  cd <diretório>     - Muda diretório
  pwd                - Mostra diretório atual
  ls, dir            - Lista arquivos

📄 Arquivos:
  new                - Novo arquivo
  open <arquivo>     - Abre arquivo
  save               - Salva arquivo atual
  del <arquivo>      - Deleta arquivo
  copy <orig> <dest> - Copia arquivo
  move <orig> <dest> - Move arquivo

🔧 Sistema:
  cls, clear         - Limpa console
  python <script>    - Executa script Python
  pip <comando>      - Executa pip
  git <comando>      - Executa git

🎨 IDE:
  theme              - Muda tema
  snippets           - Gerencia snippets
  packages           - Gerencia pacotes
  explorer           - Mostra/oculta explorador
  run                - Executa arquivo atual
  status             - Status da IDE

❓ Ajuda:
  help, ?            - Mostra esta ajuda
  history            - Mostra histórico
  exit, quit         - Sai do terminal

💡 Dica: Use ↑↓ para navegar no histórico!
"""
        self.main_window.append_to_console(help_text)
    
    def exit_terminal(self, *args):
        """Sai do terminal"""
        self.main_window.append_to_console(f"{TextIcons.COMMAND_EXIT} Saindo do terminal...\n")
    
    def show_current_directory(self, *args):
        """Mostra o diretório atual"""
        self.main_window.append_to_console(f"{TextIcons.COMMAND_PWD} Diretório atual: {os.getcwd()}\n")
    
    def list_directory(self, *args):
        """Lista arquivos do diretório"""
        try:
            path = args[0] if args else "."
            if os.path.exists(path):
                items = os.listdir(path)
                self.main_window.append_to_console(f"{TextIcons.COMMAND_LS} Conteúdo de '{path}':\n")
                
                for item in sorted(items):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        icon = TextIcons.FOLDER
                        item += "/"
                    else:
                        icon = TextIcons.get_icon_for_file_type(item)
                    
                    self.main_window.append_to_console(f"  {icon} {item}\n")
            else:
                self.print_error(f"Diretório '{path}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao listar diretório: {e}")
    
    def change_directory(self, *args):
        """Muda o diretório atual"""
        if not args:
            self.print_error("Uso: cd <diretório>")
            return
        
        try:
            new_dir = args[0]
            if new_dir == "..":
                new_dir = os.path.dirname(os.getcwd())
            elif not os.path.isabs(new_dir):
                new_dir = os.path.join(os.getcwd(), new_dir)
            
            if os.path.exists(new_dir) and os.path.isdir(new_dir):
                os.chdir(new_dir)
                self.current_directory = os.getcwd()
                self.main_window.append_to_console(f"{TextIcons.COMMAND_CD} Diretório alterado para: {os.getcwd()}\n")
            else:
                self.print_error(f"Diretório '{new_dir}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao mudar diretório: {e}")
    
    def make_directory(self, *args):
        """Cria um novo diretório"""
        if not args:
            self.print_error("Uso: mkdir <nome_do_diretório>")
            return
        
        try:
            for dir_name in args:
                os.makedirs(dir_name, exist_ok=True)
                self.main_window.append_to_console(f"{TextIcons.SUCCESS} Diretório '{dir_name}' criado\n")
        except Exception as e:
            self.print_error(f"Erro ao criar diretório: {e}")
    
    def remove_directory(self, *args):
        """Remove um diretório"""
        if not args:
            self.print_error("Uso: rmdir <nome_do_diretório>")
            return
        
        try:
            for dir_name in args:
                if os.path.exists(dir_name):
                    shutil.rmtree(dir_name)
                    self.main_window.append_to_console(f"{TextIcons.SUCCESS} Diretório '{dir_name}' removido\n")
                else:
                    self.print_error(f"Diretório '{dir_name}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao remover diretório: {e}")
    
    def delete_file(self, *args):
        """Deleta um arquivo"""
        if not args:
            self.print_error("Uso: del <arquivo>")
            return
        
        try:
            for file_name in args:
                if os.path.exists(file_name):
                    os.remove(file_name)
                    self.main_window.append_to_console(f"{TextIcons.SUCCESS} Arquivo '{file_name}' removido\n")
                else:
                    self.print_error(f"Arquivo '{file_name}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao remover arquivo: {e}")
    
    def copy_file(self, *args):
        """Copia um arquivo"""
        if len(args) < 2:
            self.print_error("Uso: copy <origem> <destino>")
            return
        
        try:
            source = args[0]
            destination = args[1]
            
            if os.path.exists(source):
                shutil.copy2(source, destination)
                self.main_window.append_to_console(f"{TextIcons.SUCCESS} Arquivo copiado: {source} → {destination}\n")
            else:
                self.print_error(f"Arquivo '{source}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao copiar arquivo: {e}")
    
    def move_file(self, *args):
        """Move um arquivo"""
        if len(args) < 2:
            self.print_error("Uso: move <origem> <destino>")
            return
        
        try:
            source = args[0]
            destination = args[1]
            
            if os.path.exists(source):
                shutil.move(source, destination)
                self.main_window.append_to_console(f"{TextIcons.SUCCESS} Arquivo movido: {source} → {destination}\n")
            else:
                self.print_error(f"Arquivo '{source}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao mover arquivo: {e}")
    
    def show_file_content(self, *args):
        """Mostra conteúdo de um arquivo"""
        if not args:
            self.print_error("Uso: type <arquivo>")
            return
        
        try:
            file_path = args[0]
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.main_window.append_to_console(f"{TextIcons.INFO} Conteúdo de '{file_path}':\n")
                    self.main_window.append_to_console(content + "\n")
            else:
                self.print_error(f"Arquivo '{file_path}' não encontrado")
        except Exception as e:
            self.print_error(f"Erro ao ler arquivo: {e}")
    
    def echo_text(self, *args):
        """Ecoa texto"""
        if args:
            text = " ".join(args)
            self.main_window.append_to_console(f"{text}\n")
    
    def show_history(self, *args):
        """Mostra histórico de comandos"""
        if self.command_history:
            self.main_window.append_to_console(f"{TextIcons.COMMAND_HISTORY} Histórico de comandos:\n")
            for i, cmd in enumerate(self.command_history[-10:], 1):  # Últimos 10 comandos
                self.main_window.append_to_console(f"  {i:2d}. {cmd}\n")
        else:
            self.main_window.append_to_console(f"{TextIcons.INFO} Nenhum comando no histórico\n")
    
    def run_system_command(self, command):
        """Executa comando do sistema"""
        try:
            process = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=self.current_directory)
            
            if process.stdout:
                self.main_window.append_to_console(process.stdout)
            
            if process.stderr:
                self.main_window.append_to_console(process.stderr)
                
            if process.returncode != 0:
                self.print_error(f"Comando retornou código de saída: {process.returncode}")
                
        except Exception as e:
            self.print_error(f"Erro ao executar comando: {e}")
    
    def run_python(self, *args):
        """Executa script Python"""
        if not args:
            self.print_error("Uso: python <script.py>")
            return
        
        script = args[0]
        if os.path.exists(script):
            try:
                process = subprocess.run(['python', script] + args[1:], 
                                      capture_output=True, text=True, cwd=self.current_directory)
                
                if process.stdout:
                    self.main_window.append_to_console(process.stdout)
                
                if process.stderr:
                    self.main_window.append_to_console(process.stderr)
                    
            except Exception as e:
                self.print_error(f"Erro ao executar script Python: {e}")
        else:
            self.print_error(f"Script '{script}' não encontrado")
    
    def run_pip(self, *args):
        """Executa comando pip"""
        try:
            process = subprocess.run(['pip'] + list(args), 
                                  capture_output=True, text=True, cwd=self.current_directory)
            
            if process.stdout:
                self.main_window.append_to_console(process.stdout)
            
            if process.stderr:
                self.main_window.append_to_console(process.stderr)
                
        except Exception as e:
            self.print_error(f"Erro ao executar pip: {e}")
    
    def run_git(self, *args):
        """Executa comando git"""
        try:
            process = subprocess.run(['git'] + list(args), 
                                  capture_output=True, text=True, cwd=self.current_directory)
            
            if process.stdout:
                self.main_window.append_to_console(process.stdout)
            
            if process.stderr:
                self.main_window.append_to_console(process.stderr)
                
        except Exception as e:
            self.print_error(f"Erro ao executar git: {e}")
    
    def show_status(self, *args):
        """Mostra status da IDE"""
        current_editor = self.main_window.tab_manager.get_current_editor()
        if current_editor:
            content = current_editor.toPlainText()
            lines = len(content.split('\n'))
            chars = len(content)
            
            status_text = f"""
{TextIcons.INFO} Status da IDE:
  📄 Arquivo atual: {self.main_window.tab_manager.get_current_tab_info().get('filename', 'Sem nome')}
  📊 Linhas: {lines}
  🔤 Caracteres: {chars}
  🎨 Tema: {self.main_window.theme_manager.current_theme}
  📁 Diretório: {os.getcwd()}
  💻 Sistema: {platform.system()} {platform.release()}
"""
            self.main_window.append_to_console(status_text)
        else:
            self.print_error("Nenhum editor ativo")
    
    def show_info(self, *args):
        """Mostra informações do sistema"""
        info_text = f"""
{TextIcons.INFO} Informações do Sistema:
  💻 Sistema Operacional: {platform.system()} {platform.release()}
  🐍 Python: {platform.python_version()}
  📁 Diretório atual: {os.getcwd()}
  👤 Usuário: {os.getenv('USERNAME', 'Desconhecido')}
  🏠 Home: {os.path.expanduser('~')}
"""
        self.main_window.append_to_console(info_text)
    
    def change_theme(self, *args):
        """Muda o tema da IDE"""
        if args:
            theme_name = args[0]
            self.main_window.change_theme(theme_name)
            self.main_window.append_to_console(f"{TextIcons.SUCCESS} Tema alterado para: {theme_name}\n")
        else:
            self.main_window.show_theme_selector()
    
    def show_snippets(self, *args):
        """Mostra snippets disponíveis"""
        snippets = self.main_window.snippet_manager.get_all_snippets()
        if snippets:
            self.main_window.append_to_console(f"{TextIcons.SNIPPETS} Snippets disponíveis:\n")
            for name in snippets.keys():
                self.main_window.append_to_console(f"  📝 {name}\n")
        else:
            self.main_window.append_to_console(f"{TextIcons.INFO} Nenhum snippet disponível\n")
    
    def show_packages(self, *args):
        """Abre gerenciador de pacotes"""
        self.main_window.show_package_manager()
        self.main_window.append_to_console(f"{TextIcons.PACKAGES} Gerenciador de pacotes aberto\n")
    
    def toggle_explorer(self, *args):
        """Mostra/oculta explorador de arquivos"""
        self.main_window.toggle_file_explorer()
        self.main_window.append_to_console(f"{TextIcons.EXPLORER} Explorador de arquivos alternado\n")
    
    def new_file(self, *args):
        """Cria novo arquivo"""
        self.main_window.add_new_tab()
        self.main_window.append_to_console(f"{TextIcons.NEW_FILE} Novo arquivo criado\n")
    
    def open_file(self, *args):
        """Abre arquivo"""
        if args:
            file_path = args[0]
            if os.path.exists(file_path):
                self.main_window.open_file_from_path(file_path)
                self.main_window.append_to_console(f"{TextIcons.OPEN_FILE} Arquivo aberto: {file_path}\n")
            else:
                self.print_error(f"Arquivo '{file_path}' não encontrado")
        else:
            self.main_window.open_file()
    
    def save_file(self, *args):
        """Salva arquivo atual"""
        self.main_window.save_file()
        self.main_window.append_to_console(f"{TextIcons.SAVE_FILE} Arquivo salvo\n")
    
    def run_current_file(self, *args):
        """Executa arquivo atual"""
        self.main_window.run_code()
        self.main_window.append_to_console(f"{TextIcons.RUN_CODE} Executando arquivo atual\n")
    
    def print_error(self, message):
        """Imprime mensagem de erro"""
        self.main_window.append_to_console(f"{TextIcons.ERROR} {message}\n")
    
    def get_previous_command(self):
        """Retorna comando anterior do histórico"""
        if self.command_history and self.history_index > 0:
            self.history_index -= 1
            return self.command_history[self.history_index]
        return ""
    
    def get_next_command(self):
        """Retorna próximo comando do histórico"""
        if self.history_index < len(self.command_history) - 1:
            self.history_index += 1
            return self.command_history[self.history_index]
        return "" 
