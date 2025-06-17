from ...client import PostGridAPIError

class PostcardError(PostGridAPIError):
    """Base exception for Postcard-related errors."""
    pass

class PostcardNotFoundError(PostcardError):
    """Raised when a postcard is not found."""
    pass

class PostcardValidationError(PostcardError):
    """Raised when postcard validation fails."""
    pass

class InvalidProgressionError(PostcardError):
    """Raised when attempting to progress a postcard with an invalid status."""
    pass

class AddressValidationError(PostcardError):
    """Raised when address validation fails."""
    pass

class PostcardCreationError(PostcardError):
    """Raised when there's an error creating a postcard."""
    pass