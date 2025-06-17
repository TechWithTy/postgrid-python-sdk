from enum import StrEnum

class WebhookEventType(StrEnum):
    """Types of events that can trigger webhooks."""
    POSTCARD_CREATED = "postcard.created"
    POSTCARD_UPDATED = "postcard.updated"
    POSTCARD_DELETED = "postcard.deleted"
    # Add other event types as needed

class WebhookStatus(StrEnum):
    """Status of a webhook."""
    ACTIVE = "active"
    INACTIVE = "inactive"

class ObjectType(StrEnum):
    """Object types in the API."""
    WEBHOOK = "webhook"
    WEBHOOK_INVOCATION = "webhook_invocation"