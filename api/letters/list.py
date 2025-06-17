"""List and filter letter orders from PostGrid.

This module provides functionality to retrieve a paginated list of letters
with optional search and filtering capabilities.
"""
from __future__ import annotations

from typing import Any, Optional

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import LetterListError
from ._responses import LetterListResponse


async def list_letters(
    client: PostGridClient,
    *,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
) -> LetterListResponse:
    """Retrieve a paginated list of letter orders.

    Args:
        client: An authenticated PostGrid client instance.
        skip: Number of records to skip for pagination (default: 0).
        limit: Maximum number of records to return (1-100, default: 10).
        search: Optional search term to filter letters.

    Returns:
        A LetterListResponse containing the paginated list of letters.

    Raises:
        LetterListError: If there's an error listing the letters.
        ValueError: If pagination parameters are invalid.
    """
    # Validate pagination parameters
    if skip < 0:
        raise ValueError("skip must be a non-negative integer")
    if not (1 <= limit <= 100):
        raise ValueError("limit must be between 1 and 100")

    # Build query parameters
    params: dict[str, Any] = {
        "skip": skip,
        "limit": limit,
    }
    if search:
        params["search"] = search

    try:
        response = await client.get(
            "letters",
            params=params,
            response_model=LetterListResponse,
        )
        return response
    except PostGridError as e:
        raise LetterListError(f"Failed to list letters: {str(e)}") from e