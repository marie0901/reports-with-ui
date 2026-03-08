"""Report plugins package."""

from .base import BaseReportPlugin, register_plugin, get_plugin, list_plugins
# Import implementations to trigger registration
from .implementations import *

__all__ = [
    "BaseReportPlugin",
    "register_plugin",
    "get_plugin", 
    "list_plugins",
]
