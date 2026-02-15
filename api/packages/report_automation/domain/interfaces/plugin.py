"""Abstract interfaces for plugin system."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
from ..models import CampaignData, ProcessedData, ReportSpecification


class ReportPlugin(ABC):
    """Abstract base class for report type plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name/identifier."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Plugin description."""
        pass
    
    @property
    @abstractmethod
    def supported_file_count(self) -> int:
        """Number of input files this plugin supports (1 for single, -1 for unlimited)."""
        pass
    
    @abstractmethod
    def validate_input(self, input_files: List[Path]) -> bool:
        """Validate input files are compatible with this plugin."""
        pass
    
    @abstractmethod
    def process_data(self, input_files: List[Path]) -> ProcessedData:
        """Process input files and return report-ready data."""
        pass
    
    @abstractmethod
    def generate_report(self, data: ProcessedData, output_path: Path) -> None:
        """Generate Excel report from processed data."""
        pass
    
    @abstractmethod
    def get_configuration(self) -> ReportSpecification:
        """Get plugin configuration specification."""
        pass


class PluginRegistry(ABC):
    """Abstract interface for plugin discovery and management."""
    
    @abstractmethod
    def register_plugin(self, plugin: ReportPlugin) -> None:
        """Register a report plugin."""
        pass
    
    @abstractmethod
    def get_plugin(self, name: str) -> Optional[ReportPlugin]:
        """Get plugin by name."""
        pass
    
    @abstractmethod
    def list_plugins(self) -> List[str]:
        """List all registered plugin names."""
        pass
    
    @abstractmethod
    def discover_plugins(self, plugin_dir: Path) -> List[ReportPlugin]:
        """Discover plugins in directory."""
        pass
    
    @abstractmethod
    def validate_plugin(self, plugin: ReportPlugin) -> bool:
        """Validate plugin implementation."""
        pass


class PluginLoader(ABC):
    """Abstract interface for loading plugins dynamically."""
    
    @abstractmethod
    def load_plugin(self, plugin_path: Path) -> ReportPlugin:
        """Load plugin from file path."""
        pass
    
    @abstractmethod
    def load_plugins_from_directory(self, directory: Path) -> List[ReportPlugin]:
        """Load all plugins from directory."""
        pass
    
    @abstractmethod
    def reload_plugin(self, plugin_name: str) -> ReportPlugin:
        """Reload plugin by name."""
        pass
