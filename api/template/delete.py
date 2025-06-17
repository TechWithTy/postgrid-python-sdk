"""
Template deletion endpoint for PostGrid API.

This module provides an API endpoint for deleting templates in PostGrid.
It handles template deletion with proper validation, error handling, and response formatting.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status

from ...client import PostGridClient
from ._exceptions import (
    TemplateDeleteError,
    TemplateError,
    TemplateNotFoundError,
)
from ._responses import TemplateDeleteResponse

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



async def delete_template(
    template_id: str,
    client: PostGridClient = Depends(get_client)
) -> TemplateDeleteResponse:
    """
    Delete a template from PostGrid.
    
    Args:
        template_id: The ID of the template to delete
        client: The PostGrid client instance
        
    Returns:
        TemplateDeleteResponse: Confirmation of the deletion
        
    Raises:
        HTTPException: If there's an error deleting the template
    """
    try:
        # Make the API request to delete the template
        response = await client.delete(f"print-mail/v1/templates/{template_id}")
        
        # Handle 404 Not Found
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise TemplateNotFoundError(template_id=template_id)
            
        # Handle other error status codes
        response.raise_for_status()
        
        # Parse and return the response
        return TemplateDeleteResponse(**response.json())
        
    except TemplateNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        ) from e
    except Exception as e:
        # Log the error and return a 500 response
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        ) from e


