"""Custom exceptions for the PostGrid Letter API."""
from __future__ import annotations

from ...client import PostGridAPIError


class LetterError(PostGridAPIError):
    """Base exception for all letter-related errors."""


class LetterNotFoundError(LetterError):
    """Raised when a letter cannot be found."""

    def __init__(self, letter_id: str, message: str | None = None) -> None:
        self.letter_id = letter_id
        msg = message or f"Letter with ID '{letter_id}' not found"
        super().__init__(msg)


class LetterCreateError(LetterError):
    """Raised when letter creation fails."""


class LetterUpdateError(LetterError):
    """Raised when updating a letter fails."""

    def __init__(self, letter_id: str, message: str | None = None) -> None:
        self.letter_id = letter_id
        msg = message or f"Failed to update letter with ID '{letter_id}'"
        super().__init__(msg)


class LetterDeleteError(LetterError):
    """Raised when deleting a letter fails."""

    def __init__(self, letter_id: str, message: str | None = None) -> None:
        self.letter_id = letter_id
        msg = message or f"Failed to delete letter with ID '{letter_id}'"
        super().__init__(msg)


class LetterListError(LetterError):
    """Raised when listing letters fails."""


class InvalidProgressionError(LetterError):
    """Raised when attempting to progress a letter to an invalid status."""
    
    def __init__(self, letter_id: str, current_status: str, message: str | None = None) -> None:
        self.letter_id = letter_id
        self.current_status = current_status
        msg = message or (
            f"Cannot progress letter with ID '{letter_id}'. "
            f"Current status is '{current_status}' which cannot be progressed further."
        )
        super().__init__(msg)


class LetterCancelError(LetterError):
    """Raised when a letter cannot be canceled."""
    
    def __init__(self, letter_id: str, message: str | None = None) -> None:
        self.letter_id = letter_id
        msg = message or f"Failed to cancel letter with ID '{letter_id}'"
        super().__init__(msg)