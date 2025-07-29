# PyPy IDE 🐍

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Um editor de código Python simples, elegante e funcional desenvolvido com PyQt5. O PyPy IDE oferece uma interface moderna com tema Dracula, syntax highlighting, numeração de linhas e um console integrado para execução de código Python.

![PyPy IDE Interface](https://i.ibb.co/R1nHZvq/image.png)

## ✨ Características

- **Editor de Código Avançado**: Syntax highlighting para Python, numeração de linhas, e destaque da linha atual
- **Múltiplas Abas**: Suporte a múltiplos arquivos abertos simultaneamente com indicadores de modificação
- **Autocompletar Inteligente**: Sugestões baseadas em keywords, built-ins e pacotes instalados
- **Gerenciador de Pacotes**: Instalação e gerenciamento de pacotes Python via pip
- **Snippets de Código**: Templates pré-definidos para acelerar o desenvolvimento
- **Suporte a Input/Output**: Execução interativa com suporte a `input()` e `print()`
- **Barra de Status**: Informações em tempo real sobre arquivo, posição do cursor e encoding
- **Múltiplos Temas**: 6 temas profissionais incluindo VS Code Dark, Dracula, Monokai, Solarized Dark, GitHub Dark e One Dark
- **Explorador de Arquivos**: Navegação e gerenciamento de arquivos integrado
- **Interface Aprimorada**: Design moderno e profissional similar ao VS Code
- **Cursor e Seleção Melhorados**: Estilização avançada do cursor e seleção de texto
- **Abas com Botões de Fechamento**: Interface de abas moderna com indicadores visuais
- **Menu de Contexto Avançado**: Menus contextuais ricos com ícones e funcionalidades

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
- Suporte completo a input() e print()

#### 📦 Gerenciador de Pacotes
- Instale bibliotecas Python diretamente na IDE
- Visualize pacotes instalados
- Interface gráfica para gerenciamento de dependências

#### 🎯 Autocompletar Inteligente
- Sugestões de palavras-chave Python
- Autocompletar de funções built-in
- Suporte a bibliotecas instaladas
- Atualização automática de sugestões

#### ⌨️ Snippets de Código
- Templates prontos para estruturas comuns
- Acesso via menu Editar → Snippets
- Inserção rápida de código boilerplate

## 🎨 Múltiplos Temas

A IDE PyPy oferece 6 temas profissionais para personalizar sua experiência de desenvolvimento:

### VS Code Dark (Padrão)
- **Tema principal**: Baseado no Visual Studio Code
- **Cores**: Cinza escuro (#1e1e1e) com azul de destaque (#007acc)
- **Ideal para**: Desenvolvedores que preferem a aparência do VS Code

### Dracula
- **Cores**: Roxo escuro (#282a36) com tons vibrantes
- **Destaque**: Verde (#50fa7b) e rosa (#ff79c6)
- **Ideal para**: Quem gosta de cores contrastantes e vibrantes

### Monokai
- **Cores**: Cinza muito escuro (#272822) com cores neon
- **Destaque**: Verde neon (#a6e22e) e rosa (#f92672)
- **Ideal para**: Desenvolvedores que preferem temas com cores neon

### Solarized Dark
- **Cores**: Azul esverdeado (#002b36) com tons suaves
- **Destaque**: Laranja (#cb4b16) e verde (#859900)
- **Ideal para**: Redução de fadiga visual e longas sessões de código

### GitHub Dark
- **Cores**: Cinza muito escuro (#0d1117) com azul GitHub
- **Destaque**: Azul (#1f6feb) e verde (#238636)
- **Ideal para**: Quem gosta da aparência do GitHub Dark

### One Dark
- **Cores**: Cinza escuro (#282c34) com tons quentes
- **Destaque**: Roxo (#c678dd) e azul (#61afef)
- **Ideal para**: Desenvolvedores que preferem temas equilibrados

### Como Trocar de Tema
1. Clique no botão **🎨** na barra de ferramentas
2. Selecione o tema desejado na lista
3. O tema será aplicado instantaneamente
4. A escolha é salva automaticamente

#### 📁 Explorador de Arquivos
- Navegação completa de arquivos e pastas
- Clique duplo para abrir arquivos
- Menu de contexto para criar/excluir arquivos
- Integração completa com o editor

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
| `Ctrl+T` | Nova aba |
| `Ctrl+Z` | Desfazer |
| `Ctrl+Y` | Refazer |
| `Ctrl+E` | Mostrar/Ocultar Explorador |
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