"""Secret contact creation endpoint for PostGrid API.

This module provides an API endpoint for creating and managing secret contacts in PostGrid.
Secret contacts have their PII (Personally Identifiable Information) redacted in the API responses.
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from ...client import PostGridClient
from ...services.contact_service import ContactService
from ._exceptions import (
    APIError,
    AuthenticationError,
    PostGridAPIException,
    RateLimitError,
    ValidationError,
)
from ._requests import ContactCreateRequest
from ._responses import ContactResponse

router = APIRouter(prefix="/contacts", tags=["secret-contacts"])


def get_contact_service(client: PostGridClient) -> ContactService:
    """Dependency that provides a ContactService instance.

    Args:
        client: The PostGrid client instance

    Returns:
        ContactService: An instance of the ContactService
    """
    return ContactService(client)



async def create_secret_contact(
    contact: ContactCreateRequest,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactResponse:
    """Create a new secret contact in PostGrid.

    Args:
        contact: The contact data to create
        contact_service: The ContactService instance

    Returns:
        ContactResponse: The created or updated contact

    Raises:
        HTTPException: If there's an error creating the contact
    """
    try:
        # Convert Pydantic model to dict and remove None values
        contact_dict = contact.dict(exclude_none=True, by_alias=True)

        # Mark as secret contact and create using the service
        contact_dict["secret"] = True
        return await contact_service.create_contact(contact_dict, secret=True)

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except AuthenticationError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except RateLimitError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except PostGridAPIException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e
