# CG_TDD Test Strategy: Issue #42 - CSV Export Functionality

## Test Strategy Overview

This document defines a comprehensive test strategy for implementing CSV export functionality in the nano-agent system. Following strict TDD principles, all tests will be written before implementation code, ensuring complete coverage of functional requirements, edge cases, and security considerations.

## Test Pyramid Distribution

- **Unit Tests (70%)**: Core CSV export engine, data models, utilities
- **Integration Tests (20%)**: API endpoints, CLI commands, data source integration
- **End-to-End Tests (10%)**: Complete export workflows, security validation

## Test Implementation Order (TDD Red-Green-Refactor)

### Phase 1: Core CSV Export Engine
1. CSV generation utilities
2. Data formatting and sanitization
3. Field mapping and selection
4. Memory-efficient streaming

### Phase 2: Data Models and Validation
1. Export data structures
2. Privacy filtering mechanisms
3. Field validation and type conversion
4. Export metadata tracking

### Phase 3: API and CLI Integration
1. REST endpoint functionality
2. Authentication and authorization
3. CLI command processing
4. Progress tracking and status

### Phase 4: Security and Performance
1. Data privacy enforcement
2. Access control validation
3. Large dataset handling
4. Concurrent operation support

## Unit Tests

### 1. CSV Export Engine (`tests/unit/test_csv_exporter.py`)

```python
import pytest
import pandas as pd
import tempfile
import os
from io import StringIO
from unittest.mock import Mock, patch
from nano_agent.modules.csv_exporter import CSVExporter, CSVExportConfig
from nano_agent.modules.export_models import ExportData, FieldMapping

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
        
        # Check headers are mapped correctly
        assert lines[0] == 'ID,Name,Score'
        assert 'internal_notes' not in result
        assert 'confidential' not in result
        
    def test_empty_data_handling(self):
        """Test handling of empty datasets."""
        data = []
        output = StringIO()
        
        self.exporter.export_to_stream(data, output)
        result = output.getvalue()
        
        # Should still include headers if configured
        assert result.strip() == '' or result.strip() == 'No data available'
        
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
                    
    def test_memory_efficient_streaming(self):
        """Test that streaming doesn't load all data into memory at once."""
        def data_generator():
            for i in range(10000):
                yield {'id': i, 'value': f'data_{i}'}
                
        with patch.object(self.exporter, '_write_chunk') as mock_write:
            with tempfile.NamedTemporaryFile(mode='w+') as temp_file:
                self.exporter.export_generator_to_file(
                    data_generator(), 
                    temp_file.name
                )
                
                # Verify chunks were written (not all at once)
                assert mock_write.call_count > 1
                
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
        
    def test_data_type_conversion(self):
        """Test automatic data type conversion for CSV compatibility."""
        from datetime import datetime, date
        
        data = [
            {
                'timestamp': datetime(2024, 1, 15, 10, 30),
                'date': date(2024, 1, 15),
                'number': 123.456,
                'boolean': True,
                'none_value': None
            }
        ]
        
        output = StringIO()
        self.exporter.export_to_stream(data, output)
        
        result = output.getvalue()
        lines = result.strip().split('\n')
        
        # Check converted values
        data_line = lines[1]
        assert '2024-01-15 10:30:00' in data_line
        assert '2024-01-15' in data_line
        assert '123.456' in data_line
        assert 'True' in data_line
        assert '' in data_line or 'NULL' in data_line
        
    def test_error_handling_invalid_data(self):
        """Test error handling for invalid or malformed data."""
        # Test with non-serializable objects
        class CustomObject:
            pass
            
        data = [{'valid': 'data', 'invalid': CustomObject()}]
        
        output = StringIO()
        
        # Should handle gracefully, not crash
        try:
            self.exporter.export_to_stream(data, output)
            result = output.getvalue()
            
            # Should contain valid data, handle invalid gracefully
            assert 'valid' in result
            assert 'data' in result
        except Exception as e:
            # If it raises an exception, it should be a meaningful one
            assert "serialization" in str(e).lower() or "conversion" in str(e).lower()
```

### 2. Export Data Models (`tests/unit/test_export_models.py`)

```python
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from nano_agent.modules.export_models import (
    ExportData, EvaluationResult, PerformanceMetric, 
    AgentInteraction, ExportRequest, FieldMapping,
    PrivacyFilter, ExportMetadata
)

class TestExportDataModels:
    
    def test_evaluation_result_model(self):
        """Test EvaluationResult data model validation."""
        result = EvaluationResult(
            test_id="test_123",
            model_name="gpt-5-mini",
            provider="openai",
            success=True,
            score=95.5,
            execution_time=1.25,
            tokens_used=150,
            cost=0.002,
            timestamp=datetime.now(),
            error_message=None
        )
        
        assert result.test_id == "test_123"
        assert result.model_name == "gpt-5-mini"
        assert result.success is True
        assert result.score == 95.5
        
    def test_performance_metric_model(self):
        """Test PerformanceMetric data model validation."""
        metric = PerformanceMetric(
            metric_name="response_time",
            value=1.234,
            unit="seconds",
            provider="anthropic",
            model="claude-sonnet-4",
            timestamp=datetime.now(),
            metadata={"endpoint": "/v1/chat", "method": "POST"}
        )
        
        assert metric.metric_name == "response_time"
        assert metric.value == 1.234
        assert metric.unit == "seconds"
        assert isinstance(metric.metadata, dict)
        
    def test_agent_interaction_model(self):
        """Test AgentInteraction data model validation."""
        interaction = AgentInteraction(
            session_id="session_456",
            request_id="req_789",
            user_prompt="What is 2+2?",
            agent_response="The answer is 4.",
            tools_used=["calculator", "validator"],
            provider="ollama",
            model="llama-3",
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(seconds=2),
            success=True
        )
        
        assert interaction.session_id == "session_456"
        assert len(interaction.tools_used) == 2
        assert interaction.success is True
        
    def test_export_request_validation(self):
        """Test ExportRequest validation and requirements."""
        # Valid request
        request = ExportRequest(
            export_type="evaluation_results",
            date_from=datetime.now() - timedelta(days=7),
            date_to=datetime.now(),
            filters={"provider": "openai", "success": True},
            fields=["test_id", "model_name", "score"],
            privacy_level="public"
        )
        
        assert request.export_type == "evaluation_results"
        assert isinstance(request.filters, dict)
        assert len(request.fields) == 3
        
    def test_export_request_invalid_type(self):
        """Test ExportRequest validation with invalid export type."""
        with pytest.raises(ValidationError) as exc_info:
            ExportRequest(
                export_type="invalid_type",
                date_from=datetime.now(),
                date_to=datetime.now()
            )
            
        assert "export_type" in str(exc_info.value)
        
    def test_field_mapping_functionality(self):
        """Test FieldMapping for field selection and renaming."""
        mapping = FieldMapping({
            "internal_field": "Public Name",
            "test_id": "Test ID",
            "model_name": "Model"
        })
        
        # Test field selection
        original_data = {
            "internal_field": "value1",
            "test_id": "test_123",
            "model_name": "gpt-5",
            "excluded_field": "should_not_appear"
        }
        
        mapped_data = mapping.apply_to_data(original_data)
        
        assert "Public Name" in mapped_data
        assert "Test ID" in mapped_data
        assert "Model" in mapped_data
        assert "excluded_field" not in mapped_data
        assert "internal_field" not in mapped_data
        
    def test_privacy_filter_application(self):
        """Test privacy filtering of sensitive data."""
        privacy_filter = PrivacyFilter(
            sensitive_fields=["api_key", "token", "password"],
            redaction_text="[REDACTED]",
            privacy_level="strict"
        )
        
        data = {
            "api_key": "sk-secret123",
            "token": "bearer_token",
            "public_field": "safe_data",
            "user_id": "user123"
        }
        
        filtered_data = privacy_filter.apply_to_data(data)
        
        assert filtered_data["api_key"] == "[REDACTED]"
        assert filtered_data["token"] == "[REDACTED]"
        assert filtered_data["public_field"] == "safe_data"
        assert filtered_data["user_id"] == "user123"
        
    def test_export_metadata_tracking(self):
        """Test export metadata generation and tracking."""
        metadata = ExportMetadata(
            export_id="export_001",
            requested_by="user123",
            export_type="performance_metrics",
            record_count=1500,
            file_size_bytes=245760,
            created_at=datetime.now(),
            privacy_level="internal",
            filters_applied={"date_range": "last_7_days", "provider": "anthropic"}
        )
        
        assert metadata.export_id == "export_001"
        assert metadata.record_count == 1500
        assert metadata.file_size_bytes == 245760
        assert isinstance(metadata.filters_applied, dict)
        
    def test_data_model_serialization(self):
        """Test that data models can be serialized to dict/JSON."""
        result = EvaluationResult(
            test_id="test_123",
            model_name="gpt-5-mini",
            provider="openai",
            success=True,
            score=95.5,
            execution_time=1.25,
            tokens_used=150,
            cost=0.002,
            timestamp=datetime.now()
        )
        
        # Test dict conversion
        result_dict = result.model_dump()
        assert isinstance(result_dict, dict)
        assert result_dict["test_id"] == "test_123"
        assert result_dict["success"] is True
        
        # Test JSON serialization
        import json
        json_str = result.model_dump_json()
        parsed = json.loads(json_str)
        assert parsed["model_name"] == "gpt-5-mini"
```

### 3. Export API Endpoints (`tests/unit/test_export_routes.py`)

```python
import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import tempfile
import os

from nano_agent.api.export_routes import ExportRouter
from nano_agent.modules.export_models import ExportRequest, ExportMetadata
from nano_agent.modules.csv_exporter import CSVExporter

class TestExportRoutes:
    
    def setup_method(self):
        """Setup test fixtures for each test method."""
        self.router = ExportRouter()
        self.client = TestClient(self.router.app)
        
    @patch('nano_agent.modules.csv_exporter.CSVExporter')
    def test_export_evaluation_results_endpoint(self, mock_exporter):
        """Test API endpoint for exporting evaluation results."""
        mock_exporter_instance = Mock()
        mock_exporter.return_value = mock_exporter_instance
        
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59",
            "filters": {"provider": "openai"},
            "fields": ["test_id", "model_name", "score"]
        }
        
        with patch('nano_agent.api.export_routes.get_evaluation_data') as mock_get_data:
            mock_get_data.return_value = [
                {"test_id": "test1", "model_name": "gpt-5", "score": 95},
                {"test_id": "test2", "model_name": "gpt-5-mini", "score": 87}
            ]
            
            response = self.client.post("/api/exports/create", json=request_data)
            
            assert response.status_code == 202  # Accepted for async processing
            response_data = response.json()
            assert "export_id" in response_data
            assert "download_url" in response_data
            
    def test_export_request_validation(self):
        """Test validation of export request parameters."""
        # Missing required fields
        invalid_request = {
            "export_type": "evaluation_results"
            # Missing date_from, date_to
        }
        
        response = self.client.post("/api/exports/create", json=invalid_request)
        assert response.status_code == 422  # Validation error
        
        # Invalid export type
        invalid_type_request = {
            "export_type": "invalid_type",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59"
        }
        
        response = self.client.post("/api/exports/create", json=invalid_type_request)
        assert response.status_code == 422
        
    @patch('nano_agent.auth.verify_token')
    def test_authentication_required(self, mock_verify):
        """Test that authentication is required for export endpoints."""
        mock_verify.side_effect = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
        
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59"
        }
        
        response = self.client.post(
            "/api/exports/create", 
            json=request_data,
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
        
    @patch('nano_agent.auth.check_export_permissions')
    def test_authorization_for_sensitive_data(self, mock_check_perms):
        """Test authorization for exporting sensitive data."""
        mock_check_perms.return_value = False  # Insufficient permissions
        
        sensitive_request = {
            "export_type": "agent_interactions",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59",
            "privacy_level": "internal"
        }
        
        response = self.client.post("/api/exports/create", json=sensitive_request)
        assert response.status_code == 403  # Forbidden
        
    def test_export_status_endpoint(self):
        """Test checking export job status."""
        export_id = "export_12345"
        
        with patch('nano_agent.api.export_routes.get_export_status') as mock_status:
            mock_status.return_value = {
                "export_id": export_id,
                "status": "completed",
                "progress": 100,
                "download_url": f"/api/exports/{export_id}/download",
                "created_at": datetime.now().isoformat(),
                "completed_at": datetime.now().isoformat()
            }
            
            response = self.client.get(f"/api/exports/{export_id}/status")
            
            assert response.status_code == 200
            data = response.json()
            assert data["export_id"] == export_id
            assert data["status"] == "completed"
            assert data["progress"] == 100
            
    def test_export_download_endpoint(self):
        """Test downloading completed export file."""
        export_id = "export_12345"
        
        # Create temporary CSV file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write("test_id,model_name,score\n")
            temp_file.write("test1,gpt-5,95\n")
            temp_file.write("test2,gpt-5-mini,87\n")
            temp_file_path = temp_file.name
            
        try:
            with patch('nano_agent.api.export_routes.get_export_file_path') as mock_path:
                mock_path.return_value = temp_file_path
                
                response = self.client.get(f"/api/exports/{export_id}/download")
                
                assert response.status_code == 200
                assert response.headers["content-type"] == "text/csv"
                assert "attachment; filename=" in response.headers["content-disposition"]
                
                # Verify content
                content = response.content.decode('utf-8')
                assert "test_id,model_name,score" in content
                assert "test1,gpt-5,95" in content
                
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    def test_export_list_endpoint(self):
        """Test listing user's export history."""
        with patch('nano_agent.api.export_routes.get_user_exports') as mock_exports:
            mock_exports.return_value = [
                {
                    "export_id": "export_001",
                    "export_type": "evaluation_results",
                    "status": "completed",
                    "created_at": "2024-01-15T10:30:00",
                    "record_count": 150
                },
                {
                    "export_id": "export_002",
                    "export_type": "performance_metrics",
                    "status": "processing",
                    "created_at": "2024-01-15T11:00:00",
                    "progress": 75
                }
            ]
            
            response = self.client.get("/api/exports/list")
            
            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2
            assert data[0]["export_id"] == "export_001"
            assert data[1]["status"] == "processing"
            
    def test_large_export_handling(self):
        """Test handling of large export requests."""
        large_request = {
            "export_type": "agent_interactions",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-12-31T23:59:59",  # Full year
            "filters": {}  # No filters = all data
        }
        
        with patch('nano_agent.api.export_routes.estimate_export_size') as mock_estimate:
            mock_estimate.return_value = 1000000  # 1M records
            
            response = self.client.post("/api/exports/create", json=large_request)
            
            # Should accept but warn about size
            assert response.status_code == 202
            data = response.json()
            assert "warning" in data
            assert "large dataset" in data["warning"].lower()
            
    def test_concurrent_export_limits(self):
        """Test limits on concurrent exports per user."""
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59"
        }
        
        with patch('nano_agent.api.export_routes.get_user_active_exports') as mock_active:
            mock_active.return_value = 3  # Already at limit
            
            response = self.client.post("/api/exports/create", json=request_data)
            
            assert response.status_code == 429  # Too Many Requests
            data = response.json()
            assert "concurrent export limit" in data["detail"].lower()
```

## Integration Tests

### 1. End-to-End Export Workflow (`tests/integration/test_export_workflow.py`)

```python
import pytest
import tempfile
import os
import csv
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from nano_agent.modules.csv_exporter import CSVExporter, CSVExportConfig
from nano_agent.modules.export_models import ExportRequest, EvaluationResult
from nano_agent.api.export_routes import ExportService

class TestExportWorkflow:
    
    def setup_method(self):
        """Setup integration test environment."""
        self.export_service = ExportService()
        self.test_data_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Cleanup test environment."""
        import shutil
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
            
    @pytest.mark.integration
    def test_complete_evaluation_export_workflow(self):
        """Test complete workflow from request to download."""
        # Step 1: Create sample evaluation data
        sample_data = [
            EvaluationResult(
                test_id="test_001",
                model_name="gpt-5-mini",
                provider="openai",
                success=True,
                score=95.5,
                execution_time=1.25,
                tokens_used=150,
                cost=0.002,
                timestamp=datetime.now() - timedelta(hours=1)
            ),
            EvaluationResult(
                test_id="test_002",
                model_name="claude-sonnet-4",
                provider="anthropic",
                success=False,
                score=0.0,
                execution_time=0.5,
                tokens_used=75,
                cost=0.001,
                timestamp=datetime.now() - timedelta(minutes=30),
                error_message="API timeout"
            )
        ]
        
        # Step 2: Create export request
        export_request = ExportRequest(
            export_type="evaluation_results",
            date_from=datetime.now() - timedelta(days=1),
            date_to=datetime.now(),
            filters={"provider": "openai"},
            fields=["test_id", "model_name", "success", "score"]
        )
        
        # Step 3: Process export
        with patch('nano_agent.data.get_evaluation_results') as mock_get_data:
            mock_get_data.return_value = [
                result.model_dump() for result in sample_data 
                if result.provider == "openai"
            ]
            
            export_result = self.export_service.create_export(export_request)
            
            # Step 4: Verify export metadata
            assert export_result.export_id is not None
            assert export_result.status == "completed"
            assert export_result.record_count == 1  # Only OpenAI results
            
            # Step 5: Read and verify CSV content
            export_file_path = export_result.file_path
            assert os.path.exists(export_file_path)
            
            with open(export_file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                assert len(rows) == 1
                assert rows[0]['test_id'] == 'test_001'
                assert rows[0]['model_name'] == 'gpt-5-mini'
                assert rows[0]['success'] == 'True'
                assert rows[0]['score'] == '95.5'
                
    @pytest.mark.integration
    def test_performance_metrics_export_integration(self):
        """Test integration with performance metrics data source."""
        from nano_agent.modules.token_tracking import TokenTracker
        
        # Mock performance data
        performance_data = [
            {
                "metric_name": "response_time",
                "value": 1.234,
                "unit": "seconds",
                "provider": "anthropic",
                "model": "claude-sonnet-4",
                "timestamp": datetime.now(),
                "metadata": {"endpoint": "/v1/chat"}
            },
            {
                "metric_name": "tokens_per_second",
                "value": 45.6,
                "unit": "tokens/sec",
                "provider": "openai",
                "model": "gpt-5-mini",
                "timestamp": datetime.now(),
                "metadata": {"request_type": "completion"}
            }
        ]
        
        export_request = ExportRequest(
            export_type="performance_metrics",
            date_from=datetime.now() - timedelta(hours=1),
            date_to=datetime.now(),
            fields=["metric_name", "value", "provider", "model"]
        )
        
        with patch('nano_agent.data.get_performance_metrics') as mock_get_perf:
            mock_get_perf.return_value = performance_data
            
            export_result = self.export_service.create_export(export_request)
            
            # Verify CSV structure and content
            with open(export_result.file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                
                assert len(rows) == 2
                assert any(row['provider'] == 'anthropic' for row in rows)
                assert any(row['provider'] == 'openai' for row in rows)
                assert any(row['metric_name'] == 'response_time' for row in rows)
                
    @pytest.mark.integration
    def test_large_dataset_streaming_integration(self):
        """Test streaming export with large dataset."""
        # Generate large dataset
        def large_data_generator():
            for i in range(10000):
                yield {
                    "id": i,
                    "timestamp": (datetime.now() - timedelta(seconds=i)).isoformat(),
                    "value": f"data_value_{i}",
                    "category": f"cat_{i % 10}"
                }
                
        export_request = ExportRequest(
            export_type="agent_interactions",
            date_from=datetime.now() - timedelta(hours=24),
            date_to=datetime.now(),
            fields=["id", "timestamp", "value", "category"]
        )
        
        with patch('nano_agent.data.get_agent_interactions') as mock_get_interactions:
            mock_get_interactions.return_value = large_data_generator()
            
            export_result = self.export_service.create_export(export_request)
            
            # Verify file was created and has reasonable size
            assert os.path.exists(export_result.file_path)
            file_size = os.path.getsize(export_result.file_path)
            assert file_size > 100000  # Should be substantial file
            
            # Verify we can read the file without memory issues
            row_count = 0
            with open(export_result.file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    row_count += 1
                    if row_count == 1:  # Check first row structure
                        assert 'id' in row
                        assert 'timestamp' in row
                        assert 'value' in row
                        assert 'category' in row
                        
            assert row_count == 10000
            
    @pytest.mark.integration
    def test_privacy_filtering_integration(self):
        """Test privacy filtering in complete workflow."""
        sensitive_data = [
            {
                "user_id": "user123",
                "api_key": "sk-secret123",
                "request": "Hello world",
                "response": "Hi there!",
                "session_token": "session_abc",
                "public_metric": "response_time_ms"
            }
        ]
        
        export_request = ExportRequest(
            export_type="agent_interactions",
            date_from=datetime.now() - timedelta(hours=1),
            date_to=datetime.now(),
            privacy_level="public",
            fields=["user_id", "request", "response", "public_metric"]
        )
        
        with patch('nano_agent.data.get_agent_interactions') as mock_get_data:
            mock_get_data.return_value = sensitive_data
            
            export_result = self.export_service.create_export(export_request)
            
            # Read and verify sensitive data was filtered
            with open(export_result.file_path, 'r') as csvfile:
                content = csvfile.read()
                
                # Should not contain sensitive fields
                assert 'api_key' not in content
                assert 'session_token' not in content
                assert 'sk-secret123' not in content
                assert 'session_abc' not in content
                
                # Should contain allowed fields
                assert 'user_id' in content
                assert 'request' in content
                assert 'response' in content
                assert 'public_metric' in content
```

### 2. CLI Integration Tests (`tests/integration/test_cli_export.py`)

```python
import pytest
import tempfile
import os
from click.testing import CliRunner
from unittest.mock import patch, Mock

from nano_agent.cli.export_commands import export_cli

class TestCLIExportIntegration:
    
    def setup_method(self):
        """Setup CLI test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Cleanup CLI test environment."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            
    @pytest.mark.integration
    def test_cli_evaluation_export_command(self):
        """Test CLI command for exporting evaluation results."""
        output_file = os.path.join(self.temp_dir, "evaluations.csv")
        
        with patch('nano_agent.data.get_evaluation_results') as mock_get_data:
            mock_get_data.return_value = [
                {
                    "test_id": "test_001",
                    "model_name": "gpt-5-mini",
                    "success": True,
                    "score": 95.5
                }
            ]
            
            result = self.runner.invoke(export_cli, [
                'evaluations',
                '--output', output_file,
                '--provider', 'openai',
                '--date-from', '2024-01-01',
                '--date-to', '2024-01-31'
            ])
            
            assert result.exit_code == 0
            assert "Export completed successfully" in result.output
            assert os.path.exists(output_file)
            
            # Verify file content
            with open(output_file, 'r') as f:
                content = f.read()
                assert "test_id,model_name,success,score" in content
                assert "test_001,gpt-5-mini,True,95.5" in content
                
    @pytest.mark.integration
    def test_cli_progress_tracking(self):
        """Test CLI progress tracking for large exports."""
        output_file = os.path.join(self.temp_dir, "large_export.csv")
        
        def slow_data_generator():
            import time
            for i in range(100):
                time.sleep(0.01)  # Simulate slow data generation
                yield {"id": i, "data": f"value_{i}"}
                
        with patch('nano_agent.data.get_agent_interactions') as mock_get_data:
            mock_get_data.return_value = slow_data_generator()
            
            result = self.runner.invoke(export_cli, [
                'interactions',
                '--output', output_file,
                '--progress'
            ])
            
            assert result.exit_code == 0
            assert "Progress:" in result.output or "%" in result.output
            assert os.path.exists(output_file)
            
    @pytest.mark.integration
    def test_cli_field_selection(self):
        """Test CLI field selection and mapping."""
        output_file = os.path.join(self.temp_dir, "selected_fields.csv")
        
        with patch('nano_agent.data.get_evaluation_results') as mock_get_data:
            mock_get_data.return_value = [
                {
                    "test_id": "test_001",
                    "model_name": "gpt-5-mini",
                    "success": True,
                    "score": 95.5,
                    "internal_field": "should_not_appear",
                    "execution_time": 1.25
                }
            ]
            
            result = self.runner.invoke(export_cli, [
                'evaluations',
                '--output', output_file,
                '--fields', 'test_id,model_name,score'
            ])
            
            assert result.exit_code == 0
            
            with open(output_file, 'r') as f:
                content = f.read()
                # Should only contain selected fields
                assert "test_id" in content
                assert "model_name" in content
                assert "score" in content
                # Should not contain excluded fields
                assert "internal_field" not in content
                assert "execution_time" not in content
                
    @pytest.mark.integration
    def test_cli_error_handling(self):
        """Test CLI error handling and user feedback."""
        # Test with invalid date format
        result = self.runner.invoke(export_cli, [
            'evaluations',
            '--date-from', 'invalid-date',
            '--date-to', '2024-01-31'
        ])
        
        assert result.exit_code != 0
        assert "date format" in result.output.lower() or "invalid" in result.output.lower()
        
        # Test with invalid output directory
        invalid_output = "/nonexistent/directory/file.csv"
        result = self.runner.invoke(export_cli, [
            'evaluations',
            '--output', invalid_output
        ])
        
        assert result.exit_code != 0
        assert "directory" in result.output.lower() or "path" in result.output.lower()
```

## Edge Cases and Error Scenarios

### 1. Error Handling Tests (`tests/unit/test_error_scenarios.py`)

```python
import pytest
import tempfile
import os
from unittest.mock import Mock, patch
from io import StringIO

from nano_agent.modules.csv_exporter import CSVExporter, CSVExportConfig
from nano_agent.modules.export_models import ExportRequest
from nano_agent.exceptions import ExportError, DataValidationError, SecurityError

class TestErrorScenarios:
    
    def setup_method(self):
        """Setup test fixtures for error scenario testing."""
        self.config = CSVExportConfig()
        self.exporter = CSVExporter(self.config)
        
    def test_disk_space_exhaustion(self):
        """Test handling of disk space exhaustion during export."""
        large_data = [{"field": "x" * 1000} for _ in range(10000)]
        
        with patch('builtins.open', side_effect=OSError("No space left on device")):
            with pytest.raises(ExportError) as exc_info:
                self.exporter.export_to_file(large_data, "/tmp/test.csv")
                
            assert "disk space" in str(exc_info.value).lower()
            
    def test_permission_denied_file_write(self):
        """Test handling of permission denied errors."""
        data = [{"test": "data"}]
        
        with patch('builtins.open', side_effect=PermissionError("Permission denied")):
            with pytest.raises(ExportError) as exc_info:
                self.exporter.export_to_file(data, "/root/test.csv")
                
            assert "permission" in str(exc_info.value).lower()
            
    def test_malformed_data_handling(self):
        """Test handling of malformed or corrupted data."""
        malformed_data = [
            {"valid_field": "good_data"},
            {"unexpected_structure": {"nested": "data"}},
            None,  # Null record
            {"field_with_null_value": None}
        ]
        
        output = StringIO()
        
        # Should handle gracefully without crashing
        self.exporter.export_to_stream(malformed_data, output)
        result = output.getvalue()
        
        # Should contain valid data
        assert "valid_field" in result
        assert "good_data" in result
        
    def test_encoding_errors(self):
        """Test handling of encoding issues with special characters."""
        problematic_data = [
            {"text": "Normal text"},
            {"text": "Émojis 🚀 and unicode ñoño"},
            {"text": "Binary data: \x00\x01\x02"},
            {"text": "Mixed encoding: café résumé naïve"}
        ]
        
        output = StringIO()
        
        # Should handle encoding issues gracefully
        try:
            self.exporter.export_to_stream(problematic_data, output)
            result = output.getvalue()
            
            # Should preserve readable characters
            assert "Normal text" in result
            assert "café" in result or "caf" in result  # May be sanitized
            
        except UnicodeError:
            pytest.fail("CSV exporter should handle encoding issues gracefully")
            
    def test_memory_pressure_scenarios(self):
        """Test behavior under memory pressure conditions."""
        def memory_intensive_generator():
            # Simulate memory pressure by creating large objects
            for i in range(1000):
                yield {"data": "x" * 10000, "index": i}
                
        with patch('psutil.virtual_memory') as mock_memory:
            # Simulate low memory condition
            mock_memory.return_value.percent = 95  # 95% memory usage
            
            output = StringIO()
            
            # Should handle memory pressure gracefully
            try:
                self.exporter.export_generator_to_stream(
                    memory_intensive_generator(), 
                    output
                )
            except MemoryError:
                pytest.fail("Exporter should handle memory pressure gracefully")
                
    def test_concurrent_access_conflicts(self):
        """Test handling of concurrent file access conflicts."""
        data = [{"test": "concurrent_data"}]
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.close()
        
        try:
            # Simulate file lock by another process
            with patch('builtins.open', side_effect=OSError("Resource temporarily unavailable")):
                with pytest.raises(ExportError) as exc_info:
                    self.exporter.export_to_file(data, temp_file.name)
                    
                assert "resource" in str(exc_info.value).lower() or "lock" in str(exc_info.value).lower()
                
        finally:
            if os.path.exists(temp_file.name):
                os.unlink(temp_file.name)
                
    def test_network_timeout_during_data_fetch(self):
        """Test handling of network timeouts during data retrieval."""
        from nano_agent.api.export_routes import ExportService
        
        export_service = ExportService()
        
        export_request = ExportRequest(
            export_type="evaluation_results",
            date_from="2024-01-01T00:00:00",
            date_to="2024-01-31T23:59:59"
        )
        
        with patch('nano_agent.data.get_evaluation_results', side_effect=TimeoutError("Network timeout")):
            with pytest.raises(ExportError) as exc_info:
                export_service.create_export(export_request)
                
            assert "timeout" in str(exc_info.value).lower()
            
    def test_invalid_field_references(self):
        """Test handling of references to non-existent fields."""
        data = [
            {"existing_field": "value1"},
            {"existing_field": "value2"}
        ]
        
        # Try to map non-existent field
        from nano_agent.modules.export_models import FieldMapping
        
        invalid_mapping = FieldMapping({
            "existing_field": "Existing",
            "nonexistent_field": "Should Not Appear"
        })
        
        output = StringIO()
        
        # Should handle gracefully, only export existing fields
        self.exporter.export_to_stream(
            data, output, 
            field_mapping=invalid_mapping
        )
        
        result = output.getvalue()
        lines = result.strip().split('\n')
        
        # Should only have existing field header
        assert "Existing" in lines[0]
        assert "Should Not Appear" not in lines[0]
        
    def test_data_type_conversion_failures(self):
        """Test handling of data that cannot be converted to CSV format."""
        from datetime import datetime
        import decimal
        
        problematic_data = [
            {
                "good_field": "string_value",
                "complex_object": {"nested": {"deep": "value"}},
                "decimal_field": decimal.Decimal("123.456"),
                "datetime_field": datetime.now(),
                "function_field": lambda x: x + 1,  # Not serializable
                "circular_ref": None
            }
        ]
        
        # Create circular reference
        problematic_data[0]["circular_ref"] = problematic_data[0]
        
        output = StringIO()
        
        # Should handle conversion failures gracefully
        self.exporter.export_to_stream(problematic_data, output)
        result = output.getvalue()
        
        # Should contain convertible data
        assert "good_field" in result
        assert "string_value" in result
        
        # Should handle problematic fields (convert or exclude)
        # The exact behavior depends on implementation choice
        assert len(result) > 0  # Should produce some output
        
    def test_security_breach_attempts(self):
        """Test security measures against malicious export requests."""
        from nano_agent.api.export_routes import ExportService
        
        export_service = ExportService()
        
        # Attempt to export sensitive system data
        malicious_request = ExportRequest(
            export_type="evaluation_results",
            date_from="2024-01-01T00:00:00", 
            date_to="2024-01-31T23:59:59",
            fields=["api_key", "password", "secret_token", "private_data"]
        )
        
        with patch('nano_agent.auth.verify_field_access') as mock_verify:
            # Simulate security check failure
            mock_verify.side_effect = SecurityError("Access denied to sensitive fields")
            
            with pytest.raises(SecurityError) as exc_info:
                export_service.create_export(malicious_request)
                
            assert "access denied" in str(exc_info.value).lower()
```

## Performance and Load Tests

### 1. Performance Benchmarks (`tests/performance/test_export_performance.py`)

```python
import pytest
import time
import psutil
import os
from datetime import datetime, timedelta
from unittest.mock import patch

from nano_agent.modules.csv_exporter import CSVExporter, CSVExportConfig
from nano_agent.api.export_routes import ExportService

class TestExportPerformance:
    
    @pytest.mark.performance
    def test_large_dataset_export_performance(self):
        """Test export performance with large datasets."""
        # Generate 100K records
        large_dataset = [
            {
                "id": i,
                "timestamp": datetime.now() - timedelta(seconds=i),
                "value": f"data_value_{i}",
                "score": i * 0.01,
                "provider": f"provider_{i % 3}",
                "model": f"model_{i % 5}"
            }
            for i in range(100000)
        ]
        
        config = CSVExportConfig(streaming_chunk_size=5000)
        exporter = CSVExporter(config)
        
        start_time = time.time()
        start_memory = psutil.Process().memory_info().rss
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as temp_file:
            exporter.export_to_file(large_dataset, temp_file.name)
            
            end_time = time.time()
            end_memory = psutil.Process().memory_info().rss
            
            execution_time = end_time - start_time
            memory_delta = end_memory - start_memory
            
            # Performance assertions
            assert execution_time < 30.0  # Should complete in under 30 seconds
            assert memory_delta < 500 * 1024 * 1024  # Less than 500MB memory increase
            
            # Verify file was created correctly
            assert os.path.exists(temp_file.name)
            file_size = os.path.getsize(temp_file.name)
            assert file_size > 1000000  # Should be substantial file
            
    @pytest.mark.performance  
    def test_concurrent_export_performance(self):
        """Test performance under concurrent export load."""
        import threading
        import concurrent.futures
        
        def create_export_job(job_id):
            """Simulate concurrent export job."""
            data = [
                {"job_id": job_id, "index": i, "data": f"job_{job_id}_data_{i}"}
                for i in range(1000)
            ]
            
            config = CSVExportConfig()
            exporter = CSVExporter(config)
            
            with tempfile.NamedTemporaryFile(mode='w+', suffix=f'_job_{job_id}.csv') as temp_file:
                start_time = time.time()
                exporter.export_to_file(data, temp_file.name)
                end_time = time.time()
                
                return {
                    "job_id": job_id,
                    "execution_time": end_time - start_time,
                    "file_size": os.path.getsize(temp_file.name)
                }
        
        # Run 10 concurrent export jobs
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_export_job, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
        total_time = time.time() - start_time
        
        # Performance assertions
        assert total_time < 15.0  # All jobs should complete in under 15 seconds
        assert len(results) == 10  # All jobs should complete successfully
        
        # Check individual job performance
        for result in results:
            assert result["execution_time"] < 5.0  # Each job under 5 seconds
            assert result["file_size"] > 1000  # Reasonable file size
            
    @pytest.mark.performance
    def test_memory_usage_streaming(self):
        """Test memory usage remains constant during streaming."""
        def large_data_generator():
            for i in range(50000):
                yield {
                    "index": i,
                    "large_text": "x" * 1000,  # 1KB per record
                    "timestamp": datetime.now().isoformat()
                }
        
        config = CSVExportConfig(streaming_chunk_size=1000)
        exporter = CSVExporter(config)
        
        memory_samples = []
        
        def monitor_memory():
            """Monitor memory usage during export."""
            while True:
                memory_samples.append(psutil.Process().memory_info().rss)
                time.sleep(0.1)
                
        # Start memory monitoring
        import threading
        monitor_thread = threading.Thread(target=monitor_memory, daemon=True)
        monitor_thread.start()
        
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv') as temp_file:
            exporter.export_generator_to_file(large_data_generator(), temp_file.name)
            
        time.sleep(0.5)  # Allow final memory sample
        
        # Analyze memory usage
        if len(memory_samples) > 10:
            max_memory = max(memory_samples)
            min_memory = min(memory_samples)
            memory_variance = max_memory - min_memory
            
            # Memory should not grow substantially during streaming
            assert memory_variance < 100 * 1024 * 1024  # Less than 100MB variance
            
    @pytest.mark.performance
    def test_api_response_times(self):
        """Test API endpoint response times under load."""
        from fastapi.testclient import TestClient
        from nano_agent.api.export_routes import ExportRouter
        
        router = ExportRouter()
        client = TestClient(router.app)
        
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59",
            "fields": ["test_id", "model_name", "score"]
        }
        
        response_times = []
        
        # Test multiple requests
        for _ in range(20):
            start_time = time.time()
            
            with patch('nano_agent.data.get_evaluation_results') as mock_get_data:
                mock_get_data.return_value = [
                    {"test_id": f"test_{i}", "model_name": "gpt-5", "score": 95}
                    for i in range(100)
                ]
                
                response = client.post("/api/exports/create", json=request_data)
                
            end_time = time.time()
            response_times.append(end_time - start_time)
            
            assert response.status_code == 202
            
        # Performance assertions
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        
        assert avg_response_time < 1.0  # Average under 1 second
        assert max_response_time < 2.0  # Max under 2 seconds
        assert len([t for t in response_times if t < 0.5]) > 15  # 75% under 0.5 seconds
```

## Test Environment Setup

### 1. Test Configuration (`tests/conftest.py`)

```python
import pytest
import tempfile
import shutil
import os
from unittest.mock import Mock, patch

@pytest.fixture(scope="session")
def test_data_dir():
    """Create temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)
    
@pytest.fixture
def mock_auth():
    """Mock authentication for testing."""
    with patch('nano_agent.auth.verify_token') as mock_verify:
        mock_verify.return_value = {"user_id": "test_user", "permissions": ["export"]}
        yield mock_verify
        
@pytest.fixture
def sample_evaluation_data():
    """Sample evaluation data for testing."""
    from datetime import datetime, timedelta
    
    return [
        {
            "test_id": "test_001",
            "model_name": "gpt-5-mini",
            "provider": "openai",
            "success": True,
            "score": 95.5,
            "execution_time": 1.25,
            "tokens_used": 150,
            "cost": 0.002,
            "timestamp": datetime.now() - timedelta(hours=1)
        },
        {
            "test_id": "test_002",
            "model_name": "claude-sonnet-4", 
            "provider": "anthropic",
            "success": False,
            "score": 0.0,
            "execution_time": 0.5,
            "tokens_used": 75,
            "cost": 0.001,
            "timestamp": datetime.now() - timedelta(minutes=30),
            "error_message": "API timeout"
        }
    ]
    
@pytest.fixture
def mock_data_sources():
    """Mock data source functions."""
    with patch('nano_agent.data.get_evaluation_results') as mock_eval, \
         patch('nano_agent.data.get_performance_metrics') as mock_perf, \
         patch('nano_agent.data.get_agent_interactions') as mock_interact:
        
        yield {
            'evaluations': mock_eval,
            'performance': mock_perf,
            'interactions': mock_interact
        }
```

### 2. Test Data Factories (`tests/factories.py`)

```python
from datetime import datetime, timedelta
import random
from typing import List, Dict, Any

class TestDataFactory:
    """Factory for generating test data."""
    
    @staticmethod
    def create_evaluation_results(count: int = 10) -> List[Dict[str, Any]]:
        """Create sample evaluation results."""
        providers = ["openai", "anthropic", "ollama"]
        models = ["gpt-5-mini", "claude-sonnet-4", "llama-3"]
        
        results = []
        for i in range(count):
            provider = random.choice(providers)
            model = random.choice(models)
            success = random.choice([True, False, True, True])  # 75% success rate
            
            results.append({
                "test_id": f"test_{i:03d}",
                "model_name": model,
                "provider": provider,
                "success": success,
                "score": round(random.uniform(0, 100), 1) if success else 0.0,
                "execution_time": round(random.uniform(0.5, 5.0), 2),
                "tokens_used": random.randint(50, 500),
                "cost": round(random.uniform(0.001, 0.01), 4),
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 168)),
                "error_message": None if success else "Test error message"
            })
            
        return results
        
    @staticmethod
    def create_performance_metrics(count: int = 20) -> List[Dict[str, Any]]:
        """Create sample performance metrics."""
        metrics = ["response_time", "tokens_per_second", "memory_usage", "cpu_usage"]
        providers = ["openai", "anthropic", "ollama"]
        
        results = []
        for i in range(count):
            metric = random.choice(metrics)
            provider = random.choice(providers)
            
            # Generate realistic values based on metric type
            if metric == "response_time":
                value = round(random.uniform(0.5, 3.0), 3)
                unit = "seconds"
            elif metric == "tokens_per_second":
                value = round(random.uniform(20.0, 100.0), 1)
                unit = "tokens/sec"
            elif metric == "memory_usage":
                value = round(random.uniform(100.0, 1000.0), 1)
                unit = "MB"
            else:  # cpu_usage
                value = round(random.uniform(10.0, 80.0), 1)
                unit = "percent"
                
            results.append({
                "metric_name": metric,
                "value": value,
                "unit": unit,
                "provider": provider,
                "model": f"model_{provider}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(1, 1440)),
                "metadata": {"endpoint": f"/v1/{metric}", "region": "us-east-1"}
            })
            
        return results
```

## Mock Strategy

### 1. External Dependencies Mocking (`tests/mocks/external_deps.py`)

```python
from unittest.mock import Mock, patch
import contextlib

class MockDataSources:
    """Mock external data sources for testing."""
    
    @contextlib.contextmanager
    def mock_database_queries():
        """Mock database query functions."""
        with patch('nano_agent.data.database.query_evaluation_results') as mock_query:
            mock_query.return_value = []
            yield mock_query
            
    @contextlib.contextmanager  
    def mock_file_system():
        """Mock file system operations."""
        with patch('os.path.exists') as mock_exists, \
             patch('os.makedirs') as mock_makedirs, \
             patch('os.unlink') as mock_unlink:
            
            mock_exists.return_value = True
            yield {
                'exists': mock_exists,
                'makedirs': mock_makedirs,
                'unlink': mock_unlink
            }
            
    @contextlib.contextmanager
    def mock_authentication():
        """Mock authentication and authorization."""
        with patch('nano_agent.auth.verify_token') as mock_verify, \
             patch('nano_agent.auth.check_permissions') as mock_perms:
            
            mock_verify.return_value = {"user_id": "test_user"}
            mock_perms.return_value = True
            
            yield {
                'verify': mock_verify,
                'permissions': mock_perms
            }
```

## Coverage Requirements and Success Criteria

### Coverage Thresholds
- **Unit Tests**: 95% line coverage, 90% branch coverage
- **Integration Tests**: 85% integration point coverage
- **End-to-End Tests**: 100% critical path coverage

### Success Criteria

#### Functional Requirements
- ✅ Export evaluation results to CSV format with configurable fields
- ✅ Support filtering by date range, provider, model, and success status
- ✅ Handle large datasets (>100K records) efficiently with streaming
- ✅ Provide progress tracking for long-running operations
- ✅ Implement field mapping and privacy filtering
- ✅ Support multiple export types (evaluations, performance, interactions)

#### Performance Requirements
- ✅ Export 10,000 records in under 30 seconds
- ✅ Support 10 concurrent export operations without degradation
- ✅ Memory usage under 500MB for any single export operation
- ✅ 99.9% export success rate under normal conditions
- ✅ API response times under 2 seconds for export requests

#### Security Requirements
- ✅ No sensitive data (API keys, tokens) in exports without explicit permission
- ✅ All export operations require valid authentication
- ✅ Field-level access control based on user permissions
- ✅ Complete audit trail for all export activities
- ✅ Secure temporary file handling with automatic cleanup

#### Quality Requirements
- ✅ Comprehensive error handling with meaningful messages
- ✅ Graceful handling of malformed or missing data
- ✅ Proper encoding support for international characters
- ✅ Configurable CSV formatting options
- ✅ Robust validation of all input parameters

## TDD Implementation Order

### Red-Green-Refactor Cycles

1. **Phase 1: Core Engine (Week 1)**
   - Write failing tests for CSV export utilities
   - Implement minimal CSV generation functionality
   - Refactor for streaming and performance

2. **Phase 2: Data Models (Week 1-2)**
   - Write failing tests for data validation
   - Implement Pydantic models and validation
   - Refactor for extensibility and type safety

3. **Phase 3: API Integration (Week 2)**
   - Write failing tests for REST endpoints
   - Implement FastAPI routes and middleware
   - Refactor for proper error handling

4. **Phase 4: CLI Interface (Week 2-3)**
   - Write failing tests for CLI commands
   - Implement Click-based command interface
   - Refactor for usability and help text

5. **Phase 5: Security & Performance (Week 3-4)**
   - Write failing tests for security controls
   - Implement authentication and authorization
   - Refactor for performance optimization

### Validation Strategy

Each TDD cycle must include:
- **Red Phase**: Failing test that specifies exact behavior
- **Green Phase**: Minimal implementation to pass the test
- **Refactor Phase**: Code improvement while maintaining green tests
- **Integration Validation**: Tests pass in combination with existing code
- **Performance Validation**: Performance benchmarks remain within targets

## Test Execution Strategy

### Local Development
```bash
# Run all unit tests
pytest tests/unit/ -v

# Run integration tests  
pytest tests/integration/ -v --integration

# Run performance tests
pytest tests/performance/ -v --performance

# Run with coverage
pytest tests/ --cov=nano_agent --cov-report=html
```

### CI/CD Pipeline
```bash
# Fast feedback loop (unit tests only)
pytest tests/unit/ -x --tb=short

# Full test suite with parallel execution
pytest tests/ -n auto --dist=worksteal

# Performance regression testing
pytest tests/performance/ --benchmark-only
```

### Quality Gates
- All tests must pass before merge
- Coverage thresholds must be maintained
- Performance benchmarks must not regress by >10%
- Security tests must pass with zero vulnerabilities
- Integration tests must pass against live data sources

This comprehensive test strategy ensures robust, secure, and performant CSV export functionality that meets all requirements while following strict TDD principles.