import subprocess

class PacketInjection:
    """Packet Injection for WiFi attacks"""
    
    def __init__(self, interface):
        self.interface = interface
    
    def check_injection(self):
        """Test packet injection capability"""
        try:
            cmd = ["aireplay-ng", "--test", self.interface]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            return "Injection is working" in result.stdout
        except:
            return False
    
    def send_beacon(self, ssid, bssid, channel):
        """Send beacon frames"""
        try:
            cmd = ["mdk3", self.interface, "b", "-n", ssid, "-c", str(channel)]
            subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except:
            return False
    
    def send_custom_packet(self, packet_data):
        """Send custom crafted packet"""
        try:
            from scapy.all import send
            send(packet_data, iface=self.interface)
            return True
        except:
            return False
