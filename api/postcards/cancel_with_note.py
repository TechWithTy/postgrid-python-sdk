"""
Core functionality for canceling a postcard with a note in the PostGrid API.
"""

import httpx
from pydantic import BaseModel, Field

from ...client import PostGridClient
from ._exceptions import PostcardError, PostcardNotFoundError
from ._responses import PostcardResponse


class CancelPostcardRequest(BaseModel):
    """Request model for canceling a postcard with a note."""
    note: str = Field(
        ...,
        description="A note explaining the reason for cancellation",
        min_length=1,
        max_length=1000,
        example="Cancelled due to template changes"
    )


async def cancel_postcard_with_note(
    client: PostGridClient,
    postcard_id: str,
    note: str
) -> PostcardResponse:
    """
    Cancel a postcard by its ID with a note explaining the reason.

    Args:
        client: Authenticated PostGrid client
        postcard_id: The ID of the postcard to cancel (starts with 'postcard_')
        note: A note explaining the reason for cancellation

    Returns:
        PostcardResponse: The canceled postcard with updated status and cancellation details

    Raises:
        PostcardNotFoundError: If the postcard is not found
        PostcardError: For other API errors
        ValueError: If postcard_id is invalid or note is empty
    """
    if not postcard_id.startswith('postcard_'):
        raise ValueError("postcard_id must start with 'postcard_'")
    if not note.strip():
        raise ValueError("Note cannot be empty")

    # Validate the request using Pydantic model
    request_data = CancelPostcardRequest(note=note)

    try:
        async with client:
            response = await client.post(
                f"/postcards/{postcard_id}/cancellation",
                json=request_data.model_dump()
            )
            return PostcardResponse(**response)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise PostcardNotFoundError(f"Postcard {postcard_id} not found")
        elif e.response.status_code == 400:
            error_detail = e.response.json().get('error', {}).get('message', 'Invalid request')
            raise PostcardError(f"Validation error: {error_detail}") from e
        else:
            error_detail = e.response.json().get('error', {}).get('message', str(e))
            raise PostcardError(
                f"Error canceling postcard with note: {error_detail}"
            ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e