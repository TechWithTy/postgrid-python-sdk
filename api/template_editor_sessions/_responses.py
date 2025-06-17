from datetime import datetime
from pydantic import  Field
from typing import Optional, List, Dict, Any
from .._base import BaseResponse

class TemplateEditorSessionResponse(BaseResponse):
    """Response model for a template editor session."""
    id: str = Field(..., description="Unique identifier for the session")
    object: str = Field("template_editor_session", description="Type of object")
    url: str = Field(..., description="URL to access the template editor session")
    expires_at: datetime = Field(..., description="When the session will expire")
    status: str = Field(..., description="Status of the session")
    metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Set of key-value pairs for storing additional data"
    )

class DeleteTemplateEditorSessionResponse(BaseResponse):
    """Response model for deleting a template editor session."""
    id: str = Field(..., description="ID of the deleted session")
    object: str = Field("template_editor_session", description="Type of object")
    deleted: bool = Field(..., description="Whether the session was deleted")

class ListTemplateEditorSessionsResponse(BaseResponse):
    """Response model for listing template editor sessions."""
    data: List[TemplateEditorSessionResponse] = Field(
        default_factory=list,
        description="List of template editor sessions"
    )
    count: int = Field(0, description="Total number of sessions")