import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class AuditLogger:
    def __init__(self):
        self.log_dir = "logs"
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup main logger
        self.logger = logging.getLogger('WifiAudit')
        self.logger.setLevel(logging.INFO)
        
        # File handler with rotation
        log_file = os.path.join(self.log_dir, 'audit_log.txt')
        handler = RotatingFileHandler(log_file, maxBytes=10*1024*1024, backupCount=5)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Also log errors separately
        error_file = os.path.join(self.log_dir, 'error_log.txt')
        error_handler = RotatingFileHandler(error_file, maxBytes=5*1024*1024, backupCount=3)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)
    
    def log_scan(self, networks):
        """Log scan results"""
        self.logger.info(f"Scan completed: Found {len(networks)} networks")
        
    def log_capture(self, bssid, essid):
        """Log handshake capture"""
        self.logger.info(f"Handshake captured - BSSID: {bssid}, ESSID: {essid}")
    
    def log_crack(self, bssid, success, password=None):
        """Log cracking attempt"""
        if success:
            self.logger.warning(f"Password cracked for {bssid}: {password}")
        else:
            self.logger.info(f"Failed to crack password for {bssid}")