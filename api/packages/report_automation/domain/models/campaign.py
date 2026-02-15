"""Core data models for campaign data and report processing."""

from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel, Field, validator


class CampaignData(BaseModel):
    """Represents a single row of CSV campaign data."""
    
    timestamp: datetime
    timestamp_rfc3339: Optional[str] = None
    template_id: str
    template_name: str
    campaign_name: str
    sent: int = Field(ge=0, description="Number of emails sent")
    delivered: int = Field(ge=0, description="Number of emails delivered")
    opened: int = Field(ge=0, description="Number of emails opened")
    clicked: int = Field(ge=0, description="Number of emails clicked")
    converted: int = Field(ge=0, description="Number of conversions")
    bounced: int = Field(ge=0, description="Number of bounced emails")
    unsubscribed: int = Field(ge=0, description="Number of unsubscribes")

    @validator('delivered')
    def delivered_not_greater_than_sent(cls, v, values):
        """Validate that delivered count doesn't exceed sent count."""
        if 'sent' in values and v > values['sent']:
            raise ValueError('delivered cannot be greater than sent')
        return v

    @validator('opened')
    def opened_not_greater_than_delivered(cls, v, values):
        """Validate that opened count doesn't exceed delivered count."""
        if 'delivered' in values and v > values['delivered']:
            raise ValueError('opened cannot be greater than delivered')
        return v


class ReportConfig(BaseModel):
    """Configuration for report generation."""
    
    report_type: str
    template_mappings: Dict[str, str] = Field(
        description="Template name to time period mapping, e.g., '2d' -> '1d'"
    )
    weekly_boundaries: List[Tuple[str, str]] = Field(
        description="List of (start_date, end_date) tuples for weekly periods"
    )
    time_periods: List[str] = Field(
        default=["10m", "1h", "1d", "3d", "7d"],
        description="Supported time periods"
    )
    brand_patterns: Dict[str, List[str]] = Field(
        default={"Casino A": ["casino"], "Sport B": ["sport"]},
        description="Brand identification patterns"
    )


class ExcelLayout(BaseModel):
    """Defines Excel output structure and formatting."""
    
    columns: Dict[str, str] = Field(
        description="Metric to column letter mapping, e.g., 'total' -> 'H'"
    )
    week_labels: List[str] = Field(
        description="Week labels for column headers"
    )
    metric_labels: List[str] = Field(
        default=[
            "Sent", "Delivered", "Opened", "Clicked",
            "Converted (Dep/Acc.Bon)", "Unsubscribe",
            "% Delivered", "% Open", "% Click", "% CR"
        ],
        description="Metric labels for row headers"
    )
    brand_sections: Dict[str, Dict[str, str]] = Field(
        description="Brand-specific column mappings"
    )


class MetricCalculation(BaseModel):
    """Business rules for metric calculations."""
    
    base_metrics: List[str] = Field(
        default=["sent", "delivered", "opened", "clicked", "converted"],
        description="Base metrics to aggregate"
    )
    percentage_metrics: List[str] = Field(
        default=["% Delivered", "% Open", "% Click", "% CR"],
        description="Percentage metrics to calculate"
    )
    aggregation_method: str = Field(
        default="sum",
        description="Method for aggregating metrics across time periods"
    )
    percentage_precision: int = Field(
        default=2,
        description="Decimal places for percentage calculations"
    )

    @validator('aggregation_method')
    def validate_aggregation_method(cls, v):
        """Validate aggregation method is supported."""
        allowed_methods = ["sum", "mean", "max", "min"]
        if v not in allowed_methods:
            raise ValueError(f'aggregation_method must be one of {allowed_methods}')
        return v


class ProcessedData(BaseModel):
    """Represents processed campaign data ready for Excel generation."""
    
    report_type: str
    time_periods: List[str]
    weekly_data: Dict[str, Dict[str, Dict[str, int]]] = Field(
        description="Nested dict: time_period -> week -> metric -> value"
    )
    totals: Dict[str, Dict[str, int]] = Field(
        description="Total values: time_period -> metric -> value"
    )
    percentages: Dict[str, Dict[str, float]] = Field(
        description="Calculated percentages: time_period -> metric -> percentage"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the processing"
    )
