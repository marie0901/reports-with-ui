"""Base plugin system."""

from .plugin import BaseReportPlugin
from .registry import PluginRegistry, register_plugin, get_plugin, list_plugins

__all__ = [
    "BaseReportPlugin",
    "PluginRegistry", 
    "register_plugin",
    "get_plugin",
    "list_plugins",
]
