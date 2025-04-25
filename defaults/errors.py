from fastapi import HTTPException, status

class BaseAppError(HTTPException):
    """Base error class for application exceptions"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: str,
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail={
            "error_code": error_code,
            "message": message,
            "status": False
        })


class NotFoundError(BaseAppError):
    """Resource not found error"""
    
    def __init__(self, resource_type: str, resource_id: str):
        message = f"{resource_type} with id '{resource_id}' not found"
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_code="RESOURCE_NOT_FOUND",
        )


class ValidationError(BaseAppError):
    """Input validation error"""
    
    def __init__(self, message: str = "Invalid input"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            error_code="VALIDATION_ERROR",
        )


class AuthenticationError(BaseAppError):
    """Authentication error"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_code="AUTHENTICATION_ERROR",
        )


class AuthorizationError(BaseAppError):
    """Authorization error"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_code="AUTHORIZATION_ERROR",
        )


class ConflictError(BaseAppError):
    """Resource conflict error"""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="RESOURCE_CONFLICT",
        )


class RateLimitError(BaseAppError):
    """Rate limit exceeded error"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
        )


class ServerError(BaseAppError):
    """Internal server error"""
    
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_code="INTERNAL_SERVER_ERROR",
        )


class ServiceUnavailableError(BaseAppError):
    """Service unavailable error"""
    
    def __init__(self, message: str = "Service temporarily unavailable"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            message=message,
            error_code="SERVICE_UNAVAILABLE",
        )


class BadGatewayError(BaseAppError):
    """Bad gateway error"""
    
    def __init__(self, message: str = "Bad gateway"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            message=message,
            error_code="BAD_GATEWAY",
        )