from plugins.base_plugin import BasePlugin

class ExamplePlugin(BasePlugin):
    """Example plugin template"""
    
    def __init__(self):
        super().__init__("Example Plugin", "1.0.0")
    
    def initialize(self):
        print(f"[+] Initializing {self.name} v{self.version}")
        return True
    
    def execute(self, *args, **kwargs):
        print(f"[*] Executing {self.name}")
        return True
    
    def cleanup(self):
        print(f"[*] Cleaning up {self.name}")
        return True
