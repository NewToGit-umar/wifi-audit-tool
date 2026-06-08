import subprocess
import re
import sys
import os

class NetworkScanner:
    @staticmethod
    def get_interfaces():
        """Get wireless interfaces."""
        try:
            # Prefer wireless interfaces
            result = subprocess.run(["iwconfig"], capture_output=True, text=True, timeout=10)
            interfaces = []
            for line in result.stdout.splitlines():
                if "no wireless extensions" not in line and ":" in line:
                    iface = line.split()[0].strip()
                    if iface:
                        interfaces.append(iface)
            if not interfaces:
                # fallback
                result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
                for line in result.stdout.split('\n'):
                    if ':' in line and not line.startswith(' '):
                        iface = line.split(':')[1].strip().split()[0]
                        if iface and not iface.startswith(('lo', 'eth', 'enp')):
                            interfaces.append(iface)
            return interfaces or ["wlan0"]
        except:
            return ["wlan0"]

    @staticmethod
    def scan_networks():
        if sys.platform == 'win32':
            return NetworkScanner._scan_windows()
        return NetworkScanner._scan_linux()

    @staticmethod
    def _scan_linux():
        networks = []
        try:
            # Primary: Try nmcli (works without monitor mode)
            result = subprocess.run(
                ["nmcli", "-t", "-f", "SSID,BSSID,CHAN,SIGNAL", "dev", "wifi"],
                capture_output=True, text=True, timeout=12, check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                for line in result.stdout.strip().split('\n'):
                    if not line or "SSID" in line: continue
                    parts = line.split(':', 3)
                    if len(parts) >= 3:
                        ssid = parts[0] if parts[0] else "<Hidden>"
                        bssid = parts[1]
                        ch = parts[2]
                        pwr = parts[3] if len(parts) > 3 else "N/A"
                        networks.append({
                            "ssid": ssid,
                            "bssid": bssid,
                            "ch": ch,
                            "pwr": pwr,
                            "enc": "WPA/WPA2"
                        })
        except:
            pass

        if not networks:
            networks = NetworkScanner._scan_with_iwlist()

        if not networks:
            networks = [{"ssid": "No networks (run as root / check adapter)", "bssid": "N/A", "ch": "N/A", "pwr": "N/A", "enc": "N/A"}]

        return networks

    @staticmethod
    def _scan_with_iwlist():
        """Improved iwlist fallback with sudo attempt"""
        try:
            interfaces = NetworkScanner.get_interfaces()
            iface = next((i for i in interfaces if 'wlan' in i.lower()), interfaces[0])

            # Try with sudo first
            cmd = ["sudo", "iwlist", iface, "scan"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            
            if result.returncode != 0:
                # Try without sudo (may fail)
                result = subprocess.run(["iwlist", iface, "scan"], capture_output=True, text=True, timeout=15)

            output = result.stdout
            if not output.strip():
                return []

            # Better parsing
            networks = []
            current = {}
            for line in output.splitlines():
                line = line.strip()
                if "Cell" in line and current:
                    if current.get("ssid"):
                        networks.append(current)
                    current = {}
                if "Address:" in line:
                    current["bssid"] = line.split("Address: ")[-1].strip()
                if "ESSID:" in line:
                    current["ssid"] = line.split("ESSID:")[-1].strip('"')
                if "Channel:" in line:
                    m = re.search(r'Channel:(\d+)', line)
                    current["ch"] = m.group(1) if m else "N/A"
                if "Signal" in line or "Quality" in line:
                    m = re.search(r'Signal level=([-\d]+)', line) or re.search(r'Quality=(\d+)', line)
                    current["pwr"] = m.group(1) if m else "N/A"
            if current.get("ssid"):
                networks.append(current)
            return networks
        except Exception as e:
            print(f"[!] iwlist scan failed: {e}")
            return []