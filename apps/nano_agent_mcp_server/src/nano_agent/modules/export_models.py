"""Data models for CSV export functionality."""

from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, field_validator


class ExportType(str, Enum):
    """Valid export types."""
    EVALUATION_RESULTS = "evaluation_results"
    PERFORMANCE_METRICS = "performance_metrics"
    AGENT_INTERACTIONS = "agent_interactions"


class PrivacyLevel(str, Enum):
    """Privacy levels for exports."""
    PUBLIC = "public"
    INTERNAL = "internal"
    RESTRICTED = "restricted"
    STRICT = "strict"


class EvaluationResult(BaseModel):
    """Model for evaluation result data."""
    test_id: str
    model_name: str
    provider: str
    success: bool
    score: float
    execution_time: float
    tokens_used: int
    cost: float
    timestamp: datetime
    error_message: Optional[str] = None


class PerformanceMetric(BaseModel):
    """Model for performance metric data."""
    metric_name: str
    value: float
    unit: str
    provider: str
    model: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class AgentInteraction(BaseModel):
    """Model for agent interaction data."""
    session_id: str
    request_id: str
    user_prompt: str
    agent_response: str
    tools_used: List[str]
    provider: str
    model: str
    start_time: datetime
    end_time: datetime
    success: bool


class ExportRequest(BaseModel):
    """Model for export request validation."""
    export_type: ExportType
    date_from: datetime
    date_to: datetime
    filters: Optional[Dict[str, Any]] = None
    fields: Optional[List[str]] = None
    privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC
    
    @field_validator('date_to')
    @classmethod
    def validate_date_range(cls, v, info):
        if 'date_from' in info.data and v < info.data['date_from']:
            raise ValueError('date_to must be after date_from')
        return v


class ExportMetadata(BaseModel):
    """Model for tracking export metadata."""
    export_id: str
    requested_by: str
    export_type: str
    record_count: int
    file_size_bytes: int
    created_at: datetime
    privacy_level: str
    filters_applied: Optional[Dict[str, Any]] = None


class FieldMapping:
    """Field mapping for CSV exports with renaming and filtering."""
    
    def __init__(self, mapping: Dict[str, str]):
        self.mapping = mapping
    
    def apply_to_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply field mapping to data dictionary."""
        result = {}
        for old_field, new_field in self.mapping.items():
            if old_field in data:
                result[new_field] = data[old_field]
        return result


class PrivacyFilter:
    """Privacy filtering for sensitive data."""
    
    def __init__(
        self, 
        sensitive_fields: List[str], 
        redaction_text: str = "[REDACTED]",
        privacy_level: str = "public"
    ):
        self.sensitive_fields = sensitive_fields
        self.redaction_text = redaction_text
        self.privacy_level = privacy_level
    
    def apply_to_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Apply privacy filtering to data dictionary."""
        result = data.copy()
        for field in self.sensitive_fields:
            if field in result:
                result[field] = self.redaction_text
        return result