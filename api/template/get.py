"""
Template retrieval endpoint for PostGrid API.

This module provides an API endpoint for retrieving a single template by ID
from PostGrid. It handles template retrieval with proper error handling.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, status

from ...client import PostGridClient
from ._exceptions import TemplateNotFoundError
from ._responses import TemplateBaseResponse

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
        pass

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get(
    "/{template_id}",
    response_model=TemplateBaseResponse,
    status_code=status.HTTP_200_OK,
    summary="Get a template by ID",
    description="Retrieves a template by its unique identifier.",
    responses={
        200: {"description": "Template retrieved successfully"},
        400: {"description": "Invalid template ID format"},
        404: {"description": "Template not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_template(
    template_id: Annotated[
        str,
        Path(
            ...,
            description="The unique identifier of the template to retrieve",
            example="template_c6HSqnsD1h2zoeHJ6Z9EEA",
            regex=r"^template_[a-zA-Z0-9]+",
        ),
    ],
    client: PostGridClient = Depends(get_client),
) -> TemplateBaseResponse:
    """
    Retrieve a template by its ID.

    Args:
        template_id: The unique identifier of the template to retrieve
        client: The PostGrid client instance

    Returns:
        TemplateBaseResponse: The requested template

    Raises:
        HTTPException: If the template is not found or another error occurs
    """
    try:
        # Make the API call to retrieve the template
        response = await client.get(f"templates/{template_id}")
        
        # The response should already be validated by the client
        return response
        
    except TemplateNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except Exception as e:
        # Handle other potential errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving the template: {str(e)}",
        ) from e