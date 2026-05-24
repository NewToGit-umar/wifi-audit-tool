import subprocess
import os

class InterfaceManager:
    """Manage network interface configuration"""
    
    @staticmethod
    def get_interfaces():
        """Get all network interfaces"""
        try:
            result = subprocess.run(["ip", "link", "show"], capture_output=True, text=True)
            interfaces = []
            for line in result.stdout.split('\n'):
                if ':' in line and not line.startswith(' '):
                    iface = line.split(':')[1].strip()
                    if iface and not iface.startswith('lo'):
                        interfaces.append(iface)
            return interfaces
        except:
            return []
    
    @staticmethod
    def enable_monitor_mode(interface):
        """Enable monitor mode on interface"""
        try:
            subprocess.run(["ip", "link", "set", interface, "down"], check=True)
            subprocess.run(["iwconfig", interface, "mode", "Monitor"], check=True)
            subprocess.run(["ip", "link", "set", interface, "up"], check=True)
            return True
        except:
            return False
    
    @staticmethod
    def disable_monitor_mode(interface):
        """Disable monitor mode on interface"""
        try:
            subprocess.run(["ip", "link", "set", interface, "down"], check=True)
            subprocess.run(["iwconfig", interface, "mode", "Managed"], check=True)
            subprocess.run(["ip", "link", "set", interface, "up"], check=True)
            return True
        except:
            return False
