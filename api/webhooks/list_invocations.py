"""List webhook invocations with pagination."""
from __future__ import annotations

from typing import Any

from app.core.third_party_integrations.postgrid._base import ListResponse
from app.core.third_party_integrations.postgrid.client import PostGridClient

from ._exceptions import WebhookError
from ._responses import WebhookInvocationResponse


class WebhookInvocationListResponse(ListResponse[WebhookInvocationResponse]):
    """Response model for listing webhook invocations."""


async def list_webhook_invocations(
    client: PostGridClient,
    webhook_id: str,
    limit: int = 10,
    skip: int = 0,
) -> WebhookInvocationListResponse:
    """
    List invocations for a specific webhook.

    Args:
        client: Authenticated PostGrid client
        webhook_id: ID of the webhook to list invocations for
        limit: Maximum number of invocations to return (1-100)
        skip: Number of invocations to skip for pagination

    Returns:
        WebhookInvocationListResponse: List of webhook invocations

    Raises:
        WebhookError: If the webhook ID is invalid or API request fails
    """
    if not webhook_id or not webhook_id.startswith("webhook_"):
        raise WebhookError("Invalid webhook ID format. Must start with 'webhook_'")

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
            f"/webhooks/{webhook_id}/invocations",
            params=params,
        )

        if response.status_code == 200:
            return WebhookInvocationListResponse(**response.json())

        raise WebhookError(f"Failed to list webhook invocations: {response.text}")

    except Exception as e:
        raise WebhookError(f"Failed to list webhook invocations: {str(e)}") from e