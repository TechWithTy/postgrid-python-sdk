# app/core/third_party_integrations/postgrid/api/route/_exceptions.py
from typing import Any, Dict, Optional

from pydantic import BaseModel

class PostGridAPIError(BaseModel):
    type: str
    message: str
    param: Optional[str] = None
    code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class PostGridAPIException(Exception):
    def __init__(
        self,
        status_code: int,
        error: PostGridAPIError,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        self.status_code = status_code
        self.error = error
        self.headers = headers or {}
        super().__init__(f"API error {status_code}: {error.message}")

class ValidationError(PostGridAPIException):
    """Raised when input validation fails."""
    pass

class AuthenticationError(PostGridAPIException):
    """Raised when authentication fails."""
    pass

class RateLimitError(PostGridAPIException):
    """Raised when rate limit is exceeded."""
    pass

class APIError(PostGridAPIException):
    """Raised for 5xx server errors."""
    pass