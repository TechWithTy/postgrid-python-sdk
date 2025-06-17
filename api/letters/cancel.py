"""Cancel a letter in PostGrid.

This module provides functionality to cancel a letter that hasn't been sent yet.
"""
from __future__ import annotations

from typing import Optional

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import LetterCancelError, LetterNotFoundError
from ._responses import LetterResponse


async def cancel_letter(
    client: PostGridClient,
    letter_id: str,
) -> Optional[LetterResponse]:
    """Cancel a letter that hasn't been sent yet.

    Args:
        client: An authenticated PostGrid client instance.
        letter_id: The ID of the letter to cancel (starts with 'letter_').

    Returns:
        The canceled letter details if successful, None if the letter was already canceled.

    Raises:
        ValueError: If the letter_id is invalid.
        LetterNotFoundError: If the letter doesn't exist.
        LetterCancelError: If the letter couldn't be canceled.
    """
    if not letter_id or not isinstance(letter_id, str) or not letter_id.startswith("letter_"):
        raise ValueError("Invalid letter_id. Must be a string starting with 'letter_'.")

    try:
        response = await client.delete(
            f"letters/{letter_id}",
            response_model=LetterResponse,
        )
        return response

    except PostGridError as e:
        if "not_found" in str(e).lower():
            raise LetterNotFoundError(f"Letter with ID '{letter_id}' not found") from e
        if "already_canceled" in str(e).lower():
            return None  # Letter was already canceled
        raise LetterCancelError(f"Failed to cancel letter: {str(e)}") from e