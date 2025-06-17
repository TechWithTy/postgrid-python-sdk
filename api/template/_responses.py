"""
Pydantic response models for PostGrid Template API.

This module defines the response schemas for template operations
in the PostGrid API.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator

from ._enums import TemplateObjectType


class TemplateBaseResponse(BaseModel):
    """Base response model for template operations."""
    id: str = Field(..., description="Unique identifier for the template")
    object: str = Field(..., description="Type of the object")
    live: bool = Field(..., description="Whether the template is in live mode")
    description: Optional[str] = Field(None, description="Template description")
    html: Optional[str] = Field(None, description="HTML content of the template")
    created_at: Optional[datetime] = Field(None, alias="createdAt", description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt", description="Last update timestamp")
    
    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def parse_dates(cls, value: str | None) -> datetime | None:
        """Parse datetime strings into datetime objects."""
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    
    model_config = {
        "populate_by_name": True,
        "extra": "ignore"
    }


class TemplateUpdateResponse(TemplateBaseResponse):
    """Response model for template update operations."""
    pass


class TemplateListResponse(BaseModel):
    """Response model for listing templates with pagination."""
    data: list[TemplateBaseResponse] = Field(..., description="List of templates")
    object: str = Field("list", description="Type of object, always 'list'")
    count: int = Field(..., description="Total number of templates")
    limit: int = Field(..., description="Number of templates per page")
    skip: int = Field(..., description="Number of templates skipped")
    total_count: int = Field(..., alias="totalCount", description="Total number of templates available")


class TemplateDeleteResponse(BaseModel):
    """Response model for template delete operations."""
    id: str = Field(..., description="ID of the deleted template")
    object: str = Field(..., description="Type of the object")
    deleted: bool = Field(..., description="Whether the deletion was successful")
    
    model_config = {
        "populate_by_name": True,
        "extra": "ignore"
    }