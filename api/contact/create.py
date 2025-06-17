"""
Contact creation endpoint for PostGrid API.

This module provides an API endpoint for creating and managing contacts in PostGrid.
It handles contact creation with proper validation, error handling, and response formatting.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status

from ...client import PostGridClient
from ._exceptions import (
    APIError,
    AuthenticationError,
    PostGridAPIError,
    PostGridAPIException,
    RateLimitError,
    ValidationError,
)
from ._requests import ContactCreateRequest
from ._responses import ContactResponse

# Initialize the PostGrid client
_client = PostGridClient()


async def get_client() -> AsyncGenerator[PostGridClient, None]:
    """Dependency that yields a PostGrid client instance.

    Yields:
        PostGridClient: An instance of the PostGrid client
    """
    try:
        yield _client
    finally:
        # Cleanup if needed when the request is done
        await _client.close()

router = APIRouter(prefix="/contacts", tags=["contacts"])


async def create_contact(
    contact: ContactCreateRequest = Depends(),
    client: PostGridClient = Depends(get_client)
) -> ContactResponse:
    """
    Create a new contact in PostGrid.
    
    - **first_name**: Contact's first name (required if company_name not provided)
    - **last_name**: Contact's last name
    - **company_name**: Company name (required if first_name not provided)
    - **email**: Contact's email address
    - **phone_number**: Contact's phone number
    - **job_title**: Contact's job title
    - **address_line1**: First line of the address (required)
    - **address_line2**: Second line of the address
    - **city**: City
    - **province_or_state**: Province or state
    - **postal_or_zip**: Postal or ZIP code
    - **country_code**: ISO country code (default: "CA")
    - **description**: Description of the contact
    - **metadata**: Optional metadata
    - **skip_verification**: Skip address verification (default: False)
    - **force_verified_status**: Force verified status (default: False)
    """
    try:
        # Convert Pydantic model to dict and remove None values
        contact_dict = contact.dict(exclude_none=True, by_alias=True)
        
        # Make API request with form-encoded data
        response = await client.post(
            "/print-mail/v1/contacts",
            data=contact_dict,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Handle the response
        if response.status_code == 201:
            return ContactResponse(**response.json())
        elif response.status_code == 400:
            error_data = response.json()
            raise ValidationError(
                status_code=400,
                error=PostGridAPIError(
                    type="validation_error",
                    message=error_data.get("message", "Validation failed"),
                    details=error_data.get("errors"),
                )
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                status_code=401,
                error=PostGridAPIError(
                    type="authentication_error",
                    message="Invalid API key",
                )
            )
        elif response.status_code == 429:
            raise RateLimitError(
                status_code=429,
                error=PostGridAPIError(
                    type="rate_limit_error",
                    message="Rate limit exceeded",
                ),
                headers=dict(response.headers),
            )
        else:
            error_data = response.json()
            raise APIError(
                status_code=response.status_code,
                error=PostGridAPIError(
                    type="api_error",
                    message=error_data.get("message", "An error occurred"),
                    details=error_data,
                )
            )
            
    except PostGridAPIException:
        # Re-raise our custom exceptions
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )