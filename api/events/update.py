"""
Template update endpoint for PostGrid API.

This module provides an API endpoint for updating templates in PostGrid.
It handles template updates with proper validation, error handling, and response formatting.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status

from ...client import PostGridClient
from ._exceptions import TemplateNotFoundError, TemplateUpdateError
from ._requests import TemplateUpdateRequest
from ._responses import TemplateUpdateResponse

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


async def update_template(
    template_id: str,
    template_data: TemplateUpdateRequest,
    client: PostGridClient = Depends(get_client)
) -> TemplateUpdateResponse:
    """
    Update an existing template in PostGrid.
    
    Args:
        template_id: The ID of the template to update
        template_data: The template data to update
        client: The PostGrid client instance
        
    Returns:
        TemplateUpdateResponse: The updated template data
        
    Raises:
        HTTPException: If there's an error updating the template
    """
    try:
        # Convert Pydantic model to dict and remove None values
        update_data = template_data.model_dump(exclude_none=True)
        
        # Make the API request to update the template
        response = await client.put(
            f"print-mail/v1/templates/{template_id}",
            data=update_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Handle 404 Not Found
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise TemplateNotFoundError(template_id=template_id)
            
        # Handle other error status codes
        response.raise_for_status()
        
        # Parse and return the response
        return TemplateUpdateResponse(**response.json())
        
    except TemplateNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except TemplateUpdateError as e:
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


# Register the route
router.patch(
    "/{template_id}",
    response_model=TemplateUpdateResponse,
    status_code=status.HTTP_200_OK,
    summary="Update a template",
    description="Update an existing template with the specified ID.",
    responses={
        200: {"description": "Template updated successfully"},
        400: {"description": "Invalid request data"},
        404: {"description": "Template not found"},
        500: {"description": "Internal server error"}
    }
)(update_template)