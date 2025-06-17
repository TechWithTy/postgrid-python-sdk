"""Get webhook by ID."""
from __future__ import annotations

from app.core.third_party_integrations.postgrid.api.webhooks._exceptions import (
    WebhookError,
    WebhookNotFoundError,
)
from app.core.third_party_integrations.postgrid.api.webhooks._responses import WebhookResponse
from app.core.third_party_integrations.postgrid.client import PostGridClient


async def get_webhook(
    client: PostGridClient,
    webhook_id: str,
) -> WebhookResponse:
    """
    Retrieve a webhook by its ID.

    Args:
        client: Authenticated PostGrid client
        webhook_id: The ID of the webhook to retrieve

    Returns:
        WebhookResponse: The retrieved webhook details

    Raises:
        WebhookNotFoundError: If the webhook is not found
        WebhookError: If the API request fails
    """
    if not webhook_id or not webhook_id.startswith("webhook_"):
        raise WebhookError("Invalid webhook ID format")

    try:
        response = await client.get(f"/webhooks/{webhook_id}")

        if response.status_code == 404:
            raise WebhookNotFoundError(f"Webhook {webhook_id} not found")

        response.raise_for_status()
        return WebhookResponse(**response.json())

    except WebhookNotFoundError:
        raise
    except Exception as e:
        raise WebhookError(f"Failed to retrieve webhook: {str(e)}") from e