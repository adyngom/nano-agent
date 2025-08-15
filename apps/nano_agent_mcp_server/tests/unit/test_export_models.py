import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
from nano_agent.modules.export_models import (
    EvaluationResult, PerformanceMetric, 
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