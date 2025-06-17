"""
Core functionality for listing postcards with pagination and search.
"""

from typing import Optional
import httpx

from ...client import PostGridClient
from ._exceptions import PostcardError
from ._responses import PostcardResponse, PostcardListResponse


async def list_postcards(
    client: PostGridClient,
    *,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None
) -> PostcardListResponse:
    """
    List postcards with optional pagination and search.

    Args:
        client: Authenticated PostGrid client
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return (1-100)
        search: Optional search term to filter postcards

    Returns:
        PostcardListResponse: Paginated list of postcards containing:
            - data: List[PostcardResponse] - The list of postcard objects
            - limit: int - The number of items per page
            - skip: int - The number of items skipped
            - totalCount: int - Total number of items available
            - object: str - Always "list"

    Raises:
        PostcardError: If there's an error listing postcards
        ValueError: If pagination parameters are invalid
    """
    if skip < 0:
        raise ValueError("skip must be >= 0")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")

    params = {
        "skip": str(skip),
        "limit": str(limit)
    }
    if search:
        params["search"] = search

    try:
        async with client:
            # Get raw response from API
            response = await client.get(
                "/postcards",
                params=params
            )
            
            # Ensure the response has the expected structure
            if not isinstance(response, dict) or "data" not in response:
                raise PostcardError("Invalid response format from PostGrid API")
            
            # Parse each postcard in the data array
            postcards = [PostcardResponse(**item) for item in response.get("data", [])]
            
            # Create the response object
            return PostcardListResponse(
                data=postcards,
                limit=response.get("limit", limit),
                skip=response.get("skip", skip),
                totalCount=response.get("totalCount", len(postcards)),
                object=response.get("object", "list")
            )

    except httpx.HTTPStatusError as e:
        error_detail = e.response.json().get('error', {}).get('message', str(e))
        raise PostcardError(
            f"Error listing postcards: {error_detail}"
        ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e