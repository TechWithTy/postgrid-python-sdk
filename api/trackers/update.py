# update.py
from typing import Any, Dict, Optional
from ..client import PostGridClient
from ._exceptions import PostGridTrackerNotFoundError, PostGridAPIError
from ._requests import TrackerUpdateRequest
from ._responses import TrackerResponse

async def update_tracker(
    client: PostGridClient,
    tracker_id: str,
    data: TrackerUpdateRequest
) -> TrackerResponse:
    """
    Update a tracker in PostGrid.
    
    Args:
        client: Authenticated PostGrid client
        tracker_id: ID of the tracker to update
        data: Tracker update data
        
    Returns:
        TrackerResponse: The updated tracker
        
    Raises:
        PostGridTrackerNotFoundError: If the tracker is not found
        PostGridAPIError: If there's an error with the API request
    """
    try:
        response = await client.patch(
            f"/print-mail/v1/trackers/{tracker_id}",
            json=data.dict(exclude_none=True)
        )
        response.raise_for_status()
        return TrackerResponse.parse_obj(response.json())
    except Exception as e:
        if hasattr(e, "status_code") and e.status_code == 404:
            raise PostGridTrackerNotFoundError(f"Tracker {tracker_id} not found")
        raise PostGridAPIError(
            status_code=getattr(e, "status_code", 500),
            detail=str(e)
        )