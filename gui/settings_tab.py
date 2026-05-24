from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QCheckBox, QSpinBox, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # General Settings
        general_group = QGroupBox("General Settings")
        general_layout = QVBoxLayout()
        
        self.verbose = QCheckBox("Verbose Output")
        self.verbose.setChecked(True)
        general_layout.addWidget(self.verbose)
        
        timeout_layout = QHBoxLayout()
        timeout_layout.addWidget(QLabel("Capture Timeout (seconds):"))
        self.timeout = QSpinBox()
        self.timeout.setValue(30)
        self.timeout.setRange(10, 300)
        timeout_layout.addWidget(self.timeout)
        general_layout.addLayout(timeout_layout)
        
        deauth_layout = QHBoxLayout()
        deauth_layout.addWidget(QLabel("Deauth Count:"))
        self.deauth_count = QSpinBox()
        self.deauth_count.setValue(20)
        self.deauth_count.setRange(1, 100)
        deauth_layout.addWidget(self.deauth_count)
        general_layout.addLayout(deauth_layout)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Output Settings
        output_group = QGroupBox("Output Settings")
        output_layout = QVBoxLayout()
        
        self.save_captures = QCheckBox("Save Captures to File")
        self.save_captures.setChecked(True)
        output_layout.addWidget(self.save_captures)
        
        self.auto_crack = QCheckBox("Auto-start Cracking")
        self.auto_crack.setChecked(False)
        output_layout.addWidget(self.auto_crack)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("Save Settings")
        btn_reset = QPushButton("Reset to Default")
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_reset)
        layout.addLayout(btn_layout)
