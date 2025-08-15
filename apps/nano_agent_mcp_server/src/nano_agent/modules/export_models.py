"""Data models for CSV export functionality."""

from typing import Dict, Any, Optional
from pydantic import BaseModel


class FieldMapping:
    """Simple field mapping for CSV exports."""
    
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping
    
    def apply_to_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply field mapping to data dictionary."""
        result = {}
        for old_field, new_field in self.mapping.items():
            if old_field in data:
                result[new_field] = data[old_field]
        return result