"""Cancel a letter in PostGrid with a note.

This module provides functionality to cancel a letter that hasn't been sent yet
and include a note explaining the reason for cancellation.
"""
from __future__ import annotations

from typing import Optional

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import LetterCancelError, LetterNotFoundError
from ._responses import LetterResponse


async def cancel_letter_with_note(
    client: PostGridClient,
    letter_id: str,
    note: str,
) -> LetterResponse:
    """Cancel a letter that hasn't been sent yet with a note.

    Args:
        client: An authenticated PostGrid client instance.
        letter_id: The ID of the letter to cancel (starts with 'letter_').
        note: The reason for cancellation (required, max 500 characters).

    Returns:
        The canceled letter details with cancellation information.

    Raises:
        ValueError: If the letter_id is invalid or note is empty.
        LetterNotFoundError: If the letter doesn't exist.
        LetterCancelError: If the letter couldn't be canceled.
    """
    if not letter_id or not isinstance(letter_id, str) or not letter_id.startswith("letter_"):
        raise ValueError("Invalid letter_id. Must be a string starting with 'letter_'.")
    
    if not note or not isinstance(note, str):
        raise ValueError("A non-empty note is required for cancellation.")
    
    if len(note) > 500:
        raise ValueError("Note must be 500 characters or less.")

    try:
        response = await client.post(
            f"letters/{letter_id}/cancellation",
            data={"note": note},
            response_model=LetterResponse,
        )
        return response

    except PostGridError as e:
        if "not_found" in str(e).lower():
            raise LetterNotFoundError(f"Letter with ID '{letter_id}' not found") from e
        if "already_canceled" in str(e).lower():
            raise LetterCancelError(f"Letter {letter_id} was already canceled") from e
        if "cannot_be_canceled" in str(e).lower():
            raise LetterCancelError(f"Letter {letter_id} cannot be canceled (may already be sent)") from e
        raise LetterCancelError(f"Failed to cancel letter: {str(e)}") from e