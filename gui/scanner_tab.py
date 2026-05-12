from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
from modules.network_scanner import NetworkScanner

class ScannerThread(QThread):
    networks_found = pyqtSignal(list)
    
    def run(self):
        networks = NetworkScanner.scan_networks()
        self.networks_found.emit(networks)

class ScannerTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)
        
        header_label = QLabel("Network Discovery & Scanning")
        header_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        layout.addWidget(header_label)
        
        guide_label = QLabel("Step 1: Select your wireless interface (must support monitor mode) and click 'Start Scan' to discover nearby APs.")
        guide_label.setFont(QFont("Segoe UI", 12))
        guide_label.setStyleSheet("color: #a0a0a0; margin-bottom: 10px;")
        guide_label.setWordWrap(True)
        layout.addWidget(guide_label)
        
        controls_layout = QHBoxLayout()
        
        self.btn_start = QPushButton("▶ Start Scan")
        self.btn_start.setFixedWidth(160)
        self.btn_start.setFixedHeight(45)
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; font-size: 14px; border-radius: 6px;")
        self.btn_start.clicked.connect(self.start_scan)
        
        self.btn_clear = QPushButton("⏹ Clear Results")
        self.btn_clear.setFixedWidth(160)
        self.btn_clear.setFixedHeight(45)
        self.btn_clear.setCursor(Qt.PointingHandCursor)
        self.btn_clear.setStyleSheet("background-color: #f44336; color: white; font-weight: bold; font-size: 14px; border-radius: 6px;")
        self.btn_clear.clicked.connect(self.clear_results)
        
        controls_layout.addWidget(self.btn_start)
        controls_layout.addWidget(self.btn_clear)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["BSSID", "PWR", "Beacons", "CH", "ENC", "ESSID"])
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget { background-color: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 6px; font-size: 13px; }
            QHeaderView::section { background-color: #2b2b2b; padding: 8px; border: 1px solid #3d3d3d; font-size: 13px; font-weight: bold; }
            QTableWidget::item:selected { background-color: #4CAF50; }
        """)
        layout.addWidget(self.table)
        
        self.scanner_thread = ScannerThread()
        self.scanner_thread.networks_found.connect(self.update_table)

    def start_scan(self):
        self.btn_start.setEnabled(False)
        self.btn_start.setText("Scanning...")
        self.clear_results()
        self.scanner_thread.start()
        
    def update_table(self, networks):
        self.table.setRowCount(len(networks))
        for row, net in enumerate(networks):
            self.table.setItem(row, 0, QTableWidgetItem(net.get("bssid", "N/A")))
            self.table.setItem(row, 1, QTableWidgetItem(net.get("pwr", "N/A")))
            self.table.setItem(row, 2, QTableWidgetItem("~"))
            self.table.setItem(row, 3, QTableWidgetItem(net.get("ch", "N/A")))
            self.table.setItem(row, 4, QTableWidgetItem(net.get("enc", "N/A")))
            self.table.setItem(row, 5, QTableWidgetItem(net.get("ssid", "N/A")))
        self.btn_start.setEnabled(True)
        self.btn_start.setText("▶ Start Scan")
        
    def clear_results(self):
        self.table.setRowCount(0)
