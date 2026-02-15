"""Abstract interfaces for core services."""

from .data import DataProcessor, DataTransformer, ReportGenerator
from .config import ConfigLoader, ConfigManager
from .plugin import ReportPlugin, PluginRegistry, PluginLoader
from .excel import ExcelGenerator, ExcelFormatter, ExcelValidator

__all__ = [
    # Data processing interfaces
    "DataProcessor",
    "DataTransformer", 
    "ReportGenerator",
    
    # Configuration interfaces
    "ConfigLoader",
    "ConfigManager",
    
    # Plugin interfaces
    "ReportPlugin",
    "PluginRegistry",
    "PluginLoader",
    
    # Excel interfaces
    "ExcelGenerator",
    "ExcelFormatter",
    "ExcelValidator",
]
