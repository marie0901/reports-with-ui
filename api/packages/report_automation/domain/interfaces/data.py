"""Abstract interfaces for data processing services."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any
from ..models import CampaignData, ProcessedData


class DataProcessor(ABC):
    """Abstract interface for processing CSV data."""
    
    @abstractmethod
    def read_csv(self, file_path: Path) -> List[CampaignData]:
        """Read and validate CSV data into CampaignData models."""
        pass
    
    @abstractmethod
    def validate_data(self, data: List[CampaignData]) -> bool:
        """Validate campaign data meets business requirements."""
        pass
    
    @abstractmethod
    def filter_by_brand(self, data: List[CampaignData], brand: str) -> List[CampaignData]:
        """Filter campaign data by brand patterns."""
        pass
    
    @abstractmethod
    def filter_by_time_period(self, data: List[CampaignData], period: str) -> List[CampaignData]:
        """Filter campaign data by time period."""
        pass


class DataTransformer(ABC):
    """Abstract interface for transforming campaign data."""
    
    @abstractmethod
    def aggregate_by_weeks(self, data: List[CampaignData], boundaries: List[tuple]) -> Dict[str, Dict[str, int]]:
        """Aggregate campaign data by weekly boundaries."""
        pass
    
    @abstractmethod
    def calculate_percentages(self, aggregated_data: Dict[str, Dict[str, int]]) -> Dict[str, Dict[str, float]]:
        """Calculate percentage metrics from aggregated data."""
        pass
    
    @abstractmethod
    def transform_for_report(self, data: List[CampaignData], report_type: str) -> ProcessedData:
        """Transform raw data into report-ready format."""
        pass


class ReportGenerator(ABC):
    """Abstract interface for generating Excel reports."""
    
    @abstractmethod
    def create_workbook(self, data: ProcessedData, output_path: Path) -> None:
        """Create Excel workbook from processed data."""
        pass
    
    @abstractmethod
    def apply_formatting(self, workbook_path: Path, report_type: str) -> None:
        """Apply report-specific formatting to Excel workbook."""
        pass
    
    @abstractmethod
    def validate_output(self, output_path: Path) -> bool:
        """Validate generated Excel file meets requirements."""
        pass
