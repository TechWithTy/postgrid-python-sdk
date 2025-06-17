class WebhookError(Exception):
    """Base exception for webhook-related errors."""
    pass

class WebhookNotFoundError(WebhookError):
    """Raised when a webhook is not found."""
    pass

class WebhookValidationError(WebhookError):
    """Raised when webhook validation fails."""
    pass

class WebhookInvocationError(WebhookError):
    """Raised when there's an error with webhook invocations."""
    pass