"""
Delete contact endpoint for PostGrid API.

This module provides an API endpoint for deleting a contact by its ID.
"""
from __future__ import annotations

import re
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from ...client import PostGridClient
from ._exceptions import (
    APIError,
    AuthenticationError,
    PostGridAPIError,
    RateLimitError,
    ValidationError,
)
from ._responses import ContactDeleteResponse

# Regex pattern for contact ID validation
CONTACT_ID_PATTERN = r'^contact_[a-zA-Z0-9]+$'

async def delete_contact(
    contact_id: Annotated[
        str,
        Path(
            ...,
            description="The unique identifier of the contact to delete",
            example="contact_nA8mdzveShFEmFraaChaDn",
            regex=CONTACT_ID_PATTERN,
        ),
    ],
    postgrid: PostGridClient = Depends(),
) -> ContactDeleteResponse:
    """
    Delete a contact by its ID.

    Args:
        contact_id: The unique identifier of the contact to delete
        postgrid: Injected PostGrid client

    Returns:
        ContactDeleteResponse: Confirmation of deletion

    Raises:
        HTTPException: If the contact cannot be deleted
    """
    try:
        # Validate contact ID format
        if not re.match(CONTACT_ID_PATTERN, contact_id):
            raise ValidationError(
                400,
                PostGridAPIError(
                    type="invalid_request_error",
                    message=f"Invalid contact ID format: {contact_id}",
                ),
            )

        # Make the API request to delete the contact
        response = await postgrid.delete(f"contacts/{contact_id}")

        # Handle different status codes
        if response.status_code == 401:
            raise AuthenticationError("Invalid API key")
        if response.status_code == 404:
            raise APIError(
                404,
                PostGridAPIError(
                    type="not_found",
                    message="Contact not found"
                )
            )
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        if not response.is_success:
            raise APIError(f"PostGrid API error: {response.text}")

        # Parse and return the response
        return ContactDeleteResponse(**response.json())

    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e)) from e
    except APIError as e:
        raise HTTPException(
            status_code=500,
            detail="An error occurred while deleting the contact",
        ) from e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e