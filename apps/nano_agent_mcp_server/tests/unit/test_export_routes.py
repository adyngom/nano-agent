import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi.testclient import TestClient
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import tempfile
import os

from nano_agent.api.export_routes import router
from nano_agent.modules.export_models import ExportRequest, ExportMetadata


@pytest.fixture
def client():
    """Create test client for API endpoints."""
    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router, prefix="/api/exports")
    return TestClient(app)


class TestExportRoutes:
    
    @patch('nano_agent.modules.csv_exporter.CSVExporter')
    @patch('nano_agent.api.export_routes.get_evaluation_data')
    @patch('nano_agent.api.export_routes.get_user_active_exports')
    def test_export_evaluation_results_endpoint(self, mock_active, mock_get_data, mock_exporter, client):
        """Test API endpoint for exporting evaluation results."""
        mock_active.return_value = 0  # Don't trigger rate limit
        mock_exporter_instance = Mock()
        mock_exporter.return_value = mock_exporter_instance
        
        mock_get_data.return_value = [
            {"test_id": "test1", "model_name": "gpt-5", "score": 95},
            {"test_id": "test2", "model_name": "gpt-5-mini", "score": 87}
        ]
        
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59",
            "filters": {"provider": "openai"},
            "fields": ["test_id", "model_name", "score"]
        }
        
        response = client.post("/api/exports/create", json=request_data)
        
        assert response.status_code == 202  # Accepted for async processing
        response_data = response.json()
        assert "export_id" in response_data
        assert "download_url" in response_data
        
    def test_export_request_validation(self, client):
        """Test validation of export request parameters."""
        # Missing required fields
        invalid_request = {
            "export_type": "evaluation_results"
            # Missing date_from, date_to
        }
        
        response = client.post("/api/exports/create", json=invalid_request)
        assert response.status_code == 422  # Validation error
        
        # Invalid export type
        invalid_type_request = {
            "export_type": "invalid_type",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59"
        }
        
        response = client.post("/api/exports/create", json=invalid_type_request)
        assert response.status_code == 422
        
    @patch('nano_agent.api.export_routes.verify_token')
    @patch('nano_agent.api.export_routes.get_user_active_exports')
    def test_authentication_required(self, mock_active, mock_verify, client):
        """Test that authentication is required for export endpoints."""
        mock_verify.side_effect = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
        mock_active.return_value = 0  # Don't trigger rate limit
        
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59"
        }
        
        response = client.post(
            "/api/exports/create", 
            json=request_data,
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
        
    @patch('nano_agent.api.export_routes.check_export_permissions')
    @patch('nano_agent.api.export_routes.get_user_active_exports')
    def test_authorization_for_sensitive_data(self, mock_active, mock_check_perms, client):
        """Test authorization for exporting sensitive data."""
        mock_check_perms.return_value = False  # Insufficient permissions
        mock_active.return_value = 0  # Don't trigger rate limit
        
        sensitive_request = {
            "export_type": "agent_interactions",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59",
            "privacy_level": "internal"
        }
        
        response = client.post("/api/exports/create", json=sensitive_request)
        assert response.status_code == 403  # Forbidden
        
    @patch('nano_agent.api.export_routes.get_export_status')
    def test_export_status_endpoint(self, mock_status, client):
        """Test checking export job status."""
        export_id = "export_12345"
        
        mock_status.return_value = {
            "export_id": export_id,
            "status": "completed",
            "progress": 100,
            "download_url": f"/api/exports/{export_id}/download",
            "created_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat()
        }
        
        response = client.get(f"/api/exports/{export_id}/status")
        
        assert response.status_code == 200
        data = response.json()
        assert data["export_id"] == export_id
        assert data["status"] == "completed"
        assert data["progress"] == 100
        
    @patch('nano_agent.api.export_routes.get_export_file_path')
    def test_export_download_endpoint(self, mock_path, client):
        """Test downloading completed export file."""
        export_id = "export_12345"
        
        # Create temporary CSV file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_file.write("test_id,model_name,score\n")
            temp_file.write("test1,gpt-5,95\n")
            temp_file.write("test2,gpt-5-mini,87\n")
            temp_file_path = temp_file.name
            
        try:
            mock_path.return_value = temp_file_path
            
            response = client.get(f"/api/exports/{export_id}/download")
            
            assert response.status_code == 200
            assert "text/csv" in response.headers["content-type"]
            assert "attachment; filename=" in response.headers["content-disposition"]
            
            # Verify content
            content = response.content.decode('utf-8')
            assert "test_id,model_name,score" in content
            assert "test1,gpt-5,95" in content
            
        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    @patch('nano_agent.api.export_routes.get_user_exports')
    def test_export_list_endpoint(self, mock_exports, client):
        """Test listing user's export history."""
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
        
        response = client.get("/api/exports/list")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["export_id"] == "export_001"
        assert data[1]["status"] == "processing"
        
    @patch('nano_agent.api.export_routes.estimate_export_size')
    @patch('nano_agent.api.export_routes.get_user_active_exports')
    def test_large_export_handling(self, mock_active, mock_estimate, client):
        """Test handling of large export requests."""
        mock_active.return_value = 0  # Don't trigger rate limit
        mock_estimate.return_value = 1000000  # 1M records
        
        large_request = {
            "export_type": "agent_interactions",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-12-31T23:59:59",  # Full year
            "filters": {}  # No filters = all data
        }
        
        response = client.post("/api/exports/create", json=large_request)
        
        # Should accept but warn about size
        assert response.status_code == 202
        data = response.json()
        assert "warning" in data
        assert "large dataset" in data["warning"].lower()
        
    @patch('nano_agent.api.export_routes.get_user_active_exports')
    def test_concurrent_export_limits(self, mock_active, client):
        """Test limits on concurrent exports per user."""
        request_data = {
            "export_type": "evaluation_results",
            "date_from": "2024-01-01T00:00:00",
            "date_to": "2024-01-31T23:59:59"
        }
        
        mock_active.return_value = 3  # Already at limit
        
        response = client.post("/api/exports/create", json=request_data)
        
        assert response.status_code == 429  # Too Many Requests
        data = response.json()
        assert "concurrent export limit" in data["detail"].lower()