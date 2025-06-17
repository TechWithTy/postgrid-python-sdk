# get.py
from typing import Optional
from ..client import PostGridClient
from ._exceptions import PostGridTrackerNotFoundError, PostGridAPIError
from ._responses import TrackerResponse

async def get_tracker(
    client: PostGridClient,
    tracker_id: str
) -> TrackerResponse:
    """
    Get a tracker by ID from PostGrid.
    
    Args:
        client: Authenticated PostGrid client
        tracker_id: ID of the tracker to retrieve
        
    Returns:
        TrackerResponse: The requested tracker
        
    Raises:
        PostGridTrackerNotFoundError: If the tracker is not found
        PostGridAPIError: If there's an error with the API request
    """
    try:
        response = await client.get(f"/print-mail/v1/trackers/{tracker_id}")
        response.raise_for_status()
        return TrackerResponse.parse_obj(response.json())
    except Exception as e:
        if hasattr(e, "status_code") and e.status_code == 404:
            raise PostGridTrackerNotFoundError(f"Tracker {tracker_id} not found")
        raise PostGridAPIError(
            status_code=getattr(e, "status_code", 500),
            detail=str(e)
        )