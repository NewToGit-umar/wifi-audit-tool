import subprocess
import os
import sys

class SystemChecker:
    """Check system requirements and tools"""
    
    REQUIRED_TOOLS = [
        'aircrack-ng',
        'airodump-ng',
        'aireplay-ng',
        'nmcli',
        'ip',
        'iwconfig'
    ]
    
    @staticmethod
    def check_root():
        """Check if running as root"""
        return os.geteuid() == 0 if hasattr(os, 'geteuid') else False
    
    @staticmethod
    def check_tool(tool):
        """Check if a tool is installed"""
        try:
            subprocess.run(["which", tool], capture_output=True, check=True)
            return True
        except:
            return False
    
    @staticmethod
    def check_all_tools():
        """Check if all required tools are installed"""
        missing = []
        for tool in SystemChecker.REQUIRED_TOOLS:
            if not SystemChecker.check_tool(tool):
                missing.append(tool)
        return missing
    
    @staticmethod
    def get_os():
        """Get operating system"""
        return sys.platform
    
    @staticmethod
    def check_python_version():
        """Check Python version"""
        return sys.version_info
