"""Plugin registry for managing report plugins."""

from typing import Dict, Type, Optional
from .plugin import BaseReportPlugin


class PluginRegistry:
    """Registry for discovering and managing report plugins."""
    
    def __init__(self):
        self._plugins: Dict[str, Type[BaseReportPlugin]] = {}
    
    def register(self, plugin_class: Type[BaseReportPlugin]) -> None:
        """Register a plugin class."""
        plugin_name = plugin_class.name if hasattr(plugin_class, 'name') else plugin_class.__name__
        self._plugins[plugin_name] = plugin_class
    
    def get(self, name: str) -> Optional[Type[BaseReportPlugin]]:
        """Get plugin class by name."""
        return self._plugins.get(name)
    
    def list_plugins(self) -> list:
        """List all registered plugin names."""
        return list(self._plugins.keys())
    
    def has_plugin(self, name: str) -> bool:
        """Check if plugin is registered."""
        return name in self._plugins


# Global registry instance
_registry = PluginRegistry()


def register_plugin(plugin_class: Type[BaseReportPlugin]) -> Type[BaseReportPlugin]:
    """Decorator to register a plugin."""
    _registry.register(plugin_class)
    return plugin_class


def get_plugin(name: str) -> Optional[Type[BaseReportPlugin]]:
    """Get plugin by name."""
    return _registry.get(name)


def list_plugins() -> list:
    """List all registered plugins."""
    return _registry.list_plugins()
