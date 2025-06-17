"""Update webhook functionality for PostGrid API."""
from __future__ import annotations

from typing import Any

from pydantic import HttpUrl

from app.core.third_party_integrations.postgrid._base import BaseResponse
from app.core.third_party_integrations.postgrid.api.webhooks._enums import WebhookEventType
from app.core.third_party_integrations.postgrid.api.webhooks._exceptions import (
    WebhookError,
    WebhookNotFoundError,
    WebhookValidationError,
)
from app.core.third_party_integrations.postgrid.client import PostGridClient


class UpdateWebhookRequest(BaseResponse):
    """Request model for updating a webhook.

    Attributes:
        url: The HTTPS URL where webhook events will be sent
        enabled_events: List of event types to subscribe to
        description: Optional description for the webhook
        metadata: Optional metadata for the webhook
        secret: Optional secret for signing webhook payloads (min 20 chars, no spaces)
    """
    url: HttpUrl | None = None
    enabled_events: list[WebhookEventType] | None = None
    description: str | None = None
    metadata: dict[str, Any] | None = None
    secret: str | None = None
    enabled: bool | None = None

    class Config:
        """Pydantic config."""
        json_encoders = {
            WebhookEventType: lambda v: v.value,
        }


class WebhookResponse(BaseResponse):
    """Response model for webhook operations.

    Attributes:
        id: The unique identifier for the webhook
        url: The URL where webhook events will be sent
        enabled_events: List of event types the webhook is subscribed to
        enabled: Whether the webhook is active
        description: Optional description for the webhook
        metadata: Optional metadata for the webhook
        secret: The secret used to sign webhook payloads
        created_at: When the webhook was created
        updated_at: When the webhook was last updated
    """
    id: str
    url: HttpUrl
    enabled_events: list[WebhookEventType]
    enabled: bool
    description: str | None = None
    metadata: dict[str, Any] | None = None
    secret: str
    created_at: str
    updated_at: str
    live: bool
    object: str = "webhook"

    class Config:
        """Pydantic config."""
        json_encoders = {
            WebhookEventType: lambda v: v.value,
        }


async def update_webhook(
    client: PostGridClient,
    webhook_id: str,
    *,
    url: str | None = None,
    enabled_events: list[WebhookEventType] | None = None,
    description: str | None = None,
    metadata: dict[str, Any] | None = None,
    secret: str | None = None,
    enabled: bool | None = None,
) -> WebhookResponse:
    """Update an existing webhook in PostGrid.

    Args:
        client: Authenticated PostGrid client instance
        webhook_id: The ID of the webhook to update (must start with 'webhook_')
        url: New HTTPS URL for the webhook (optional)
        enabled_events: New list of event types to subscribe to (optional)
        description: New description for the webhook (optional)
        metadata: New metadata for the webhook (optional)
        secret: New secret for signing webhook payloads (min 20 chars, no spaces) (optional)
        enabled: Whether the webhook should be active (optional)

    Returns:
        WebhookResponse: The updated webhook details

    Raises:
        WebhookValidationError: If input validation fails
        WebhookNotFoundError: If the webhook doesn't exist
        WebhookError: If the API request fails
    """
    if not webhook_id or not webhook_id.startswith("webhook_"):
        raise WebhookValidationError("Invalid webhook ID format")

    if secret and (len(secret) < 20 or ' ' in secret):
        raise WebhookValidationError(
            "Secret must be at least 20 characters long and contain no spaces"
        )

    # Prepare the request payload with only provided fields
    payload = {}
    if url is not None:
        payload["url"] = url
    if enabled_events is not None:
        payload["enabledEvents"] = [e.value for e in enabled_events]
    if description is not None:
        payload["description"] = description
    if metadata is not None:
        payload["metadata"] = metadata
    if secret is not None:
        payload["secret"] = secret
    if enabled is not None:
        payload["enabled"] = enabled

    try:
        response = await client.post(f"/webhooks/{webhook_id}", json=payload)

        if response.status_code == 404:
            raise WebhookNotFoundError(f"Webhook {webhook_id} not found")

        response.raise_for_status()
        
        data = response.json()
        # Convert string event types back to enum values
        if "enabledEvents" in data and data["enabledEvents"]:
            data["enabled_events"] = [
                WebhookEventType(event) for event in data.pop("enabledEvents")
            ]

        return WebhookResponse(**data)

    except WebhookNotFoundError:
        raise
    except Exception as e:
        raise WebhookError(f"Failed to update webhook: {str(e)}") from e
