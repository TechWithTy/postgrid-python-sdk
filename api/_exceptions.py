"""Global exceptions for the PostGrid API client."""
from __future__ import annotations

from typing import Any


class PostGridError(Exception):
    """Base exception for all PostGrid API errors."""
    
    def __init__(
        self,
        message: str = "An error occurred with the PostGrid API",
        status_code: int | None = None,
        response: Any = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the exception.
        
        Args:
            message: The error message
            status_code: HTTP status code
            response: The raw response from the API
            errors: List of error details
        """
        self.message = message
        self.status_code = status_code
        self.response = response
        self.errors = errors or []
        super().__init__(self.message)

    def __str__(self) -> str:
        """Return the string representation of the error."""
        if self.status_code:
            return f"{self.status_code}: {self.message}"
        return self.message


class PostGridAPIError(PostGridError):
    """Raised when the API returns an error response."""
    
    def __init__(
        self,
        message: str = "An unexpected error occurred with the PostGrid API",
        status_code: int | None = None,
        response: Any = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the exception."""
        super().__init__(message, status_code, response, errors)


class PostGridAuthenticationError(PostGridError):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        message: str = "Authentication failed. Please check your API key.",
        status_code: int | None = 401,
        response: Any = None,
    ) -> None:
        """Initialize the exception."""
        super().__init__(message, status_code, response)


class PostGridRateLimitError(PostGridError):
    """Raised when the rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded. Please wait before making more requests.",
        status_code: int | None = 429,
        response: Any = None,
        retry_after: int = 60,
    ) -> None:
        """Initialize the exception.
        
        Args:
            message: The error message
            status_code: HTTP status code
            response: The raw response from the API
            retry_after: Number of seconds to wait before retrying
        """
        self.retry_after = retry_after
        super().__init__(message, status_code, response)


class PostGridValidationError(PostGridError):
    """Raised when request validation fails."""
    
    def __init__(
        self,
        message: str = "Invalid request data",
        status_code: int | None = 400,
        response: Any = None,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        """Initialize the exception."""
        super().__init__(message, status_code, response, errors)


class PostGridNotFoundError(PostGridError):
    """Raised when a requested resource is not found."""
    
    def __init__(
        self,
        message: str = "The requested resource was not found",
        status_code: int | None = 404,
        response: Any = None,
    ) -> None:
        """Initialize the exception."""
        super().__init__(message, status_code, response)


class PostGridServerError(PostGridError):
    """Raised when the server encounters an error."""
    
    def __init__(
        self,
        message: str = "The server encountered an error",
        status_code: int | None = 500,
        response: Any = None,
    ) -> None:
        """Initialize the exception."""
        super().__init__(message, status_code, response)


class PostGridTimeoutError(PostGridError):
    """Raised when a request times out."""
    
    def __init__(
        self,
        message: str = "The request timed out",
        status_code: int | None = 504,
    ) -> None:
        """Initialize the exception."""
        super().__init__(message, status_code)


class PostGridNetworkError(PostGridError):
    """Raised when a network error occurs."""
    
    def __init__(
        self,
        message: str = "A network error occurred",
        original_exception: Exception | None = None,
    ) -> None:
        """Initialize the exception.
        
        Args:
            message: The error message
            original_exception: The original exception that was raised
        """
        self.original_exception = original_exception
        super().__init__(message)


class PostGridConfigurationError(PostGridError):
    """Raised when there is a configuration error."""
    
    def __init__(
        self,
        message: str = "Configuration error",
    ) -> None:
        """Initialize the exception."""
        super().__init__(message)