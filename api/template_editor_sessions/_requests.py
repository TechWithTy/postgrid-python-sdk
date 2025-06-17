from typing import Any

from pydantic import BaseModel, Field

class BaseTemplateEditorSessionRequest(BaseModel):
    """Base request model for template editor sessions."""
    metadata: dict[str, Any] | None = Field(
        None,
        description="Set of key-value pairs for storing additional data"
    )

class CreateTemplateEditorSessionRequest(BaseTemplateEditorSessionRequest):
    """Request model for creating a template editor session."""
    pass  # No specific fields needed for creation based on docs