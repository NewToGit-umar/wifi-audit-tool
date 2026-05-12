from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from gui.cracker_tab import CrackerTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto-Hack Tool [ROOT]")
        self.setMinimumSize(700, 450)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)
        
        self.setup_sidebar()
        self.setup_content_area()
        
    def setup_sidebar(self):
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setFixedWidth(140)
        
        self.sidebar_layout = QVBoxLayout(self.sidebar_frame)
        self.sidebar_layout.setContentsMargins(5, 10, 5, 10)
        
        self.title_label = QLabel("W1F1_Pwn\n[Active]")
        self.title_label.setFont(QFont("Consolas", 12, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: #00ff00;")
        self.sidebar_layout.addWidget(self.title_label)
        
        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar_frame)

    def setup_content_area(self):
        self.content_stack = QStackedWidget()
        self.content_stack.addWidget(CrackerTab())
        self.main_layout.addWidget(self.content_stack)
