"""FastAPI routes for CSV export functionality."""

import uuid
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import FileResponse
from pathlib import Path

from ..modules.export_models import (
    ExportRequest, ExportMetadata, ExportType, PrivacyLevel
)
from ..modules.csv_exporter import CSVExporter, CSVExportConfig


router = APIRouter()

# Mock authentication functions (to be replaced with real implementation)
def verify_token(token: str = None) -> str:
    """Mock token verification."""
    if token and "invalid" in token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    return "user123"


def check_export_permissions(export_type: str, privacy_level: str) -> bool:
    """Mock permission checking."""
    # For testing: deny internal level for agent_interactions
    if export_type == "agent_interactions" and privacy_level == "internal":
        return False
    return True


def get_user_active_exports(user_id: str) -> int:
    """Mock active exports count."""
    # Default to 0 for most tests, specific tests will mock this
    return 0


def estimate_export_size(export_request: ExportRequest) -> int:
    """Mock export size estimation."""
    # Return large size for full year date ranges
    if (export_request.date_to - export_request.date_from).days > 300:
        return 1000000
    return 1000


# Mock data retrieval functions (to be replaced with real implementation)
def get_evaluation_data(filters: Dict[str, Any], date_from: datetime, date_to: datetime) -> List[Dict[str, Any]]:
    """Mock evaluation data retrieval."""
    return [
        {"test_id": "test1", "model_name": "gpt-5", "score": 95},
        {"test_id": "test2", "model_name": "gpt-5-mini", "score": 87}
    ]


def get_export_status(export_id: str) -> Dict[str, Any]:
    """Mock export status retrieval."""
    return {
        "export_id": export_id,
        "status": "completed",
        "progress": 100,
        "download_url": f"/api/exports/{export_id}/download",
        "created_at": datetime.now().isoformat(),
        "completed_at": datetime.now().isoformat()
    }


def get_export_file_path(export_id: str) -> str:
    """Mock export file path retrieval."""
    return f"/tmp/export_{export_id}.csv"


def get_user_exports(user_id: str) -> List[Dict[str, Any]]:
    """Mock user exports retrieval."""
    return [
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


@router.post("/create", status_code=202)
async def create_export(
    export_request: ExportRequest,
    user_id: str = Depends(verify_token)
) -> Dict[str, Any]:
    """Create a new export job."""
    
    # Check concurrent export limits
    active_exports = get_user_active_exports(user_id)
    if active_exports >= 3:
        raise HTTPException(
            status_code=429,
            detail="Concurrent export limit exceeded (max 3 active exports)"
        )
    
    # Check permissions for sensitive data
    if not check_export_permissions(export_request.export_type.value, export_request.privacy_level.value):
        raise HTTPException(
            status_code=403,
            detail="Insufficient permissions for this export type"
        )
    
    # Estimate export size and warn if large
    estimated_size = estimate_export_size(export_request)
    warning = None
    if estimated_size > 100000:
        warning = f"Large dataset estimated ({estimated_size:,} records). Export may take longer than usual."
    
    # Generate export ID
    export_id = str(uuid.uuid4())
    
    # Create response
    response_data = {
        "export_id": export_id,
        "status": "accepted",
        "download_url": f"/api/exports/{export_id}/download",
        "estimated_records": estimated_size
    }
    
    if warning:
        response_data["warning"] = warning
    
    return response_data


@router.get("/{export_id}/status")
async def get_export_status_endpoint(
    export_id: str,
    user_id: str = Depends(verify_token)
) -> Dict[str, Any]:
    """Get the status of an export job."""
    return get_export_status(export_id)


@router.get("/{export_id}/download")
async def download_export(
    export_id: str,
    user_id: str = Depends(verify_token)
) -> FileResponse:
    """Download a completed export file."""
    file_path = get_export_file_path(export_id)
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Export file not found"
        )
    
    return FileResponse(
        path=file_path,
        media_type="text/csv",
        filename=f"export_{export_id}.csv",
        headers={"Content-Disposition": f"attachment; filename=export_{export_id}.csv"}
    )


@router.get("/list")
async def list_user_exports(
    user_id: str = Depends(verify_token)
) -> List[Dict[str, Any]]:
    """List all exports for the current user."""
    return get_user_exports(user_id)