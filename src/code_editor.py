from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt5.QtGui import QFont, QColor, QPainter, QTextCharFormat
from PyQt5.QtCore import Qt, QRect, QSize
from .constants import DRACULA_COLORS, EDITOR_CONFIG


class LineNumberArea(QWidget):
    """Área de numeração de linhas do editor"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class CodeEditor(QPlainTextEdit):
    """Editor de código com numeração de linhas e breakpoints"""
    
    def __init__(self):
        super().__init__()
        self.setFont(QFont(EDITOR_CONFIG['font_family'], EDITOR_CONFIG['font_size']))
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * EDITOR_CONFIG['tab_width'])
        self.setStyleSheet(f"background-color: {DRACULA_COLORS['background']}; color: {DRACULA_COLORS['foreground']};")
        
        self.lineNumberArea = LineNumberArea(self)
        self.breakpoints = set()  # Para armazenar os breakpoints

        # Conectar sinais
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        """Calcula a largura da área de numeração de linhas"""
        digits = len(str(self.blockCount()))
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        """Atualiza a largura da área de numeração"""
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        """Atualiza a área de numeração de linhas"""
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        """Redimensiona a área de numeração quando o editor é redimensionado"""
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        """Destaca a linha atual"""
        extraSelections = []

        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(DRACULA_COLORS['line_highlight'])

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextCharFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def toggleBreakpoint(self, block_number):
        """Alternar breakpoint na linha especificada"""
        if block_number in self.breakpoints:
            self.breakpoints.remove(block_number)
        else:
            self.breakpoints.add(block_number)
        self.viewport().update()

    def lineNumberAreaPaintEvent(self, event):
        """Pinta a área de numeração de linhas"""
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), QColor(DRACULA_COLORS['line_number_bg']))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + int(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(QColor(DRACULA_COLORS['line_number_fg']))
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignRight, number)

                # Desenhar breakpoints
                if blockNumber in self.breakpoints:
                    painter.setBrush(QColor(DRACULA_COLORS['breakpoint']))
                    radius = 5
                    painter.drawEllipse(self.lineNumberArea.width() - radius - 4, top + 2, radius * 2, radius * 2)

            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def mousePressEvent(self, event):
        """Detecta cliques na área de número de linha para definir breakpoints"""
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            if x < self.lineNumberAreaWidth():  # Se clicar na área de número de linha
                block = self.firstVisibleBlock()
                top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
                block_number = block.blockNumber()
                while block.isValid():
                    bottom = top + int(self.blockBoundingRect(block).height())
                    if top <= event.pos().y() <= bottom:
                        self.toggleBreakpoint(block_number)
                        break
                    block = block.next()
                    top = bottom
                    block_number += 1
        super().mousePressEvent(event) 