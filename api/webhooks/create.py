"""Webhook creation functionality for PostGrid API."""
from __future__ import annotations

from datetime import datetime

from pydantic import HttpUrl

from app.core.third_party_integrations.postgrid._base import BaseResponse
from app.core.third_party_integrations.postgrid.api.webhooks._enums import WebhookEventType
from app.core.third_party_integrations.postgrid.api.webhooks._exceptions import (
    WebhookError,
    WebhookValidationError,
)
from app.core.third_party_integrations.postgrid.api.webhooks._requests import CreateWebhookRequest
from app.core.third_party_integrations.postgrid.client import PostGridClient


class WebhookResponse(BaseResponse):
    """Response model for webhook operations.

    Attributes:
        url: The URL where webhook events will be sent
        event_types: List of event types the webhook is subscribed to
        enabled: Whether the webhook is active
        secret: Optional secret for signing webhook payloads
        created_at: When the webhook was created
        updated_at: When the webhook was last updated
    """
    url: HttpUrl
    event_types: list[WebhookEventType]
    enabled: bool = True
    secret: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

async def create_webhook(
    client: PostGridClient,
    url: str,
    event_types: list[WebhookEventType],
    enabled: bool = True,
    secret: str | None = None,
) -> WebhookResponse:
    """Create a new webhook in PostGrid.

    This function creates a new webhook with the specified configuration. The webhook
    will be called for each event type specified in the event_types list.

    Example:
        ```python
        webhook = await create_webhook(
            client=postgrid_client,
            url="https://example.com/webhooks/postgrid",
            event_types=[WebhookEventType.LETTER_CREATED],
            secret="your-secret-key"
        )
        ```

    Args:
        client: Authenticated PostGrid client instance
        url: The URL where webhook events will be sent (must be HTTPS)
        event_types: List of event types to subscribe to (must not be empty)
        enabled: Whether the webhook should be active (default: True)
        secret: Optional secret for signing webhook payloads (16-100 chars)

    Returns:
        WebhookResponse: The created webhook details

    Raises:
        WebhookValidationError: If input validation fails (e.g., invalid URL format)
        WebhookError: If the API request fails or returns an invalid response
    """
    try:
        # Validate input using Pydantic model
        request = CreateWebhookRequest(
            url=url,
            event_types=event_types,
            enabled=enabled,
            secret=secret,
        )
        
        response = await client.post(
            "/webhooks",
            json=request.dict(exclude_none=True),
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        if not response_data.get("id", "").startswith("webhook_"):
            raise WebhookError("Invalid webhook ID in response")
            
        return WebhookResponse(**response_data)

    except WebhookValidationError:
        raise
    except Exception as e:
        raise WebhookError(f"Failed to create webhook: {str(e)}") from e