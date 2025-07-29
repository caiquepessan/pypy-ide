#!/usr/bin/env python3
"""
PyPy IDE - Um editor de código Python simples e elegante
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.main_window import IDEMainWindow


def main():
    """Função principal da aplicação"""
    app = QApplication(sys.argv)
    window = IDEMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
