class PluginManager:
    """Manage plugins dynamically"""
    
    def __init__(self):
        self.plugins = {}
    
    def register(self, plugin):
        """Register a plugin"""
        self.plugins[plugin.name] = plugin
        return True
    
    def unregister(self, plugin_name):
        """Unregister a plugin"""
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            return True
        return False
    
    def get_plugin(self, plugin_name):
        """Get plugin by name"""
        return self.plugins.get(plugin_name, None)
    
    def list_plugins(self):
        """List all plugins"""
        return list(self.plugins.keys())
    
    def execute_plugin(self, plugin_name, *args, **kwargs):
        """Execute a plugin"""
        plugin = self.get_plugin(plugin_name)
        if plugin and plugin.enabled:
            return plugin.execute(*args, **kwargs)
        return False
