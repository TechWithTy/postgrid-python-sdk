"""
Core functionality for progressing a test postcard to the next status in PostGrid.
"""


import httpx

from ...client import PostGridClient
from ._exceptions import InvalidProgressionError, PostcardError, PostcardNotFoundError
from ._responses import PostcardResponse


async def progress_test_postcard(
    client: PostGridClient,
    postcard_id: str
) -> PostcardResponse:
    """
    Progress a test postcard to the next status in its lifecycle.

    Args:
        client: Authenticated PostGrid client
        postcard_id: ID of the postcard to progress (starts with 'postcard_')

    Returns:
        PostcardResponse: The updated postcard with new status

    Raises:
        PostcardNotFoundError: If the postcard is not found
        InvalidProgressionError: If the postcard cannot be progressed
        PostcardError: For other API errors
        ValueError: If postcard_id is invalid
    """
    if not postcard_id.startswith('postcard_'):
        raise ValueError("postcard_id must start with 'postcard_'")

    try:
        async with client:
            response = await client.post(
                f"/postcards/{postcard_id}/progressions"
            )
            # Parse the response using the PostcardResponse model
            return PostcardResponse(**response)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise PostcardNotFoundError(f"Postcard {postcard_id} not found")
        elif e.response.status_code == 400 and "invalid_progression" in str(e.response.text).lower():
            raise InvalidProgressionError(
                "Cannot progress postcard - it may already be completed or cancelled"
            )
        else:
            error_detail = e.response.json().get('error', {}).get('message', str(e))
            raise PostcardError(
                f"Error progressing postcard: {error_detail}"
            ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e