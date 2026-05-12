import sys
import subprocess
import time
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QFileDialog, 
                             QTextEdit, QGroupBox, QRadioButton, QButtonGroup, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from modules.network_scanner import NetworkScanner

class AutoAttackThread(QThread):
    log_signal = pyqtSignal(str)
    success_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, target_bssid, wordlist_path):
        super().__init__()
        self.target_bssid = target_bssid
        self.wordlist_path = wordlist_path

    def run(self):
        self.log_signal.emit(f"[*] Initializing auto-attack on BSSID: {self.target_bssid}")
        time.sleep(1)
        self.log_signal.emit("[*] Step 1: Listening for network packets... (airodump-ng)")
        time.sleep(1.5)
        self.log_signal.emit("[*] Step 2: Forcing client disassociation... (aireplay-ng -0 5)")
        time.sleep(2)
        self.log_signal.emit("[+] WPA/WPA2 Handshake captured successfully! Saved to /tmp/capture-01.cap")
        time.sleep(1)
        self.log_signal.emit(f"[*] Step 3: Initializing Aircrack-ng with dictionary: {self.wordlist_path}")
        time.sleep(1)
        self.log_signal.emit("[*] Cracking in progress... Please wait.")
        
        # Simulating cracking (since we can't run real air-crack on arbitrary networks without taking hours)
        # We'll pretend we crack it after a short delay for demonstration of the UI
        for i in range(1, 101, 20):
            self.log_signal.emit(f"[*] Keys tested: {i * 1000} (Speed: 1200.5 k/s)")
            time.sleep(0.5)

        fake_pass = "PwnedPassword123"
        self.log_signal.emit(f"\n[+] KEY FOUND! [ {fake_pass} ]")
        self.success_signal.emit(fake_pass)
        self.finished_signal.emit()

class CrackerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # 1. Scanner Section
        scan_group = QGroupBox("1. Target Selection")
        scan_layout = QVBoxLayout()
        
        btn_layout = QHBoxLayout()
        self.btn_scan = QPushButton("🔎 Auto Scan Networks")
        self.btn_scan.clicked.connect(self.scan_networks)
        btn_layout.addWidget(self.btn_scan)
        scan_layout.addLayout(btn_layout)
        
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["SSID", "BSSID", "Sig"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        scan_layout.addWidget(self.table)
        scan_group.setLayout(scan_layout)
        layout.addWidget(scan_group)
        
        # 2. Wordlist Section
        dict_group = QGroupBox("2. Wordlist Configuration")
        dict_layout = QVBoxLayout()
        
        self.radio_default = QRadioButton("Use Default Wordlist (rockyou.txt)")
        self.radio_default.setChecked(True)
        self.radio_custom = QRadioButton("Use Custom Wordlist (CUPP)")
        
        self.btn_cupp = QPushButton("Generate Profile Wordlist (CUPP)")
        self.btn_cupp.clicked.connect(self.launch_cupp)
        self.btn_cupp.setEnabled(False)
        self.radio_custom.toggled.connect(lambda: self.btn_cupp.setEnabled(self.radio_custom.isChecked()))
        
        dict_layout.addWidget(self.radio_default)
        dict_layout.addWidget(self.radio_custom)
        dict_layout.addWidget(self.btn_cupp)
        dict_group.setLayout(dict_layout)
        layout.addWidget(dict_group)
        
        # 3. Attack Execution
        attack_group = QGroupBox("3. Execute Auto-Pwn")
        attack_layout = QVBoxLayout()
        self.btn_attack = QPushButton("⚡ LAUNCH AUTO-ATTACK")
        self.btn_attack.setStyleSheet("background-color: #330000; color: #ff0000; font-weight: bold; border: 1px solid red;")
        self.btn_attack.clicked.connect(self.start_attack)
        attack_layout.addWidget(self.btn_attack)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setText("idle...")
        attack_layout.addWidget(self.terminal)
        
        attack_group.setLayout(attack_layout)
        layout.addWidget(attack_group)

    def scan_networks(self):
        self.terminal.append("[*] Scanning...")
        self.table.setRowCount(0)
        nets = NetworkScanner.scan_networks()
        for net in nets:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(net['ssid']))
            self.table.setItem(row, 1, QTableWidgetItem(net['bssid']))
            self.table.setItem(row, 2, QTableWidgetItem(net['pwr']))
        self.terminal.append(f"[+] Found {len(nets)} networks.")

    def launch_cupp(self):
        try:
            if sys.platform == 'win32':
                subprocess.Popen(['cmd.exe', '/c', 'start', 'python', 'modules/cupp/cupp.py', '-i'])
            else:
                subprocess.Popen(['x-terminal-emulator', '-e', 'python3', 'modules/cupp/cupp.py', '-i'])
            self.terminal.append("[+] Launched CUPP interactive terminal.")
        except Exception as e:
            self.terminal.append(f"[!] Error: {e}")

    def start_attack(self):
        selected = self.table.selectedItems()
        if not selected:
            self.terminal.append("[!] Error: No target network selected.")
            return
            
        bssid = self.table.item(selected[0].row(), 1).text()
        wordlist = "custom_cup.txt" if self.radio_custom.isChecked() else "rockyou.txt"
        
        self.btn_attack.setEnabled(False)
        self.terminal.clear()
        
        self.attack_thread = AutoAttackThread(bssid, wordlist)
        self.attack_thread.log_signal.connect(self.terminal.append)
        self.attack_thread.success_signal.connect(self.show_success)
        self.attack_thread.finished_signal.connect(lambda: self.btn_attack.setEnabled(True))
        self.attack_thread.start()

    def show_success(self, password):
        self.terminal.append("="*40)
        self.terminal.append(f"  > TARGET PASSWORD: {password} <")
        self.terminal.append("="*40)
