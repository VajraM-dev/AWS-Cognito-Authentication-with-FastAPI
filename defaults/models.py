from pydantic import BaseModel
from typing import TypeVar, Generic, Optional, Dict, Any, List

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str

T = TypeVar('T')
class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    success: bool
    status_code: int
    message: str
    data: Optional[T] = None
    meta: Optional[Dict[str, Any]] = None
    errors: Optional[List[Dict[str, Any]]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "status_code": 200,
                "message": "Operation successful",
                "data": {},
                "meta": {"page": 1, "limit": 10, "total": 100},
                "errors": None
            }
        }
