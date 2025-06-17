# list.py
from typing import List, Optional
from ..client import PostGridClient
from ._enums import SortBy, SortOrder
from ._exceptions import PostGridAPIError
from ._responses import ListResponse, TrackerResponse

async def list_trackers(
    client: PostGridClient,
    limit: int = 10,
    skip: int = 0,
    sort_by: Optional[SortBy] = None,
    sort_order: SortOrder = SortOrder.DESC
) -> ListResponse[TrackerResponse]:
    """
    List trackers with pagination and sorting.
    
    Args:
        client: Authenticated PostGrid client
        limit: Maximum number of trackers to return (1-100)
        skip: Number of trackers to skip for pagination
        sort_by: Field to sort by
        sort_order: Sort order (asc/desc)
        
    Returns:
        ListResponse[TrackerResponse]: Paginated list of trackers
        
    Raises:
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
            "/print-mail/v1/trackers",
            params=params
        )
        response.raise_for_status()
        return ListResponse[TrackerResponse].parse_obj(response.json())
    except Exception as e:
        if hasattr(e, "status_code") and e.status_code == 404:
            # Return empty list for 404 (no trackers found)
            return ListResponse[TrackerResponse](
                object="list",
                limit=limit,
                skip=skip,
                total_count=0,
                data=[]
            )
        raise PostGridAPIError(
            status_code=getattr(e, "status_code", 500),
            detail=str(e)
        )