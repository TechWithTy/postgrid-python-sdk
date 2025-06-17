"""
Single-line address contact creation endpoint for PostGrid API.

This module provides an API endpoint for creating contacts with a single-line address.
PostGrid will automatically parse and verify the address.
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
from ._requests import SingleLineContactCreateRequest
from ._responses import ContactResponse

router = APIRouter(prefix="/contacts", tags=["contacts"])


def get_contact_service(client: PostGridClient) -> ContactService:
    """Dependency that provides a ContactService instance.

    Args:
        client: The PostGrid client instance

    Returns:
        ContactService: An instance of the ContactService
    """
    return ContactService(client)


async def create_contact_single_line(
    contact: SingleLineContactCreateRequest,
    contact_service: ContactService = Depends(get_contact_service),
) -> ContactResponse:
    """
    Create a new contact in PostGrid with a single-line address.

    - **first_name**: Contact's first name (required if company_name not provided)
    - **last_name**: Contact's last name
    - **company_name**: Company name (required if first_name not provided)
    - **email**: Contact's email address
    - **phone_number**: Contact's phone number
    - **job_title**: Contact's job title
    - **address_line1**: Complete address in a single line (required)
    - **country_code**: ISO country code (default: "CA")
    - **description**: Description of the contact
    - **metadata**: Optional metadata
    - **skip_verification**: Skip address verification (default: False)
    - **force_verified_status**: Force verified status (default: False)
    - **secret**: Mark as secret contact (default: False)
    """
    try:
        # Convert Pydantic model to dict and remove None values
        contact_dict = contact.dict(exclude_none=True, by_alias=True)

        # Use the contact service to create the contact
        return await contact_service.create_single_line_contact(contact_dict)

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