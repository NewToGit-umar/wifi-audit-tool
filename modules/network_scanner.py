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
        """Improved Linux scan with robust parsing + iwlist fallback."""
        networks = []
        try:
            # Try nmcli first
            result = subprocess.run(
                ["nmcli", "-f", "BSSID,SSID,CHAN,SIGNAL,SECURITY", "dev", "wifi", "--terse"],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0:
                output = result.stdout
                for line in output.strip().split('\n'):
                    if not line or line.startswith('BSSID'): continue
                    # Robust extraction with regex
                    bssid_match = re.search(r'([0-9A-Fa-f]{2}(?::[0-9A-Fa-f]{2}){5})', line)
                    bssid = bssid_match.group(1) if bssid_match else "N/A"
                    
                    ch_match = re.search(r'CHAN:(\d+)', line) or re.search(r':(\d+):', line)
                    ch = ch_match.group(1) if ch_match else "N/A"
                    
                    signal_match = re.search(r'SIGNAL:(\d+)', line)
                    pwr = signal_match.group(1) if signal_match else "N/A"
                    
                    ssid_match = re.search(r'SSID:([^:]+?)(?=:SECURITY:|$|:\d+)', line)
                    ssid = ssid_match.group(1).strip() if ssid_match else "<Hidden>"
                    
                    networks.append({
                        "ssid": ssid or "<Hidden>",
                        "bssid": bssid,
                        "enc": "WPA/WPA2",  # simplified
                        "pwr": pwr,
                        "ch": ch
                    })
        except Exception:
            pass

        if not networks or all(n.get("ch") == "N/A" for n in networks):
            # Fallback to iwlist (excellent for channels)
            networks = NetworkScanner._scan_with_iwlist()

        return networks or [{"ssid": "No networks (run as root / check adapter)", "bssid": "N/A", "enc": "N/A", "pwr": "N/A", "ch": "N/A"}]

    @staticmethod
    def _scan_with_iwlist():
        """Fallback using iwlist for reliable channel detection."""
        try:
            interfaces = NetworkScanner.get_interfaces()
            iface = next((i for i in interfaces if 'wlan' in i or 'wifi' in i), interfaces[0] if interfaces else "wlan0")
            
            result = subprocess.run(["iwlist", iface, "scan"], 
                                  capture_output=True, text=True, timeout=15)
            output = result.stdout
        except Exception:
            return [{"ssid": "iwlist failed (need root/monitor mode?)", "bssid": "N/A", "enc": "N/A", "pwr": "N/A", "ch": "N/A"}]

        networks = []
        current = {}
        for line in output.splitlines():
            line = line.strip()
            if "Cell " in line and current:
                networks.append(current)
                current = {}
            if "Address:" in line:
                current["bssid"] = line.split("Address: ")[-1]
            if "ESSID:" in line:
                current["ssid"] = line.split("ESSID:")[-1].strip('"')
            if "Channel:" in line:
                ch_m = re.search(r'Channel:(\d+)', line)
                current["ch"] = ch_m.group(1) if ch_m else "N/A"
            if "Signal level" in line or "Quality" in line:
                sig_m = re.search(r'Signal level=([-\d]+)', line) or re.search(r'Quality=(\d+)', line)
                current["pwr"] = sig_m.group(1) if sig_m else "N/A"
            if "Encryption key:" in line:
                current["enc"] = "WPA/WPA2" if "on" in line else "Open"
        if current:
            networks.append(current)
        return networks
