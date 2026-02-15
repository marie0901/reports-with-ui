"""Excel layout and formatting models."""

from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, validator


class CellPosition(BaseModel):
    """Represents a cell position in Excel."""
    
    row: int = Field(ge=1, description="Row number (1-based)")
    column: str = Field(description="Column letter (e.g., 'A', 'B', 'AA')")
    
    @validator('column')
    def validate_column(cls, v):
        """Validate column letter format."""
        if not v.isalpha() or not v.isupper():
            raise ValueError('Column must be uppercase alphabetic')
        return v


class CellStyle(BaseModel):
    """Cell formatting style."""
    
    font_bold: bool = Field(default=False, description="Bold font")
    font_size: int = Field(default=11, ge=8, le=72, description="Font size")
    background_color: Optional[str] = Field(default=None, description="Background color (hex)")
    text_color: Optional[str] = Field(default=None, description="Text color (hex)")
    alignment: str = Field(default="left", description="Text alignment")
    number_format: Optional[str] = Field(default=None, description="Number format")
    
    @validator('alignment')
    def validate_alignment(cls, v):
        """Validate alignment options."""
        valid_alignments = ["left", "center", "right"]
        if v not in valid_alignments:
            raise ValueError(f'Alignment must be one of {valid_alignments}')
        return v


class ExcelSection(BaseModel):
    """Represents a section in the Excel report."""
    
    name: str = Field(description="Section name")
    start_row: int = Field(ge=1, description="Starting row number")
    end_row: int = Field(ge=1, description="Ending row number")
    columns: Dict[str, str] = Field(description="Metric to column mapping")
    header_style: Optional[CellStyle] = Field(default=None, description="Header cell style")
    data_style: Optional[CellStyle] = Field(default=None, description="Data cell style")
    
    @validator('end_row')
    def end_row_after_start(cls, v, values):
        """Validate end row is after start row."""
        if 'start_row' in values and v < values['start_row']:
            raise ValueError('end_row must be >= start_row')
        return v


class WorksheetLayout(BaseModel):
    """Complete worksheet layout definition."""
    
    name: str = Field(description="Worksheet name")
    sections: List[ExcelSection] = Field(description="Worksheet sections")
    column_widths: Dict[str, float] = Field(
        default_factory=dict,
        description="Column letter to width mapping"
    )
    freeze_panes: Optional[CellPosition] = Field(
        default=None,
        description="Cell position to freeze panes"
    )
    
    # Global styles
    default_font: str = Field(default="Arial", description="Default font family")
    default_font_size: int = Field(default=11, description="Default font size")
    
    @validator('sections')
    def validate_no_overlapping_sections(cls, v):
        """Validate sections don't overlap."""
        for i, section1 in enumerate(v):
            for section2 in v[i+1:]:
                if not (section1.end_row < section2.start_row or section2.end_row < section1.start_row):
                    raise ValueError(f'Sections {section1.name} and {section2.name} overlap')
        return v


class ExcelReport(BaseModel):
    """Complete Excel report structure."""
    
    filename: str = Field(description="Output filename")
    worksheets: List[WorksheetLayout] = Field(description="Worksheet layouts")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Report metadata"
    )
    
    @validator('filename')
    def validate_filename(cls, v):
        """Validate filename has .xlsx extension."""
        if not v.endswith('.xlsx'):
            raise ValueError('Filename must have .xlsx extension')
        return v
