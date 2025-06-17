"""Retrieve a specific letter by ID from PostGrid.

This module provides functionality to fetch a single letter by its ID,
with optional expansion of related resources.
"""
from __future__ import annotations

from typing import Literal

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import LetterNotFoundError
from ._responses import LetterResponse

# Type alias for valid expand options
ExpandOption = Literal["template", "returnEnvelope"]


async def get_letter(
    client: PostGridClient,
    letter_id: str,
    *,
    expand: list[ExpandOption] | None = None,
) -> LetterResponse:
    """Retrieve a specific letter by its ID.

    Args:
        client: An authenticated PostGrid client instance.
        letter_id: The ID of the letter to retrieve (starts with 'letter_').
        expand: Optional list of related resources to expand in the response.
                Can include 'template' or 'returnEnvelope'.

    Returns:
        The requested letter details.

    Raises:
        ValueError: If the letter_id is invalid.
        LetterNotFoundError: If the letter with the given ID is not found.
        PostGridError: For other API-related errors.
    """
    # Validate letter_id format
    if not letter_id or not isinstance(letter_id, str) or not letter_id.startswith("letter_"):
        raise ValueError("Invalid letter_id. Must be a string starting with 'letter_'.")

    # Prepare query parameters
    params = {}
    if expand:
        # Convert list of expand options to the format expected by the API
        params["expand[]"] = list(expand)

    try:
        response = await client.get(
            f"letters/{letter_id}",
            params=params if params else None,
            response_model=LetterResponse,
        )
        return response
    except PostGridError as e:
        if "not found" in str(e).lower() or "does not exist" in str(e).lower():
            raise LetterNotFoundError(letter_id=letter_id) from e
        raise