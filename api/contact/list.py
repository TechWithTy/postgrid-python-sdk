"""
Core functionality for listing contacts from PostGrid.
This module contains the business logic for retrieving a paginated list of contacts.
"""
from __future__ import annotations

from typing import Any

from ...client import PostGridClient
from ._exceptions import (
    APIError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)
from ._responses import ContactListResponse


async def list_contacts(
    client: PostGridClient,
    *,
    skip: int = 0,
    limit: int = 10,
    search: str | None = None
) -> ContactListResponse:
    """Retrieve a paginated list of contacts with optional search.

    Args:
        client: An instance of the PostGrid client
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return (1-100)
        search: Optional search term to filter contacts

    Returns:
        ContactListResponse: A paginated list of contacts

    Raises:
        ValidationError: If request parameters are invalid
        AuthenticationError: If API key is invalid
        RateLimitError: If rate limit is exceeded
        APIError: For other API-related errors
    """
    # Validate parameters
    if skip < 0:
        raise ValidationError("Skip must be a non-negative integer")
    if not 1 <= limit <= 100:
        raise ValidationError("Limit must be between 1 and 100")

    # Build query parameters
    params: dict[str, Any] = {
        "skip": skip,
        "limit": limit,
    }
    if search:
        params["search"] = search

    # Make API request
    response = await client.get(
        "/print-mail/v1/contacts",
        params=params
    )

    # Handle the response
    if response.status_code == 200:
        return ContactListResponse.parse_obj(response.json())

    # Handle specific PostGrid API errors
    if response.status_code == 400:
        raise ValidationError("Invalid request parameters")
    if response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    if response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")
    
    raise APIError(f"PostGrid API error: {response.text}")