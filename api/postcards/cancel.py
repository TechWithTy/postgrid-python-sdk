"""
Core functionality for canceling a postcard in the PostGrid API.
"""

import httpx

from ...client import PostGridClient
from ._exceptions import PostcardError, PostcardNotFoundError
from ._responses import PostcardResponse


async def cancel_postcard(
    client: PostGridClient,
    postcard_id: str
) -> PostcardResponse:
    """
    Cancel a postcard by its ID.

    Args:
        client: Authenticated PostGrid client
        postcard_id: The ID of the postcard to cancel (starts with 'postcard_')

    Returns:
        PostcardResponse: The canceled postcard with updated status

    Raises:
        PostcardNotFoundError: If the postcard is not found
        PostcardError: For other API errors
        ValueError: If postcard_id is invalid
    """
    if not postcard_id.startswith('postcard_'):
        raise ValueError("postcard_id must start with 'postcard_'")

    try:
        async with client:
            response = await client.delete(f"/postcards/{postcard_id}")
            return PostcardResponse(**response)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise PostcardNotFoundError(f"Postcard {postcard_id} not found")
        else:
            error_detail = e.response.json().get('error', {}).get('message', str(e))
            raise PostcardError(
                f"Error canceling postcard: {error_detail}"
            ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e