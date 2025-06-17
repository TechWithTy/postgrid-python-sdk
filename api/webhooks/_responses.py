import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from app.core.third_party_integrations.postgrid.api.webhooks._enums import (
    ObjectType,
    WebhookEventType,
)

from ..._base import BaseResponse, ListResponse


class CreateWebhookRequest(BaseModel):
    """Request model for creating a webhook."""
    url: HttpUrl = Field(..., description="The URL where webhook events will be sent")
    event_types: list[WebhookEventType] = Field(
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
    event_types: Optional[list[WebhookEventType]] = Field(
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
    


class WebhookResponse(BaseResponse):
    """Response model for webhook operations."""
    url: HttpUrl
    event_types: list[WebhookEventType]
    enabled: bool = True
    secret: str | None = None
    object: str = ObjectType.WEBHOOK

    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class WebhookListResponse(ListResponse[WebhookResponse]):
    """Response model for listing webhooks."""


class WebhookInvocationResponse(BaseResponse):
    """Response model for webhook invocations."""
    status_code: int = Field(alias="statusCode")
    type: str
    webhook: str
    object: str = ObjectType.WEBHOOK_INVOCATION


class WebhookInvocationListResponse(ListResponse[WebhookInvocationResponse]):
    """Response model for listing webhook invocations."""
