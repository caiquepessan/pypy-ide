# PyPy IDE 🐍

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um editor de código Python simples, elegante e funcional desenvolvido com PyQt5. O PyPy IDE oferece uma interface moderna com tema Dracula, syntax highlighting, numeração de linhas e um console integrado para execução de código Python.

![PyPy IDE Interface](https://i.imgur.com/8zIkSzy.png)

## ✨ Características

- 🎨 **Tema Dracula**: Interface moderna e elegante com cores escuras
- 📝 **Syntax Highlighting**: Destaque de sintaxe para Python com Pygments
- 🔢 **Numeração de Linhas**: Visualização clara das linhas de código
- 🎯 **Breakpoints Visuais**: Clique na área de numeração para definir breakpoints
- ▶️ **Execução Integrada**: Execute código Python diretamente na IDE
- 💻 **Console Integrado**: Terminal embutido para comandos do sistema
- 📁 **Gerenciamento de Arquivos**: Abrir, salvar e salvar como arquivos Python
- ⌨️ **Atalhos de Teclado**: Navegação rápida com atalhos intuitivos

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/caiquepessan/pypy-ide.git
   cd pypy-ide
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação**
   ```bash
   python main.py
   ```

## 🎮 Como Usar

### Interface Principal

A IDE é dividida em duas áreas principais:

- **Editor de Código**: Área superior para escrever código Python
- **Console de Saída**: Área inferior para ver resultados e executar comandos

### Funcionalidades Principais

#### 📝 Editor de Código
- Digite seu código Python no editor
- Syntax highlighting automático
- Numeração de linhas
- Destaque da linha atual
- Breakpoints visuais (clique na área de numeração)

#### ▶️ Executar Código
- **F5**: Executa o código Python no editor
- **Botão Executar**: Clique no botão da barra de ferramentas
- **Menu**: Arquivo → Executar

#### 💻 Console Integrado
- Digite comandos do sistema no console
- Use `>> ` como prefixo para comandos
- Pressione Enter para executar

#### 📁 Gerenciamento de Arquivos
- **Ctrl+O**: Abrir arquivo
- **Ctrl+S**: Salvar arquivo
- **Salvar Como**: Menu Arquivo → Salvar Como

### Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `F5` | Executar código |
| `Ctrl+O` | Abrir arquivo |
| `Ctrl+S` | Salvar arquivo |
| `Ctrl+Q` | Sair da aplicação |

## 🏗️ Estrutura do Projeto

```
pypy-ide/
├── main.py                 # Ponto de entrada da aplicação
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
├── LICENSE                # Licença do projeto
└── src/                   # Código fonte
    ├── __init__.py        # Inicializador do pacote
    ├── constants.py       # Constantes e configurações
    ├── syntax_highlighter.py  # Syntax highlighting
    ├── code_editor.py     # Editor de código
    └── main_window.py     # Janela principal da IDE
```

## 🎨 Tema Dracula

O PyPy IDE utiliza o tema Dracula, oferecendo:

- **Cores Escuras**: Reduz fadiga visual
- **Alto Contraste**: Melhor legibilidade
- **Paleta Harmoniosa**: Cores cuidadosamente escolhidas

### Paleta de Cores

- **Fundo**: `#282a36`
- **Texto**: `#f8f8f2`
- **Palavras-chave**: `#ff79c6`
- **Funções**: `#50fa7b`
- **Strings**: `#f1fa8c`
- **Comentários**: `#6272a4`
- **Números**: `#bd93f9`

## 🔧 Desenvolvimento

### Estrutura Modular

O projeto foi organizado em módulos separados para facilitar manutenção e extensão:

- **`constants.py`**: Centraliza configurações e cores
- **`syntax_highlighter.py`**: Gerencia highlighting de sintaxe
- **`code_editor.py`**: Editor de código com numeração de linhas
- **`main_window.py`**: Janela principal e lógica da aplicação

### Adicionando Novas Funcionalidades

1. **Novos Temas**: Modifique `DRACULA_COLORS` em `constants.py`
2. **Novos Atalhos**: Adicione em `main_window.py`
3. **Novos Menus**: Estenda `_create_menu()` em `main_window.py`

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Mantenha o código limpo e bem documentado
- Adicione testes para novas funcionalidades
- Siga as convenções de nomenclatura Python
- Atualize a documentação quando necessário

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- **PyQt5**: Framework para interface gráfica
- **Pygments**: Biblioteca para syntax highlighting
- **Tema Dracula**: Inspiração para as cores da interface
- **Comunidade Python**: Por todas as ferramentas e bibliotecas

## 📞 Contato

- **GitHub**: [@ciquepessan](https://github.com/ciquepessan)
- **Email**: ciquepessan123@gmail.com
- **Projeto**: [PyPy IDE](https://github.com/ciquepessan/pypy-ide)

---

⭐ Se este projeto te ajudou, considere dar uma estrela no repositório! 