import pytest
import pandas as pd
import tempfile
import os
from io import StringIO
from unittest.mock import Mock, patch

from nano_agent.modules.csv_exporter import CSVExporter, CSVExportConfig
from nano_agent.modules.export_models import FieldMapping


class TestCSVExporter:
    
    def setup_method(self):
        """Setup test fixtures for each test method."""
        self.config = CSVExportConfig(
            delimiter=',',
            quote_char='"',
            include_headers=True,
            streaming_chunk_size=1000
        )
        self.exporter = CSVExporter(self.config)
        
    def test_csv_exporter_initialization(self):
        """Test CSV exporter initializes with correct configuration."""
        assert self.exporter.config.delimiter == ','
        assert self.exporter.config.quote_char == '"'
        assert self.exporter.config.include_headers is True
        assert self.exporter.config.streaming_chunk_size == 1000
        
    def test_simple_data_export(self):
        """Test exporting simple tabular data to CSV."""
        data = [
            {'name': 'test1', 'value': 100, 'status': 'success'},
            {'name': 'test2', 'value': 200, 'status': 'failed'}
        ]
        
        output = StringIO()
        self.exporter.export_to_stream(data, output)
        
        result = output.getvalue()
        lines = result.strip().split('\n')
        
        # Remove carriage returns for cross-platform compatibility
        lines = [line.rstrip('\r') for line in lines]
        
        assert lines[0] == 'name,value,status'
        assert lines[1] == 'test1,100,success'
        assert lines[2] == 'test2,200,failed'
        
    def test_data_sanitization(self):
        """Test that sensitive data is properly sanitized."""
        data = [
            {
                'api_key': 'sk-secret123',
                'token': 'bearer-token',
                'safe_field': 'public_data'
            }
        ]
        
        sensitive_fields = ['api_key', 'token']
        output = StringIO()
        
        self.exporter.export_to_stream(
            data, output, 
            sanitize_fields=sensitive_fields
        )
        
        result = output.getvalue()
        assert 'sk-secret123' not in result
        assert 'bearer-token' not in result
        assert '[REDACTED]' in result
        assert 'public_data' in result
        
    def test_field_mapping_selection(self):
        """Test custom field mapping and selection."""
        data = [
            {
                'internal_id': 'id123',
                'user_name': 'john',
                'score': 95,
                'internal_notes': 'confidential'
            }
        ]
        
        field_mapping = FieldMapping({
            'internal_id': 'ID',
            'user_name': 'Name',
            'score': 'Score'
        })
        
        output = StringIO()
        self.exporter.export_to_stream(
            data, output, 
            field_mapping=field_mapping
        )
        
        result = output.getvalue()
        lines = result.strip().split('\n')
        
        # Remove carriage returns for cross-platform compatibility
        lines = [line.rstrip('\r') for line in lines]
        
        # Check headers are mapped correctly
        assert lines[0] == 'ID,Name,Score'
        assert 'internal_notes' not in result
        assert 'confidential' not in result
        
    def test_streaming_large_dataset(self):
        """Test streaming export for large datasets."""
        # Generate large dataset
        large_data = [
            {'id': i, 'data': f'value_{i}', 'timestamp': f'2024-01-{i%30+1:02d}'}
            for i in range(5000)
        ]
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            try:
                self.exporter.export_to_file(large_data, temp_file.name)
                
                # Verify file was created and has correct content
                assert os.path.exists(temp_file.name)
                
                with open(temp_file.name, 'r') as f:
                    lines = f.readlines()
                    
                # Should have header + 5000 data rows
                assert len(lines) == 5001
                assert 'id,data,timestamp' in lines[0]
                
            finally:
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                    
    def test_special_character_handling(self):
        """Test handling of special characters in data."""
        data = [
            {
                'text': 'Hello, "World"',
                'newlines': 'Line1\nLine2',
                'unicode': 'Café ñoño'
            }
        ]
        
        output = StringIO()
        self.exporter.export_to_stream(data, output)
        
        result = output.getvalue()
        
        # Special characters should be properly escaped
        assert '"Hello, ""World"""' in result  # Quoted quotes
        assert 'Café ñoño' in result  # Unicode preserved