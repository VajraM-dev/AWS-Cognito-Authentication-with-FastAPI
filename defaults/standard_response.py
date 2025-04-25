from typing import Dict, Any
from fastapi import status
from defaults.models import ApiResponse

# Helper functions to create standardized responses
def success_response(
    data: Any = None, 
    message: str = "Operation successful", 
    status_code: int = status.HTTP_200_OK, 
    meta: Dict[str, Any] = None
) -> ApiResponse:
    """Create a success response"""
    return ApiResponse(
        success=True,
        status_code=status_code,
        message=message,
        data=data,
        meta=meta
    )