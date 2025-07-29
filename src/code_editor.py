from PyQt5.QtWidgets import QPlainTextEdit, QWidget, QTextEdit
from PyQt5.QtGui import QFont, QColor, QPainter, QTextCharFormat, QPen, QBrush
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
        self.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {DRACULA_COLORS['background']}; 
                color: {DRACULA_COLORS['foreground']};
                border: none;
                padding: 8px;
                line-height: 1.4;
                selection-background-color: {DRACULA_COLORS['selection']};
                selection-color: {DRACULA_COLORS['foreground']};
            }}
            QPlainTextEdit:focus {{
                border: 1px solid {DRACULA_COLORS['function']};
                border-radius: 4px;
            }}
        """)
        
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
        space = 8 + self.fontMetrics().horizontalAdvance('9') * digits
        return max(space, 50)  # Mínimo de 50px

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
            lineColor.setAlpha(80)  # Mais transparente

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
                
                # Cor do número da linha
                if blockNumber + 1 in self.breakpoints:
                    painter.setPen(QPen(QColor(DRACULA_COLORS['error']), 1))
                    painter.setBrush(QBrush(QColor(DRACULA_COLORS['error'])))
                    # Desenha círculo do breakpoint
                    painter.drawEllipse(QRect(2, top + 2, 8, 8))
                else:
                    painter.setPen(QColor(DRACULA_COLORS['line_number_fg']))
                
                # Desenha o número da linha
                painter.drawText(QRect(0, top, self.lineNumberArea.width() - 4, self.fontMetrics().height()),
                               Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + int(self.blockBoundingRect(block).height())
            blockNumber += 1

    def mousePressEvent(self, event):
        """Manipula cliques do mouse na área de numeração"""
        if event.button() == Qt.LeftButton:
            # Calcula a linha clicada
            block = self.firstVisibleBlock()
            blockNumber = block.blockNumber()
            top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
            bottom = top + int(self.blockBoundingRect(block).height())
            
            while block.isValid():
                if event.y() >= top and event.y() <= bottom:
                    self.toggleBreakpoint(blockNumber + 1)
                    break
                block = block.next()
                top = bottom
                bottom = top + int(self.blockBoundingRect(block).height())
                blockNumber += 1
        
        super().mousePressEvent(event) 