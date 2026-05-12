import subprocess
import re
import sys

class NetworkScanner:
    @staticmethod
    def scan_networks():
        """Scans for WiFi networks cross-platform."""
        if sys.platform == 'win32':
            return NetworkScanner._scan_windows()
        else:
            return NetworkScanner._scan_linux()

    @staticmethod
    def _scan_linux():
        try:
            # nmcli -t -f BSSID,FREQ,SIGNAL,SECURITY,SSID dev wifi
            result = subprocess.run(["nmcli", "-t", "-f", "BSSID,SIGNAL,SECURITY,SSID,CHAN", "dev", "wifi"], 
                                    capture_output=True, text=True, check=True)
            output = result.stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            return [{"ssid": "Error (Need nmcli)", "bssid": "N/A", "enc": "N/A", "pwr": "N/A", "ch": "N/A"}]

        networks = []
        for line in output.split('\n'):
            if not line.strip(): continue
            parts = line.split(':')
            if len(parts) >= 8: # nmcli escapes colons in MAC addresses, splitting gives more parts
                # Reconstruct MAC
                bssid = ":".join(parts[0:6])
                pwr = parts[6]
                enc = parts[7]
                ssid = parts[8] if len(parts) > 8 else "<Hidden>"
                ch = parts[9] if len(parts) > 9 else "0"
                networks.append({"ssid": ssid, "bssid": bssid, "enc": enc, "pwr": pwr, "ch": ch})
        return networks

    @staticmethod
    def _scan_windows():
        try:
            # Run the netsh command to get detailed BSSID info
            result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], 
                                    capture_output=True, text=True, check=True)
            output = result.stdout
        except (FileNotFoundError, subprocess.CalledProcessError):
            return [{"ssid": "Error", "bssid": "N/A", "enc": "N/A", "pwr": "N/A", "ch": "N/A"}]

        networks = []
        current_ssid = ""
        current_enc = ""

        # Parse the output line by line
        for line in output.split('\n'):
            line = line.strip()
            
            if line.startswith("SSID"):
                match = re.match(r"SSID\s+\d+\s+:\s*(.*)", line)
                if match:
                    current_ssid = match.group(1).strip()
                    if not current_ssid:
                        current_ssid = "<Hidden SSID>"
            
            elif line.startswith("Authentication"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_enc = parts[1].strip()
                    
            elif line.startswith("Encryption"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    current_enc += f" / {parts[1].strip()}"
                    
            elif line.startswith("BSSID"):
                parts = line.split(":", 1)
                if len(parts) > 1:
                    bssid = parts[1].strip()
                    networks.append({
                        "ssid": current_ssid,
                        "bssid": bssid,
                        "enc": current_enc,
                        "pwr": "N/A",
                        "ch": "N/A"
                    })
                    
            elif line.startswith("Signal"):
                if networks: # Apply to the most recently added BSSID
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        networks[-1]["pwr"] = parts[1].strip()
                        
            elif line.startswith("Channel"):
                if networks:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        networks[-1]["ch"] = parts[1].strip()

        return networks
