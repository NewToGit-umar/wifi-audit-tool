import subprocess
import re
import sys

class NetworkScanner:
    @staticmethod
    def get_interfaces():
        """Get available network interfaces."""
        try:
            result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True, check=True)
            interfaces = []
            for line in result.stdout.split('\n'):
                if ':' in line and not line.startswith(' '):
                    iface = line.split(':')[1].strip()
                    if iface and not iface.startswith('lo'):
                        interfaces.append(iface)
            return interfaces
        except (FileNotFoundError, subprocess.CalledProcessError):
            return []

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
            # Try airodump-ng first (more reliable for auditing)
            try:
                subprocess.run(["airodump-ng", "--output-format", "csv", "-w", "/tmp/scan_temp", 
                              "--write-interval", "1", "--run-time", "6", "wlan0"], 
                             timeout=8, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except:
                pass

            # Fallback to nmcli
            result = subprocess.run(["nmcli", "-t", "-f", "BSSID,SIGNAL,SECURITY,SSID,CHAN", 
                                   "dev", "wifi"], 
                                  capture_output=True, text=True, timeout=8)
            output = result.stdout
        except:
            return [{"ssid": "Scan failed - run as root", "bssid": "N/A", "enc": "N/A", "pwr": "N/A", "ch": "N/A"}]

        networks = []
        for line in output.split('\n'):
            if not line.strip(): 
                continue
            parts = line.split(':')
            if len(parts) >= 4:
                try:
                    bssid = ":".join(parts[:6])
                    signal = parts[6] if len(parts) > 6 else "N/A"
                    security = parts[7] if len(parts) > 7 else "WPA2"
                    ssid = ":".join(parts[8:]) if len(parts) > 8 else "<Hidden>"
                    ch = "N/A"
                    networks.append({
                        "ssid": ssid,
                        "bssid": bssid,
                        "enc": security,
                        "pwr": signal,
                        "ch": ch
                    })
                except:
                    continue
        return networks[:20]  # Limit results
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
