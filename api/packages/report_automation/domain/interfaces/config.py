"""Abstract interfaces for configuration management."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List
from ..models import ReportSpecification, ReportConfig


class ConfigLoader(ABC):
    """Abstract interface for loading configuration files."""
    
    @abstractmethod
    def load_report_config(self, report_type: str) -> ReportSpecification:
        """Load configuration for a specific report type."""
        pass
    
    @abstractmethod
    def load_from_file(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration from YAML/JSON file."""
        pass
    
    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate configuration structure and values."""
        pass
    
    @abstractmethod
    def get_available_reports(self) -> List[str]:
        """Get list of available report types."""
        pass


class ConfigManager(ABC):
    """Abstract interface for managing configuration state."""
    
    @abstractmethod
    def get_config(self, report_type: str) -> ReportConfig:
        """Get runtime configuration for report type."""
        pass
    
    @abstractmethod
    def update_config(self, report_type: str, config: ReportConfig) -> None:
        """Update configuration for report type."""
        pass
    
    @abstractmethod
    def cache_config(self, report_type: str, config: ReportConfig) -> None:
        """Cache configuration for performance."""
        pass
    
    @abstractmethod
    def clear_cache(self) -> None:
        """Clear configuration cache."""
        pass
