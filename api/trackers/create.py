# create.py
from typing import Any, Dict, Optional
from ..client import PostGridClient
from ._exceptions import PostGridTrackerError, PostGridAPIError
from ._requests import TrackerCreateRequest
from ._responses import TrackerResponse

async def create_tracker(
    client: PostGridClient,
    data: TrackerCreateRequest
) -> TrackerResponse:
    """
    Create a new tracker in PostGrid.
    
    Args:
        client: Authenticated PostGrid client
        data: Tracker creation data
        
    Returns:
        TrackerResponse: The created tracker
        
    Raises:
        PostGridAPIError: If there's an error with the API request
    """
    try:
        response = await client.post(
            "/print-mail/v1/trackers",
            json=data.dict(exclude_none=True)
        )
        response.raise_for_status()
        return TrackerResponse.parse_obj(response.json())
    except Exception as e:
        raise PostGridAPIError(
            status_code=getattr(e, "status_code", 500),
            detail=str(e)
        )