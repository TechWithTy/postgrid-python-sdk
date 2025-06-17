"""Delete webhook functionality for PostGrid API."""
from __future__ import annotations

from pydantic import BaseModel, Field

from app.core.third_party_integrations.postgrid.api.webhooks._exceptions import (
    WebhookError,
    WebhookNotFoundError,
    WebhookValidationError,
)
from app.core.third_party_integrations.postgrid.client import PostGridClient


class DeleteWebhookResponse(BaseModel):
    """Response model for webhook deletion.

    Attributes:
        id: The ID of the deleted webhook
        object: The type of object (always "webhook")
        deleted: Whether the webhook was successfully deleted
    """
    id: str = Field(..., description="The ID of the deleted webhook")
    object: str = Field("webhook", description="The type of object")
    deleted: bool = Field(..., description="Whether the webhook was deleted")


async def delete_webhook(
    client: PostGridClient,
    webhook_id: str,
) -> DeleteWebhookResponse:
    """Delete a webhook in PostGrid.

    Args:
        client: Authenticated PostGrid client instance
        webhook_id: The ID of the webhook to delete (must start with 'webhook_')

    Returns:
        DeleteWebhookResponse: Confirmation of the deletion

    Raises:
        WebhookValidationError: If webhook ID format is invalid
        WebhookNotFoundError: If the webhook doesn't exist
        WebhookError: If the API request fails

    Example:
        ```python
        response = await delete_webhook(
            client=postgrid_client,
            webhook_id="webhook_123"
        )
        print(f"Deleted webhook: {response.id}")
        ```
    """
    if not webhook_id or not webhook_id.startswith("webhook_"):
        raise WebhookValidationError("Invalid webhook ID format")

    try:
        response = await client.delete(f"/webhooks/{webhook_id}")

        if response.status_code == 404:
            raise WebhookNotFoundError(f"Webhook {webhook_id} not found")

        response.raise_for_status()

        return DeleteWebhookResponse(**response.json())

    except WebhookNotFoundError:
        raise
    except Exception as e:
        raise WebhookError(f"Failed to delete webhook: {str(e)}") from e
