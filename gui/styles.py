# Theme and styling constants

DARK_THEME = {
    'primary': '#00ff00',
    'secondary': '#003300',
    'bg': '#000000',
    'bg_alt': '#0a0a0a',
    'text': '#00ff00',
    'error': '#ff0000',
    'success': '#00ff00',
}

STYLE_SHEET = """
    QMainWindow, QWidget {
        background-color: #0a0a0a;
        color: #00ff00;
    }
    QGroupBox {
        border: 1px solid #00ff00;
        border-radius: 5px;
        margin-top: 10px;
        padding-top: 10px;
        color: #00ff00;
    }
    QPushButton {
        background-color: #001100;
        color: #00ff00;
        border: 1px solid #00ff00;
        padding: 5px;
        border-radius: 3px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: #003300;
    }
    QPushButton:pressed {
        background-color: #00ff00;
        color: #000000;
    }
    QTableWidget, QTableWidget::item {
        background-color: #000500;
        color: #00ff00;
        border: none;
        gridline-color: #003300;
    }
    QHeaderView::section {
        background-color: #001100;
        color: #00ff00;
        border: 1px solid #00ff00;
        padding: 3px;
    }
    QTextEdit {
        background-color: #000500;
        color: #00ff00;
        border: 1px solid #003300;
    }
    QLineEdit, QComboBox {
        background-color: #000500;
        color: #00ff00;
        border: 1px solid #003300;
        padding: 3px;
    }
"""
