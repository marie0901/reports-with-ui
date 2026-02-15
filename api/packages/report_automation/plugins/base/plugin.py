"""Base plugin system for report generation."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any
import pandas as pd


class BaseReportPlugin(ABC):
    """Abstract base class for report plugins."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name identifier."""
        pass
    
    @property
    @abstractmethod
    def supports_multiple_files(self) -> bool:
        """Whether plugin supports multiple input files."""
        pass
    
    @abstractmethod
    def process_csv(self, csv_path: Path) -> pd.DataFrame:
        """Read and process CSV file(s)."""
        pass
    
    @abstractmethod
    def transform_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Transform data into report structure."""
        pass
    
    @abstractmethod
    def generate_excel(self, report_data: Dict[str, Any], output_path: Path) -> None:
        """Generate Excel file from report data."""
        pass
    
    
    def validate_input(self, csv_path: Path) -> bool:
        """Validate input file(s) exist and are readable."""
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
        return True
    
    def execute(self, input_path: Path, output_path: Path) -> None:
        """Execute full report generation pipeline."""
        self.validate_input(input_path)
        data = self.process_csv(input_path)
        report_data = self.transform_data(data)
        self.generate_excel(report_data, output_path)

    def get_input_slots(self) -> List[Dict[str, Any]]:
        """Return list of expected input slots."""
        # Default implementation: single 'source' slot
        return [{
            "id": "source",
            "label": "Source Files",
            "description": "Upload CSV files for the report.",
            "required": True,
            "accept": ".csv"
        }]

    def get_expected_templates(self) -> Dict[str, List[str]]:
        """Return mapping of slot IDs to expected template names."""
        return {}

    def get_config(self) -> Dict[str, Any]:
        """Return full configuration for frontend."""
        return {
            "name": self.name,
            "input_slots": self.get_input_slots(),
            "expected_templates": self.get_expected_templates()
        }

    def validate_data(self, input_paths: List[Path]) -> Dict[str, Any]:
        """Analyze data and return a summary of matches/mismatches."""
        # Default implementation: basic row counts
        summary = {"total_files": len(input_paths), "files": []}
        for path in input_paths:
            try:
                df = pd.read_csv(path)
                summary["files"].append({
                    "name": path.name,
                    "rows": len(df),
                    "status": "ok"
                })
            except Exception as e:
                summary["files"].append({
                    "name": path.name,
                    "status": "error",
                    "error": str(e)
                })
        return summary
