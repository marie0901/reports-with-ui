"""Plugin registry for managing report plugins."""

from typing import Dict, Type, Optional, List
import os
import json
from pathlib import Path
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
        # 1. Check hardcoded plugins
        if name in self._plugins:
            return self._plugins[name]
            
        # 2. Check dynamic JSON configs
        config_path = self._get_config_path(name)
        if config_path and config_path.exists():
            return self._create_dynamic_plugin_class(config_path)
            
        return None
    
    def list_plugins(self) -> List[str]:
        """List all registered and dynamic plugin names."""
        plugins = set(self._plugins.keys())
        
        # Add dynamic configs
        config_dir = self._get_config_dir()
        if config_dir.exists():
            for f in config_dir.glob("*.json"):
                plugins.add(f.stem)
                
        return sorted(list(plugins))
    
    def has_plugin(self, name: str) -> bool:
        """Check if plugin is registered or available as config."""
        if name in self._plugins:
            return True
        config_path = self._get_config_path(name)
        return config_path and config_path.exists()

    def _get_config_dir(self) -> Path:
        """Get the directory where JSON configs are stored."""
        # Assuming we are in api/packages/report_automation/plugins/base/registry.py
        # api is 5 levels up
        return Path(__file__).parents[4] / "storage" / "configs"

    def _get_config_path(self, name: str) -> Optional[Path]:
        """Get path to a specific JSON config."""
        path = self._get_config_dir() / f"{name}.json"
        return path

    def _create_dynamic_plugin_class(self, config_path: Path) -> Type[BaseReportPlugin]:
        """Create a class on the fly for the dynamic plugin."""
        from ..implementations.dynamic import DynamicReportPlugin
        
        class ConfiguredDynamicPlugin(DynamicReportPlugin):
            def __init__(self, *args, **kwargs):
                super().__init__(config_path)
                
        return ConfiguredDynamicPlugin


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
