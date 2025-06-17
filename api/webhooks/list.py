"""List webhooks with pagination."""
from __future__ import annotations

from typing import Any

from app.core.third_party_integrations.postgrid._base import ListResponse
from app.core.third_party_integrations.postgrid.client import PostGridClient
from app.core.third_party_integrations.postgrid.api.webhooks._exceptions import WebhookError
from app.core.third_party_integrations.postgrid.api.webhooks._responses import WebhookResponse

class WebhookListResponse(ListResponse[WebhookResponse]):
    """Response model for listing webhooks."""


async def list_webhooks(
    client: PostGridClient,
    limit: int = 10,
    skip: int = 0,
) -> WebhookListResponse:
    """
    List all webhooks with pagination.

    Args:
        client: Authenticated PostGrid client
        limit: Maximum number of webhooks to return (default: 10, max: 100)
        skip: Number of webhooks to skip for pagination (default: 0)

    Returns:
        WebhookListResponse: Paginated list of webhooks

    Raises:
        WebhookError: If the API request fails
    """
    try:
        # Ensure limit is within bounds
        if limit is None or limit < 1 or limit > 100:
            limit = 10
        # Ensure skip is not negative
        if skip is None or skip < 0:
            skip = 0

        params: dict[str, Any] = {
            "limit": limit,
            "skip": skip,
        }

        response = await client.get(
            "/webhooks",
            params=params,
        )

        response.raise_for_status()
        return WebhookListResponse(**response.json())

    except Exception as e:
        raise WebhookError(f"Failed to list webhooks: {str(e)}") from e