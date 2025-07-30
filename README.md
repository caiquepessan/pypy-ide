# 🐍 PyPy IDE v2.0 - IDE Python Moderna

Uma IDE Python moderna e elegante com interface intuitiva, ícones SVG profissionais e funcionalidades avançadas.

## ✨ Características Principais

### 🎨 Interface Moderna
- **Ícones SVG Profissionais**: Sistema de ícones vetoriais modernos e escaláveis
- **Temas Personalizáveis**: Múltiplos temas incluindo Dracula, VS Code Dark, Light e mais
- **Interface Intuitiva**: Design limpo e organizado com toolbar e menus contextuais
- **Responsividade**: Interface adaptável com splitters e layouts flexíveis

### 💻 Editor Avançado
- **Syntax Highlighting**: Destaque de sintaxe para Python com cores personalizáveis
- **Autocompletar Inteligente**: Sugestões automáticas para Python keywords, built-ins e pacotes
- **Múltiplas Abas**: Suporte a múltiplos arquivos simultâneos
- **Números de Linha**: Opcional com configuração personalizável
- **Undo/Redo**: Histórico completo de ações

### 🖥️ Terminal Integrado
- **Comandos Internos**: Sistema robusto de comandos integrados
- **Histórico de Comandos**: Navegação com setas ↑↓
- **Comandos do Sistema**: Execução de comandos do sistema operacional
- **Comandos IDE**: Controle da IDE via terminal
- **Navegação de Arquivos**: cd, ls, pwd, mkdir, rmdir, etc.

### 📁 Gerenciamento de Arquivos
- **Explorador Integrado**: Navegação visual de arquivos e pastas
- **Operações de Arquivo**: Copiar, mover, deletar, visualizar conteúdo
- **Suporte a Múltiplos Formatos**: Python, texto, imagens, áudio, vídeo
- **Ícones por Tipo**: Identificação visual por tipo de arquivo

### 🔧 Ferramentas de Desenvolvimento
- **Debug Básico**: Sistema de debug integrado
- **Gerenciador de Pacotes**: Interface para pip e instalação de pacotes
- **Snippets de Código**: Templates reutilizáveis para desenvolvimento
- **Configurações Avançadas**: Painel de configurações personalizável

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- PyQt5

### Instalação Rápida
```bash
# Clone o repositório
git clone https://github.com/caiquepessan/pypy-ide.git
cd pypy-ide

# Instale as dependências
pip install -r requirements.txt

# Execute a IDE
python main.py
```

## 🎯 Funcionalidades Detalhadas

### Ícones SVG Modernos
O PyPy IDE v2.0 utiliza um sistema completo de ícones SVG vetoriais:

- **Ícones de Arquivo**: Novo, abrir, salvar, fechar
- **Ícones de Execução**: Play, debug, stop
- **Ícones de Interface**: Terminal, configurações, explorador
- **Ícones de Ferramentas**: Pacotes, temas, snippets
- **Ícones de Status**: Sucesso, erro, informação, aviso

### Terminal Integrado Avançado
Comandos disponíveis:

#### 📁 Navegação
```bash
cd <diretório>     # Mudar diretório
pwd                # Mostrar diretório atual
ls, dir            # Listar arquivos
```

#### 📄 Operações de Arquivo
```bash
new                # Novo arquivo
open <arquivo>     # Abrir arquivo
save               # Salvar arquivo atual
del <arquivo>      # Deletar arquivo
copy <orig> <dest> # Copiar arquivo
move <orig> <dest> # Mover arquivo
type <arquivo>     # Mostrar conteúdo
```

#### 🔧 Sistema
```bash
cls, clear         # Limpar console
python <script>    # Executar script Python
pip <comando>      # Executar pip
git <comando>      # Executar git
```

#### 🎨 Controle da IDE
```bash
theme              # Mudar tema
snippets           # Gerenciar snippets
packages           # Gerenciar pacotes
explorer           # Mostrar/ocultar explorador
run                # Executar arquivo atual
status             # Status da IDE
info               # Informações do sistema
help               # Mostrar ajuda
```

### Atalhos de Teclado
- **F5**: Executar código
- **F6**: Debug
- **Ctrl+`**: Terminal integrado
- **Ctrl+E**: Mostrar/ocultar explorador
- **Ctrl+T**: Nova aba
- **Ctrl+O**: Abrir arquivo
- **Ctrl+S**: Salvar
- **F1**: Ajuda

## 🎨 Temas Disponíveis

- **Dracula**: Tema escuro elegante
- **VS Code Dark**: Inspirado no Visual Studio Code
- **Light**: Tema claro
- **Monokai**: Tema colorido
- **Solarized**: Tema suave

## 📦 Estrutura do Projeto

```
pypy-ide/
├── main.py                 # Ponto de entrada
├── requirements.txt        # Dependências
├── README.md              # Documentação
├── icons/                 # Ícones SVG
│   ├── new_file.svg
│   ├── open_file.svg
│   ├── save_file.svg
│   ├── run_code.svg
│   ├── debug.svg
│   ├── terminal.svg
│   ├── settings.svg
│   ├── explorer.svg
│   ├── themes.svg
│   ├── packages.svg
│   ├── close.svg
│   ├── help.svg
│   ├── info.svg
│   ├── success.svg
│   └── error.svg
└── src/                   # Código fonte
    ├── main_window.py     # Janela principal
    ├── icons.py          # Sistema de ícones
    ├── terminal_commands.py # Comandos do terminal
    ├── code_editor.py    # Editor de código
    ├── syntax_highlighter.py # Syntax highlighting
    ├── tab_manager.py    # Gerenciador de abas
    ├── theme_manager.py  # Gerenciador de temas
    ├── file_explorer.py  # Explorador de arquivos
    ├── autocomplete.py   # Autocompletar
    ├── package_manager.py # Gerenciador de pacotes
    ├── constants.py      # Constantes
    └── ...
```

## 🔧 Configuração

### Configurações do Editor
- Tamanho da fonte: 8-24pt
- Largura da tabulação: 2-8 espaços
- Salvar automaticamente
- Mostrar números de linha
- Word wrap

### Configurações do Terminal
- Histórico de comandos: 50 comandos
- Comandos personalizados
- Autocompletar
- Syntax highlighting

## 🐛 Debug

O sistema de debug básico inclui:
- Breakpoints visuais
- Execução passo a passo
- Informações de debug no console
- Controle de execução

## 📝 Snippets

Snippets pré-definidos incluídos:
- Classes Python
- Funções
- Estruturas de controle
- Decorators
- Context managers
- Async functions

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- **PyQt5**: Framework GUI
- **Pygments**: Syntax highlighting
- **Feather Icons**: Ícones SVG base
- **Comunidade Python**: Suporte e feedback

## 📞 Suporte

- **Issues**: Reporte bugs e sugestões no GitHub
- **Documentação**: Consulte este README
- **Terminal**: Digite `help` no terminal integrado

---

**PyPy IDE v2.0** - Transformando o desenvolvimento Python com interface moderna e funcionalidades avançadas! 🚀 