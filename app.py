import sys
import os

# CRITICAL FIX: Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui.main_window import MainWindow

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Hacker Theme Styling (your original)
    hacker_style = """
        * {
            background-color: #000000;
            color: #00ff00;
            font-family: inherit;
        }
        QMainWindow, QWidget {
            background-color: #0a0a0a;
        }
        QFrame {
            border: 1px solid #00ff00;
            border-radius: 2px;
        }
        QPushButton {
            background-color: #001100;
            color: #00ff00;
            border: 1px solid #00ff00;
            padding: 4px 8px;
            font-size: 10px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #003300;
        }
        QPushButton:pressed {
            background-color: #00ff00;
            color: #000000;
        }
        QLabel {
            border: none;
            font-size: 10px;
            color: #00ff00;
        }
        QListWidget, QTableWidget, QTreeWidget, QTextEdit, QComboBox, QLineEdit {
            background-color: #000500;
            color: #00ff00;
            border: 1px solid #003300;
            selection-background-color: #00ff00;
            selection-color: #000000;
            font-size: 10px;
        }
        QHeaderView::section {
            background-color: #001100;
            color: #00ff00;
            border: 1px solid #003300;
        }
    """
    app.setStyleSheet(hacker_style)
    
    # Set default monospace font
    font = app.font()
    font.setFamily("Consolas")
    font.setPointSize(9)
    app.setFont(font)
        
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()