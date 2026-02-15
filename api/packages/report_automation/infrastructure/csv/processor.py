"""CSV processing implementation."""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
import logging

from ...domain.interfaces import DataProcessor
from ...domain.models import CampaignData


logger = logging.getLogger(__name__)


class CSVProcessor(DataProcessor):
    """Implementation of CSV data processing."""
    
    def __init__(self):
        """Initialize CSV processor."""
        self.required_columns = [
            "timestamp", "template_id", "template_name", "campaign_name",
            "sent", "delivered", "opened", "clicked", "converted", 
            "bounced", "unsubscribed"
        ]
        self.brand_patterns = {
            "Casino A": ["casino", "Casino A"],
            "Sport B": ["sport", "Sport B"]
        }
    
    def read_csv(self, file_path: Path) -> List[CampaignData]:
        """Read and validate CSV data into CampaignData models."""
        logger.info(f"Reading CSV file: {file_path}")
        
        if not file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        
        try:
            # Read CSV with pandas
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} rows from CSV")
            
            # Validate required columns
            self._validate_columns(df)
            
            # Process timestamps
            df = self._process_timestamps(df)
            
            # Convert to CampaignData models
            campaign_data = []
            for _, row in df.iterrows():
                try:
                    data = CampaignData(
                        timestamp=row['timestamp'],
                        timestamp_rfc3339=row.get('timestamp_RFC3339'),
                        template_id=str(row['template_id']),
                        template_name=str(row['template_name']),
                        campaign_name=str(row['campaign_name']),
                        sent=int(row['sent']),
                        delivered=int(row['delivered']),
                        opened=int(row['opened']),
                        clicked=int(row['clicked']),
                        converted=int(row['converted']),
                        bounced=int(row['bounced']),
                        unsubscribed=int(row['unsubscribed'])
                    )
                    campaign_data.append(data)
                except Exception as e:
                    logger.warning(f"Skipping invalid row {len(campaign_data)}: {e}")
                    continue
            
            logger.info(f"Successfully processed {len(campaign_data)} valid rows")
            return campaign_data
            
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            raise
    
    def validate_data(self, data: List[CampaignData]) -> bool:
        """Validate campaign data meets business requirements."""
        if not data:
            logger.warning("No data to validate")
            return False
        
        # Check for basic data integrity
        for i, campaign in enumerate(data):
            # Validate metric relationships
            if campaign.delivered > campaign.sent:
                logger.error(f"Row {i}: delivered ({campaign.delivered}) > sent ({campaign.sent})")
                return False
            
            if campaign.opened > campaign.delivered:
                logger.error(f"Row {i}: opened ({campaign.opened}) > delivered ({campaign.delivered})")
                return False
            
            if campaign.clicked > campaign.opened:
                logger.error(f"Row {i}: clicked ({campaign.clicked}) > opened ({campaign.opened})")
                return False
        
        logger.info(f"Data validation passed for {len(data)} records")
        return True
    
    def filter_by_brand(self, data: List[CampaignData], brand: str) -> List[CampaignData]:
        """Filter campaign data by brand patterns."""
        if brand not in self.brand_patterns:
            logger.warning(f"Unknown brand: {brand}")
            return []
        
        patterns = self.brand_patterns[brand]
        filtered_data = []
        
        for campaign in data:
            # Check if any brand pattern matches template or campaign name
            template_lower = campaign.template_name.lower()
            campaign_lower = campaign.campaign_name.lower()
            
            if any(pattern.lower() in template_lower or pattern.lower() in campaign_lower 
                   for pattern in patterns):
                filtered_data.append(campaign)
        
        logger.info(f"Filtered {len(filtered_data)} records for brand: {brand}")
        return filtered_data
    
    def filter_by_time_period(self, data: List[CampaignData], period: str) -> List[CampaignData]:
        """Filter campaign data by time period."""
        # Extract time period patterns from template names
        filtered_data = []
        
        for campaign in data:
            template_name = campaign.template_name.lower()
            
            # Check for direct period match in template name
            if period == "10m" and "10 min" in template_name:
                filtered_data.append(campaign)
            elif period == "1h" and ("1h" in template_name or "1 h" in template_name):
                filtered_data.append(campaign)
            elif period == "1d" and ("1d" in template_name or "2d" in template_name):
                filtered_data.append(campaign)
            elif period == "3d" and ("3d" in template_name or "4d" in template_name):
                filtered_data.append(campaign)
            elif period == "7d" and ("7d" in template_name or "8d" in template_name):
                filtered_data.append(campaign)
        
        logger.info(f"Filtered {len(filtered_data)} records for period: {period}")
        return filtered_data
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Validate that required columns are present."""
        missing_columns = [col for col in self.required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        logger.debug(f"All required columns present: {self.required_columns}")
    
    def _process_timestamps(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process timestamp columns to datetime objects."""
        try:
            # Convert timestamp column to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Remove timezone info if present (for Excel compatibility)
            if df['timestamp'].dt.tz is not None:
                df['timestamp'] = df['timestamp'].dt.tz_localize(None)
            
            logger.debug("Timestamps processed successfully")
            return df
            
        except Exception as e:
            logger.error(f"Error processing timestamps: {e}")
            raise ValueError(f"Invalid timestamp format: {e}")
    
    def get_date_range(self, data: List[CampaignData]) -> tuple:
        """Get the date range of the campaign data."""
        if not data:
            return None, None
        
        timestamps = [campaign.timestamp for campaign in data]
        min_date = min(timestamps)
        max_date = max(timestamps)
        
        logger.info(f"Date range: {min_date.date()} to {max_date.date()}")
        return min_date, max_date
    
    def get_template_summary(self, data: List[CampaignData]) -> Dict[str, int]:
        """Get summary of templates and their counts."""
        template_counts = {}
        for campaign in data:
            template_counts[campaign.template_name] = template_counts.get(campaign.template_name, 0) + 1
        
        logger.info(f"Found {len(template_counts)} unique templates")
        return template_counts
