# list_visits.py
from typing import List, Optional
from ..client import PostGridClient
from ._enums import SortBy, SortOrder
from ._exceptions import PostGridTrackerNotFoundError, PostGridAPIError
from ._responses import ListResponse, TrackerVisitResponse

async def list_tracker_visits(
    client: PostGridClient,
    tracker_id: str,
    limit: int = 10,
    skip: int = 0,
    sort_by: Optional[SortBy] = None,
    sort_order: SortOrder = SortOrder.DESC
) -> ListResponse[TrackerVisitResponse]:
    """
    List visits for a specific tracker.
    
    Args:
        client: Authenticated PostGrid client
        tracker_id: ID of the tracker to get visits for
        limit: Maximum number of visits to return (1-100)
        skip: Number of visits to skip for pagination
        sort_by: Field to sort by
        sort_order: Sort order (asc/desc)
        
    Returns:
        ListResponse[TrackerVisitResponse]: Paginated list of tracker visits
        
    Raises:
        PostGridTrackerNotFoundError: If the tracker is not found
        PostGridAPIError: If there's an error with the API request
    """
    params = {
        "limit": limit,
        "skip": skip,
        "sortOrder": sort_order.value
    }
    if sort_by:
        params["sortBy"] = sort_by.value

    try:
        response = await client.get(
            f"/print-mail/v1/trackers/{tracker_id}/visits",
            params=params
        )
        response.raise_for_status()
        return ListResponse[TrackerVisitResponse].parse_obj(response.json())
    except Exception as e:
        if hasattr(e, "status_code"):
            if e.status_code == 404:
                raise PostGridTrackerNotFoundError(f"Tracker {tracker_id} not found")
        raise PostGridAPIError(
            status_code=getattr(e, "status_code", 500),
            detail=str(e)
        )