"""CSV export functionality for nano-agent system.

This module provides CSV export capabilities with data sanitization, 
field mapping, and streaming support for large datasets.
"""

import csv
from typing import List, Dict, Any, Optional, TextIO, Union
from dataclasses import dataclass
from io import StringIO

from .export_models import FieldMapping


@dataclass
class CSVExportConfig:
    """Configuration for CSV export operations."""
    delimiter: str = ','
    quote_char: str = '"'
    include_headers: bool = True
    streaming_chunk_size: int = 1000


class CSVExporter:
    """CSV export engine with data sanitization and streaming support."""
    
    def __init__(self, config: CSVExportConfig):
        self.config = config
    
    def export_to_stream(
        self, 
        data: List[Dict[str, Any]], 
        output: TextIO,
        sanitize_fields: Optional[List[str]] = None,
        field_mapping: Optional[FieldMapping] = None
    ) -> None:
        """Export data to a stream (StringIO, file, etc.).
        
        Args:
            data: List of dictionaries to export
            output: TextIO stream to write CSV data to
            sanitize_fields: List of field names to redact for security
            field_mapping: Optional field mapping for renaming/filtering fields
        """
        if not data:
            return
        
        # Apply transformations in order: mapping first, then sanitization
        processed_data = self._apply_field_mapping(data, field_mapping)
        processed_data = self._apply_sanitization(processed_data, sanitize_fields)
        
        # Get fieldnames from first row
        fieldnames = list(processed_data[0].keys()) if processed_data else []
        
        # Create CSV writer with configured options
        writer = csv.DictWriter(
            output,
            fieldnames=fieldnames,
            delimiter=self.config.delimiter,
            quotechar=self.config.quote_char,
            quoting=csv.QUOTE_MINIMAL
        )
        
        # Write headers if configured
        if self.config.include_headers:
            writer.writeheader()
        
        # Write data rows
        for row in processed_data:
            writer.writerow(row)
    
    def export_to_file(
        self, 
        data: List[Dict[str, Any]], 
        file_path: str,
        sanitize_fields: Optional[List[str]] = None,
        field_mapping: Optional[FieldMapping] = None
    ) -> None:
        """Export data to a file.
        
        Args:
            data: List of dictionaries to export
            file_path: Path to output CSV file
            sanitize_fields: List of field names to redact for security
            field_mapping: Optional field mapping for renaming/filtering fields
        """
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            self.export_to_stream(data, f, sanitize_fields, field_mapping)
    
    def _apply_field_mapping(
        self, 
        data: List[Dict[str, Any]], 
        field_mapping: Optional[FieldMapping]
    ) -> List[Dict[str, Any]]:
        """Apply field mapping transformation to data."""
        if not field_mapping:
            return data
        
        mapped_data = []
        for row in data:
            mapped_row = field_mapping.apply_to_data(row)
            mapped_data.append(mapped_row)
        return mapped_data
    
    def _apply_sanitization(
        self, 
        data: List[Dict[str, Any]], 
        sensitive_fields: Optional[List[str]]
    ) -> List[Dict[str, Any]]:
        """Replace sensitive field values with [REDACTED]."""
        if not sensitive_fields:
            return data
        
        sanitized_data = []
        for row in data:
            sanitized_row = row.copy()
            for field in sensitive_fields:
                if field in sanitized_row:
                    sanitized_row[field] = '[REDACTED]'
            sanitized_data.append(sanitized_row)
        return sanitized_data