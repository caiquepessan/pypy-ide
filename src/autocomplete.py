import keyword
import builtins
from PyQt5.QtWidgets import QCompleter, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from .package_manager import get_installed_packages


class PythonCompleter(QCompleter):
    """Autocompletar para Python"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_completions()
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setWrapAround(False)
    
    def setup_completions(self):
        """Configura as sugestões de autocompletar"""
        completions = []
        
        # Palavras-chave do Python
        completions.extend(keyword.kwlist)
        
        # Funções built-in
        completions.extend(dir(builtins))
        
        # Bibliotecas comuns
        common_libs = [
            'os', 'sys', 're', 'json', 'datetime', 'time', 'random',
            'math', 'collections', 'itertools', 'functools', 'pathlib',
            'requests', 'numpy', 'pandas', 'matplotlib', 'seaborn',
            'tkinter', 'PyQt5', 'flask', 'django', 'sqlite3'
        ]
        completions.extend(common_libs)
        
        # Métodos comuns
        methods = [
            'append', 'extend', 'insert', 'remove', 'pop', 'clear',
            'index', 'count', 'sort', 'reverse', 'copy', 'len',
            'print', 'input', 'range', 'enumerate', 'zip', 'map',
            'filter', 'reduce', 'sum', 'min', 'max', 'abs', 'round',
            'str', 'int', 'float', 'bool', 'list', 'tuple', 'dict',
            'set', 'frozenset', 'open', 'read', 'write', 'close'
        ]
        completions.extend(methods)
        
        # Cria o modelo
        model = QStandardItemModel()
        for completion in sorted(set(completions)):
            item = QStandardItem(completion)
            model.appendRow(item)
        
        self.setModel(model)
    
    def update_completions(self):
        """Atualiza as sugestões com pacotes instalados"""
        try:
            installed_packages = get_installed_packages()
            model = self.model()
            
            # Adiciona pacotes instalados
            for package in installed_packages:
                item = QStandardItem(package)
                model.appendRow(item)
                
        except Exception as e:
            print(f"Erro ao atualizar autocompletar: {e}")


class CodeEditorCompleter:
    """Integra autocompletar com o editor de código"""
    
    def __init__(self, editor):
        self.editor = editor
        self.completer = PythonCompleter(editor)
        self.setup_completer()
    
    def setup_completer(self):
        """Configura o autocompletar no editor"""
        self.completer.setWidget(self.editor)
        self.completer.activated.connect(self.insert_completion)
        
        # Conecta eventos do editor
        self.editor.textChanged.connect(self.handle_text_change)
    
    def insert_completion(self, completion):
        """Insere a sugestão selecionada"""
        cursor = self.editor.textCursor()
        cursor.insertText(completion)
        self.editor.setTextCursor(cursor)
    
    def handle_text_change(self):
        """Manipula mudanças no texto para mostrar sugestões"""
        cursor = self.editor.textCursor()
        current_word = self.get_current_word(cursor)
        
        if len(current_word) >= 2:  # Mostra sugestões após 2 caracteres
            self.show_completions(current_word, cursor)
    
    def get_current_word(self, cursor):
        """Obtém a palavra atual do cursor"""
        line = cursor.block().text()
        position = cursor.positionInBlock()
        
        # Encontra o início da palavra atual
        start = position
        while start > 0 and (line[start-1].isalnum() or line[start-1] == '_'):
            start -= 1
        
        return line[start:position]
    
    def show_completions(self, word, cursor):
        """Mostra sugestões de autocompletar"""
        # Filtra sugestões baseadas na palavra atual
        model = self.completer.model()
        filtered_model = QStandardItemModel()
        
        for i in range(model.rowCount()):
            item = model.item(i)
            if item and word.lower() in item.text().lower():
                new_item = QStandardItem(item.text())
                filtered_model.appendRow(new_item)
        
        if filtered_model.rowCount() > 0:
            self.completer.setModel(filtered_model)
            
            # Posiciona o popup
            rect = self.editor.cursorRect()
            rect.setWidth(200)
            
            self.completer.complete(rect)
        else:
            self.completer.popup().hide()
    
    def update_package_completions(self):
        """Atualiza sugestões com pacotes instalados"""
        self.completer.update_completions()


class SnippetManager:
    """Gerencia snippets de código"""
    
    def __init__(self):
        self.snippets = {
            'for': 'for item in items:\n    pass',
            'while': 'while condition:\n    pass',
            'if': 'if condition:\n    pass',
            'def': 'def function_name():\n    pass',
            'class': 'class ClassName:\n    def __init__(self):\n        pass',
            'try': 'try:\n    pass\nexcept Exception as e:\n    pass',
            'with': 'with open("file.txt", "r") as f:\n    pass',
            'list': 'my_list = []',
            'dict': 'my_dict = {}',
            'set': 'my_set = set()',
            'tuple': 'my_tuple = ()',
            'lambda': 'lambda x: x',
            'list_comp': '[x for x in items]',
            'dict_comp': '{k: v for k, v in items}',
            'generator': '(x for x in items)',
            'main': 'if __name__ == "__main__":\n    main()',
            'import': 'import module',
            'from': 'from module import function',
            'print': 'print("Hello, World!")',
            'input': 'user_input = input("Digite algo: ")',
            'range': 'for i in range(10):\n    print(i)',
            'enumerate': 'for index, item in enumerate(items):\n    print(index, item)',
            'zip': 'for item1, item2 in zip(list1, list2):\n    print(item1, item2)',
            'map': 'result = list(map(function, items))',
            'filter': 'result = list(filter(condition, items))',
            'reduce': 'from functools import reduce\nresult = reduce(function, items)',
            'sort': 'items.sort()',
            'sorted': 'sorted_items = sorted(items)',
            'reverse': 'items.reverse()',
            'reversed': 'for item in reversed(items):\n    print(item)',
            'len': 'length = len(items)',
            'sum': 'total = sum(numbers)',
            'min': 'minimum = min(numbers)',
            'max': 'maximum = max(numbers)',
            'abs': 'absolute = abs(number)',
            'round': 'rounded = round(number, 2)',
            'str': 'string = str(object)',
            'int': 'integer = int(string)',
            'float': 'floating = float(string)',
            'bool': 'boolean = bool(value)',
            'list': 'my_list = list(iterable)',
            'tuple': 'my_tuple = tuple(iterable)',
            'dict': 'my_dict = dict(iterable)',
            'set': 'my_set = set(iterable)',
            'open': 'with open("filename.txt", "r") as file:\n    content = file.read()',
            'read': 'content = file.read()',
            'write': 'file.write("content")',
            'close': 'file.close()',
            'split': 'parts = string.split()',
            'join': 'result = " ".join(parts)',
            'strip': 'cleaned = string.strip()',
            'replace': 'new_string = string.replace("old", "new")',
            'find': 'index = string.find("substring")',
            'count': 'occurrences = string.count("substring")',
            'upper': 'uppercase = string.upper()',
            'lower': 'lowercase = string.lower()',
            'title': 'title_case = string.title()',
            'capitalize': 'capitalized = string.capitalize()',
            'startswith': 'if string.startswith("prefix"):\n    pass',
            'endswith': 'if string.endswith("suffix"):\n    pass',
            'isdigit': 'if string.isdigit():\n    pass',
            'isalpha': 'if string.isalpha():\n    pass',
            'isalnum': 'if string.isalnum():\n    pass',
            'isspace': 'if string.isspace():\n    pass',
            'append': 'my_list.append(item)',
            'extend': 'my_list.extend(items)',
            'insert': 'my_list.insert(index, item)',
            'remove': 'my_list.remove(item)',
            'pop': 'item = my_list.pop()',
            'clear': 'my_list.clear()',
            'index': 'position = my_list.index(item)',
            'count': 'occurrences = my_list.count(item)',
            'sort': 'my_list.sort()',
            'reverse': 'my_list.reverse()',
            'copy': 'new_list = my_list.copy()',
            'get': 'value = my_dict.get(key, default)',
            'setdefault': 'value = my_dict.setdefault(key, default)',
            'update': 'my_dict.update(other_dict)',
            'keys': 'keys = my_dict.keys()',
            'values': 'values = my_dict.values()',
            'items': 'for key, value in my_dict.items():\n    print(key, value)',
            'pop': 'value = my_dict.pop(key)',
            'clear': 'my_dict.clear()',
            'add': 'my_set.add(item)',
            'remove': 'my_set.remove(item)',
            'discard': 'my_set.discard(item)',
            'union': 'result = set1.union(set2)',
            'intersection': 'result = set1.intersection(set2)',
            'difference': 'result = set1.difference(set2)',
            'symmetric_difference': 'result = set1.symmetric_difference(set2)',
            'update': 'my_set.update(other_set)',
            'clear': 'my_set.clear()',
            'copy': 'new_set = my_set.copy()',
            'issubset': 'if set1.issubset(set2):\n    pass',
            'issuperset': 'if set1.issuperset(set2):\n    pass',
            'isdisjoint': 'if set1.isdisjoint(set2):\n    pass'
        }
    
    def get_snippet(self, name):
        """Retorna um snippet pelo nome"""
        return self.snippets.get(name, '')
    
    def get_all_snippets(self):
        """Retorna todos os snippets"""
        return self.snippets.copy()
    
    def add_snippet(self, name, code):
        """Adiciona um novo snippet"""
        self.snippets[name] = code
    
    def remove_snippet(self, name):
        """Remove um snippet"""
        if name in self.snippets:
            del self.snippets[name]
    
    def search_snippets(self, query):
        """Busca snippets por nome"""
        results = {}
        query_lower = query.lower()
        for name, code in self.snippets.items():
            if query_lower in name.lower():
                results[name] = code
        return results 