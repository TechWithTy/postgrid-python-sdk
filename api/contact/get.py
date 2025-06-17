"""
Core functionality for retrieving a contact from PostGrid.
This module contains the business logic for getting a contact by ID.
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
from ._responses import ContactResponse

async def get_contact(
    contact_id: str,
    client: PostGridClient
) -> ContactResponse:
    """Retrieve a specific contact by its ID.

    Args:
        contact_id: The unique identifier of the contact
        client: An instance of the PostGrid client

    Returns:
        ContactResponse: The requested contact details

    Raises:
        ValidationError: If the contact ID format is invalid
        AuthenticationError: If API key is invalid
        RateLimitError: If rate limit is exceeded
        APIError: For other API-related errors
    """
    # Make API request
    response = await client.get(f"/print-mail/v1/contacts/{contact_id}")

    # Handle the response
    if response.status_code == 200:
        return ContactResponse.parse_obj(response.json())

    # Handle specific PostGrid API errors
    if response.status_code == 400:
        raise ValidationError("Invalid contact ID format")
    if response.status_code == 401:
        raise AuthenticationError("Invalid API key")
    if response.status_code == 404:
        raise APIError("Contact not found")
    if response.status_code == 429:
        raise RateLimitError("Rate limit exceeded")
    
    raise APIError(f"PostGrid API error: {response.text}")