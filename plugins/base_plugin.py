from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Base class for all plugins"""
    
    def __init__(self, name, version):
        self.name = name
        self.version = version
        self.enabled = True
    
    @abstractmethod
    def initialize(self):
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute plugin functionality"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """Cleanup resources"""
        pass
    
    def get_info(self):
        """Get plugin information"""
        return {
            'name': self.name,
            'version': self.version,
            'enabled': self.enabled
        }
