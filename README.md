# 🐍 PyPy IDE - IDE Python Moderna

Uma IDE Python moderna e elegante desenvolvida com PyQt5, oferecendo uma experiência de desenvolvimento completa e intuitiva.

## ✨ Características Principais

### 🎨 Interface Moderna
- **Ícones Unicode Modernos**: Interface limpa e intuitiva com ícones Unicode
- **Sistema de Temas**: Múltiplos temas disponíveis (Dracula, VS Code Dark, Light, etc.)
- **Interface Responsiva**: Layout adaptável com splitters e toolbars

### 📝 Editor Avançado
- **Syntax Highlighting**: Destaque de sintaxe para Python
- **Autocompletar Inteligente**: Sugestões baseadas em pacotes instalados
- **Snippets de Código**: Templates pré-definidos para acelerar o desenvolvimento
- **Múltiplas Abas**: Suporte a múltiplos arquivos simultaneamente
- **Números de Linha**: Visualização da posição do cursor

### 💻 Terminal Integrado
- **Comandos Avançados**: Sistema completo de comandos internos
- **Navegação por Histórico**: Use ↑↓ para navegar no histórico de comandos
- **Comandos do Sistema**: Execução de comandos Python, pip, git, etc.
- **Comandos da IDE**: Controle da IDE via terminal

### 📁 Gerenciamento de Arquivos
- **Explorador de Arquivos**: Navegação visual de diretórios
- **Abertura Inteligente**: Detecta arquivos já abertos
- **Salvamento Automático**: Opção de salvamento automático
- **Múltiplos Formatos**: Suporte a diferentes tipos de arquivo

### 🔧 Ferramentas Integradas
- **Gerenciador de Pacotes**: Instalação e gerenciamento de pacotes Python
- **Debug Básico**: Funcionalidades de debug integradas
- **Configurações**: Interface de configuração personalizável
- **Sistema de Ajuda**: Documentação integrada

## 🚀 Comandos do Terminal

### 📁 Navegação
```bash
cd <diretório>     # Muda diretório
pwd                # Mostra diretório atual
ls, dir            # Lista arquivos
```

### 📄 Arquivos
```bash
new                # Novo arquivo
open <arquivo>     # Abre arquivo
save               # Salva arquivo atual
del <arquivo>      # Deleta arquivo
copy <orig> <dest> # Copia arquivo
move <orig> <dest> # Move arquivo
```

### 🔧 Sistema
```bash
cls, clear         # Limpa console
python <script>    # Executa script Python
pip <comando>      # Executa pip
git <comando>      # Executa git
```

### 🎨 IDE
```bash
theme              # Muda tema
snippets           # Gerencia snippets
packages           # Gerencia pacotes
explorer           # Mostra/oculta explorador
run                # Executa arquivo atual
status             # Status da IDE
help               # Mostra ajuda
```

## ⌨️ Atalhos de Teclado

### 📄 Arquivo
- `Ctrl+N` - Novo arquivo
- `Ctrl+O` - Abrir arquivo
- `Ctrl+S` - Salvar
- `Ctrl+T` - Nova aba
- `Ctrl+Q` - Sair

### ✏️ Editar
- `Ctrl+Z` - Desfazer
- `Ctrl+Y` - Refazer
- `Ctrl+C` - Copiar
- `Ctrl+V` - Colar
- `Ctrl+X` - Recortar

### 🚀 Execução
- `F5` - Executar código
- `F6` - Debug
- `Ctrl+`` - Terminal integrado

### 🗂️ Navegação
- `Ctrl+E` - Mostrar/ocultar explorador
- `Ctrl+F` - Buscar
- `Ctrl+H` - Substituir

### 🎨 Interface
- `F1` - Ajuda
- `Ctrl+,` - Configurações

## 🛠️ Instalação

### Pré-requisitos
- Python 3.7+
- PyQt5

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pypy-ide.git
cd pypy-ide

# Instale as dependências
pip install -r requirements.txt

# Execute a IDE
python main.py
```

## 📦 Dependências

```
PyQt5>=5.15.0
```

## 🎨 Temas Disponíveis

- **Dracula**: Tema escuro elegante
- **VS Code Dark**: Tema escuro inspirado no VS Code
- **Light**: Tema claro
- **Monokai**: Tema colorido
- **Solarized**: Tema suave

## 🔧 Configuração

A IDE oferece uma interface de configuração completa onde você pode:

- Ajustar tamanho da fonte
- Configurar largura da tabulação
- Definir tema padrão
- Configurar histórico de comandos
- Personalizar comportamento do terminal

## 💡 Dicas de Uso

1. **Terminal Integrado**: Use `Ctrl+`` para abrir o terminal
2. **Histórico de Comandos**: Use ↑↓ no terminal para navegar
3. **Autocompletar**: Digite e pressione `Ctrl+Space` para sugestões
4. **Snippets**: Use o menu Editar > Snippets para templates
5. **Temas**: Experimente diferentes temas em Visual > Temas
6. **Explorador**: Use `Ctrl+E` para mostrar/ocultar o explorador

## 🐛 Debug

Para reportar bugs ou sugerir melhorias:

1. Abra uma issue no GitHub
2. Inclua informações sobre seu sistema
3. Descreva o problema detalhadamente

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- PyQt5 pela excelente framework GUI
- Comunidade Python pela inspiração
- Contribuidores que ajudaram a melhorar a IDE

---

**Desenvolvido com ❤️ em Python** 