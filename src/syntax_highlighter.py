from PyQt5.QtGui import QTextCharFormat, QColor, QSyntaxHighlighter
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token
from .constants import DRACULA_COLORS


class PythonHighlighter(QSyntaxHighlighter):
    """Syntax highlighter para código Python com tema Dracula"""
    
    def __init__(self, document):
        super().__init__(document)
        self.lexer = PythonLexer()
        self.formats = {
            Token.Keyword: QTextCharFormat(),
            Token.Name.Function: QTextCharFormat(),
            Token.Name.Variable: QTextCharFormat(),
            Token.Name.Class: QTextCharFormat(),
            Token.Name: QTextCharFormat(),
            Token.Comment: QTextCharFormat(),
            Token.String: QTextCharFormat(),
            Token.Error: QTextCharFormat(),
            Token.Number: QTextCharFormat(),
            Token.Operator: QTextCharFormat()
        }

        # Definir cores estilo Dracula Theme
        self.formats[Token.Keyword].setForeground(QColor(DRACULA_COLORS['keyword']))
        self.formats[Token.Name.Function].setForeground(QColor(DRACULA_COLORS['function']))
        self.formats[Token.Name.Variable].setForeground(QColor(DRACULA_COLORS['variable']))
        self.formats[Token.Name.Class].setForeground(QColor(DRACULA_COLORS['class']))
        self.formats[Token.Name].setForeground(QColor(DRACULA_COLORS['identifier']))
        self.formats[Token.Comment].setForeground(QColor(DRACULA_COLORS['comment']))
        self.formats[Token.String].setForeground(QColor(DRACULA_COLORS['string']))
        self.formats[Token.Error].setForeground(QColor(DRACULA_COLORS['error']))
        self.formats[Token.Number].setForeground(QColor(DRACULA_COLORS['number']))
        self.formats[Token.Operator].setForeground(QColor(DRACULA_COLORS['operator']))

    def highlightBlock(self, text):
        """Aplica highlighting ao bloco de texto"""
        for token, content in lex(text, self.lexer):
            length = len(content)
            if token in self.formats:
                self.setFormat(text.find(content), length, self.formats[token]) 