from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer, pyqtSignal

class StatusBar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.status_label = QLabel("Ready")
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress)
        self.setLayout(layout)
    
    def set_status(self, text):
        self.status_label.setText(text)
    
    def show_progress(self, value):
        self.progress.setValue(value)
        self.progress.setVisible(True)
    
    def hide_progress(self):
        self.progress.setVisible(False)

class TerminalOutput(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.label = QLabel("Terminal Output")
        layout.addWidget(self.label)
        self.setLayout(layout)
