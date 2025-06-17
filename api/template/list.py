"""
Template listing endpoint for PostGrid API.

This module provides an API endpoint for listing templates in PostGrid.
It handles template listing with proper pagination, filtering, and error handling.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, Query, status

from ...client import PostGridClient
from ._exceptions import TemplateListError
from ._responses import TemplateListResponse

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

router = APIRouter(prefix="/templates", tags=["templates"])


@router.get(
    "",
    response_model=TemplateListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Templates",
    description="List all templates with optional filtering and pagination.",
)
async def list_templates(
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of templates to return",
    ),
    skip: int = Query(
        default=0,
        ge=0,
        description="Number of templates to skip for pagination",
    ),
    search: str | None = Query(
        default=None,
        description="Search term to filter templates by name or description",
    ),
    client: PostGridClient = Depends(get_client),
) -> TemplateListResponse:
    """
    List templates with optional filtering and pagination.

    Args:
        limit: Maximum number of templates to return (1-100)
        skip: Number of templates to skip for pagination
        search: Optional search term to filter templates
        client: The PostGrid client instance

    Returns:
        TemplateListResponse: List of templates matching the criteria

    Raises:
        HTTPException: If there's an error listing the templates
    """
    try:
        # Build query parameters
        params = {"limit": limit, "skip": skip}
        if search:
            params["search"] = search

        # Make the API request to list templates
        response = await client.get(
            "print-mail/v1/templates",
            params=params
        )

        # Handle error status codes
        response.raise_for_status()

        # Parse and return the response
        return TemplateListResponse(**response.json())

    except TemplateListError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) from e
    except Exception as e:
        # Log the error and return a 500 response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e
