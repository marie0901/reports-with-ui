"""Configuration models for report specifications."""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class TemplateMapping(BaseModel):
    """Template name to time period mapping configuration."""
    
    source_template: str = Field(description="Original template name from CSV")
    target_period: str = Field(description="Mapped time period (e.g., '1d', '3d')")
    brand: Optional[str] = Field(default=None, description="Associated brand")


class WeeklyBoundary(BaseModel):
    """Weekly boundary configuration."""
    
    week_number: int = Field(ge=1, le=52, description="Week number")
    start_date: str = Field(description="Start date in YYYY-MM-DD format")
    end_date: str = Field(description="End date in YYYY-MM-DD format")
    label: str = Field(description="Display label for the week")

    @validator('start_date', 'end_date')
    def validate_date_format(cls, v):
        """Validate date format is YYYY-MM-DD."""
        from datetime import datetime
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        return v


class ColumnMapping(BaseModel):
    """Excel column mapping configuration."""
    
    metric: str = Field(description="Metric name")
    column_letter: str = Field(description="Excel column letter (e.g., 'H', 'I')")
    week_offset: Optional[int] = Field(default=None, description="Week offset for multi-week columns")

    @validator('column_letter')
    def validate_column_letter(cls, v):
        """Validate column letter format."""
        if not v.isalpha() or not v.isupper():
            raise ValueError('Column letter must be uppercase alphabetic')
        return v


class ReportSpecification(BaseModel):
    """Complete specification for a report type."""
    
    name: str = Field(description="Report type name")
    description: str = Field(description="Report description")
    template_mappings: List[TemplateMapping] = Field(description="Template to period mappings")
    weekly_boundaries: List[WeeklyBoundary] = Field(description="Weekly boundary definitions")
    column_mappings: List[ColumnMapping] = Field(description="Excel column mappings")
    time_periods: List[str] = Field(description="Supported time periods")
    brands: List[str] = Field(default=["Casino A", "Sport B"], description="Supported brands")
    
    # Business rules
    aggregation_method: str = Field(default="sum", description="Metric aggregation method")
    percentage_precision: int = Field(default=2, description="Decimal places for percentages")
    
    # Excel formatting
    header_color: str = Field(default="D3D3D3", description="Header background color")
    brand_colors: Dict[str, str] = Field(
        default={"Casino A": "FFB6C1", "Sport B": "ADD8E6"},
        description="Brand-specific colors"
    )
    
    @validator('time_periods')
    def validate_time_periods(cls, v):
        """Validate time periods are in expected format."""
        valid_patterns = ['m', 'h', 'd']
        for period in v:
            if not any(period.endswith(pattern) for pattern in valid_patterns):
                raise ValueError(f'Invalid time period format: {period}')
        return v
