from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional
from ._enums import WebhookEventType

class CreateWebhookRequest(BaseModel):
    """Request model for creating a webhook."""
    url: HttpUrl = Field(..., description="The URL where webhook events will be sent")
    event_types: List[WebhookEventType] = Field(
        ...,
        description="List of event types to subscribe to",
        min_items=1
    )
    enabled: bool = Field(
        default=True,
        description="Whether the webhook is active"
    )
    secret: Optional[str] = Field(
        None,
        description="Optional secret for signing webhook payloads",
        min_length=16,
        max_length=100
    )

class UpdateWebhookRequest(BaseModel):
    """Request model for updating a webhook."""
    url: Optional[HttpUrl] = Field(None, description="The new webhook URL")
    event_types: Optional[List[WebhookEventType]] = Field(
        None,
        description="New list of event types to subscribe to"
    )
    enabled: Optional[bool] = Field(
        None,
        description="Whether the webhook is active"
    )
    secret: Optional[str] = Field(
        None,
        description="New secret for signing webhook payloads",
        min_length=16,
        max_length=100
    )