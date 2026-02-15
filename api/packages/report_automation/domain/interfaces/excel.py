"""Abstract interfaces for Excel generation and formatting."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..models import ProcessedData, WorksheetLayout, ExcelReport


class ExcelGenerator(ABC):
    """Abstract interface for Excel file generation."""
    
    @abstractmethod
    def create_workbook(self, layout: WorksheetLayout) -> Any:
        """Create new Excel workbook with specified layout."""
        pass
    
    @abstractmethod
    def add_worksheet(self, workbook: Any, layout: WorksheetLayout) -> Any:
        """Add worksheet to existing workbook."""
        pass
    
    @abstractmethod
    def populate_data(self, worksheet: Any, data: ProcessedData) -> None:
        """Populate worksheet with processed data."""
        pass
    
    @abstractmethod
    def save_workbook(self, workbook: Any, output_path: Path) -> None:
        """Save workbook to file."""
        pass


class ExcelFormatter(ABC):
    """Abstract interface for Excel formatting."""
    
    @abstractmethod
    def apply_cell_style(self, worksheet: Any, cell_range: str, style: Dict[str, Any]) -> None:
        """Apply styling to cell range."""
        pass
    
    @abstractmethod
    def set_column_width(self, worksheet: Any, column: str, width: float) -> None:
        """Set column width."""
        pass
    
    @abstractmethod
    def add_borders(self, worksheet: Any, cell_range: str, border_style: str) -> None:
        """Add borders to cell range."""
        pass
    
    @abstractmethod
    def freeze_panes(self, worksheet: Any, cell: str) -> None:
        """Freeze panes at specified cell."""
        pass


class ExcelValidator(ABC):
    """Abstract interface for Excel file validation."""
    
    @abstractmethod
    def validate_structure(self, file_path: Path, expected_layout: WorksheetLayout) -> bool:
        """Validate Excel file structure matches expected layout."""
        pass
    
    @abstractmethod
    def validate_data(self, file_path: Path, expected_data: ProcessedData) -> bool:
        """Validate Excel file data matches expected values."""
        pass
    
    @abstractmethod
    def check_formatting(self, file_path: Path, report_type: str) -> bool:
        """Check if formatting meets report type requirements."""
        pass
