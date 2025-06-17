"""
Core functionality for retrieving a specific postcard by ID.
"""

from typing import Optional
import httpx

from ...client import PostGridClient
from ._exceptions import PostcardError, PostcardNotFoundError
from ._responses import PostcardResponse


async def get_postcard(
    client: PostGridClient,
    postcard_id: str,
    *,
    expand: Optional[list[str]] = None
) -> PostcardResponse:
    """
    Get a specific postcard by its ID.

    Args:
        client: Authenticated PostGrid client
        postcard_id: The ID of the postcard to retrieve (starts with 'postcard_')
        expand: Optional list of fields to expand in the response.
                Valid values: 'frontTemplate', 'backTemplate'

    Returns:
        PostcardResponse: The requested postcard

    Raises:
        PostcardNotFoundError: If the postcard is not found
        PostcardError: For other API errors
        ValueError: If postcard_id is invalid
    """
    if not postcard_id.startswith('postcard_'):
        raise ValueError("postcard_id must start with 'postcard_'")

    # Prepare query parameters
    params = {}
    if expand:
        valid_expansions = {'frontTemplate', 'backTemplate'}
        invalid = set(expand) - valid_expansions
        if invalid:
            raise ValueError(f"Invalid expand values: {', '.join(invalid)}. "
                           "Must be one of: frontTemplate, backTemplate")
        params = {"expand[]": list(expand)}

    try:
        async with client:
            response = await client.get(
                f"/postcards/{postcard_id}",
                params=params
            )
            return PostcardResponse(**response)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise PostcardNotFoundError(f"Postcard {postcard_id} not found")
        else:
            error_detail = e.response.json().get('error', {}).get('message', str(e))
            raise PostcardError(
                f"Error retrieving postcard: {error_detail}"
            ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e