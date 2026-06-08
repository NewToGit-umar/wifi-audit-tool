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
        """Enable monitor mode on interface using nmcli + iw"""
        try:
            # Tell NetworkManager to stop managing this interface
            subprocess.run(["nmcli", "device", "set", interface, "managed", "no"], 
                         check=True, stderr=subprocess.DEVNULL)
            
            # Bring interface down
            subprocess.run(["ip", "link", "set", interface, "down"], check=True)
            
            # Set monitor mode using modern iw command
            subprocess.run(["iw", interface, "set", "monitor"], check=True)
            
            # Bring interface back up
            subprocess.run(["ip", "link", "set", interface, "up"], check=True)
            
            return True
        except Exception as e:
            print(f"[!] Failed to enable monitor mode: {e}")
            return False
    
    @staticmethod
    def disable_monitor_mode(interface):
        """Disable monitor mode on interface"""
        try:
            subprocess.run(["ip", "link", "set", interface, "down"], check=True)
            subprocess.run(["iw", interface, "set", "managed"], check=True)
            subprocess.run(["ip", "link", "set", interface, "up"], check=True)
            
            # Give control back to NetworkManager
            subprocess.run(["nmcli", "device", "set", interface, "managed", "yes"], 
                         check=True, stderr=subprocess.DEVNULL)
            
            return True
        except Exception as e:
            print(f"[!] Failed to disable monitor mode: {e}")
            return False
