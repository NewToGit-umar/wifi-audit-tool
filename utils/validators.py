import re
import os

class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_mac_address(mac):
        """Validate MAC address format"""
        pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return re.match(pattern, mac) is not None
    
    @staticmethod
    def validate_ssid(ssid):
        """Validate SSID"""
        return 1 <= len(ssid) <= 32
    
    @staticmethod
    def validate_channel(channel):
        """Validate WiFi channel"""
        try:
            ch = int(channel)
            return 1 <= ch <= 165
        except:
            return False
    
    @staticmethod
    def validate_file(filepath):
        """Validate file exists and is readable"""
        return os.path.exists(filepath) and os.path.isfile(filepath)
    
    @staticmethod
    def validate_wordlist(filepath):
        """Validate wordlist file"""
        if not Validators.validate_file(filepath):
            return False
        try:
            with open(filepath, 'r', errors='ignore') as f:
                return f.read(1) != ''
        except:
            return False
