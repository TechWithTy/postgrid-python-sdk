"""
Template creation endpoint for PostGrid API.

This module provides an API endpoint for creating new templates
in PostGrid with proper validation and error handling.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ...client import PostGridClient
from ._exceptions import TemplateCreateError
from ._responses import TemplateBaseResponse

# Initialize the PostGrid client
_client = PostGridClient()


class TemplateCreateRequest(BaseModel):
    """Request model for creating a new template."""
    html: str = Field(
        ...,
        min_length=1,
        description="HTML content for the template. Can include template variables like {{variable}}.",
        example="<b>Hello</b> {{to.firstName}}!",
    )
    description: str | None = Field(
        None,
        max_length=255,
        description="Optional description for the template.",
        example="My first template!",
    )
    metadata: dict[str, Any] | None = Field(
        None,
        description="Optional metadata to store with the template.",
        example={"to": "Jimmy"},
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "html": "<b>Hello</b> {{to.firstName}}!",
                "description": "My first template!",
                "metadata": {"to": "Jimmy"}
            }
        }
    }


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


@router.post(
    "/",
    response_model=TemplateBaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new template",
    description="Creates a new template with the provided HTML content and optional metadata.",
    responses={
        201: {"description": "Template created successfully"},
        400: {"description": "Invalid request data"},
        500: {"description": "Internal server error"},
    },
)
async def create_template(
    template_data: TemplateCreateRequest,
    client: PostGridClient = Depends(get_client),
) -> TemplateBaseResponse:
    """
    Create a new template in PostGrid.

    Args:
        template_data: The template data including HTML content and optional metadata
        client: The PostGrid client instance

    Returns:
        TemplateBaseResponse: The created template data

    Raises:
        HTTPException: If template creation fails
    """
    try:
        # Convert the request model to a dictionary, excluding unset fields
        request_data = template_data.dict(exclude_unset=True)

        # Make the API call to create the template
        response = await client.post(
            "templates",
            json=request_data,
        )

        # The response should already be validated by the client
        return response

    except TemplateCreateError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the template: {str(e)}",
        ) from e